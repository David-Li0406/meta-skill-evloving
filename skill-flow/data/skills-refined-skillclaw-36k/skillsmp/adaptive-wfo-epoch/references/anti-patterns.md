# Anti-Patterns: Adaptive Walk-Forward Epoch Selection

Common failures and how to avoid them.

## 1. Peak Picking (Severity: HIGH)

### Symptom

Best epoch is always at the boundary of the search space.

```
Epoch candidates: [400, 800, 1000, 2000]
Selected epochs across folds: [2000, 2000, 400, 2000, 400, 2000, ...]
```

### Root Cause

Search space doesn't contain the true optimum. The optimal epoch is outside the tested range.

### Detection

```python
def detect_peak_picking(selection_history: list[int], epoch_configs: list[int]) -> bool:
    """Returns True if >50% selections are at boundaries."""
    min_epoch, max_epoch = min(epoch_configs), max(epoch_configs)
    boundary_count = sum(1 for e in selection_history if e in [min_epoch, max_epoch])
    return boundary_count / len(selection_history) > 0.5
```

### Fix

1. **Expand range**: If selecting 2000 often, add 3000, 4000
2. **Check for plateau**: If WFE is flat at boundary, true optimum may be beyond
3. **Add intermediate points**: If jumping between 400 and 2000, test 600, 1200

```python
# WRONG: Narrow range
EPOCH_CONFIGS = [400, 800]

# BETTER: Use AWFESConfig with appropriate bounds
from adaptive_wfo_epoch import AWFESConfig

config = AWFESConfig.from_search_space(
    min_epoch=200,
    max_epoch=3200,
    granularity=5,  # Log-spaced: [200, 400, 800, 1600, 3200]
)
```

## 2. Insufficient Folds (Severity: HIGH)

### Symptom

Effective sample size (N_eff) is too low for statistical significance.

```
Folds: 10
Epochs: 4
N_eff = 10 × (1/√4) × 0.7 ≈ 3.5  # Too low!
```

### Root Cause

Not enough folds to distinguish signal from noise in epoch selection.

### Detection

```python
def check_effective_sample_size(
    n_folds: int,
    n_epochs: int,
    autocorr: float = 0.3,
    min_n_eff: int = 10,
) -> bool:
    """Returns True if N_eff is sufficient."""
    import math
    selection_factor = 1 / math.sqrt(n_epochs)
    corr_factor = (1 - autocorr) / (1 + autocorr)
    n_eff = n_folds * selection_factor * corr_factor
    return n_eff >= min_n_eff
```

### Fix

1. **Increase folds**: Target N_eff ≥ 30 for reliable inference
2. **Extend data span**: More historical data = more folds
3. **Reduce epoch candidates**: Fewer choices = higher N_eff

```python
# WRONG: 10 folds with 4 epochs → N_eff ≈ 3.5
N_FOLDS = 10
config = AWFESConfig.from_search_space(min_epoch=400, max_epoch=2000, granularity=4)

# BETTER: 50 folds with 3 epochs → N_eff ≈ 20
N_FOLDS = 50
config = AWFESConfig.from_search_space(min_epoch=400, max_epoch=1600, granularity=3)
# Fewer epochs + more folds = higher effective sample size
```

## 3. Ignoring Temporal Autocorrelation (Severity: HIGH)

### Symptom

Consecutive folds have correlated performance, making each fold non-independent.

```
Fold 0: WFE=0.65, epoch=800
Fold 1: WFE=0.64, epoch=800  # Correlated!
Fold 2: WFE=0.66, epoch=800  # Still correlated!
```

### Root Cause

Overlapping training data between consecutive folds, or no embargo period.

### Detection

```python
def compute_fold_autocorrelation(wfe_series: list[float], lag: int = 1) -> float:
    """Compute autocorrelation of WFE across folds."""
    import numpy as np
    if len(wfe_series) < lag + 2:
        return float("nan")
    return float(np.corrcoef(wfe_series[:-lag], wfe_series[lag:])[0, 1])

# WARNING if autocorr > 0.3
```

### Fix

1. **Add embargo period**: Gap between train and test periods
2. **Reduce fold overlap**: Increase step size between folds
3. **Use purged cross-validation**: Remove samples that could leak

```python
# WRONG: Adjacent folds with no gap
fold_0: train=[0:1000], test=[1000:1100]
fold_1: train=[100:1100], test=[1100:1200]  # 90% overlap!

# BETTER: Embargo + reduced overlap
fold_0: train=[0:1000], embargo=[1000:1050], test=[1050:1150]
fold_1: train=[500:1500], embargo=[1500:1550], test=[1550:1650]  # 50% overlap
```

## 4. Overfitting to In-Sample (Severity: HIGH)

### Symptom

In-sample Sharpe is much higher than out-of-sample, even with optimal epoch.

```
IS_Sharpe: 3.5
OOS_Sharpe: 0.8
WFE: 0.23  # Severe overfitting!
```

### Root Cause

Model is memorizing training data patterns that don't generalize.

### Detection

```python
def detect_overfitting(is_sharpe: float, oos_sharpe: float) -> str:
    """Classify overfitting severity.

    Labels aligned with SKILL.md classify_wfe() (see Guardrails G1):
    - EXCELLENT (≥0.70): Excellent transfer, low overfitting
    - ACCEPTABLE (0.50-0.70): Acceptable transfer (alias: GOOD)
    - INVESTIGATE (0.30-0.50): Moderate transfer, investigate
    - REJECT (<0.30): Severe overfitting, reject (alias: SEVERE)

    Note: ACCEPTABLE/GOOD and REJECT/SEVERE are synonyms.
    SKILL.md uses ACCEPTABLE/REJECT; some older code uses GOOD/SEVERE.
    """
    if is_sharpe <= 0:
        return "NO_SIGNAL"

    wfe = oos_sharpe / is_sharpe

    if wfe >= 0.7:
        return "EXCELLENT"
    elif wfe >= 0.5:
        return "ACCEPTABLE"  # Aligned with SKILL.md (was: GOOD)
    elif wfe >= 0.3:
        return "INVESTIGATE"
    else:
        return "REJECT"  # Aligned with SKILL.md (was: SEVERE)
```

### Fix

1. **Reduce epochs**: Less training time = less memorization
2. **Add regularization**: Dropout, weight decay, early stopping
3. **Simplify model**: Fewer parameters = less capacity to overfit
4. **Increase training data**: More diverse patterns

```python
# WRONG: High capacity, long training
EPOCHS = 2000
HIDDEN_SIZE = 128
DROPOUT = 0.1

# BETTER: Lower capacity, regularized
EPOCHS = 400
HIDDEN_SIZE = 48
DROPOUT = 0.3
WEIGHT_DECAY = 0.01
```

## 5. Using sqrt(252) for Crypto (Severity: MEDIUM)

### Symptom

Annualized Sharpe ratios are inflated by ~18%.

```
# Crypto trades 24/7, but using equity assumption
daily_sharpe = 0.1
annual_sharpe = 0.1 * sqrt(252)  # WRONG: 1.59
annual_sharpe = 0.1 * sqrt(365)  # CORRECT: 1.91

# The error: sqrt(365)/sqrt(252) = 1.20 = 20% inflation
```

### Root Cause

Using equity market convention (252 trading days) for crypto (365 days).

### Detection

```python
def check_annualization_factor(market: str, factor: float) -> bool:
    """Validate annualization factor for market type."""
    CORRECT_FACTORS = {
        "crypto_daily": 365,
        "crypto_weekly": 7,  # 7 days per week
        "equity_daily": 252,
        "equity_weekly": 5,  # 5 trading days per week
    }
    return factor == CORRECT_FACTORS.get(market, factor)
```

### Fix

```python
# WRONG for crypto (daily to weekly conversion)
sharpe_tw = daily_sharpe * np.sqrt(5)  # Equity assumption

# CORRECT for crypto
sharpe_tw = daily_sharpe * np.sqrt(7)  # Crypto 24/7

# EXCEPTION: Session-filtered crypto (London-NY hours only)
# Use sqrt(5) because you're only trading 5 days
```

**Note**: For range bars, use time-weighted Sharpe (`sharpe_tw`) with
`compute_time_weighted_sharpe()`. See [range-bar-metrics.md](./range-bar-metrics.md).

## 6. Single Epoch Selection (No Uncertainty) (Severity: MEDIUM)

### Symptom

Reporting a single "optimal" epoch without confidence interval.

```
"Optimal epoch: 800"  # WRONG: No uncertainty quantification
```

### Root Cause

Treating epoch selection as deterministic when it's subject to sampling variation.

### Detection

Look for reports that:

- Give single epoch value without CI
- Don't report WFE variance across folds
- Don't show epoch distribution

### Fix

Report uncertainty in epoch selection:

```python
def report_epoch_selection_with_uncertainty(
    selection_history: list[dict],
) -> dict:
    """Report epoch selection with uncertainty quantification."""
    epochs = [s["epoch"] for s in selection_history]
    wfes = [s["wfe"] for s in selection_history if s["wfe"] is not None]

    return {
        "selected_epoch": max(set(epochs), key=epochs.count),  # Mode
        "epoch_mean": np.mean(epochs),
        "epoch_std": np.std(epochs),
        "wfe_mean": np.mean(wfes),
        "wfe_ci_95": np.percentile(wfes, [2.5, 97.5]),
        "epoch_distribution": {e: epochs.count(e) for e in set(epochs)},
    }
```

**Good reporting**:

```
Optimal epoch: 800 (selected 45% of folds)
Epoch distribution: {400: 20%, 800: 45%, 1000: 25%, 2000: 10%}
WFE at 800: 0.52 [0.38, 0.66] (95% CI)
```

## 7. Expanding Window for Range Bar Training (CRITICAL)

### Symptom

Training window grows with each fold instead of sliding forward.

```
EXPANDING WINDOW (WRONG for range bars):
Fold 1:  [====TRAIN====][TEST]                    (3,000 bars)
Fold 5:  [========TRAIN========][TEST]            (15,000 bars)
Fold 10: [============TRAIN============][TEST]    (30,000 bars)
Fold 20: [==================TRAIN==================][TEST]  (60,000 bars)

FIXED WINDOW (CORRECT):
Fold 1:  [====TRAIN====][TEST]                    (3,000 bars)
Fold 5:       [====TRAIN====][TEST]               (3,000 bars)
Fold 10:           [====TRAIN====][TEST]          (3,000 bars)
Fold 20:                     [====TRAIN====][TEST] (3,000 bars)
```

### Root Cause

Misapplying time-series CV conventions to range bar data. Range bars have non-uniform time spacing, making expanding windows especially problematic.

### Why This Is Critical for Range Bars

**Multi-agent analysis (2026-01-19) identified 7 compounding issues:**

| Issue                    | Impact                                                    | Severity |
| ------------------------ | --------------------------------------------------------- | -------- |
| **Fold non-equivalence** | WFE computed on 3K vs 60K bars incomparable               | CRITICAL |
| **Regime dilution**      | Early folds miss crashes, later folds average out signals | CRITICAL |
| **Feature drift**        | MinMaxScaler sees 20x different data volumes              | HIGH     |
| **Epoch mismatch**       | Fixed 400 epochs underfit late folds, overfit early       | HIGH     |
| **Risk understatement**  | Max drawdown understated 20-40% (path-length effect)      | HIGH     |
| **Embargo decay**        | 100-bar embargo = 3.3% of fold 1, 0.17% of fold 20        | MEDIUM   |
| **Memory/runtime**       | 6x memory growth, 3x runtime increase                     | MEDIUM   |

### Detection

```python
def detect_expanding_window(folds: list[Fold]) -> bool:
    """Returns True if expanding window detected (ANTI-PATTERN)."""
    train_sizes = [f.train_end_idx - f.train_start_idx for f in folds]

    # Fixed window: all sizes equal
    if len(set(train_sizes)) == 1:
        return False  # OK

    # Expanding window: sizes increase monotonically
    is_expanding = all(
        train_sizes[i] <= train_sizes[i+1]
        for i in range(len(train_sizes)-1)
    )

    return is_expanding


def validate_fixed_window(folds: list[Fold]) -> None:
    """Raise error if expanding window detected."""
    if detect_expanding_window(folds):
        raise ValueError(
            "CRITICAL: Expanding window detected for range bar training. "
            "This anti-pattern causes fold non-equivalence, regime dilution, "
            "and biased risk metrics. Use fixed sliding window instead."
        )
```

### Fix

**Always use fixed-size sliding window for range bar ML training:**

```python
# WRONG: Expanding window (train_start always 0)
def generate_expanding_folds(total_bars, n_folds):
    step = total_bars // n_folds
    for i in range(n_folds):
        train_end = (i + 1) * step
        yield Fold(train_start=0, train_end=train_end, ...)  # Growing!

# CORRECT: Fixed sliding window
def generate_fixed_folds(total_bars, train_size, test_size, step_size):
    for i in range(n_folds):
        train_start = i * step_size
        train_end = train_start + train_size  # Constant size
        yield Fold(train_start=train_start, train_end=train_end, ...)
```

### Statistical Justification

| Property                | Expanding Window               | Fixed Window         |
| ----------------------- | ------------------------------ | -------------------- |
| IS variance             | Heterogeneous (decreasing)     | Homogeneous          |
| WFE comparability       | Apples to oranges              | Apples to apples     |
| Regime recency          | Diluted over time              | Constant recency     |
| Risk metric reliability | Systematically biased          | Unbiased             |
| Bayesian smoothing      | Requires heteroskedastic model | Standard model works |

### Exceptions

**None for range bar ML training.**

The only valid expanding window use case is cumulative learning where every historical instance matters (e.g., rare event detection). Range bar prediction requires **recency-weighted regime adaptation**, which expanding windows prevent.

### Enforcement

Add runtime validation to prevent accidental use:

```python
# At experiment start
validate_fixed_window(folds)

# In fold generation
assert all(
    folds[i].train_start_idx > folds[i-1].train_start_idx
    for i in range(1, len(folds))
), "train_start must advance (not anchored at 0)"
```

---

## 8. Meta-Overfitting (Overfitting the Epoch Search) (Severity: HIGH)

### Symptom

Epoch selection itself overfits to the search space.

```
Fold 0: epoch=800 (WFE=0.55)
Fold 1: epoch=2000 (WFE=0.53)
Fold 2: epoch=400 (WFE=0.56)
...
# High variance in selection, but aggregate looks good

# Then in production:
Production WFE: 0.35  # Much worse than backtest!
```

### Root Cause

With 4 epochs × 31 folds = 124 selection decisions, some "lucky" selections inflate aggregate WFE.

### Detection

```python
def detect_meta_overfitting(
    selection_history: list[dict],
    epoch_configs: list[int],
) -> dict:
    """Detect signs of meta-overfitting."""
    epochs = [s["epoch"] for s in selection_history]

    # High variance is suspicious
    epoch_std = np.std(epochs)
    epoch_mean = np.mean(epochs)
    cv = epoch_std / epoch_mean  # Coefficient of variation

    # Uniform distribution suggests random selection
    from scipy.stats import chisquare
    observed = [epochs.count(e) for e in epoch_configs]
    expected = [len(epochs) / len(epoch_configs)] * len(epoch_configs)
    chi2, p_value = chisquare(observed, expected)

    return {
        "epoch_cv": cv,
        "uniformity_p_value": p_value,
        "is_suspicious": cv > 0.5 or p_value > 0.5,
        "diagnosis": (
            "HIGH_VARIANCE" if cv > 0.5 else
            "NEAR_UNIFORM" if p_value > 0.5 else
            "OK"
        ),
    }
```

### Fix

1. **Limit epoch candidates**: 3-4 options maximum
2. **Use stability penalty**: Penalize frequent changes
3. **Hold out final folds**: Reserve 20% for meta-validation
4. **Apply DSR correction**: Account for 124 trials in significance test

```python
# WRONG: Too many epoch options (10 options = meta-overfitting risk)
config = AWFESConfig.from_search_space(min_epoch=100, max_epoch=1000, granularity=10)

# BETTER: Limited options with adaptive stability
config = AWFESConfig.from_search_space(min_epoch=400, max_epoch=1600, granularity=3)
# Use AdaptiveStabilityPenalty which derives threshold from WFE variance
from adaptive_wfo_epoch import AdaptiveStabilityPenalty
stability = AdaptiveStabilityPenalty()  # Adapts to observed WFE noise
```

## Summary Checklist

Before deploying adaptive epoch selection:

- [ ] **Expanding window**: Using fixed sliding window (NOT expanding) for range bars?
- [ ] **Peak picking**: Are selections clustered at boundaries? (Expand search bounds if yes)
- [ ] **Sample size**: Is N_eff ≥ 30? (Use fewer epochs or more folds)
- [ ] **Autocorrelation**: Is fold autocorrelation < 0.3?
- [ ] **Overfitting**: Is WFE > 0.50 across folds? (Guidelines, not hard thresholds)
- [ ] **Annualization**: Using `AWFESConfig.get_annualization_factor()` for correct market/time_unit?
- [ ] **Uncertainty**: Reporting confidence intervals via `BayesianEpochSmoother.get_confidence_interval()`?
- [ ] **Meta-overfitting**: Epoch CV < 0.5? Not near-uniform? (Use `AdaptiveStabilityPenalty`)
- [ ] **IS_Sharpe threshold**: Using `compute_is_sharpe_threshold(n_samples)` instead of fixed 1.0?

If any check fails, investigate before production deployment.

**CRITICAL**: The expanding window check is a **hard gate** for range bar training. All other checks are warnings that require investigation.

**Principled Configuration**: Use `AWFESConfig.from_search_space(min_epoch, max_epoch, granularity)` to derive all parameters from search bounds. See [SKILL.md](../SKILL.md#principled-configuration-framework) for details.
