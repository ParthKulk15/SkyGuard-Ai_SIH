import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '.')

from src.preprocessing.dataset_loader import get_train_val_test_splits
from src.features.feature_engineering import generate_engineed_features
from src.preprocessing.cleaner import DataCleaner
from src.anomaly_detection.baseline import RuleBaselineDetector
from src.anomaly_detection.isolation_forest import SkyGuardIsolationForest
from src.anomaly_detection.autoencoder import SkyGuardAutoencoder
from src.anomaly_detection.fault_classifier import SkyGuardFaultClassifier
from src.spatial.spatial_consistency import SpatialConsistencyEvaluator
from src.evaluation.metrics import compute_binary_metrics, compute_per_anomaly_type_performance

def run_perfect():
    print("================ TESTING PERFECT FUSION PIPELINE ================", flush=True)
    df_train_raw, df_val_raw, df_test_raw = get_train_val_test_splits(val_split_time='2026-05-14 00:00:00')
    
    # 1. SORT DATASETS CHRONOLOGICALLY BY STATION AND TIMESTAMP
    df_train_raw = df_train_raw.sort_values(['station_id', 'timestamp']).reset_index(drop=True)
    df_val_raw = df_val_raw.sort_values(['station_id', 'timestamp']).reset_index(drop=True)
    df_test_raw = df_test_raw.sort_values(['station_id', 'timestamp']).reset_index(drop=True)
    
    df_train_feat = generate_engineed_features(df_train_raw)
    df_val_feat = generate_engineed_features(df_val_raw)
    df_test_feat = generate_engineed_features(df_test_raw)
    
    cleaner = DataCleaner()
    cleaner.fit(df_train_feat)
    
    df_train = cleaner.transform(df_train_feat)
    df_val = cleaner.transform(df_val_feat)
    df_test = cleaner.transform(df_test_feat)
    
    y_test = df_test['is_anomaly'].values
    df_train_normal = df_train[df_train['is_anomaly'] == 0].copy()

    # 2. TRAIN UNSUPERVISED MODELS
    iforest = SkyGuardIsolationForest(mode='global', contamination=0.035, random_state=42)
    iforest.fit(df_train)
    
    autoencoder = SkyGuardAutoencoder(random_state=42)
    autoencoder.fit(df_train_normal, epochs=20, batch_size=256, lr=1e-3)

    _, if_scores = iforest.predict(df_test)
    _, ae_scores = autoencoder.predict(df_test)

    # 3. CONSTRUCT PERFECT DECISION LAYER
    fused_flags = []
    fused_scores = []
    
    for idx, row in df_test.iterrows():
        obs = row.to_dict()
        if_s = if_scores[idx]
        ae_s = ae_scores[idx]
        
        # Hard Stream / Data Integrity Fault Rules
        is_missing = (obs.get('raw_is_missing', 0) == 1.0) or (obs.get('temperature_missing', 0) == 1.0)
        is_dup = (obs.get('raw_is_duplicate_packet', 0) == 1.0)
        is_corrupt = (obs.get('temperature', 25.0) > 55.0) or (obs.get('humidity', 50.0) > 100.0) or (obs.get('humidity', 50.0) < 0.0)
        
        # Multivariate sensor failure check (simultaneous shift across >=2 sensors)
        t_res = abs(obs.get('temperature_residual', 0.0) or 0.0)
        p_res = abs(obs.get('pressure_residual', 0.0) or 0.0)
        h_res = abs(obs.get('humidity_residual', 0.0) or 0.0)
        multi_sensor_shift = (t_res >= 2.0 and p_res >= 2.0) or (t_res >= 2.0 and h_res >= 15.0) or (p_res >= 2.0 and h_res >= 15.0)
        
        if is_missing or is_dup or is_corrupt:
            fused_flag = 1
            fused_score = 1.0
        elif multi_sensor_shift and (if_s > 0.20 or ae_s > 0.05):
            fused_flag = 1
            fused_score = max(if_s, 0.85)
        else:
            fused_flag = 0
            fused_score = 0.35 * if_s + 0.35 * ae_s

        fused_flags.append(fused_flag)
        fused_scores.append(fused_score)

    y_pred = np.array(fused_flags)
    metrics = compute_binary_metrics(y_test, y_pred)
    print("\n================ FINAL REFINED SYSTEM TEST METRICS ================")
    print(metrics)
    
    df_per_type = compute_per_anomaly_type_performance(df_test, y_pred)
    print("\n================ PER-FAULT PERFORMANCE BREAKDOWN ================")
    print(df_per_type)

run_perfect()
