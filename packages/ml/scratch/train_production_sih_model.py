import sys
sys.path.insert(0, '.')

import pandas as pd
import numpy as np
import os
import json
import joblib

from src.preprocessing.cleaner import DataCleaner, get_model_features, FEATURE_COLUMNS
from src.features.feature_engineering import generate_engineed_features
from src.anomaly_detection.isolation_forest import SkyGuardIsolationForest
from src.anomaly_detection.autoencoder import SkyGuardAutoencoder
from src.anomaly_detection.fault_classifier import SkyGuardFaultClassifier
from src.degradation.degradation_model import StationDegradationEvaluator
from src.inference.pipeline import SkyGuardInferenceEngine

os.makedirs('models', exist_ok=True)


def train_sih_production_models():
    print("================ 1. LOADING ALL HISTORICAL DATA FOR PRODUCTION TRAINING ================")
    df_train_raw = pd.read_csv('pc_anomaly_training.csv')
    df_deg_raw = pd.read_csv('sensor_degradation.csv')
    
    # Keep test_dataset.csv strictly held out; production training must only
    # use approved historical training observations.
    df_full_raw = df_train_raw.copy()
    df_full_raw['timestamp'] = pd.to_datetime(df_full_raw['timestamp'])
    
    # SORT CHRONOLOGICALLY BY STATION_ID AND TIMESTAMP
    df_full_raw = df_full_raw.sort_values(['station_id', 'timestamp']).reset_index(drop=True)
    
    print(f"Total Full Production Training Rows: {len(df_full_raw)} ({df_full_raw['timestamp'].min()} to {df_full_raw['timestamp'].max()})")
    
    # Feature engineering on full dataset
    print("\n================ 2. GENERATING PRODUCTION FEATURES & FITTING CLEANER ================")
    df_full_feat = generate_engineed_features(df_full_raw)
    
    cleaner = DataCleaner()
    cleaner.fit(df_full_feat)
    df_full_clean = cleaner.transform(df_full_feat)
    
    # Separate normal observations for unsupervised models
    df_normal_clean = df_full_clean[df_full_clean['is_anomaly'] == 0].copy()
    print(f"Normal Training Observations for Unsupervised Models: {len(df_normal_clean)} / {len(df_full_clean)}")

    # 3. Train Production Isolation Forest
    print("\n================ 3. TRAINING PRODUCTION ISOLATION FOREST ================")
    iforest = SkyGuardIsolationForest(mode='global', contamination=0.035, random_state=42)
    iforest.fit(df_full_clean)
    iforest.save('models/isolation_forest.joblib', 'models/scaler.joblib')
    print("Saved models/isolation_forest.joblib")

    # 4. Train Production PyTorch Autoencoder
    print("\n================ 4. TRAINING PRODUCTION PYTORCH AUTOENCODER ================")
    autoencoder = SkyGuardAutoencoder(random_state=42)
    autoencoder.fit(df_normal_clean, epochs=25, batch_size=256, lr=1e-3)
    autoencoder.save('models/autoencoder.pt', 'models/scaler.joblib')
    print("Saved models/autoencoder.pt")

    # 5. Train Production Supervised Fault Classifier
    print("\n================ 5. TRAINING PRODUCTION FAULT CLASSIFIER ================")
    fault_classifier = SkyGuardFaultClassifier(n_estimators=150, random_state=42)
    fault_classifier.fit(df_full_clean, target_col='fault_type')
    fault_classifier.save('models/fault_classifier.joblib', 'models/scaler.joblib')
    print("Saved models/fault_classifier.joblib")

    # 6. Train Production Station Degradation Evaluator
    print("\n================ 6. TRAINING PRODUCTION DEGRADATION MODEL ================")
    degradation_evaluator = StationDegradationEvaluator(random_state=42)
    degradation_evaluator.fit(df_deg_raw)
    degradation_evaluator.save('models/degradation_model.joblib')
    print("Saved models/degradation_model.joblib")

    # 7. Save Production Feature and Model Configs
    print("\n================ 7. SAVING PRODUCTION CONFIGURATIONS ================")
    feature_config = {
        'feature_columns': FEATURE_COLUMNS,
        'station_ids': sorted(df_full_clean['station_id'].unique().tolist()),
        'median_imputation_values': cleaner.median_values
    }
    with open('models/feature_config.json', 'w') as f:
        json.dump(feature_config, f, indent=2)
    print("Saved models/feature_config.json")

    model_config = {
        'version': '1.0.0-production-sih',
        'fusion_weights': {
            'w_baseline': 0.40,
            'w_iforest': 0.35,
            'w_autoencoder': 0.25
        },
        'decision_threshold': 0.45,
        'spatial_penalty': 0.20,
        'spatial_credit': -0.25
    }
    with open('models/model_config.json', 'w') as f:
        json.dump(model_config, f, indent=2)
    print("Saved models/model_config.json")

    # 8. Verify Production SkyGuardInferenceEngine
    print("\n================ 8. VERIFYING PRODUCTION INFERENCE ENGINE ================")
    engine = SkyGuardInferenceEngine(models_dir='models')
    
    # Test single JSON packet prediction
    sample_packet = {
        "timestamp": "2026-06-01 12:00:00",
        "station_id": "AWS001",
        "temperature": 24.5,
        "pressure": 1012.3,
        "humidity": 65.0
    }
    result = engine.predict_single(sample_packet)
    print("\nSample Single Packet Prediction Output:")
    print(json.dumps(result, indent=2))
    
    # Test missing data (COMMUNICATION_FAILURE) packet
    comm_packet = {
        "timestamp": "2026-06-01 12:05:00",
        "station_id": "AWS001",
        "temperature": None,
        "pressure": None,
        "humidity": None
    }
    comm_result = engine.predict_single(comm_packet)
    print("\nSample Communication Failure Packet Prediction Output:")
    print(json.dumps(comm_result, indent=2))

    print("\nProduction training completed successfully! Model is 100% ready for SIH!")


if __name__ == '__main__':
    train_sih_production_models()
