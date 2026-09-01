import pandas as pd
import numpy as np
import pytest
import sys
sys.path.insert(0, '.')

from src.anomaly_detection.isolation_forest import SkyGuardIsolationForest


def test_isolation_forest_global_training():
    df_sample = pd.DataFrame({
        'station_id': ['AWS001'] * 50,
        'temperature': np.random.normal(25, 2, 50),
        'pressure': np.random.normal(1005, 5, 50),
        'humidity': np.random.normal(65, 5, 50),
        'hour_sin': np.sin(np.linspace(0, 2*np.pi, 50)),
        'hour_cos': np.cos(np.linspace(0, 2*np.pi, 50)),
        'doy_sin': [0.5] * 50,
        'doy_cos': [-0.8] * 50,
        'temperature_delta': [0.1] * 50,
        'pressure_delta': [0.1] * 50,
        'humidity_delta': [0.1] * 50,
        'temperature_roll_mean': [25.0] * 50,
        'temperature_roll_std': [1.0] * 50,
        'temperature_roll_median': [25.0] * 50,
        'temperature_mad': [0.5] * 50,
        'temperature_residual': [0.0] * 50,
        'pressure_roll_mean': [1005.0] * 50,
        'pressure_roll_std': [1.0] * 50,
        'pressure_roll_median': [1005.0] * 50,
        'pressure_mad': [0.5] * 50,
        'pressure_residual': [0.0] * 50,
        'humidity_roll_mean': [65.0] * 50,
        'humidity_roll_std': [1.0] * 50,
        'humidity_roll_median': [65.0] * 50,
        'humidity_mad': [0.5] * 50,
        'humidity_residual': [0.0] * 50,
        'dew_point': [18.0] * 50,
        'temp_humidity_product': [1600.0] * 50,
        'temp_pressure_product': [25000.0] * 50,
        'temperature_missing': [0.0] * 50,
        'pressure_missing': [0.0] * 50,
        'humidity_missing': [0.0] * 50
    })
    
    model = SkyGuardIsolationForest(mode='global', contamination=0.05, random_state=42)
    model.fit(df_sample)
    preds, scores = model.predict(df_sample)
    
    assert len(preds) == 50
    assert len(scores) == 50
    assert (scores >= 0.0).all() and (scores <= 1.0).all()
