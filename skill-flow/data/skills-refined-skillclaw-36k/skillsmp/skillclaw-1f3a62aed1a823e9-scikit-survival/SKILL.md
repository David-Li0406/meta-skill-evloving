---
name: scikit-survival
description: Use this skill when performing survival analysis and time-to-event modeling in Python with the scikit-survival library, particularly when dealing with censored data and fitting various survival models.
---

# Skill body

## Overview

scikit-survival is a Python library for survival analysis built on top of scikit-learn. It provides specialized tools for time-to-event analysis, addressing the unique challenges of censored data where some observations are only partially known.

## When to Use This Skill

Use this skill when:
- Performing survival analysis or time-to-event modeling
- Working with censored data (right-censored, left-censored, or interval-censored)
- Fitting Cox proportional hazards models (standard or penalized)
- Building ensemble survival models (Random Survival Forests, Gradient Boosting)
- Training Survival Support Vector Machines
- Evaluating survival model performance (concordance index, Brier score, time-dependent AUC)
- Estimating Kaplan-Meier or Nelson-Aalen curves
- Analyzing competing risks
- Preprocessing survival data or handling missing values in survival datasets

## Core Capabilities

### 1. Model Types and Selection

scikit-survival provides multiple model families, each suited for different scenarios:

#### Cox Proportional Hazards Models
**Use for**: Standard survival analysis with interpretable coefficients
- `CoxPHSurvivalAnalysis`: Basic Cox model
- `CoxnetSurvivalAnalysis`: Penalized Cox with elastic net for high-dimensional data
- `IPCRidge`: Ridge regression for accelerated failure time models

#### Ensemble Methods
**Use for**: High predictive performance with complex non-linear relationships
- `RandomSurvivalForest`: Robust, non-parametric ensemble method
- `GradientBoostingSurvivalAnalysis`: Gradient boosting for survival data

### 2. Model Evaluation
- Evaluate model performance using metrics such as the concordance index and Brier score.
- Conduct time-dependent AUC analysis for more nuanced performance insights.

### 3. Data Handling
- Preprocess survival data, including handling missing values and ensuring proper formatting for analysis.

### 4. Competing Risks
- Analyze competing risks to understand the impact of different events on survival outcomes.

## Conclusion

This skill encapsulates the essential functionalities of the scikit-survival library, providing a comprehensive toolkit for conducting survival analysis in Python.