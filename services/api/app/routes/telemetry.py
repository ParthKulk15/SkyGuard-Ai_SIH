from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.data.sample_data import STATIONS
from app.services.ml_service import ml_service


router = APIRouter(prefix="/v1", tags=["telemetry"])
KNOWN_STATIONS = {station["station_id"] for station in STATIONS}


class TelemetryRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "station_id": "AWS-DL-01",
                "timestamp": "2026-09-01T10:00:00Z",
                "temperature": 28.4,
                "pressure": 1007.2,
                "humidity": 61.0,
            }
        }
    )

    station_id: str = Field(..., min_length=1, max_length=32)
    timestamp: datetime | None = None
    temperature: float | None = Field(default=None, ge=-80, le=80)
    pressure: float | None = Field(default=None, ge=300, le=1200)
    humidity: float | None = Field(default=None, ge=0, le=100)
    edge_anomaly_score: float | None = Field(default=None, ge=0)
    edge_status: str | None = None

    @field_validator("timestamp")
    @classmethod
    def timestamp_is_timezone_aware(cls, value: datetime | None) -> datetime | None:
        if value is not None and value.tzinfo is None:
            raise ValueError("timestamp must include a timezone")
        return value


class TelemetryResponse(BaseModel):
    accepted: bool
    station_id: str
    timestamp: datetime
    observation: dict[str, Any]
    inference: dict[str, Any]
    data_source: str


@router.post("/telemetry", status_code=200)
def receive_telemetry(payload: TelemetryRequest) -> TelemetryResponse:
    if payload.station_id not in KNOWN_STATIONS:
        raise HTTPException(status_code=404, detail=f"Unknown station: {payload.station_id}")

    timestamp = payload.timestamp or datetime.now(timezone.utc)
    observation = {
        "station_id": payload.station_id,
        "timestamp": timestamp.isoformat(),
        "temperature": payload.temperature,
        "pressure": payload.pressure,
        "relative_humidity": payload.humidity,
    }
    result = ml_service.predict(observation)
    return TelemetryResponse(
        accepted=True,
        station_id=payload.station_id,
        timestamp=timestamp,
        observation=observation,
        inference=result,
        data_source="esp32_http",
    )
