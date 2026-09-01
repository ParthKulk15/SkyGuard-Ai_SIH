# SkyGuard AI — Dataset Inventory Report

This document provides a comprehensive audit of all CSV datasets provided for training, evaluating, and validating the SkyGuard AI anomaly detection system.

## Summary Inventory Table

| Dataset Name | File Path | Shape (Rows x Cols) | Date Range | Stations | Unique Purpose / Identification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **pc_anomaly_training** | `pc_anomaly_training.csv` | 46,998 x 57 | 2026-05-01 00:00 to 2026-05-28 04:40 | AWS001 - AWS006 (6) | Primary Training & Validation dataset containing raw observations, temporal features, rolling statistics, spatial features, and anomaly annotations. |
| **test_dataset** | `test_dataset.csv` | 8,298 x 57 | 2026-05-28 04:45 to 2026-06-01 23:55 | AWS001 - AWS006 (6) | Dedicated Chronological Hold-out Test Dataset for final model evaluation. Zero overlap with training data. |
| **spatial_consistency** | `spatial_consistency.csv` | 46,998 x 21 | 2026-05-01 00:00 to 2026-05-28 04:40 | AWS001 - AWS006 (6) | Spatial consistency subset containing spatial neighbor medians, residuals, z-scores, and regional consensus metrics. |
| **sensor_degradation** | `sensor_degradation.csv` | 168 x 16 | 2026-05-01 to 2026-05-28 | AWS001 - AWS006 (6) | Station-level daily aggregated operational metrics for sensor health scoring and degradation tracking. |
| **fault_classification** | `fault_classification.csv` | 46,998 x 57 | 2026-05-01 00:00 to 2026-05-28 04:40 | AWS001 - AWS006 (6) | **Identical duplicate copy** of `pc_anomaly_training.csv` (100% row-for-row match). |

---

## Relationship & Duplication Analysis

1. **`fault_classification.csv` vs `pc_anomaly_training.csv`**:
   - Verification (`df_train.equals(df_fc)`): **TRUE**. Both datasets contain identical 46,998 rows and 57 columns.
   - **Decision**: `fault_classification.csv` is logged as a duplicate copy. To prevent redundant training and data leakage, model development uses `pc_anomaly_training.csv` as the primary training split.

2. **`spatial_consistency.csv` vs `pc_anomaly_training.csv`**:
   - `spatial_consistency.csv` contains 21 columns corresponding to the exact same 46,998 station-timestamp timestamps present in `pc_anomaly_training.csv`.
   - It provides neighbor medians (`neighbor_temperature_median`, `neighbor_pressure_median`, `neighbor_humidity_median`), spatial residuals, and consensus scores.

3. **`test_dataset.csv` vs `pc_anomaly_training.csv`**:
   - Temporal relationship: `test_dataset.csv` begins at `2026-05-28 04:45:00` immediately following the end of `pc_anomaly_training.csv` at `2026-05-28 04:40:00`.
   - Station-Timestamp Overlap: **0 overlapping rows**.
   - **Decision**: `test_dataset.csv` serves as an untouched 100% hold-out test set for Phase 8-9 evaluation.

---

## Detailed Column & Label Distribution Breakdown

### 1. Training Dataset (`pc_anomaly_training.csv`)
- **Total Rows**: 46,998
- **Anomaly Count**: 1,662 (3.54% positive rate)
- **Normal Count**: 45,336 (96.46%)
- **Fault Type Breakdown**:
  - `NORMAL`: 45,336
  - `TEMPERATURE_DRIFT`: 288
  - `PRESSURE_DRIFT`: 288
  - `HUMIDITY_DRIFT`: 288
  - `TEMPERATURE_BIAS`: 216
  - `PRESSURE_BIAS`: 120
  - `HUMIDITY_BIAS`: 120
  - `TEMPERATURE_FROZEN`: 108
  - `PRESSURE_FROZEN`: 108
  - `HUMIDITY_FROZEN`: 108
  - `TEMPERATURE_SPIKE`: 6
  - `PRESSURE_SPIKE`: 6
  - `HUMIDITY_SPIKE`: 6
- **Event Type (Genuine Meteorological Events)**:
  - `NONE`: 45,635
  - `REGIONAL_HEATWAVE`: 535
  - `COLD_WAVE`: 432
  - `RAPID_PRESSURE_SYSTEM`: 396

### 2. Test Dataset (`test_dataset.csv`)
- **Total Rows**: 8,298
- **Anomaly Count**: 102 (1.23% positive rate)
- **Normal Count**: 8,196 (98.77%)
- **Fault Type Breakdown**:
  - `NORMAL`: 8,196
  - `COMMUNICATION_FAILURE`: 30
  - `DATA_CORRUPTION`: 24
  - `DUPLICATE_PACKET`: 24
  - `SIMULTANEOUS_SENSOR_FAILURE`: 24
- **Event Type**:
  - `NONE`: 7,866
  - `WIDESPREAD_HUMIDITY_SURGE`: 432 (is_genuine_event = 1)

### 3. Sensor Degradation Dataset (`sensor_degradation.csv`)
- **Total Rows**: 168 (28 days x 6 stations)
- **Degradation Level**: `HEALTHY`: 142, `WATCH`: 26
- **Maintenance Priority**: `LOW`: 142, `MEDIUM`: 26

---

## Target Leakage & Feature Classification

To prevent target leakage, all features are categorized into **Forbidden Target Columns** and **Allowed Model Features**.

### Forbidden Target Columns (REJECTED FROM MODEL INPUTS):
- `is_anomaly`, `fault_type`, `severity`, `event_type`, `is_genuine_event`, `fault_parameter`
- `spatial_anomaly_score`, `spatial_consensus_score`, `event_likelihood`, `sensor_fault_likelihood`
- `degradation_level`, `maintenance_priority`, `estimated_health_risk_score`, `sensor_health_score`

### Allowed Input Features:
- **Raw Sensor Features**: `temperature`, `pressure`, `humidity`
- **Station Context**: `latitude`, `longitude`, `altitude_m`
- **Temporal Cyclical**: `hour_sin`, `hour_cos`, `doy_sin`, `doy_cos`
- **Rate-of-Change (Delta)**: `temperature_delta`, `pressure_delta`, `humidity_delta`
- **Rolling Statistical Features**: `temperature_roll_mean`, `temperature_roll_std`, `temperature_roll_median`, `temperature_mad`, `temperature_residual`, `pressure_roll_mean`, `pressure_roll_std`, `pressure_roll_median`, `pressure_mad`, `pressure_residual`, `humidity_roll_mean`, `humidity_roll_std`, `humidity_roll_median`, `humidity_mad`, `humidity_residual`
- **Physical Interaction Features**: `dew_point`, `temp_humidity_product`, `temp_pressure_product`
- **Missingness Signals**: `temperature_missing`, `pressure_missing`, `humidity_missing`
- **Spatial Consensus Inputs (for Spatial Module)**: `neighbor_temperature_median`, `neighbor_pressure_median`, `neighbor_humidity_median`, `spatial_residual_temperature`, `spatial_residual_pressure`, `spatial_residual_humidity`
