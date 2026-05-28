---
name: explaining-machine-learning-models
description: Use this skill when you need to provide interpretability and explainability for machine learning models, helping users understand model predictions, feature importance, and overall behavior.
---

# Skill body

## Overview

This skill empowers Claude to analyze and explain machine learning models. It helps users understand why a model makes certain predictions, identify the most influential features, and gain insights into the model's overall behavior.

## How It Works

1. **Analyze Context**: Claude analyzes the user's request and the available model data.
2. **Select Explanation Technique**: Claude chooses the most appropriate explanation technique (e.g., SHAP, LIME) based on the model type and the user's needs.
3. **Generate Explanations**: Claude uses the selected technique to generate explanations for model predictions.
4. **Present Results**: Claude presents the explanations in a clear and concise format, highlighting key insights and feature importances.

## When to Use This Skill

This skill activates when you need to:
- Understand why a machine learning model made a specific prediction.
- Identify the most important features influencing a model's output.
- Debug model performance issues by identifying unexpected feature interactions.
- Communicate model insights to non-technical stakeholders.
- Ensure fairness and transparency in model predictions.

## Examples

### Example 1: Understanding Loan Application Decisions

User request: "Explain why this loan application was rejected."

The skill will:
1. Analyze the loan application data and the model's prediction.
2. Calculate SHAP values to determine the contribution of each feature to the rejection decision.
3. Present the results, highlighting the features that most strongly influenced the outcome, such as credit score or debt-to-income ratio.

### Example 2: Identifying Key Factors in Customer Churn

User request: "Interpret the customer churn model and identify the most important factors."

The skill will:
1. Analyze the customer churn model and its predictions.
2. Use LIME to generate explanations for the model's predictions.
3. Present the key factors influencing customer churn, such as service usage or customer demographics.