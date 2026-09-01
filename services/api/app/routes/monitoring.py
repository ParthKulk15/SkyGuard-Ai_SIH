from __future__ import annotations

from fastapi import APIRouter, Query

from app.services.sample_data_service import sample_data_service


router = APIRouter(prefix="/v1", tags=["stations"])


@router.get("/stations")
def stations() -> list[dict]:
    return sample_data_service.latest_station_rows()


@router.get("/stations/{station_id}")
def station_detail(station_id: str, points: int = Query(default=48, ge=1, le=288)) -> dict:
    return sample_data_service.station_detail(station_id=station_id, points=points)
