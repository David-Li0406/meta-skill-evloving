---
name: aeon
description: Use this skill for time series machine learning tasks such as classification, regression, clustering, forecasting, anomaly detection, segmentation, and similarity search when working with temporal data and sequential patterns.
---

# Aeon Time Series Machine Learning

## Overview

Aeon is a scikit-learn compatible Python toolkit for time series machine learning. It provides state-of-the-art algorithms for various tasks including classification, regression, clustering, forecasting, anomaly detection, segmentation, and similarity search.

## When to Use This Skill

Apply this skill when:
- Classifying or predicting from time series data
- Detecting anomalies or change points in temporal sequences
- Clustering similar time series patterns
- Forecasting future values
- Finding repeated patterns (motifs) or unusual subsequences (discords)
- Comparing time series with specialized distance metrics
- Extracting features from temporal data

## Installation

```bash
pip install aeon
```

## Core Capabilities

### 1. Time Series Classification

Categorize time series into predefined classes. 

**Quick Start:**
```python
from aeon.classification.convolution_based import RocketClassifier
from aeon.datasets import load_classification

# Load data
X_train, y_train = load_classification("GunPoint", split="train")
X_test, y_test = load_classification("GunPoint", split="test")

# Train classifier
clf = RocketClassifier(n_kernels=10000)
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
```

**Algorithm Selection:**
- **Speed + Performance**: `MiniRocketClassifier`, `Arsenal`
- **Maximum Accuracy**: `HIVECOTEV2`, `InceptionTimeClassifier`
- **Interpretability**: `ShapeletTransformClassifier`, `Catch22Classifier`
- **Small Datasets**: `KNeighborsTimeSeriesClassifier` with DTW distance

### 2. Time Series Regression

Predict continuous values from time series.

**Quick Start:**
```python
from aeon.regression.convolution_based import RocketRegressor
from aeon.datasets import load_regression

X_train, y_train = load_regression("Covid3Month", split="train")
X_test, y_test = load_regression("Covid3Month", split="test")

reg = RocketRegressor()
reg.fit(X_train, y_train)
predictions = reg.predict(X_test)
```