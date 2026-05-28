**Skill**: [MLflow Python](../SKILL.md)

# Query Patterns

DataFrame operations for analyzing MLflow experiments and runs.

## Basic Queries

### List All Experiments

```bash
uv run scripts/query_experiments.py experiments
```

### Search Runs in Experiment

```bash
uv run scripts/query_experiments.py runs --experiment "crypto-backtests"
```

## Filtering Runs

MLflow uses SQL-like filter syntax:

### By Metrics

```bash
# Sharpe ratio > 1.5
uv run scripts/query_experiments.py runs \
  --experiment "crypto-backtests" \
  --filter "metrics.sharpe_ratio > 1.5"

# Multiple conditions (AND)
uv run scripts/query_experiments.py runs \
  --experiment "crypto-backtests" \
  --filter "metrics.sharpe_ratio > 1.5 AND metrics.max_drawdown > -0.2"

# Max drawdown better than -15%
uv run scripts/query_experiments.py runs \
  --experiment "crypto-backtests" \
  --filter "metrics.max_drawdown > -0.15"
```

### By Parameters

```bash
# Specific strategy
uv run scripts/query_experiments.py runs \
  --experiment "crypto-backtests" \
  --filter "params.strategy = 'momentum'"

# Timeframe filter
uv run scripts/query_experiments.py runs \
  --experiment "crypto-backtests" \
  --filter "params.timeframe = '1h'"
```

### By Run Status

```bash
# Only completed runs
uv run scripts/query_experiments.py runs \
  --experiment "crypto-backtests" \
  --filter "status = 'FINISHED'"

# Failed runs
uv run scripts/query_experiments.py runs \
  --experiment "crypto-backtests" \
  --filter "status = 'FAILED'"
```

## Ordering Results

```bash
# Best Sharpe ratio first
uv run scripts/query_experiments.py runs \
  --experiment "crypto-backtests" \
  --order-by "metrics.sharpe_ratio DESC"

# Most recent first
uv run scripts/query_experiments.py runs \
  --experiment "crypto-backtests" \
  --order-by "start_time DESC"

# Lowest drawdown first (least negative)
uv run scripts/query_experiments.py runs \
  --experiment "crypto-backtests" \
  --order-by "metrics.max_drawdown DESC"
```

## Output Formats

### Table (Default)

```bash
uv run scripts/query_experiments.py runs --experiment "crypto-backtests" --format table
```

### CSV Export

```bash
uv run scripts/query_experiments.py runs \
  --experiment "crypto-backtests" \
  --format csv > results.csv
```

### JSON Export

```bash
uv run scripts/query_experiments.py runs \
  --experiment "crypto-backtests" \
  --format json > results.json
```

## Selecting Columns

```bash
# Specific columns only
uv run scripts/query_experiments.py runs \
  --experiment "crypto-backtests" \
  --columns "run_name,metrics.sharpe_ratio,metrics.max_drawdown,params.strategy"
```

## Python API Patterns

For advanced queries, use the MLflow Python API directly:

```python
import mlflow
import pandas as pd

# Get experiment
experiment = mlflow.get_experiment_by_name("crypto-backtests")

# Search with complex filters
runs = mlflow.search_runs(
    experiment_ids=[experiment.experiment_id],
    filter_string="metrics.sharpe_ratio > 1.0",
    order_by=["metrics.sharpe_ratio DESC"],
    max_results=100
)

# DataFrame operations
best_runs = runs[runs["metrics.win_rate"] > 0.5]
grouped = runs.groupby("params.strategy")["metrics.sharpe_ratio"].mean()

# Export
runs.to_csv("analysis.csv", index=False)
runs.to_parquet("analysis.parquet")
```

## Filter Syntax Reference

| Operator | Example                        | Description      |
| -------- | ------------------------------ | ---------------- |
| `=`      | `params.strategy = 'momentum'` | Equals           |
| `!=`     | `status != 'FAILED'`           | Not equals       |
| `>`      | `metrics.sharpe_ratio > 1.5`   | Greater than     |
| `>=`     | `metrics.win_rate >= 0.5`      | Greater or equal |
| `<`      | `metrics.max_drawdown < -0.1`  | Less than        |
| `<=`     | `metrics.volatility <= 0.3`    | Less or equal    |
| `LIKE`   | `params.strategy LIKE 'mom%'`  | Pattern match    |
| `AND`    | `... AND ...`                  | Logical AND      |
| `OR`     | `... OR ...`                   | Logical OR       |
