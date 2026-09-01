import numpy as np
import pandas as pd
from typing import Dict, Any, List
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix


def compute_binary_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Computes precision, recall, F1, FPR, TPR, accuracy, and confusion matrix entries."""
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    accuracy = accuracy_score(y_true, y_pred)
    
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    return {
        'precision': float(precision),
        'recall': float(recall),
        'f1': float(f1),
        'fpr': float(fpr),
        'tpr': float(tpr),
        'accuracy': float(accuracy),
        'tn': int(tn),
        'fp': int(fp),
        'fn': int(fn),
        'tp': int(tp)
    }


def compute_per_anomaly_type_performance(df: pd.DataFrame, y_pred: np.ndarray) -> pd.DataFrame:

    records = []
    fault_types = sorted(df['fault_type'].unique().tolist())
    
    for ft in fault_types:
        sub_mask = df['fault_type'] == ft
        y_true_sub = df.loc[sub_mask, 'is_anomaly'].values
        y_pred_sub = y_pred[sub_mask]
        count = len(y_true_sub)
        
        # If it's NORMAL, anomaly ground truth is 0. If it's a fault, ground truth is 1.
        prec = precision_score(y_true_sub, y_pred_sub, zero_division=0)
        rec = recall_score(y_true_sub, y_pred_sub, zero_division=0)
        f1 = f1_score(y_true_sub, y_pred_sub, zero_division=0)
        
        cm = confusion_matrix(y_true_sub, y_pred_sub, labels=[0, 1])
        tn, fp, fn, tp = cm.ravel()
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        
        records.append({
            'anomaly_type': ft,
            'count': count,
            'precision': round(float(prec), 4),
            'recall': round(float(rec), 4),
            'F1': round(float(f1), 4),
            'false_positive_rate': round(float(fpr), 4)
        })
        
    return pd.DataFrame(records)
