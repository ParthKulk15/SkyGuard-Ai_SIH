from __future__ import annotations

from fastapi import APIRouter, Query

from app.services.sample_data_service import sample_data_service


router = APIRouter(prefix="/v1", tags=["weather"])


@router.get("/weather")
def weather(station_id: str | None = None, hours: int = Query(default=24, ge=1, le=72)) -> dict:
    return sample_data_service.weather_series(station_id=station_id, hours=hours)
