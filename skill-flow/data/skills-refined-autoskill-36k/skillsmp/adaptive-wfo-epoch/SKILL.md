---
name: adaptive-wfo-epoch
description: >
  Adaptive epoch selection for Walk-Forward Optimization using efficient frontier analysis.
  Per-fold epoch sweeps with WFE-based selection and carry-forward priors.
  TRIGGERS - epoch selection, WFO epoch, walk-forward epoch, training epochs WFO,
  efficient frontier epochs, overfitting epochs, epoch sweep, BiLSTM epochs,
  WFE optimization, adaptive hyperparameter, Pardo WFE, epoch carry-forward.
allowed-tools: Read, Grep, Glob, Bash
---

# Adaptive Walk-Forward Epoch Selection (AWFES)

Machine-readable reference for adaptive epoch selection within Walk-Forward Optimization (WFO). Optimizes training epochs per-fold using Walk-Forward Efficiency (WFE) as the objective.

## Quick Start

```python
from adaptive_wfo_epoch import AWFESConfig, compute_efficient_frontier

# Generate epoch candidates from search bounds and granularity
config = AWFESConfig.from_search_space(
    min_epoch=100,
    max_epoch=2000,
    granularity=5,  # Number of frontier points
)
# config.epoch_configs → [100, 211, 447, 945, 2000] (log-spaced)

# Per-fold epoch sweep
for fold in wfo_folds:
    epoch_metrics = []
    for epoch in config.epoch_configs:
        is_sharpe, oos_sharpe = train_and_evaluate(fold, epochs=epoch)
        wfe = config.compute_wfe(is_sharpe, oos_sharpe, n_samples=len(fold.train))
        epoch_metrics.append({"epoch": epoch, "wfe": wfe, "is_sharpe": is_sharpe})

    # Select from efficient frontier
    selected_epoch = compute_efficient_frontier(epoch_metrics)

    # Carry forward to next fold as prior
    prior_epoch = selected_epoch
```

## Methodology Overview

### What This Is

Per-fold adaptive epoch selection where:

1. Train models across a range of epochs (e.g., 400, 800, 1000, 2000)
2. Compute WFE = OOS_Sharpe / IS_Sharpe for each epoch count
3. Find the "efficient frontier" - epochs maximizing WFE vs training cost
4. Select optimal epoch from frontier for OOS evaluation
5. Carry forward as prior for next fold

### What This Is NOT

- **NOT early stopping**: Early stopping monitors validation loss continuously; this evaluates discrete candidates post-hoc
- **NOT Bayesian optimization**: No surrogate model; direct evaluation of all candidates
- **NOT nested cross-validation**: Uses temporal WFO, not shuffled splits

## Academic Foundations

| Concept                     | Citation                       | Key Insight                                       |
| --------------------------- | ------------------------------ | ------------------------------------------------- |
| Walk-Forward Efficiency     | Pardo (1992, 2008)             | WFE = OOS_Return / IS_Return as robustness metric |
| Deflated Sharpe Ratio       | Bailey & López de Prado (2014) | Adjusts for multiple testing                      |
| Pareto-Optimal HP Selection | Bischl et al. (2023)           | Multi-objective hyperparameter optimization       |
| Warm-Starting               | Nomura & Ono (2021)            | Transfer knowledge between optimization runs      |

See [references/academic-foundations.md](./references/academic-foundations.md) for full literature review.

## Core Formula: Walk-Forward Efficiency

```python
def compute_wfe(
    is_sharpe: float,
    oos_sharpe: float,
    n_samples: int | None = None,
) -> float | None:
    """Walk-Forward Efficiency - measures performance transfer.

    WFE = OOS_Sharpe / IS_Sharpe

    Interpretation (guidelines, not hard thresholds):
    - WFE ≥ 0.70: Excellent transfer (low overfitting)
    - WFE 0.50-0.70: Good transfer
    - WFE 0.30-0.50: Moderate transfer (investigate)
    - WFE < 0.30: Severe overfitting (likely reject)

    The IS_Sharpe minimum is derived from signal-to-noise ratio,
    not a fixed magic number. See compute_is_sharpe_threshold().

    Reference: Pardo (2008) "The Evaluation and Optimization of Trading Strategies"
    """
    # Data-driven threshold: IS_Sharpe must exceed 2σ noise floor
    min_is_sharpe = compute_is_sharpe_threshold(n_samples) if n_samples else 0.1

    if abs(is_sharpe) < min_is_sharpe:
        return None
    return oos_sharpe / is_sharpe
```

## Principled Configuration Framework

All parameters in AWFES are derived from first principles or data characteristics, not arbitrary magic numbers.

### AWFESConfig: Unified Configuration

```python
from dataclasses import dataclass, field
from typing import Literal
import numpy as np

@dataclass
class AWFESConfig:
    """AWFES configuration with principled parameter derivation.

    No magic numbers - all values derived from search space or data.
    """
    # Search space bounds (user-specified)
    min_epoch: int
    max_epoch: int
    granularity: int  # Number of frontier points

    # Derived automatically
    epoch_configs: list[int] = field(init=False)
    prior_variance: float = field(init=False)
    observation_variance: float = field(init=False)

    # Market context for annualization
    # crypto_session_filtered: Use when data is filtered to London-NY weekday hours
    market_type: Literal["crypto_24_7", "crypto_session_filtered", "equity", "forex"] = "crypto_24_7"
    time_unit: Literal["bar", "daily", "weekly"] = "weekly"

    def __post_init__(self):
        # Generate epoch configs with log spacing (optimal for frontier discovery)
        self.epoch_configs = self._generate_epoch_configs()

        # Derive Bayesian variances from search space
        self.prior_variance, self.observation_variance = self._derive_variances()

    def _generate_epoch_configs(self) -> list[int]:
        """Generate epoch candidates with log spacing.

        Log spacing is optimal for efficient frontier because:
        1. Early epochs: small changes matter more (underfit → fit transition)
        2. Late epochs: diminishing returns (already near convergence)
        3. Uniform coverage of the WFE vs cost trade-off space

        Formula: epoch_i = min × (max/min)^(i/(n-1))
        """
        if self.granularity < 2:
            return [self.min_epoch]

        log_min = np.log(self.min_epoch)
        log_max = np.log(self.max_epoch)
        log_epochs = np.linspace(log_min, log_max, self.granularity)

        return sorted(set(int(round(np.exp(e))) for e in log_epochs))

    def _derive_variances(self) -> tuple[float, float]:
        """Derive Bayesian variances from search space.

        Principle: Prior should span the search space with ~95% coverage.

        For Normal distribution: 95% CI = mean ± 1.96σ
        If we want 95% of prior mass in [min_epoch, max_epoch]:
            range = max - min = 2 × 1.96 × σ = 3.92σ
            σ = range / 3.92
            σ² = (range / 3.92)²

        Observation variance: Set to achieve reasonable learning rate.
        Rule: observation_variance ≈ prior_variance / 4
        This means each observation updates the posterior meaningfully
        but doesn't dominate the prior immediately.
        """
        epoch_range = self.max_epoch - self.min_epoch
        prior_std = epoch_range / 3.92  # 95% CI spans search space
        prior_variance = prior_std ** 2

        # Observation variance: 1/4 of prior for balanced learning
        # This gives ~0.2 weight to each new observation initially
        observation_variance = prior_variance / 4

        return prior_variance, observation_variance

    @classmethod
    def from_search_space(
        cls,
        min_epoch: int,
        max_epoch: int,
        granularity: int = 5,
        market_type: str = "crypto_24_7",
    ) -> "AWFESConfig":
        """Create config from search space bounds."""
        return cls(
            min_epoch=min_epoch,
            max_epoch=max_epoch,
            granularity=granularity,
            market_type=market_type,
        )

    def compute_wfe(
        self,
        is_sharpe: float,
        oos_sharpe: float,
        n_samples: int | None = None,
    ) -> float | None:
        """Compute WFE with data-driven IS_Sharpe threshold."""
        min_is = compute_is_sharpe_threshold(n_samples) if n_samples else 0.1
        if abs(is_sharpe) < min_is:
            return None
        return oos_sharpe / is_sharpe

    def get_annualization_factor(self) -> float:
        """Get annualization factor to scale Sharpe from time_unit to ANNUAL.

        IMPORTANT: This returns sqrt(periods_per_year) for scaling to ANNUAL Sharpe.
        For daily-to-weekly scaling, use get_daily_to_weekly_factor() instead.

        Principled derivation:
        - Sharpe scales with √(periods per year)
        - Crypto 24/7: 365 days/year, 52.14 weeks/year
        - Crypto session-filtered: 252 days/year (like equity)
        - Equity: 252 trading days/year, ~52 weeks/year
        - Forex: ~252 days/year (varies by pair)
        """
        PERIODS_PER_YEAR = {
            ("crypto_24_7", "daily"): 365,
            ("crypto_24_7", "weekly"): 52.14,
            ("crypto_24_7", "bar"): None,  # Cannot annualize bars directly
            ("crypto_session_filtered", "daily"): 252,  # London-NY weekdays only
            ("crypto_session_filtered", "weekly"): 52,
            ("equity", "daily"): 252,
            ("equity", "weekly"): 52,
            ("forex", "daily"): 252,
        }

        key = (self.market_type, self.time_unit)
        periods = PERIODS_PER_YEAR.get(key)

        if periods is None:
            raise ValueError(
                f"Cannot annualize {self.time_unit} for {self.market_type}. "
                "Use daily or weekly aggregation first."
            )

        return np.sqrt(periods)

    def get_daily_to_weekly_factor(self) -> float:
        """Get factor to scale DAILY Sharpe to WEEKLY Sharpe.

        This is different from get_annualization_factor()!
        - Daily → Weekly: sqrt(days_per_week)
        - Daily → Annual: sqrt(days_per_year)  (use get_annualization_factor)

        Market-specific:
        - Crypto 24/7: sqrt(7) = 2.65 (7 trading days/week)
        - Crypto session-filtered: sqrt(5) = 2.24 (weekdays only)
        - Equity: sqrt(5) = 2.24 (5 trading days/week)
        """
        DAYS_PER_WEEK = {
            "crypto_24_7": 7,
            "crypto_session_filtered": 5,  # London-NY weekdays only
            "equity": 5,
            "forex": 5,
        }

        days = DAYS_PER_WEEK.get(self.market_type)
        if days is None:
            raise ValueError(f"Unknown market type: {self.market_type}")

        return np.sqrt(days)
```

### IS_Sharpe Threshold: Signal-to-Noise Derivation

```python
def compute_is_sharpe_threshold(n_samples: int | None = None) -> float:
    """Compute minimum IS_Sharpe threshold from signal-to-noise ratio.

    Principle: IS_Sharpe must be statistically distinguishable from zero.

    Under null hypothesis (no skill), Sharpe ~ N(0, 1/√n).
    To reject null at α=0.05 (one-sided), need Sharpe > 1.645/√n.

    For practical use, we use 2σ threshold (≈97.7% confidence):
        threshold = 2.0 / √n

    This adapts to sample size:
    - n=100: threshold ≈ 0.20
    - n=400: threshold ≈ 0.10
    - n=1600: threshold ≈ 0.05

    Fallback for unknown n: 0.1 (assumes n≈400, typical fold size)

    Rationale for 0.1 fallback:
    - 2/√400 = 0.1, so 0.1 assumes ~400 samples per fold
    - This is conservative: 400 samples is typical for weekly folds
    - If actual n is smaller, threshold is looser (accepts more noise)
    - If actual n is larger, threshold is tighter (fine, we're conservative)
    - The 0.1 value also corresponds to "not statistically distinguishable
      from zero at reasonable sample sizes" - a natural floor for Sharpe SE
    """
    if n_samples is None or n_samples < 10:
        # Conservative fallback: 0.1 assumes ~400 samples (typical fold size)
        # Derivation: 2/√400 = 0.1; see rationale above
        return 0.1

    return 2.0 / np.sqrt(n_samples)
```

## Guardrails (Principled Guidelines)

### G1: WFE Thresholds

The traditional thresholds (0.30, 0.50, 0.70) are **guidelines based on practitioner consensus**, not derived from first principles. They represent:

| Threshold | Meaning     | Statistical Basis                                          |
| --------- | ----------- | ---------------------------------------------------------- |
| **0.30**  | Hard reject | Retaining <30% of IS performance is almost certainly noise |
| **0.50**  | Warning     | At 50%, half the signal is lost - investigate              |
| **0.70**  | Target      | Industry standard for "good" transfer                      |

```python
# These are GUIDELINES, not hard rules
# Adjust based on your domain and risk tolerance
WFE_THRESHOLDS = {
    "hard_reject": 0.30,  # Below this: almost certainly overfitting
    "warning": 0.50,      # Below this: significant signal loss
    "target": 0.70,       # Above this: good generalization
}

def classify_wfe(wfe: float | None) -> str:
    """Classify WFE with principled thresholds."""
    if wfe is None:
        return "INVALID"  # IS_Sharpe below noise floor
    if wfe < WFE_THRESHOLDS["hard_reject"]:
        return "REJECT"
    if wfe < WFE_THRESHOLDS["warning"]:
        return "INVESTIGATE"
    if wfe < WFE_THRESHOLDS["target"]:
        return "ACCEPTABLE"
    return "EXCELLENT"
```

### G2: IS_Sharpe Minimum (Data-Driven)

**OLD (magic number):**

```python
# WRONG: Fixed threshold regardless of sample size
if is_sharpe < 1.0:
    wfe = None
```

**NEW (principled):**

```python
# CORRECT: Threshold adapts to sample size
min_is_sharpe = compute_is_sharpe_threshold(n_samples)
if is_sharpe < min_is_sharpe:
    wfe = None  # Below noise floor for this sample size
```

The threshold derives from the standard error of Sharpe ratio: SE(SR) ≈ 1/√n.

**Note on SE(Sharpe) approximation**: The formula `1/√n` is a first-order approximation valid when SR is small (close to 0). The full Lo (2002) formula is:

```
SE(SR) = √((1 + 0.5×SR²) / n)
```

For high-Sharpe strategies (SR > 1.0), the simplified formula underestimates SE by ~25-50%. Use the full formula when evaluating strategies with SR > 1.0.

### G3: Stability Penalty for Epoch Changes (Adaptive)

The stability penalty prevents hyperparameter churn. Instead of fixed thresholds, use **relative improvement** based on WFE variance:

```python
def compute_stability_threshold(wfe_history: list[float]) -> float:
    """Compute stability threshold from observed WFE variance.

    Principle: Require improvement exceeding noise level.

    If WFE has std=0.15 across folds, random fluctuation could be ±0.15.
    To distinguish signal from noise, require improvement > 1σ of WFE.

    Minimum: 5% (prevent switching on negligible improvements)
    Maximum: 20% (don't be overly conservative)
    """
    if len(wfe_history) < 3:
        return 0.10  # Default until enough history

    wfe_std = np.std(wfe_history)
    threshold = max(0.05, min(0.20, wfe_std))
    return threshold


class AdaptiveStabilityPenalty:
    """Stability penalty that adapts to observed WFE variance."""

    def __init__(self):
        self.wfe_history: list[float] = []
        self.epoch_changes: list[int] = []

    def should_change_epoch(
        self,
        current_wfe: float,
        candidate_wfe: float,
        current_epoch: int,
        candidate_epoch: int,
    ) -> bool:
        """Decide whether to change epochs based on adaptive threshold."""
        self.wfe_history.append(current_wfe)

        if current_epoch == candidate_epoch:
            return False  # Same epoch, no change needed

        threshold = compute_stability_threshold(self.wfe_history)
        improvement = (candidate_wfe - current_wfe) / max(abs(current_wfe), 0.01)

        if improvement > threshold:
            self.epoch_changes.append(len(self.wfe_history))
            return True

        return False  # Improvement not significant
```

### G4: DSR Adjustment for Epoch Search (Principled)

```python
def adjusted_dsr_for_epoch_search(
    sharpe: float,
    n_folds: int,
    n_epochs: int,
    sharpe_se: float | None = None,
    n_samples_per_fold: int | None = None,
) -> float:
    """Deflated Sharpe Ratio accounting for epoch selection multiplicity.

    When selecting from K epochs, the expected maximum Sharpe under null
    is inflated. This adjustment corrects for that selection bias.

    Principled SE estimation:
    - If n_samples provided: SE(Sharpe) ≈ 1/√n
    - Otherwise: estimate from typical fold size

    Reference: Bailey & López de Prado (2014), Gumbel distribution
    """
    from math import sqrt, log, pi

    n_trials = n_folds * n_epochs  # Total selection events

    if n_trials < 2:
        return sharpe  # No multiple testing correction needed

    # Expected maximum under null (Gumbel distribution)
    # E[max(Z_1, ..., Z_n)] ≈ √(2·ln(n)) - (γ + ln(π/2)) / √(2·ln(n))
    # where γ ≈ 0.5772 is Euler-Mascheroni constant
    euler_gamma = 0.5772156649
    sqrt_2_log_n = sqrt(2 * log(n_trials))
    e_max_z = sqrt_2_log_n - (euler_gamma + log(pi / 2)) / sqrt_2_log_n

    # Estimate Sharpe SE if not provided
    if sharpe_se is None:
        if n_samples_per_fold is not None:
            sharpe_se = 1.0 / sqrt(n_samples_per_fold)
        else:
            # Conservative default: assume ~300 samples per fold
            sharpe_se = 1.0 / sqrt(300)

    # Expected maximum Sharpe under null
    e_max_sharpe = e_max_z * sharpe_se

    # Deflated Sharpe
    return max(0, sharpe - e_max_sharpe)
```

**Example**: For 5 epochs × 50 folds = 250 trials with 300 samples/fold:

- `sharpe_se ≈ 0.058`
- `e_max_z ≈ 2.88`
- `e_max_sharpe ≈ 0.17`
- A Sharpe of 1.0 deflates to **0.83** after adjustment.

## WFE Aggregation Methods

**WARNING: Cauchy Distribution Under Null**

Under the null hypothesis (no predictive skill), WFE follows a **Cauchy distribution**, which has:

- No defined mean (undefined expectation)
- No defined variance (infinite)
- Heavy tails (extreme values common)

This makes **arithmetic mean unreliable**. A single extreme WFE can dominate the average. **Always prefer median or pooled methods** for robust WFE aggregation. See [references/mathematical-formulation.md](./references/mathematical-formulation.md) for the proof: `WFE | H0 ~ Cauchy(0, sqrt(T_IS/T_OOS))`.

### Method 1: Pooled WFE (Recommended for precision-weighted)

```python
def pooled_wfe(fold_results: list[dict]) -> float:
    """Weights each fold by its sample size (precision).

    Formula: Σ(T_OOS × SR_OOS) / Σ(T_IS × SR_IS)

    Advantage: More stable than arithmetic mean, handles varying fold sizes.
    Use when: Fold sizes vary significantly.
    """
    numerator = sum(r["n_oos"] * r["oos_sharpe"] for r in fold_results)
    denominator = sum(r["n_is"] * r["is_sharpe"] for r in fold_results)

    if denominator < 1e-10:
        return float("nan")
    return numerator / denominator
```

### Method 2: Median WFE (Recommended for robustness)

```python
def median_wfe(fold_results: list[dict]) -> float:
    """Robust to outliers, standard in robust statistics.

    Advantage: Single extreme fold doesn't dominate.
    Use when: Suspected outlier folds (regime changes, data issues).
    """
    wfes = [r["wfe"] for r in fold_results if r["wfe"] is not None]
    return float(np.median(wfes)) if wfes else float("nan")
```

### Method 3: Weighted Arithmetic Mean

```python
def weighted_mean_wfe(fold_results: list[dict]) -> float:
    """Weights by inverse variance (efficiency weighting).

    Formula: Σ(w_i × WFE_i) / Σ(w_i)
    where w_i = 1 / Var(WFE_i) ≈ n_oos × n_is / (n_oos + n_is)

    Advantage: Optimal when combining estimates of different precision.
    Use when: All folds have similar characteristics.
    """
    weighted_sum = 0.0
    weight_total = 0.0

    for r in fold_results:
        if r["wfe"] is None:
            continue
        weight = r["n_oos"] * r["n_is"] / (r["n_oos"] + r["n_is"] + 1e-10)
        weighted_sum += weight * r["wfe"]
        weight_total += weight

    return weighted_sum / weight_total if weight_total > 0 else float("nan")
```

### Aggregation Selection Guide

| Scenario            | Recommended Method | Rationale               |
| ------------------- | ------------------ | ----------------------- |
| Variable fold sizes | Pooled WFE         | Weights by precision    |
| Suspected outliers  | Median WFE         | Robust to extremes      |
| Homogeneous folds   | Weighted mean      | Optimal efficiency      |
| Reporting           | **All three**      | Cross-check consistency |

## Efficient Frontier Algorithm

```python
def compute_efficient_frontier(
    epoch_metrics: list[dict],
    wfe_weight: float = 1.0,
    time_weight: float = 0.1,
) -> tuple[list[int], int]:
    """
    Find Pareto-optimal epochs and select best.

    An epoch is on the frontier if no other epoch dominates it
    (better WFE AND lower training time).

    Args:
        epoch_metrics: List of {epoch, wfe, training_time_sec}
        wfe_weight: Weight for WFE in selection (higher = prefer generalization)
        time_weight: Weight for training time (higher = prefer speed)

    Returns:
        (frontier_epochs, selected_epoch)
    """
    import numpy as np

    # Filter valid metrics
    valid = [(m["epoch"], m["wfe"], m.get("training_time_sec", m["epoch"]))
             for m in epoch_metrics
             if m["wfe"] is not None and np.isfinite(m["wfe"])]

    if not valid:
        # Fallback: return epoch with best OOS Sharpe
        best_oos = max(epoch_metrics, key=lambda m: m.get("oos_sharpe", 0))
        return ([best_oos["epoch"]], best_oos["epoch"])

    # Pareto dominance check
    frontier = []
    for i, (epoch_i, wfe_i, time_i) in enumerate(valid):
        dominated = False
        for j, (epoch_j, wfe_j, time_j) in enumerate(valid):
            if i == j:
                continue
            # j dominates i if: better/equal WFE AND lower/equal time (strict in at least one)
            if (wfe_j >= wfe_i and time_j <= time_i and
                (wfe_j > wfe_i or time_j < time_i)):
                dominated = True
                break
        if not dominated:
            frontier.append((epoch_i, wfe_i, time_i))

    frontier_epochs = [e for e, _, _ in frontier]

    if len(frontier) == 1:
        return (frontier_epochs, frontier[0][0])

    # Weighted score selection
    wfes = np.array([w for _, w, _ in frontier])
    times = np.array([t for _, _, t in frontier])

    wfe_norm = (wfes - wfes.min()) / (wfes.max() - wfes.min() + 1e-10)
    time_norm = (times.max() - times) / (times.max() - times.min() + 1e-10)

    scores = wfe_weight * wfe_norm + time_weight * time_norm
    best_idx = np.argmax(scores)

    return (frontier_epochs, frontier[best_idx][0])
```

## Carry-Forward Mechanism

```python
class AdaptiveEpochSelector:
    """Maintains epoch selection state across WFO folds with adaptive stability."""

    def __init__(self, epoch_configs: list[int]):
        self.epoch_configs = epoch_configs
        self.selection_history: list[dict] = []
        self.last_selected: int | None = None
        self.stability = AdaptiveStabilityPenalty()  # Use adaptive, not fixed

    def select_epoch(self, epoch_metrics: list[dict]) -> int:
        """Select epoch with adaptive stability penalty for changes."""
        frontier_epochs, candidate = compute_efficient_frontier(epoch_metrics)

        # Apply adaptive stability penalty if changing epochs
        if self.last_selected is not None and candidate != self.last_selected:
            candidate_wfe = next(
                m["wfe"] for m in epoch_metrics if m["epoch"] == candidate
            )
            last_wfe = next(
                (m["wfe"] for m in epoch_metrics if m["epoch"] == self.last_selected),
                0.0
            )

            # Use adaptive threshold derived from WFE variance
            if not self.stability.should_change_epoch(
                last_wfe, candidate_wfe, self.last_selected, candidate
            ):
                candidate = self.last_selected

        # Record and return
        self.selection_history.append({
            "epoch": candidate,
            "frontier": frontier_epochs,
            "changed": candidate != self.last_selected,
        })
        self.last_selected = candidate
        return candidate
```

## Anti-Patterns

| Anti-Pattern                      | Symptom                             | Fix                               | Severity |
| --------------------------------- | ----------------------------------- | --------------------------------- | -------- |
| **Expanding window (range bars)** | Train size grows per fold           | Use fixed sliding window          | CRITICAL |
| **Peak picking**                  | Best epoch always at sweep boundary | Expand range, check for plateau   | HIGH     |
| **Insufficient folds**            | effective_n < 30                    | Increase folds or data span       | HIGH     |
| **Ignoring temporal autocorr**    | Folds correlated                    | Use purged CV, gap between folds  | HIGH     |
| **Overfitting to IS**             | IS >> OOS Sharpe                    | Reduce epochs, add regularization | HIGH     |
| **sqrt(252) for crypto**          | Inflated Sharpe                     | Use sqrt(365) or sqrt(7) weekly   | MEDIUM   |
| **Single epoch selection**        | No uncertainty quantification       | Report confidence interval        | MEDIUM   |
| **Meta-overfitting**              | Epoch selection itself overfits     | Limit to 3-4 candidates max       | HIGH     |

**CRITICAL**: Never use expanding window for range bar ML training. Expanding windows create fold non-equivalence, regime dilution, and systematically bias risk metrics. See [references/anti-patterns.md](./references/anti-patterns.md) for the full analysis (Section 7).

## Decision Tree

See [references/epoch-selection-decision-tree.md](./references/epoch-selection-decision-tree.md) for the full practitioner decision tree.

```
Start
  │
  ├─ IS_Sharpe > compute_is_sharpe_threshold(n)? ──NO──> Mark WFE invalid, use fallback
  │         │                                            (threshold = 2/√n, adapts to sample size)
  │        YES
  │         │
  ├─ Compute WFE for each epoch
  │         │
  ├─ Any WFE > 0.30? ──NO──> REJECT all epochs (severe overfit)
  │         │                (guideline, not hard threshold)
  │        YES
  │         │
  ├─ Compute efficient frontier
  │         │
  ├─ Apply AdaptiveStabilityPenalty
  │         │ (threshold derived from WFE variance)
  └─> Return selected epoch
```

## Integration with rangebar-eval-metrics

This skill extends [rangebar-eval-metrics](../rangebar-eval-metrics/SKILL.md):

| Metric Source         | Used For                                 | Reference                                                                                |
| --------------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------- |
| `sharpe_tw`           | WFE numerator (OOS) and denominator (IS) | [range-bar-metrics.md](./references/range-bar-metrics.md)                                |
| `n_bars`              | Sample size for aggregation weights      | [metrics-schema.md](../rangebar-eval-metrics/references/metrics-schema.md)               |
| `psr`, `dsr`          | Final acceptance criteria                | [sharpe-formulas.md](../rangebar-eval-metrics/references/sharpe-formulas.md)             |
| `prediction_autocorr` | Validate model isn't collapsed           | [ml-prediction-quality.md](../rangebar-eval-metrics/references/ml-prediction-quality.md) |
| `is_collapsed`        | Model health check                       | [ml-prediction-quality.md](../rangebar-eval-metrics/references/ml-prediction-quality.md) |
| Extended risk metrics | Deep risk analysis (optional)            | [risk-metrics.md](../rangebar-eval-metrics/references/risk-metrics.md)                   |

### Recommended Workflow

1. **Compute base metrics** using `rangebar-eval-metrics:compute_metrics.py`
2. **Feed to AWFES** for epoch selection with `sharpe_tw` as primary signal
3. **Validate** with `psr > 0.85` and `dsr > 0.50` before deployment
4. **Monitor** `is_collapsed` and `prediction_autocorr` for model health

---

## OOS Application Phase

### Overview

After epoch selection via efficient frontier, apply the selected epochs to held-out test data for final OOS performance metrics. This phase produces "live trading" results that simulate deployment.

### Nested WFO Structure

AWFES uses **Nested WFO** with three data splits per fold:

```
                    AWFES: Nested WFO Data Split (per fold)

#############     +----------+     +---------+     +----------+     #==========#
# Train 60% # --> | Gap 6% A | --> | Val 20% | --> | Gap 6% B | --> H Test 20% H
#############     +----------+     +---------+     +----------+     #==========#
```

<details>
<summary>graph-easy source</summary>

```
graph { label: "AWFES: Nested WFO Data Split (per fold)"; flow: east; }

[ Train 60% ] { border: bold; }
[ Gap 6% A ]
[ Val 20% ]
[ Gap 6% B ]
[ Test 20% ] { border: double; }

[ Train 60% ] -> [ Gap 6% A ]
[ Gap 6% A ] -> [ Val 20% ]
[ Val 20% ] -> [ Gap 6% B ]
[ Gap 6% B ] -> [ Test 20% ]
```

</details>

### Per-Fold Workflow

```
                  AWFES: Per-Fold Workflow

                   -----------------------
                  |      Fold i Data      |
                   -----------------------
                    |
                    v
                  +-----------------------+
                  | Split: Train/Val/Test |
                  +-----------------------+
                    |
                    v
                  +-----------------------+
                  | Epoch Sweep on Train  |
                  +-----------------------+
                    |
                    v
                  +-----------------------+
                  |  Compute WFE on Val   |
                  +-----------------------+
                    |
                    | val optimal
                    v
                  #=======================#
                  H    Bayesian Update    H
                  #=======================#
                    |
                    | smoothed epoch
                    v
                  +-----------------------+
                  |   Train Final Model   |
                  +-----------------------+
                    |
                    v
                  #=======================#
                  H   Evaluate on Test    H
                  #=======================#
                    |
                    v
                   -----------------------
                  |    Fold i Metrics     |
                   -----------------------
```

<details>
<summary>graph-easy source</summary>

```
graph { label: "AWFES: Per-Fold Workflow"; flow: south; }

[ Fold i Data ] { shape: rounded; }
[ Split: Train/Val/Test ]
[ Epoch Sweep on Train ]
[ Compute WFE on Val ]
[ Bayesian Update ] { border: double; }
[ Train Final Model ]
[ Evaluate on Test ] { border: double; }
[ Fold i Metrics ] { shape: rounded; }

[ Fold i Data ] -> [ Split: Train/Val/Test ]
[ Split: Train/Val/Test ] -> [ Epoch Sweep on Train ]
[ Epoch Sweep on Train ] -> [ Compute WFE on Val ]
[ Compute WFE on Val ] -- val optimal --> [ Bayesian Update ]
[ Bayesian Update ] -- smoothed epoch --> [ Train Final Model ]
[ Train Final Model ] -> [ Evaluate on Test ]
[ Evaluate on Test ] -> [ Fold i Metrics ]
```

</details>

### Bayesian Carry-Forward Across Folds

```
                                 AWFES: Bayesian Carry-Forward Across Folds

 -------   init   +--------+  posterior   +--------+  posterior   +--------+     +--------+      -----------
| Prior | ------> | Fold 1 | -----------> | Fold 2 | -----------> | Fold 3 | ..> | Fold N | --> | Aggregate |
 -------          +--------+              +--------+              +--------+     +--------+      -----------
```

<details>
<summary>graph-easy source</summary>

```
graph { label: "AWFES: Bayesian Carry-Forward Across Folds"; flow: east; }

[ Prior ] { shape: rounded; }
[ Fold 1 ]
[ Fold 2 ]
[ Fold 3 ]
[ Fold N ]
[ Aggregate ] { shape: rounded; }

[ Prior ] -- init --> [ Fold 1 ]
[ Fold 1 ] -- posterior --> [ Fold 2 ]
[ Fold 2 ] -- posterior --> [ Fold 3 ]
[ Fold 3 ] ..> [ Fold N ]
[ Fold N ] -> [ Aggregate ]
```

</details>

### Bayesian Epoch Selection for OOS

Instead of using the current fold's optimal epoch (look-ahead bias), use **Bayesian-smoothed epoch** from prior folds:

```python
class BayesianEpochSelector:
    """Bayesian updating of epoch selection across folds.

    Also known as: BayesianEpochSmoother (alias in epoch-smoothing.md)

    Variance parameters are DERIVED from search space, not hard-coded.
    See AWFESConfig._derive_variances() for the principled derivation.
    """

    def __init__(
        self,
        epoch_configs: list[int],
        prior_mean: float | None = None,
        prior_variance: float | None = None,
        observation_variance: float | None = None,
    ):
        self.epoch_configs = sorted(epoch_configs)

        # PRINCIPLED DERIVATION: Variances from search space
        # If not provided, derive from epoch range
        epoch_range = max(epoch_configs) - min(epoch_configs)

        # Prior spans search space with 95% coverage
        # 95% CI = mean ± 1.96σ → range = 3.92σ → σ² = (range/3.92)²
        default_prior_var = (epoch_range / 3.92) ** 2

        # Observation variance: 1/4 of prior for balanced learning
        default_obs_var = default_prior_var / 4

        self.posterior_mean = prior_mean or np.mean(epoch_configs)
        self.posterior_variance = prior_variance or default_prior_var
        self.observation_variance = observation_variance or default_obs_var
        self.history: list[dict] = []

    def update(self, observed_optimal_epoch: int, wfe: float) -> int:
        """Update posterior with new fold's optimal epoch.

        Uses precision-weighted Bayesian update:
        posterior_mean = (prior_precision * prior_mean + obs_precision * obs) /
                        (prior_precision + obs_precision)

        Args:
            observed_optimal_epoch: Optimal epoch from current fold's validation
            wfe: Walk-Forward Efficiency (used to weight observation)

        Returns:
            Smoothed epoch selection for TEST evaluation
        """
        # Weight observation by WFE (higher WFE = more reliable signal)
        # Clamp WFE to [0.1, 2.0] to prevent extreme weights:
        #   - Lower bound 0.1: Prevents division issues and ensures minimum weight
        #   - Upper bound 2.0: WFE > 2 is suspicious (OOS > 2× IS suggests:
        #       a) Regime shift favoring OOS (lucky timing, not skill)
        #       b) IS severely overfit (artificially low denominator)
        #       c) Data anomaly or look-ahead bias
        #     Capping at 2.0 treats such observations with skepticism
        wfe_clamped = max(0.1, min(wfe, 2.0))
        effective_variance = self.observation_variance / wfe_clamped

        prior_precision = 1.0 / self.posterior_variance
        obs_precision = 1.0 / effective_variance

        # Bayesian update
        new_precision = prior_precision + obs_precision
        new_mean = (
            prior_precision * self.posterior_mean +
            obs_precision * observed_optimal_epoch
        ) / new_precision

        # Record before updating
        self.history.append({
            "observed_epoch": observed_optimal_epoch,
            "wfe": wfe,
            "prior_mean": self.posterior_mean,
            "posterior_mean": new_mean,
            "selected_epoch": self._snap_to_config(new_mean),
        })

        self.posterior_mean = new_mean
        self.posterior_variance = 1.0 / new_precision

        return self._snap_to_config(new_mean)

    def _snap_to_config(self, continuous_epoch: float) -> int:
        """Snap continuous estimate to nearest valid epoch config."""
        return min(self.epoch_configs, key=lambda e: abs(e - continuous_epoch))

    def get_current_epoch(self) -> int:
        """Get current smoothed epoch without updating."""
        return self._snap_to_config(self.posterior_mean)
```

### Application Workflow

```python
def apply_awfes_to_test(
    folds: list[Fold],
    model_factory: Callable,
    bayesian_selector: BayesianEpochSelector,
) -> list[dict]:
    """Apply AWFES with Bayesian smoothing to test data.

    Workflow per fold:
    1. Split into train/validation/test (60/20/20)
    2. Sweep epochs on train, compute WFE on validation
    3. Update Bayesian posterior with validation-optimal epoch
    4. Train final model at Bayesian-selected epoch on train+validation
    5. Evaluate on TEST (untouched data)
    """
    results = []

    for fold_idx, fold in enumerate(folds):
        # Step 1: Split data
        train, validation, test = fold.split_nested(
            train_pct=0.60,
            validation_pct=0.20,
            test_pct=0.20,
            embargo_pct=0.06,  # 6% gap at each boundary
        )

        # Step 2: Epoch sweep on train → validate on validation
        epoch_metrics = []
        for epoch in bayesian_selector.epoch_configs:
            model = model_factory()
            model.fit(train.X, train.y, epochs=epoch)

            is_sharpe = compute_sharpe(model.predict(train.X), train.y)
            val_sharpe = compute_sharpe(model.predict(validation.X), validation.y)

            # Use data-driven threshold instead of hardcoded 0.1
            is_threshold = compute_is_sharpe_threshold(len(train.X))
            wfe = val_sharpe / is_sharpe if is_sharpe > is_threshold else None

            epoch_metrics.append({
                "epoch": epoch,
                "is_sharpe": is_sharpe,
                "val_sharpe": val_sharpe,
                "wfe": wfe,
            })

        # Step 3: Find validation-optimal and update Bayesian
        val_optimal = max(
            [m for m in epoch_metrics if m["wfe"] is not None],
            key=lambda m: m["wfe"],
            default={"epoch": bayesian_selector.epoch_configs[0], "wfe": 0.3}
        )
        selected_epoch = bayesian_selector.update(
            val_optimal["epoch"],
            val_optimal["wfe"],
        )

        # Step 4: Train final model on train+validation at selected epoch
        combined_X = np.vstack([train.X, validation.X])
        combined_y = np.hstack([train.y, validation.y])
        final_model = model_factory()
        final_model.fit(combined_X, combined_y, epochs=selected_epoch)

        # Step 5: Evaluate on TEST (untouched)
        test_predictions = final_model.predict(test.X)
        test_metrics = compute_oos_metrics(test_predictions, test.y, test.timestamps)

        results.append({
            "fold_idx": fold_idx,
            "validation_optimal_epoch": val_optimal["epoch"],
            "bayesian_selected_epoch": selected_epoch,
            "test_metrics": test_metrics,
            "epoch_metrics": epoch_metrics,
        })

    return results
```

See [references/oos-application.md](./references/oos-application.md) for complete implementation.

---

## Epoch Smoothing Methods

### Why Smooth Epoch Selections?

Raw per-fold epoch selections are noisy due to:

- Limited validation data per fold
- Regime changes between folds
- Stochastic training dynamics

Smoothing reduces variance while preserving signal.

### Method Comparison

| Method                     | Formula                   | Pros                            | Cons                          |
| -------------------------- | ------------------------- | ------------------------------- | ----------------------------- |
| **Bayesian (Recommended)** | Precision-weighted update | Principled, handles uncertainty | More complex                  |
| EMA                        | `α × new + (1-α) × old`   | Simple, responsive              | No uncertainty quantification |
| SMA                        | Mean of last N            | Most stable                     | Slow to adapt                 |
| Median                     | Median of last N          | Robust to outliers              | Loses magnitude info          |

### Bayesian Updating (Primary Method)

```python
def bayesian_epoch_update(
    prior_mean: float,
    prior_variance: float,
    observed_epoch: int,
    observation_variance: float,
    wfe_weight: float = 1.0,
) -> tuple[float, float]:
    """Single Bayesian update step.

    Mathematical formulation:
    - Prior: N(μ₀, σ₀²)
    - Observation: N(x, σ_obs²/wfe)  # WFE-weighted
    - Posterior: N(μ₁, σ₁²)

    Where:
    μ₁ = (μ₀/σ₀² + x·wfe/σ_obs²) / (1/σ₀² + wfe/σ_obs²)
    σ₁² = 1 / (1/σ₀² + wfe/σ_obs²)
    """
    # Effective observation variance (lower WFE = less reliable)
    eff_obs_var = observation_variance / max(wfe_weight, 0.1)

    prior_precision = 1.0 / prior_variance
    obs_precision = 1.0 / eff_obs_var

    posterior_precision = prior_precision + obs_precision
    posterior_mean = (
        prior_precision * prior_mean + obs_precision * observed_epoch
    ) / posterior_precision
    posterior_variance = 1.0 / posterior_precision

    return posterior_mean, posterior_variance
```

### Exponential Moving Average (Alternative)

```python
def ema_epoch_update(
    current_ema: float,
    observed_epoch: int,
    alpha: float = 0.3,
) -> float:
    """EMA update: more weight on recent observations.

    α = 0.3 means ~90% of signal from last 7 folds.
    α = 0.5 means ~90% of signal from last 4 folds.
    """
    return alpha * observed_epoch + (1 - alpha) * current_ema
```

### Initialization Strategies

| Strategy             | When to Use              | Implementation                       |
| -------------------- | ------------------------ | ------------------------------------ |
| **Midpoint prior**   | No domain knowledge      | `mean(epoch_configs)`                |
| **Literature prior** | Published optimal exists | Known optimal ± uncertainty          |
| **Burn-in**          | Sufficient data          | Use first N folds for initialization |

```python
# RECOMMENDED: Use AWFESConfig for principled derivation
config = AWFESConfig.from_search_space(
    min_epoch=80,
    max_epoch=400,
    granularity=5,
)
# prior_variance = ((400-80)/3.92)² ≈ 6,658 (derived automatically)
# observation_variance = prior_variance/4 ≈ 1,665 (derived automatically)

# Alternative strategies (if manual configuration needed):

# Strategy 1: Search-space derived (same as AWFESConfig)
epoch_range = max(EPOCH_CONFIGS) - min(EPOCH_CONFIGS)
prior_mean = np.mean(EPOCH_CONFIGS)
prior_variance = (epoch_range / 3.92) ** 2  # 95% CI spans search space

# Strategy 2: Burn-in (use first 5 folds)
burn_in_optima = [run_fold_sweep(fold) for fold in folds[:5]]
prior_mean = np.mean(burn_in_optima)
base_variance = (epoch_range / 3.92) ** 2 / 4  # Reduced after burn-in
prior_variance = max(np.var(burn_in_optima), base_variance)
```

See [references/epoch-smoothing.md](./references/epoch-smoothing.md) for extended analysis.

---

## OOS Metrics Specification

### Metric Tiers for Test Evaluation

Following [rangebar-eval-metrics](../rangebar-eval-metrics/SKILL.md), compute these metrics on TEST data.

**CRITICAL for Range Bars**: Use time-weighted Sharpe (`sharpe_tw`) instead of simple bar Sharpe. See [range-bar-metrics.md](./references/range-bar-metrics.md) for the canonical implementation. The metrics below assume time-weighted computation for range bar data.

#### Tier 1: Primary Metrics (Mandatory)

| Metric                  | Formula                                  | Threshold | Purpose              |
| ----------------------- | ---------------------------------------- | --------- | -------------------- |
| `sharpe_tw`             | Time-weighted (see range-bar-metrics.md) | > 0       | Core performance     |
| `hit_rate`              | `n_correct_sign / n_total`               | > 0.50    | Directional accuracy |
| `cumulative_pnl`        | `Σ(pred × actual)`                       | > 0       | Total return         |
| `positive_sharpe_folds` | `n_folds(sharpe_tw > 0) / n_folds`       | > 0.55    | Consistency          |
| `wfe_test`              | `test_sharpe_tw / validation_sharpe_tw`  | > 0.30    | Final transfer       |

#### Tier 2: Risk Metrics

| Metric          | Formula                        | Threshold | Purpose        |
| --------------- | ------------------------------ | --------- | -------------- |
| `max_drawdown`  | `max(peak - trough) / peak`    | < 0.30    | Worst loss     |
| `calmar_ratio`  | `annual_return / max_drawdown` | > 0.5     | Risk-adjusted  |
| `profit_factor` | `gross_profit / gross_loss`    | > 1.0     | Win/loss ratio |
| `cvar_10pct`    | `mean(worst 10% returns)`      | > -0.05   | Tail risk      |

#### Tier 3: Statistical Validation

| Metric             | Formula                           | Threshold | Purpose                   |
| ------------------ | --------------------------------- | --------- | ------------------------- |
| `psr`              | `P(true_sharpe > 0)`              | > 0.85    | Statistical significance  |
| `dsr`              | `sharpe - E[max_sharpe_null]`     | > 0.50    | Multiple testing adjusted |
| `binomial_pvalue`  | `binom.test(n_positive, n_total)` | < 0.05    | Sign test                 |
| `hac_ttest_pvalue` | HAC-adjusted t-test               | < 0.05    | Autocorrelation robust    |

### Metric Computation Code

```python
import numpy as np
from scipy.stats import norm, binomtest  # norm for PSR, binomtest for sign test

def compute_oos_metrics(
    predictions: np.ndarray,
    actuals: np.ndarray,
    timestamps: np.ndarray,
    duration_us: np.ndarray | None = None,  # Required for range bars
    market_type: str = "crypto_24_7",  # For annualization factor
) -> dict[str, float]:
    """Compute full OOS metrics suite for test data.

    Args:
        predictions: Model predictions (signed magnitude)
        actuals: Actual returns
        timestamps: Bar timestamps for daily aggregation
        duration_us: Bar durations in microseconds (REQUIRED for range bars)

    Returns:
        Dictionary with all tier metrics

    IMPORTANT: For range bars, pass duration_us to compute sharpe_tw.
    Simple bar_sharpe violates i.i.d. assumption - see range-bar-metrics.md.
    """
    pnl = predictions * actuals

    # Tier 1: Primary
    # For range bars: Use time-weighted Sharpe (canonical)
    if duration_us is not None:
        from exp066e_tau_precision import compute_time_weighted_sharpe
        sharpe_tw, weighted_std, total_days = compute_time_weighted_sharpe(
            bar_pnl=pnl,
            duration_us=duration_us,
            annualize=True,
        )
    else:
        # Fallback for time bars (all same duration)
        daily_pnl = group_by_day(pnl, timestamps)
        weekly_factor = get_daily_to_weekly_factor(market_type=market_type)
        sharpe_tw = (
            np.mean(daily_pnl) / np.std(daily_pnl) * weekly_factor
            if np.std(daily_pnl) > 1e-10 else 0.0
        )

    hit_rate = np.mean(np.sign(predictions) == np.sign(actuals))
    cumulative_pnl = np.sum(pnl)

    # Tier 2: Risk
    equity_curve = np.cumsum(pnl)
    running_max = np.maximum.accumulate(equity_curve)
    drawdowns = (running_max - equity_curve) / np.maximum(running_max, 1e-10)
    max_drawdown = np.max(drawdowns)

    gross_profit = np.sum(pnl[pnl > 0])
    gross_loss = abs(np.sum(pnl[pnl < 0]))
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float("inf")

    # CVaR (10%)
    sorted_pnl = np.sort(pnl)
    cvar_cutoff = max(1, int(len(sorted_pnl) * 0.10))
    cvar_10pct = np.mean(sorted_pnl[:cvar_cutoff])

    # Tier 3: Statistical (use sharpe_tw for PSR)
    sharpe_se = 1.0 / np.sqrt(len(pnl)) if len(pnl) > 0 else 1.0
    psr = norm.cdf(sharpe_tw / sharpe_se) if sharpe_se > 0 else 0.5

    n_positive = np.sum(pnl > 0)
    n_total = len(pnl)
    # Use binomtest (binom_test deprecated since scipy 1.10)
    binomial_pvalue = binomtest(n_positive, n_total, 0.5, alternative="greater").pvalue

    return {
        # Tier 1 (use sharpe_tw for range bars)
        "sharpe_tw": sharpe_tw,
        "hit_rate": hit_rate,
        "cumulative_pnl": cumulative_pnl,
        "n_bars": len(pnl),
        # Tier 2
        "max_drawdown": max_drawdown,
        "profit_factor": profit_factor,
        "cvar_10pct": cvar_10pct,
        # Tier 3
        "psr": psr,
        "binomial_pvalue": binomial_pvalue,
    }
```

### Aggregation Across Folds

```python
def aggregate_test_metrics(fold_results: list[dict]) -> dict[str, float]:
    """Aggregate test metrics across all folds.

    NOTE: For range bars, use sharpe_tw (time-weighted).
    See range-bar-metrics.md for why simple bar_sharpe is invalid for range bars.
    """
    metrics = [r["test_metrics"] for r in fold_results]

    # Positive Sharpe Folds (use sharpe_tw for range bars)
    sharpes = [m["sharpe_tw"] for m in metrics]
    positive_sharpe_folds = np.mean([s > 0 for s in sharpes])

    # Median for robustness
    median_sharpe_tw = np.median(sharpes)
    median_hit_rate = np.median([m["hit_rate"] for m in metrics])

    # DSR for multiple testing (use time-weighted Sharpe)
    n_trials = len(metrics)
    dsr = compute_dsr(median_sharpe_tw, n_trials)

    return {
        "n_folds": len(metrics),
        "positive_sharpe_folds": positive_sharpe_folds,
        "median_sharpe_tw": median_sharpe_tw,
        "mean_sharpe_tw": np.mean(sharpes),
        "std_sharpe_tw": np.std(sharpes),
        "median_hit_rate": median_hit_rate,
        "dsr": dsr,
        "total_pnl": sum(m["cumulative_pnl"] for m in metrics),
    }
```

See [references/oos-metrics.md](./references/oos-metrics.md) for threshold justifications.

---

## Look-Ahead Bias Prevention

### The Problem

Using the same data for epoch selection AND final evaluation creates look-ahead bias:

```
❌ WRONG: Use fold's own optimal epoch for fold's OOS evaluation
   - Epoch selection "sees" validation returns
   - Then apply same epoch to OOS from same period
   - Result: Overly optimistic performance
```

### The Solution: Nested WFO + Bayesian Lag

```
✅ CORRECT: Bayesian-smoothed epoch from PRIOR folds for current TEST
   - Epoch selection on train/validation (inner loop)
   - Update Bayesian posterior with validation-optimal
   - Apply Bayesian-selected epoch to TEST (outer loop)
   - TEST data completely untouched during selection
```

### v3 Temporal Ordering (CRITICAL - 2026 Fix)

The v3 implementation fixes a subtle but critical look-ahead bias bug in the original AWFES workflow. The key insight: **TEST must use `prior_bayesian_epoch`, NOT `val_optimal_epoch`**.

#### The Bug (v2 and earlier)

```python
# v2 BUG: Bayesian update BEFORE test evaluation
for fold in folds:
    epoch_metrics = sweep_epochs(fold.train, fold.validation)
    val_optimal_epoch = select_optimal(epoch_metrics)

    # WRONG: Update Bayesian with current fold's val_optimal
    bayesian.update(val_optimal_epoch, wfe)
    selected_epoch = bayesian.get_current_epoch()  # CONTAMINATED!

    # This selected_epoch is influenced by val_optimal from SAME fold
    test_metrics = evaluate(selected_epoch, fold.test)  # LOOK-AHEAD BIAS
```

#### The Fix (v3)

```python
# v3 CORRECT: Get prior epoch BEFORE any work on current fold
for fold in folds:
    # Step 1: FIRST - Get epoch from ONLY prior folds
    prior_bayesian_epoch = bayesian.get_current_epoch()  # BEFORE any fold work

    # Step 2: Train and sweep to find this fold's optimal
    epoch_metrics = sweep_epochs(fold.train, fold.validation)
    val_optimal_epoch = select_optimal(epoch_metrics)

    # Step 3: TEST uses prior_bayesian_epoch (NOT val_optimal!)
    test_metrics = evaluate(prior_bayesian_epoch, fold.test)  # UNBIASED

    # Step 4: AFTER test - update Bayesian for FUTURE folds only
    bayesian.update(val_optimal_epoch, wfe)  # For fold+1, fold+2, ...
```

#### Why This Matters

| Aspect                | v2 (Buggy)              | v3 (Fixed)          |
| --------------------- | ----------------------- | ------------------- |
| When Bayesian updated | Before test eval        | After test eval     |
| Test epoch source     | Current fold influences | Only prior folds    |
| Information flow      | Future → Present        | Past → Present only |
| Expected bias         | Optimistic by ~10-20%   | Unbiased            |

#### Validation Checkpoint

```python
# MANDATORY: Log these values for audit trail
fold_log.info(
    f"Fold {fold_idx}: "
    f"prior_bayesian_epoch={prior_bayesian_epoch}, "
    f"val_optimal_epoch={val_optimal_epoch}, "
    f"test_uses={prior_bayesian_epoch}"  # MUST equal prior_bayesian_epoch
)
```

See [references/look-ahead-bias.md](./references/look-ahead-bias.md) for detailed examples.

### Embargo Requirements

| Boundary           | Embargo           | Rationale                 |
| ------------------ | ----------------- | ------------------------- |
| Train → Validation | 6% of fold        | Prevent feature leakage   |
| Validation → Test  | 6% of fold        | Prevent selection leakage |
| Fold → Fold        | 1 hour (calendar) | Range bar duration        |

```python
def compute_embargo_indices(
    n_total: int,
    train_pct: float = 0.60,
    val_pct: float = 0.20,
    test_pct: float = 0.20,
    embargo_pct: float = 0.06,
) -> dict[str, tuple[int, int]]:
    """Compute indices for nested split with embargoes.

    Returns dict with (start, end) tuples for each segment.
    """
    embargo_size = int(n_total * embargo_pct)

    train_end = int(n_total * train_pct)
    val_start = train_end + embargo_size
    val_end = val_start + int(n_total * val_pct)
    test_start = val_end + embargo_size
    test_end = n_total

    return {
        "train": (0, train_end),
        "embargo_1": (train_end, val_start),
        "validation": (val_start, val_end),
        "embargo_2": (val_end, test_start),
        "test": (test_start, test_end),
    }
```

### Validation Checklist

Before running AWFES with OOS application:

- [ ] **Three-way split**: Train/Validation/Test clearly separated
- [ ] **Embargoes**: 6% gap at each boundary
- [ ] **Bayesian lag**: Current fold uses posterior from prior folds
- [ ] **No peeking**: Test data untouched until final evaluation
- [ ] **Temporal order**: No shuffling, strict time sequence
- [ ] **Feature computation**: Features computed BEFORE split, no recalculation

### Anti-Patterns

| Anti-Pattern                                     | Detection                              | Fix                    |
| ------------------------------------------------ | -------------------------------------- | ---------------------- |
| Using current fold's epoch on current fold's OOS | `selected_epoch == fold_optimal_epoch` | Use Bayesian posterior |
| Validation overlaps test                         | Date ranges overlap                    | Add embargo            |
| Features computed on full dataset                | Scaler fit includes test               | Per-split scaling      |
| Fold shuffling                                   | Folds not time-ordered                 | Enforce temporal order |

See [references/look-ahead-bias.md](./references/look-ahead-bias.md) for detailed examples.

---

## References

| Topic                    | Reference File                                                                    |
| ------------------------ | --------------------------------------------------------------------------------- |
| Academic Literature      | [academic-foundations.md](./references/academic-foundations.md)                   |
| Mathematical Formulation | [mathematical-formulation.md](./references/mathematical-formulation.md)           |
| Decision Tree            | [epoch-selection-decision-tree.md](./references/epoch-selection-decision-tree.md) |
| Anti-Patterns            | [anti-patterns.md](./references/anti-patterns.md)                                 |
| OOS Application          | [oos-application.md](./references/oos-application.md)                             |
| Epoch Smoothing          | [epoch-smoothing.md](./references/epoch-smoothing.md)                             |
| OOS Metrics              | [oos-metrics.md](./references/oos-metrics.md)                                     |
| Look-Ahead Bias          | [look-ahead-bias.md](./references/look-ahead-bias.md)                             |
| **Feature Sets**         | [feature-sets.md](./references/feature-sets.md)                                   |
| **xLSTM Implementation** | [xlstm-implementation.md](./references/xlstm-implementation.md)                   |
| **Range Bar Metrics**    | [range-bar-metrics.md](./references/range-bar-metrics.md)                         |

## Full Citations

- Bailey, D. H., & López de Prado, M. (2014). The deflated Sharpe ratio: Correcting for selection bias, backtest overfitting and non-normality. _The Journal of Portfolio Management_, 40(5), 94-107.
- Bischl, B., et al. (2023). Multi-Objective Hyperparameter Optimization in Machine Learning. _ACM Transactions on Evolutionary Learning and Optimization_.
- López de Prado, M. (2018). _Advances in Financial Machine Learning_. Wiley. Chapter 7.
- Nomura, M., & Ono, I. (2021). Warm Starting CMA-ES for Hyperparameter Optimization. _AAAI Conference on Artificial Intelligence_.
- Pardo, R. E. (2008). _The Evaluation and Optimization of Trading Strategies, 2nd Edition_. John Wiley & Sons.
