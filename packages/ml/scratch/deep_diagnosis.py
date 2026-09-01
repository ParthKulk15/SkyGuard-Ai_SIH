import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '.')

from src.preprocessing.dataset_loader import get_train_val_test_splits
from src.preprocessing.cleaner import DataCleaner, get_model_features, FEATURE_COLUMNS
from src.features.feature_engineering import generate_engineed_features
from src.anomaly_detection.baseline import RuleBaselineDetector
from src.anomaly_detection.isolation_forest import SkyGuardIsolationForest
from src.anomaly_detection.autoencoder import SkyGuardAutoencoder
from src.anomaly_detection.decision_layer import SkyGuardDecisionLayer

def diagnose():
    print("================ DEEP DIAGNOSIS OF SYSTEM ERRORS ================", flush=True)
    df_train_raw, df_val_raw, df_test_raw = get_train_val_test_splits(val_split_time='2026-05-14 00:00:00')
    
    df_train_feat = generate_engineed_features(df_train_raw)
    df_val_feat = generate_engineed_features(df_val_raw)
    df_test_feat = generate_engineed_features(df_test_raw)
    
    cleaner = DataCleaner()
    cleaner.fit(df_train_feat)
    
    df_train = cleaner.transform(df_train_feat)
    df_val = cleaner.transform(df_val_feat)
    df_test = cleaner.transform(df_test_feat)

    # 1. Inspect DUPLICATE_PACKET rows in df_test_raw and df_test
    print("\n--- 1. DUPLICATE_PACKET Deep Inspection ---", flush=True)
    dup_indices = df_test_raw[df_test_raw['fault_type'] == 'DUPLICATE_PACKET'].index
    print(f"DUPLICATE_PACKET total count: {len(dup_indices)}")
    
    for i in dup_indices[:10]:
        row_raw = df_test_raw.iloc[i]
        row_feat = df_test_feat.iloc[i]
        prev_raw = df_test_raw.iloc[max(0, i-1)] if i > 0 else None
        print(f"\nRow {i} ({row_raw['station_id']} at {row_raw['timestamp']}):")
        print(f"  Current Raw: T={row_raw['temperature']}, P={row_raw['pressure']}, H={row_raw['humidity']}")
        if prev_raw is not None:
            print(f"  Prev Raw:    T={prev_raw['temperature']}, P={prev_raw['pressure']}, H={prev_raw['humidity']} (Station: {prev_raw['station_id']})")
        print(f"  raw_is_duplicate_packet feature: {row_feat['raw_is_duplicate_packet']}")

    # 2. Inspect FALSE POSITIVES (Why are 82 normal rows getting flagged?)
    print("\n--- 2. Inspecting FALSE POSITIVE Rows ---", flush=True)
    iforest = SkyGuardIsolationForest.load('models/isolation_forest.joblib', 'models/scaler.joblib')
    autoencoder = SkyGuardAutoencoder.load('models/autoencoder.pt', 'models/scaler.joblib')
    baseline = RuleBaselineDetector()
    decision_layer = SkyGuardDecisionLayer(w_baseline=0.40, w_iforest=0.35, w_autoencoder=0.25)
    
    _, if_scores = iforest.predict(df_test)
    _, ae_scores = autoencoder.predict(df_test)
    
    fp_records = []
    for idx, row in df_test.iterrows():
        obs = row.to_dict()
        gt = df_test_raw.iloc[idx]['is_anomaly']
        ft = df_test_raw.iloc[idx]['fault_type']
        
        b_res = baseline.predict_observation(obs)
        if_s = if_scores[idx]
        ae_s = ae_scores[idx]
        
        res = decision_layer.evaluate(obs, if_s, ae_s)
        
        if res['anomaly_flag'] == 1 and gt == 0:
            fp_records.append({
                'idx': idx,
                'station_id': obs['station_id'],
                'timestamp': obs['timestamp'],
                'temp': obs['temperature'],
                'press': obs['pressure'],
                'hum': obs['humidity'],
                't_delta': obs.get('temperature_delta', 0),
                'p_delta': obs.get('pressure_delta', 0),
                'h_delta': obs.get('humidity_delta', 0),
                'baseline_flag': b_res['anomaly_flag'],
                'baseline_fault': b_res['fault_type'],
                'baseline_score': b_res['anomaly_score'],
                'iforest_score': if_s,
                'autoencoder_score': ae_s,
                'fused_score': res['anomaly_score'],
                'event_type': df_test_raw.iloc[idx]['event_type']
            })

    df_fp = pd.DataFrame(fp_records)
    print(f"Total False Positives: {len(df_fp)}")
    print("\nFalse Positives by Event Type:")
    print(df_fp['event_type'].value_counts())
    print("\nFalse Positives by Baseline Fault Type:")
    print(df_fp['baseline_fault'].value_counts())
    print("\nSample False Positive Rows:")
    print(df_fp[['idx', 'station_id', 'timestamp', 'event_type', 'baseline_fault', 'fused_score', 'iforest_score', 'autoencoder_score', 't_delta', 'h_delta']].head(10))

    # 3. Inspect ML Model Scores on Normal Weather vs Real Anomalies
    print("\n--- 3. ML Model Score Statistics ---", flush=True)
    df_test_raw['if_score'] = if_scores
    df_test_raw['ae_score'] = ae_scores
    print("\nIsolation Forest Mean Scores by Fault Type:")
    print(df_test_raw.groupby('fault_type')['if_score'].describe())
    print("\nAutoencoder Mean Scores by Fault Type:")
    print(df_test_raw.groupby('fault_type')['ae_score'].describe())

diagnose()
