import pandas as pd
import numpy as np
import pytest
import sys
sys.path.insert(0, '.')

from src.preprocessing.cleaner import DataCleaner, get_model_features, TARGET_COLUMNS, FEATURE_COLUMNS
from src.preprocessing.dataset_loader import get_train_val_test_splits


def test_target_columns_rejection():

    sample = pd.DataFrame([{
        'temperature': 25.0,
        'pressure': 1013.2,
        'humidity': 65.0,
        'is_anomaly': 1,
        'fault_type': 'TEMPERATURE_SPIKE',
        'severity': 'HIGH'
    }])
    
    X = get_model_features(sample, include_spatial=False)
    for col in TARGET_COLUMNS:
        assert col not in X.columns, f"Target leak column {col} was found in model input features!"


def test_data_cleaner_imputation():
    cleaner = DataCleaner()
    df_raw = pd.DataFrame([
        {'station_id': 'AWS001', 'timestamp': '2026-05-01 00:00:00', 'temperature': 22.0, 'pressure': 1000.0, 'humidity': 60.0},
        {'station_id': 'AWS001', 'timestamp': '2026-05-01 00:05:00', 'temperature': np.nan, 'pressure': 1000.0, 'humidity': 60.0},
        {'station_id': 'AWS001', 'timestamp': '2026-05-01 00:10:00', 'temperature': 24.0, 'pressure': 1000.0, 'humidity': 60.0}
    ])
    cleaner.fit(df_raw)
    df_clean = cleaner.transform(df_raw)
    assert df_clean['temperature'].isna().sum() == 0, "DataCleaner failed to impute missing value!"
    assert df_clean.iloc[1]['temperature'] == 22.0, "DataCleaner failed forward fill!"


def test_chronological_splits():
    df_train, df_val, df_test = get_train_val_test_splits(val_ratio=0.2)
    assert len(df_train) > 0
    assert len(df_val) > 0
    assert len(df_test) > 0
    
    max_train_time = df_train['timestamp'].max()
    min_val_time = df_val['timestamp'].min()
    assert max_train_time <= min_val_time, "Validation split overlaps chronologically with training set!"
    
    max_val_time = df_val['timestamp'].max()
    min_test_time = df_test['timestamp'].min()
    assert max_val_time <= min_test_time, "Test set overlaps chronologically with validation set!"
