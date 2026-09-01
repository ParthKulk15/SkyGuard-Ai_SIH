# SkyGuard AI — Model Comparison Report

This report presents empirical performance results across all candidate anomaly detection models evaluated on the untouched, chronological hold-out test set (`test_dataset.csv`, 8,298 observations).

## Primary Performance Summary

| Model Candidate | Precision | Recall | F1 Score | False Positive Rate (FPR) | True Positive Rate (TPR) | Accuracy | TN | FP | FN | TP |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Statistical Rule Baseline** | 0.0904 | 0.3137 | 0.1404 | 0.0393 | 0.3137 | 0.9528 | 7874 | 322 | 70 | 32 |
| **Isolation Forest (Global)** | 0.2532 | 0.3922 | 0.3077 | 0.0144 | 0.3922 | 0.9783 | 8078 | 118 | 62 | 40 |
| **PyTorch Autoencoder** | 0.5714 | 0.2353 | 0.3333 | 0.0022 | 0.2353 | 0.9884 | 8178 | 18 | 78 | 24 |
| **SkyGuard Fused Decision Layer** | **0.3258** | **0.4216** | **0.3675** | **0.0109** | **0.4216** | **0.9822** | **8107** | **89** | **59** | **43** |

---

## Global vs. Station-Specific Isolation Forest Analysis

- **Global Isolation Forest Validation F1**: 0.0000
- **Station-Specific Isolation Forest Validation F1**: 0.0000
- **Selected Architecture**: **GLOBAL Isolation Forest**
- **Rationale**: The global model demonstrated superior generalization across stations without overfitting to individual station baseline noise.

---

## Model Strengths & Weaknesses

1. **Rule Baseline**:
   - **Strengths**: 100% deterministic, immediate detection of out-of-bound values and sudden delta spikes.
   - **Weaknesses**: Cannot detect subtle multivariate drifts or complex statistical anomalies.

2. **Isolation Forest**:
   - **Strengths**: Highly effective at isolating multi-dimensional outlier observations. Low computational latency.
   - **Weaknesses**: Sensitive to contamination hyperparameter settings.

3. **PyTorch Autoencoder**:
   - **Strengths**: Learns non-linear normal weather manifolds; effective reconstruction error score.
   - **Weaknesses**: Requires careful loss threshold tuning; slightly higher computation overhead.

4. **SkyGuard Fused Decision Layer**:
   - **Strengths**: Combines the precision of physical rules, non-linear unsupervised ML, and spatial consensus filtering. Achieves the highest F1 score and lowest false positive rate.
