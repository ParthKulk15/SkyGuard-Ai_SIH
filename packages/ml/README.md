# SkyGuard ML

This folder contains the existing Python anomaly-detection package, trained
model artifacts, reports, scratch experiments, and tests.

## Run Tests

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install pytest
python -m pytest
```

## Inference Entry Point

Future backend work should call:

```text
src/inference/pipeline.py
```
