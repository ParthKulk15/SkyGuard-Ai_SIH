# SkyGuard AI

SkyGuard AI screens Automatic Weather Station (AWS) observations of
temperature, atmospheric pressure, and relative humidity. The present
repository contains a complete synthetic-data generator and trained ESP32 E1
edge anomaly detector for an ESP32 DevKit and BME280 sensor.

> All datasets in this repository are synthetic. They are not real AWS or
> meteorological observations and must not be represented as such.

## Contents

* `data/` — six generated training/evaluation CSV datasets.
* `generate_datasets.py` — realistic correlated weather and labelled fault
  generator.
* `training/train_edge.py` — trains, benchmarks, serializes, and exports E1.
* `edge/esp32/edge_model.h` — generated dependency-free C/C++ tree model.
* `edge/esp32/skyguard_devkit.ino` — ESP32 DevKit + BME280 + MQTT firmware.
* `models/edge_benchmark.json` — reproducible synthetic validation result.

## Install and reproduce

```powershell
cd firmware/esp32
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python generate_datasets.py
python training/train_edge.py
```

Training exports `models/edge_e1.joblib`,
`models/edge_benchmark.json`, and `edge/esp32/edge_model.h`.

## ESP32 deployment

See [the complete ESP32 DevKit deployment guide](docs/esp32_deployment.md).

## Edge model

E1 is a depth-5 Decision Tree trained on the lightweight features in
`data/edge_training.csv`: raw T/P/RH, deltas, causal six-reading statistics,
and missing-data flags. It does not attempt spatial analysis or maintenance
prediction; those are server tasks. Deterministic limits run beside the model
to catch impossible values, communication loss, and frozen readings.

The latest synthetic chronological validation result is recorded in
`models/edge_benchmark.json`. It must be revalidated against representative,
calibrated field data before operational use.

## MQTT contract

The firmware publishes to:

```text
skyguard/station/<station-id>/telemetry
```

Payload fields include `station_id`, T/P/RH values, `edge_anomaly_score`,
`edge_status`, `model_name`, and `model_version`.

## License

Add the license appropriate for your SIH team before making the repository
public.
