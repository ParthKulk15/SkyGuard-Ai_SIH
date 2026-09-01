import pandas as pd
import numpy as np
from typing import Tuple, Dict, Optional

TRAIN_PATH = 'pc_anomaly_training.csv'
TEST_PATH = 'test_dataset.csv'
SPATIAL_PATH = 'spatial_consistency.csv'
DEGRADATION_PATH = 'sensor_degradation.csv'


def load_raw_datasets() -> Dict[str, pd.DataFrame]:
    return {
        'train': pd.read_csv(TRAIN_PATH),
        'test': pd.read_csv(TEST_PATH),
        'spatial': pd.read_csv(SPATIAL_PATH),
        'degradation': pd.read_csv(DEGRADATION_PATH)
    }


def get_train_val_test_splits(
    val_split_time: str = '2026-05-14 00:00:00',
    val_ratio: Optional[float] = None
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    df_train_full = pd.read_csv(TRAIN_PATH)
    df_test = pd.read_csv(TEST_PATH)
    
    # Sort chronologically by timestamp
    df_train_full['timestamp'] = pd.to_datetime(df_train_full['timestamp'])
    df_test['timestamp'] = pd.to_datetime(df_test['timestamp'])
    
    df_train_full = df_train_full.sort_values(['timestamp', 'station_id']).reset_index(drop=True)
    df_test = df_test.sort_values(['timestamp', 'station_id']).reset_index(drop=True)
    
    if val_ratio is not None:
        total_rows = len(df_train_full)
        split_idx = int(total_rows * (1.0 - val_ratio))
        split_dt = df_train_full.iloc[split_idx]['timestamp']
    else:
        split_dt = pd.to_datetime(val_split_time)
        
    train_mask = df_train_full['timestamp'] < split_dt
    val_mask = df_train_full['timestamp'] >= split_dt
    
    df_train = df_train_full[train_mask].copy().reset_index(drop=True)
    df_val = df_train_full[val_mask].copy().reset_index(drop=True)
    
    return df_train, df_val, df_test
