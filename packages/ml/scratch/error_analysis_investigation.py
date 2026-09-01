import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '.')

from src.preprocessing.dataset_loader import get_train_val_test_splits
from src.preprocessing.cleaner import DataCleaner, get_model_features
from src.features.feature_engineering import generate_engineed_features
from src.anomaly_detection.baseline import RuleBaselineDetector
from src.anomaly_detection.isolation_forest import SkyGuardIsolationForest
from src.anomaly_detection.autoencoder import SkyGuardAutoencoder
from src.anomaly_detection.fault_classifier import SkyGuardFaultClassifier
from src.spatial.spatial_consistency import SpatialConsistencyEvaluator
from src.degradation.degradation_model import StationDegradationEvaluator
from src.anomaly_detection.decision_layer import SkyGuardDecisionLayer

def investigate():
    print("================ ERROR ANALYSIS INVESTIGATION ================", flush=True)
    df_train_raw, df_val_raw, df_test_raw = get_train_val_test_splits(val_ratio=0.2)
    
    # 1. COMMUNICATION_FAILURE Analysis
    print("\n--- 1. COMMUNICATION_FAILURE Raw Rows ---", flush=True)
    comm_fail_rows = df_test_raw[df_test_raw['fault_type'] == 'COMMUNICATION_FAILURE']
    print(f"Total COMM_FAILURE count in test set: {len(comm_fail_rows)}")
    print("Missing counts in raw test set for COMM_FAILURE:")
    print(comm_fail_rows[['temperature', 'pressure', 'humidity']].isna().sum())
    
    print("Missing counts in raw test set for NORMAL:")
    norm_rows = df_test_raw[df_test_raw['fault_type'] == 'NORMAL']
    print(norm_rows[['temperature', 'pressure', 'humidity']].isna().sum())

    # 2. DUPLICATE_PACKET Analysis
    print("\n--- 2. DUPLICATE_PACKET Raw Rows ---", flush=True)
    dup_rows = df_test_raw[df_test_raw['fault_type'] == 'DUPLICATE_PACKET']
    print(f"Total DUPLICATE_PACKET count in test set: {len(dup_rows)}")
    print("Sample DUPLICATE_PACKET rows:")
    print(dup_rows[['timestamp', 'station_id', 'temperature', 'pressure', 'humidity']].head(6))

    # 3. Cleaned representations
    print("\n--- 3. Cleaned Feature Matrix Audit ---", flush=True)
    cleaner = DataCleaner()
    cleaner.fit(generate_engineed_features(df_train_raw))
    
    # Before cleaning: calculate missing indicators from raw dataframe!
    df_test_raw_feat = generate_engineed_features(df_test_raw)
    print("Raw test set temperature_missing sum before DataCleaner:", df_test_raw_feat['temperature_missing'].sum())
    
    df_test_clean = cleaner.transform(df_test_raw_feat)
    print("Cleaned test set temperature_missing sum after DataCleaner:", df_test_clean['temperature_missing'].sum())

    # 4. Score breakdown per fault type
    print("\n--- 4. Computing Vectorized Scores per Fault Type ---", flush=True)
    iforest = SkyGuardIsolationForest.load('models/isolation_forest.joblib', 'models/scaler.joblib')
    autoencoder = SkyGuardAutoencoder.load('models/autoencoder.pt', 'models/scaler.joblib')
    
    _, if_scores = iforest.predict(df_test_clean)
    _, ae_scores = autoencoder.predict(df_test_clean)
    
    df_test_raw['iforest_score'] = if_scores
    df_test_raw['autoencoder_score'] = ae_scores
    
    summary = df_test_raw.groupby('fault_type')[['iforest_score', 'autoencoder_score']].agg(['mean', 'min', 'max', 'std'])
    print(summary)

investigate()
