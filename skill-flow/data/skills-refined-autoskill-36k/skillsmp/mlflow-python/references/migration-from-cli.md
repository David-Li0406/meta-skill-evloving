**Skill**: [MLflow Python](../SKILL.md)

# Migration from CLI

Mapping from MLflow CLI commands to Python API scripts.

## Why Migrate?

| Feature          | CLI               | Python API             |
| ---------------- | ----------------- | ---------------------- |
| Log metrics      | **Not supported** | `mlflow.log_metrics()` |
| Log parameters   | **Not supported** | `mlflow.log_params()`  |
| Query runs       | Text parsing      | DataFrame output       |
| Metric history   | Not available     | Native support         |
| Filter syntax    | Limited           | Full SQL-like          |
| Authentication   | Embedded in URI   | Separate env vars      |
| Batch operations | Not supported     | Full support           |

## Command Mapping

### List Experiments

```bash
# Old (CLI)
mlflow experiments search --view-type ACTIVE_ONLY

# New (Python)
uv run scripts/query_experiments.py experiments
```

### List Runs

```bash
# Old (CLI)
mlflow runs list --experiment-id 1

# New (Python)
uv run scripts/query_experiments.py runs --experiment "experiment-name"
```

### Create Experiment

```bash
# Old (CLI)
mlflow experiments create --experiment-name "my-experiment"

# New (Python)
uv run scripts/create_experiment.py --name "my-experiment" --description "Description here"
```

### Log Metrics (NEW - CLI Cannot Do This)

```bash
# CLI: Not possible!

# Python API:
uv run scripts/log_backtest.py \
  --experiment "crypto-backtests" \
  --run-name "btc_momentum" \
  --returns data.csv
```

### Get Metric History (NEW - CLI Cannot Do This)

```bash
# CLI: Not possible!

# Python API:
uv run scripts/get_metric_history.py --run-id abc123 --metrics sharpe_ratio
```

## Authentication Migration

### Old Pattern (Non-Idiomatic)

```bash
# Credentials embedded in URI (problematic)
export MLFLOW_TRACKING_URI="http://user:pass@mlflow.server.com:5000"
```

### New Pattern (Idiomatic)

```bash
# Separate environment variables
export MLFLOW_TRACKING_URI="http://mlflow.server.com:5000"
export MLFLOW_TRACKING_USERNAME="user"
export MLFLOW_TRACKING_PASSWORD="pass"
```

Or via mise `.env.local`:

```bash
# .env.local (gitignored)
MLFLOW_TRACKING_URI=http://mlflow.eonlabs.com:5000
MLFLOW_TRACKING_USERNAME=eonlabs
MLFLOW_TRACKING_PASSWORD=<password>
```

## Features Only Available in Python API

### 1. Log Metrics and Parameters

```python
import mlflow

with mlflow.start_run():
    mlflow.log_params({"strategy": "momentum", "lookback": 20})
    mlflow.log_metrics({"sharpe": 1.5, "max_drawdown": -0.15})
```

### 2. Metric History

```python
client = mlflow.tracking.MlflowClient()
history = client.get_metric_history(run_id, "sharpe_ratio")
```

### 3. DataFrame Queries

```python
runs = mlflow.search_runs(
    experiment_ids=["1"],
    filter_string="metrics.sharpe_ratio > 1.5",
    order_by=["metrics.sharpe_ratio DESC"]
)
# Returns pandas DataFrame
```

### 4. Batch Operations

```python
# Update multiple runs
for run_id in run_ids:
    mlflow.set_tag(run_id, "reviewed", "true")
```

### 5. Artifact Management

```python
# Log artifacts
mlflow.log_artifact("model.pkl")
mlflow.log_artifacts("./model_dir")

# Download artifacts
client.download_artifacts(run_id, "model.pkl", "./local_dir")
```

## Deleted Skill: mlflow-query

The `mlflow-query` skill has been deleted. It used:

- CLI commands (`uvx mlflow experiments search`)
- Text parsing of CLI output
- Doppler for credentials (non-idiomatic for MLflow)

All functionality is now available in `mlflow-python` with:

- Python API (more powerful)
- DataFrame output (easier analysis)
- mise `[env]` for configuration (idiomatic)
