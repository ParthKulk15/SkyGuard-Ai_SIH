import pandas as pd
import numpy as np
import pytest
import torch
import sys
sys.path.insert(0, '.')

from src.anomaly_detection.autoencoder import SkyGuardAutoencoder


def test_autoencoder_training():
    df_sample = pd.DataFrame({
        'station_id': ['AWS001'] * 30,
        'temperature': np.random.normal(25, 2, 30),
        'pressure': np.random.normal(1005, 5, 30),
        'humidity': np.random.normal(65, 5, 30),
        'hour_sin': np.sin(np.linspace(0, 2*np.pi, 30)),
        'hour_cos': np.cos(np.linspace(0, 2*np.pi, 30)),
        'doy_sin': [0.5] * 30,
        'doy_cos': [-0.8] * 30,
        'temperature_delta': [0.1] * 30,
        'pressure_delta': [0.1] * 30,
        'humidity_delta': [0.1] * 30,
        'temperature_roll_mean': [25.0] * 30,
        'temperature_roll_std': [1.0] * 30,
        'temperature_roll_median': [25.0] * 30,
        'temperature_mad': [0.5] * 30,
        'temperature_residual': [0.0] * 30,
        'pressure_roll_mean': [1005.0] * 30,
        'pressure_roll_std': [1.0] * 30,
        'pressure_roll_median': [1005.0] * 30,
        'pressure_mad': [0.5] * 30,
        'pressure_residual': [0.0] * 30,
        'humidity_roll_mean': [65.0] * 30,
        'humidity_roll_std': [1.0] * 30,
        'humidity_roll_median': [65.0] * 30,
        'humidity_mad': [0.5] * 30,
        'humidity_residual': [0.0] * 30,
        'dew_point': [18.0] * 30,
        'temp_humidity_product': [1600.0] * 30,
        'temp_pressure_product': [25000.0] * 30,
        'temperature_missing': [0.0] * 30,
        'pressure_missing': [0.0] * 30,
        'humidity_missing': [0.0] * 30
    })
    
    ae = SkyGuardAutoencoder(random_state=42)
    ae.fit(df_sample, epochs=3, batch_size=16)
    preds, scores = ae.predict(df_sample)
    
    assert len(preds) == 30
    assert len(scores) == 30
    assert (scores >= 0.0).all() and (scores <= 1.0).all()
