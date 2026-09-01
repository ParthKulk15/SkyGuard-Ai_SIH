import pandas as pd
import numpy as np
import joblib
from typing import Dict, Any, Tuple, List
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, precision_score, recall_score
import os

from src.preprocessing.cleaner import get_model_features, FEATURE_COLUMNS, DataCleaner


class SkyGuardIsolationForest:
    def __init__(self, mode: str = 'global', contamination: float = 0.035, random_state: int = 42):
        assert mode in ['global', 'station_specific'], "mode must be 'global' or 'station_specific'"
        self.mode = mode
        self.contamination = contamination
        self.random_state = random_state
        self.global_model = None
        self.station_models = {}
        self.scaler = StandardScaler()
        self.threshold = 0.5
        self.feature_names = None

    def fit(self, df_train: pd.DataFrame):
        cleaner = DataCleaner()
        df_clean = cleaner.fit_transform(df_train)
        X_train = get_model_features(df_clean, include_spatial=False)
        self.feature_names = list(X_train.columns)

        # Scale features
        X_scaled = self.scaler.fit_transform(X_train)
        df_scaled = pd.DataFrame(X_scaled, columns=self.feature_names, index=df_clean.index)

        if self.mode == 'global':
            self.global_model = IsolationForest(
                n_estimators=150,
                contamination=self.contamination,
                random_state=self.random_state,
                n_jobs=-1
            )
            self.global_model.fit(df_scaled)
        else:
            df_scaled['station_id'] = df_clean['station_id']
            for station, group in df_scaled.groupby('station_id'):
                X_st = group.drop(columns=['station_id'])
                model = IsolationForest(
                    n_estimators=150,
                    contamination=self.contamination,
                    random_state=self.random_state,
                    n_jobs=-1
                )
                model.fit(X_st)
                self.station_models[station] = model

        return self

    def predict_raw_scores(self, df: pd.DataFrame) -> np.ndarray:

        cleaner = DataCleaner()
        df_clean = cleaner.transform(df)
        X = get_model_features(df_clean, include_spatial=False)
        
        # Ensure all columns present
        for col in self.feature_names:
            if col not in X.columns:
                X[col] = 0.0
        X = X[self.feature_names]

        X_scaled = self.scaler.transform(X)
        df_scaled = pd.DataFrame(X_scaled, columns=self.feature_names, index=df_clean.index)

        if self.mode == 'global':
            # decision_function returns negative values for anomalies, positive for normal
            raw_scores = -self.global_model.decision_function(df_scaled)
        else:
            df_scaled['station_id'] = df_clean['station_id']
            raw_scores = np.zeros(len(df_scaled))
            for station, group in df_scaled.groupby('station_id'):
                idx = group.index
                X_st = group.drop(columns=['station_id'])
                if station in self.station_models:
                    model = self.station_models[station]
                else:
                    # Fallback to first station model if unknown station
                    model = list(self.station_models.values())[0]
                raw_scores[idx] = -model.decision_function(X_st)
                
        # Normalize raw scores to [0, 1] range using min-max scaling adjustment
        min_s, max_s = raw_scores.min(), raw_scores.max()
        if max_s > min_s:
            norm_scores = (raw_scores - min_s) / (max_s - min_s)
        else:
            norm_scores = np.zeros_like(raw_scores)
            
        return norm_scores

    def tune_threshold(self, df_val: pd.DataFrame, y_val: np.ndarray) -> float:
        scores = self.predict_raw_scores(df_val)
        best_f1 = 0.0
        best_thresh = 0.5
        
        for thresh in np.linspace(0.1, 0.9, 81):
            preds = (scores >= thresh).astype(int)
            score_f1 = f1_score(y_val, preds, zero_division=0)
            if score_f1 > best_f1:
                best_f1 = score_f1
                best_thresh = thresh
                
        self.threshold = float(best_thresh)
        return self.threshold

    def predict(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        scores = self.predict_raw_scores(df)
        preds = (scores >= self.threshold).astype(int)
        return preds, scores

    def save(self, model_path: str, scaler_path: str):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump({
            'mode': self.mode,
            'contamination': self.contamination,
            'threshold': self.threshold,
            'global_model': self.global_model,
            'station_models': self.station_models,
            'feature_names': self.feature_names
        }, model_path)
        joblib.dump(self.scaler, scaler_path)

    @classmethod
    def load(cls, model_path: str, scaler_path: str):
        data = joblib.load(model_path)
        inst = cls(mode=data['mode'], contamination=data['contamination'])
        inst.threshold = data['threshold']
        inst.global_model = data['global_model']
        inst.station_models = data['station_models']
        inst.feature_names = data['feature_names']
        inst.scaler = joblib.load(scaler_path)
        return inst
