# SkyGuard AI — Feature Importance Analysis

This report documents feature importance rankings derived from the Random Forest Fault Classifier across raw sensor readings, temporal cyclical features, rate-of-change deltas, rolling statistical moments, physical interaction terms, and stream quality indicators.

## 1. Top Feature Importance Rankings (Gini Importance)

| Rank | Feature Name | Category | Gini Importance | Diagnostic Role |
| :--- | :--- | :--- | :--- | :--- |
| 1 | `doy_cos` | Raw / Interaction | 0.1193 | Primary signal for anomaly discrimination |
| 2 | `doy_sin` | Raw / Interaction | 0.1055 | Primary signal for anomaly discrimination |
| 3 | `temp_humidity_product` | Raw / Interaction | 0.0779 | Primary signal for anomaly discrimination |
| 4 | `pressure_mad` | Rolling Stat | 0.0521 | Primary signal for anomaly discrimination |
| 5 | `pressure` | Raw / Interaction | 0.0516 | Primary signal for anomaly discrimination |
| 6 | `pressure_residual` | Rolling Stat | 0.0511 | Primary signal for anomaly discrimination |
| 7 | `humidity` | Raw / Interaction | 0.0462 | Primary signal for anomaly discrimination |
| 8 | `dew_point` | Raw / Interaction | 0.0430 | Primary signal for anomaly discrimination |
| 9 | `pressure_roll_std` | Rolling Stat | 0.0419 | Primary signal for anomaly discrimination |
| 10 | `humidity_residual` | Rolling Stat | 0.0341 | Primary signal for anomaly discrimination |
| 11 | `temperature` | Raw / Interaction | 0.0323 | Primary signal for anomaly discrimination |
| 12 | `pressure_delta` | Delta / Change | 0.0323 | Primary signal for anomaly discrimination |
| 13 | `temperature_residual` | Rolling Stat | 0.0284 | Primary signal for anomaly discrimination |
| 14 | `temperature_roll_std` | Rolling Stat | 0.0282 | Primary signal for anomaly discrimination |
| 15 | `temperature_mad` | Rolling Stat | 0.0279 | Primary signal for anomaly discrimination |
