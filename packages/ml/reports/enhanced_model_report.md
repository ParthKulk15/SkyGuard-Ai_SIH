# SkyGuard Enhanced Hybrid Evaluation

The test dataset was never used for fitting or augmentation. The final operational prediction uses deterministic packet-integrity, physical-range, and multi-sensor checks; the trained classifier remains available for learned drift diagnosis.

- Original training observations: 46,998
- Training observations after augmentation: 51,748
- Held-out test observations: 8,298
- Accuracy: 0.9993
- Precision: 1.0000
- Recall: 0.9412
- F1: 0.9697
- Confusion matrix: TN=8196, FP=0, FN=6, TP=96

The six false negatives are the first readings in duplicate-packet sequences. A first packet is observationally identical to a legitimate new packet; subsequent repeated packets are detected causally.
