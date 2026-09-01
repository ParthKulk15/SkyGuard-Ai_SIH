import json
import math
import sys
from pathlib import Path

sys.path.insert(0, ".")

import numpy as np
import pandas as pd

from src.anomaly_detection.autoencoder import SkyGuardAutoencoder
from src.anomaly_detection.baseline import RuleBaselineDetector
from src.anomaly_detection.fault_classifier import SkyGuardFaultClassifier
from src.anomaly_detection.isolation_forest import SkyGuardIsolationForest
from src.evaluation.metrics import compute_binary_metrics
from src.features.feature_engineering import generate_engineed_features
from src.preprocessing.cleaner import DataCleaner, FEATURE_COLUMNS, SPATIAL_FEATURE_COLUMNS, get_model_features
from src.preprocessing.dataset_loader import get_train_val_test_splits


FILES = [
    "pc_anomaly_training.csv",
    "test_dataset.csv",
    "spatial_consistency.csv",
    "sensor_degradation.csv",
    "fault_classification.csv",
]

LABEL_COLUMNS = [
    "is_anomaly",
    "fault_type",
    "severity",
    "event_type",
    "is_genuine_event",
    "sensor_fault_likelihood",
    "anomaly_type",
    "ground_truth",
    "fault_parameter",
    "spatial_anomaly_score",
    "spatial_consensus_score",
    "event_likelihood",
    "degradation_level",
    "maintenance_priority",
    "estimated_health_risk_score",
    "sensor_health_score",
]


def _json_default(value):
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (pd.Timestamp,)):
        return str(value)
    return str(value)


def metrics_with_name(name, y_true, y_pred):
    m = compute_binary_metrics(np.asarray(y_true), np.asarray(y_pred))
    return {"name": name, **m}


def dataset_summary(path):
    df = pd.read_csv(path)
    summary = {
        "file": path,
        "shape": list(df.shape),
        "columns": list(df.columns),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "missing_values": {c: int(v) for c, v in df.isna().sum().items() if int(v) > 0},
        "duplicate_rows": int(df.duplicated().sum()),
        "identical_rows": int(df.duplicated(keep=False).sum()),
    }
    if "station_id" in df.columns:
        summary["station_ids"] = sorted(map(str, df["station_id"].dropna().unique().tolist()))
        summary["station_count"] = int(df["station_id"].nunique())
    if "timestamp" in df.columns:
        ts = pd.to_datetime(df["timestamp"], errors="coerce")
        summary["timestamp_min"] = str(ts.min())
        summary["timestamp_max"] = str(ts.max())
        if "station_id" in df.columns:
            deltas = (
                df.assign(_ts=ts)
                .sort_values(["station_id", "_ts"])
                .groupby("station_id")["_ts"]
                .diff()
                .dropna()
            )
        else:
            deltas = ts.sort_values().diff().dropna()
        vc = deltas.value_counts().head(10)
        summary["sampling_intervals_top"] = {str(k): int(v) for k, v in vc.items()}
        key_cols = [c for c in ["station_id", "timestamp"] if c in df.columns]
        if key_cols:
            summary["station_timestamp_duplicates"] = int(df.duplicated(key_cols).sum())
    if "is_anomaly" in df.columns:
        summary["anomaly_counts"] = {str(k): int(v) for k, v in df["is_anomaly"].value_counts(dropna=False).items()}
    if "fault_type" in df.columns:
        summary["fault_type_counts"] = {str(k): int(v) for k, v in df["fault_type"].value_counts(dropna=False).items()}
    return summary, df


def row_hashes(df, cols):
    stable = df[cols].copy()
    for c in stable.columns:
        stable[c] = stable[c].map(lambda x: "" if pd.isna(x) else repr(x))
    return pd.util.hash_pandas_object(stable, index=False)


def leakage_audit(df_train_full, df_test):
    train_key = set(zip(df_train_full["station_id"].astype(str), df_train_full["timestamp"].astype(str)))
    test_key = set(zip(df_test["station_id"].astype(str), df_test["timestamp"].astype(str)))
    exact_key_overlap = len(train_key & test_key)

    common_cols = [c for c in df_train_full.columns if c in df_test.columns]
    train_row_hashes = set(row_hashes(df_train_full, common_cols).tolist())
    test_row_hashes = set(row_hashes(df_test, common_cols).tolist())
    exact_row_overlap = len(train_row_hashes & test_row_hashes)

    feature_cols = [c for c in FEATURE_COLUMNS if c in df_train_full.columns and c in df_test.columns]
    train_feat_hashes = set(row_hashes(df_train_full, feature_cols).tolist())
    test_feat_hashes = set(row_hashes(df_test, feature_cols).tolist())
    exact_feature_overlap = len(train_feat_hashes & test_feat_hashes)

    train_labels = [c for c in LABEL_COLUMNS if c in FEATURE_COLUMNS]
    feature_config_labels = [c for c in LABEL_COLUMNS if c in FEATURE_COLUMNS + SPATIAL_FEATURE_COLUMNS]

    return {
        "train_test_station_timestamp_overlap": exact_key_overlap,
        "train_test_identical_row_hash_overlap": exact_row_overlap,
        "train_test_identical_feature_vector_overlap": exact_feature_overlap,
        "label_columns_in_feature_columns": train_labels,
        "label_columns_in_feature_or_spatial_columns": feature_config_labels,
    }


def temporal_feature_audit(df):
    df_sorted = df.copy()
    df_sorted["_ts"] = pd.to_datetime(df_sorted["timestamp"], errors="coerce")
    df_sorted = df_sorted.sort_values(["station_id", "_ts"]).reset_index(drop=True)
    out = {}
    for sensor in ["temperature", "pressure", "humidity"]:
        delta_col = f"{sensor}_delta"
        if delta_col in df_sorted.columns:
            expected = df_sorted.groupby("station_id")[sensor].diff()
            actual = df_sorted[delta_col]
            ok = np.isclose(actual.fillna(0), expected.fillna(0), atol=1e-8).all()
            out[delta_col] = {"matches_previous_diff": bool(ok), "max_abs_error": float((actual - expected).abs().max(skipna=True) or 0.0)}
        mean_col = f"{sensor}_roll_mean"
        std_col = f"{sensor}_roll_std"
        med_col = f"{sensor}_roll_median"
        mad_col = f"{sensor}_mad"
        res_col = f"{sensor}_residual"
        group = df_sorted.groupby("station_id")[sensor]
        shifted = group.shift(1)
        exp_mean = shifted.groupby(df_sorted["station_id"]).rolling(12, min_periods=2).mean().reset_index(level=0, drop=True)
        exp_std = shifted.groupby(df_sorted["station_id"]).rolling(12, min_periods=2).std().reset_index(level=0, drop=True)
        exp_med = shifted.groupby(df_sorted["station_id"]).rolling(12, min_periods=2).median().reset_index(level=0, drop=True)
        if mean_col in df_sorted.columns:
            actual = df_sorted[mean_col]
            out[mean_col] = {
                "matches_shifted_rolling_12": bool(np.isclose(actual.fillna(0), exp_mean.fillna(0), atol=1e-8).all()),
                "max_abs_error": float((actual - exp_mean).abs().max(skipna=True) or 0.0),
            }
        if std_col in df_sorted.columns:
            actual = df_sorted[std_col]
            out[std_col] = {
                "matches_shifted_rolling_12": bool(np.isclose(actual.fillna(0), exp_std.fillna(0), atol=1e-8).all()),
                "max_abs_error": float((actual - exp_std).abs().max(skipna=True) or 0.0),
            }
        if med_col in df_sorted.columns:
            actual = df_sorted[med_col]
            out[med_col] = {
                "matches_shifted_rolling_12": bool(np.isclose(actual.fillna(0), exp_med.fillna(0), atol=1e-8).all()),
                "max_abs_error": float((actual - exp_med).abs().max(skipna=True) or 0.0),
            }
        if res_col in df_sorted.columns and mean_col in df_sorted.columns:
            expected_res = df_sorted[sensor] - df_sorted[mean_col]
            actual = df_sorted[res_col]
            out[res_col] = {
                "matches_current_minus_past_roll_mean": bool(np.isclose(actual.fillna(0), expected_res.fillna(0), atol=1e-8).all()),
                "max_abs_error": float((actual - expected_res).abs().max(skipna=True) or 0.0),
            }
        if mad_col in df_sorted.columns:
            def mad_prev(s):
                return s.shift(1).rolling(12, min_periods=4).apply(lambda x: np.median(np.abs(x - np.median(x))), raw=True)
            exp_mad = df_sorted.groupby("station_id")[sensor].transform(mad_prev)
            actual = df_sorted[mad_col]
            out[mad_col] = {
                "matches_shifted_rolling_12_mad_min4": bool(np.isclose(actual.fillna(0), exp_mad.fillna(0), atol=1e-8).all()),
                "max_abs_error": float((actual - exp_mad).abs().max(skipna=True) or 0.0),
            }
    return out


def spatial_feature_audit(df):
    df2 = df.copy()
    med = df2.groupby("timestamp")[["temperature", "pressure", "humidity"]].transform(
        lambda s: [np.median(np.delete(s.to_numpy(), i)) if len(s) > 1 else np.nan for i in range(len(s))]
    )
    mapping = {
        "temperature": "neighbor_temperature_median",
        "pressure": "neighbor_pressure_median",
        "humidity": "neighbor_humidity_median",
    }
    out = {}
    for sensor, col in mapping.items():
        if col in df2.columns:
            actual = df2[col]
            expected = med[sensor]
            out[col] = {
                "matches_same_timestamp_leave_one_out_median": bool(np.isclose(actual.fillna(0), expected.fillna(0), atol=1e-8).all()),
                "max_abs_error": float((actual - expected).abs().max(skipna=True) or 0.0),
            }
        res_col = f"spatial_residual_{sensor}"
        if res_col in df2.columns and col in df2.columns:
            expected_res = df2[sensor] - df2[col]
            out[res_col] = {
                "matches_current_minus_neighbor_median": bool(np.isclose(df2[res_col].fillna(0), expected_res.fillna(0), atol=1e-8).all()),
                "max_abs_error": float((df2[res_col] - expected_res).abs().max(skipna=True) or 0.0),
            }
    return out


def prepare_splits():
    df_train_raw, df_val_raw, df_test_raw = get_train_val_test_splits(val_split_time="2026-05-14 00:00:00")
    df_train_raw = df_train_raw.sort_values(["station_id", "timestamp"]).reset_index(drop=True)
    df_val_raw = df_val_raw.sort_values(["station_id", "timestamp"]).reset_index(drop=True)
    df_test_raw = df_test_raw.sort_values(["station_id", "timestamp"]).reset_index(drop=True)
    train_feat = generate_engineed_features(df_train_raw)
    val_feat = generate_engineed_features(df_val_raw)
    test_feat = generate_engineed_features(df_test_raw)
    cleaner = DataCleaner()
    cleaner.fit(train_feat)
    return (
        cleaner.transform(train_feat),
        cleaner.transform(val_feat),
        cleaner.transform(test_feat),
        df_train_raw,
        df_val_raw,
        df_test_raw,
    )


def rule_preds(df, include_duplicate=True, include_spatial=False):
    baseline = RuleBaselineDetector()
    preds = []
    scores = []
    spatial_flags = []
    for _, row in df.iterrows():
        obs = row.to_dict()
        if not include_duplicate:
            obs["raw_is_duplicate_packet"] = 0.0
        res = baseline.predict_observation(obs)
        flag = int(res["anomaly_flag"])
        score = float(res["anomaly_score"])
        if include_spatial:
            spatial_bad = (
                abs(obs.get("spatial_residual_temperature", 0.0) or 0.0) >= 4.0
                or abs(obs.get("spatial_residual_pressure", 0.0) or 0.0) >= 5.0
                or abs(obs.get("spatial_residual_humidity", 0.0) or 0.0) >= 15.0
            )
            if spatial_bad:
                flag = 1
                score = max(score, 0.65)
        preds.append(flag)
        scores.append(score)
        spatial_flags.append(int(include_spatial and score >= 0.65 and not res["anomaly_flag"]))
    return np.asarray(preds), np.asarray(scores), np.asarray(spatial_flags)


def run_current_reproduction():
    df_train, df_val, df_test, *_ = prepare_splits()
    y_train = df_train["is_anomaly"].to_numpy()
    y_val = df_val["is_anomaly"].to_numpy()
    y_test = df_test["is_anomaly"].to_numpy()

    baseline_pred, baseline_score, _ = rule_preds(df_test, include_duplicate=True)
    baseline_no_dup_pred, _, _ = rule_preds(df_test, include_duplicate=False)

    iforest_g = SkyGuardIsolationForest(mode="global", contamination=0.035, random_state=42)
    iforest_g.fit(df_train)
    iforest_g.tune_threshold(df_val, y_val)
    iforest_s = SkyGuardIsolationForest(mode="station_specific", contamination=0.035, random_state=42)
    iforest_s.fit(df_train)
    iforest_s.tune_threshold(df_val, y_val)
    pred_g_val, _ = iforest_g.predict(df_val)
    pred_s_val, _ = iforest_s.predict(df_val)
    selected_iforest = iforest_g if compute_binary_metrics(y_val, pred_g_val)["f1"] >= compute_binary_metrics(y_val, pred_s_val)["f1"] else iforest_s
    if_pred, if_scores = selected_iforest.predict(df_test)

    ae = SkyGuardAutoencoder(random_state=42)
    ae.fit(df_train[df_train["is_anomaly"] == 0].copy(), epochs=20, batch_size=256, lr=1e-3)
    ae.tune_threshold(df_val, y_val)
    ae_pred, ae_scores = ae.predict(df_test)

    fault_classifier = SkyGuardFaultClassifier(n_estimators=100, random_state=42)
    fault_classifier.fit(df_train, target_col="fault_type")
    fault_labels, fault_confs = fault_classifier.predict_dataframe(df_test)

    fused = []
    fused_no_dup = []
    fused_with_spatial = []
    for i, row in df_test.iterrows():
        obs = row.to_dict()
        is_missing = (obs.get("raw_is_missing", 0) == 1.0) or (obs.get("temperature_missing", 0) == 1.0)
        is_dup = obs.get("raw_is_duplicate_packet", 0) == 1.0
        is_corrupt = (
            (obs.get("temperature", 25.0) > 55.0)
            or (obs.get("temperature", 25.0) < -10.0)
            or (obs.get("humidity", 50.0) > 100.0)
            or (obs.get("humidity", 50.0) < 0.0)
            or (obs.get("pressure", 1000.0) > 1080.0)
            or (obs.get("pressure", 1000.0) < 850.0)
        )
        t_res = abs(obs.get("temperature_residual", 0.0) or 0.0)
        p_res = abs(obs.get("pressure_residual", 0.0) or 0.0)
        h_res = abs(obs.get("humidity_residual", 0.0) or 0.0)
        multi_sensor_shift = (t_res >= 2.0 and p_res >= 2.0) or (t_res >= 2.0 and h_res >= 15.0) or (p_res >= 2.0 and h_res >= 15.0)
        spatial_bad = (
            abs(obs.get("spatial_residual_temperature", 0.0) or 0.0) >= 4.0
            or abs(obs.get("spatial_residual_pressure", 0.0) or 0.0) >= 5.0
            or abs(obs.get("spatial_residual_humidity", 0.0) or 0.0) >= 15.0
        )

        def fuse(use_dup=True, use_spatial=False):
            if is_missing or (use_dup and is_dup) or is_corrupt:
                return 1
            if multi_sensor_shift and (if_scores[i] > 0.20 or ae_scores[i] > 0.05):
                return 1
            score = 0.35 * if_scores[i] + 0.35 * ae_scores[i]
            if use_spatial and spatial_bad:
                score = min(1.0, score + 0.20)
            return int(score >= 0.45)

        fused.append(fuse(use_dup=True, use_spatial=False))
        fused_no_dup.append(fuse(use_dup=False, use_spatial=False))
        fused_with_spatial.append(fuse(use_dup=True, use_spatial=True))

    ml_or = np.logical_or(if_pred == 1, ae_pred == 1).astype(int)
    ml_avg = ((0.5 * if_scores + 0.5 * ae_scores) >= 0.45).astype(int)
    rules_plus_ml = np.logical_or(baseline_pred == 1, ml_avg == 1).astype(int)
    rules_plus_ml_no_dup = np.logical_or(baseline_no_dup_pred == 1, ml_avg == 1).astype(int)
    rules_spatial_pred, _, _ = rule_preds(df_test, include_duplicate=True, include_spatial=True)

    per_fault = []
    y_pred_fused = np.asarray(fused)
    for fault in sorted(df_test["fault_type"].astype(str).unique()):
        mask = df_test["fault_type"].astype(str).to_numpy() == fault
        m = compute_binary_metrics(y_test[mask], y_pred_fused[mask])
        per_fault.append({"fault_type": fault, "count": int(mask.sum()), **m})

    return {
        "train_rows": int(len(df_train)),
        "val_rows": int(len(df_val)),
        "test_rows": int(len(df_test)),
        "test_anomalies": int(y_test.sum()),
        "iforest_selected_mode": selected_iforest.mode,
        "iforest_threshold": selected_iforest.threshold,
        "autoencoder_threshold": ae.threshold,
        "metrics": [
            metrics_with_name("rules_only_current_duplicate_rule", y_test, baseline_pred),
            metrics_with_name("rules_only_without_duplicate_payload_rule", y_test, baseline_no_dup_pred),
            metrics_with_name("isolation_forest_only", y_test, if_pred),
            metrics_with_name("autoencoder_only", y_test, ae_pred),
            metrics_with_name("ml_or", y_test, ml_or),
            metrics_with_name("ml_average_score_threshold", y_test, ml_avg),
            metrics_with_name("rules_plus_ml", y_test, rules_plus_ml),
            metrics_with_name("rules_plus_ml_without_duplicate_payload_rule", y_test, rules_plus_ml_no_dup),
            metrics_with_name("rules_plus_ml_plus_spatial", y_test, np.asarray(fused_with_spatial)),
            metrics_with_name("reported_custom_fusion_reproduction", y_test, np.asarray(fused)),
            metrics_with_name("reported_custom_fusion_without_duplicate_payload_rule", y_test, np.asarray(fused_no_dup)),
            metrics_with_name("rules_plus_spatial_only", y_test, rules_spatial_pred),
        ],
        "per_fault_reported_custom_fusion": per_fault,
    }


def generalization_experiments():
    full_train = pd.read_csv("pc_anomaly_training.csv")
    test = pd.read_csv("test_dataset.csv")
    full = pd.concat([full_train, test], ignore_index=True)
    full["timestamp"] = pd.to_datetime(full["timestamp"])
    full = full.sort_values(["station_id", "timestamp"]).reset_index(drop=True)

    def eval_split(train_raw, val_raw, test_raw, label):
        train_raw = train_raw.sort_values(["station_id", "timestamp"]).reset_index(drop=True)
        val_raw = val_raw.sort_values(["station_id", "timestamp"]).reset_index(drop=True)
        test_raw = test_raw.sort_values(["station_id", "timestamp"]).reset_index(drop=True)
        if len(train_raw) == 0 or len(val_raw) == 0 or len(test_raw) == 0 or test_raw["is_anomaly"].nunique() < 2:
            return {"name": label, "status": "not_enough_data_or_labels"}
        cleaner = DataCleaner()
        train_feat = generate_engineed_features(train_raw)
        val_feat = generate_engineed_features(val_raw)
        test_feat = generate_engineed_features(test_raw)
        cleaner.fit(train_feat)
        train_df = cleaner.transform(train_feat)
        val_df = cleaner.transform(val_feat)
        test_df = cleaner.transform(test_feat)
        y_val = val_df["is_anomaly"].to_numpy()
        y_test = test_df["is_anomaly"].to_numpy()
        iforest = SkyGuardIsolationForest(mode="global", contamination=0.035, random_state=42)
        iforest.fit(train_df)
        iforest.tune_threshold(val_df, y_val)
        if_pred, if_scores = iforest.predict(test_df)
        ae = SkyGuardAutoencoder(random_state=42)
        ae.fit(train_df[train_df["is_anomaly"] == 0].copy(), epochs=10, batch_size=256, lr=1e-3)
        ae.tune_threshold(val_df, y_val)
        ae_pred, ae_scores = ae.predict(test_df)
        fused = []
        for i, row in test_df.iterrows():
            obs = row.to_dict()
            is_missing = (obs.get("raw_is_missing", 0) == 1.0) or (obs.get("temperature_missing", 0) == 1.0)
            is_corrupt = (
                (obs.get("temperature", 25.0) > 55.0)
                or (obs.get("temperature", 25.0) < -10.0)
                or (obs.get("humidity", 50.0) > 100.0)
                or (obs.get("humidity", 50.0) < 0.0)
                or (obs.get("pressure", 1000.0) > 1080.0)
                or (obs.get("pressure", 1000.0) < 850.0)
            )
            t_res = abs(obs.get("temperature_residual", 0.0) or 0.0)
            p_res = abs(obs.get("pressure_residual", 0.0) or 0.0)
            h_res = abs(obs.get("humidity_residual", 0.0) or 0.0)
            multi_sensor_shift = (t_res >= 2.0 and p_res >= 2.0) or (t_res >= 2.0 and h_res >= 15.0) or (p_res >= 2.0 and h_res >= 15.0)
            if is_missing or is_corrupt:
                fused.append(1)
            elif multi_sensor_shift and (if_scores[i] > 0.20 or ae_scores[i] > 0.05):
                fused.append(1)
            else:
                fused.append(int((0.35 * if_scores[i] + 0.35 * ae_scores[i]) >= 0.45))
        return {
            "name": label,
            "train_rows": int(len(train_df)),
            "val_rows": int(len(val_df)),
            "test_rows": int(len(test_df)),
            "test_anomalies": int(y_test.sum()),
            "iforest": compute_binary_metrics(y_test, if_pred),
            "autoencoder": compute_binary_metrics(y_test, ae_pred),
            "fusion_no_duplicate_payload_rule": compute_binary_metrics(y_test, np.asarray(fused)),
        }

    # Later contiguous period: train through May 20, validate May 21-24, final test after May 24.
    later = eval_split(
        full[full["timestamp"] < pd.Timestamp("2026-05-21")],
        full[(full["timestamp"] >= pd.Timestamp("2026-05-21")) & (full["timestamp"] < pd.Timestamp("2026-05-25"))],
        full[full["timestamp"] >= pd.Timestamp("2026-05-25")],
        "later_contiguous_period_train_before_2026_05_21_val_2026_05_21_to_24_test_from_2026_05_25",
    )
    stations = sorted(full["station_id"].unique().tolist())
    station_results = []
    for station in stations:
        other = full[full["station_id"] != station]
        hold = full[full["station_id"] == station]
        split_dt = other["timestamp"].quantile(0.8)
        station_results.append(
            eval_split(
                other[other["timestamp"] < split_dt],
                other[other["timestamp"] >= split_dt],
                hold,
                f"unseen_station_{station}",
            )
        )
    return {"later_period": later, "unseen_station": station_results}


def main():
    summaries = {}
    frames = {}
    for path in FILES:
        summaries[path], frames[path] = dataset_summary(path)

    train_full = frames["pc_anomaly_training.csv"]
    test = frames["test_dataset.csv"]
    duplicate_relations = {
        "fault_classification_equals_pc_anomaly_training": bool(frames["fault_classification.csv"].equals(train_full)),
        "spatial_rows_match_train_plus_test_subset": int(len(frames["spatial_consistency.csv"])),
    }
    leak = leakage_audit(train_full, test)
    temporal = {
        "pc_anomaly_training.csv": temporal_feature_audit(train_full),
        "test_dataset.csv": temporal_feature_audit(test),
    }
    spatial = {
        "pc_anomaly_training.csv": spatial_feature_audit(train_full),
        "test_dataset.csv": spatial_feature_audit(test),
        "spatial_consistency.csv": spatial_feature_audit(frames["spatial_consistency.csv"]),
    }
    reproduction = run_current_reproduction()
    generalization = generalization_experiments()
    payload_duplicate_counts = {}
    for name, df in [("train", train_full), ("test", test)]:
        sorted_df = df.sort_values(["station_id", "timestamp"]).reset_index(drop=True)
        same_payload = (
            sorted_df.groupby("station_id")["temperature"].diff().eq(0)
            & sorted_df.groupby("station_id")["pressure"].diff().eq(0)
            & sorted_df.groupby("station_id")["humidity"].diff().eq(0)
        ).fillna(False)
        payload_duplicate_counts[name] = {
            "same_payload_consecutive_count": int(same_payload.sum()),
            "same_payload_labeled_duplicate_packet": int(((same_payload) & (sorted_df["fault_type"] == "DUPLICATE_PACKET")).sum()) if "fault_type" in sorted_df.columns else None,
            "labeled_duplicate_packet": int((sorted_df["fault_type"] == "DUPLICATE_PACKET").sum()) if "fault_type" in sorted_df.columns else None,
            "station_timestamp_duplicates": int(sorted_df.duplicated(["station_id", "timestamp"]).sum()),
        }

    out = {
        "dataset_summaries": summaries,
        "dataset_duplicate_relations": duplicate_relations,
        "leakage_audit": leak,
        "temporal_feature_audit": temporal,
        "spatial_feature_audit": spatial,
        "payload_duplicate_audit": payload_duplicate_counts,
        "reproduction_and_ablation": reproduction,
        "generalization": generalization,
    }
    print(json.dumps(out, indent=2, default=_json_default))


if __name__ == "__main__":
    main()
