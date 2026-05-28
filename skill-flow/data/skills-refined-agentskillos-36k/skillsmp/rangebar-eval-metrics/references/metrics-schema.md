# Metrics JSON Schema

JSON Schema for validating range bar evaluation metrics output.

## Schema Version

```yaml
schema_version: "1.0.0"
compatible_with: "rangebar-eval-metrics@9.37+"
```

## Full Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/terrylica/cc-skills/rangebar-eval-metrics/v1",
  "title": "Range Bar Evaluation Metrics",
  "description": "Output schema for compute_metrics.py",
  "type": "object",
  "properties": {
    "weekly_sharpe": {
      "type": "number",
      "description": "Daily-aggregated Sharpe scaled to weekly (sqrt(7) for crypto, sqrt(5) for equity)"
    },
    "hit_rate": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Directional accuracy (proportion of correct sign predictions)"
    },
    "cumulative_pnl": {
      "type": "number",
      "description": "Total PnL over evaluation period"
    },
    "n_bars": {
      "type": "integer",
      "minimum": 0,
      "description": "Number of range bars in evaluation"
    },
    "positive_sharpe_rate": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Proportion of folds with positive Sharpe (aggregate only)"
    },
    "max_drawdown": {
      "type": "number",
      "maximum": 0,
      "description": "Maximum drawdown (negative value)"
    },
    "bar_sharpe": {
      "type": "number",
      "description": "Raw bar-level Sharpe (NOT daily-aggregated, for comparison only)"
    },
    "return_per_bar": {
      "type": "number",
      "description": "Average return per bar"
    },
    "profit_factor": {
      "type": "number",
      "minimum": 0,
      "description": "Gross profit / gross loss (Inf if no losses)"
    },
    "cv_fold_returns": {
      "type": "number",
      "minimum": 0,
      "description": "Coefficient of variation across fold returns"
    },
    "ic": {
      "type": ["number", "null"],
      "minimum": -1,
      "maximum": 1,
      "description": "Information Coefficient (Spearman rank correlation)"
    },
    "prediction_autocorr": {
      "type": ["number", "null"],
      "minimum": -1,
      "maximum": 1,
      "description": "Lag-1 autocorrelation of predictions (detects sticky LSTM)"
    },
    "sharpe_se": {
      "type": ["number", "null"],
      "minimum": 0,
      "description": "Standard error of Sharpe (Mertens 2002)"
    },
    "psr": {
      "type": ["number", "null"],
      "minimum": 0,
      "maximum": 1,
      "description": "Probabilistic Sharpe Ratio (Bailey & López de Prado 2012)"
    },
    "dsr": {
      "type": ["number", "null"],
      "minimum": 0,
      "maximum": 1,
      "description": "Deflated Sharpe Ratio (Bailey & López de Prado 2014)"
    },
    "skewness": {
      "type": "number",
      "description": "Skewness of daily returns"
    },
    "kurtosis": {
      "type": "number",
      "description": "Kurtosis of daily returns (Pearson form, normal = 3)"
    },
    "binomial_pvalue": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "P-value for sign test (n_positive vs n_total)"
    },
    "autocorr_lag1": {
      "type": "number",
      "minimum": -1,
      "maximum": 1,
      "description": "Lag-1 autocorrelation of fold Sharpes (aggregate only)"
    },
    "effective_n": {
      "type": "number",
      "minimum": 0,
      "description": "Autocorrelation-adjusted sample size (aggregate only)"
    },
    "var_95": {
      "type": "number",
      "description": "Value at Risk at 95% confidence (daily, negative value)"
    },
    "cvar_95": {
      "type": "number",
      "description": "Conditional VaR (Expected Shortfall) at 95%"
    },
    "omega_ratio": {
      "type": ["number", "null"],
      "minimum": 0,
      "description": "Omega ratio (gains/losses above threshold)"
    },
    "sortino_ratio": {
      "type": ["number", "null"],
      "description": "Sortino ratio (downside deviation only)"
    },
    "ulcer_index": {
      "type": "number",
      "minimum": 0,
      "description": "Ulcer Index (RMS of percentage drawdowns)"
    },
    "calmar_ratio": {
      "type": ["number", "null"],
      "description": "Calmar ratio (annual return / max drawdown)"
    },
    "error": {
      "type": "string",
      "description": "Error message if computation failed"
    }
  },
  "oneOf": [
    {
      "required": ["weekly_sharpe", "hit_rate", "cumulative_pnl", "n_bars"],
      "not": { "required": ["error"] }
    },
    {
      "required": ["error"]
    }
  ]
}
```

## Tier Mappings

### Primary Metrics (Tier 1)

| Field                  | Type    | Required | Go Threshold |
| ---------------------- | ------- | -------- | ------------ |
| `weekly_sharpe`        | number  | Yes      | > 0          |
| `hit_rate`             | number  | Yes      | > 0.50       |
| `cumulative_pnl`       | number  | Yes      | > 0          |
| `n_bars`               | integer | Yes      | >= 100       |
| `positive_sharpe_rate` | number  | Agg only | > 0.55       |

### Secondary Metrics (Tier 2)

| Field             | Type          | Required | Warning Threshold |
| ----------------- | ------------- | -------- | ----------------- |
| `max_drawdown`    | number        | No       | > -0.30           |
| `bar_sharpe`      | number        | No       | -                 |
| `return_per_bar`  | number        | No       | -                 |
| `profit_factor`   | number        | No       | > 1.0             |
| `cv_fold_returns` | number        | No       | < 1.5             |
| `ic`              | number / null | No       | > 0.02            |

### Diagnostic Metrics (Tier 3)

| Field                 | Type          | Required | Publication Threshold |
| --------------------- | ------------- | -------- | --------------------- |
| `psr`                 | number / null | No       | > 0.85                |
| `dsr`                 | number / null | No       | > 0.50                |
| `binomial_pvalue`     | number        | Agg only | < 0.05                |
| `autocorr_lag1`       | number        | Agg only | -                     |
| `effective_n`         | number        | Agg only | >= 30                 |
| `sharpe_se`           | number / null | No       | -                     |
| `skewness`            | number        | No       | -                     |
| `kurtosis`            | number        | No       | -                     |
| `prediction_autocorr` | number / null | No       | 0.3 - 0.7 (healthy)   |

### Risk Metrics (Extended)

| Field           | Type          | Required | Threshold |
| --------------- | ------------- | -------- | --------- |
| `var_95`        | number        | No       | > -0.05   |
| `cvar_95`       | number        | No       | > -0.08   |
| `omega_ratio`   | number / null | No       | > 1.0     |
| `sortino_ratio` | number / null | No       | > 0       |
| `ulcer_index`   | number        | No       | < 0.10    |
| `calmar_ratio`  | number / null | No       | > 0.5     |

## Validation Script

```python
#!/usr/bin/env python3
"""Validate metrics JSON against schema."""

import json
import sys
from pathlib import Path

try:
    from jsonschema import validate, ValidationError
except ImportError:
    print("Install jsonschema: pip install jsonschema")
    sys.exit(1)

SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "weekly_sharpe": {"type": "number"},
        "hit_rate": {"type": "number", "minimum": 0, "maximum": 1},
        "cumulative_pnl": {"type": "number"},
        "n_bars": {"type": "integer", "minimum": 0},
    },
    "oneOf": [
        {
            "required": ["weekly_sharpe", "hit_rate", "cumulative_pnl", "n_bars"],
            "not": {"required": ["error"]}
        },
        {"required": ["error"]}
    ]
}


def validate_metrics(metrics_path: Path) -> bool:
    """Validate metrics file against schema."""
    with open(metrics_path) as f:
        metrics = json.load(f)

    try:
        validate(instance=metrics, schema=SCHEMA)
        print(f"✓ {metrics_path}: Valid")
        return True
    except ValidationError as e:
        print(f"✗ {metrics_path}: {e.message}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_schema.py <metrics.json>")
        sys.exit(1)

    success = validate_metrics(Path(sys.argv[1]))
    sys.exit(0 if success else 1)
```

## Example Valid Output

### Single Fold

```json
{
  "weekly_sharpe": 1.23,
  "hit_rate": 0.54,
  "cumulative_pnl": 0.0456,
  "n_bars": 1247,
  "max_drawdown": -0.0234,
  "bar_sharpe": 0.89,
  "profit_factor": 1.34,
  "ic": 0.067,
  "prediction_autocorr": 0.45,
  "sharpe_se": 0.31,
  "psr": 0.91,
  "dsr": 0.62,
  "skewness": -0.23,
  "kurtosis": 4.12
}
```

### Aggregate

```json
{
  "mean_weekly_sharpe": 0.87,
  "std_weekly_sharpe": 0.45,
  "median_weekly_sharpe": 0.92,
  "positive_sharpe_rate": 0.68,
  "n_folds": 31,
  "binomial_pvalue": 0.023,
  "autocorr_lag1": 0.12,
  "effective_n": 27.4
}
```

### Error Case

```json
{
  "error": "no_data"
}
```

## Usage with compute_metrics.py

```bash
# Compute and validate
python scripts/compute_metrics.py \
  --predictions preds.npy \
  --actuals actuals.npy \
  --timestamps ts.npy \
  --output metrics.json

python scripts/validate_schema.py metrics.json
```

## Semantic Versioning

| Version | Changes                                                  |
| ------- | -------------------------------------------------------- |
| 1.0.0   | Initial schema with Tier 1-3 metrics                     |
| 1.1.0   | Added extended risk metrics (VaR, Sortino, Omega, Ulcer) |
| 1.2.0   | Added transaction costs fields (planned)                 |

## References

- [JSON Schema Specification](https://json-schema.org/draft/2020-12/json-schema-core)
- [rangebar-eval-metrics SKILL.md](../SKILL.md)
