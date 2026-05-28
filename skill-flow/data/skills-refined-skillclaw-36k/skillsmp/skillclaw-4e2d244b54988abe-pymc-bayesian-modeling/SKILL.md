---
name: pymc-bayesian-modeling
description: Use this skill when you need to build, fit, validate, and compare Bayesian models using the PyMC library for probabilistic programming and inference.
---

# PyMC Bayesian Modeling

## Overview

PyMC is a Python library for Bayesian modeling and probabilistic programming. It allows you to build, fit, validate, and compare Bayesian models using its modern API (version 5.x+), including hierarchical models, MCMC sampling (NUTS), variational inference, and model comparison (LOO, WAIC).

## When to Use This Skill

This skill should be used when:
- Building Bayesian models (linear/logistic regression, hierarchical models, time series, etc.)
- Performing MCMC sampling or variational inference
- Conducting prior/posterior predictive checks
- Diagnosing sampling issues (divergences, convergence, ESS)
- Comparing multiple models using information criteria (LOO, WAIC)
- Implementing uncertainty quantification through Bayesian methods
- Working with hierarchical/multilevel data structures
- Handling missing data or measurement error in a principled way

## Standard Bayesian Workflow

Follow this workflow for building and validating Bayesian models:

### 1. Data Preparation

```python
import pymc as pm
import arviz as az
import numpy as np

# Load and prepare data
X = ...  # Predictors
y = ...  # Outcomes

# Standardize predictors for better sampling
X_mean = X.mean(axis=0)
X_std = X.std(axis=0)
X_scaled = (X - X_mean) / X_std
```

**Key practices:**
- Standardize continuous predictors (improves sampling efficiency)
- Center outcomes when possible
- Handle missing data explicitly (treat as parameters)
- Use named dimensions with `coords` for clarity

### 2. Model Building

```python
coords = {
    'predictors': ['var1', 'var2', 'var3'],
    'obs_id': np.arange(len(y))
}

with pm.Model(coords=coords) as model:
    # Priors
    alpha = pm.Normal('alpha', mu=0, sigma=1)
    beta = pm.Normal('beta', mu=0, sigma=1, dims='predictors')
    sigma = pm.HalfNormal('sigma', sigma=1)

    # Linear predictor
    mu = alpha + pm.math.dot(X_scaled, beta)

    # Likelihood
    y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y, dims='obs_id')
```

**Key practices:**
- Use weakly informative priors (not flat priors)
- Use `HalfNormal` or `Exponential` for scale parameters
- Use named dimensions (`dims`) instead of `shape` when possible
- Use `pm.Data()` for values that will be updated for predictions