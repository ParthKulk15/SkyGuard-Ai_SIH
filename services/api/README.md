# SkyGuard API

FastAPI backend foundation for the SkyGuard AI SIH 2026 prototype.

The API uses deterministic synthetic Automatic Weather Station data and reuses
the existing ML inference pipeline from `packages/ml/src/inference/pipeline.py`.
No real IMD API, real AWS sensor feed, wind, irradiance, solar power, or inverter
telemetry is used.

## Run Locally

```powershell
cd services/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Copy `.env.example` to `.env` when changing local CORS settings.

Open API docs:

```text
http://localhost:8000/docs
```

## Endpoints

```text
GET  /health
GET  /v1/overview
GET  /v1/stations
GET  /v1/stations/{station_id}
GET  /v1/weather
POST /v1/telemetry
GET  /v1/anomalies
POST /v1/inference
GET  /v1/incidents
GET  /v1/reports/live-monitor.pdf
GET  /v1/simulation/status
POST /v1/simulation/scenario
```
