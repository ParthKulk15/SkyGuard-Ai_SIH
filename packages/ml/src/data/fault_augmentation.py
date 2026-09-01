"""Reproducible, training-only fault injection for SkyGuard telemetry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np
import pandas as pd


DEFAULT_AUGMENTATION_COUNTS: Dict[str, int] = {
    "COMMUNICATION_FAILURE": 400,
    "DATA_CORRUPTION": 400,
    "DUPLICATE_PACKET": 400,
    "SIMULTANEOUS_SENSOR_FAILURE": 400,
    "TEMPERATURE_SPIKE": 300,
    "PRESSURE_SPIKE": 300,
    "HUMIDITY_SPIKE": 300,
    "TEMPERATURE_FROZEN": 250,
    "PRESSURE_FROZEN": 250,
    "HUMIDITY_FROZEN": 250,
    "TEMPERATURE_BIAS": 250,
    "PRESSURE_BIAS": 250,
    "HUMIDITY_BIAS": 250,
    "TEMPERATURE_DRIFT": 250,
    "PRESSURE_DRIFT": 250,
    "HUMIDITY_DRIFT": 250,
}


@dataclass(frozen=True)
class TrainingFaultAugmenter:
    """Inject known telemetry fault signatures into normal training observations.

    The augmenter never consumes validation or test rows.  It is intended to
    cover operational faults that are absent or too rare in collected history,
    while preserving the existing feature schema used by the inference model.
    """

    random_state: int = 42

    def augment(
        self,
        train_df: pd.DataFrame,
        counts: Dict[str, int] | None = None,
    ) -> pd.DataFrame:
        counts = counts or DEFAULT_AUGMENTATION_COUNTS
        normal = train_df.loc[train_df["is_anomaly"].eq(0)].copy()
        if normal.empty:
            raise ValueError("Fault augmentation requires at least one normal training observation.")

        rng = np.random.default_rng(self.random_state)
        generated = [train_df.copy()]
        for fault_type, count in counts.items():
            if count <= 0:
                continue
            sample = normal.sample(n=count, replace=len(normal) < count, random_state=int(rng.integers(0, 2**31 - 1))).copy()
            sample = self._label_fault(sample, fault_type)
            generated.append(self._inject(sample, fault_type, rng))

        return pd.concat(generated, ignore_index=True)

    @staticmethod
    def _label_fault(df: pd.DataFrame, fault_type: str) -> pd.DataFrame:
        df["is_anomaly"] = 1
        df["fault_type"] = fault_type
        parameter = fault_type.split('_', maxsplit=1)[0].lower()
        df["fault_parameter"] = "all" if fault_type in {
            "COMMUNICATION_FAILURE", "DUPLICATE_PACKET", "SIMULTANEOUS_SENSOR_FAILURE"
        } else parameter
        df["severity"] = "CRITICAL" if fault_type in {"COMMUNICATION_FAILURE", "DATA_CORRUPTION"} else "HIGH"
        df["event_type"] = "SENSOR_FAULT"
        df["is_genuine_event"] = 0
        return df

    @staticmethod
    def _set(df: pd.DataFrame, column: str, value) -> None:
        df[column] = value

    @staticmethod
    def _reference(df: pd.DataFrame, column: str, fallback: float) -> pd.Series:
        if column not in df.columns:
            return pd.Series(fallback, index=df.index, dtype=float)
        return pd.to_numeric(df[column], errors="coerce").fillna(fallback)

    def _inject(self, df: pd.DataFrame, fault_type: str, rng: np.random.Generator) -> pd.DataFrame:
        if fault_type == "COMMUNICATION_FAILURE":
            for column in ("temperature", "pressure", "humidity", "dew_point"):
                self._set(df, column, np.nan)
            for column in ("temperature_missing", "pressure_missing", "humidity_missing", "raw_is_missing"):
                self._set(df, column, 1.0)
            self._set(df, "raw_is_duplicate_packet", 0.0)
            return df

        if fault_type == "DATA_CORRUPTION":
            humidity = rng.uniform(120.0, 140.0, len(df))
            self._set(df, "humidity", humidity)
            humidity_reference = self._reference(df, "humidity_roll_mean", 70.0)
            self._set(df, "humidity_delta", humidity - humidity_reference)
            self._set(df, "humidity_residual", humidity - humidity_reference)
            self._set(df, "temp_humidity_product", pd.to_numeric(df["temperature"], errors="coerce") * humidity)
            self._set(df, "temperature_missing", 0.0)
            self._set(df, "pressure_missing", 0.0)
            self._set(df, "humidity_missing", 0.0)
            self._set(df, "raw_is_missing", 0.0)
            self._set(df, "raw_is_duplicate_packet", 0.0)
            return df

        if fault_type == "DUPLICATE_PACKET":
            for column in ("temperature_delta", "pressure_delta", "humidity_delta"):
                self._set(df, column, 0.0)
            for column in ("temp_persistence", "press_persistence", "hum_persistence"):
                self._set(df, column, 3.0)
            self._set(df, "raw_is_duplicate_packet", 1.0)
            self._set(df, "raw_is_missing", 0.0)
            return df

        if fault_type == "SIMULTANEOUS_SENSOR_FAILURE":
            temperature_shift = rng.uniform(18.0, 22.0, len(df))
            pressure_shift = rng.uniform(18.0, 22.0, len(df))
            temperature = pd.to_numeric(df["temperature"], errors="coerce") + temperature_shift
            pressure = pd.to_numeric(df["pressure"], errors="coerce") + pressure_shift
            self._set(df, "temperature", temperature)
            self._set(df, "pressure", pressure)
            self._set(df, "temperature_delta", temperature_shift)
            self._set(df, "pressure_delta", pressure_shift)
            self._set(df, "temperature_residual", temperature - self._reference(df, "temperature_roll_mean", 25.0))
            self._set(df, "pressure_residual", pressure - self._reference(df, "pressure_roll_mean", 1010.0))
            self._set(df, "temp_humidity_product", temperature * pd.to_numeric(df["humidity"], errors="coerce"))
            self._set(df, "temp_pressure_product", temperature * pressure)
            self._set(df, "raw_is_missing", 0.0)
            self._set(df, "raw_is_duplicate_packet", 0.0)
            return df

        if fault_type.endswith("_SPIKE"):
            sensor, shift = {
                "TEMPERATURE_SPIKE": ("temperature", rng.uniform(15.0, 22.0, len(df))),
                "PRESSURE_SPIKE": ("pressure", rng.uniform(15.0, 22.0, len(df))),
                "HUMIDITY_SPIKE": ("humidity", rng.uniform(25.0, 35.0, len(df))),
            }[fault_type]
            values = pd.to_numeric(df[sensor], errors="coerce") + shift
            if sensor == "humidity":
                values = values.clip(upper=99.0)
            self._set(df, sensor, values)
            prefix = {"temperature": "temperature", "pressure": "pressure", "humidity": "humidity"}[sensor]
            self._set(df, f"{prefix}_delta", shift)
            self._set(df, f"{prefix}_residual", values - self._reference(df, f"{prefix}_roll_mean", float(values.median())))
            return df

        if fault_type.endswith("_FROZEN"):
            prefix = fault_type.split('_', maxsplit=1)[0].lower()
            self._set(df, {"temperature": "temp_persistence", "pressure": "press_persistence", "humidity": "hum_persistence"}[prefix], 8.0)
            self._set(df, f"{prefix}_delta", 0.0)
            self._set(df, "raw_is_duplicate_packet", 0.0)
            return df

        if fault_type.endswith("_BIAS") or fault_type.endswith("_DRIFT"):
            prefix = fault_type.split('_', maxsplit=1)[0].lower()
            base_shift = {
                "temperature": rng.uniform(3.0, 5.0, len(df)),
                "pressure": rng.uniform(4.0, 7.0, len(df)),
                "humidity": rng.uniform(8.0, 14.0, len(df)),
            }[prefix]
            if fault_type.endswith("_DRIFT"):
                base_shift *= 0.65
            values = pd.to_numeric(df[prefix], errors="coerce") + base_shift
            self._set(df, prefix, values)
            self._set(df, f"{prefix}_residual", values - self._reference(df, f"{prefix}_roll_mean", float(values.median())))
            self._set(df, f"{prefix}_delta", base_shift if fault_type.endswith("_BIAS") else base_shift / 6.0)
            return df

        raise ValueError(f"Unsupported augmentation fault type: {fault_type}")
