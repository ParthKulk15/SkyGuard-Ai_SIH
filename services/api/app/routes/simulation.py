from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.sample_data_service import sample_data_service


router = APIRouter(prefix="/v1/simulation", tags=["simulation"])


class ScenarioRequest(BaseModel):
    scenario: str


@router.get("/status")
def simulation_status() -> dict:
    return sample_data_service.simulation_status()


@router.post("/scenario")
def simulation_scenario(request: ScenarioRequest) -> dict:
    return sample_data_service.set_scenario(request.scenario)
