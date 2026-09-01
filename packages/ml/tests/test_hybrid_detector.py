import pandas as pd

from src.anomaly_detection.hybrid_detector import SkyGuardHybridDetector


def _training_data():
    return pd.DataFrame([
        {"station_id": "AWS001", "timestamp": "2026-01-01 00:00:00", "temperature": 20.0, "pressure": 1005.0, "humidity": 70.0, "is_anomaly": 0},
        {"station_id": "AWS001", "timestamp": "2026-01-01 00:05:00", "temperature": 20.1, "pressure": 1005.1, "humidity": 70.2, "is_anomaly": 0},
    ])


def test_hybrid_detector_detects_physical_corruption():
    detector = SkyGuardHybridDetector().fit(_training_data())
    result = detector.predict_observation({"station_id": "AWS001", "timestamp": "2026-01-01 00:10:00", "temperature": 20.0, "pressure": 1005.0, "humidity": 120.0})
    assert result["anomaly_flag"] == 1
    assert result["fault_type"] == "DATA_CORRUPTION"


def test_hybrid_detector_detects_duplicate_stream_packet():
    detector = SkyGuardHybridDetector().fit(_training_data())
    first = {"station_id": "AWS001", "timestamp": "2026-01-01 00:10:00", "temperature": 21.0, "pressure": 1006.0, "humidity": 71.0}
    detector.predict_observation(first)
    second = dict(first, timestamp="2026-01-01 00:15:00")
    result = detector.predict_observation(second)
    assert result["anomaly_flag"] == 1
    assert result["fault_type"] == "DUPLICATE_PACKET"
