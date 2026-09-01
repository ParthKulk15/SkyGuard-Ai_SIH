import pandas as pd
import numpy as np
import joblib
import os
from typing import Dict, Any, List, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

from src.preprocessing.cleaner import get_model_features, DataCleaner


class SkyGuardFaultClassifier:
    def __init__(self, n_estimators: int = 100, random_state: int = 42):
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=15,
            class_weight='balanced_subsample',
            random_state=random_state,
            n_jobs=-1,
        )
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_names = None
        self.cleaner = DataCleaner()

    def fit(self, df_train: pd.DataFrame, target_col: str = 'fault_type'):
        df_clean = self.cleaner.fit_transform(df_train)
        X_train = get_model_features(df_clean, include_spatial=False)
        self.feature_names = list(X_train.columns)

        X_scaled = self.scaler.fit_transform(X_train)
        y = self.label_encoder.fit_transform(df_train[target_col].astype(str))

        self.model.fit(X_scaled, y)
        return self

    def predict_observation(self, obs: Dict[str, Any]) -> Tuple[str, float]:

        df_single = pd.DataFrame([obs])
        df_clean = self.cleaner.transform(df_single)
        X = get_model_features(df_clean, include_spatial=False)
        
        for col in self.feature_names:
            if col not in X.columns:
                X[col] = 0.0
        X = X[self.feature_names]

        X_scaled = self.scaler.transform(X)
        probas = self.model.predict_proba(X_scaled)[0]
        max_idx = int(np.argmax(probas))
        fault_type = str(self.label_encoder.classes_[max_idx])
        confidence = float(probas[max_idx])

        return fault_type, confidence

    def predict_dataframe(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        df_clean = self.cleaner.transform(df)
        X = get_model_features(df_clean, include_spatial=False)
        
        for col in self.feature_names:
            if col not in X.columns:
                X[col] = 0.0
        X = X[self.feature_names]

        X_scaled = self.scaler.transform(X)
        preds_encoded = self.model.predict(X_scaled)
        preds_labels = self.label_encoder.inverse_transform(preds_encoded)
        
        probas = self.model.predict_proba(X_scaled)
        confidences = np.max(probas, axis=1)

        return preds_labels, confidences

    def predict_anomaly_probability(self, df: pd.DataFrame) -> np.ndarray:
        """Return P(any fault), rather than the confidence of one fault class."""
        df_clean = self.cleaner.transform(df)
        X = get_model_features(df_clean, include_spatial=False)
        for col in self.feature_names:
            if col not in X.columns:
                X[col] = 0.0
        X_scaled = self.scaler.transform(X[self.feature_names])
        probas = self.model.predict_proba(X_scaled)
        normal_index = np.where(self.label_encoder.classes_ == 'NORMAL')[0]
        normal_probability = probas[:, normal_index[0]] if len(normal_index) else 0.0
        return 1.0 - normal_probability

    def save(self, model_path: str, scaler_path: str):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'label_encoder': self.label_encoder,
            'feature_names': self.feature_names,
            'cleaner': self.cleaner
        }, model_path)
        joblib.dump(self.scaler, scaler_path)

    @classmethod
    def load(cls, model_path: str, scaler_path: str):
        data = joblib.load(model_path)
        inst = cls()
        inst.model = data['model']
        inst.label_encoder = data['label_encoder']
        inst.feature_names = data['feature_names']
        inst.cleaner = data.get('cleaner', DataCleaner())
        inst.scaler = joblib.load(scaler_path)
        return inst
