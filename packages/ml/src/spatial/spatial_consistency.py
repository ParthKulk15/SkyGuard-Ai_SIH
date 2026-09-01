import pandas as pd
import numpy as np
from typing import Dict, Any


class SpatialConsistencyEvaluator:
    """
    Evaluates spatial consistency between an AWS station and neighboring stations
    to distinguish genuine regional weather events from isolated sensor faults.
    """
    def __init__(self, temp_diff_threshold: float = 4.0, press_diff_threshold: float = 5.0, hum_diff_threshold: float = 15.0):
        self.temp_diff_threshold = temp_diff_threshold
        self.press_diff_threshold = press_diff_threshold
        self.hum_diff_threshold = hum_diff_threshold

    def evaluate_observation(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        temp = obs.get('temperature', None)
        press = obs.get('pressure', None)
        hum = obs.get('humidity', None)
        
        n_temp = obs.get('neighbor_temperature_median', None)
        n_press = obs.get('neighbor_pressure_median', None)
        n_hum = obs.get('neighbor_humidity_median', None)
        
        # Spatial residuals (Station reading minus neighbor median)
        r_temp = obs.get('spatial_residual_temperature', (temp - n_temp) if (temp is not None and n_temp is not None) else 0.0)
        r_press = obs.get('spatial_residual_pressure', (press - n_press) if (press is not None and n_press is not None) else 0.0)
        r_hum = obs.get('spatial_residual_humidity', (hum - n_hum) if (hum is not None and n_hum is not None) else 0.0)
        
        abs_r_temp = abs(r_temp or 0.0)
        abs_r_press = abs(r_press or 0.0)
        abs_r_hum = abs(r_hum or 0.0)
        
        is_spatially_inconsistent = False
        explanations = []
        
        if abs_r_temp >= self.temp_diff_threshold:
            is_spatially_inconsistent = True
            explanations.append(f"Temperature deviates by {r_temp:+.1f}°C from regional neighbor median ({n_temp:.1f}°C).")
            
        if abs_r_press >= self.press_diff_threshold:
            is_spatially_inconsistent = True
            explanations.append(f"Pressure deviates by {r_press:+.1f} hPa from regional neighbor median ({n_press:.1f} hPa).")
            
        if abs_r_hum >= self.hum_diff_threshold:
            is_spatially_inconsistent = True
            explanations.append(f"Relative humidity deviates by {r_hum:+.1f}% from regional neighbor median ({n_hum:.1f}%).")
            
        # Consensus score (1.0 = full agreement with neighbors, 0.0 = total isolated divergence)
        max_dev = max(abs_r_temp / self.temp_diff_threshold, abs_r_press / self.press_diff_threshold, abs_r_hum / self.hum_diff_threshold)
        spatial_consensus_score = float(np.clip(1.0 - (max_dev / 3.0), 0.0, 1.0))
        spatial_fault_score = float(np.clip(max_dev / 2.0, 0.0, 1.0))
        
        return {
            'is_spatially_inconsistent': is_spatially_inconsistent,
            'spatial_consensus_score': spatial_consensus_score,
            'spatial_fault_score': spatial_fault_score,
            'residual_temp': float(r_temp or 0.0),
            'residual_press': float(r_press or 0.0),
            'residual_hum': float(r_hum or 0.0),
            'spatial_explanation': " | ".join(explanations) if explanations else "Observation is in high spatial consensus with surrounding AWS stations."
        }
