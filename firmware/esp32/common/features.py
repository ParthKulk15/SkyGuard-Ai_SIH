from __future__ import annotations
import math
from typing import Iterable
import numpy as np
import pandas as pd

PARAMS = ("temperature", "pressure", "humidity")


def dew_point_c(temp: float, humidity: float) -> float:
    """Magnus approximation; returns NaN for invalid input."""
    if not np.isfinite(temp) or not np.isfinite(humidity) or humidity <= 0:
        return float("nan")
    a, b = 17.27, 237.7
    alpha = (a * temp / (b + temp)) + math.log(min(humidity, 100) / 100)
    return b * alpha / (a - alpha)


def robust_z(value: float, values: Iterable[float]) -> float:
    a = np.asarray(list(values), dtype=float)
    a = a[np.isfinite(a)]
    if len(a) == 0 or not np.isfinite(value):
        return 0.0
    median = float(np.median(a))
    mad = float(np.median(np.abs(a - median)))
    return 0.6745 * (value - median) / max(mad, 0.1)


def add_temporal_features(df: pd.DataFrame, window: int = 6) -> pd.DataFrame:
    """Causal, station-local features: no future readings are used."""
    out = df.sort_values(["station_id", "timestamp"]).copy()
    ts = pd.to_datetime(out["timestamp"])
    out["hour_sin"] = np.sin(2 * np.pi * ts.dt.hour / 24)
    out["hour_cos"] = np.cos(2 * np.pi * ts.dt.hour / 24)
    out["doy_sin"] = np.sin(2 * np.pi * ts.dt.dayofyear / 366)
    out["doy_cos"] = np.cos(2 * np.pi * ts.dt.dayofyear / 366)
    for p in PARAMS:
        g = out.groupby("station_id", group_keys=False)[p]
        out[f"{p}_prev"] = g.shift(1)
        out[f"{p}_delta"] = out[p] - out[f"{p}_prev"]
        out[f"{p}_roll_mean"] = g.transform(lambda x: x.shift(1).rolling(window, min_periods=2).mean())
        out[f"{p}_roll_std"] = g.transform(lambda x: x.shift(1).rolling(window, min_periods=2).std())
        out[f"{p}_roll_median"] = g.transform(lambda x: x.shift(1).rolling(window, min_periods=2).median())
        out[f"{p}_residual"] = out[p] - out[f"{p}_roll_mean"]
        out[f"{p}_missing"] = out[p].isna().astype(int)
    out["dew_point"] = [dew_point_c(t, h) for t, h in zip(out.temperature, out.humidity)]
    out["temp_humidity_product"] = out.temperature * out.humidity
    out["temp_pressure_product"] = out.temperature * out.pressure
    return out.replace([np.inf, -np.inf], np.nan)


EDGE_FEATURES = [
    "temperature", "pressure", "humidity", "temperature_delta", "pressure_delta",
    "humidity_delta", "temperature_roll_mean", "pressure_roll_mean", "humidity_roll_mean",
    "temperature_roll_std", "pressure_roll_std", "humidity_roll_std",
    "temperature_missing", "pressure_missing", "humidity_missing",
]

PC_FEATURES = EDGE_FEATURES + [
    "temperature_residual", "pressure_residual", "humidity_residual", "dew_point",
    "temp_humidity_product", "temp_pressure_product", "hour_sin", "hour_cos", "doy_sin", "doy_cos",
]
