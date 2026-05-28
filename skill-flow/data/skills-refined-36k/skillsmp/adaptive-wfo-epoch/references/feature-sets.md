# Feature Sets for BiLSTM Training

Reference for standardized feature sets used in AWFES experiments. Documents the evolution from A_baseline (v1) to A_baseline_v2 with stationary features.

## Feature Set Evolution

| Version           | Features              | Scaler                 | Issues                                   |
| ----------------- | --------------------- | ---------------------- | ---------------------------------------- |
| A_baseline (v1)   | 4 raw features        | MixedScaler            | Non-stationary, lookahead bias in scaler |
| **A_baseline_v2** | 9 stationary features | TemporalScaler (no-op) | **Recommended**                          |

## A_baseline (v1) - Legacy 4 Features

**Status**: Deprecated - use A_baseline_v2 instead.

| Feature         | Type            | Range     | Scaler | Issues          |
| --------------- | --------------- | --------- | ------ | --------------- |
| `returns`       | Raw returns     | Unbounded | MinMax | Non-stationary  |
| `momentum_20`   | 20-bar momentum | Unbounded | Robust | Heavy tails     |
| `atr_14`        | 14-bar ATR      | Unbounded | Robust | Scale-dependent |
| `volume_change` | Vol vs MA       | Unbounded | Robust | Heavy tails     |

**Known Issues**:

- Non-stationary features create distribution shift across folds
- MixedScaler fit can leak information if not carefully applied
- Heavy tails cause gradient instability in LSTM training
- Scale-dependent features don't transfer across assets

## A_baseline_v2 - Stationary Features (RECOMMENDED)

**Status**: Current standard for AWFES experiments.

| Feature         | Type                     | Range   | Transform                        | Purpose                     |
| --------------- | ------------------------ | ------- | -------------------------------- | --------------------------- |
| `returns_vs`    | Vol-standardized returns | [-4, 4] | `ret / rolling_vol(20)`          | Removes volatility clusters |
| `momentum_z`    | Z-scored momentum        | [-4, 4] | `zscore(momentum, 100)`          | Bounded, comparable         |
| `atr_pct`       | ATR as % of price        | [-4, 4] | `atr / close * 100`              | Scale-invariant             |
| `volume_z`      | Log volume z-score       | [-4, 4] | `zscore(log(vol/ma_vol))`        | Heavy-tail handling         |
| `rsi_14`        | RSI normalized           | [0, 1]  | `rsi / 100`                      | Bounded momentum regime     |
| `bb_pct_b`      | Bollinger %B             | [0, 1]  | `(close - bb_lower) / bb_range`  | Mean-reversion signal       |
| `vol_regime`    | Binary high/low vol      | {0, 1}  | `atr > median(atr, 100)`         | Regime context              |
| `return_accel`  | Return acceleration      | [-4, 4] | `zscore(ret_5 - ret_10)`         | Momentum change detection   |
| `pv_divergence` | Price-vol correlation    | [-4, 4] | `zscore(rolling_corr(ret, vol))` | Exhaustion detection        |

### Why v2 Features Are Better

1. **Pre-transformed stationarity**: All features bounded and normalized before training
2. **No scaler lookahead**: TemporalScaler is a no-op since features already normalized
3. **Rolling z-score**: 100-bar window prevents information leakage
4. **Better gradient flow**: Bounded ranges prevent exploding/vanishing gradients
5. **Cross-asset transferability**: Scale-invariant features work across different price levels

### Computation Example

```python
def compute_stationary_features(df: pd.DataFrame, zscore_window: int = 100) -> pd.DataFrame:
    """Compute A_baseline_v2 stationary features.

    All features are pre-transformed to be stationary with bounded ranges.
    Uses rolling z-score normalization to prevent lookahead bias.
    """
    # Helper for rolling z-score with clipping
    def rolling_zscore(series: pd.Series, window: int = zscore_window) -> pd.Series:
        mean = series.rolling(window, min_periods=20).mean()
        std = series.rolling(window, min_periods=20).std()
        z = (series - mean) / (std + 1e-8)
        return z.clip(-4, 4)  # Bound to [-4, 4]

    # Raw intermediate calculations
    returns = df["close"].pct_change()
    rolling_vol = returns.rolling(20).std()
    momentum_20 = df["close"].pct_change(20)
    atr_14 = compute_atr(df, 14)  # Your ATR implementation
    volume_ma = df["volume"].rolling(20).mean()
    rsi_14 = compute_rsi(df["close"], 14)  # Your RSI implementation

    # Bollinger Bands
    bb_mid = df["close"].rolling(20).mean()
    bb_std = df["close"].rolling(20).std()
    bb_upper = bb_mid + 2 * bb_std
    bb_lower = bb_mid - 2 * bb_std

    # Stationary features
    df["returns_vs"] = (returns / (rolling_vol + 1e-8)).clip(-4, 4)
    df["momentum_z"] = rolling_zscore(momentum_20)
    df["atr_pct"] = rolling_zscore(atr_14 / df["close"] * 100)
    df["volume_z"] = rolling_zscore(np.log(df["volume"] / (volume_ma + 1)))
    df["rsi_14"] = rsi_14 / 100  # Already bounded [0, 1]
    df["bb_pct_b"] = ((df["close"] - bb_lower) / (bb_upper - bb_lower + 1e-8)).clip(0, 1)
    df["vol_regime"] = (atr_14 > atr_14.rolling(100).median()).astype(float)
    df["return_accel"] = rolling_zscore(returns.rolling(5).mean() - returns.rolling(10).mean())
    df["pv_divergence"] = rolling_zscore(
        returns.rolling(20).corr(df["volume"].pct_change())
    )

    return df


A_BASELINE_V2_FEATURES = [
    "returns_vs",
    "momentum_z",
    "atr_pct",
    "volume_z",
    "rsi_14",
    "bb_pct_b",
    "vol_regime",
    "return_accel",
    "pv_divergence",
]
```

## TemporalScaler (No-Op Scaler)

For A_baseline_v2 features, use `TemporalScaler` which is a no-op:

```python
class TemporalScaler:
    """No-op scaler for pre-transformed stationary features.

    Features in A_baseline_v2 are already:
    - Z-score normalized with rolling windows
    - Clipped to bounded ranges
    - Stationary by construction

    This scaler exists to maintain API compatibility with pipelines
    that expect a scaler object.
    """

    def fit(self, X: np.ndarray) -> "TemporalScaler":
        return self  # No-op

    def transform(self, X: np.ndarray) -> np.ndarray:
        return X  # Pass-through

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return X  # Pass-through

    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        return X  # Pass-through
```

## Automatic Scaler Selection

```python
def create_sequences_with_scaler(
    df: pd.DataFrame,
    features: list[str],
    target: str,
    seq_len: int,
) -> tuple[np.ndarray, np.ndarray, Any, np.ndarray]:
    """Create sequences with automatic scaler selection.

    If features are a subset of A_BASELINE_V2_FEATURES, uses TemporalScaler.
    Otherwise, uses MixedScaler (legacy behavior).
    """
    if set(features).issubset(set(A_BASELINE_V2_FEATURES)):
        scaler = TemporalScaler()
    else:
        scaler = MixedScaler(features)

    # ... rest of sequence creation
    return X, y, scaler, timestamps
```

## Migration Guide: v1 to v2

### Before (v1)

```python
from features import compute_features, A_BASELINE_FEATURES
from scalers import MixedScaler

df = compute_features(df)
features = A_BASELINE_FEATURES  # ['returns', 'momentum_20', 'atr_14', 'volume_change']

scaler = MixedScaler(features)
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### After (v2)

```python
from features import compute_stationary_features, A_BASELINE_V2_FEATURES
from scalers import TemporalScaler

df = compute_stationary_features(df)
features = A_BASELINE_V2_FEATURES  # 9 stationary features

scaler = TemporalScaler()  # No-op, features already normalized
X_train_scaled = scaler.fit_transform(X_train)  # Pass-through
X_test_scaled = scaler.transform(X_test)  # Pass-through
```

## Validation Checklist

Before using a feature set in AWFES:

- [ ] All features bounded (no unbounded ranges)
- [ ] Stationarity test passes (ADF p < 0.05)
- [ ] No lookahead in feature computation (rolling windows only)
- [ ] Scaler fit on train only (or no scaler needed for v2)
- [ ] Feature correlation < 0.95 (no redundant features)
- [ ] Missing values handled (forward-fill or drop)

## References

- [rangebar-eval-metrics](../../rangebar-eval-metrics/SKILL.md) - Metric computation
- [look-ahead-bias.md](./look-ahead-bias.md) - Bias prevention
- [anti-patterns.md](./anti-patterns.md) - Common mistakes
