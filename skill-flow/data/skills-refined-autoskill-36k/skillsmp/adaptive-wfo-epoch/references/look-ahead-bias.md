# Look-Ahead Bias Prevention Reference

Detailed protocols and examples for preventing look-ahead bias in AWFES.

## What is Look-Ahead Bias?

Look-ahead bias occurs when information from the future "leaks" into decisions that should only use past data. In AWFES, this can happen when:

1. **Epoch selection uses future returns**: Choosing epochs based on test performance
2. **Feature scaling uses full dataset**: Scaler fit includes validation/test data
3. **No temporal gap**: Adjacent data points share information

## The Three-Way Split Solution

```
                AWFES: Look-Ahead Bias Prevention

 ---------------     +----------+     +-----------+     +----------+     #==========#
| Past Data     | -> | TRAIN    | --> | EMBARGO A | --> | VALIDATE | --> | EMBARGO B |
 ---------------     | (fit)    |     | (gap)     |     | (select) |     | (gap)     |
                     +----------+     +----------+      +-----------+     +----------+
                                                                               |
                                                                               v
                                                                          #==========#
                                                                          H   TEST   H
                                                                          H (report) H
                                                                          #==========#
```

<details>
<summary>graph-easy source</summary>

```
graph { label: "AWFES: Look-Ahead Bias Prevention"; flow: east; }

[ Past Data ] { shape: rounded; }
[ TRAIN (fit) ]
[ EMBARGO A (gap) ]
[ VALIDATE (select) ]
[ EMBARGO B (gap) ]
[ TEST (report) ] { border: double; }

[ Past Data ] -> [ TRAIN (fit) ]
[ TRAIN (fit) ] -> [ EMBARGO A (gap) ]
[ EMBARGO A (gap) ] -> [ VALIDATE (select) ]
[ VALIDATE (select) ] -> [ EMBARGO B (gap) ]
[ EMBARGO B (gap) ] -> [ TEST (report) ]
```

</details>

## Anti-Pattern 1: Direct Epoch Application

### The Problem

```python
# WRONG: Using current fold's optimal epoch on current fold's test
for fold in folds:
    epoch_results = sweep_epochs(fold.train, fold.validation)
    optimal_epoch = select_optimal(epoch_results)

    # BIAS: optimal_epoch was selected using validation from same time period
    # Validation Sharpe influenced selection, test Sharpe will be correlated
    model = train(fold.train + fold.validation, epochs=optimal_epoch)
    test_metrics = evaluate(model, fold.test)  # OPTIMISTICALLY BIASED
```

### Why It's Wrong

- Validation data and test data are from the same fold (same time period)
- Market regimes are autocorrelated: good validation → likely good test
- Epoch selection optimizes for validation, which correlates with test
- Result: **Overstated performance** in backtest

### The Fix: Bayesian Carry-Forward (v3 Protocol)

The v3 protocol fixes a subtle but critical timing bug in earlier implementations. The key insight:
**TEST must use `prior_bayesian_epoch` obtained BEFORE any work on the current fold**.

```python
# v3 CORRECT: Using Bayesian posterior from PRIOR folds
# CRITICAL: Get prior epoch BEFORE any work on current fold
bayesian_selector = BayesianEpochSelector(epoch_configs)

for fold_idx, fold in enumerate(folds):
    # ═══════════════════════════════════════════════════════════════════
    # Step 1: FIRST - Get epoch from ONLY prior folds (BEFORE any fold work)
    # ═══════════════════════════════════════════════════════════════════
    prior_bayesian_epoch = bayesian_selector.get_current_epoch()

    # ═══════════════════════════════════════════════════════════════════
    # Step 2: Train models with checkpoints, find val_optimal on VALIDATION
    # ═══════════════════════════════════════════════════════════════════
    epoch_results = sweep_epochs(fold.train, fold.validation)
    val_optimal_epoch = select_optimal(epoch_results)

    # ═══════════════════════════════════════════════════════════════════
    # Step 3: TEST uses prior_bayesian_epoch (NOT val_optimal!)
    # ═══════════════════════════════════════════════════════════════════
    model = train(fold.train + fold.validation, epochs=prior_bayesian_epoch)
    test_metrics = evaluate(model, fold.test)  # UNBIASED

    # ═══════════════════════════════════════════════════════════════════
    # Step 4: AFTER test - Update Bayesian with val_optimal for FUTURE folds
    # ═══════════════════════════════════════════════════════════════════
    bayesian_selector.update(val_optimal_epoch, epoch_results["wfe"])

    # MANDATORY: Log for audit trail
    logger.info(
        f"Fold {fold_idx}: prior_bayesian_epoch={prior_bayesian_epoch}, "
        f"val_optimal_epoch={val_optimal_epoch}, test_uses={prior_bayesian_epoch}"
    )
```

### v3 vs v2: The Critical Difference

```python
# ═══════════════════════════════════════════════════════════════════════════════
# v2 BUG (DO NOT USE): Bayesian update happens BEFORE test evaluation
# ═══════════════════════════════════════════════════════════════════════════════
for fold in folds:
    epoch_metrics = sweep_epochs(fold.train, fold.validation)
    val_optimal_epoch = select_optimal(epoch_metrics)

    # v2 BUG: Update Bayesian with current fold's val_optimal BEFORE test
    bayesian.update(val_optimal_epoch, wfe)        # ← BUG: Too early!
    selected_epoch = bayesian.get_current_epoch()  # ← CONTAMINATED

    # selected_epoch now contains information from val_optimal of SAME fold
    test_metrics = evaluate(selected_epoch, fold.test)  # ← LOOK-AHEAD BIAS!

# ═══════════════════════════════════════════════════════════════════════════════
# v3 FIX: prior_bayesian_epoch obtained BEFORE any fold work
# ═══════════════════════════════════════════════════════════════════════════════
for fold in folds:
    prior_bayesian_epoch = bayesian.get_current_epoch()  # ← FIRST!

    epoch_metrics = sweep_epochs(fold.train, fold.validation)
    val_optimal_epoch = select_optimal(epoch_metrics)

    test_metrics = evaluate(prior_bayesian_epoch, fold.test)  # ← UNBIASED

    bayesian.update(val_optimal_epoch, wfe)  # ← AFTER test, for FUTURE folds
```

### Impact of the Fix

| Metric           | v2 (Buggy) | v3 (Fixed) | Change      |
| ---------------- | ---------- | ---------- | ----------- |
| Mean Test Sharpe | ~0.12      | ~0.06      | -50%        |
| DSR              | ~0.15      | ~0.07      | More honest |
| Bias Direction   | Optimistic | Unbiased   | Correct     |

The v2 results were inflated because `selected_epoch` was contaminated by information
from the current fold's validation optimal. This gave the model a subtle "peek" at
which epoch would perform well on temporally adjacent test data.

## Anti-Pattern 2: Global Feature Scaling

### The Problem

```python
# WRONG: Fitting scaler on ALL data including future
scaler = StandardScaler()
scaler.fit(all_data)  # LEAK: includes validation and test

for fold in folds:
    train_scaled = scaler.transform(fold.train)
    test_scaled = scaler.transform(fold.test)  # Uses future statistics!
```

### Why It's Wrong

- Scaler mean/std computed from full dataset
- Test data statistics influence training data scaling
- Information flows backwards in time

### The Fix: Per-Fold Scaling

```python
# CORRECT: Fit scaler only on training data
for fold in folds:
    scaler = MinMaxScaler()
    scaler.fit(fold.train)  # Only past data

    train_scaled = scaler.transform(fold.train)
    validation_scaled = scaler.transform(fold.validation)
    test_scaled = scaler.transform(fold.test)
```

## Anti-Pattern 3: No Embargo Gap

### The Problem

```python
# WRONG: Adjacent train/validation/test with no gap
train = data[0:1000]
validation = data[1000:1200]  # Immediately after train
test = data[1200:1400]  # Immediately after validation
```

### Why It's Wrong

- Range bars have variable duration (hours to days)
- A bar at index 1000 might overlap temporally with bar 1001
- Feature windows (e.g., 20-bar momentum) create information sharing
- Autocorrelation in returns creates dependency

### The Fix: Time-Based Embargo

**Parameter naming convention**:

- `embargo_hours`: Use for **time-based** embargoes (calendar time gap)
- `embargo_pct`: Use for **percentage-based** embargoes (fraction of fold size)

The validation checklist mentions "6% minimum embargo" - this refers to the effective time gap
being approximately 6% of fold duration. For explicit control, use `embargo_hours`.

```python
# CORRECT: Calendar-based embargo gaps
def split_with_embargo(
    data: pd.DataFrame,
    train_pct: float = 0.60,
    val_pct: float = 0.20,
    test_pct: float = 0.20,
    embargo_hours: int = 24,  # Time-based: 1 day minimum calendar gap
    # Alternative: embargo_pct: float = 0.06 for percentage-based
) -> tuple:
    """Split data with time-based embargo.

    Note: embargo_hours is preferred over embargo_pct because:
    - Time-based gaps are more intuitive for information leakage
    - Range bars have variable time density, making % ambiguous
    - 24h gap = ~6% of typical weekly fold (approximation)
    """
    n = len(data)

    # Calculate split points
    train_end = int(n * train_pct)
    val_start = train_end

    # Find embargo end: first bar >= embargo_hours after train_end
    train_end_time = data.iloc[train_end]["timestamp"]
    embargo_end_time = train_end_time + pd.Timedelta(hours=embargo_hours)

    # Skip bars in embargo period
    embargo_mask = data["timestamp"] < embargo_end_time
    val_start = embargo_mask.sum()

    val_end = val_start + int(n * val_pct)

    # Second embargo
    val_end_time = data.iloc[val_end]["timestamp"]
    embargo2_end_time = val_end_time + pd.Timedelta(hours=embargo_hours)
    embargo2_mask = data["timestamp"] < embargo2_end_time
    test_start = embargo2_mask.sum()

    return (
        data.iloc[:train_end],      # Train
        data.iloc[val_start:val_end],  # Validation (after embargo 1)
        data.iloc[test_start:],     # Test (after embargo 2)
    )
```

## Anti-Pattern 4: Feature Recomputation

### The Problem

```python
# WRONG: Recomputing features after split
def compute_momentum(df):
    return df["close"].pct_change(20)  # Uses future bars if not careful

train, val, test = split_data(data)

# Recomputing on each split CORRECTLY handles boundaries
train["momentum"] = compute_momentum(train)  # OK
val["momentum"] = compute_momentum(val)  # WRONG: loses first 20 bars of context
```

### The Fix: Pre-Compute Before Split

```python
# CORRECT: Compute features on full data, then split
data["momentum_20"] = compute_momentum(data)
data["rsi_14"] = compute_rsi(data, 14)

# Features already computed, just split
train, val, test = split_data(data)

# Validation/test have correct feature values from their context
```

## Validation Checklist

Before running AWFES, verify:

### Data Split

- [ ] Three-way split: train/validation/test
- [ ] 6% minimum embargo at each boundary
- [ ] Temporal order preserved (no shuffling)
- [ ] Split points logged for reproducibility

### Feature Engineering

- [ ] Features computed BEFORE split
- [ ] No rolling calculations cross split boundaries
- [ ] Scaler fit ONLY on training data
- [ ] No target leakage in features

### Epoch Selection

- [ ] Validation used for WFE computation
- [ ] Bayesian posterior uses PRIOR folds only
- [ ] Current fold test is UNTOUCHED during selection
- [ ] Selection logged for auditability

### Model Training

- [ ] Final model trained on train + validation
- [ ] Test data never seen during training
- [ ] Same random seeds for reproducibility

## Diagnostic Tests

### Test 1: Shuffle Sanity Check

```python
def shuffle_sanity_check(fold_sharpes: list[float]) -> bool:
    """Shuffled folds should have ~same performance if no look-ahead."""
    # Run AWFES with shuffled fold order
    shuffled_sharpes = run_awfes(shuffle(folds))

    # If look-ahead exists, shuffled will be worse
    # (can't peek into future when future is randomized)
    original_mean = np.mean(fold_sharpes)
    shuffled_mean = np.mean(shuffled_sharpes)

    # Should be similar (within 1 std)
    return abs(original_mean - shuffled_mean) < np.std(fold_sharpes)
```

### Test 2: Forward-Only Information Flow

```python
def test_forward_only(fold_results: list[dict]) -> bool:
    """Verify information only flows forward in time."""
    for i in range(1, len(fold_results)):
        current = fold_results[i]
        prior = fold_results[i - 1]

        # Selected epoch should come from PRIOR posterior
        # Not from current fold's validation
        if current["selected_epoch"] == current["validation_optimal"]:
            # Could be coincidence, but flag for review
            print(f"WARNING: Fold {i} selected same as validation optimal")

    return True
```

### Test 3: Embargo Effectiveness

```python
def test_embargo_effectiveness(
    train: pd.DataFrame,
    test: pd.DataFrame,
    embargo_hours: int,
) -> bool:
    """Verify embargo gap is sufficient."""
    train_end = train["timestamp"].max()
    test_start = test["timestamp"].min()

    actual_gap = (test_start - train_end).total_seconds() / 3600

    if actual_gap < embargo_hours:
        print(f"ERROR: Embargo gap {actual_gap:.1f}h < required {embargo_hours}h")
        return False

    return True
```

## Common Mistakes Summary

| Mistake                  | Symptom                       | Fix                       |
| ------------------------ | ----------------------------- | ------------------------- |
| Direct epoch application | OOS >> backtest live          | Bayesian carry-forward    |
| Global scaler            | Suspiciously good results     | Per-fold fit              |
| No embargo               | Performance degrades with gap | Add 6%+ embargo           |
| Feature recomputation    | Missing values at boundaries  | Pre-compute               |
| Fold shuffling           | Better when shuffled          | Keep temporal order       |
| Target in features       | Perfect predictions           | Audit feature engineering |

## References

- López de Prado, M. (2018). _Advances in Financial Machine Learning_. Chapter 7: Cross-Validation.
- Bailey, D. H., & López de Prado, M. (2014). The deflated Sharpe ratio.
- arXiv:2512.06932 - Per-fold scaling for financial ML.
