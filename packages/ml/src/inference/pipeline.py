import pandas as pd
import numpy as np
import os
import json
from typing import Dict, Any, List

from src.anomaly_detection.hybrid_detector import SkyGuardHybridDetector
from src.features.feature_engineering import generate_engineed_features
from src.preprocessing.cleaner import DataCleaner


class SkyGuardInferenceEngine:
    """
    Production inference engine loading pre-trained SkyGuard models.
    Executes real-time observation assessment without retraining.
    Designed for direct integration into SIH / FastAPI / Flask / Dashboard APIs.
    """
    def __init__(self, models_dir: str = 'models'):
        self.models_dir = models_dir
        hybrid_path = os.path.join(models_dir, 'hybrid_detector.joblib')
        self.hybrid_detector = SkyGuardHybridDetector.load(hybrid_path) if os.path.exists(hybrid_path) else None
        if self.hybrid_detector is not None:
            return

        # Legacy ensemble fallback for installations without the v2 artifact.
        from src.anomaly_detection.isolation_forest import SkyGuardIsolationForest
        from src.anomaly_detection.autoencoder import SkyGuardAutoencoder
        from src.anomaly_detection.fault_classifier import SkyGuardFaultClassifier
        from src.degradation.degradation_model import StationDegradationEvaluator
        from src.anomaly_detection.decision_layer import SkyGuardDecisionLayer
        self.iforest = SkyGuardIsolationForest.load(
            os.path.join(models_dir, 'isolation_forest.joblib'),
            os.path.join(models_dir, 'isolation_forest_scaler.joblib')
            if os.path.exists(os.path.join(models_dir, 'isolation_forest_scaler.joblib'))
            else os.path.join(models_dir, 'scaler.joblib')
        )
        self.autoencoder = SkyGuardAutoencoder.load(
            os.path.join(models_dir, 'autoencoder.pt'),
            os.path.join(models_dir, 'autoencoder_scaler.joblib')
            if os.path.exists(os.path.join(models_dir, 'autoencoder_scaler.joblib'))
            else os.path.join(models_dir, 'scaler.joblib')
        )
        self.fault_classifier = SkyGuardFaultClassifier.load(
            os.path.join(models_dir, 'fault_classifier.joblib'),
            os.path.join(models_dir, 'fault_classifier_scaler.joblib')
            if os.path.exists(os.path.join(models_dir, 'fault_classifier_scaler.joblib'))
            else os.path.join(models_dir, 'scaler.joblib')
        )
        self.degradation_evaluator = StationDegradationEvaluator.load(
            os.path.join(models_dir, 'degradation_model.joblib')
        )
        self.decision_layer = SkyGuardDecisionLayer()

    def predict_observation(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assesses a single AWS sensor packet dictionary.
        Returns full anomaly detection, severity, fault classification, and explanation.
        """
        if self.hybrid_detector is not None:
            return self._format_hybrid_result(self.hybrid_detector.predict_observation(obs))
        df_obs = pd.DataFrame([obs])
        return self._predict_dataframe(df_obs)[0]

    @staticmethod
    def _format_hybrid_result(result: Dict[str, Any]) -> Dict[str, Any]:
        """Maintain the established inference response contract for v2."""
        result = dict(result)
        result["sensor_health_info"] = {
            "sensor_health_score": 95.0 if not result["anomaly_flag"] else 70.0,
            "degradation_level": "HEALTHY" if not result["anomaly_flag"] else "WATCH",
            "maintenance_priority": "LOW" if not result["anomaly_flag"] else "MEDIUM",
        }
        return result

    def _assess_prepared_observation(self, obs_clean: Dict[str, Any]) -> Dict[str, Any]:
        """Run model fusion on one already-featured and cleaned packet."""
        df_clean = pd.DataFrame([obs_clean])

        # 1. Isolation Forest score
        _, iforest_scores = self.iforest.predict(df_clean)
        iforest_score = float(iforest_scores[0])

        # 2. Autoencoder score
        _, ae_scores = self.autoencoder.predict(df_clean)
        ae_score = float(ae_scores[0])

        # 3. Supervised Fault Classification
        fault_type_pred, fault_conf = self.fault_classifier.predict_observation(obs_clean)

        # 4. Station Degradation Assessment
        health_info = self.degradation_evaluator.evaluate_station(obs_clean)

        # 5. Fused Decision Layer Synthesis
        assessment = self.decision_layer.evaluate(
            obs=obs_clean,
            iforest_score=iforest_score,
            autoencoder_score=ae_score,
            fault_type_pred=fault_type_pred,
            fault_conf=fault_conf,
            health_info=health_info
        )

        return assessment

    def _predict_dataframe(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Feature a complete stream before scoring it.

        This preserves per-station order, allowing duplicate-packet and
        temporal features to be computed against the preceding packet rather
        than treating every batch row as an unrelated singleton.
        """
        frame = df.copy()
        if 'humidity' not in frame.columns and 'relative_humidity' in frame.columns:
            frame['humidity'] = frame['relative_humidity']
        frame['_skyguard_input_order'] = np.arange(len(frame))
        df_feat = generate_engineed_features(frame)
        cleaner = DataCleaner()
        df_clean = cleaner.fit_transform(df_feat)
        df_clean = df_clean.sort_values('_skyguard_input_order')

        results = []
        for _, row in df_clean.iterrows():
            obs_clean = row.drop(labels=['_skyguard_input_order']).to_dict()
            results.append(self._assess_prepared_observation(obs_clean))
        return results

    def predict_single(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        """Alias for predict_observation for SIH / API convenience."""
        return self.predict_observation(obs)

    def predict_batch(self, df_or_list) -> List[Dict[str, Any]]:
        """Batch inference method for processing telemetry dataframes or JSON lists."""
        if self.hybrid_detector is not None:
            return [self._format_hybrid_result(result) for result in self.hybrid_detector.predict_batch(df_or_list)]
        df = pd.DataFrame(df_or_list) if isinstance(df_or_list, list) else df_or_list.copy()
        return self._predict_dataframe(df)
