# OOS Metrics Specification Reference

Detailed specification for metrics computed on held-out test data.

## Metric Hierarchy

```
                    AWFES: OOS Metrics Hierarchy

 -----------     +-----------+     +-------------+      -----------
| Primary   | -> | Secondary | --> | Statistical | --> | Decision  |
 -----------     +-----------+     +-------------+      -----------
```

<details>
<summary>graph-easy source</summary>

```
graph { label: "AWFES: OOS Metrics Hierarchy"; flow: east; }

[ Primary ] { shape: rounded; }
[ Secondary ]
[ Statistical ]
[ Decision ] { shape: rounded; }

[ Primary ] -> [ Secondary ]
[ Secondary ] -> [ Statistical ]
[ Statistical ] -> [ Decision ]
```

</details>

## Tier 1: Primary Metrics (MANDATORY)

These metrics MUST be computed for every fold's test data.

### 1.1 Time-Weighted Sharpe Ratio (sharpe_tw)

```python
def sharpe_tw(
    pnl: np.ndarray,
    duration_us: np.ndarray,
    annualize: bool = True,
) -> float:
    """Time-weighted Sharpe for range bars.

    CRITICAL: Range bars have variable duration - simple bar_sharpe
    violates i.i.d. assumption. Use time-weighted Sharpe instead.

    See range-bar-metrics.md for full derivation.

    Formula:
    weights = duration_days / total_days
    weighted_mean = sum(pnl * weights)
    weighted_var = sum(weights * (pnl - weighted_mean)^2)
    sharpe_tw = (weighted_mean / sqrt(weighted_var)) * sqrt(252)
    """
    MICROSECONDS_PER_DAY = 86400 * 1e6
    duration_days = duration_us / MICROSECONDS_PER_DAY
    total_days = np.sum(duration_days)
    weights = duration_days / total_days

    weighted_mean = np.sum(pnl * weights)
    weighted_var = np.sum(weights * (pnl - weighted_mean) ** 2)
    weighted_std = np.sqrt(weighted_var)

    if weighted_std < 1e-10:
        return 0.0

    sharpe = weighted_mean / weighted_std
    if annualize:
        sharpe *= np.sqrt(252)

    return sharpe
```

**Threshold**: `sharpe_tw > 0` for positive signal

**Note**: For time bars with uniform duration (e.g., 1-minute bars), you can use
simple daily aggregation as a fallback. But for range bars, always use `sharpe_tw`.

### 1.2 Hit Rate (Directional Accuracy)

```python
def hit_rate(predictions: np.ndarray, actuals: np.ndarray) -> float:
    """Fraction of correct directional predictions.

    Formula:
    hit_rate = n_correct_sign / n_total

    Interpretation:
    - hit_rate > 0.50: Better than random
    - hit_rate > 0.52: Statistically meaningful for large N
    - hit_rate > 0.55: Strong directional signal
    """
    correct = np.sign(predictions) == np.sign(actuals)
    return np.mean(correct)
```

**Threshold**: `hit_rate > 0.50` (better than chance)

### 1.3 Cumulative PnL

```python
def cumulative_pnl(predictions: np.ndarray, actuals: np.ndarray) -> float:
    """Total profit/loss from predictions.

    Formula:
    cumulative_pnl = sum(pred_i * actual_i)

    This assumes:
    - predictions are signed magnitudes (positive = long, negative = short)
    - actuals are returns
    - Position sizing proportional to prediction confidence
    """
    return np.sum(predictions * actuals)
```

**Threshold**: `cumulative_pnl > 0` (profitable)

### 1.4 Positive Sharpe Folds (Cross-Fold)

```python
def positive_sharpe_folds(fold_sharpes_tw: list[float]) -> float:
    """Fraction of folds with positive time-weighted Sharpe.

    Formula:
    positive_sharpe_folds = n_folds(sharpe_tw > 0) / n_folds

    Interpretation:
    - > 0.50: Majority of folds profitable
    - > 0.55: Consistent signal
    - > 0.65: Strong consistency
    """
    return np.mean([s > 0 for s in fold_sharpes_tw])
```

**Threshold**: `positive_sharpe_folds > 0.55`

### 1.5 WFE Test (Final Transfer)

```python
def wfe_test(test_sharpe: float, validation_sharpe: float) -> float | None:
    """Walk-Forward Efficiency from validation to test.

    Formula:
    wfe_test = test_sharpe / validation_sharpe

    This measures final transfer quality:
    - validation → test should maintain performance
    - Large drop indicates validation was still overfitting
    """
    if abs(validation_sharpe) < 0.1:
        return None
    return test_sharpe / validation_sharpe
```

**Threshold**: `wfe_test > 0.30`

## Tier 2: Risk Metrics

### 2.1 Maximum Drawdown

```python
def max_drawdown(pnl: np.ndarray) -> float:
    """Largest peak-to-trough decline.

    Formula:
    max_dd = max(peak - equity) / peak

    Interpretation:
    - < 0.10: Excellent risk control
    - 0.10-0.20: Acceptable
    - 0.20-0.30: High risk
    - > 0.30: REJECT
    """
    equity = np.cumsum(pnl)
    running_max = np.maximum.accumulate(equity)

    # Avoid division by zero
    running_max = np.maximum(running_max, 1e-10)

    drawdowns = (running_max - equity) / running_max
    return np.max(drawdowns) if len(drawdowns) > 0 else 0.0
```

**Threshold**: `max_drawdown < 0.30`

### 2.2 Profit Factor

```python
def profit_factor(pnl: np.ndarray) -> float:
    """Ratio of gross profits to gross losses.

    Formula:
    profit_factor = sum(positive_pnl) / abs(sum(negative_pnl))

    Interpretation:
    - > 1.0: Profitable
    - > 1.5: Good
    - > 2.0: Excellent
    - inf: No losing trades (suspicious)
    """
    gross_profit = np.sum(pnl[pnl > 0])
    gross_loss = abs(np.sum(pnl[pnl < 0]))

    if gross_loss < 1e-10:
        return float("inf") if gross_profit > 0 else 1.0

    return gross_profit / gross_loss
```

**Threshold**: `profit_factor > 1.0`

### 2.3 Conditional Value-at-Risk (CVaR)

```python
def cvar(pnl: np.ndarray, alpha: float = 0.10) -> float:
    """Expected shortfall: mean of worst alpha% returns.

    Formula:
    CVaR_α = mean(worst α% of returns)

    Interpretation:
    - CVaR_10 > -0.05: Acceptable tail risk
    - CVaR_10 > -0.02: Good tail risk
    - CVaR_10 > 0: No tail losses (rare)
    """
    sorted_pnl = np.sort(pnl)
    cutoff = max(1, int(len(sorted_pnl) * alpha))
    return np.mean(sorted_pnl[:cutoff])
```

**Threshold**: `cvar_10pct > -0.05`

### 2.4 Calmar Ratio

```python
def calmar_ratio(
    pnl: np.ndarray,
    timestamps: np.ndarray,
    annualization: float = 365,  # Days per year
) -> float:
    """Annual return divided by maximum drawdown.

    Formula:
    calmar = annualized_return / max_drawdown

    Better than Sharpe for strategies with large drawdowns.
    """
    # Compute annualized return
    n_days = (timestamps[-1] - timestamps[0]).days
    if n_days < 1:
        return 0.0

    total_return = np.sum(pnl)
    annual_return = total_return * (annualization / n_days)

    # Get max drawdown
    max_dd = max_drawdown(pnl)
    if max_dd < 1e-10:
        return float("inf") if annual_return > 0 else 0.0

    return annual_return / max_dd
```

**Threshold**: `calmar_ratio > 0.5`

## Tier 3: Statistical Validation

### 3.1 Probabilistic Sharpe Ratio (PSR)

```python
from scipy.stats import norm

def psr(
    sharpe: float,
    n_observations: int,
    benchmark: float = 0.0,
) -> float:
    """Probability that true Sharpe exceeds benchmark.

    Formula:
    PSR = Φ[(SR - SR*) / SE(SR)]
    SE(SR) = 1 / sqrt(n)

    Reference: Bailey & López de Prado (2012)
    """
    if n_observations < 2:
        return 0.5

    sharpe_se = 1.0 / np.sqrt(n_observations)
    z_score = (sharpe - benchmark) / sharpe_se

    return norm.cdf(z_score)
```

**Threshold**: `psr > 0.85`

### 3.2 Deflated Sharpe Ratio (DSR)

```python
def dsr(
    sharpe: float,
    n_trials: int,
    sharpe_se: float = 0.3,
) -> float:
    """Sharpe adjusted for multiple testing.

    Formula:
    DSR = SR - E[max(SR_null)]
    E[max] ≈ sqrt(2 * ln(N)) - (ln(ln(N)) + ln(4π)) / (2 * sqrt(2 * ln(N)))

    Reference: Bailey & López de Prado (2014)
    """
    from math import sqrt, log, pi

    if n_trials < 2:
        return sharpe

    # Expected maximum Sharpe under null
    e_max = sqrt(2 * log(n_trials))
    e_max -= (log(log(n_trials)) + log(4 * pi)) / (2 * sqrt(2 * log(n_trials)))
    e_max *= sharpe_se

    return max(0, sharpe - e_max)
```

**Threshold**: `dsr > 0.50`

### 3.3 Binomial Sign Test

```python
from scipy.stats import binom_test

def binomial_pvalue(
    n_positive: int,
    n_total: int,
    null_prob: float = 0.5,
) -> float:
    """P-value for sign test.

    Tests: H0: P(positive) = 0.5 vs H1: P(positive) > 0.5

    Interpretation:
    - p < 0.05: Significant at 95% confidence
    - p < 0.01: Significant at 99% confidence
    """
    return binom_test(n_positive, n_total, null_prob, alternative="greater")
```

**Threshold**: `binomial_pvalue < 0.05`

### 3.4 HAC-Adjusted T-Test

```python
from statsmodels.stats.sandwich_covariance import cov_hac

def hac_ttest_pvalue(returns: np.ndarray) -> float:
    """T-test with Heteroskedasticity and Autocorrelation Consistent SE.

    Uses Newey-West estimator for standard errors.

    Necessary for range bars due to:
    - Variable duration → heteroskedasticity
    - Clustering → autocorrelation
    """
    import statsmodels.api as sm

    n = len(returns)
    if n < 10:
        return 1.0

    # OLS with constant
    X = np.ones((n, 1))
    model = sm.OLS(returns, X).fit(cov_type="HAC", cov_kwds={"maxlags": 5})

    return model.pvalues[0]
```

**Threshold**: `hac_ttest_pvalue < 0.05`

## Aggregation Functions

### Fold-Level Aggregation

```python
def aggregate_fold_metrics(fold_results: list[dict]) -> dict[str, float]:
    """Aggregate metrics across all folds.

    Uses median for robustness to outlier folds.
    Note: Uses sharpe_tw (time-weighted) for range bar data.
    """
    sharpes = [r["sharpe_tw"] for r in fold_results]
    hit_rates = [r["hit_rate"] for r in fold_results]
    pnls = [r["cumulative_pnl"] for r in fold_results]

    # Positive counts for binomial test
    n_positive_sharpe = sum(1 for s in sharpes if s > 0)
    n_positive_pnl = sum(1 for p in pnls if p > 0)

    return {
        # Central tendency (time-weighted Sharpe)
        "mean_sharpe_tw": np.mean(sharpes),
        "median_sharpe_tw": np.median(sharpes),
        "std_sharpe_tw": np.std(sharpes),
        "mean_hit_rate": np.mean(hit_rates),

        # Consistency
        "positive_sharpe_folds": n_positive_sharpe / len(sharpes),
        "positive_pnl_rate": n_positive_pnl / len(pnls),

        # Totals
        "total_pnl": sum(pnls),
        "n_folds": len(fold_results),

        # Statistical
        "binomial_sharpe_pvalue": binom_test(
            n_positive_sharpe, len(sharpes), 0.5, alternative="greater"
        ),
    }
```

## Threshold Summary

| Metric                | Threshold | Type        | Rationale            |
| --------------------- | --------- | ----------- | -------------------- |
| sharpe_tw             | > 0       | Primary     | Positive signal      |
| hit_rate              | > 0.50    | Primary     | Better than random   |
| cumulative_pnl        | > 0       | Primary     | Profitable           |
| positive_sharpe_folds | > 0.55    | Primary     | Consistent           |
| wfe_test              | > 0.30    | Primary     | Transfer quality     |
| max_drawdown          | < 0.30    | Risk        | Capital preservation |
| profit_factor         | > 1.0     | Risk        | Win/loss ratio       |
| cvar_10pct            | > -0.05   | Risk        | Tail risk            |
| calmar_ratio          | > 0.5     | Risk        | Risk-adjusted        |
| psr                   | > 0.85    | Statistical | Significance         |
| dsr                   | > 0.50    | Statistical | Multiple testing     |
| binomial_pvalue       | < 0.05    | Statistical | Sign test            |
| hac_ttest_pvalue      | < 0.05    | Statistical | Autocorrelation      |

**Note**: For range bars, `sharpe_tw` is the time-weighted Sharpe ratio.
See [range-bar-metrics.md](./range-bar-metrics.md) for canonical implementation.

## Decision Framework

```
                      AWFES: Metric Decision Flow

 ---------------   pass   +-----------+   pass   +-------------+      --------
| Tier 1 Check  | ------> | Tier 2    | -------> | Tier 3      | --> | ACCEPT |
 ---------------          | Risk Gate |          | Statistical |      --------
        |                 +-----------+          +-------------+
        | fail                  | fail                 | fail
        v                       v                      v
   ----------              ----------             ----------
  | REJECT  |             | REJECT  |            | WARNING |
   ----------              ----------             ----------
```

<details>
<summary>graph-easy source</summary>

```
graph { label: "AWFES: Metric Decision Flow"; flow: east; }

[ Tier 1 Check ] { shape: rounded; }
[ Tier 2 Risk Gate ]
[ Tier 3 Statistical ]
[ ACCEPT ] { shape: rounded; }
[ REJECT T1 ] { shape: rounded; }
[ REJECT T2 ] { shape: rounded; }
[ WARNING ] { shape: rounded; }

[ Tier 1 Check ] -- pass --> [ Tier 2 Risk Gate ]
[ Tier 2 Risk Gate ] -- pass --> [ Tier 3 Statistical ]
[ Tier 3 Statistical ] -- pass --> [ ACCEPT ]

[ Tier 1 Check ] -- fail --> [ REJECT T1 ]
[ Tier 2 Risk Gate ] -- fail --> [ REJECT T2 ]
[ Tier 3 Statistical ] -- fail --> [ WARNING ]
```

</details>
