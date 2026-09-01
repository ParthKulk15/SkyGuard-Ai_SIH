from __future__ import annotations

from fastapi import APIRouter, Response

from app.services.report_service import report_service
from app.services.sample_data_service import sample_data_service


router = APIRouter(prefix="/v1", tags=["reports"])


@router.get("/reports/live-monitor.pdf")
def live_monitor_pdf() -> Response:
    pdf = report_service.build_live_monitor_pdf(
        overview=sample_data_service.overview(),
        stations=sample_data_service.latest_station_rows(),
        anomalies=sample_data_service.anomalies(),
    )
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": 'inline; filename="skyguard-live-monitor.pdf"'},
    )
