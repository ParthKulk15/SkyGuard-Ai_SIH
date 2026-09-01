import pandas as pd
import numpy as np
import pytest
import sys
sys.path.insert(0, '.')

from src.anomaly_detection.decision_layer import SkyGuardDecisionLayer


def test_decision_layer_fusion():
    layer = SkyGuardDecisionLayer()
    obs_norm = {
        'temperature': 25.0,
        'pressure': 1005.0,
        'humidity': 65.0,
        'neighbor_temperature_median': 25.1,
        'neighbor_pressure_median': 1005.0,
        'neighbor_humidity_median': 65.0
    }
    
    res = layer.evaluate(
        obs=obs_norm,
        iforest_score=0.1,
        autoencoder_score=0.1,
        fault_type_pred='NORMAL',
        fault_conf=0.95
    )
    
    assert res['anomaly_flag'] == 0
    assert res['severity'] == 'NONE'
    assert res['fault_type'] == 'NORMAL'
    assert res['anomaly_score'] < 0.45
