"""
Breast Cancer Classification — Baseline Model
===============================================
This script trains a baseline SVM classifier on the Wisconsin Breast Cancer dataset.
The current hyperparameters are untuned defaults — accuracy is around 90%.

Usage:
    python train_baseline.py

Output:
    results/baseline_metrics.json
"""

import json
import os
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Load dataset
data = load_breast_cancer()
X, y = data.data, data.target
feature_names = list(data.feature_names)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Dataset: {data.DESCR.split(chr(10))[0]}")
print(f"Features: {X.shape[1]}, Samples: {X.shape[0]}")
print(f"Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")
print(f"Class distribution: {dict(zip(*np.unique(y, return_counts=True)))}")

# -------------------------------------------------------------------
# Baseline: SVM with deliberately suboptimal hyperparameters
# - No feature scaling (SVM is highly sensitive to feature magnitudes)
# - Linear kernel (may underfit nonlinear boundaries)
# - Very small C (excessive regularization, underfitting)
# -------------------------------------------------------------------
model = SVC(kernel="linear", C=0.001, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")

metrics = {
    "model": "SVC",
    "hyperparameters": {"kernel": "linear", "C": 0.001, "scaling": False},
    "test_accuracy": round(accuracy_score(y_test, y_pred), 4),
    "test_precision": round(precision_score(y_test, y_pred), 4),
    "test_recall": round(recall_score(y_test, y_pred), 4),
    "test_f1": round(f1_score(y_test, y_pred), 4),
    "cv_mean_accuracy": round(cv_scores.mean(), 4),
    "cv_std_accuracy": round(cv_scores.std(), 4),
}

out_path = os.path.join(RESULTS_DIR, "baseline_metrics.json")
with open(out_path, "w") as f:
    json.dump(metrics, f, indent=2)

print(f"\n=== Baseline Results ===")
for k, v in metrics.items():
    print(f"  {k}: {v}")
print(f"\nSaved to {out_path}")
print("NOTE: This baseline is intentionally untuned. Accuracy can be significantly")
print("      improved through proper feature scaling and hyperparameter optimization.")
