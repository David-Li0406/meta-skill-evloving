---
name: tuning-hyperparameters
description: Use this skill when you need to optimize machine learning model hyperparameters through grid search, random search, or Bayesian optimization to enhance model performance.
---

# Skill body

## Overview

This skill empowers Claude to fine-tune machine learning models by automatically searching for the optimal hyperparameter configurations. It leverages different search strategies (grid, random, Bayesian) to efficiently explore the hyperparameter space and identify settings that maximize model performance.

## How It Works

1. **Analyzing Requirements**: Claude analyzes the user's request to determine the model, the hyperparameters to tune, the search strategy, and the evaluation metric.
2. **Generating Code**: Claude generates Python code using appropriate ML libraries (e.g., scikit-learn, Optuna) to implement the specified hyperparameter search. The code includes data loading, preprocessing, model training, and evaluation.
3. **Executing Search**: The generated code is executed to perform the hyperparameter search. The plugin iterates through different hyperparameter combinations, trains the model with each combination, and evaluates its performance.
4. **Reporting Results**: Claude reports the best hyperparameter configuration found during the search, along with the corresponding performance metrics. It also provides insights into the search process and potential areas for further optimization.

## When to Use This Skill

This skill activates when you need to:
- Optimize the performance of a machine learning model.
- Automatically search for the best hyperparameter settings.
- Compare different hyperparameter search strategies.
- Improve model accuracy, precision, recall, or other relevant metrics.

## Examples

### Example 1: Optimizing a Random Forest Model

User request: "Tune hyperparameters of a Random Forest model using grid search to maximize accuracy on the iris dataset. Consider n_estimators and max_depth."

The skill will:
1. Generate code to perform a grid search over the specified hyperparameters (n_estimators, max_depth) of a Random Forest model using the iris dataset.
2. Execute the code and return the best hyperparameter configuration along with the model's performance metrics.