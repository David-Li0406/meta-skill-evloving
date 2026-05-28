# Temporal Aggregation for Range Bars

## Core Principle: UTC Day Boundaries

```python
def _group_by_day(pnl: np.ndarray, timestamps: np.ndarray) -> np.ndarray:
    """Canonical daily aggregation function.

    ALWAYS use this before computing Sharpe or risk metrics.
    """
    df = pd.DataFrame({
        "pnl": pnl,
        "ts": pd.to_datetime(timestamps, utc=True)  # EXPLICIT UTC
    })
    df["date"] = df["ts"].dt.date
    return df.groupby("date")["pnl"].sum().values
```

## Why UTC?

1. **Crypto standard**: Binance, CoinGecko, all major exchanges use UTC
2. **No DST issues**: UTC never changes
3. **Consistent aggregation**: Same day boundary globally

## Session Filter Interaction

**CRITICAL ORDER**: Filter THEN aggregate.

```python
def evaluate_with_filter(predictions, actuals, timestamps, session_filter=True):
    """Correct order: filter → aggregate → compute."""

    # Step 1: Apply session filter (if enabled)
    if session_filter:
        mask = compute_tradeable_mask(timestamps)
        predictions = predictions[mask]
        actuals = actuals[mask]
        timestamps = timestamps[mask]

    # Step 2: Now aggregate to daily
    pnl = predictions * actuals
    daily_pnl = _group_by_day(pnl, timestamps)

    # Step 3: Compute Sharpe on daily
    sharpe = np.mean(daily_pnl) / np.std(daily_pnl) * np.sqrt(7)

    return sharpe
```

## Dual-View Computation

Compute BOTH views independently:

```python
def compute_dual_view(predictions, actuals, timestamps):
    """Independent computation for each view."""

    pnl = predictions * actuals

    # View 1: All bars (no filter)
    all_bars_metrics = evaluate_fold(predictions, actuals, None, timestamps)

    # View 2: Session filtered (London-NY)
    mask = compute_tradeable_mask(timestamps)
    filtered_metrics = evaluate_fold(predictions, actuals, mask, timestamps)

    return {
        "oos_metrics": filtered_metrics,      # Primary (strategy evaluation)
        "oos_metrics_all": all_bars_metrics   # Diagnostic (regime detection)
    }
```

## Timezone Reference

```yaml
timezone_mapping:
  crypto_standard: "UTC"

  market_sessions:
    tokyo: "Asia/Tokyo" # UTC+9
    london: "Europe/London" # UTC+0 (winter) / UTC+1 (summer)
    new_york: "America/New_York" # UTC-5 (winter) / UTC-4 (summer)

  aggregation_rule:
    always_use: "UTC"
    never_use: "Local market timezone for aggregation"
```

## Multi-Day Bar Handling (Edge Case)

Very rare for range bars, but handle gracefully:

```python
def detect_multi_day_bars(timestamps: np.ndarray) -> dict:
    """Check for bars spanning multiple days.

    Only possible with very wide thresholds + low volatility.
    """
    df = pd.DataFrame({
        "ts": pd.to_datetime(timestamps, utc=True)
    })
    df["date"] = df["ts"].dt.date
    df["prev_date"] = df["date"].shift(1)

    # Bar duration in days
    df["duration_days"] = (df["ts"] - df["ts"].shift(1)).dt.total_seconds() / 86400

    multi_day = df[df["duration_days"] > 1]

    return {
        "n_multi_day": len(multi_day),
        "max_duration_days": float(df["duration_days"].max()),
        "has_multi_day": len(multi_day) > 0
    }
```

## Validation Checklist

```yaml
validation_checklist:
  - id: UTC_EXPLICIT
    check: "All pd.to_datetime() calls include utc=True"
    example: "pd.to_datetime(timestamps, utc=True)"

  - id: DAILY_BEFORE_SHARPE
    check: "Daily aggregation happens before Sharpe computation"
    rationale: "Raw bar-level Sharpe violates IID"

  - id: FILTER_THEN_AGGREGATE
    check: "Session filter applied before aggregation"
    order: "filter → aggregate → compute"

  - id: DUAL_VIEW_INDEPENDENT
    check: "Both views computed independently"
    not: "Filtering the all-bars view"

  - id: NO_LOCAL_TIMEZONE
    check: "No hardcoded local timezone assumptions"
    anti_pattern: "tz.localize(ts)"
```
