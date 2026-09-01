"""Create component-specific preprocessing artifacts without touching test data."""

from __future__ import annotations

from pathlib import Path
import sys

import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.anomaly_detection.isolation_forest import SkyGuardIsolationForest
from src.features.feature_engineering import generate_engineed_features
from src.preprocessing.cleaner import DataCleaner, get_model_features


def rebuild() -> None:
    raw = pd.read_csv(ROOT / 'pc_anomaly_training.csv')
    raw['timestamp'] = pd.to_datetime(raw['timestamp'])
    # Match the chronological training window used by the original evaluation.
    raw = raw.loc[raw['timestamp'] < pd.Timestamp('2026-05-14 00:00:00')].copy()
    featured = generate_engineed_features(raw)
    cleaned = DataCleaner().fit_transform(featured)
    models = ROOT / 'models'

    iforest = SkyGuardIsolationForest(mode='global', contamination=0.035, random_state=42)
    iforest.fit(cleaned)
    iforest.save(str(models / 'isolation_forest.joblib'), str(models / 'isolation_forest_scaler.joblib'))

    # The saved autoencoder expects a scaler trained on normal observations.
    normal = cleaned.loc[cleaned['is_anomaly'].eq(0)]
    auto_cleaner = DataCleaner()
    normal_clean = auto_cleaner.fit_transform(normal)
    auto_scaler = StandardScaler().fit(get_model_features(normal_clean, include_spatial=False))
    joblib.dump(auto_scaler, models / 'autoencoder_scaler.joblib')
    print('Wrote isolation_forest_scaler.joblib and autoencoder_scaler.joblib')


if __name__ == '__main__':
    rebuild()
