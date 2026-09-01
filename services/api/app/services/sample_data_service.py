from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException

from app.data.sample_data import SCENARIOS, STATIONS
from app.services.ml_service import ml_service


def _now_slot() -> datetime:
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    return now - timedelta(minutes=now.minute % 5)


def _stable_unit(*parts: Any) -> float:
    digest = hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF


@dataclass
class SimulationState:
    scenario: str = "normal"
    running: bool = True
    updated_at: datetime = field(default_factory=_now_slot)


class SampleDataService:
    def __init__(self) -> None:
        self.state = SimulationState()

    def set_scenario(self, scenario: str) -> dict[str, Any]:
        if scenario not in SCENARIOS:
            raise HTTPException(status_code=400, detail=f"Unsupported simulation scenario: {scenario}")
        self.state.scenario = scenario
        self.state.updated_at = _now_slot()
        return self.simulation_status()

    def simulation_status(self) -> dict[str, Any]:
        return {
            "scenario": self.state.scenario,
            "running": self.state.running,
            "simulation_time": _now_slot().isoformat(),
            "last_updated": self.state.updated_at.isoformat(),
            "available_scenarios": sorted(SCENARIOS),
            "data_source": "synthetic",
        }

    def station_metadata(self) -> list[dict[str, Any]]:
        return [{k: station[k] for k in ("station_id", "name", "region", "latitude", "longitude")} for station in STATIONS]

    def observations(self, points: int = 24, station_id: str | None = None) -> list[dict[str, Any]]:
        stations = self._select_stations(station_id)
        end = _now_slot()
        times = [end - timedelta(minutes=5 * i) for i in reversed(range(points))]
        rows: list[dict[str, Any]] = []
        for station in stations:
            for index, stamp in enumerate(times):
                rows.append(self._observation_for(station, stamp, index, len(times)))
        return rows

    def latest_station_rows(self) -> list[dict[str, Any]]:
        latest_by_station = [self.observations(points=12, station_id=s["station_id"])[-1] for s in STATIONS]
        return [self._enrich_observation(row) for row in latest_by_station]

    def station_detail(self, station_id: str, points: int = 48) -> dict[str, Any]:
        station = self._get_station(station_id)
        history = self.observations(points=points, station_id=station_id)
        latest = self._enrich_observation(history[-1])
        return {
            **{k: station[k] for k in ("station_id", "name", "region", "latitude", "longitude")},
            "latest": latest,
            "history": history,
            "data_source": "synthetic",
        }

    def weather_series(self, station_id: str | None = None, hours: int = 24) -> dict[str, Any]:
        points = max(1, min(288, hours * 12))
        rows = self.observations(points=points, station_id=station_id)
        return {"data_source": "synthetic", "scenario": self.state.scenario, "observations": rows}

    def anomalies(self) -> list[dict[str, Any]]:
        anomalies = []
        for row in self.latest_station_rows():
            if row["anomaly_flag"]:
                anomalies.append({
                    "id": f"{row['station_id']}-{row['last_updated']}",
                    "station_id": row["station_id"],
                    "timestamp": row["last_updated"],
                    "parameter": self._parameter_from_fault(row["anomaly_type"]),
                    "anomaly_type": row["anomaly_type"],
                    "severity": row["severity"],
                    "confidence": row["confidence"],
                    "status": "active",
                    "data_source": "synthetic",
                })
        return anomalies

    def overview(self) -> dict[str, Any]:
        stations = self.latest_station_rows()
        anomalies = self.anomalies()
        total = len(stations)
        healthy = sum(1 for row in stations if row["status"] == "healthy")
        warning = sum(1 for row in stations if row["status"] == "warning")
        critical = sum(1 for row in stations if row["status"] == "critical")
        data_quality = self._data_quality(stations)
        health_score = round(sum(row["health_score"] for row in stations) / total, 2) if total else 0.0
        return {
            "network_health_score": health_score,
            "total_stations": total,
            "healthy_stations": healthy,
            "warning_stations": warning,
            "critical_stations": critical,
            "active_anomalies": len(anomalies),
            "data_quality": data_quality,
            "last_updated": _now_slot().isoformat(),
            "simulation_mode": True,
            "ai_status": "operational" if ml_service.available else "ml_unavailable",
            "recent_anomalies": anomalies[:5],
            "station_summary": stations,
            "data_source": "synthetic",
            "scenario": self.state.scenario,
        }

    def _observation_for(self, station: dict[str, Any], stamp: datetime, index: int, total: int) -> dict[str, Any]:
        minutes = stamp.hour * 60 + stamp.minute
        day_cycle = math.sin((minutes / 1440) * 2 * math.pi - math.pi / 2)
        small_cycle = math.sin((minutes / 360) * 2 * math.pi)
        station_jitter = (_stable_unit(station["station_id"], stamp.date()) - 0.5) * 0.6
        temperature = station["base_temperature"] + 5.5 * day_cycle + 0.8 * small_cycle + station_jitter
        pressure = station["base_pressure"] - 1.3 * day_cycle + 0.4 * math.cos(index / 5)
        humidity = station["base_humidity"] - 9.0 * day_cycle + 1.2 * math.sin(index / 4)

        row = {
            "timestamp": stamp.isoformat(),
            "station_id": station["station_id"],
            "temperature": round(temperature, 2),
            "pressure": round(pressure, 2),
            "relative_humidity": round(max(5.0, min(98.0, humidity)), 2),
            "data_source": "synthetic",
            "scenario": self.state.scenario,
        }
        return self._apply_scenario(row, station, index, total)

    def _apply_scenario(self, row: dict[str, Any], station: dict[str, Any], index: int, total: int) -> dict[str, Any]:
        scenario = self.state.scenario
        affected = station["station_id"] in {"AWS-RJ-01", "AWS-GJ-01"} or index >= total - 3
        if scenario == "normal":
            return row
        if scenario == "temperature_spike" and station["station_id"] == "AWS-RJ-01" and index == total - 1:
            row["temperature"] = 62.0
        elif scenario == "temperature_drift" and station["station_id"] == "AWS-DL-01":
            row["temperature"] = round(row["temperature"] + index * 0.32, 2)
        elif scenario == "frozen_sensor" and station["station_id"] == "AWS-MH-01" and index >= total - 8:
            row["temperature"] = 29.5
            row["pressure"] = 1009.2
            row["relative_humidity"] = 72.0
            row["temp_persistence"] = 8.0
            row["press_persistence"] = 8.0
            row["hum_persistence"] = 8.0
        elif scenario == "missing_data" and station["station_id"] == "AWS-AS-01" and index == total - 1:
            row["temperature"] = None
            row["pressure"] = None
            row["relative_humidity"] = None
            row["raw_is_missing"] = 1.0
        elif scenario == "duplicate_packet" and station["station_id"] == "AWS-KA-01" and index == total - 1:
            row["raw_is_duplicate_packet"] = 1.0
        elif scenario == "data_corruption" and station["station_id"] == "AWS-TN-01" and index == total - 1:
            row["relative_humidity"] = 135.0
        elif scenario == "simultaneous_sensor_failure" and station["station_id"] == "AWS-WB-01" and index == total - 1:
            row["temperature"] = 58.0
            row["pressure"] = 1092.0
        elif scenario == "multivariate_inconsistency" and station["station_id"] == "AWS-GJ-01" and index == total - 1:
            row["temperature"] = 45.0
            row["pressure"] = 1048.0
            row["relative_humidity"] = 88.0
        elif scenario == "regional_weather_event" and affected:
            row["temperature"] = round((row["temperature"] or 0) + 6.5, 2)
            row["pressure"] = round((row["pressure"] or 0) - 7.0, 2)
            row["relative_humidity"] = round(min(98.0, (row["relative_humidity"] or 0) + 14.0), 2)
        return row

    def _enrich_observation(self, row: dict[str, Any]) -> dict[str, Any]:
        result = ml_service.predict(row)
        score = float(result.get("anomaly_score", 0.0) or 0.0)
        health = max(0.0, round(100.0 - score * 45.0, 2))
        severity = str(result.get("severity", "NONE"))
        if severity in {"CRITICAL", "HIGH"}:
            status = "critical"
        elif severity == "MEDIUM" or int(result.get("anomaly_flag", 0) or 0):
            status = "warning"
        else:
            status = "healthy"
        return {
            "station_id": row["station_id"],
            "region": self._get_station(row["station_id"])["region"],
            "latitude": self._get_station(row["station_id"])["latitude"],
            "longitude": self._get_station(row["station_id"])["longitude"],
            "temperature": row["temperature"],
            "pressure": row["pressure"],
            "relative_humidity": row["relative_humidity"],
            "health_score": health,
            "status": status,
            "last_updated": row["timestamp"],
            "anomaly_flag": int(result.get("anomaly_flag", 0) or 0),
            "anomaly_type": result.get("fault_type", "NORMAL"),
            "severity": severity,
            "confidence": float(result.get("confidence", 0.0) or 0.0),
            "explanation": result.get("explanation", ""),
            "model_available": bool(result.get("model_available", False)),
            "data_source": "synthetic",
        }

    def _select_stations(self, station_id: str | None) -> list[dict[str, Any]]:
        if station_id is None:
            return STATIONS
        return [self._get_station(station_id)]

    def _get_station(self, station_id: str) -> dict[str, Any]:
        for station in STATIONS:
            if station["station_id"] == station_id:
                return station
        raise HTTPException(status_code=404, detail=f"Station not found: {station_id}")

    @staticmethod
    def _parameter_from_fault(fault: str) -> str:
        fault_upper = fault.upper()
        if "TEMP" in fault_upper:
            return "temperature"
        if "PRESSURE" in fault_upper:
            return "pressure"
        if "HUMIDITY" in fault_upper:
            return "relative_humidity"
        return "packet"

    @staticmethod
    def _data_quality(stations: list[dict[str, Any]]) -> float:
        total_fields = len(stations) * 3
        missing = sum(row[field] is None for row in stations for field in ("temperature", "pressure", "relative_humidity"))
        return round(100.0 * (1.0 - missing / total_fields), 2) if total_fields else 0.0


sample_data_service = SampleDataService()
