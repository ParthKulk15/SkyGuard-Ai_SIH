from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_overview_endpoint() -> None:
    response = client.get("/v1/overview")
    assert response.status_code == 200
    body = response.json()
    assert body["simulation_mode"] is True
    assert body["total_stations"] >= 8
    assert "station_summary" in body


def test_station_endpoint() -> None:
    response = client.get("/v1/stations/AWS-DL-01")
    assert response.status_code == 200
    body = response.json()
    assert body["station_id"] == "AWS-DL-01"
    assert body["latest"]["station_id"] == "AWS-DL-01"
    assert body["history"]


def test_weather_endpoint_uses_sih_fields_only() -> None:
    response = client.get("/v1/weather?station_id=AWS-DL-01&hours=1")
    assert response.status_code == 200
    observations = response.json()["observations"]
    assert observations
    first = observations[0]
    assert {"timestamp", "station_id", "temperature", "pressure", "relative_humidity"}.issubset(first)
    assert "wind" not in first
    assert "irradiance" not in first
    assert "power" not in first


def test_anomaly_endpoint() -> None:
    client.post("/v1/simulation/scenario", json={"scenario": "data_corruption"})
    response = client.get("/v1/anomalies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_inference_endpoint() -> None:
    response = client.post(
        "/v1/inference",
        json={
            "station_id": "AWS-DL-01",
            "timestamp": "2026-09-01T10:00:00Z",
            "temperature": 26.0,
            "pressure": 1007.0,
            "relative_humidity": 130.0,
        },
    )
    assert response.status_code == 200
    assert "result" in response.json()
    assert "anomaly_flag" in response.json()["result"]


def test_esp32_http_telemetry_endpoint() -> None:
    response = client.post(
        "/v1/telemetry",
        json={
            "station_id": "AWS-DL-01",
            "timestamp": "2026-09-01T10:00:00Z",
            "temperature": 28.4,
            "pressure": 1007.2,
            "humidity": 61.0,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["accepted"] is True
    assert body["data_source"] == "esp32_http"
    assert body["observation"]["relative_humidity"] == 61.0
    assert "inference" in body


def test_simulation_scenario() -> None:
    response = client.post("/v1/simulation/scenario", json={"scenario": "temperature_spike"})
    assert response.status_code == 200
    assert response.json()["scenario"] == "temperature_spike"


def test_pdf_generation() -> None:
    response = client.get("/v1/reports/live-monitor.pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")
