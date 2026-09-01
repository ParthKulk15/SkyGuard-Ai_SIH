from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.ml_service import ml_service
from app.services.sample_data_service import sample_data_service


router = APIRouter(prefix="/v1", tags=["anomalies"])


class ObservationRequest(BaseModel):
    timestamp: str | None = None
    station_id: str = Field(..., examples=["AWS-DL-01"])
    temperature: float | None
    pressure: float | None
    relative_humidity: float | None


@router.get("/anomalies")
def anomalies() -> list[dict]:
    return sample_data_service.anomalies()


@router.post("/inference")
def inference(observation: ObservationRequest) -> dict[str, Any]:
    result = ml_service.predict(observation.model_dump())
    return {
        "input": observation.model_dump(),
        "result": result,
        "data_source": "synthetic" if observation.timestamp is None else "caller_supplied",
    }


@router.get("/incidents")
def incidents() -> list[dict]:
    return [
        {
            **anomaly,
            "incident_id": anomaly["id"],
            "title": anomaly["anomaly_type"].replace("_", " ").title(),
        }
        for anomaly in sample_data_service.anomalies()
    ]
