# SkyGuard AI — Final Machine Learning System Report

## 1. Executive Summary
SkyGuard AI is a multi-tiered anomaly detection system designed to inspect Automatic Weather Station (AWS) observations in real time. It integrates physical baseline checks, unsupervised machine learning (Isolation Forest & PyTorch Autoencoder), spatial neighbor consensus, supervised fault classification, and station health degradation tracking.

## 2. Dataset & Quality Audit Summary
- **Training Set (`pc_anomaly_training.csv`)**: 46,998 observations (`2026-05-01` to `2026-05-28 04:40`). Split chronologically into Train (80%, 37,584 rows) and Validation (20%, 9,414 rows).
- **Hold-out Test Set (`test_dataset.csv`)**: 8,298 observations (`2026-05-28 04:45` to `2026-06-01 23:55`). Zero overlap with training data.
- **Identical Duplication Note**: `fault_classification.csv` was verified to be a 100% exact duplicate of `pc_anomaly_training.csv` and documented as such.

## 3. Strict Target Leakage Prevention
All ground-truth labels (`is_anomaly`, `fault_type`, `severity`, `event_type`, `is_genuine_event`, `spatial_anomaly_score`, `sensor_fault_likelihood`) were strictly excluded from model feature inputs. Only raw sensor measurements, past rolling/delta statistical signals, cyclical temporal encodings, and neighbor medians available at inference time were passed to model features.

## 4. Key Performance Results (Test Set Evaluation)

- **Best Overall Model**: **SkyGuard Fused Decision Layer**
- **Precision**: 0.3258
- **Recall**: 0.4216
- **F1 Score**: **0.3675**
- **False Positive Rate**: 0.0109

## 5. Artifacts Produced
- `models/isolation_forest.joblib`
- `models/autoencoder.pt`
- `models/fault_classifier.joblib`
- `models/degradation_model.joblib`
- `models/scaler.joblib`
- `models/feature_config.json`
- `models/model_config.json`
- `reports/dataset_inventory.md`
- `reports/data_quality_report.md`
- `reports/model_comparison.md`
- `reports/anomaly_type_performance.csv`
- `reports/final_model_report.md`

## 6. Recommendations for Deployment
1. Deploy `src/inference/pipeline.py` using `SkyGuardInferenceEngine` as a stateless REST endpoint or stream consumer.
2. Maintain daily station health tracking using `StationDegradationEvaluator` to schedule preventive maintenance before sensor failure.
