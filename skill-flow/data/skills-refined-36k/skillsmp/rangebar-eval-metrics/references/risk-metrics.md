# Risk Metrics for Range Bars

## Key Principle: Daily Aggregation First

For all risk metrics on range bars, **aggregate to daily before computation**:

```python
def _group_by_day(pnl: np.ndarray, timestamps: np.ndarray) -> np.ndarray:
    """Standard daily aggregation."""
    df = pd.DataFrame({"pnl": pnl, "ts": pd.to_datetime(timestamps, utc=True)})
    df["date"] = df["ts"].dt.date
    return df.groupby("date")["pnl"].sum().values
```

## VaR and CVaR (Expected Shortfall)

```python
def compute_var_cvar(
    pnl: np.ndarray,
    timestamps: np.ndarray,
    confidence: float = 0.95
) -> tuple[float, float]:
    """Value at Risk and Conditional VaR on daily-aggregated PnL.

    Args:
        pnl: Bar-level PnL
        timestamps: Bar timestamps
        confidence: Confidence level (0.95 = 95%)

    Returns:
        (VaR, CVaR) tuple
    """
    daily_pnl = _group_by_day(pnl, timestamps)

    alpha = 1 - confidence
    var = float(np.percentile(daily_pnl, alpha * 100))

    tail = daily_pnl[daily_pnl <= var]
    cvar = float(np.mean(tail)) if len(tail) > 0 else var

    return var, cvar
```

## Omega Ratio

```python
def compute_omega(
    pnl: np.ndarray,
    timestamps: np.ndarray,
    threshold: float = 0.0,
    min_days: int = 5
) -> float:
    """Omega ratio with daily aggregation.

    Omega = sum(gains above threshold) / sum(losses below threshold)

    Reference: Keating & Shadwick (2002)

    REMEDIATION (2026-01-19 audit):
    - Added min_days parameter to avoid unreliable values with too few samples.
    - Return NaN when n_days < min_days.

    Source: Multi-agent audit finding (robustness-analyst subagent)
    """
    daily_pnl = _group_by_day(pnl, timestamps)

    # REMEDIATION: Minimum sample size check
    if len(daily_pnl) < min_days:
        return float("nan")  # Unreliable with too few days

    excess = daily_pnl - threshold
    gains = excess[excess > 0].sum()
    losses = (-excess[excess < 0]).sum()

    if losses < 1e-10:
        return float("nan")  # No losses

    return float(gains / losses)
```

## Ulcer Index

**CRITICAL**: Uses equity curve, NOT cumsum of returns.

```python
def compute_ulcer_index(
    pnl: np.ndarray,
    timestamps: np.ndarray,
    initial_equity: float = 10000.0
) -> float:
    """Ulcer Index from equity curve.

    Ulcer = sqrt(mean(drawdown_pct^2))

    Reference: Peter Martin (1987)

    REMEDIATION (2026-01-19 audit):
    - Guard against division by zero when peak equity = 0.
    - Can happen if initial_equity + early losses < 0.

    Source: Multi-agent audit finding (risk-analyst subagent)
    """
    daily_pnl = _group_by_day(pnl, timestamps)

    # Build equity curve (NOT just cumsum)
    equity = initial_equity + np.cumsum(daily_pnl)

    # Percentage drawdowns from peak
    peak = np.maximum.accumulate(equity)

    # REMEDIATION: Guard against division by zero when peak = 0
    with np.errstate(divide='ignore', invalid='ignore'):
        drawdown_pct = np.where(peak > 1e-10, (equity - peak) / peak, 0.0)

    return float(np.sqrt((drawdown_pct ** 2).mean()))
```

## Sortino Ratio

Preferred over Sharpe for crypto (asymmetric returns):

```python
def compute_sortino(
    pnl: np.ndarray,
    timestamps: np.ndarray,
    mar: float = 0.0,  # Minimum Acceptable Return
    annualization: int = 365  # Crypto default
) -> float:
    """Sortino ratio using downside deviation only.

    Sortino = (Mean - MAR) / Downside Deviation

    Reference: Sortino & Price (1994)
    """
    daily_pnl = _group_by_day(pnl, timestamps)

    # Downside returns only
    downside = daily_pnl[daily_pnl < mar]
    if len(downside) == 0:
        return float("inf")  # No downside

    downside_std = np.std(downside, ddof=1)
    if downside_std < 1e-10:
        return float("nan")

    excess_return = np.mean(daily_pnl) - mar
    sortino = (excess_return / downside_std) * np.sqrt(annualization)

    return float(sortino)
```

## Max Drawdown and Recovery Factor

```python
def compute_max_drawdown(
    pnl: np.ndarray,
    timestamps: np.ndarray,
    initial_equity: float = 10000.0
) -> tuple[float, int]:
    """Max drawdown and duration.

    Returns:
        (max_dd_pct, duration_days)
    """
    daily_pnl = _group_by_day(pnl, timestamps)
    equity = initial_equity + np.cumsum(daily_pnl)

    peak = np.maximum.accumulate(equity)
    drawdown = (equity - peak) / peak

    max_dd = float(drawdown.min())

    # Duration: days from peak to recovery
    in_drawdown = drawdown < 0
    if not in_drawdown.any():
        return max_dd, 0

    # Find longest drawdown period
    changes = np.diff(in_drawdown.astype(int))
    starts = np.where(changes == 1)[0] + 1
    ends = np.where(changes == -1)[0] + 1

    if len(starts) == 0:
        starts = np.array([0]) if in_drawdown[0] else np.array([])
    if len(ends) == 0 or (len(starts) > 0 and ends[-1] < starts[-1]):
        ends = np.append(ends, len(drawdown))

    durations = ends[:len(starts)] - starts[:len(starts)]
    max_duration = int(durations.max()) if len(durations) > 0 else 0

    return max_dd, max_duration


def compute_recovery_factor(total_return: float, max_drawdown: float) -> float:
    """Recovery Factor = Total Return / |Max Drawdown|."""
    if abs(max_drawdown) < 1e-10:
        return float("nan")
    return float(total_return / abs(max_drawdown))
```

## Profit Factor

```python
def compute_profit_factor(
    pnl: np.ndarray,
    timestamps: np.ndarray,
    min_days: int = 5
) -> float:
    """Profit Factor with daily aggregation.

    PF = sum(winning days) / |sum(losing days)|

    REMEDIATION (2026-01-19 audit):
    - Added min_days parameter to avoid unreliable values with too few samples.
    - Return NaN when n_days < min_days.

    Source: Multi-agent audit finding (robustness-analyst subagent)
    """
    daily_pnl = _group_by_day(pnl, timestamps)

    # REMEDIATION: Minimum sample size check
    if len(daily_pnl) < min_days:
        return float("nan")  # Unreliable with too few days

    gains = daily_pnl[daily_pnl > 0].sum()
    losses = abs(daily_pnl[daily_pnl < 0].sum())

    if losses < 1e-10:
        return float("inf") if gains > 0 else 1.0

    return float(gains / losses)
```

## Academic References

```bibtex
@article{keating2002omega,
  title={An Introduction to Omega},
  author={Keating, Con and Shadwick, William F},
  journal={AIMA Newsletter},
  year={2002}
}

@article{martin1987ulcer,
  title={The Ulcer Index},
  author={Martin, Peter},
  journal={Technical Analysis of Stocks \& Commodities},
  year={1987}
}

@article{sortino1994performance,
  title={Performance Measurement in a Downside Risk Framework},
  author={Sortino, Frank A and Price, Lee N},
  journal={The Journal of Investing},
  year={1994}
}
```
