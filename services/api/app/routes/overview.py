from __future__ import annotations

from fastapi import APIRouter

from app.services.sample_data_service import sample_data_service


router = APIRouter(prefix="/v1", tags=["overview"])


@router.get("/overview")
def overview() -> dict:
    return sample_data_service.overview()
