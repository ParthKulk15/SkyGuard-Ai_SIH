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
from src.spatial.spatial_consistency import SpatialConsistencyEvaluator
from src.evaluation.metrics import compute_binary_metrics, compute_per_anomaly_type_performance

def test_prec():
    df_train_raw, df_val_raw, df_test_raw = get_train_val_test_splits(val_split_time='2026-05-14 00:00:00')
    
    # Sort chronologically by station_id and timestamp BEFORE feature engineering
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
    
    # Baseline with tuned residual guards
    baseline = RuleBaselineDetector(config={
        'temp_delta_threshold': 4.0,
        'pressure_delta_threshold': 3.5,
        'humidity_delta_threshold': 20.0,
        'residual_z_threshold': 4.0,
        'frozen_ticks_threshold': 6,
        'temp_min_bound': -10.0,
        'temp_max_bound': 55.0,
        'humidity_min_bound': 0.0,
        'humidity_max_bound': 100.0,
        'pressure_min_bound': 850.0,
        'pressure_max_bound': 1080.0
    })
    
    spatial = SpatialConsistencyEvaluator()
    
    fused_flags = []
    for idx, row in df_test.iterrows():
        obs = row.to_dict()
        b_res = baseline.predict_observation(obs)
        
        # Hard stream fault rules (COMMUNICATION_FAILURE, DATA_CORRUPTION, DUPLICATE_PACKET)
        if obs.get('raw_is_missing', 0) == 1.0 or obs.get('temperature_missing', 0) == 1.0:
            fused_flags.append(1)
        elif obs.get('raw_is_duplicate_packet', 0) == 1.0:
            fused_flags.append(1)
        elif obs.get('temperature', 25.0) > 55.0 or obs.get('humidity', 50.0) > 100.0 or obs.get('humidity', 50.0) < 0.0:
            fused_flags.append(1)
        elif b_res['fault_type'] in ['SIMULTANEOUS_SENSOR_FAILURE']:
            fused_flags.append(1)
        else:
            fused_flags.append(0)

    y_pred = np.array(fused_flags)
    metrics = compute_binary_metrics(y_test, y_pred)
    print("\nHigh Precision Stream System Test Metrics:", metrics)
    
    df_per_type = compute_per_anomaly_type_performance(df_test, y_pred)
    print("\nPer-Fault Breakdown:")
    print(df_per_type)

test_prec()
