# SkyGuard AI

SkyGuard AI is organized as a local-development monorepo for the dashboard UI,
machine-learning work, and ESP32 edge firmware.

## Folder Structure

```text
apps/
  web/              Vite frontend dashboard
services/
  api/              Backend placeholder; API work is pending
packages/
  ml/               Existing Python ML package, models, reports, and tests
firmware/
  esp32/            ESP32 edge model, firmware, and edge-training utilities
```

## Backend Status

Backend work is pending, so the frontend currently runs with local/static data.
The `services/api` folder is reserved for the future local API. When backend
work starts, it should expose endpoints that wrap the inference code in
`packages/ml/src/inference/pipeline.py`.

## Run Locally

Install and run the web app:

```powershell
npm install
npm start
```

Or run it directly from the web app folder:

```powershell
cd apps/web
npm install
npm run dev
```

Build the frontend:

```powershell
npm run web:build
```

Run ML tests:

```powershell
cd packages/ml
python -m pytest
```

## Data Notice

The datasets currently included in this repository are synthetic and should not
be represented as live meteorological or AWS observations.
