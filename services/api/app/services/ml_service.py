from __future__ import annotations

import logging
import sys
from threading import Lock
from typing import Any

from app.config import get_settings

logger = logging.getLogger(__name__)


class MLService:
    def __init__(self) -> None:
        self._engine: Any | None = None
        self._error: str | None = None
        self._lock = Lock()

    @property
    def available(self) -> bool:
        self._ensure_engine()
        return self._engine is not None

    @property
    def error(self) -> str | None:
        self._ensure_engine()
        return self._error

    def _ensure_engine(self) -> None:
        if self._engine is not None or self._error is not None:
            return
        with self._lock:
            if self._engine is not None or self._error is not None:
                return
            settings = get_settings()
            ml_root = settings.ml_root
            try:
                if str(ml_root) not in sys.path:
                    sys.path.insert(0, str(ml_root))
                from src.inference.pipeline import SkyGuardInferenceEngine

                self._engine = SkyGuardInferenceEngine(models_dir=str(settings.ml_models_dir))
                logger.info("SkyGuard ML inference engine initialized from %s", settings.ml_models_dir)
            except Exception as exc:  # pragma: no cover - exact dependency failures vary by machine.
                self._error = f"{type(exc).__name__}: {exc}"
                logger.exception("Failed to initialize SkyGuard ML inference engine")

    def predict(self, observation: dict[str, Any]) -> dict[str, Any]:
        self._ensure_engine()
        if self._engine is None:
            return {
                "model_available": False,
                "simulated": False,
                "error": self._error,
                "anomaly_flag": 0,
                "anomaly_score": 0.0,
                "fault_type": "MODEL_UNAVAILABLE",
                "severity": "UNKNOWN",
                "confidence": 0.0,
                "explanation": "ML inference engine is not available in this local environment.",
                "sensor_health_info": {"sensor_health_score": 0.0, "degradation_level": "UNKNOWN", "maintenance_priority": "UNKNOWN"},
            }
        payload = dict(observation)
        if "humidity" not in payload and "relative_humidity" in payload:
            payload["humidity"] = payload["relative_humidity"]
        result = self._engine.predict_batch([payload])[0]
        result["model_available"] = True
        result["simulated"] = False
        return result


ml_service = MLService()
