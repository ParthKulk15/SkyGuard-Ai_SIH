import pandas as pd
import numpy as np
from typing import Dict, Any


def generate_human_explanation(obs: Dict[str, Any], baseline_res: Dict[str, Any], spatial_res: Dict[str, Any], is_anomaly: int) -> str:
    """Generates precise human-readable natural language explanation for observation assessment."""
    if not is_anomaly:
        return "Observation is within normal physical bounds and in agreement with historical station trends and neighboring AWS stations."
        
    parts = []
    
    # Check baseline rules explanation
    if baseline_res.get('explanation') and "Normal observation" not in baseline_res.get('explanation'):
        parts.append(baseline_res['explanation'])
        
    # Check spatial inconsistency
    if spatial_res.get('is_spatially_inconsistent'):
        parts.append(spatial_res['spatial_explanation'])
        
    # Default feature-deviation fallback if no specific rule fired
    if not parts:
        t_res = obs.get('temperature_residual', 0.0)
        h_res = obs.get('humidity_residual', 0.0)
        p_res = obs.get('pressure_residual', 0.0)
        
        max_res_param = 'temperature'
        max_res_val = t_res
        if abs(h_res) > abs(max_res_val):
            max_res_param = 'humidity'
            max_res_val = h_res
        if abs(p_res) > abs(max_res_val):
            max_res_param = 'pressure'
            max_res_val = p_res
            
        parts.append(f"Observation exhibits anomalous multidimensional statistical divergence, primarily driven by {max_res_param} deviation ({max_res_val:+.2f} relative to rolling mean).")
        
    return " | ".join(parts)
