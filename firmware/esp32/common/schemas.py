from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class Observation(BaseModel):
    station_id: str
    timestamp: datetime
    temperature: float | None = Field(default=None, description="Degrees Celsius")
    pressure: float | None = Field(default=None, description="hPa")
    humidity: float | None = Field(default=None, description="Relative humidity percent")
    latitude: float | None = None
    longitude: float | None = None
    battery_voltage: float | None = None
    communication_ok: bool = True


class Diagnostic(BaseModel):
    status: Literal["NORMAL", "WARNING", "ANOMALY", "CRITICAL"]
    anomaly_score: float
    confidence: float
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    fault_type: str
    affected_parameter: str | None = None
    sensor_health: float
    recommended_action: str
    estimated_temperature: float | None = None
    estimated_pressure: float | None = None
    estimated_humidity: float | None = None
    data_status: Literal["RAW", "IMPUTED"] = "RAW"
    explanation: str
    model_name: str = "SkyGuard-IF"
    model_version: str = "1.0.0"
    timestamp: datetime
    station_id: str
