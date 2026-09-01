import pandas as pd
import numpy as np
import pytest
import sys
sys.path.insert(0, '.')

from src.inference.pipeline import SkyGuardInferenceEngine


def test_inference_pipeline_execution():
    engine = SkyGuardInferenceEngine(models_dir='models')
    
    # Normal sample observation
    norm_obs = {
        'station_id': 'AWS001',
        'timestamp': '2026-05-30 12:00:00',
        'temperature': 25.4,
        'relative_humidity': 65.0,
        'pressure': 1008.5,
        'temperature_delta': 0.1,
        'pressure_delta': 0.05,
        'humidity_delta': 0.2
    }
    
    res = engine.predict_observation(norm_obs)
    
    assert 'anomaly_flag' in res
    assert 'anomaly_score' in res
    assert 'severity' in res
    assert 'fault_type' in res
    assert 'confidence' in res
    assert 'explanation' in res
    assert 'sensor_health_info' in res
    
    assert res['anomaly_flag'] in [0, 1]
    assert 0.0 <= res['anomaly_score'] <= 1.0
    assert 0.0 <= res['confidence'] <= 1.0
    assert isinstance(res['explanation'], str) and len(res['explanation']) > 0


def test_inference_pipeline_anomalous_sample():
    engine = SkyGuardInferenceEngine(models_dir='models')
    
    # Extreme anomaly observation (humidity out of bounds)
    anom_obs = {
        'station_id': 'AWS002',
        'timestamp': '2026-05-30 14:30:00',
        'temperature': 26.0,
        'relative_humidity': 130.0, # Physical out of bounds violation
        'pressure': 1007.0
    }
    
    res = engine.predict_observation(anom_obs)
    assert res['anomaly_flag'] == 1, "Inference pipeline failed to flag extreme anomaly sample!"
    assert res['severity'] in ['HIGH', 'CRITICAL']
