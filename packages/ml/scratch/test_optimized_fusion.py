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

def run_opt():
    print("================ TESTING OPTIMIZED SYSTEM ================", flush=True)
    df_train_raw, df_val_raw, df_test_raw = get_train_val_test_splits(val_split_time='2026-05-14 00:00:00')
    
    # Sort chronologically by station_id and timestamp BEFORE feature engineering!
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

    # Refined Baseline Rules with guarded denominators
    baseline = RuleBaselineDetector()
    
    # Train Isolation Forest on normal train data with tuned contamination
    iforest = SkyGuardIsolationForest(mode='global', contamination=0.035, random_state=42)
    iforest.fit(df_train)
    
    # Train PyTorch Autoencoder on normal train data
    autoencoder = SkyGuardAutoencoder(random_state=42)
    autoencoder.fit(df_train_normal, epochs=20, batch_size=256, lr=1e-3)

    _, if_scores = iforest.predict(df_test)
    _, ae_scores = autoencoder.predict(df_test)
    
    # Decision layer fusion
    fused_flags = []
    fused_scores = []
    
    for idx, row in df_test.iterrows():
        obs = row.to_dict()
        b_res = baseline.predict_observation(obs)
        if_s = if_scores[idx]
        ae_s = ae_scores[idx]
        
        # Hard stream rules override (COMMUNICATION_FAILURE, DATA_CORRUPTION, DUPLICATE_PACKET)
        if b_res['fault_type'] in ['COMMUNICATION_FAILURE', 'DATA_CORRUPTION', 'DUPLICATE_PACKET']:
            fused_flag = 1
            fused_score = 1.0
        elif b_res['anomaly_flag'] == 1 and (if_s > 0.18 or ae_s > 0.05):
            fused_flag = 1
            fused_score = max(b_res['anomaly_score'], if_s)
        elif if_s > 0.40 and ae_s > 0.15:
            fused_flag = 1
            fused_score = (if_s + ae_s) / 2.0
        else:
            fused_flag = 0
            fused_score = 0.35 * b_res['anomaly_score'] + 0.35 * if_s + 0.30 * ae_s

        fused_flags.append(fused_flag)
        fused_scores.append(fused_score)

    y_pred = np.array(fused_flags)
    metrics = compute_binary_metrics(y_test, y_pred)
    print("\nOptimized Fused System Test Metrics:", metrics)
    
    df_per_type = compute_per_anomaly_type_performance(df_test, y_pred)
    print("\nPer-Fault Breakdown (Optimized Fused System):")
    print(df_per_type)

run_opt()
