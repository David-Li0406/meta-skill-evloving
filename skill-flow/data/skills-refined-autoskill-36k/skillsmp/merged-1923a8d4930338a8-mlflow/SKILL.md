---
name: mlflow
description: Use this skill for managing the ML lifecycle with MLflow, including tracking experiments, packaging models, managing registries, and deploying models.
---

# MLflow Skill

Complete guide for MLflow - ML lifecycle platform.

## When to Use This Skill

Use MLflow when you need to:
- Track ML experiments with parameters, metrics, and artifacts.
- Manage model registries with versioning and stage transitions.
- Deploy models to various platforms (local, cloud, serving).
- Reproduce experiments with project configurations.
- Compare model versions and performance metrics.
- Collaborate on ML projects with team workflows.
- Integrate with any ML framework (framework-agnostic).

## Installation

```bash
# Core
pip install mlflow

# With extras
pip install mlflow[extras]  # Includes SQLAlchemy, boto3, etc.
```

## Quick Reference

### Components
| Component | Description |
|-----------|-------------|
| **Tracking** | Log experiments |
| **Projects** | Package ML code |
| **Models** | Model packaging |
| **Registry** | Model versioning |
| **Serving** | Model deployment |

### CLI Commands
```bash
mlflow run .                    # Run project
mlflow ui                       # Start UI
mlflow models serve -m model    # Serve model
mlflow server                   # Start tracking server
```

## Experiment Tracking

### Basic Logging
```python
import mlflow

# Set experiment
mlflow.set_experiment("my-experiment")

# Start run
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("epochs", 100)

    # Log metrics
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.05)

    # Log multiple metrics over time
    for epoch in range(10):
        mlflow.log_metric("train_loss", 0.1 - epoch * 0.01, step=epoch)

    # Log artifacts
    mlflow.log_artifact("model.pkl")
    mlflow.log_artifacts("./outputs")

    # Log tags
    mlflow.set_tag("model_type", "neural_network")
```

### Auto-Logging
```python
import mlflow

# Enable autologging for various frameworks
mlflow.sklearn.autolog()
mlflow.pytorch.autolog()
mlflow.tensorflow.autolog()
mlflow.xgboost.autolog()
mlflow.lightgbm.autolog()
```

### Manual Run Management
```python
# Create run manually
run = mlflow.start_run(run_name="my-run")
try:
    mlflow.log_param("param1", "value1")
    mlflow.log_metric("metric1", 0.9)
finally:
    mlflow.end_run()

# Get run info
run_id = run.info.run_id
print(f"Run ID: {run_id}")

# Resume run
with mlflow.start_run(run_id=run_id):
    mlflow.log_metric("additional_metric", 0.95)
```

### Nested Runs
```python
with mlflow.start_run(run_name="parent"):
    mlflow.log_param("parent_param", "value")

    for i in range(3):
        with mlflow.start_run(run_name=f"child_{i}", nested=True):
            mlflow.log_param("child_param", i)
            mlflow.log_metric("child_metric", i * 0.1)
```

## Model Logging

### Log Scikit-learn Model
```python
from sklearn.ensemble import RandomForestClassifier
import mlflow.sklearn

model = RandomForestClassifier()
model.fit(X_train, y_train)

with mlflow.start_run():
    # Log model
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="my-rf-model"
    )
```

### Log PyTorch Model
```python
import mlflow.pytorch

with mlflow.start_run():
    mlflow.pytorch.log_model(
        pytorch_model=model,
        artifact_path="model",
        conda_env="conda.yaml",
        code_paths=["./src"]
    )
```

### Load Model
```python
# From run
model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

# From registry
model = mlflow.sklearn.load_model("models:/my-model/1")
model = mlflow.sklearn.load_model("models:/my-model/Production")

# As PyFunc
model = mlflow.pyfunc.load_model(f"runs:/{run_id}/model")
predictions = model.predict(X_test)
```

## Model Registry

### Register Model
```python
# During logging
mlflow.sklearn.log_model(
    model,
    "model",
    registered_model_name="my-model"
)

# After logging
result = mlflow.register_model(
    model_uri=f"runs:/{run_id}/model",
    name="my-model"
)
```

### Manage Versions
```python
from mlflow import MlflowClient

client = MlflowClient()

# Get model versions
versions = client.search_model_versions("name='my-model'")

# Transition stage
client.transition_model_version_stage(
    name="my-model",
    version=1,
    stage="Production"  # None, Staging, Production, Archived
)

# Add description
client.update_model_version(
    name="my-model",
    version=1,
    description="Production model v1"
)

# Add tags
client.set_model_version_tag(
    name="my-model",
    version=1,
    key="validation_status",
    value="approved"
)
```

## Model Serving

### Local Serving
```bash
# Serve from run
mlflow models serve -m runs:/<run_id>/model -p 5001

# Serve from registry
mlflow models serve -m models:/my-model/Production -p 5001
```

### Make Predictions
```bash
curl -X POST http://localhost:5001/invocations \
  -H "Content-Type: application/json" \
  -d '{"dataframe_split": {"columns": ["a", "b"], "data": [[1, 2]]}}'
```

## Best Practices

1. **Always set experiment** - Organize runs.
2. **Log signatures** - Model input/output schemas.
3. **Use auto-logging** - Reduce boilerplate.
4. **Version models** - Track production models.
5. **Use artifacts** - Store plots, configs.
6. **Tag runs** - Searchable metadata.
7. **Nested runs** - Hyperparameter tuning.
8. **Remote tracking** - Collaborate with team.
9. **CI/CD integration** - Automated training.
10. **Monitor serving** - Track predictions.

## Resources

- **Documentation**: https://mlflow.org/docs/latest
- **GitHub**: https://github.com/mlflow/mlflow