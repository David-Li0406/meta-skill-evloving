# Crypto Market Considerations

## Annualization: sqrt(7) and sqrt(365)

**CRITICAL**: Crypto trades 24/7, 365 days/year.

```python
# CORRECT for crypto
DAYS_PER_WEEK_CRYPTO = 7
DAYS_PER_YEAR_CRYPTO = 365

weekly_sharpe = daily_sharpe * np.sqrt(DAYS_PER_WEEK_CRYPTO)  # sqrt(7) = 2.65
annual_sharpe = daily_sharpe * np.sqrt(DAYS_PER_YEAR_CRYPTO)  # sqrt(365) = 19.1

# WRONG for crypto (equity assumptions)
# weekly_sharpe = daily_sharpe * np.sqrt(5)  # DON'T DO THIS
# annual_sharpe = daily_sharpe * np.sqrt(252)  # DON'T DO THIS
```

## Session Definitions (UTC)

```yaml
sessions:
  asia:
    start: "00:00"
    end: "08:00"
    characteristics: "Lower volume, mean-reversion tendency"

  europe:
    start: "08:00"
    end: "16:00"
    characteristics: "Increasing volume, momentum starts"

  americas:
    start: "14:00"
    end: "22:00"
    characteristics: "Highest volume, trend continuation"

  london_ny_overlap:
    start: "14:00"
    end: "16:00"
    characteristics: "Peak liquidity, best for execution"

  overnight:
    start: "22:00"
    end: "08:00"
    characteristics: "Lowest liquidity, higher spreads"
```

## Session Filter Implementation

**CRITICAL: Use `zoneinfo.ZoneInfo` for DST-aware timezone handling.**

Python's `zoneinfo` module (stdlib since 3.9) uses the IANA timezone database and
automatically handles Daylight Saving Time transitions for both London (GMT/BST)
and New York (EST/EDT).

### DST Transition Handling

London and New York have different DST transition dates:

- **UK**: Last Sunday of March (forward), Last Sunday of October (back)
- **US**: 2nd Sunday of March (forward), 1st Sunday of November (back)

This creates 2-3 week gaps where one region is in DST and the other isn't.
`ZoneInfo` handles this automatically:

| Period                            | London | NY  | Session Start (UTC) | Session End (UTC) |
| --------------------------------- | ------ | --- | ------------------- | ----------------- |
| Winter (both standard)            | GMT    | EST | 08:00               | 21:00             |
| Spring gap (UK summer, US winter) | GMT    | EDT | 08:00               | 20:00             |
| Summer (both DST)                 | BST    | EDT | 07:00               | 20:00             |
| Fall gap (UK winter, US summer)   | GMT    | EDT | 08:00               | 20:00             |

```python
from datetime import datetime, time
from zoneinfo import ZoneInfo
import pandas as pd

# CORRECT: Use ZoneInfo for DST-aware handling
LONDON_TZ = ZoneInfo("Europe/London")   # GMT (winter) / BST (summer)
NY_TZ = ZoneInfo("America/New_York")    # EST (winter) / EDT (summer)

LONDON_OPEN = time(8, 0)   # 8:00 AM London local
NY_CLOSE = time(16, 0)     # 4:00 PM NY local


def get_session_bounds_utc(date) -> tuple[pd.Timestamp, pd.Timestamp]:
    """Get London open to NY close in UTC for a given date.

    DST is handled automatically by ZoneInfo.
    """
    london_open = pd.Timestamp(
        datetime.combine(date, LONDON_OPEN), tz=LONDON_TZ
    ).tz_convert("UTC")

    ny_close = pd.Timestamp(
        datetime.combine(date, NY_CLOSE), tz=NY_TZ
    ).tz_convert("UTC")

    return london_open, ny_close


def is_tradeable_bar(bar_close_ts: pd.Timestamp) -> bool:
    """Check if bar falls within London-NY session.

    Uses bar close timestamp for session membership.
    """
    if bar_close_ts.tzinfo is None:
        bar_close_ts = bar_close_ts.tz_localize("UTC")

    ts_london = bar_close_ts.tz_convert(LONDON_TZ)
    weekday = ts_london.weekday()

    # Skip weekends
    if weekday >= 5:
        return False

    session_open, session_close = get_session_bounds_utc(ts_london.date())
    return session_open <= bar_close_ts <= session_close


def compute_tradeable_mask(timestamps: np.ndarray) -> np.ndarray:
    """Boolean mask for tradeable bars."""
    return np.array([
        is_tradeable_bar(pd.Timestamp(ts))
        for ts in timestamps
    ])
```

### Anti-Patterns (DO NOT USE)

```python
# WRONG: Using fixed UTC offsets (ignores DST)
# london_open_utc = datetime(..., hour=8) - timedelta(hours=0)  # WRONG!

# WRONG: Using pytz without localize() (deprecated)
# import pytz
# tz = pytz.timezone("Europe/London")
# ts = datetime(..., tzinfo=tz)  # WRONG! Use tz.localize() instead

# WRONG: Hardcoded session hours in UTC
# SESSION_START_UTC = 8  # WRONG! Varies with DST
# SESSION_END_UTC = 21   # WRONG! Varies with DST
```

## Weekend/Weekday Split

Research shows distinct characteristics:

```python
def compute_weekend_weekday_split(
    pnl: np.ndarray,
    timestamps: np.ndarray
) -> dict:
    """Separate metrics for weekends vs weekdays.

    Empirical findings (Bitcoin 2014-2024):
    - Weekend volume: 60-70% of weekday
    - Weekend volatility: Lower
    - Weekend momentum: Higher returns (Monday effect)
    """
    df = pd.DataFrame({
        "pnl": pnl,
        "ts": pd.to_datetime(timestamps, utc=True)
    })
    df["is_weekend"] = df["ts"].dt.dayofweek >= 5

    weekday_pnl = df[~df["is_weekend"]]["pnl"].values
    weekend_pnl = df[df["is_weekend"]]["pnl"].values

    def safe_sharpe(arr):
        if len(arr) < 2 or np.std(arr) < 1e-10:
            return 0.0
        return float(np.mean(arr) / np.std(arr))

    return {
        "sharpe_weekday": safe_sharpe(weekday_pnl),
        "sharpe_weekend": safe_sharpe(weekend_pnl),
        "n_weekday_bars": len(weekday_pnl),
        "n_weekend_bars": len(weekend_pnl),
        "pnl_frac_weekend": (
            weekend_pnl.sum() / (weekday_pnl.sum() + weekend_pnl.sum())
            if (weekday_pnl.sum() + weekend_pnl.sum()) != 0 else 0.0
        )
    }
```

## Funding Rate Exposure

For perpetual futures strategies:

```python
def estimate_funding_impact(
    positions: np.ndarray,
    timestamps: np.ndarray,
    avg_funding_rate_8h: float = 0.0001  # 1 bp per 8h
) -> float:
    """Estimate funding cost/income for perpetuals.

    Funding settles every 8 hours (00:00, 08:00, 16:00 UTC).
    Long pays short when rate > 0.

    Args:
        positions: Position sizes (positive = long)
        timestamps: Position timestamps
        avg_funding_rate_8h: Average 8h funding rate (positive = longs pay)

    Returns:
        Total funding PnL (negative = cost)
    """
    df = pd.DataFrame({
        "position": positions,
        "ts": pd.to_datetime(timestamps, utc=True)
    })

    # Funding times
    df["hour"] = df["ts"].dt.hour
    df["is_funding"] = df["hour"].isin([0, 8, 16])

    # Funding impact: -position * rate (longs pay when rate > 0)
    funding_events = df[df["is_funding"]]
    total_funding = -(funding_events["position"] * avg_funding_rate_8h).sum()

    return float(total_funding)
```

## UTC Day Boundaries

```python
def group_by_utc_day(
    pnl: np.ndarray,
    timestamps: np.ndarray
) -> pd.DataFrame:
    """Group by UTC calendar day.

    CRITICAL: Always use UTC for crypto aggregation.
    """
    df = pd.DataFrame({
        "pnl": pnl,
        "ts": pd.to_datetime(timestamps, utc=True)  # Explicit UTC
    })
    df["date"] = df["ts"].dt.date

    return df.groupby("date").agg({
        "pnl": "sum",
        "ts": "count"  # Bar count per day
    }).rename(columns={"ts": "n_bars"})
```

## Dual-View Evaluation

For comprehensive analysis:

```yaml
dual_view:
  session_filtered:
    purpose: "Strategy performance evaluation"
    filter: "London 08:00 to NY 16:00, weekdays only"
    annualization: "sqrt(5) - 5 trading days per week"
    use_for:
      - "Primary Sharpe calculation"
      - "Risk metrics"
      - "Go/no-go decisions"

  all_bars:
    purpose: "Regime detection and data quality"
    filter: "None (all bars)"
    annualization: "sqrt(7) - crypto trades 24/7"
    use_for:
      - "Bar count stability diagnostic"
      - "Weekend/weekday comparison"
      - "Volatility regime detection"
```

## CRITICAL: Session-Specific Annualization

**THIS IS THE MOST IMPORTANT DISTINCTION FOR CRYPTO RANGE BARS.**

| View                 | Filter              | days_per_week | Weekly Sharpe            | Rationale                  |
| -------------------- | ------------------- | ------------- | ------------------------ | -------------------------- |
| **Session-filtered** | London-NY, weekdays | **5**         | `daily_sharpe * sqrt(5)` | Only 5 active trading days |
| **All-bars**         | None                | **7**         | `daily_sharpe * sqrt(7)` | Crypto trades 24/7/365     |

```python
# CORRECT dual-view implementation
def compute_dual_view_metrics(
    predictions: np.ndarray,
    actuals: np.ndarray,
    timestamps: np.ndarray
) -> dict:
    """Compute metrics with CORRECT annualization for each view."""

    # All bars view - sqrt(7) because crypto is 24/7
    all_bars = evaluate_fold(
        predictions, actuals, None, timestamps,
        days_per_week=7  # CRITICAL: 7 for all-bars
    )

    # Session-filtered view - sqrt(5) because we filter to 5 trading days
    mask = compute_tradeable_mask(timestamps)
    filtered = evaluate_fold(
        predictions, actuals, mask, timestamps,
        days_per_week=5  # CRITICAL: 5 for session-filtered
    )

    return {
        "oos_metrics": filtered,      # Primary (sqrt(5))
        "oos_metrics_all": all_bars   # Diagnostic (sqrt(7))
    }


# WRONG - using same annualization for both views
# filtered = evaluate_fold(..., days_per_week=7)  # INCORRECT!
```

### Why This Matters

1. **Session-filtered uses sqrt(5)**: When you filter to London-NY weekday hours, you're
   effectively trading a 5-day week like equities. The variance scaling must match.

2. **All-bars uses sqrt(7)**: The full 24/7 crypto dataset has 7 trading days worth
   of data per week, so annualization must use sqrt(7).

3. **Mixing them is a methodological error**: Using sqrt(7) for session-filtered
   **overstates** the Sharpe ratio by ~18% (`sqrt(7)/sqrt(5) = 1.183`).

```python
# Example of the overstatement
daily_sharpe = 0.1

correct_filtered = daily_sharpe * np.sqrt(5)   # 0.224
incorrect_filtered = daily_sharpe * np.sqrt(7)  # 0.265

overstatement = incorrect_filtered / correct_filtered  # 1.183 = 18.3% overstatement!
```
