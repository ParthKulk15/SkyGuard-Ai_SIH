import pandas as pd
import numpy as np
import joblib
import os
from typing import Dict, Any
from sklearn.ensemble import RandomForestClassifier


class StationDegradationEvaluator:

    def __init__(self, random_state: int = 42):
        self.model = RandomForestClassifier(n_estimators=50, random_state=random_state)
        self.feature_names = [
            'anomaly_frequency', 'anomaly_severity', 'station_disagreement',
            'temperature_drift', 'pressure_drift', 'humidity_drift',
            'rolling_variance', 'repeated_fault_count'
        ]
        self.is_fitted = False

    def fit(self, df_deg: pd.DataFrame):
        X = df_deg[self.feature_names].fillna(0.0)
        y = df_deg['degradation_level']
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def calculate_health_score(self, metrics: Dict[str, Any]) -> float:
        """
        Calculates transparent 0-100 sensor health score.
        100 = Perfect station health, < 75 = Degradation Watch.
        """
        anom_freq = metrics.get('anomaly_frequency', 0.0) or 0.0
        anom_sev = metrics.get('anomaly_severity', 0.0) or 0.0
        disagreement = metrics.get('station_disagreement', 0.0) or 0.0
        drift_sum = (abs(metrics.get('temperature_drift', 0.0) or 0.0) +
                     abs(metrics.get('pressure_drift', 0.0) or 0.0) +
                     abs(metrics.get('humidity_drift', 0.0) or 0.0))
        
        penalty = (anom_freq * 120.0) + (anom_sev * 0.4) + (disagreement * 50.0) + (drift_sum * 100.0)
        health_score = float(np.clip(100.0 - penalty, 0.0, 100.0))
        return health_score

    def evaluate_station(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        health_score = self.calculate_health_score(metrics)
        
        if self.is_fitted:
            X_single = pd.DataFrame([{f: metrics.get(f, 0.0) for f in self.feature_names}]).fillna(0.0)
            deg_level = str(self.model.predict(X_single)[0])
        else:
            deg_level = "HEALTHY" if health_score >= 85.0 else ("WATCH" if health_score >= 70.0 else "CRITICAL")
            
        maint_priority = "LOW" if deg_level == "HEALTHY" else ("MEDIUM" if deg_level == "WATCH" else "HIGH")
        
        return {
            'sensor_health_score': health_score,
            'degradation_level': deg_level,
            'maintenance_priority': maint_priority
        }

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'is_fitted': self.is_fitted,
            'feature_names': self.feature_names
        }, path)

    @classmethod
    def load(cls, path: str):
        data = joblib.load(path)
        inst = cls()
        inst.model = data['model']
        inst.is_fitted = data['is_fitted']
        inst.feature_names = data['feature_names']
        return inst
