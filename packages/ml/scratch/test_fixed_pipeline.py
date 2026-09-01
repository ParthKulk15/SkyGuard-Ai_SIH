import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '.')

from src.preprocessing.dataset_loader import get_train_val_test_splits
from src.features.feature_engineering import generate_engineed_features
from src.preprocessing.cleaner import DataCleaner, FEATURE_COLUMNS
from src.anomaly_detection.baseline import RuleBaselineDetector
from src.anomaly_detection.isolation_forest import SkyGuardIsolationForest
from src.anomaly_detection.autoencoder import SkyGuardAutoencoder
from src.spatial.spatial_consistency import SpatialConsistencyEvaluator
from src.evaluation.metrics import compute_binary_metrics, compute_per_anomaly_type_performance

def test_fixed():
    print("================ TESTING FIXED PIPELINE ================", flush=True)
    df_train_raw, df_val_raw, df_test_raw = get_train_val_test_splits(val_split_time='2026-05-14 00:00:00')
    
    # CRITICAL FIX 1: Sort raw dataframes by station_id and timestamp BEFORE feature engineering!
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
    
    print("\n--- Testing Baseline with Sorted Station Data ---", flush=True)
    baseline = RuleBaselineDetector()
    df_base_preds = baseline.predict_dataframe(df_test)
    y_pred_base = df_base_preds['anomaly_flag'].values
    
    metrics_base = compute_binary_metrics(y_test, y_pred_base)
    print("Fixed Baseline Test Metrics:", metrics_base)
    
    df_per_type = compute_per_anomaly_type_performance(df_test, y_pred_base)
    print("\nPer-Fault Breakdown (Fixed Baseline):")
    print(df_per_type)

test_fixed()
