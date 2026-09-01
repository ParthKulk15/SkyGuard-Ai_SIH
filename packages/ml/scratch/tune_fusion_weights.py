import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '.')

from src.preprocessing.dataset_loader import get_train_val_test_splits
from src.preprocessing.cleaner import DataCleaner
from src.features.feature_engineering import generate_engineed_features
from src.anomaly_detection.baseline import RuleBaselineDetector
from src.anomaly_detection.isolation_forest import SkyGuardIsolationForest
from src.anomaly_detection.autoencoder import SkyGuardAutoencoder
from sklearn.metrics import f1_score

def tune():
    print("================ TUNING FUSION WEIGHTS ON VALIDATION SET ONLY ================", flush=True)
    df_train_raw, df_val_raw, df_test_raw = get_train_val_test_splits(val_split_time='2026-05-14 00:00:00')
    
    df_train_feat = generate_engineed_features(df_train_raw)
    df_val_feat = generate_engineed_features(df_val_raw)
    
    cleaner = DataCleaner()
    cleaner.fit(df_train_feat)
    df_val = cleaner.transform(df_val_feat)
    
    y_val = df_val['is_anomaly'].values
    print(f"Validation anomaly count: {y_val.sum()} / {len(y_val)}", flush=True)
    
    # Load trained models
    iforest = SkyGuardIsolationForest.load('models/isolation_forest.joblib', 'models/scaler.joblib')
    autoencoder = SkyGuardAutoencoder.load('models/autoencoder.pt', 'models/scaler.joblib')
    baseline = RuleBaselineDetector()

    _, if_scores_val = iforest.predict(df_val)
    _, ae_scores_val = autoencoder.predict(df_val)

    # Vectorized Stream Quality and Hard Rule flags
    raw_missing = (df_val['raw_is_missing'] == 1.0) | (df_val['temperature_missing'] == 1.0)
    raw_dup = (df_val['raw_is_duplicate_packet'] == 1.0)
    hard_anom = raw_missing | raw_dup
    
    base_scores_val = np.where(hard_anom, 1.0, 0.05)
    base_flags_val = hard_anom.astype(int).values
    
    best_f1 = -1.0
    best_weights = (0.40, 0.35, 0.25)
    best_thresh = 0.45

    # Grid search weights & threshold
    for w_b in np.linspace(0.2, 0.6, 5):
        for w_if in np.linspace(0.2, 0.6, 5):
            for w_ae in np.linspace(0.1, 0.5, 5):
                w_tot = w_b + w_if + w_ae
                wb_n, wif_n, wae_n = w_b / w_tot, w_if / w_tot, w_ae / w_tot
                
                fused_scores = wb_n * base_scores_val + wif_n * if_scores_val + wae_n * ae_scores_val
                
                for thresh in np.linspace(0.30, 0.60, 7):
                    preds = ((fused_scores >= thresh) | (base_flags_val == 1)).astype(int)
                    f1 = f1_score(y_val, preds, zero_division=0)
                    if f1 > best_f1:
                        best_f1 = f1
                        best_weights = (round(float(wb_n), 3), round(float(wif_n), 3), round(float(wae_n), 3))
                        best_thresh = round(float(thresh), 3)

    print(f"Optimal Validation Weights (w_base, w_iforest, w_autoencoder): {best_weights}", flush=True)
    print(f"Optimal Validation Decision Threshold: {best_thresh}", flush=True)
    print(f"Validation F1 Score: {best_f1:.4f}", flush=True)

if __name__ == '__main__':
    tune()
