"""Deterministic synthetic weather telemetry for UI/backend development."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterator, Optional

import math
import random


FAULT_CYCLE = ("NORMAL", "NORMAL", "NORMAL", "TEMPERATURE_SPIKE", "NORMAL", "DATA_CORRUPTION", "NORMAL", "DUPLICATE_PACKET", "NORMAL", "SIMULTANEOUS_SENSOR_FAILURE")


@dataclass
class DemoTelemetryGenerator:
    """Generate realistic-looking packets without requiring physical sensors.

    The generated payload matches the ESP32 MQTT contract. ``fault_every`` is
    measured in emitted packets and ``seed`` makes browser/backend demos
    reproducible. Use ``fault_sequence`` to force a particular scenario.
    """

    device_id: str = "AWS-DEMO-001"
    seed: int = 42
    interval_seconds: int = 5
    fault_every: int = 10
    start_time: Optional[datetime] = None
    fault_sequence: Optional[tuple[str, ...]] = None

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)
        self._index = 0
        self._time = self.start_time or datetime.now(timezone.utc)
        self._last: Optional[Dict[str, float]] = None

    def next(self) -> Dict[str, object]:
        """Return one packet and advance the simulated station clock."""
        phase = self._index / 12.0
        temperature = 25.0 + 5.0 * math.sin(phase) + self._rng.gauss(0, 0.12)
        pressure = 1008.0 + 4.0 * math.cos(phase / 2) + self._rng.gauss(0, 0.08)
        humidity = 68.0 - 10.0 * math.sin(phase) + self._rng.gauss(0, 0.5)
        fault = self._fault_for_index(self._index)

        if fault == "TEMPERATURE_SPIKE":
            temperature += 12.0
        elif fault == "DATA_CORRUPTION":
            humidity = 130.0
        elif fault == "SIMULTANEOUS_SENSOR_FAILURE":
            temperature += 18.0
            pressure += 18.0
        elif fault == "COMMUNICATION_FAILURE":
            temperature = pressure = humidity = None
        elif fault == "DUPLICATE_PACKET" and self._last is not None:
            temperature = self._last["temperature"]
            pressure = self._last["pressure"]
            humidity = self._last["humidity"]

        packet: Dict[str, object] = {
            "device_id": self.device_id,
            "timestamp": self._time.isoformat().replace("+00:00", "Z"),
            "temperature": None if temperature is None else round(temperature, 3),
            "pressure": None if pressure is None else round(pressure, 3),
            "humidity": None if humidity is None else round(humidity, 3),
            "edge_anomaly": fault != "NORMAL",
            "edge_score": 0.05 if fault == "NORMAL" else 0.95,
            "edge_fault_type": fault,
            "model_version": "tinyml-demo-v1",
            "firmware_version": "demo-1.0.0",
            "demo_mode": True,
        }
        if temperature is not None:
            self._last = {"temperature": temperature, "pressure": pressure, "humidity": humidity}  # type: ignore[dict-item]
        self._index += 1
        self._time += timedelta(seconds=self.interval_seconds)
        return packet

    def _fault_for_index(self, index: int) -> str:
        if self.fault_sequence:
            return self.fault_sequence[index % len(self.fault_sequence)]
        if self.fault_every <= 0 or index == 0 or index % self.fault_every:
            return "NORMAL"
        return FAULT_CYCLE[(index // self.fault_every) % len(FAULT_CYCLE)]

    def stream(self, count: Optional[int] = None) -> Iterator[Dict[str, object]]:
        emitted = 0
        while count is None or emitted < count:
            yield self.next()
            emitted += 1
