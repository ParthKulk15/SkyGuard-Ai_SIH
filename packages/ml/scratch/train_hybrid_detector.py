"""Train SkyGuard's deployable hybrid detector and publish an honest report."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.anomaly_detection.hybrid_detector import SkyGuardHybridDetector
from src.evaluation.metrics import compute_binary_metrics


def metrics_for(model: SkyGuardHybridDetector, data: pd.DataFrame) -> dict:
    predictions = model.predict_batch(data)
    flags = [result["anomaly_flag"] for result in predictions]
    return compute_binary_metrics(data["is_anomaly"].to_numpy(), flags)


def train() -> dict:
    raw = pd.read_csv(ROOT / "pc_anomaly_training.csv")
    raw["timestamp"] = pd.to_datetime(raw["timestamp"])
    cutoff = pd.Timestamp("2026-05-14 00:00:00")
    train_data = raw.loc[raw["timestamp"] < cutoff].copy()
    validation_data = raw.loc[raw["timestamp"] >= cutoff].copy()
    test_data = pd.read_csv(ROOT / "test_dataset.csv")

    model = SkyGuardHybridDetector().fit(train_data)
    model.save(str(ROOT / "models" / "hybrid_detector.joblib"))
    report = {
        "model_version": model.metadata["version"],
        "training_rows": int(len(train_data)),
        "validation_rows": int(len(validation_data)),
        "held_out_test_rows": int(len(test_data)),
        "validation_metrics": metrics_for(model, validation_data),
        "held_out_test_metrics": metrics_for(model, test_data),
        "artifact": "models/hybrid_detector.joblib",
    }
    (ROOT / "models" / "hybrid_model_config.json").write_text(json.dumps(model.metadata | {"config": model.config}, indent=2), encoding="utf-8")
    (ROOT / "reports" / "hybrid_detector_evaluation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (ROOT / "reports" / "hybrid_model_card.md").write_text(
        "# SkyGuard Hybrid Detector Model Card\n\n"
        "## Intended use\n\nDetect packet integrity, physical-range, duplicate, frozen, spike, and joint sensor faults in weather-station telemetry.\n\n"
        "## Evaluation\n\n"
        f"- Chronological validation F1: {report['validation_metrics']['f1']:.4f}\n"
        f"- Held-out test F1: {report['held_out_test_metrics']['f1']:.4f}\n"
        f"- Held-out test accuracy: {report['held_out_test_metrics']['accuracy']:.4f}\n\n"
        "## Limitations\n\nThe historical labels are synthetic and strongly imbalanced. The model must be monitored against real labeled field faults before autonomous maintenance or correction actions are enabled.\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    train()
