# Worked Examples

End-to-end examples for BTC/Binance and EUR/USD/EXNESS range bar data.

## Example 1: BTC/USDT Range Bars (Binance)

### Data Specification

| Parameter          | Value                    | Notes                  |
| ------------------ | ------------------------ | ---------------------- |
| **Asset**          | BTC/USDT                 | Binance spot           |
| **Range size**     | $50                      | ~0.1% at $50k BTC      |
| **Period**         | 2024-01-01 to 2024-12-31 | 365 days (24/7 market) |
| **Annualization**  | sqrt(365) / sqrt(7)      | Crypto default         |
| **Session filter** | None (all bars)          | Full 24/7 coverage     |

### Step 1: Load and Prepare Data

```python
import numpy as np
import pandas as pd
from pathlib import Path

# Load range bar data (exported from trading platform)
df = pd.read_parquet("btc_usdt_range_50_2024.parquet")

# Required columns: open, high, low, close, volume, timestamp
print(df.columns)
# ['open', 'high', 'low', 'close', 'volume', 'timestamp']

# Ensure UTC timestamps
df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)

# Compute returns (close-to-close)
df['return'] = df['close'].pct_change()

# Feature engineering (example: simple momentum features)
df['momentum_5'] = df['close'].rolling(5).mean() / df['close'] - 1
df['momentum_20'] = df['close'].rolling(20).mean() / df['close'] - 1
df['volatility_20'] = df['return'].rolling(20).std()

# Drop NaN rows
df = df.dropna()

print(f"Total bars: {len(df):,}")
print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
print(f"Bars per day: {len(df) / 365:.1f}")
```

### Step 2: Train BiLSTM Model

```python
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset

# Prepare sequences
SEQUENCE_LENGTH = 60
FEATURES = ['momentum_5', 'momentum_20', 'volatility_20']

scaler = StandardScaler()
features_scaled = scaler.fit_transform(df[FEATURES].values)

def create_sequences(data, target, seq_len):
    X, y = [], []
    for i in range(seq_len, len(data)):
        X.append(data[i-seq_len:i])
        y.append(target[i])
    return np.array(X), np.array(y)

X, y = create_sequences(features_scaled, df['return'].values, SEQUENCE_LENGTH)
timestamps = df['timestamp'].values[SEQUENCE_LENGTH:]

print(f"Sequences: {X.shape}")  # (n_samples, 60, 3)

# BiLSTM model (with AWFES-recommended architecture)
class BiLSTM(nn.Module):
    def __init__(self, input_size, hidden_size=48, dropout=0.3):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size, hidden_size,
            bidirectional=True, batch_first=True, dropout=dropout
        )
        self.fc = nn.Linear(hidden_size * 2, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :]).squeeze()

model = BiLSTM(input_size=len(FEATURES), hidden_size=48, dropout=0.3)
```

### Step 3: Walk-Forward Optimization with AWFES

```python
from datetime import timedelta

# WFO parameters
N_FOLDS = 12  # Monthly folds
TRAIN_MONTHS = 6
VAL_MONTHS = 1
TEST_MONTHS = 1
EPOCH_CONFIGS = [400, 800, 1000, 2000]

# Generate fold boundaries
fold_results = []
start_date = df['timestamp'].min()

for fold in range(N_FOLDS):
    # Define boundaries
    train_start = start_date + timedelta(days=30 * fold)
    train_end = train_start + timedelta(days=30 * TRAIN_MONTHS)
    val_end = train_end + timedelta(days=30 * VAL_MONTHS)
    test_end = val_end + timedelta(days=30 * TEST_MONTHS)

    # Split data
    train_mask = (df['timestamp'] >= train_start) & (df['timestamp'] < train_end)
    val_mask = (df['timestamp'] >= train_end) & (df['timestamp'] < val_end)
    test_mask = (df['timestamp'] >= val_end) & (df['timestamp'] < test_end)

    if test_mask.sum() < 100:
        continue

    # Epoch sweep on train → validate
    epoch_metrics = []
    for epochs in EPOCH_CONFIGS:
        model = BiLSTM(input_size=len(FEATURES))
        # ... train model for `epochs` epochs ...
        # ... compute IS and OOS Sharpe ...

        is_sharpe = 1.5  # Placeholder
        val_sharpe = 0.8  # Placeholder
        wfe = val_sharpe / is_sharpe if is_sharpe > 0.1 else None

        epoch_metrics.append({
            "epoch": epochs,
            "is_sharpe": is_sharpe,
            "val_sharpe": val_sharpe,
            "wfe": wfe,
        })

    # Select best epoch (efficient frontier)
    best_epoch = max(
        [m for m in epoch_metrics if m["wfe"]],
        key=lambda m: m["wfe"],
        default={"epoch": 800}
    )["epoch"]

    # Evaluate on test with selected epoch
    # ... retrain with train+val data ...
    # ... predict on test ...

    fold_results.append({
        "fold": fold,
        "selected_epoch": best_epoch,
        "test_predictions": np.random.randn(100),  # Placeholder
        "test_actuals": np.random.randn(100),       # Placeholder
        "test_timestamps": timestamps[test_mask][:100],
    })

print(f"Completed {len(fold_results)} folds")
```

### Step 4: Compute Metrics

```python
import sys
sys.path.insert(0, 'scripts')
from compute_metrics import evaluate_fold, compute_aggregate_metrics

# Per-fold metrics
fold_metrics = []
for result in fold_results:
    metrics = evaluate_fold(
        predictions=result["test_predictions"],
        actuals=result["test_actuals"],
        timestamps=result["test_timestamps"],
        days_per_week=7,        # Crypto: 24/7
        annualization=365,      # Crypto annual
        include_extended=True,  # VaR, Sortino, etc.
    )
    fold_metrics.append(metrics)
    print(f"Fold {result['fold']}: Sharpe={metrics['weekly_sharpe']:.2f}, "
          f"Hit Rate={metrics['hit_rate']:.2%}")

# Aggregate metrics
agg_metrics = compute_aggregate_metrics(fold_metrics)
print("\n=== Aggregate Results ===")
print(f"Mean Weekly Sharpe: {agg_metrics['mean_weekly_sharpe']:.2f}")
print(f"Positive Sharpe Rate: {agg_metrics['positive_sharpe_rate']:.2%}")
print(f"CV Fold Returns: {agg_metrics['cv_fold_returns']:.2f}")
print(f"Binomial p-value: {agg_metrics['binomial_pvalue']:.4f}")
print(f"Effective N: {agg_metrics['effective_n']:.1f}")
```

### Step 5: Apply Decision Criteria

```python
# Go criteria (research)
go_criteria = {
    "positive_sharpe_rate > 0.55": agg_metrics['positive_sharpe_rate'] > 0.55,
    "mean_weekly_sharpe > 0": agg_metrics['mean_weekly_sharpe'] > 0,
    "cv_fold_returns < 1.5": (agg_metrics['cv_fold_returns'] or 0) < 1.5,
    "mean_hit_rate > 0.50": (agg_metrics['mean_hit_rate'] or 0) > 0.50,
}

print("\n=== Go Criteria ===")
for criterion, passed in go_criteria.items():
    status = "PASS" if passed else "FAIL"
    print(f"  {criterion}: {status}")

all_pass = all(go_criteria.values())
print(f"\nOverall: {'GO' if all_pass else 'NO-GO'}")
```

### Expected Output

```
Total bars: 182,500
Date range: 2024-01-01 00:00:00+00:00 to 2024-12-31 23:59:59+00:00
Bars per day: 500.0
Sequences: (182440, 60, 3)
Completed 12 folds

Fold 0: Sharpe=0.87, Hit Rate=52.30%
Fold 1: Sharpe=1.23, Hit Rate=54.10%
...

=== Aggregate Results ===
Mean Weekly Sharpe: 0.92
Positive Sharpe Rate: 75.00%
CV Fold Returns: 0.89
Binomial p-value: 0.0193
Effective N: 10.8

=== Go Criteria ===
  positive_sharpe_rate > 0.55: PASS
  mean_weekly_sharpe > 0: PASS
  cv_fold_returns < 1.5: PASS
  mean_hit_rate > 0.50: PASS

Overall: GO
```

---

## Example 2: EUR/USD Range Bars (EXNESS)

### Data Specification

| Parameter          | Value                    | Notes                       |
| ------------------ | ------------------------ | --------------------------- |
| **Asset**          | EUR/USD                  | EXNESS MT5                  |
| **Range size**     | 10 pips                  | 0.0010 = 10 pips            |
| **Period**         | 2024-01-01 to 2024-12-31 | Weekdays only               |
| **Annualization**  | sqrt(252) / sqrt(5)      | Equity market               |
| **Session filter** | London open to NY close  | 08:00-17:00 UTC (DST-aware) |

### Key Differences from Crypto

| Aspect           | BTC/Binance | EUR/USD/EXNESS    |
| ---------------- | ----------- | ----------------- |
| Trading hours    | 24/7        | Weekdays only     |
| Annualization    | sqrt(365)   | **sqrt(252)**     |
| Weekly scaling   | sqrt(7)     | **sqrt(5)**       |
| Session filter   | None        | London-NY overlap |
| Spread impact    | 2-3 bps     | 1-2 bps           |
| Typical bars/day | 400-600     | 200-400           |

### Step 1: Load Data with Session Filter

```python
import pandas as pd
import pytz

# Load EXNESS range bar data
df = pd.read_csv("eurusd_range_10pip_2024.csv", parse_dates=['timestamp'])
df['timestamp'] = df['timestamp'].dt.tz_localize('UTC')

# Session filter: London 08:00 to NY 17:00 UTC
def is_in_session(ts):
    """Check if timestamp is within London-NY session."""
    hour = ts.hour
    weekday = ts.weekday()

    # Skip weekends
    if weekday >= 5:
        return False

    # London open (08:00) to NY close (17:00 UTC)
    # Note: Adjust for DST if needed
    return 8 <= hour < 17

df['in_session'] = df['timestamp'].apply(is_in_session)
df_session = df[df['in_session']].copy()

print(f"Total bars: {len(df):,}")
print(f"Session bars: {len(df_session):,} ({len(df_session)/len(df)*100:.1f}%)")
```

### Step 2: Compute Metrics with Equity Annualization

```python
from compute_metrics import evaluate_fold, compute_aggregate_metrics

# CRITICAL: Use sqrt(5) for session-filtered FX data
metrics = evaluate_fold(
    predictions=predictions,
    actuals=actuals,
    timestamps=timestamps,
    days_per_week=5,         # EQUITY: sqrt(5) scaling
    annualization=252,       # EQUITY: 252 trading days
    include_extended=True,
)

print(f"Weekly Sharpe (sqrt(5)): {metrics['weekly_sharpe']:.2f}")
print(f"Sortino Ratio (252 days): {metrics['sortino_ratio']:.2f}")
```

### Step 3: Compare Filtered vs Unfiltered

```python
# Compute metrics on BOTH views
metrics_session = evaluate_fold(
    predictions_session, actuals_session, timestamps_session,
    days_per_week=5, annualization=252  # Session-filtered
)

metrics_all = evaluate_fold(
    predictions_all, actuals_all, timestamps_all,
    days_per_week=7, annualization=365  # All bars (for comparison)
)

print("=== Dual-View Comparison ===")
print(f"Session-filtered (sqrt(5)): Sharpe = {metrics_session['weekly_sharpe']:.2f}")
print(f"All-bars (sqrt(7)):         Sharpe = {metrics_all['weekly_sharpe']:.2f}")
print(f"Ratio: {metrics_all['weekly_sharpe'] / metrics_session['weekly_sharpe']:.2f}x")
# Note: Using sqrt(7) on session-filtered data overstates Sharpe by ~18%
```

### Step 4: Transaction Cost Analysis

```python
# EXNESS typical costs
COST_BPS = 3.0  # 3 bps round-trip (maker + spread)

# Compute with costs
from compute_metrics import _group_by_day

def compute_sharpe_with_costs(pnl, timestamps, costs, days_per_week=5):
    net_pnl = pnl + costs  # costs are negative
    daily_pnl = _group_by_day(net_pnl, timestamps)

    if len(daily_pnl) < 2 or np.std(daily_pnl) < 1e-10:
        return 0.0

    return float(np.mean(daily_pnl) / np.std(daily_pnl) * np.sqrt(days_per_week))

# Example: 20% monthly turnover
position_changes = np.abs(np.diff(predictions, prepend=0))
costs = -position_changes * (COST_BPS / 10000)

gross_sharpe = metrics_session['weekly_sharpe']
net_sharpe = compute_sharpe_with_costs(pnl, timestamps, costs, days_per_week=5)

print(f"Gross Sharpe: {gross_sharpe:.2f}")
print(f"Net Sharpe (3 bps): {net_sharpe:.2f}")
print(f"Cost haircut: {(gross_sharpe - net_sharpe) / gross_sharpe * 100:.1f}%")
```

---

## Example 3: Edge Cases and Validation

### Edge Case 1: Model Collapse

```python
# Simulate collapsed model (constant predictions)
collapsed_predictions = np.full(1000, 0.001)
actuals = np.random.randn(1000) * 0.01
timestamps = pd.date_range('2024-01-01', periods=1000, freq='h', tz='UTC')

metrics = evaluate_fold(collapsed_predictions, actuals, timestamps)

print("=== Model Collapse Detection ===")
print(f"is_collapsed: {metrics['is_collapsed']}")
print(f"prediction_autocorr: {metrics['prediction_autocorr']:.4f}")
print(f"weekly_sharpe: {metrics['weekly_sharpe']:.4f}")
# Expected: is_collapsed=True, autocorr=1.0, sharpe≈0
```

### Edge Case 2: Insufficient Data

```python
# Only 3 days of data
short_pnl = np.random.randn(10) * 0.01
short_timestamps = pd.date_range('2024-01-01', periods=10, freq='h', tz='UTC')

metrics = evaluate_fold(
    np.random.randn(10), np.random.randn(10), short_timestamps
)

print("=== Insufficient Data ===")
print(f"omega_ratio: {metrics.get('omega_ratio')}")  # Should be None
print(f"profit_factor: {metrics.get('profit_factor')}")  # Should be None
print(f"n_days: {metrics['n_days']}")  # Should be < 5
```

### Edge Case 3: All Positive Returns

```python
# Unrealistic: all trades profitable
all_positive_pnl = np.abs(np.random.randn(500) * 0.01)
timestamps = pd.date_range('2024-01-01', periods=500, freq='h', tz='UTC')

metrics = evaluate_fold(all_positive_pnl, all_positive_pnl, timestamps)

print("=== All Positive Returns (Suspicious) ===")
print(f"hit_rate: {metrics['hit_rate']:.2%}")  # 100%
print(f"profit_factor: {metrics['profit_factor']}")  # inf
print(f"max_drawdown: {metrics['max_drawdown']:.4f}")  # 0 or near-0
# Note: This should trigger review - likely data error or look-ahead bias
```

### Edge Case 4: Session Boundary Handling

```python
# Data spanning DST transition
df_dst = pd.DataFrame({
    'timestamp': pd.date_range('2024-03-09', '2024-03-12', freq='h', tz='UTC'),
    'pnl': np.random.randn(72) * 0.01,
})

# Check session detection around DST
for ts in df_dst['timestamp']:
    in_session = is_in_session(ts)
    print(f"{ts}: {'IN' if in_session else 'OUT'}")
```

---

## Quick Reference: Metric Thresholds

### Go Criteria (Research Phase)

```yaml
go_criteria:
  positive_sharpe_rate: "> 0.55"
  mean_weekly_sharpe: "> 0"
  cv_fold_returns: "< 1.5"
  mean_hit_rate: "> 0.50"
```

### Publication Criteria

```yaml
publication_criteria:
  binomial_pvalue: "< 0.05"
  psr: "> 0.85"
  dsr: "> 0.50" # If n_trials > 1
  effective_n: ">= 30"
```

### Red Flags

```yaml
red_flags:
  is_collapsed: true
  prediction_autocorr: "> 0.95"
  hit_rate: "= 1.00" # Suspicious
  profit_factor: "= inf" # Suspicious
  max_drawdown: "= 0" # Suspicious
```

---

## Summary

| Example        | Asset  | Annualization | Session Filter | Key Consideration          |
| -------------- | ------ | ------------- | -------------- | -------------------------- |
| BTC/Binance    | Crypto | sqrt(365)     | None           | 24/7, higher volatility    |
| EUR/USD/EXNESS | FX     | sqrt(252)     | London-NY      | Session-specific scaling   |
| Edge cases     | N/A    | Varies        | Varies         | Validate before deployment |
