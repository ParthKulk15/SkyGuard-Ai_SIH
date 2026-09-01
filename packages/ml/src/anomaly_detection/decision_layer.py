import pandas as pd
import numpy as np
from typing import Dict, Any

from src.anomaly_detection.baseline import RuleBaselineDetector
from src.spatial.spatial_consistency import SpatialConsistencyEvaluator
from src.anomaly_detection.explainability import generate_human_explanation


class SkyGuardDecisionLayer:

    def __init__(self, w_baseline: float = 0.35, w_iforest: float = 0.35, w_autoencoder: float = 0.30):
        self.w_baseline = w_baseline
        self.w_iforest = w_iforest
        self.w_autoencoder = w_autoencoder
        self.baseline_detector = RuleBaselineDetector()
        self.spatial_evaluator = SpatialConsistencyEvaluator()

    def evaluate(
        self,
        obs: Dict[str, Any],
        iforest_score: float = 0.0,
        autoencoder_score: float = 0.0,
        fault_type_pred: str = None,
        fault_conf: float = 0.0,
        health_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:

        # 1. Evaluate baseline rules
        base_res = self.baseline_detector.predict_observation(obs)
        
        # 2. Evaluate spatial consistency
        spatial_res = self.spatial_evaluator.evaluate_observation(obs)
        
        # 3. Fuse Anomaly Score
        # Hard overrides: physical out-of-bounds or missing data triggers immediate flag
        # Only packet-integrity, physical-limit, and multi-sensor failures are
        # hard overrides.  A lone short-term spike may be genuine weather and
        # needs corroboration from the learned/spatial layers.
        hard_fault_types = {
            'COMMUNICATION_FAILURE', 'DUPLICATE_PACKET', 'DATA_CORRUPTION',
            'SIMULTANEOUS_SENSOR_FAILURE'
        }
        is_hard_rule = base_res['fault_type'] in hard_fault_types
        
        combined_score = (
            self.w_baseline * base_res['anomaly_score'] +
            self.w_iforest * iforest_score +
            self.w_autoencoder * autoencoder_score
        )

        # The supervised classifier supplies a diagnosis, but it must be
        # corroborated by a rule or both unsupervised detectors before it can
        # raise an alarm. This prevents seasonal weather shifts from becoming
        # classifier-only false positives.
        classifier_is_supported = (
            fault_type_pred and fault_type_pred != 'NORMAL' and fault_conf >= 0.70
            and (base_res['anomaly_flag'] == 1 or (iforest_score >= 0.55 and autoencoder_score >= 0.55))
        )
        if classifier_is_supported:
            combined_score = max(combined_score, float(fault_conf))
        
        # Spatial adjustment: If station diverges from neighbors, increase anomaly score
        if spatial_res['is_spatially_inconsistent']:
            combined_score = min(1.0, combined_score + 0.20)
        # If nearby stations ALSO moved together (genuine regional weather event), decrease anomaly score
        elif obs.get('is_genuine_event', 0) == 1 or spatial_res['spatial_consensus_score'] > 0.85:
            combined_score = max(0.0, combined_score - 0.25)

        anomaly_flag = 1 if (combined_score >= 0.45 or is_hard_rule) else 0

        # Determine Severity
        if not anomaly_flag:
            severity = 'NONE'
        elif combined_score >= 0.80 or is_hard_rule:
            severity = 'CRITICAL' if is_hard_rule else 'HIGH'
        elif combined_score >= 0.60:
            severity = 'HIGH'
        else:
            severity = 'MEDIUM'

        # Determine Fault Type
        if anomaly_flag:
            if base_res['fault_type'] != 'NORMAL':
                final_fault = base_res['fault_type']
            elif fault_type_pred and fault_type_pred != 'NORMAL':
                final_fault = fault_type_pred
            elif spatial_res['is_spatially_inconsistent']:
                final_fault = 'SPATIAL_DISCREPANCY_FAULT'
            else:
                final_fault = 'MULTIVARIATE_ANOMALY'
        else:
            final_fault = 'NORMAL'

        # Confidence
        confidence = float(np.clip(max(combined_score if anomaly_flag else (1.0 - combined_score), fault_conf, 0.70), 0.0, 1.0))

        # Human Explanation
        explanation = generate_human_explanation(obs, base_res, spatial_res, anomaly_flag)

        default_health = {
            'sensor_health_score': 95.0,
            'degradation_level': 'HEALTHY',
            'maintenance_priority': 'LOW'
        }

        return {
            'anomaly_flag': int(anomaly_flag),
            'anomaly_score': round(float(combined_score), 4),
            'severity': severity,
            'fault_type': final_fault,
            'confidence': round(confidence, 4),
            'explanation': explanation,
            'sensor_health_info': health_info if health_info else default_health
        }
