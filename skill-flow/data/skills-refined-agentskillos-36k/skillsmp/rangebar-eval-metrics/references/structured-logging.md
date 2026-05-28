# Structured Logging Contract for AWFES Experiments

Machine-readable NDJSON logging standard for ML experiments. Enables observability, debugging, and post-hoc analysis.

## Why Structured Logging?

1. **Machine-analyzable**: NDJSON format for programmatic analysis
2. **Audit trail**: Complete record of experiment decisions
3. **Debugging**: Correlate events across distributed components
4. **Metrics extraction**: Automated pipeline monitoring

## NDJSON Schema

Every log line is a JSON object with stable schema:

```json
{
  "timestamp": "2026-01-20T15:28:45.123456+00:00",
  "level": "INFO",
  "message": "Fold 1 complete: TestSharpe=0.0576, WFE=0.183",
  "component": "awfes_v3",
  "environment": "research",
  "pid": 12345,
  "tid": 67890,
  "trace_id": "exp066_20260120_152845_abc123",
  "file": "exp066_awfes_v3.py",
  "line": 456,
  "function": "run_nested_fold",
  "context": {
    "fold_idx": 1,
    "test_sharpe": 0.0576,
    "wfe": 0.183,
    "prior_bayesian_epoch": 450,
    "val_optimal_epoch": 500
  }
}
```

## Required Fields

| Field         | Type     | Description                             |
| ------------- | -------- | --------------------------------------- |
| `timestamp`   | ISO 8601 | UTC timestamp with microseconds         |
| `level`       | enum     | DEBUG, INFO, WARNING, ERROR, CRITICAL   |
| `message`     | string   | Human-readable summary                  |
| `component`   | string   | Component identifier (e.g., "awfes_v3") |
| `environment` | string   | "research", "staging", "production"     |
| `pid`         | int      | Process ID                              |
| `tid`         | int      | Thread ID                               |
| `trace_id`    | string   | Experiment-wide correlation ID          |
| `file`        | string   | Source file name                        |
| `line`        | int      | Line number                             |
| `function`    | string   | Function name                           |

## Optional Context Field

The `context` field contains structured data specific to the log event:

### Fold Events

```json
{
  "context": {
    "fold_idx": 1,
    "n_train": 3900,
    "n_val": 780,
    "n_test": 300,
    "embargo_bars": 70
  }
}
```

### Epoch Selection Events

```json
{
  "context": {
    "fold_idx": 1,
    "prior_bayesian_epoch": 450,
    "val_optimal_epoch": 500,
    "test_epoch_used": 450,
    "wfe": 0.183,
    "frontier_epochs": [250, 450, 650]
  }
}
```

### Test Results Events

```json
{
  "context": {
    "fold_idx": 1,
    "test_sharpe": 0.0576,
    "test_hit_rate": 0.512,
    "test_n_bars": 300,
    "dsr": {
      "dsr": 0.0685,
      "sharpe_se": 0.059,
      "expected_max_null": 0.107,
      "z_score": -1.14,
      "significant": false
    }
  }
}
```

### Bayesian Update Events

```json
{
  "context": {
    "fold_idx": 1,
    "prior_mean": 425.0,
    "posterior_mean": 437.5,
    "prior_variance": 6658.0,
    "posterior_variance": 5326.4,
    "observed_epoch": 500,
    "wfe_weight": 0.183
  }
}
```

## Implementation with loguru

```python
import json
from datetime import timezone
from uuid import uuid4
from loguru import logger

COMPONENT_NAME = "awfes_v3"
ENVIRONMENT = "research"
EXPERIMENT_TRACE_ID = f"exp066_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:6]}"


def ndjson_serializer(record: dict) -> str:
    """Serialize loguru record to NDJSON with stable schema."""
    log_entry = {
        "timestamp": record["time"].astimezone(timezone.utc).isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "component": COMPONENT_NAME,
        "environment": ENVIRONMENT,
        "pid": record["process"].id,
        "tid": record["thread"].id,
        "trace_id": EXPERIMENT_TRACE_ID,
        "file": record["file"].name,
        "line": record["line"],
        "function": record["function"],
    }

    # Add context from extra fields
    if record["extra"]:
        context = {k: v for k, v in record["extra"].items() if not k.startswith("_")}
        if context:
            log_entry["context"] = context

    return json.dumps(log_entry, default=str, ensure_ascii=False)


def configure_structured_logging(log_dir: str = "logs") -> None:
    """Configure loguru for structured NDJSON logging."""
    from pathlib import Path

    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Remove default handler
    logger.remove()

    # Console: human-readable format
    logger.add(
        lambda msg: print(msg, end=""),
        format="{time:HH:mm:ss} | {level: <8} | {message}",
        level="INFO",
    )

    # File: NDJSON format with rotation
    logger.add(
        f"{log_dir}/{COMPONENT_NAME}_{{time:YYYY-MM-DD}}.ndjson",
        format="{message}",
        serialize=False,
        filter=lambda record: True,
        level="DEBUG",
        rotation="100 MB",
        retention="30 days",
    )

    # Patch the sink to use our serializer
    # (In practice, use a custom sink or serialize manually)
```

## Log Event Types

### Experiment Lifecycle

| Event                 | Level | When                    |
| --------------------- | ----- | ----------------------- |
| `experiment_start`    | INFO  | Beginning of experiment |
| `experiment_config`   | INFO  | Configuration dump      |
| `experiment_complete` | INFO  | End of experiment       |
| `experiment_error`    | ERROR | Unrecoverable failure   |

### Fold Lifecycle

| Event                       | Level | When                      |
| --------------------------- | ----- | ------------------------- |
| `fold_start`                | INFO  | Beginning of fold         |
| `fold_data_split`           | DEBUG | After data split          |
| `fold_epoch_sweep_start`    | DEBUG | Beginning epoch sweep     |
| `fold_epoch_result`         | DEBUG | Each epoch evaluation     |
| `fold_epoch_sweep_complete` | INFO  | Epoch sweep done          |
| `fold_bayesian_update`      | INFO  | Bayesian posterior update |
| `fold_test_evaluation`      | INFO  | Test set evaluation       |
| `fold_complete`             | INFO  | End of fold               |

### Critical Checkpoints (MANDATORY)

These log events MUST be present for audit compliance:

```python
# MANDATORY: v3 temporal ordering checkpoint
fold_log.info(
    "v3_temporal_checkpoint",
    fold_idx=fold_idx,
    prior_bayesian_epoch=prior_bayesian_epoch,
    val_optimal_epoch=val_optimal_epoch,
    test_epoch_used=prior_bayesian_epoch,  # MUST equal prior_bayesian_epoch
    temporal_order_valid=True,
)

# MANDATORY: DSR computation
fold_log.info(
    "dsr_computed",
    fold_idx=fold_idx,
    sharpe=test_sharpe,
    dsr=dsr_result["dsr"],
    significant=dsr_result["significant"],
    n_trials=n_trials,
)
```

## Analysis Queries

### Extract All Fold Results

```bash
# Using jq to extract fold results
cat logs/awfes_v3_*.ndjson | \
  jq -c 'select(.message | contains("fold_complete"))' | \
  jq -s '[.[] | .context]'
```

### Find Look-Ahead Violations

```bash
# v3 temporal order must have test_epoch_used == prior_bayesian_epoch
cat logs/awfes_v3_*.ndjson | \
  jq -c 'select(.message == "v3_temporal_checkpoint")' | \
  jq 'select(.context.test_epoch_used != .context.prior_bayesian_epoch)'
```

### Aggregate DSR Statistics

```bash
# Extract all DSR values
cat logs/awfes_v3_*.ndjson | \
  jq -c 'select(.message == "dsr_computed")' | \
  jq -s '{
    mean_dsr: ([.[].context.dsr] | add / length),
    n_significant: ([.[].context.significant] | map(select(. == true)) | length),
    n_total: length
  }'
```

## File Naming Convention

```
{component}_{YYYY-MM-DD}.ndjson
```

Examples:

- `awfes_v3_2026-01-20.ndjson`
- `bilstm_trainer_2026-01-20.ndjson`

## Retention Policy

| Environment | Retention | Rotation |
| ----------- | --------- | -------- |
| Research    | 30 days   | 100 MB   |
| Staging     | 7 days    | 50 MB    |
| Production  | 90 days   | 500 MB   |

## References

- [loguru documentation](https://loguru.readthedocs.io/)
- [NDJSON specification](http://ndjson.org/)
- [devops-tools:python-logging-best-practices](../../../devops-tools/skills/python-logging-best-practices/SKILL.md)
