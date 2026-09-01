import pandas as pd
import numpy as np
import pytest
import sys
sys.path.insert(0, '.')

from src.features.feature_engineering import generate_engineed_features, compute_dew_point, compute_persistence


def test_dew_point_calculation():
    temp = pd.Series([25.0, 30.0, 15.0])
    hum = pd.Series([60.0, 80.0, 90.0])
    dp = compute_dew_point(temp, hum)
    assert len(dp) == 3
    assert (dp < temp).all(), "Dew point temperature cannot exceed ambient dry bulb temperature!"


def test_persistence_calculation():
    s = pd.Series([25.0, 25.0, 25.0, 26.0, 26.0, 27.0])
    pers = compute_persistence(s)
    assert list(pers) == [1, 2, 3, 1, 2, 1], f"Expected [1,2,3,1,2,1], got {list(pers)}"


def test_engineered_features_generation():
    df_sample = pd.DataFrame([
        {'station_id': 'AWS001', 'timestamp': '2026-05-01 12:00:00', 'temperature': 25.0, 'pressure': 1008.0, 'humidity': 65.0},
        {'station_id': 'AWS001', 'timestamp': '2026-05-01 12:05:00', 'temperature': 25.0, 'pressure': 1008.0, 'humidity': 65.0}
    ])
    df_feat = generate_engineed_features(df_sample)
    
    assert 'hour_sin' in df_feat.columns
    assert 'hour_cos' in df_feat.columns
    assert 'dew_point' in df_feat.columns
    assert 'temp_persistence' in df_feat.columns
    assert df_feat.iloc[1]['temp_persistence'] == 2
