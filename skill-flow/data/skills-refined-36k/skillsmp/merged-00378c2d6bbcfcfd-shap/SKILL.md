---
name: shap
description: Use this skill for model interpretability and explainability using SHAP (SHapley Additive exPlanations) when explaining machine learning model predictions, computing feature importance, generating SHAP plots, debugging models, analyzing model bias or fairness, comparing models, or implementing explainable AI.
---

# SHAP (SHapley Additive exPlanations)

## Overview

SHAP is a unified approach to explain machine learning model outputs using Shapley values from cooperative game theory. This skill provides comprehensive guidance for:

- Computing SHAP values for any model type
- Creating visualizations to understand feature importance
- Debugging and validating model behavior
- Analyzing fairness and bias
- Implementing explainable AI in production

SHAP works with all model types: tree-based models (XGBoost, LightGBM, CatBoost, Random Forest), deep learning models (TensorFlow, PyTorch, Keras), linear models, and black-box models.

## When to Use This Skill

**Trigger this skill when users ask about**:
- "Explain which features are most important in my model"
- "Generate SHAP plots" (waterfall, beeswarm, bar, scatter, force, heatmap, etc.)
- "Why did my model make this prediction?"
- "Calculate SHAP values for my model"
- "Visualize feature importance using SHAP"
- "Debug my model's behavior" or "validate my model"
- "Check my model for bias" or "analyze fairness"
- "Compare feature importance across models"
- "Implement explainable AI" or "add explanations to my model"
- "Understand feature interactions"
- "Create model interpretation dashboard"

## Quick Start Guide

### Step 1: Select the Right Explainer

**Decision Tree**:

1. **Tree-based model?** (XGBoost, LightGBM, CatBoost, Random Forest, Gradient Boosting)
   - Use `shap.TreeExplainer` (fast, exact)

2. **Deep neural network?** (TensorFlow, PyTorch, Keras, CNNs, RNNs, Transformers)
   - Use `shap.DeepExplainer` or `shap.GradientExplainer`

3. **Linear model?** (Linear/Logistic Regression, GLMs)
   - Use `shap.LinearExplainer` (extremely fast)

4. **Any other model?** (SVMs, custom functions, black-box models)
   - Use `shap.KernelExplainer` (model-agnostic but slower)

5. **Unsure?**
   - Use `shap.Explainer` (automatically selects best algorithm)

### Step 2: Compute SHAP Values

```python
import shap
import xgboost as xgb

# Train model
model = xgb.XGBClassifier().fit(X_train, y_train)

# Create explainer
explainer = shap.TreeExplainer(model)

# Compute SHAP values
shap_values = explainer(X_test)
```

### Step 3: Visualize Results

**For Global Understanding** (entire dataset):
```python
shap.plots.beeswarm(shap_values, max_display=15)
shap.plots.bar(shap_values)
```

**For Individual Predictions**:
```python
shap.plots.waterfall(shap_values[0])
shap.plots.force(shap_values[0])
```

**For Feature Relationships**:
```python
shap.plots.scatter(shap_values[:, "Feature_Name"])
shap.plots.scatter(shap_values[:, "Age"], color=shap_values[:, "Education"])
```

## Core Workflows

This skill supports several common workflows. Choose the workflow that matches the current task.

### Workflow 1: Basic Model Explanation

**Goal**: Understand what drives model predictions

**Steps**:
1. Train model and create appropriate explainer
2. Compute SHAP values for test set
3. Generate global importance plots (beeswarm or bar)
4. Examine top feature relationships (scatter plots)
5. Explain specific predictions (waterfall plots)

### Workflow 2: Model Debugging

**Goal**: Identify and fix model issues

**Steps**:
1. Compute SHAP values
2. Identify prediction errors
3. Explain misclassified samples
4. Check for unexpected feature importance (data leakage)
5. Validate feature relationships make sense
6. Check feature interactions

### Workflow 3: Feature Engineering

**Goal**: Use SHAP insights to improve features

**Steps**:
1. Compute SHAP values for baseline model
2. Identify nonlinear relationships (candidates for transformation)
3. Identify feature interactions (candidates for interaction terms)
4. Engineer new features
5. Retrain and compare SHAP values
6. Validate improvements

### Workflow 4: Model Comparison

**Goal**: Compare multiple models to select best interpretable option

**Steps**:
1. Train multiple models
2. Compute SHAP values for each
3. Compare global feature importance
4. Check consistency of feature rankings
5. Analyze specific predictions across models
6. Select based on accuracy, interpretability, and consistency

### Workflow 5: Fairness and Bias Analysis

**Goal**: Detect and analyze model bias across demographic groups

**Steps**:
1. Identify protected attributes (gender, race, age, etc.)
2. Compute SHAP values
3. Compare feature importance across groups
4. Check protected attribute SHAP importance
5. Identify proxy features
6. Implement mitigation strategies if bias found

### Workflow 6: Production Deployment

**Goal**: Integrate SHAP explanations into production systems

**Steps**:
1. Train and save model
2. Create and save explainer
3. Build explanation service
4. Create API endpoints for predictions with explanations
5. Implement caching and optimization
6. Monitor explanation quality

## Key Concepts

### SHAP Values

**Definition**: SHAP values quantify each feature's contribution to a prediction, measured as the deviation from the expected model output (baseline).

### Background Data / Baseline

**Purpose**: Represents "typical" input to establish baseline expectations.

### Model Output Types

**Critical Consideration**: Understand what your model outputs (raw output, probability, log-odds).

## Common Patterns

### Pattern 1: Complete Model Analysis

```python
explainer = shap.TreeExplainer(model)
shap_values = explainer(X_test)
shap.plots.beeswarm(shap_values)
shap.plots.bar(shap_values)
```

### Pattern 2: Cohort Comparison

```python
cohort1_mask = X_test['Group'] == 'A'
cohort2_mask = X_test['Group'] == 'B'
shap.plots.bar({
    "Group A": shap_values[cohort1_mask],
    "Group B": shap_values[cohort2_mask]
})
```

### Pattern 3: Debugging Errors

```python
errors = model.predict(X_test) != y_test
error_indices = np.where(errors)[0]
for idx in error_indices[:5]:
    shap.plots.waterfall(shap_values[idx])
```

## Performance Optimization

### Speed Considerations

**Explainer Speed** (fastest to slowest):
1. `LinearExplainer`
2. `TreeExplainer`
3. `DeepExplainer`
4. `GradientExplainer`
5. `KernelExplainer`
6. `PermutationExplainer`

### Optimization Strategies

**For Large Datasets**:
```python
shap_values = explainer(X_test[:1000])
```

## Troubleshooting

### Issue: Wrong explainer choice
**Solution**: Always use TreeExplainer for tree-based models.

### Issue: Insufficient background data
**Solution**: Use 100-1000 representative samples.

### Issue: Confusing units
**Solution**: Check model output type.

## Integration with Other Tools

### Jupyter Notebooks
- Interactive force plots work seamlessly.

### MLflow / Experiment Tracking
```python
import mlflow
with mlflow.start_run():
    model = train_model(X_train, y_train)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_test)
```

### Production APIs
```python
class ExplanationService:
    def __init__(self, model_path, explainer_path):
        self.model = joblib.load(model_path)
        self.explainer = joblib.load(explainer_path)

    def predict_with_explanation(self, X):
        prediction = self.model.predict(X)
        shap_values = self.explainer(X)
        return {
            'prediction': prediction[0],
            'base_value': shap_values.base_values[0],
            'feature_contributions': dict(zip(X.columns, shap_values.values[0]))
        }
```

## Reference Documentation

This skill includes comprehensive reference documentation organized by topic.

## Best Practices Summary

1. **Choose the right explainer**.
2. **Start global, then go local**.
3. **Use multiple visualizations**.
4. **Select appropriate background data**.
5. **Understand model output units**.
6. **Validate with domain knowledge**.
7. **Optimize for performance**.
8. **Check for data leakage**.
9. **Consider feature correlations**.
10. **Remember SHAP shows association, not causation**.

## Installation

```bash
pip install shap
pip install shap matplotlib
```

**Dependencies**: numpy, pandas, scikit-learn, matplotlib, scipy

**Optional**: xgboost, lightgbm, tensorflow, torch (depending on model types)

## Additional Resources

- **Official Documentation**: https://shap.readthedocs.io/
- **GitHub Repository**: https://github.com/slundberg/shap
- **Original Paper**: Lundberg & Lee (2017) - "A Unified Approach to Interpreting Model Predictions"
- **Nature MI Paper**: Lundberg et al. (2020) - "From local explanations to global understanding with explainable AI for trees"

This skill provides comprehensive coverage of SHAP for model interpretability across all use cases and model types.