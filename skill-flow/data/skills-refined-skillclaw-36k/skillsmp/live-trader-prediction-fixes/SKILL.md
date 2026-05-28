---
name: live-trader-prediction-fixes
description: "Fix live trader prediction issues: zeros returned, excessive data fetching, insufficient bars. Trigger when predictions show all zeros, excessive API calls, or Markov features show uniform priors."
author: Claude Code
date: 2026-01-26
---

# Live Trader Prediction Fixes (v3.6.1)

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-26 |
| **Goal** | Fix live trader returning all-zero predictions and continuously fetching thousands of bars |
| **Environment** | Python 3.10, alpaca_trading v3.6.0 |
| **Status** | Success |

## Context

The live trader exhibited three interconnected issues:
1. All predictions returned `signal=0, confidence=0.0` for most symbols
2. The trader continuously fetched 8000+ bars on every update cycle
3. Some symbols showed confidence values but still returned signal=0 (HOLD)

### Symptoms in gate_status.json
```json
{
  "CMF": { "signal": 0, "confidence": 0.0, "final_status": "HOLD" },
  "LXP": { "signal": 0, "confidence": 0.0, "final_status": "HOLD" },
  "PFE": { "signal": 0, "confidence": 0.549, "final_status": "HOLD" }
}
```

Most symbols had `confidence=0.0`, indicating predictions were failing early and returning neutral results.

## Root Causes

### Issue 1: Markov State Not Persisted

In `MultiTimeframePricePredictor._get_rl_prediction()`, a **new** `InferenceObservationBuilder` was created on every prediction call:

```python
# WRONG - creates new builder each call, resets Markov state
obs_builder = InferenceObservationBuilder(
    window=window,
    use_gpu_markov=True,
    target_features=target_features
)
```

This reset the Markov chains to uniform priors `[0.33, 0.34, 0.33]` on every call, making the Markov regime features useless for prediction.

### Issue 2: Excessive Data Fetching

In `DataFetcher.get_latest_bars()`, the lookback was calculated as:

```python
# WRONG - doesn't account for weekends/holidays
delta = _timeframe_to_timedelta(timeframe) * (count * 2)  # count * 2 is naive
```

For `count=8000` 1-minute bars, this requested 16,000 minutes (~11 days) of data, but:
- Stocks only trade 6.5 hours/day (390 minutes)
- 8000 1-minute trading bars actually span ~30+ calendar days
- The 2x multiplier was both arbitrary and insufficient

### Issue 3: Insufficient Hourly Bars

The prediction pipeline required 120 hourly bars (100 window + 20 buffer), but:
- `max_bars=8000` for 1-minute data only produced ~133 hourly bars when resampled
- This was borderline and could fail if any data was missing
- The fallback hourly fetch used `lookback_days=15`, which only yields ~97 hourly bars for stocks

## Verified Solutions

### Fix 1: Persist Markov State Across Calls

Store `InferenceObservationBuilder` instances and reuse them:

```python
# In MultiTimeframePricePredictor.__init__
self._obs_builders: Dict[str, any] = {}  # Stateful builders per timeframe

# In _get_rl_prediction - reuse existing builder
builder_key = f"{timeframe}_{target_features}"
if builder_key not in self._obs_builders:
    logger.info(f"Creating InferenceObservationBuilder for {timeframe}")
    self._obs_builders[builder_key] = InferenceObservationBuilder(
        window=window,
        use_gpu_markov=True,
        target_features=target_features
    )

obs_builder = self._obs_builders[builder_key]  # Reuse!
obs = obs_builder.build(prices=prices, high=high, low=low)
```

**Key insight**: The Markov chains need to see historical price evolution to produce meaningful regime probabilities. Resetting them each call defeats their purpose.

### Fix 2: Intelligent Lookback Calculation

Replace naive `count * 2` with market-aware calculation:

```python
def get_latest_bars(self, symbol, count=750, timeframe="1Min"):
    tf_delta = _timeframe_to_timedelta(timeframe)
    tf_minutes = tf_delta.total_seconds() / 60

    if tf_minutes < 60:  # Intraday
        # Stocks trade ~390 minutes/day (6.5 hours)
        trading_days_needed = max(1, count / 390)
        calendar_days = trading_days_needed * 1.5  # 7/5 = 1.4, plus buffer
        calendar_days = max(calendar_days, 5)  # Minimum 5 days
        delta = timedelta(days=calendar_days)
    elif tf_minutes < 1440:  # Hourly
        trading_days_needed = max(1, count / 6.5)
        calendar_days = trading_days_needed * 1.5 + 2
        delta = timedelta(days=calendar_days)
    else:  # Daily or weekly
        calendar_days = count * 1.5 + 5
        delta = timedelta(days=calendar_days)
```

### Fix 3: Increase Data Buffers

In `scripts/live_trader.py`:
```python
# Before
max_bars = 8000  # ~133 hourly bars when resampled

# After
max_bars = 12000  # ~200 hourly bars when resampled
```

In `multi_tf_predictor.py` fallback fetch:
```python
# Before
lookback_days = 15  # Only ~97 hourly bars for stocks

# After
lookback_days = 40  # ~260 hourly bars for stocks
```

## Failed Attempts

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Just increase max_bars | Didn't fix zero confidence - Markov state was still resetting | Data quantity isn't the issue if state isn't persisted |
| Add logging without fixing | Confirmed zeros but didn't solve it | Good for diagnosis, but need to fix root cause |
| Using `build_inference_observation()` function | This is stateless - defaults to uniform priors | Must use `InferenceObservationBuilder` class for stateful inference |

## Verification

After applying fixes, predictions show real values:
```
2026-01-26 10:28:21,957 [INFO] CMF: Prediction: dir=0, mag=0.00%, conf=0.547, size=50%, regime=elevated
2026-01-26 10:28:22,479 [INFO] VERX: Prediction: dir=1, mag=0.60%, conf=0.427, size=50%, regime=high
```

Key indicators of success:
- Non-zero confidence values (0.427, 0.547)
- Direction predictions (VERX shows dir=1 for LONG)
- Markov-derived regime labels (elevated, high)

## Files Modified

```
alpaca_trading/data/fetcher.py:
  - get_latest_bars(): Intelligent lookback calculation

alpaca_trading/prediction/multi_tf_predictor.py:
  - __init__(): Added self._obs_builders dict
  - _get_rl_prediction(): Reuse builders per timeframe
  - predict(): Increased fallback lookback_days from 15 to 40

scripts/live_trader.py:
  - update_bars(): Increased max_bars from 8000 to 12000
  - Warmup section: Added detailed logging
```

## Key Insights

1. **Stateful vs Stateless Inference**: The standalone `build_inference_observation()` function is for single-shot inference where Markov state is passed externally. The `InferenceObservationBuilder` class is for stateful inference where Markov state evolves.

2. **Market Hours Matter**: Any lookback calculation for trading data must account for:
   - Trading hours (6.5 hours/day for US stocks)
   - Weekends (5 trading days / 7 calendar days)
   - Holidays (add buffer)

3. **Borderline Isn't Good Enough**: If you need 120 bars minimum, don't fetch 133. Fetch 200+ to handle edge cases.

4. **Confidence vs Direction**: A symbol can have non-zero confidence but still predict HOLD (dir=0). This is valid - it means the model is confident about staying neutral.

## Related Skills

- `markov-regime-features`: Original diagnosis of Markov uniform prior issue
- `persistent-cache-gap-filling`: Data caching strategy leveraged by this fix
- `data-source-priority`: Data fetching hierarchy

## References

- `alpaca_trading/gpu/inference_obs_builder.py`: InferenceObservationBuilder class
- `alpaca_trading/prediction/multi_tf_predictor.py`: MultiTimeframePricePredictor
- `scripts/live_trader.py`: Live trading loop
