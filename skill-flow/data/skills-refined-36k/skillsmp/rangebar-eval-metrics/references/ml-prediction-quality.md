# ML Prediction Quality Metrics

## Information Coefficient (IC)

The standard metric for alpha model quality:

```python
from scipy.stats import spearmanr, pearsonr

def compute_ic(
    predictions: np.ndarray,
    actuals: np.ndarray,
    method: str = "spearman"
) -> float:
    """Information Coefficient - prediction/return correlation.

    Args:
        predictions: Model predictions
        actuals: Actual returns
        method: "spearman" (rank, preferred) or "pearson" (linear)

    Returns:
        IC in [-1, 1]. Thresholds:
        - >0.02: Acceptable
        - >0.05: Good
        - >0.10: Excellent
    """
    if len(predictions) < 10:
        return float("nan")

    if method == "spearman":
        ic, _ = spearmanr(predictions, actuals)
    else:
        ic, _ = pearsonr(predictions, actuals)

    return float(ic)


def compute_icir(
    predictions: np.ndarray,
    actuals: np.ndarray,
    timestamps: np.ndarray,
    window: int = 20  # Rolling window
) -> float:
    """IC Information Ratio - IC stability over time.

    ICIR = mean(IC) / std(IC) across rolling windows

    Higher ICIR = more consistent signal quality.
    """
    df = pd.DataFrame({
        "pred": predictions,
        "actual": actuals,
        "ts": pd.to_datetime(timestamps, utc=True)
    }).sort_values("ts")

    # Rolling IC
    ics = []
    for i in range(window, len(df)):
        window_data = df.iloc[i-window:i]
        ic, _ = spearmanr(window_data["pred"], window_data["actual"])
        if not np.isnan(ic):
            ics.append(ic)

    if len(ics) < 2:
        return float("nan")

    ic_mean = np.mean(ics)
    ic_std = np.std(ics)

    if ic_std < 1e-10:
        return float("nan")

    return float(ic_mean / ic_std)
```

## Hit Rate (Directional Accuracy)

```python
def compute_hit_rate(
    predictions: np.ndarray,
    actuals: np.ndarray
) -> float:
    """Directional accuracy.

    LIMITATIONS for regression models:
    - Ignores prediction magnitude
    - pred=0.001 and pred=1.0 treated equally
    - Use alongside IC for full picture
    """
    correct = np.sign(predictions) == np.sign(actuals)
    return float(np.mean(correct))
```

## Prediction Autocorrelation (Sticky Detection)

Detects common LSTM pathology of "sticky" predictions:

```python
def compute_prediction_autocorr(
    predictions: np.ndarray,
    lag: int = 1
) -> float:
    """Lag-1 autocorrelation of predictions.

    Healthy range: 0.3 - 0.7

    WARNING signs:
    - >0.9: Predictions barely change ("sticky LSTM")
    - =1.0: Constant predictions (model collapsed to mean)
    - <0.1: Predictions are noise (no memory)

    REMEDIATION (2026-01-19 audit):
    - Return 1.0 for constant predictions (std < 1e-10)
    - NaN from corrcoef division-by-zero is incorrect semantically

    Source: Multi-agent audit finding (model-expert subagent)
    """
    if len(predictions) < lag + 2:
        return float("nan")

    # REMEDIATION: Check for constant predictions (std ≈ 0)
    if np.std(predictions) < 1e-10:
        return 1.0  # Constant predictions have perfect autocorrelation

    return float(np.corrcoef(
        predictions[:-lag],
        predictions[lag:]
    )[0, 1])


def detect_sticky_predictions(
    predictions: np.ndarray,
    threshold: float = 0.9
) -> dict:
    """Full sticky prediction diagnostic.

    Returns:
        - autocorr_lag1: Lag-1 autocorrelation
        - variance_ratio: var(diff) / var(pred)
        - is_sticky: Boolean flag
    """
    autocorr = compute_prediction_autocorr(predictions, lag=1)

    # Variance ratio: should be >0.2 for healthy models
    var_pred = np.var(predictions)
    var_diff = np.var(np.diff(predictions))
    var_ratio = var_diff / var_pred if var_pred > 1e-10 else 0.0

    return {
        "autocorr_lag1": autocorr,
        "variance_ratio": float(var_ratio),
        "is_sticky": autocorr > threshold or var_ratio < 0.1
    }
```

## Residual Diagnostics (Ljung-Box)

```python
from statsmodels.stats.diagnostic import acorr_ljungbox

def compute_residual_diagnostics(
    predictions: np.ndarray,
    actuals: np.ndarray,
    lags: list[int] = [1, 5, 10]
) -> dict:
    """Ljung-Box test for residual autocorrelation.

    If residuals are autocorrelated, model is missing structure.

    Returns:
        - lb_stats: Test statistics per lag
        - lb_pvalues: P-values (>0.05 = white noise residuals)
        - has_structure: True if p < 0.05 for any lag
    """
    residuals = actuals - predictions

    result = acorr_ljungbox(residuals, lags=lags, return_df=True)

    return {
        "lb_stats": result["lb_stat"].tolist(),
        "lb_pvalues": result["lb_pvalue"].tolist(),
        "has_structure": any(result["lb_pvalue"] < 0.05)
    }
```

## Combined Quality Score

```python
def compute_prediction_quality_score(
    predictions: np.ndarray,
    actuals: np.ndarray,
    timestamps: np.ndarray
) -> dict:
    """Combined quality assessment.

    Returns score 0-100 with letter grade.
    """
    ic = compute_ic(predictions, actuals, method="spearman")
    hit_rate = compute_hit_rate(predictions, actuals)
    sticky = detect_sticky_predictions(predictions)

    # Scoring
    score = 0.0

    # IC contribution (0-40 points)
    if not np.isnan(ic):
        if ic > 0.10:
            score += 40
        elif ic > 0.05:
            score += 30
        elif ic > 0.02:
            score += 20
        elif ic > 0:
            score += 10

    # Hit rate contribution (0-30 points)
    if hit_rate > 0.55:
        score += 30
    elif hit_rate > 0.52:
        score += 20
    elif hit_rate > 0.50:
        score += 10

    # Non-sticky contribution (0-30 points)
    if not sticky["is_sticky"]:
        score += 30
    elif sticky["autocorr_lag1"] < 0.95:
        score += 15

    # Letter grade
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    return {
        "score": score,
        "grade": grade,
        "ic": ic,
        "hit_rate": hit_rate,
        "is_sticky": sticky["is_sticky"],
        "autocorr_lag1": sticky["autocorr_lag1"]
    }
```

## Model Collapse Detection (2026-01-19 Audit Addition)

**CRITICAL**: BiLSTM models can collapse to mean prediction when:

- hidden_size is too small (e.g., 16)
- dropout is too aggressive (e.g., 0.5)
- Signal-to-noise ratio is too low

```python
def detect_model_collapse(
    predictions: np.ndarray,
    threshold: float = 1e-6
) -> dict:
    """Detect if model has collapsed to constant predictions.

    REMEDIATION (2026-01-19 audit):
    - Check prediction standard deviation
    - Log warning when detected
    - Continue recording for diagnostics

    Source: Multi-agent audit finding (model-expert subagent)

    Args:
        predictions: Model output predictions
        threshold: Std threshold below which collapse is detected

    Returns:
        Dictionary with collapse detection results
    """
    pred_std = np.std(predictions)
    is_collapsed = pred_std < threshold

    if is_collapsed:
        import logging
        logging.warning(
            f"Model collapse detected: std(predictions)={pred_std:.2e}. "
            "Check architecture/hyperparameters."
        )

    return {
        "is_collapsed": is_collapsed,
        "prediction_std": float(pred_std),
        "prediction_mean": float(np.mean(predictions)),
        "prediction_range": float(np.ptp(predictions)),  # max - min
    }


# RECOMMENDED ARCHITECTURE FIXES for BiLSTM mean prediction collapse:
# 1. Increase hidden_size: 16 → 48 (triple capacity)
# 2. Reduce dropout: 0.5 → 0.3 (less aggressive regularization)
# 3. Check learning rate: may need adjustment
# 4. Verify input feature variance: constant inputs → constant outputs
```

## When to Use Each Metric

| Metric             | Use Case                   | Limitation             |
| ------------------ | -------------------------- | ---------------------- |
| **IC (Spearman)**  | Overall prediction quality | Doesn't capture timing |
| **ICIR**           | Signal stability over time | Needs enough windows   |
| **Hit Rate**       | Quick sanity check         | Ignores magnitude      |
| **Autocorr**       | Detect LSTM pathologies    | Model-specific         |
| **Ljung-Box**      | Residual analysis          | Assumes linearity      |
| **Collapse Check** | Detect mean-prediction bug | Needs model output     |
