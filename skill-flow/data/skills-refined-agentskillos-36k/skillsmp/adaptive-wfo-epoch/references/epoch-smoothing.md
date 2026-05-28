# Epoch Smoothing Methods Reference

Detailed mathematical formulation and implementation for epoch smoothing.

## Mathematical Foundation

### The Problem: Noisy Epoch Selection

Per-fold optimal epochs are noisy estimates of the true optimal:

```
observed_optimal_i = true_optimal + noise_i
```

Where `noise_i` arises from:

- Limited validation samples
- Stochastic training dynamics
- Market regime variation

**Goal**: Estimate `true_optimal` by combining noisy observations.

## Bayesian Updating (Primary Method)

### Conjugate Normal-Normal Model

Assuming:

- Prior: `true_optimal ~ N(μ₀, σ₀²)`
- Likelihood: `observed | true_optimal ~ N(true_optimal, σ²/wfe)`

The posterior is:

```
true_optimal | observed ~ N(μ₁, σ₁²)

where:
μ₁ = (μ₀/σ₀² + x·wfe/σ²) / (1/σ₀² + wfe/σ²)
σ₁² = 1 / (1/σ₀² + wfe/σ²)
```

### WFE Weighting Rationale

WFE measures how reliable the epoch selection is:

- High WFE (0.7+) → validation closely tracks training → reliable selection
- Low WFE (0.3-0.5) → validation diverges → noisy selection

Weighting by WFE gives more influence to reliable observations.

### Full Implementation

```python
from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class BayesianState:
    """State of Bayesian epoch estimator."""

    mean: float
    variance: float
    n_observations: int = 0


class BayesianEpochSmoother:
    """Bayesian smoothing for epoch selection.

    Also known as: BayesianEpochSelector (alias in SKILL.md)

    Uses conjugate Normal-Normal updating with WFE-weighted observations.
    """

    def __init__(
        self,
        epoch_configs: list[int],
        prior_mean: Optional[float] = None,
        prior_variance: Optional[float] = None,
        observation_variance: Optional[float] = None,
        min_wfe_weight: float = 0.1,
    ):
        """Initialize smoother.

        Args:
            epoch_configs: Valid epoch values
            prior_mean: Prior mean (default: midpoint of configs)
            prior_variance: Prior variance (default: derived from search space)
            observation_variance: Base observation noise variance (default: prior_var/4)
            min_wfe_weight: Minimum WFE weight to prevent division by zero

        Variance Derivation (if not provided):
            Prior should span search space with ~95% coverage.
            For Normal: 95% CI = mean ± 1.96σ → range = 3.92σ → σ² = (range/3.92)²
            Observation variance: prior_variance/4 for balanced learning rate.
        """
        self.epoch_configs = sorted(epoch_configs)
        self.min_wfe_weight = min_wfe_weight

        # Derive variances from search space if not provided
        epoch_range = max(self.epoch_configs) - min(self.epoch_configs)
        default_prior_var = (epoch_range / 3.92) ** 2  # 95% CI spans search space
        default_obs_var = default_prior_var / 4  # Balanced learning rate

        self.observation_variance = observation_variance or default_obs_var

        # Initialize state with derived or provided variance
        self.state = BayesianState(
            mean=prior_mean or np.mean(epoch_configs),
            variance=prior_variance or default_prior_var,
            n_observations=0,
        )

        # History for diagnostics
        self.history: list[dict] = []

    def update(self, observed_epoch: int, wfe: float) -> int:
        """Update posterior with new observation.

        Args:
            observed_epoch: Optimal epoch from current fold's validation
            wfe: Walk-Forward Efficiency (reliability weight)

        Returns:
            Smoothed epoch selection (snapped to valid config)
        """
        # Clamp WFE to [min_wfe_weight, 2.0] to prevent extreme weights:
        #   - Lower bound (min_wfe_weight=0.1): Prevents division issues
        #   - Upper bound (2.0): WFE > 2 indicates OOS >> IS, which suggests
        #     regime shift or data anomaly rather than genuine skill transfer.
        #     Capping at 2.0 treats such observations with appropriate skepticism.
        wfe_clamped = max(self.min_wfe_weight, min(wfe, 2.0))

        # Effective observation variance (lower WFE = higher variance)
        eff_obs_var = self.observation_variance / wfe_clamped

        # Bayesian update
        prior_precision = 1.0 / self.state.variance
        obs_precision = 1.0 / eff_obs_var

        posterior_precision = prior_precision + obs_precision
        posterior_mean = (
            prior_precision * self.state.mean +
            obs_precision * observed_epoch
        ) / posterior_precision
        posterior_variance = 1.0 / posterior_precision

        # Record history
        self.history.append({
            "observed_epoch": observed_epoch,
            "wfe": wfe,
            "wfe_clamped": wfe_clamped,
            "prior_mean": self.state.mean,
            "prior_variance": self.state.variance,
            "posterior_mean": posterior_mean,
            "posterior_variance": posterior_variance,
            "selected_epoch": self._snap_to_config(posterior_mean),
        })

        # Update state
        self.state = BayesianState(
            mean=posterior_mean,
            variance=posterior_variance,
            n_observations=self.state.n_observations + 1,
        )

        return self._snap_to_config(posterior_mean)

    def get_current_epoch(self) -> int:
        """Get current smoothed epoch without updating."""
        return self._snap_to_config(self.state.mean)

    def get_confidence_interval(self, level: float = 0.95) -> tuple[int, int]:
        """Get confidence interval for true optimal epoch.

        Args:
            level: Confidence level (default: 95%)

        Returns:
            (lower, upper) epoch bounds
        """
        from scipy.stats import norm

        z = norm.ppf((1 + level) / 2)
        std = np.sqrt(self.state.variance)

        lower = self.state.mean - z * std
        upper = self.state.mean + z * std

        return (
            self._snap_to_config(lower),
            self._snap_to_config(upper),
        )

    def _snap_to_config(self, continuous: float) -> int:
        """Snap continuous value to nearest valid config."""
        return min(self.epoch_configs, key=lambda e: abs(e - continuous))

    def reset(self, prior_mean: Optional[float] = None) -> None:
        """Reset to prior state with derived variance."""
        epoch_range = max(self.epoch_configs) - min(self.epoch_configs)
        default_prior_var = (epoch_range / 3.92) ** 2  # 95% CI spans search space

        self.state = BayesianState(
            mean=prior_mean or np.mean(self.epoch_configs),
            variance=default_prior_var,
            n_observations=0,
        )
        self.history.clear()
```

## Alternative Methods

### Exponential Moving Average (EMA)

Simpler than Bayesian, good for quick implementation.

```python
class EMAEpochSmoother:
    """Exponential moving average epoch smoothing."""

    def __init__(
        self,
        epoch_configs: list[int],
        alpha: float = 0.3,
        initial: Optional[float] = None,
    ):
        """Initialize EMA smoother.

        Args:
            epoch_configs: Valid epoch values
            alpha: Smoothing factor (higher = more responsive)
                   α=0.3 → ~90% signal from last 7 observations
                   α=0.5 → ~90% signal from last 4 observations
            initial: Initial EMA value
        """
        self.epoch_configs = sorted(epoch_configs)
        self.alpha = alpha
        self.ema = initial or np.mean(epoch_configs)
        self.history: list[dict] = []

    def update(self, observed_epoch: int) -> int:
        """Update EMA with new observation."""
        new_ema = self.alpha * observed_epoch + (1 - self.alpha) * self.ema

        self.history.append({
            "observed": observed_epoch,
            "prior_ema": self.ema,
            "posterior_ema": new_ema,
            "selected": self._snap_to_config(new_ema),
        })

        self.ema = new_ema
        return self._snap_to_config(new_ema)

    def _snap_to_config(self, continuous: float) -> int:
        return min(self.epoch_configs, key=lambda e: abs(e - continuous))
```

### Simple Moving Average (SMA)

Most stable but slowest to adapt.

```python
class SMAEpochSmoother:
    """Simple moving average epoch smoothing."""

    def __init__(
        self,
        epoch_configs: list[int],
        window: int = 5,
    ):
        self.epoch_configs = sorted(epoch_configs)
        self.window = window
        self.observations: list[int] = []

    def update(self, observed_epoch: int) -> int:
        """Update SMA with new observation."""
        self.observations.append(observed_epoch)
        if len(self.observations) > self.window:
            self.observations.pop(0)

        sma = np.mean(self.observations)
        return self._snap_to_config(sma)

    def _snap_to_config(self, continuous: float) -> int:
        return min(self.epoch_configs, key=lambda e: abs(e - continuous))
```

### Median Smoother

Robust to outliers from regime changes.

```python
class MedianEpochSmoother:
    """Median-based epoch smoothing."""

    def __init__(
        self,
        epoch_configs: list[int],
        window: int = 5,
    ):
        self.epoch_configs = sorted(epoch_configs)
        self.window = window
        self.observations: list[int] = []

    def update(self, observed_epoch: int) -> int:
        """Update with new observation, return median."""
        self.observations.append(observed_epoch)
        if len(self.observations) > self.window:
            self.observations.pop(0)

        median_val = np.median(self.observations)
        return self._snap_to_config(median_val)

    def _snap_to_config(self, continuous: float) -> int:
        return min(self.epoch_configs, key=lambda e: abs(e - continuous))
```

## Method Selection Guide

| Criterion                      | Bayesian | EMA          | SMA  | Median |
| ------------------------------ | -------- | ------------ | ---- | ------ |
| **Uncertainty quantification** | Yes      | No           | No   | No     |
| **WFE weighting**              | Yes      | No (can add) | No   | No     |
| **Responsiveness**             | Medium   | High         | Low  | Medium |
| **Outlier robustness**         | Medium   | Low          | Low  | High   |
| **Implementation complexity**  | High     | Low          | Low  | Low    |
| **Interpretability**           | Medium   | High         | High | High   |

### Recommendations

1. **Default choice**: Bayesian (principled, handles WFE weighting)
2. **Quick prototype**: EMA with α=0.3
3. **Regime change prone**: Median with window=5
4. **Maximum stability**: SMA with window=7

## Initialization Strategies

### Strategy 1: Search-Space Derived (RECOMMENDED)

```python
# Principled: Derive from search bounds (no magic numbers)
# Prior spans search space with 95% coverage
epoch_range = max(EPOCH_CONFIGS) - min(EPOCH_CONFIGS)
prior_mean = np.mean(EPOCH_CONFIGS)  # Midpoint
prior_variance = (epoch_range / 3.92) ** 2  # 95% CI spans search space

# Example: EPOCH_CONFIGS = [100, 200, 400, 800, 1600]
# epoch_range = 1500, prior_variance = (1500/3.92)² ≈ 146,506
```

### Strategy 2: Uninformative Prior

```python
# No domain knowledge - very wide prior
prior_mean = np.mean(EPOCH_CONFIGS)  # Midpoint
prior_variance = np.var(EPOCH_CONFIGS) * 4  # Very wide
```

### Strategy 3: Literature-Informed Prior

```python
# BiLSTM literature suggests 100-300 optimal for financial data
# But prefer deriving from YOUR search space
prior_mean = 200
epoch_range = max(EPOCH_CONFIGS) - min(EPOCH_CONFIGS)
prior_variance = (epoch_range / 3.92) ** 2  # Still principled
```

### Strategy 4: Burn-In Initialization

```python
# Use first N folds to establish prior
BURN_IN_FOLDS = 5
burn_in_optima = [get_fold_optimal(fold) for fold in folds[:BURN_IN_FOLDS]]

prior_mean = np.mean(burn_in_optima)
# Combine observed variance with search-space derived base
epoch_range = max(EPOCH_CONFIGS) - min(EPOCH_CONFIGS)
base_variance = (epoch_range / 3.92) ** 2 / 4  # Reduced after burn-in
prior_variance = max(np.var(burn_in_optima), base_variance)
```

### Strategy 5: Empirical Bayes

```python
# Estimate prior from full sweep data (use with caution - slight look-ahead)
all_fold_optima = [r["optimal_epoch"] for r in full_sweep_results]

prior_mean = np.mean(all_fold_optima)
prior_variance = max(np.var(all_fold_optima), 100)  # Floor to prevent collapse
```

## Convergence Analysis

### Bayesian Posterior Convergence

After N observations, posterior variance:

```
σ_N² = 1 / (1/σ₀² + N·wfe_avg/σ_obs²)
```

**Example with principled derivation** (search space [100, 2000], granularity=5):

```python
epoch_range = 2000 - 100 = 1900
prior_variance = (1900 / 3.92)² ≈ 235,000
observation_variance = prior_variance / 4 ≈ 58,750
```

With wfe_avg=0.5:

- After 5 folds: σ² ≈ 31,000 (±176 epochs)
- After 10 folds: σ² ≈ 17,600 (±133 epochs)
- After 20 folds: σ² ≈ 9,600 (±98 epochs)

**Key insight**: Larger search spaces need more folds to converge. This is principled - uncertainty should scale with search space size.

### EMA Effective Memory

For EMA with α:

- Effective window = 2/α - 1
- 90% of signal from last `log(0.1)/log(1-α)` observations

| α   | Effective Window | 90% Signal From |
| --- | ---------------- | --------------- |
| 0.2 | 9                | 11 folds        |
| 0.3 | 5.7              | 7 folds         |
| 0.5 | 3                | 4 folds         |

## Diagnostic Plots

### Posterior Evolution

```python
import matplotlib.pyplot as plt

def plot_bayesian_evolution(smoother: BayesianEpochSmoother):
    """Plot Bayesian posterior evolution."""
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    folds = list(range(len(smoother.history)))
    observed = [h["observed_epoch"] for h in smoother.history]
    posterior_mean = [h["posterior_mean"] for h in smoother.history]
    posterior_std = [np.sqrt(h["posterior_variance"]) for h in smoother.history]

    # Mean evolution
    ax1 = axes[0]
    ax1.scatter(folds, observed, label="Observed", alpha=0.6)
    ax1.plot(folds, posterior_mean, label="Posterior Mean", color="red")
    ax1.fill_between(
        folds,
        [m - 2*s for m, s in zip(posterior_mean, posterior_std)],
        [m + 2*s for m, s in zip(posterior_mean, posterior_std)],
        alpha=0.2, color="red", label="95% CI"
    )
    ax1.set_xlabel("Fold")
    ax1.set_ylabel("Epoch")
    ax1.legend()
    ax1.set_title("Bayesian Epoch Posterior Evolution")

    # Variance evolution
    ax2 = axes[1]
    ax2.plot(folds, posterior_std, color="blue")
    ax2.set_xlabel("Fold")
    ax2.set_ylabel("Posterior Std")
    ax2.set_title("Posterior Uncertainty (decreasing = learning)")

    plt.tight_layout()
    return fig
```
