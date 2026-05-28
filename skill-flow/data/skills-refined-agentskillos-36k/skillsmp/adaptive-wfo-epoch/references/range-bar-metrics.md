# Range Bar Metrics: Time-Weighted Sharpe Ratio

Machine-readable reference for computing risk-adjusted returns on range bar data where bars have variable duration.

**Source**: Alpha Forge AWFES experiments (2025-2026)
**Validated**: BTCUSDT range bar backtests with threshold 100

---

## Critical Issue: Why Simple Bar Sharpe Fails

### The Problem

Range bars are NOT time-uniform. A single range bar can span:

- 30 seconds (high volatility)
- 3 hours (low volatility)

Using simple `bar_sharpe = mean(bar_pnl) / std(bar_pnl)` treats all bars equally, which:

| Issue                      | Impact                                           |
| -------------------------- | ------------------------------------------------ |
| Violates i.i.d. assumption | Statistical inference invalid                    |
| Over-weights short bars    | Noise from volatile periods dominates            |
| Under-weights long bars    | Stable returns get discounted                    |
| Misleading Sharpe values   | Cannot compare across thresholds or time periods |

### Example

```
Bar 1: duration=1 hour,  pnl=+$100  → weight 1/61
Bar 2: duration=60 hours, pnl=+$50  → weight 60/61

Simple bar_sharpe: treats both equally (WRONG)
Time-weighted:     Bar 2 contributes 60x more (CORRECT)
```

---

## Canonical Implementation: Time-Weighted Sharpe

### Formula

```
weights[i] = duration_days[i] / total_days
weighted_mean = sum(bar_pnl * weights)
weighted_var = sum(weights * (bar_pnl - weighted_mean)^2)
weighted_std = sqrt(weighted_var)
sharpe = (weighted_mean / weighted_std) * sqrt(252)
```

### Reference Implementation

**Source file**: `examples/research/exp066e_tau_precision.py:355-407`

```python
def compute_time_weighted_sharpe(
    bar_pnl: np.ndarray,
    duration_us: np.ndarray,
    annualize: bool = True,
) -> tuple[float, float, float]:
    """
    Time-weighted Sharpe for range bars.

    Args:
        bar_pnl: Per-bar P&L (can be returns or dollar amounts)
        duration_us: Bar duration in MICROSECONDS
        annualize: If True, multiply by sqrt(252)

    Returns:
        (sharpe, weighted_std, total_days)
    """
    MICROSECONDS_PER_DAY = 86400 * 1e6

    # Convert to days for interpretability
    duration_days = duration_us / MICROSECONDS_PER_DAY
    total_days = float(np.sum(duration_days))

    # Weights sum to 1.0
    weights = duration_days / total_days

    # Weighted statistics
    weighted_mean = float(np.sum(bar_pnl * weights))
    weighted_var = float(np.sum(weights * (bar_pnl - weighted_mean) ** 2))
    weighted_std = np.sqrt(weighted_var)

    # Sharpe ratio
    if weighted_std < 1e-10:
        return 0.0, 0.0, total_days

    sharpe = weighted_mean / weighted_std
    if annualize:
        sharpe *= np.sqrt(252)

    return float(sharpe), float(weighted_std), total_days
```

---

## Data Pipeline Requirements

### Preserve `duration_us` Through Pipeline

The duration column MUST be preserved from data fetch through evaluation:

```python
# 1. Fetch range bars (duration_us is part of schema)
df = fetch_range_bars(symbol, threshold)
# df columns: open, high, low, close, volume, duration_us, timestamp

# 2. Create sequences - preserve duration_us
X, y, timestamps, duration_us = create_sequences_with_duration(
    df, features, target, seq_len
)

# 3. Evaluate with duration
metrics = evaluate_fold_range_bar(
    predictions=preds,
    actuals=actuals,
    duration_us=duration_us,  # REQUIRED
)
```

### Common Mistake: Losing Duration

```python
# WRONG: Duration lost during sequence creation
X, y = create_sequences(df[features], df[target], seq_len)
# Now we can't compute time-weighted Sharpe!

# CORRECT: Return duration alongside other outputs
X, y, timestamps, duration_us = create_sequences_with_duration(...)
```

---

## When to Use Time-Weighted vs Simple Sharpe

| Data Type              | Use Time-Weighted                  | Use Simple |
| ---------------------- | ---------------------------------- | ---------- |
| Range bars             | **YES**                            | NO         |
| Time bars (1m, 5m, 1h) | Optional (all same duration)       | YES        |
| Tick data              | **YES** (variable inter-tick time) | NO         |
| Daily bars             | Optional                           | YES        |

**Rule**: If bar duration varies by more than 2x, use time-weighted.

---

## Integration with DSR

When computing Deflated Sharpe Ratio (DSR) for range bar experiments:

```python
from scipy import stats
import numpy as np

def compute_dsr_range_bar(
    sharpe_tw: float,             # Use time-weighted, NOT simple bar_sharpe
    n_obs: int,                   # Number of bars
    n_trials: int,                # Number of strategies tested
    skew: float = 0.0,
    kurt: float = 3.0,
) -> float:
    """DSR using time-weighted Sharpe (sharpe_tw)."""
    # Mertens SE adjustment
    se = np.sqrt(
        (1 + 0.5 * sharpe_tw**2
         - skew * sharpe_tw
         + ((kurt - 3) / 4) * sharpe_tw**2) / n_obs
    )

    # Gumbel expected max under null
    gamma = 0.5772156649
    exp_max = se * (
        (1 - gamma) * stats.norm.ppf(1 - 1/n_trials) +
        gamma * stats.norm.ppf(1 - 1/(n_trials * np.e))
    )

    # DSR
    return float(stats.norm.cdf((sharpe_tw - exp_max) / se))
```

---

## NDJSON Logging Schema

When logging range bar experiment results, include both metrics:

```json
{
  "phase": "fold_complete",
  "fold_id": 3,
  "metrics": {
    "bar_sharpe": 0.234,
    "sharpe_tw": 0.187,
    "sharpe_tw_details": {
      "weighted_mean": 0.00012,
      "weighted_std": 0.0034,
      "total_days": 45.2,
      "n_bars": 4521
    }
  }
}
```

**Naming Convention**:

- `bar_sharpe` - Simple (WRONG for range bars, kept for backward compatibility)
- `sharpe_tw` - Time-weighted (CORRECT, use for all analysis)
- Summary metrics: `mean_sharpe_tw`, `median_sharpe_tw`, `std_sharpe_tw`

**Important**: Always log BOTH for comparison, but use `sharpe_tw` for:

- DSR computation
- Cross-fold comparison
- Final performance assessment

---

## Validation Checklist

Before trusting range bar Sharpe values:

- [ ] `duration_us` preserved through entire data pipeline
- [ ] `compute_time_weighted_sharpe()` used (not simple division)
- [ ] Both `bar_sharpe` and `sharpe_tw` logged for comparison
- [ ] DSR computed on `sharpe_tw` values (NOT bar_sharpe)
- [ ] Summary metrics use `_tw` suffix: `mean_sharpe_tw`, `median_sharpe_tw`
- [ ] Metrics include `sharpe_tw_details` for auditability

---

## Anti-Patterns

### 1. Using Simple Bar Sharpe for Range Bars

```python
# WRONG: Treats all bars equally
sharpe = np.mean(bar_pnl) / np.std(bar_pnl) * np.sqrt(252)

# CORRECT: Weight by duration
sharpe, _, _ = compute_time_weighted_sharpe(bar_pnl, duration_us)
```

### 2. Forgetting Annualization Factor

```python
# WRONG: No annualization
sharpe = weighted_mean / weighted_std

# CORRECT: Annualize for comparability
sharpe = (weighted_mean / weighted_std) * np.sqrt(252)
```

### 3. Using Annualized Return / Annualized Vol

```python
# WRONG: Double-counting time
annual_return = weighted_mean * 252
annual_vol = weighted_std * np.sqrt(252)
sharpe = annual_return / annual_vol  # Wrong!

# CORRECT: Sharpe annualizes via sqrt(252) only
sharpe = (weighted_mean / weighted_std) * np.sqrt(252)
```

### 4. Comparing Across Different Thresholds Without Time-Weighting

```python
# WRONG: threshold=50 has more bars, inflates significance
sharpe_50 = simple_sharpe(bars_threshold_50)
sharpe_100 = simple_sharpe(bars_threshold_100)

# CORRECT: Time-weighted normalizes for duration
sharpe_50 = time_weighted_sharpe(bars_50, duration_50)
sharpe_100 = time_weighted_sharpe(bars_100, duration_100)
```

---

## References

- [Alpha Forge exp066e_tau_precision.py](examples/research/exp066e_tau_precision.py) - Canonical implementation
- [Alpha Forge research CLAUDE.md](examples/research/CLAUDE.md) - Project standards
- [Risk Metrics for Non-Uniform Time Series](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2587178) - Academic foundation
- [Bailey & Lopez de Prado DSR](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551) - Multiple testing correction

---

## Changelog

| Date       | Change                                                | Impact                    |
| ---------- | ----------------------------------------------------- | ------------------------- |
| 2026-01-21 | Initial: Documented time-weighted Sharpe as canonical | All range bar experiments |
