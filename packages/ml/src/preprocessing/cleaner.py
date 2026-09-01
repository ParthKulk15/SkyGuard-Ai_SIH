import pandas as pd
import numpy as np

# Ground-truth label and leak-prone columns that MUST NOT be fed to model inputs
TARGET_COLUMNS = [
    'is_anomaly', 'fault_type', 'severity', 'event_type', 'is_genuine_event', 
    'fault_parameter', 'spatial_anomaly_score', 'spatial_consensus_score', 
    'event_likelihood', 'sensor_fault_likelihood', 'degradation_level', 
    'maintenance_priority', 'estimated_health_risk_score', 'sensor_health_score'
]

# Baseline / ML Model Input Features (derived solely from raw sensor readings, timestamps, and station metadata)
FEATURE_COLUMNS = [
    'temperature', 'pressure', 'humidity',
    'hour_sin', 'hour_cos', 'doy_sin', 'doy_cos',
    'temperature_delta', 'pressure_delta', 'humidity_delta',
    'temperature_roll_mean', 'temperature_roll_std', 'temperature_roll_median', 'temperature_mad', 'temperature_residual',
    'pressure_roll_mean', 'pressure_roll_std', 'pressure_roll_median', 'pressure_mad', 'pressure_residual',
    'humidity_roll_mean', 'humidity_roll_std', 'humidity_roll_median', 'humidity_mad', 'humidity_residual',
    'dew_point', 'temp_humidity_product', 'temp_pressure_product',
    'temperature_missing', 'pressure_missing', 'humidity_missing',
    'raw_is_missing', 'raw_is_duplicate_packet'
]

SPATIAL_FEATURE_COLUMNS = [
    'neighbor_temperature_median', 'spatial_residual_temperature', 'spatial_z_temperature',
    'neighbor_pressure_median', 'spatial_residual_pressure', 'spatial_z_pressure',
    'neighbor_humidity_median', 'spatial_residual_humidity', 'spatial_z_humidity'
]


class DataCleaner:
    def __init__(self):
        self.median_values = {}

    def fit(self, df: pd.DataFrame):
        df_clean = df.copy()
        for col in FEATURE_COLUMNS + SPATIAL_FEATURE_COLUMNS:
            if col in df_clean.columns:
                num_series = pd.to_numeric(df_clean[col], errors='coerce')
                self.median_values[col] = float(num_series.median()) if not num_series.dropna().empty else 0.0
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = df.copy()
        
        # Sort by station and timestamp if available
        if 'station_id' in df_clean.columns and 'timestamp' in df_clean.columns:
            df_clean = df_clean.sort_values(['station_id', 'timestamp']).reset_index(drop=True)

        # Preserve binary stream quality flags BEFORE imputing numeric series
        stream_flags = {}
        for flag_col in ['temperature_missing', 'pressure_missing', 'humidity_missing', 'raw_is_missing', 'raw_is_duplicate_packet']:
            if flag_col in df_clean.columns:
                stream_flags[flag_col] = df_clean[flag_col].copy()

        # Groupby station forward fill then backfill for missing sensor observations
        for col in FEATURE_COLUMNS + SPATIAL_FEATURE_COLUMNS:
            if col in df_clean.columns and col not in stream_flags:
                if 'station_id' in df_clean.columns:
                    df_clean[col] = df_clean.groupby('station_id')[col].transform(lambda g: g.ffill().bfill())
                else:
                    df_clean[col] = df_clean[col].ffill().bfill()
                
                # Fill remaining NaNs with fitted train median
                fill_val = self.median_values.get(col, 0.0)
                df_clean[col] = df_clean[col].fillna(fill_val)
                
        # Re-attach exact raw stream quality flags
        for flag_col, flag_series in stream_flags.items():
            df_clean[flag_col] = flag_series.fillna(0.0)

        return df_clean

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.fit(df)
        return self.transform(df)


def get_model_features(df: pd.DataFrame, include_spatial: bool = False) -> pd.DataFrame:
    cols = list(FEATURE_COLUMNS)
    if include_spatial:
        cols.extend(SPATIAL_FEATURE_COLUMNS)
    
    # Filter columns actually present in dataframe
    available_cols = [c for c in cols if c in df.columns]
    return df[available_cols].copy()
