---
name: engineering-features-for-machine-learning
description: Use this skill when you need to create, select, or transform features to enhance the performance of machine learning models.
---

# Skill body

## Overview

This skill enables Claude to leverage the feature-engineering-toolkit plugin to enhance machine learning models. It automates the process of creating new features, selecting the most relevant ones, and transforming existing features to better suit the model's needs. By using this skill, you can improve the accuracy, efficiency, and interpretability of your machine learning models.

## How It Works

1. **Analyzing Requirements**: Claude analyzes the user's request and identifies the specific feature engineering task required.
2. **Generating Code**: Claude generates Python code using the feature-engineering-toolkit plugin to perform the requested task, including data validation and error handling.
3. **Executing Task**: The generated code is executed, creating, selecting, or transforming features as requested.
4. **Providing Insights**: Claude provides performance metrics and insights related to the feature engineering process, such as the importance of newly created features or the impact of transformations on model performance.

## When to Use This Skill

This skill activates when you need to:
- Create new features from existing data to improve model accuracy.
- Select the most relevant features from a dataset to reduce model complexity and improve efficiency.
- Transform features to better suit the assumptions of a machine learning model (e.g., scaling, normalization, encoding).

## Examples

### Example 1: Improving Model Accuracy

User request: "Create new features from the existing 'age' and 'income' columns to improve the accuracy of a customer churn prediction model."

The skill will:
1. Generate code to create interaction terms between 'age' and 'income' (e.g., age * income, age / income).
2. Execute the code and evaluate the impact of the new features on model performance.

### Example 2: Selecting Relevant Features

User request: "Select the most important features from my dataset to enhance the model's performance."

The skill will:
1. Analyze the dataset and identify the features that contribute most to the model's predictive power.
2. Generate code to filter out less relevant features and provide a refined dataset for modeling.