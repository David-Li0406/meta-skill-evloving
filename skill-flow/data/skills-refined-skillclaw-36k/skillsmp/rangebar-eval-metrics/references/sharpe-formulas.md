# Sharpe Ratio Formulas for Range Bars

## Why Standard Sharpe Fails for Range Bars

Standard Sharpe annualization assumes:

1. **IID returns**: Each observation is independent, identically distributed
2. **Fixed intervals**: Observations occur at regular time intervals
3. **sqrt(N) scaling**: Volatility scales with sqrt(time)

**Range bars violate ALL three assumptions.**

## CRITICAL: Rangebar v9 Duration Unit Mismatch

> **WARNING (2026-01-22)**: The `rangebar` crate v9 returns `duration_us` in **MILLISECONDS**
> despite the column name suggesting microseconds. This causes ~1000x Sharpe inflation.

**Detection heuristic**: If 95th percentile of `duration_us` < 1e5, values are likely milliseconds.

```python
import numpy as np

def validate_duration_units(duration_us: np.ndarray) -> str:
    """Detect if duration_us is actually in milliseconds (rangebar v9 bug)."""
    p95 = np.percentile(duration_us, 95)

    if p95 < 1e5:  # < 0.1 seconds if microseconds → likely milliseconds
        return "milliseconds"  # Need MS_TO_US = 1000 conversion
    elif p95 < 1e8:  # < 100 seconds if microseconds → plausible
        return "microseconds"  # No conversion needed
    else:
        return "unknown"  # Investigate further

# Fix: Convert milliseconds to microseconds before compute_time_weighted_sharpe
MS_TO_US = 1000
duration_us_fixed = duration_us * MS_TO_US  # If validate returns "milliseconds"
```

**Impact without fix**: Sharpe inflated by ~170x (total_days 1000x smaller → annualization factor ~31x larger).

## Canonical Approach 1: Time-Weighted Sharpe Ratio (TWSR)

**Preferred for bar-level evaluation.** Directly handles variable-duration bars without aggregation.

```python
import numpy as np

def compute_time_weighted_sharpe(
    bar_pnl: np.ndarray,
    duration_us: np.ndarray,
) -> tuple[float, float, float]:
    """
    Time-Weighted Sharpe Ratio (TWSR) for variable-duration bars.

    FORMULA:
      TWSR = (simple_mean(r) / time_weighted_std(r)) × √(365.25 / T)

    Where:
      - simple_mean(r) = sum(r_i) / N (preserves total P&L sign)
      - time_weighted_std(r) = √(sum(w_i × (r_i - simple_mean)²))
      - w_i = d_i / T (time weights, sum to 1)
      - T = total observation time in days
      - 365.25 = days per year (24/7 crypto markets)

    The annualization factor √(365.25 / T) projects the observed Sharpe to
    annual units based on actual observation time T. Derived from Wiener
    process property where variance scales linearly with time.

    Returns:
        (sharpe, weighted_std, total_days)
    """
    if len(bar_pnl) == 0 or len(duration_us) == 0:
        return 0.0, 0.0, 0.0

    bar_pnl = np.asarray(bar_pnl, dtype=np.float64)
    duration_us = np.asarray(duration_us, dtype=np.float64)

    MICROSECONDS_PER_DAY = 86400.0 * 1e6
    duration_days = duration_us / MICROSECONDS_PER_DAY
    total_days = float(np.sum(duration_days))

    if total_days < 1e-15:
        return 0.0, 0.0, 0.0

    weights = duration_days / total_days
    simple_mean = float(np.mean(bar_pnl))
    weighted_var = float(np.sum(weights * (bar_pnl - simple_mean) ** 2))

    if weighted_var < 1e-20:
        return 0.0, 0.0, total_days

    weighted_std = np.sqrt(weighted_var)
    raw_sharpe = simple_mean / weighted_std

    # Time-scaled annualization: project to 365.25 days (24/7 crypto)
    annualization_factor = np.sqrt(365.25 / total_days)
    sharpe = raw_sharpe * annualization_factor

    return float(sharpe), float(weighted_std), total_days
```

**Key Properties**:

- Positive total P&L always produces positive Sharpe (sign preservation)
- Long losing bars get penalized via higher weighted volatility
- Microsecond precision for duration calculations
- Proper time-based annualization (no arbitrary 252)

**Reference**: `~/.claude/docs/GLOSSARY.md` (TWSR canonical definition)

## Canonical Approach 2: Daily Aggregation

```python
import pandas as pd
import numpy as np

def _group_by_day(pnl: np.ndarray, timestamps: np.ndarray) -> np.ndarray:
    """Aggregate bar-level PnL to daily PnL.

    This restores IID-like properties by:
    1. Normalizing variable bar counts per day
    2. Creating fixed-interval (daily) observations
    3. Reducing autocorrelation from bar clustering
    """
    df = pd.DataFrame({
        "pnl": pnl,
        "ts": pd.to_datetime(timestamps, utc=True)
    })
    df["date"] = df["ts"].dt.date
    return df.groupby("date")["pnl"].sum().values


def weekly_sharpe(pnl: np.ndarray, timestamps: np.ndarray, days_per_week: int = 7) -> float:
    """Daily-aggregated Sharpe scaled to weekly.

    Args:
        pnl: Bar-level PnL array
        timestamps: Bar close timestamps (UTC)
        days_per_week: 7 for crypto, 5 for equities

    Returns:
        Weekly Sharpe ratio
    """
    daily_pnl = _group_by_day(pnl, timestamps)

    if len(daily_pnl) < 2:
        return 0.0

    std = np.std(daily_pnl, ddof=1)
    if std < 1e-10:
        return 0.0

    daily_sharpe = np.mean(daily_pnl) / std
    return daily_sharpe * np.sqrt(days_per_week)
```

## Annualization Factors

```yaml
annualization:
  # TWSR (Time-Weighted Sharpe Ratio) - for bar-level range bar data
  twsr_crypto:
    formula: "sqrt(365.25 / T)" # T = observation period in days
    rationale: "Projects to annual based on ACTUAL observation time"
    use_when: "Bar-level evaluation with duration_us available"

  # Daily Aggregation - for daily-aggregated data
  crypto_24_7:
    daily_to_weekly: 2.6458 # sqrt(7)
    daily_to_annual: 19.1049 # sqrt(365)
    rationale: "Crypto markets trade 24/7, 365 days/year"

  equity:
    daily_to_weekly: 2.2361 # sqrt(5)
    daily_to_annual: 15.8745 # sqrt(252)
    rationale: "Equity markets trade ~252 days/year"

  # CRITICAL: Never mix these!
  anti_patterns:
    - "Using sqrt(252) for crypto TWSR"
    - "Using sqrt(365) for equities"
    - "Using sqrt(N) on bar-level data directly (use TWSR instead)"
    - "Using sqrt(T * 252) - WRONG formula (should be sqrt(365.25 / T))"
```

## Mertens (2002) Standard Error

Non-normality adjustment for Sharpe SE:

```python
from scipy import stats

def sharpe_standard_error(
    sharpe: float,
    n_observations: int,
    skewness: float,
    kurtosis: float  # Pearson form: normal = 3
) -> float:
    """Sharpe SE with Mertens (2002) non-normality adjustment.

    SE(SR) = sqrt((1 + 0.5×SR² - γ₃×SR + (γ₄-3)/4×SR²) / (n-1))

    Where:
        γ₃ = skewness
        γ₄ = kurtosis (Pearson, normal = 3)
    """
    if n_observations < 2:
        return float("nan")

    # Excess kurtosis term
    excess_kurt = kurtosis - 3.0

    variance_term = (
        1.0
        + 0.5 * sharpe**2
        - skewness * sharpe
        + (excess_kurt / 4.0) * sharpe**2
    )

    if variance_term < 0:
        return float("nan")

    return float(np.sqrt(variance_term / (n_observations - 1)))
```

## PSR (Probabilistic Sharpe Ratio)

```python
from scipy.stats import norm

def probabilistic_sharpe_ratio(
    sharpe: float,
    standard_error: float,
    benchmark: float = 0.0
) -> float:
    """P(true Sharpe > benchmark).

    Bailey & López de Prado (2012):
    PSR = Φ((SR - benchmark) / SE(SR))

    Returns:
        Probability in [0, 1]. >0.95 indicates significance.
    """
    if standard_error <= 1e-10:
        return float("nan")

    z_score = (sharpe - benchmark) / standard_error
    return float(norm.cdf(z_score))
```

## DSR (Deflated Sharpe Ratio)

Corrects for multiple testing:

```python
def deflated_sharpe_ratio(
    sharpe: float,
    standard_error: float,
    n_trials: int
) -> float:
    """Sharpe corrected for multiple testing.

    Bailey & López de Prado (2014):
    Uses Gumbel approximation for expected maximum Sharpe.

    Args:
        sharpe: Observed Sharpe (or max across trials)
        standard_error: SE of Sharpe
        n_trials: Number of independent strategies tested

    Returns:
        Probability in [0, 1]. >0.50 indicates robust performance.
    """
    if n_trials < 1 or standard_error <= 1e-10:
        return float("nan")

    gamma = 0.5772156649  # Euler-Mascheroni constant

    if n_trials == 1:
        sr_expected = 0.0
    else:
        q1 = norm.ppf(1.0 - 1.0 / n_trials)
        q2 = norm.ppf(1.0 - 1.0 / (n_trials * np.e))
        sr_expected = standard_error * ((1 - gamma) * q1 + gamma * q2)

    z_score = (sharpe - sr_expected) / standard_error
    return float(norm.cdf(z_score))
```

## MinTRL (Minimum Track Record Length)

```python
def minimum_track_record_length(
    sharpe: float,
    benchmark: float,
    skewness: float,
    kurtosis: float,  # Pearson form
    alpha: float = 0.05
) -> float:
    """Observations needed for statistical significance.

    Uses Mertens (2002) variance formula.

    CRITICAL: Use (kurtosis - 3) for excess kurtosis!
    """
    if sharpe <= benchmark:
        return float("nan")

    z_crit = norm.ppf(1 - alpha)
    excess_kurt = kurtosis - 3.0

    # Mertens variance term
    variance_term = (
        1.0
        + 0.5 * sharpe**2
        - skewness * sharpe
        + (excess_kurt / 4.0) * sharpe**2
    )

    sr_diff = sharpe - benchmark
    mintrl = variance_term * (z_crit / sr_diff) ** 2

    return float(max(1.0, mintrl))
```

## Academic References

```bibtex
@article{bailey2014deflated,
  title={The Deflated Sharpe Ratio: Correcting for Selection Bias,
         Backtest Overfitting and Non-Normality},
  author={Bailey, David H and L{\'o}pez de Prado, Marcos},
  journal={The Journal of Portfolio Management},
  year={2014}
}

@article{mertens2002sharpe,
  title={The Sharpe Ratio and the Information Ratio},
  author={Mertens, Elmar},
  journal={Financial Analysts Journal},
  year={2002}
}

@article{lo2002statistics,
  title={The Statistics of Sharpe Ratios},
  author={Lo, Andrew W},
  journal={Financial Analysts Journal},
  volume={58},
  number={4},
  pages={36--52},
  year={2002}
}
```
