import pandas as pd
import numpy as np
import pytest
import sys
sys.path.insert(0, '.')

from src.degradation.degradation_model import StationDegradationEvaluator


def test_station_health_score_calculation():
    evaluator = StationDegradationEvaluator()
    
    # Healthy station
    healthy_metrics = {
        'anomaly_frequency': 0.01,
        'anomaly_severity': 2.0,
        'station_disagreement': 0.05,
        'temperature_drift': 0.001
    }
    healthy_res = evaluator.evaluate_station(healthy_metrics)
    assert healthy_res['sensor_health_score'] >= 85.0
    assert healthy_res['degradation_level'] == 'HEALTHY'
    assert healthy_res['maintenance_priority'] == 'LOW'
    
    # Degraded station
    degraded_metrics = {
        'anomaly_frequency': 0.25,
        'anomaly_severity': 45.0,
        'station_disagreement': 0.35,
        'temperature_drift': 0.08
    }
    degraded_res = evaluator.evaluate_station(degraded_metrics)
    assert degraded_res['sensor_health_score'] < 75.0
    assert degraded_res['degradation_level'] in ['WATCH', 'CRITICAL']
