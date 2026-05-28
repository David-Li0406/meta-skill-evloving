---
name: AI/ML Operations
description: This skill should be used when the user asks to "deploy ML model", "MLOps", "model serving", "feature store", "experiment tracking", "model registry", "ML pipeline", "model monitoring", "GPU inference", "TensorFlow Serving", "MLflow", or needs help with machine learning operations and model deployment.
version: 1.0.0
---

# AI/ML Operations

Comprehensive guidance for MLOps, model deployment, and ML infrastructure.

## ML Pipeline Architecture

```
Data → Feature Engineering → Training → Evaluation → Registry → Serving → Monitoring
                                          ↑                            ↓
                                          └────── Retraining ──────────┘
```

## Model Serving

### TensorFlow Serving

```bash
docker run -p 8501:8501 \
  -v /models/mymodel:/models/mymodel \
  -e MODEL_NAME=mymodel \
  tensorflow/serving

# Inference
curl -X POST http://localhost:8501/v1/models/mymodel:predict \
  -d '{"instances": [[1.0, 2.0, 3.0]]}'
```

### Triton Inference Server

```bash
docker run --gpus=all -p 8000:8000 -p 8001:8001 -p 8002:8002 \
  -v /models:/models \
  nvcr.io/nvidia/tritonserver:23.10-py3 \
  tritonserver --model-repository=/models
```

## MLflow

```python
import mlflow

# Start experiment
mlflow.set_experiment("my-experiment")

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("epochs", 100)

    # Train model
    model = train_model(...)

    # Log metrics
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.05)

    # Log model
    mlflow.sklearn.log_model(model, "model")
```

## Feature Store

### Feast

```python
from feast import FeatureStore

store = FeatureStore(repo_path=".")

# Get features for inference
features = store.get_online_features(
    features=["user_features:age", "user_features:income"],
    entity_rows=[{"user_id": 123}]
).to_dict()
```

## Model Monitoring

- **Data drift detection** - Compare input distributions
- **Prediction drift** - Monitor output distributions
- **Performance degradation** - Track accuracy over time
- **Latency monitoring** - Inference time SLOs

## GPU Infrastructure

### Kubernetes GPU Scheduling

```yaml
resources:
  limits:
    nvidia.com/gpu: 1
nodeSelector:
  accelerator: nvidia-tesla-v100
```

## Additional Resources

### Reference Files
- **`references/mlops-tools.md`** - MLOps tool comparison
- **`references/model-serving.md`** - Model serving patterns
