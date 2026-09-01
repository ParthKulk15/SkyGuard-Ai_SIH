# SkyGuard API

Backend work is pending.

Keep future API code in this folder so the frontend, ML package, and firmware
stay separated. The intended first integration point is:

```text
packages/ml/src/inference/pipeline.py
```

Suggested future local endpoints:

```text
GET  /health
GET  /v1/stations
POST /v1/inference
```
