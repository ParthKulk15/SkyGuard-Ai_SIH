import pandas as pd
import numpy as np
import pytest
import sys
sys.path.insert(0, '.')

from src.anomaly_detection.baseline import RuleBaselineDetector


def test_baseline_spike_detection():
    detector = RuleBaselineDetector()
    obs_spike = {
        'temperature': 35.0,
        'pressure': 1005.0,
        'humidity': 60.0,
        'temperature_delta': 7.5, # Exceeds 3.0°C threshold
        'pressure_delta': 0.1,
        'humidity_delta': 1.0
    }
    res = detector.predict_observation(obs_spike)
    assert res['anomaly_flag'] == 1, "Baseline failed to flag temperature spike!"
    assert 'TEMPERATURE_SPIKE' in res['fault_type'] or 'SPIKE' in res['fault_type']


def test_baseline_out_of_bounds():
    detector = RuleBaselineDetector()
    obs_oob = {
        'temperature': 25.0,
        'pressure': 1005.0,
        'humidity': 135.0, # Physical violation (>100%)
    }
    res = detector.predict_observation(obs_oob)
    assert res['anomaly_flag'] == 1, "Baseline failed to flag humidity > 100%!"
    assert res['fault_type'] == 'DATA_CORRUPTION'
    assert res['severity'] == 'CRITICAL'


def test_baseline_normal():
    detector = RuleBaselineDetector()
    obs_norm = {
        'temperature': 25.0,
        'pressure': 1005.0,
        'humidity': 65.0,
        'temperature_delta': 0.2,
        'pressure_delta': 0.1,
        'humidity_delta': 0.5,
        'temp_persistence': 1
    }
    res = detector.predict_observation(obs_norm)
    assert res['anomaly_flag'] == 0, "Baseline flagged a normal observation!"
    assert res['fault_type'] == 'NORMAL'


def test_baseline_simultaneous_sensor_failure():
    detector = RuleBaselineDetector()
    res = detector.predict_observation({
        'temperature': 42.0, 'pressure': 1028.0, 'humidity': 80.0,
        'temperature_residual': 12.0, 'pressure_residual': 11.0,
    })
    assert res['anomaly_flag'] == 1
    assert res['fault_type'] == 'SIMULTANEOUS_SENSOR_FAILURE'
