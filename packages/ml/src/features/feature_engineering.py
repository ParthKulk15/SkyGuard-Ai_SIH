import pandas as pd
import numpy as np


def compute_dew_point(temp_c: pd.Series, rel_hum: pd.Series) -> pd.Series:
    """Magnus formula approximation for dew point temperature (°C). Safely handles NaNs."""
    temp_num = pd.to_numeric(temp_c, errors='coerce')
    hum_num = pd.to_numeric(rel_hum, errors='coerce')
    
    a = 17.27
    b = 237.7
    valid_hum = np.maximum(hum_num.fillna(50.0), 1e-4)
    alpha = ((a * temp_num) / (b + temp_num)) + np.log(valid_hum / 100.0)
    dew_point = (b * alpha) / (a - alpha)
    return dew_point


def compute_persistence(series: pd.Series) -> pd.Series:
    """Calculates consecutive identical readings count for a sensor series."""
    diff = series.diff() != 0
    run_id = diff.cumsum()
    counts = series.groupby(run_id).cumcount() + 1
    return counts


def generate_engineed_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes all legitimate features without target leakage or future information.
    Ensures input dataframe is sorted by station_id and timestamp.
    Raw stream quality indicators (missing values, duplicate packets) are captured BEFORE imputation.
    """
    df_feat = df.copy()
    if 'station_id' in df_feat.columns and 'timestamp' in df_feat.columns:
        # Temporal features must never cross station histories or be computed
        # from caller-dependent row order.
        df_feat = df_feat.sort_values(['station_id', 'timestamp']).reset_index(drop=True)
    
    if 'timestamp' in df_feat.columns:
        df_feat['dt'] = pd.to_datetime(df_feat['timestamp'], errors='coerce')
        df_feat['hour'] = df_feat['dt'].dt.hour.fillna(12)
        df_feat['day_of_year'] = df_feat['dt'].dt.dayofyear.fillna(150)
        
        # Cyclical temporal features
        df_feat['hour_sin'] = np.sin(2 * np.pi * df_feat['hour'] / 24.0)
        df_feat['hour_cos'] = np.cos(2 * np.pi * df_feat['hour'] / 24.0)
        df_feat['doy_sin'] = np.sin(2 * np.pi * df_feat['day_of_year'] / 365.25)
        df_feat['doy_cos'] = np.cos(2 * np.pi * df_feat['day_of_year'] / 365.25)

    # 1. RAW STREAM MISSING INDICATORS (Captured BEFORE DataCleaner imputation)
    df_feat['temperature_missing'] = df_feat['temperature'].isna().astype(float)
    df_feat['pressure_missing'] = df_feat['pressure'].isna().astype(float)
    df_feat['humidity_missing'] = df_feat['humidity'].isna().astype(float)
    df_feat['raw_is_missing'] = (df_feat['temperature_missing'] + df_feat['pressure_missing'] + df_feat['humidity_missing'] > 0).astype(float)

    # 2. RAW CONSECUTIVE DUPLICATE PACKET DETECTOR (Captured on raw stream per station)
    if 'station_id' in df_feat.columns:
        d_temp = (df_feat.groupby('station_id')['temperature'].diff() == 0)
        d_press = (df_feat.groupby('station_id')['pressure'].diff() == 0)
        d_hum = (df_feat.groupby('station_id')['humidity'].diff() == 0)
    else:
        d_temp = (df_feat['temperature'].diff() == 0)
        d_press = (df_feat['pressure'].diff() == 0)
        d_hum = (df_feat['humidity'].diff() == 0)
        
    computed_duplicate = (d_temp & d_press & d_hum).fillna(False).astype(float)
    # A streaming caller may already have compared the packet with retained
    # state. Preserve that stronger signal when feature engineering receives
    # a single packet rather than the full preceding sequence.
    if 'raw_is_duplicate_packet' in df_feat.columns:
        supplied_duplicate = pd.to_numeric(df_feat['raw_is_duplicate_packet'], errors='coerce').fillna(0.0)
        df_feat['raw_is_duplicate_packet'] = np.maximum(computed_duplicate, supplied_duplicate)
    else:
        df_feat['raw_is_duplicate_packet'] = computed_duplicate

    # Calculate persistence (frozen value length) per station
    if 'station_id' in df_feat.columns:
        df_feat['temp_persistence'] = df_feat.groupby('station_id')['temperature'].transform(compute_persistence)
        df_feat['press_persistence'] = df_feat.groupby('station_id')['pressure'].transform(compute_persistence)
        df_feat['hum_persistence'] = df_feat.groupby('station_id')['humidity'].transform(compute_persistence)
    else:
        df_feat['temp_persistence'] = compute_persistence(df_feat['temperature'])
        df_feat['press_persistence'] = compute_persistence(df_feat['pressure'])
        df_feat['hum_persistence'] = compute_persistence(df_feat['humidity'])

    # Calculate causal temporal features when raw telemetry is supplied.  The
    # historical CSVs already contain these columns; preserving them keeps
    # backward compatibility while live packets gain the same feature schema.
    grouped = df_feat.groupby('station_id', sort=False) if 'station_id' in df_feat.columns else None
    for sensor in ('temperature', 'pressure', 'humidity'):
        values = pd.to_numeric(df_feat[sensor], errors='coerce')
        if grouped is not None:
            delta = grouped[sensor].diff()
            roll_mean = grouped[sensor].transform(lambda s: pd.to_numeric(s, errors='coerce').rolling(6, min_periods=2).mean())
            roll_std = grouped[sensor].transform(lambda s: pd.to_numeric(s, errors='coerce').rolling(6, min_periods=2).std())
            roll_median = grouped[sensor].transform(lambda s: pd.to_numeric(s, errors='coerce').rolling(6, min_periods=2).median())
            roll_mad = grouped[sensor].transform(
                lambda s: pd.to_numeric(s, errors='coerce').rolling(6, min_periods=2).apply(
                    lambda x: float(np.median(np.abs(x - np.median(x)))), raw=True
                )
            )
        else:
            delta = values.diff()
            roll_mean = values.rolling(6, min_periods=2).mean()
            roll_std = values.rolling(6, min_periods=2).std()
            roll_median = values.rolling(6, min_periods=2).median()
            roll_mad = values.rolling(6, min_periods=2).apply(
                lambda x: float(np.median(np.abs(x - np.median(x)))), raw=True
            )

        for column, generated in {
            f'{sensor}_delta': delta,
            f'{sensor}_roll_mean': roll_mean,
            f'{sensor}_roll_std': roll_std,
            f'{sensor}_roll_median': roll_median,
            f'{sensor}_mad': roll_mad,
            f'{sensor}_residual': values - roll_mean,
        }.items():
            if column not in df_feat.columns:
                df_feat[column] = generated

    # Dew point & Physical products
    if 'dew_point' not in df_feat.columns or df_feat['dew_point'].isna().any():
        df_feat['dew_point'] = compute_dew_point(df_feat['temperature'], df_feat['humidity'])
        
    temp_num = pd.to_numeric(df_feat['temperature'], errors='coerce').fillna(20.0)
    hum_num = pd.to_numeric(df_feat['humidity'], errors='coerce').fillna(50.0)
    press_num = pd.to_numeric(df_feat['pressure'], errors='coerce').fillna(1013.25)

    df_feat['temp_humidity_product'] = temp_num * hum_num
    df_feat['temp_pressure_product'] = temp_num * press_num
    
    return df_feat
