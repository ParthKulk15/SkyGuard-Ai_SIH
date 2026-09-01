# SkyGuard AI — Data Quality Audit Report

This report documents the quality audit, value ranges, missing value distributions, anomaly balances, and data preprocessing decisions across all supplied CSV datasets.

## 1. Quality Metrics Overview

| Dataset | Total Rows | Duplicate Rows | Missing Values (Total Cells) | Stations | Anomaly Ratio | Primary Quality Note |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **pc_anomaly_training** | 46,998 | 0 | 0 (0.0%) | 6 | 3.54% | Clean dataset, complete temporal coverage without missing cells. |
| **test_dataset** | 8,298 | 0 | 792 (0.17%) | 6 | 1.23% | Contains missing sensor observations simulating sensor drops/communication failures. |
| **spatial_consistency**| 46,998 | 0 | 0 (0.0%) | 6 | 3.54% | Complete spatial feature coverage across training timestamps. |
| **sensor_degradation**  | 168 | 0 | 0 (0.0%) | 6 | N/A | Daily station aggregate metrics. Missing data pct column present as feature. |
| **fault_classification** | 46,998 | 0 | 0 (0.0%) | 6 | 3.54% | Duplicate copy of training set. |

---

## 2. Feature Value Range Audit

Below are the empirical physical ranges observed across raw and engineered numerical features in `pc_anomaly_training.csv` and `test_dataset.csv`:

### Temperature (°C)
- **Training Set Range**: Min = 16.94 °C, Mean = 27.16 °C, Max = 60.65 °C, Std = 4.52 °C
- **Test Set Range**: Min = 17.86 °C, Mean = 26.09 °C, Max = 42.93 °C, Std = 4.11 °C
- **Sanity Check**: Extreme temperature spike of 60.65 °C observed in training set coincides with synthetic `TEMPERATURE_SPIKE` anomalies.

### Atmospheric Pressure (hPa)
- **Training Set Range**: Min = 986.21 hPa, Mean = 1006.85 hPa, Max = 1047.17 hPa, Std = 6.68 hPa
- **Test Set Range**: Min = 994.52 hPa, Mean = 1006.93 hPa, Max = 1035.80 hPa, Std = 6.62 hPa
- **Sanity Check**: Expected barometric pressure variations for station elevation (~780m - 970m above sea level).

### Relative Humidity (%)
- **Training Set Range**: Min = 39.25 %, Mean = 70.07 %, Max = 126.95 %, Std = 8.10 %
- **Test Set Range**: Min = 55.68 %, Mean = 71.85 %, Max = 135.00 %, Std = 8.28 %
- **Sanity Check**: Relative humidity values > 100% (up to 135%) are physically non-viable observations representing synthetic sensor bias/corruption faults.

---

## 3. Missing Value & Null Handling Strategy

In `test_dataset.csv`, missing values occur in specific rows due to simulated sensor communication failures:
- `temperature`, `pressure`, `humidity`: 30 missing rows each (0.36%)
- `temperature_delta`, `pressure_delta`, `humidity_delta`: 36 missing rows each (0.43%)
- `spatial_residual_*`, `spatial_z_*`: 30-60 missing rows each (0.36% - 0.72%)

### Handling Protocol:
1. **Flag Missingness**: Preserve `temperature_missing`, `pressure_missing`, `humidity_missing` binary indicators as input features to inform models of sensor failure events.
2. **Imputation for Feature Vector Construction**: Use forward-fill (`ffill()`) by station to retain the last known valid sensor state for rolling and delta calculations, followed by median filling for residual NaNs.
3. **No Row Removal**: Missing test rows represent real-world sensor dropout anomalies; removing them would corrupt test evaluation metrics.

---

## 4. Distinguishing Extreme Weather Events vs. Sensor Faults

Real extreme meteorological events (e.g. heatwaves, cold waves, rapid pressure drops) exhibit spatial consensus across neighboring stations:
- **Regional Heatwave** (535 rows in training set): High temperature elevation across all 6 stations simultaneously; `spatial_residual_temperature` remains near zero. `is_genuine_event = 1`, `is_anomaly = 0`.
- **Widespread Humidity Surge** (432 rows in test set): Humidity rise observed concurrently across stations. `is_genuine_event = 1`, `is_anomaly = 0`.
- **Sensor Faults** (e.g., `TEMPERATURE_SPIKE` / `HUMIDITY_BIAS`): Isolated anomaly at a single station while surrounding stations maintain normal trends (`spatial_residual_temperature` >> threshold). `is_genuine_event = 0`, `is_anomaly = 1`.

---

## 5. Summary of Data Preprocessing Decisions

1. **Temporal Sorting**: All datasets are strictly sorted by `station_id` and `timestamp` prior to computing delta and rolling features.
2. **Feature Scaling**: RobustScaler / StandardScaler fit strictly on the Training split (`2026-05-01` to `2026-05-22`) and transformed across Validation and Test sets without data leakage.
3. **Zero Target Leakage**: Labels (`is_anomaly`, `fault_type`, `severity`, `is_genuine_event`) are isolated exclusively for evaluation metrics and supervised fault classification.
