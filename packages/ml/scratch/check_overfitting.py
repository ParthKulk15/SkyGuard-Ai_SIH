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
from src.evaluation.metrics import compute_binary_metrics, compute_per_anomaly_type_performance

def check_overfitting():
    print("================ OVERFITTING AUDIT & EVALUATION ================", flush=True)
    df_train_raw, df_val_raw, df_test_raw = get_train_val_test_splits(val_split_time='2026-05-14 00:00:00')
    
    # Sort chronologically by station_id and timestamp
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
    
    y_train = df_train['is_anomaly'].values
    y_val = df_val['is_anomaly'].values
    y_test = df_test['is_anomaly'].values

    print(f"Train Dataset: {len(df_train)} rows | Anomalies: {y_train.sum()} ({y_train.mean()*100:.2f}%)")
    print(f"Val Dataset:   {len(df_val)} rows | Anomalies: {y_val.sum()} ({y_val.mean()*100:.2f}%)")
    print(f"Test Dataset:  {len(df_test)} rows | Anomalies: {y_test.sum()} ({y_test.mean()*100:.2f}%)")

    # Load trained models
    iforest = SkyGuardIsolationForest.load('models/isolation_forest.joblib', 'models/scaler.joblib')
    autoencoder = SkyGuardAutoencoder.load('models/autoencoder.pt', 'models/scaler.joblib')
    fault_classifier = SkyGuardFaultClassifier.load('models/fault_classifier.joblib', 'models/scaler.joblib')

    # Evaluate Isolation Forest across splits
    y_pred_if_tr, _ = iforest.predict(df_train)
    y_pred_if_val, _ = iforest.predict(df_val)
    y_pred_if_te, _ = iforest.predict(df_test)
    
    m_if_tr = compute_binary_metrics(y_train, y_pred_if_tr)
    m_if_val = compute_binary_metrics(y_val, y_pred_if_val)
    m_if_te = compute_binary_metrics(y_test, y_pred_if_te)
    
    print("\n--- Isolation Forest Metrics Across Splits ---")
    print(f"Train F1: {m_if_tr['f1']:.4f} | Recall: {m_if_tr['recall']:.4f} | FPR: {m_if_tr['fpr']:.4f}")
    print(f"Val   F1: {m_if_val['f1']:.4f} | Recall: {m_if_val['recall']:.4f} | FPR: {m_if_val['fpr']:.4f}")
    print(f"Test  F1: {m_if_te['f1']:.4f} | Recall: {m_if_te['recall']:.4f} | FPR: {m_if_te['fpr']:.4f}")

    # Evaluate Autoencoder across splits
    y_pred_ae_tr, _ = autoencoder.predict(df_train)
    y_pred_ae_val, _ = autoencoder.predict(df_val)
    y_pred_ae_te, _ = autoencoder.predict(df_test)
    
    m_ae_tr = compute_binary_metrics(y_train, y_pred_ae_tr)
    m_ae_val = compute_binary_metrics(y_val, y_pred_ae_val)
    m_ae_te = compute_binary_metrics(y_test, y_pred_ae_te)
    
    print("\n--- PyTorch Autoencoder Metrics Across Splits ---")
    print(f"Train F1: {m_ae_tr['f1']:.4f} | Recall: {m_ae_tr['recall']:.4f} | FPR: {m_ae_tr['fpr']:.4f}")
    print(f"Val   F1: {m_ae_val['f1']:.4f} | Recall: {m_ae_val['recall']:.4f} | FPR: {m_ae_val['fpr']:.4f}")
    print(f"Test  F1: {m_ae_te['f1']:.4f} | Recall: {m_ae_te['recall']:.4f} | FPR: {m_ae_te['fpr']:.4f}")

    # Evaluate Fault Classifier accuracy on train vs val vs test
    acc_rf_tr = (fault_classifier.model.predict(fault_classifier.scaler.transform(df_train[fault_classifier.feature_names])) == df_train['fault_type']).mean()
    acc_rf_val = (fault_classifier.model.predict(fault_classifier.scaler.transform(df_val[fault_classifier.feature_names])) == df_val['fault_type']).mean()
    acc_rf_te = (fault_classifier.model.predict(fault_classifier.scaler.transform(df_test[fault_classifier.feature_names])) == df_test['fault_type']).mean()
    
    print("\n--- Supervised Random Forest Fault Classifier Accuracy ---")
    print(f"Train Accuracy: {acc_rf_tr*100:.2f}%")
    print(f"Val   Accuracy: {acc_rf_val*100:.2f}%")
    print(f"Test  Accuracy: {acc_rf_te*100:.2f}%")

check_overfitting()
