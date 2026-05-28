# Anti-Patterns in Range Bar Metrics

Common pitfalls and their remediation when computing metrics on range bar data.

## Transaction Costs (CRITICAL)

### The Problem

Zero-cost assumption in Sharpe calculation **overstates performance by 15-30%** for typical high-frequency strategies.

```python
# WRONG: Zero-cost assumption (common in backtesting)
pnl = predictions * actuals  # No transaction costs
sharpe = mean(pnl) / std(pnl)  # Overstated by 15-30%
```

### Impact by Strategy Type

| Strategy Type         | Typical Turnover | Cost Impact on Sharpe |
| --------------------- | ---------------- | --------------------- |
| Low-frequency (daily) | 10-50%/month     | -5% to -10%           |
| Medium-frequency      | 100-300%/month   | -15% to -25%          |
| High-frequency        | >500%/month      | -25% to -40%          |
| **Range bar BiLSTM**  | 200-400%/month   | **-20% to -30%**      |

### Cost Model

```python
def compute_transaction_costs(
    predictions: np.ndarray,
    prices: np.ndarray,
    cost_bps: float = 5.0,  # 5 bps = 0.05%
) -> np.ndarray:
    """Compute transaction costs from position changes.

    Args:
        predictions: Signed position sizes
        prices: Asset prices at each bar
        cost_bps: Round-trip cost in basis points

    Returns:
        Array of transaction costs (negative values)
    """
    position_changes = np.abs(np.diff(predictions, prepend=0))
    notional_traded = position_changes * prices
    return -notional_traded * (cost_bps / 10000)


def net_sharpe_with_costs(
    predictions: np.ndarray,
    actuals: np.ndarray,
    timestamps: np.ndarray,
    prices: np.ndarray,
    cost_bps: float = 5.0,
    days_per_week: int = 7,
) -> float:
    """Weekly Sharpe net of transaction costs."""
    gross_pnl = predictions * actuals
    tx_costs = compute_transaction_costs(predictions, prices, cost_bps)
    net_pnl = gross_pnl + tx_costs  # tx_costs are negative

    daily_pnl = _group_by_day(net_pnl, timestamps)
    if len(daily_pnl) < 2 or np.std(daily_pnl) < 1e-10:
        return 0.0

    return float(np.mean(daily_pnl) / np.std(daily_pnl) * np.sqrt(days_per_week))
```

### Typical Cost Assumptions

| Exchange/Broker     | Maker Fee | Taker Fee | Spread Impact | Total (bps) |
| ------------------- | --------- | --------- | ------------- | ----------- |
| **Binance BTC**     | 1 bps     | 2 bps     | 2-3 bps       | 5-6 bps     |
| **EXNESS EUR/USD**  | 0.5 bps   | 1 bps     | 1-2 bps       | 2-4 bps     |
| Coinbase BTC        | 4 bps     | 6 bps     | 3-5 bps       | 10-15 bps   |
| Interactive Brokers | 0.5 bps   | 0.5 bps   | 0.5 bps       | 1-2 bps     |

### Remediation

1. **Always report both gross and net Sharpe**
2. **Use conservative cost assumptions** (upper bound of range)
3. **Log turnover alongside Sharpe for cost sensitivity analysis**

```python
def evaluate_fold_with_costs(
    predictions: np.ndarray,
    actuals: np.ndarray,
    timestamps: np.ndarray,
    prices: np.ndarray,
    cost_bps: float = 5.0,
) -> dict:
    """Full evaluation with cost transparency."""
    gross_sharpe = compute_weekly_sharpe(predictions * actuals, timestamps)
    net_sharpe = net_sharpe_with_costs(
        predictions, actuals, timestamps, prices, cost_bps
    )

    # Turnover metrics
    position_changes = np.abs(np.diff(predictions, prepend=0))
    daily_turnover = _group_by_day(position_changes, timestamps)
    monthly_turnover = np.mean(daily_turnover) * 30

    return {
        "gross_weekly_sharpe": gross_sharpe,
        "net_weekly_sharpe": net_sharpe,
        "sharpe_cost_haircut": (gross_sharpe - net_sharpe) / gross_sharpe if gross_sharpe > 0 else 0,
        "monthly_turnover_pct": float(monthly_turnover * 100),
        "cost_bps_assumed": cost_bps,
    }
```

## Survivorship Bias

### The Problem

Backtesting on currently traded assets excludes delisted/failed assets, biasing results upward.

**Crypto-specific**: Many altcoins have been delisted, depegged, or gone to zero (e.g., LUNA, FTT).

### Impact

- Equity studies show 1-2% annual return bias
- Crypto markets: **3-5% bias** due to higher failure rates

### Remediation

1. Use point-in-time datasets (e.g., Kaiko, CryptoDataDownload historical)
2. Include delisted assets in backtests
3. Report "survivorship-adjusted" returns

## Look-Ahead Bias

### The Problem

Using future information in feature computation or model training.

Common sources:

- Normalizing features with full-sample statistics
- Using daily OHLC when predicting intraday
- Leaking test data into training via feature engineering

### Detection

```python
def detect_lookahead_bias(
    predictions: np.ndarray,
    timestamps: np.ndarray,
    model_training_end: pd.Timestamp,
) -> dict:
    """Check for temporal consistency."""
    pred_times = pd.to_datetime(timestamps, utc=True)

    # Predictions before training end are suspicious
    early_predictions = pred_times < model_training_end
    n_early = np.sum(early_predictions)

    return {
        "n_predictions_before_training_end": int(n_early),
        "potential_lookahead_bias": n_early > 0,
    }
```

### Remediation

See [adaptive-wfo-epoch/references/look-ahead-bias.md](../../adaptive-wfo-epoch/references/look-ahead-bias.md) for detailed prevention strategies.

## sqrt(252) for Crypto

### The Problem

Using equity annualization (sqrt(252)) for 24/7 crypto markets **understates** volatility.

```python
# WRONG
crypto_annual_sharpe = daily_sharpe * np.sqrt(252)  # Wrong!

# CORRECT
crypto_annual_sharpe = daily_sharpe * np.sqrt(365)  # 24/7 markets
crypto_weekly_sharpe = daily_sharpe * np.sqrt(7)    # Weekly
```

### Impact

Using sqrt(252) instead of sqrt(365) underestimates true Sharpe by:

- Daily → Annual: **17% understatement**
- Daily → Weekly: **15% understatement** (sqrt(5) vs sqrt(7))

See [crypto-markets.md](./crypto-markets.md) for full annualization guide.

## Model Collapse

### The Problem

BiLSTM and other RNN models can collapse to constant predictions (output = mean of targets).

Symptoms:

- `prediction_autocorr ≈ 1.0`
- `std(predictions) < 1e-6`
- `weekly_sharpe = 0` despite positive historical returns

### Causes

1. **Undersized hidden layer**: 16 units too small for range bar complexity
2. **Excessive dropout**: 0.5 dropout removes too much signal
3. **Learning rate too high**: Model overshoots and converges to mean
4. **Insufficient data**: Model can't learn meaningful patterns

### Remediation

```python
# BEFORE (causes collapse on range bars)
HIDDEN_SIZE = 16
DROPOUT = 0.5

# AFTER (prevents collapse)
HIDDEN_SIZE = 48  # Triple capacity
DROPOUT = 0.3     # Less aggressive regularization
```

See [ml-prediction-quality.md](./ml-prediction-quality.md#model-collapse-detection) for detection code.

## Insufficient Sample Size

### The Problem

Computing ratios (Omega, Profit Factor, Sharpe SE) with too few observations produces unreliable estimates.

### Minimum Sample Sizes

| Metric        | Minimum | Recommended | Rationale              |
| ------------- | ------- | ----------- | ---------------------- |
| Sharpe        | 2 days  | 30 days     | CLT assumptions        |
| Sharpe SE     | 20 days | 60 days     | Higher moments         |
| Omega         | 5 days  | 20 days     | Need both gains/losses |
| Profit Factor | 5 days  | 20 days     | Need both gains/losses |
| PSR           | 30 days | 100 days    | Statistical power      |
| DSR           | 30 days | 100 days    | Multiple testing       |

### Remediation

All functions in `compute_metrics.py` now include `min_days` guards:

```python
def compute_omega(pnl, timestamps, threshold=0.0, min_days=5):
    daily_pnl = _group_by_day(pnl, timestamps)
    if len(daily_pnl) < min_days:
        return float("nan")  # Unreliable
    # ... rest of computation
```

## Summary Checklist

Before reporting range bar metrics:

- [ ] Transaction costs modeled (gross AND net Sharpe)
- [ ] Survivorship bias considered (point-in-time data)
- [ ] Look-ahead bias prevented (temporal validation)
- [ ] Correct annualization (sqrt(7) or sqrt(365) for crypto)
- [ ] Model collapse checked (`prediction_autocorr`, `is_collapsed`)
- [ ] Sufficient sample size (n_days > min thresholds)
- [ ] Session filter matches annualization (sqrt(5) if filtered)

## References

| Anti-Pattern           | Academic Reference             |
| ---------------------- | ------------------------------ |
| Transaction costs      | De Prado (2018), Chapter 15    |
| Survivorship bias      | Brown et al. (1992)            |
| Look-ahead bias        | Bailey et al. (2014)           |
| Multiple testing (DSR) | Bailey & López de Prado (2014) |
| Small sample inference | Lo (2002)                      |
