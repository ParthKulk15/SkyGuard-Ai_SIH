# SkyGuard Hybrid Detector Model Card

## Intended use

Detect packet integrity, physical-range, duplicate, frozen, spike, and joint sensor faults in weather-station telemetry.

## Evaluation

- Chronological validation F1: 0.8125
- Held-out test F1: 0.9697
- Held-out test accuracy: 0.9993

## Limitations

The historical labels are synthetic and strongly imbalanced. The model must be monitored against real labeled field faults before autonomous maintenance or correction actions are enabled.
