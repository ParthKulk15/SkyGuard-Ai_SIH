import pandas as pd
import numpy as np
import pytest
import sys
sys.path.insert(0, '.')

from src.spatial.spatial_consistency import SpatialConsistencyEvaluator


def test_spatial_divergence():
    evaluator = SpatialConsistencyEvaluator()
    obs_divergent = {
        'temperature': 35.0,
        'pressure': 1005.0,
        'humidity': 60.0,
        'neighbor_temperature_median': 24.0, # 11°C divergence from neighbors
        'neighbor_pressure_median': 1005.0,
        'neighbor_humidity_median': 60.0
    }
    res = evaluator.evaluate_observation(obs_divergent)
    assert res['is_spatially_inconsistent'] is True, "Spatial evaluator failed to detect station divergence!"
    assert res['spatial_consensus_score'] < 0.5


def test_spatial_consensus():
    evaluator = SpatialConsistencyEvaluator()
    obs_consensus = {
        'temperature': 25.0,
        'pressure': 1005.0,
        'humidity': 60.0,
        'neighbor_temperature_median': 25.2,
        'neighbor_pressure_median': 1005.1,
        'neighbor_humidity_median': 61.0
    }
    res = evaluator.evaluate_observation(obs_consensus)
    assert res['is_spatially_inconsistent'] is False
    assert res['spatial_consensus_score'] > 0.85
