---
name: statsmodels
description: Use this skill when you need to perform statistical modeling and inference in Python, including regression analysis, time series forecasting, and diagnostics.
---

# Statsmodels: Statistical Modeling and Econometrics

## Overview

Statsmodels is Python's premier library for statistical modeling, providing tools for estimation, inference, and diagnostics across a wide range of statistical methods. Apply this skill for rigorous statistical analysis, from simple linear regression to complex time series models and econometric analyses.

## When to Use This Skill

This skill should be used when:
- Fitting regression models (OLS, WLS, GLS, quantile regression)
- Performing generalized linear modeling (logistic, Poisson, Gamma, etc.)
- Analyzing discrete outcomes (binary, multinomial, count, ordinal)
- Conducting time series analysis (ARIMA, SARIMAX, VAR, forecasting)
- Running statistical tests and diagnostics
- Testing model assumptions (heteroskedasticity, autocorrelation, normality)
- Detecting outliers and influential observations
- Comparing models (AIC/BIC, likelihood ratio tests)
- Estimating causal effects
- Producing publication-ready statistical tables and inference

## Quick Start Guide

### Linear Regression (OLS)

```python
import statsmodels.api as sm
import numpy as np
import pandas as pd

# Prepare data - ALWAYS add constant for intercept
X = sm.add_constant(X_data)

# Fit OLS model
model = sm.OLS(y, X)
results = model.fit()

# View comprehensive results
print(results.summary())

# Key results
print(f"R-squared: {results.rsquared:.4f}")
print(f"Coefficients:\\n{results.params}")
print(f"P-values:\\n{results.pvalues}")

# Predictions with confidence intervals
predictions = results.get_prediction(X_new)
pred_summary = predictions.summary_frame()
print(pred_summary)  # includes mean, CI, prediction intervals

# Diagnostics
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(results.resid, X)
print(f"Breusch-Pagan p-value: {bp_test[1]:.4f}")

# Visualize residuals
import matplotlib.pyplot as plt
plt.scatter(results.fittedvalues, results.resid)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.show()
```