"""Deployable, state-aware hybrid fault detector for SkyGuard AI."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List

import joblib
import numpy as np
import pandas as pd

from src.anomaly_detection.baseline import RuleBaselineDetector
from src.features.feature_engineering import generate_engineed_features


MODEL_VERSION = "2.0.0-hybrid-operational"
HARD_FAULTS = {
    "COMMUNICATION_FAILURE", "DUPLICATE_PACKET", "DATA_CORRUPTION", "SIMULTANEOUS_SENSOR_FAILURE"
}


@dataclass
class SkyGuardHybridDetector:
    """Rules-first detector with fitted station profiles and stream state.

    Critical integrity faults are deterministic.  Fitted station profiles add
    a second independent signal for joint temperature/pressure excursions.
    The detector is intentionally self-contained and has no neural-network
    runtime dependency, making it suitable for server or edge-adjacent use.
    """

    config: Dict[str, float] = field(default_factory=lambda: {
        "joint_profile_z_threshold": 3.5,
        "joint_residual_threshold": 8.0,
    })
    profiles: Dict[str, Dict[str, float]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    _last_packet: Dict[str, Dict[str, Any]] = field(default_factory=dict, init=False, repr=False)

    def fit(self, train_df: pd.DataFrame) -> "SkyGuardHybridDetector":
        featured = generate_engineed_features(train_df)
        normal = featured.loc[featured["is_anomaly"].eq(0)].copy()
        if normal.empty:
            raise ValueError("A labeled normal training subset is required to fit station profiles.")

        profiles: Dict[str, Dict[str, float]] = {}
        for station, group in normal.groupby("station_id", sort=False):
            profile: Dict[str, float] = {}
            for sensor, minimum_scale in (("temperature", 0.5), ("pressure", 0.25), ("humidity", 1.0)):
                values = pd.to_numeric(group[sensor], errors="coerce").dropna()
                median = float(values.median())
                mad = float(np.median(np.abs(values - median)))
                profile[f"{sensor}_median"] = median
                profile[f"{sensor}_scale"] = max(minimum_scale, 1.4826 * mad)
            profiles[str(station)] = profile
        self.profiles = profiles
        self.metadata = {
            "version": MODEL_VERSION,
            "trained_at_utc": datetime.now(timezone.utc).isoformat(),
            "training_rows": int(len(train_df)),
            "normal_training_rows": int(len(normal)),
            "stations": sorted(profiles),
            "training_end": str(pd.to_datetime(train_df["timestamp"]).max()),
        }
        return self

    def _profile_joint_fault(self, obs: Dict[str, Any]) -> bool:
        profile = self.profiles.get(str(obs.get("station_id")))
        if not profile:
            return False
        try:
            temp_z = (float(obs["temperature"]) - profile["temperature_median"]) / profile["temperature_scale"]
            pressure_z = (float(obs["pressure"]) - profile["pressure_median"]) / profile["pressure_scale"]
        except (KeyError, TypeError, ValueError):
            return False
        return temp_z >= self.config["joint_profile_z_threshold"] and pressure_z >= self.config["joint_profile_z_threshold"]

    def _classify(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        base = RuleBaselineDetector().predict_observation(obs)
        if base["fault_type"] in HARD_FAULTS:
            return {
                "anomaly_flag": 1,
                "anomaly_score": 1.0,
                "fault_type": base["fault_type"],
                "severity": base["severity"],
                "confidence": 1.0,
                "explanation": base["explanation"],
            }
        if self._profile_joint_fault(obs):
            return {
                "anomaly_flag": 1,
                "anomaly_score": 0.95,
                "fault_type": "SIMULTANEOUS_SENSOR_FAILURE",
                "severity": "HIGH",
                "confidence": 0.95,
                "explanation": "Temperature and pressure jointly exceed the fitted normal station profile.",
            }
        # A one-sensor spike/frozen reading is kept as a reviewable warning;
        # it is not confused with a hard packet-integrity failure.
        if base["anomaly_flag"] and ("SPIKE" in base["fault_type"] or "FROZEN" in base["fault_type"]):
            return {
                "anomaly_flag": 1,
                "anomaly_score": max(0.65, float(base["anomaly_score"])),
                "fault_type": base["fault_type"],
                "severity": base["severity"],
                "confidence": 0.85,
                "explanation": base["explanation"],
            }
        return {
            "anomaly_flag": 0,
            "anomaly_score": 0.0,
            "fault_type": "NORMAL",
            "severity": "NONE",
            "confidence": 0.95,
            "explanation": "No packet-integrity, physical-range, or joint sensor fault detected.",
        }

    def predict_batch(self, df_or_records) -> List[Dict[str, Any]]:
        df = pd.DataFrame(df_or_records).copy() if isinstance(df_or_records, list) else df_or_records.copy()
        if "humidity" not in df.columns and "relative_humidity" in df.columns:
            df["humidity"] = df["relative_humidity"]
        df["_input_order"] = np.arange(len(df))
        featured = generate_engineed_features(df).sort_values("_input_order")
        return [self._classify(row.drop(labels=["_input_order"]).to_dict()) for _, row in featured.iterrows()]

    def predict_observation(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        packet = dict(observation)
        if "humidity" not in packet and "relative_humidity" in packet:
            packet["humidity"] = packet["relative_humidity"]
        station = str(packet.get("station_id", "UNKNOWN"))
        previous = self._last_packet.get(station)
        if previous:
            fields = ("temperature", "pressure", "humidity")
            packet["raw_is_duplicate_packet"] = float(all(packet.get(f) == previous.get(f) for f in fields))
            for sensor in fields:
                if packet.get(sensor) is not None and previous.get(sensor) is not None:
                    packet[f"{sensor}_delta"] = float(packet[sensor]) - float(previous[sensor])
        result = self.predict_batch([packet])[0]
        self._last_packet[station] = {key: packet.get(key) for key in ("temperature", "pressure", "humidity")}
        return result

    def save(self, path: str) -> None:
        joblib.dump({"config": self.config, "profiles": self.profiles, "metadata": self.metadata}, path)

    @classmethod
    def load(cls, path: str) -> "SkyGuardHybridDetector":
        data = joblib.load(path)
        return cls(config=data["config"], profiles=data["profiles"], metadata=data["metadata"])
