# Breast Cancer Classification

Binary classification task on the **Wisconsin Breast Cancer** dataset (569 samples, 30 features).

## Problem

Predict whether a tumor is **malignant** (0) or **benign** (1) based on computed features from digitized images of fine needle aspirate (FNA) of breast mass.

## Current Status

The baseline model (`train_baseline.py`) uses an SVM with suboptimal hyperparameters and achieves ~90% accuracy. We need to improve this through systematic hyperparameter tuning.

## Project Structure

```
ml_project/
├── train_baseline.py      # Baseline training script
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── results/               # Output directory (auto-created)
```

## Goal

Optimize the SVM classifier to achieve **≥96% test accuracy** using:
1. Grid Search
2. Bayesian Optimization (Optuna)

Compare both approaches and report the best configuration.
