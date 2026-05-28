# OOS Application Phase Reference

Detailed implementation guide for applying selected epochs to test data.

## Complete Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AWFES OOS Application Workflow                        │
└─────────────────────────────────────────────────────────────────────────────┘

For each fold i:
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. SPLIT: Divide fold into train (60%), validation (20%), test (20%)        │
│    with 6% embargo gaps                                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. SWEEP: Train at each epoch on TRAIN, evaluate WFE on VALIDATION          │
│    • epochs = [80, 100, 150, 200, 400]                                       │
│    • WFE = val_sharpe / train_sharpe                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. UPDATE: Update Bayesian posterior with validation-optimal epoch           │
│    • observed = argmax(WFE)                                                  │
│    • posterior = bayesian_update(prior, observed, WFE)                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. SELECT: Get Bayesian-smoothed epoch for TEST evaluation                   │
│    • selected = snap_to_config(posterior_mean)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. TRAIN FINAL: Train on TRAIN + VALIDATION at selected epoch                │
│    • combined_data = concat(train, validation)                               │
│    • final_model = train(combined_data, epochs=selected)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 6. EVALUATE: Compute OOS metrics on TEST (untouched until now)               │
│    • predictions = final_model.predict(test_X)                               │
│    • metrics = compute_oos_metrics(predictions, test_y)                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Implementation

### Full Application Class

```python
from dataclasses import dataclass, field
from typing import Callable, Protocol
import numpy as np


class ModelProtocol(Protocol):
    """Protocol for models compatible with AWFES."""

    def fit(self, X: np.ndarray, y: np.ndarray, epochs: int) -> None:
        ...

    def predict(self, X: np.ndarray) -> np.ndarray:
        ...


@dataclass
class FoldSplit:
    """Data split for a single fold."""

    X_train: np.ndarray
    y_train: np.ndarray
    X_validation: np.ndarray
    y_validation: np.ndarray
    X_test: np.ndarray
    y_test: np.ndarray
    timestamps_test: np.ndarray
    fold_idx: int


@dataclass
class AWFESResult:
    """Result from AWFES application to a single fold."""

    fold_idx: int
    validation_optimal_epoch: int
    validation_optimal_wfe: float
    bayesian_selected_epoch: int
    posterior_mean: float
    posterior_variance: float
    test_metrics: dict[str, float]
    epoch_sweep_results: list[dict]


class AWFESOOSApplication:
    """Apply AWFES with Bayesian smoothing to test data."""

    def __init__(
        self,
        epoch_configs: list[int],
        model_factory: Callable[[], ModelProtocol],
        prior_mean: float | None = None,
        prior_variance: float | None = None,
        observation_variance: float | None = None,
    ):
        """Initialize AWFES OOS application.

        Args:
            epoch_configs: List of epoch candidates to sweep
            model_factory: Factory function returning fresh model instances
            prior_mean: Prior mean for Bayesian updating (default: midpoint)
            prior_variance: Prior variance (default: derived from search space)
            observation_variance: Observation noise variance (default: prior_var/4)

        Variance Derivation:
            Prior should span search space with ~95% coverage.
            range = max - min, σ = range/3.92, σ² = (range/3.92)²
            observation_variance = prior_variance/4 for balanced learning.
        """
        self.epoch_configs = epoch_configs
        self.model_factory = model_factory
        self.prior_mean = prior_mean or np.mean(epoch_configs)

        # Derive variances from search space if not provided
        epoch_range = max(epoch_configs) - min(epoch_configs)
        default_prior_var = (epoch_range / 3.92) ** 2  # 95% CI spans search space
        default_obs_var = default_prior_var / 4  # Balanced learning rate

        self.prior_variance = prior_variance or default_prior_var
        self.observation_variance = observation_variance or default_obs_var

        # Bayesian state
        self.posterior_mean = self.prior_mean
        self.posterior_variance = self.prior_variance
        self.history: list[AWFESResult] = []

    def process_fold(self, split: FoldSplit) -> AWFESResult:
        """Process a single fold with AWFES.

        Args:
            split: FoldSplit with train/validation/test data

        Returns:
            AWFESResult with all metrics and selections
        """
        # Step 1: Epoch sweep on train → validation
        epoch_results = []
        for epoch in self.epoch_configs:
            model = self.model_factory()
            model.fit(split.X_train, split.y_train, epochs=epoch)

            train_preds = model.predict(split.X_train)
            val_preds = model.predict(split.X_validation)

            train_sharpe = self._compute_sharpe(train_preds, split.y_train)
            val_sharpe = self._compute_sharpe(val_preds, split.y_validation)

            # Use data-driven threshold instead of hardcoded value
            # Rationale: 2/√n adapts to sample size; see compute_is_sharpe_threshold()
            is_threshold = compute_is_sharpe_threshold(len(split.X_train))
            wfe = val_sharpe / train_sharpe if abs(train_sharpe) > is_threshold else None

            epoch_results.append({
                "epoch": epoch,
                "train_sharpe": train_sharpe,
                "val_sharpe": val_sharpe,
                "wfe": wfe,
            })

        # Step 2: Find validation-optimal
        valid_results = [r for r in epoch_results if r["wfe"] is not None]
        if valid_results:
            val_optimal = max(valid_results, key=lambda r: r["wfe"])
        else:
            # Fallback: lowest epoch if no valid WFE
            val_optimal = {"epoch": self.epoch_configs[0], "wfe": 0.3}

        # Step 3: Bayesian update
        selected_epoch = self._bayesian_update(
            val_optimal["epoch"],
            val_optimal["wfe"] or 0.3,
        )

        # Step 4: Train final model on train + validation
        combined_X = np.vstack([split.X_train, split.X_validation])
        combined_y = np.hstack([split.y_train, split.y_validation])

        final_model = self.model_factory()
        final_model.fit(combined_X, combined_y, epochs=selected_epoch)

        # Step 5: Evaluate on test
        test_preds = final_model.predict(split.X_test)
        test_metrics = self._compute_oos_metrics(
            test_preds, split.y_test, split.timestamps_test
        )

        result = AWFESResult(
            fold_idx=split.fold_idx,
            validation_optimal_epoch=val_optimal["epoch"],
            validation_optimal_wfe=val_optimal["wfe"] or 0.0,
            bayesian_selected_epoch=selected_epoch,
            posterior_mean=self.posterior_mean,
            posterior_variance=self.posterior_variance,
            test_metrics=test_metrics,
            epoch_sweep_results=epoch_results,
        )

        self.history.append(result)
        return result

    def _bayesian_update(self, observed_epoch: int, wfe: float) -> int:
        """Update Bayesian posterior and return selected epoch."""
        # Clamp WFE to [0.1, 2.0] to prevent extreme weights
        wfe_clamped = max(0.1, min(wfe, 2.0))
        eff_obs_var = self.observation_variance / wfe_clamped

        prior_precision = 1.0 / self.posterior_variance
        obs_precision = 1.0 / eff_obs_var

        new_precision = prior_precision + obs_precision
        new_mean = (
            prior_precision * self.posterior_mean +
            obs_precision * observed_epoch
        ) / new_precision

        self.posterior_mean = new_mean
        self.posterior_variance = 1.0 / new_precision

        return self._snap_to_config(new_mean)

    def _snap_to_config(self, continuous: float) -> int:
        """Snap continuous value to nearest epoch config."""
        return min(self.epoch_configs, key=lambda e: abs(e - continuous))

    def _compute_sharpe(self, preds: np.ndarray, actuals: np.ndarray) -> float:
        """Compute bar-level Sharpe ratio."""
        pnl = preds * actuals
        if np.std(pnl) < 1e-10:
            return 0.0
        return np.mean(pnl) / np.std(pnl)

    def _compute_oos_metrics(
        self,
        preds: np.ndarray,
        actuals: np.ndarray,
        timestamps: np.ndarray,
        duration_us: np.ndarray | None = None,
    ) -> dict[str, float]:
        """Compute full OOS metrics suite.

        For range bars, pass duration_us to compute time-weighted Sharpe.
        See range-bar-metrics.md for why simple bar_sharpe is invalid.
        """
        pnl = preds * actuals

        # Compute Sharpe (time-weighted for range bars)
        if duration_us is not None:
            from exp066e_tau_precision import compute_time_weighted_sharpe
            sharpe_tw, _, _ = compute_time_weighted_sharpe(
                bar_pnl=pnl, duration_us=duration_us, annualize=True
            )
        else:
            # Fallback for time bars (uniform duration)
            daily_pnl = self._group_by_day(pnl, timestamps)
            sharpe_tw = (
                np.mean(daily_pnl) / np.std(daily_pnl) * np.sqrt(7)
                if len(daily_pnl) > 1 and np.std(daily_pnl) > 1e-10
                else 0.0
            )

        # Hit rate
        hit_rate = np.mean(np.sign(preds) == np.sign(actuals))

        # Risk metrics
        equity = np.cumsum(pnl)
        running_max = np.maximum.accumulate(equity)
        drawdowns = (running_max - equity) / np.maximum(running_max, 1e-10)
        max_dd = np.max(drawdowns) if len(drawdowns) > 0 else 0.0

        # Profit factor
        gross_profit = np.sum(pnl[pnl > 0])
        gross_loss = abs(np.sum(pnl[pnl < 0]))
        profit_factor = (
            gross_profit / gross_loss
            if gross_loss > 0
            else float("inf") if gross_profit > 0 else 1.0
        )

        # CVaR (10%)
        sorted_pnl = np.sort(pnl)
        cutoff = max(1, int(len(sorted_pnl) * 0.10))
        cvar_10 = np.mean(sorted_pnl[:cutoff])

        return {
            "sharpe_tw": sharpe_tw,
            "hit_rate": hit_rate,
            "cumulative_pnl": np.sum(pnl),
            "n_bars": len(pnl),
            "max_drawdown": max_dd,
            "profit_factor": profit_factor,
            "cvar_10pct": cvar_10,
        }

    def _group_by_day(
        self, values: np.ndarray, timestamps: np.ndarray
    ) -> np.ndarray:
        """Group values by calendar day."""
        import pandas as pd

        df = pd.DataFrame({"value": values, "ts": pd.to_datetime(timestamps)})
        daily = df.groupby(df["ts"].dt.date)["value"].sum()
        return daily.values

    def aggregate_results(self) -> dict[str, float]:
        """Aggregate test metrics across all processed folds.

        Uses sharpe_tw (time-weighted) for range bar data.
        See range-bar-metrics.md for canonical implementation.
        """
        if not self.history:
            return {}

        sharpes = [r.test_metrics["sharpe_tw"] for r in self.history]
        hit_rates = [r.test_metrics["hit_rate"] for r in self.history]

        return {
            "n_folds": len(self.history),
            "positive_sharpe_folds": np.mean([s > 0 for s in sharpes]),
            "mean_sharpe_tw": np.mean(sharpes),
            "median_sharpe_tw": np.median(sharpes),
            "std_sharpe_tw": np.std(sharpes),
            "mean_hit_rate": np.mean(hit_rates),
            "total_pnl": sum(r.test_metrics["cumulative_pnl"] for r in self.history),
        }
```

## Usage Example

```python
from your_model import BiLSTMModel
from adaptive_wfo_epoch import AWFESConfig

# Define epoch configs via principled derivation
config = AWFESConfig.from_search_space(
    min_epoch=80,
    max_epoch=400,
    granularity=5,  # Log-spaced: [80, 113, 160, 226, 400]
)

# Create application - variances derived from search space automatically
awfes = AWFESOOSApplication(
    epoch_configs=config.epoch_configs,
    model_factory=lambda: BiLSTMModel(hidden_size=48, dropout=0.3),
    # prior_variance and observation_variance derived automatically:
    # prior_var = ((400-80)/3.92)² ≈ 6,658
    # obs_var = prior_var/4 ≈ 1,665
)

# Process each fold
for fold in generate_folds(data):
    split = create_nested_split(fold, train_pct=0.60, val_pct=0.20, test_pct=0.20)
    result = awfes.process_fold(split)

    print(f"Fold {result.fold_idx}:")
    print(f"  Validation optimal: {result.validation_optimal_epoch} (WFE={result.validation_optimal_wfe:.3f})")
    print(f"  Bayesian selected: {result.bayesian_selected_epoch}")
    print(f"  Test Sharpe (tw): {result.test_metrics['sharpe_tw']:.3f}")

# Aggregate
agg = awfes.aggregate_results()
print(f"\nAggregate Results:")
print(f"  Positive Sharpe Folds: {agg['positive_sharpe_folds']:.1%}")
print(f"  Median Sharpe (tw): {agg['median_sharpe_tw']:.3f}")
```

## Key Design Decisions

### Why Bayesian over Direct Application?

| Approach                   | Bias              | Variance | Recommendation  |
| -------------------------- | ----------------- | -------- | --------------- |
| Direct (same fold)         | HIGH (look-ahead) | Low      | Never use       |
| Carry-forward (prior fold) | Low               | High     | Simple baseline |
| Bayesian                   | Low               | Medium   | **Recommended** |

### Why Train on Train+Validation for Final Model?

After epoch selection is complete (using validation), we want maximum data for the final model:

- Validation data is no longer needed for selection
- More training data improves generalization
- Test remains completely held out

### Why 60/20/20 Split?

| Split            | Rationale                       |
| ---------------- | ------------------------------- |
| Train (60%)      | Sufficient for model learning   |
| Validation (20%) | Enough for reliable WFE         |
| Test (20%)       | Realistic production assessment |

With 6% embargo at each boundary, effective data usage is ~82%.
