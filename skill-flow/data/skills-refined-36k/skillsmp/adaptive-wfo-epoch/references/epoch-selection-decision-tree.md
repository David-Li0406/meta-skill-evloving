# Decision Tree: Adaptive Walk-Forward Epoch Selection

Practitioner decision tree for implementing AWFES in production.

## Master Decision Tree

```
                                    START
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │  1. VALIDATE PREREQUISITES          │
                    │     - Data span ≥ 2 years?          │
                    │     - Folds ≥ 30?                   │
                    │     - Epoch range defined?          │
                    └─────────────────────────────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                        YES                        NO
                         │                         │
                         ▼                         ▼
              ┌──────────────────┐       ┌──────────────────┐
              │ Proceed to       │       │ STOP: Expand     │
              │ Step 2           │       │ data or reduce   │
              │                  │       │ fold complexity  │
              └──────────────────┘       └──────────────────┘
                         │
                         ▼
                    ┌─────────────────────────────────────┐
                    │  2. COMPUTE IS_SHARPE FOR FOLD      │
                    │     Train model, evaluate IS        │
                    └─────────────────────────────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                   IS_SR > 1.0?              IS_SR ≤ 1.0?
                         │                         │
                         ▼                         ▼
              ┌──────────────────┐       ┌──────────────────┐
              │ WFE is valid     │       │ WFE INVALID      │
              │ Continue         │       │ Use fallback:    │
              │                  │       │ - Previous epoch │
              │                  │       │ - Median epoch   │
              └──────────────────┘       └──────────────────┘
                         │
                         ▼
                    ┌─────────────────────────────────────┐
                    │  3. COMPUTE WFE FOR EACH EPOCH      │
                    │     WFE = OOS_SR / IS_SR            │
                    └─────────────────────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │  4. CHECK WFE THRESHOLD             │
                    │     Any WFE ≥ 0.30?                 │
                    └─────────────────────────────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                        YES                        NO
                         │                         │
                         ▼                         ▼
              ┌──────────────────┐       ┌──────────────────┐
              │ Continue to      │       │ REJECT ALL       │
              │ frontier         │       │ Severe overfit   │
              │ analysis         │       │ Investigate      │
              │                  │       │ model/features   │
              └──────────────────┘       └──────────────────┘
                         │
                         ▼
                    ┌─────────────────────────────────────┐
                    │  5. COMPUTE EFFICIENT FRONTIER      │
                    │     Find Pareto-optimal epochs      │
                    └─────────────────────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │  6. APPLY STABILITY PENALTY         │
                    │     Change only if >10% improvement │
                    └─────────────────────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │  7. SELECT & RECORD EPOCH           │
                    │     - Record selection history      │
                    │     - Carry forward to next fold    │
                    └─────────────────────────────────────┘
                                      │
                                      ▼
                                  NEXT FOLD
```

## Detailed Decision Nodes

### Node 1: Validate Prerequisites

```python
def validate_prerequisites(
    data_span_years: float,
    n_folds: int,
    epoch_configs: list[int],
) -> tuple[bool, list[str]]:
    """Check if prerequisites are met."""
    issues = []

    if data_span_years < 2:
        issues.append(f"Data span {data_span_years:.1f} years < 2 years minimum")

    if n_folds < 30:
        issues.append(f"Folds {n_folds} < 30 minimum for statistical significance")

    if len(epoch_configs) < 2:
        issues.append("Need at least 2 epoch candidates")

    if len(epoch_configs) > 5:
        issues.append(f"Too many epochs ({len(epoch_configs)}) - limit to 3-5")

    # Check geometric spacing
    ratios = [epoch_configs[i+1] / epoch_configs[i]
              for i in range(len(epoch_configs) - 1)]
    if max(ratios) / min(ratios) > 2:
        issues.append("Epoch spacing should be roughly geometric")

    return len(issues) == 0, issues
```

**Actions by Outcome**:

| Outcome             | Action                                        |
| ------------------- | --------------------------------------------- |
| All checks pass     | Proceed to epoch sweep                        |
| Data span too short | Acquire more data or use longer lookback      |
| Too few folds       | Reduce step size between folds                |
| Too many epochs     | Combine similar values, use geometric spacing |

### Node 2: IS_Sharpe Validation

```python
def check_is_sharpe(is_sharpe: float, min_threshold: float = 1.0) -> dict:
    """Validate in-sample Sharpe is sufficient for WFE computation."""
    return {
        "is_valid": is_sharpe >= min_threshold,
        "is_sharpe": is_sharpe,
        "action": "proceed" if is_sharpe >= min_threshold else "use_fallback",
        "reason": (
            None if is_sharpe >= min_threshold
            else f"IS_Sharpe {is_sharpe:.2f} < {min_threshold} threshold"
        ),
    }
```

**Fallback Strategy**:

```python
def get_fallback_epoch(
    previous_epoch: int | None,
    epoch_configs: list[int],
    selection_history: list[dict],
) -> int:
    """Get fallback epoch when WFE is invalid."""
    # Priority 1: Use previous fold's selection
    if previous_epoch is not None:
        return previous_epoch

    # Priority 2: Use mode from selection history
    if selection_history:
        epochs = [s["epoch"] for s in selection_history]
        return max(set(epochs), key=epochs.count)

    # Priority 3: Use median of config range
    return sorted(epoch_configs)[len(epoch_configs) // 2]
```

### Node 3: WFE Computation

```python
def compute_all_wfes(
    epoch_results: list[dict],
    is_sharpe_min: float = 1.0,
) -> list[dict]:
    """Compute WFE for each epoch candidate."""
    wfe_results = []

    for result in epoch_results:
        epoch = result["epoch"]
        is_sharpe = result["is_sharpe"]
        oos_sharpe = result["oos_sharpe"]
        training_time = result.get("training_time_sec", epoch)

        if is_sharpe < is_sharpe_min:
            wfe = None
            status = "IS_TOO_LOW"
        elif oos_sharpe < 0:
            wfe = oos_sharpe / is_sharpe  # Negative WFE
            status = "NEGATIVE_OOS"
        else:
            wfe = oos_sharpe / is_sharpe
            status = "VALID"

        wfe_results.append({
            "epoch": epoch,
            "wfe": wfe,
            "status": status,
            "is_sharpe": is_sharpe,
            "oos_sharpe": oos_sharpe,
            "training_time_sec": training_time,
        })

    return wfe_results
```

### Node 4: WFE Threshold Check

```python
def check_wfe_threshold(
    wfe_results: list[dict],
    hard_reject: float = 0.30,
    warning: float = 0.50,
) -> dict:
    """Check if any epoch passes WFE threshold."""
    valid_wfes = [r["wfe"] for r in wfe_results if r["wfe"] is not None]

    if not valid_wfes:
        return {
            "decision": "REJECT_ALL",
            "reason": "No valid WFE values computed",
            "max_wfe": None,
        }

    max_wfe = max(valid_wfes)

    if max_wfe < hard_reject:
        return {
            "decision": "REJECT_ALL",
            "reason": f"Max WFE {max_wfe:.2f} < {hard_reject} (severe overfitting)",
            "max_wfe": max_wfe,
        }
    elif max_wfe < warning:
        return {
            "decision": "WARNING",
            "reason": f"Max WFE {max_wfe:.2f} < {warning} (moderate overfitting)",
            "max_wfe": max_wfe,
        }
    else:
        return {
            "decision": "PROCEED",
            "reason": None,
            "max_wfe": max_wfe,
        }
```

**Actions by Decision**:

| Decision     | Action                                                                  |
| ------------ | ----------------------------------------------------------------------- |
| `REJECT_ALL` | Do NOT deploy. Investigate model architecture, features, regularization |
| `WARNING`    | May proceed with caution. Flag for review. Consider more regularization |
| `PROCEED`    | Continue to efficient frontier analysis                                 |

### Node 5: Efficient Frontier

```python
def find_efficient_frontier(wfe_results: list[dict]) -> list[dict]:
    """Find Pareto-optimal epochs (maximize WFE, minimize time)."""
    valid = [r for r in wfe_results if r["wfe"] is not None]

    if not valid:
        return []

    frontier = []
    for candidate in valid:
        dominated = False
        for other in valid:
            if candidate["epoch"] == other["epoch"]:
                continue
            # Other dominates if: better/equal WFE AND lower/equal time
            # with at least one strict inequality
            if (other["wfe"] >= candidate["wfe"] and
                other["training_time_sec"] <= candidate["training_time_sec"] and
                (other["wfe"] > candidate["wfe"] or
                 other["training_time_sec"] < candidate["training_time_sec"])):
                dominated = True
                break

        if not dominated:
            frontier.append(candidate)

    return sorted(frontier, key=lambda x: x["wfe"], reverse=True)
```

### Node 6: Stability Penalty

```python
def apply_stability_penalty(
    frontier: list[dict],
    previous_epoch: int | None,
    min_improvement: float = 0.10,
) -> dict:
    """Select from frontier with stability penalty."""
    if not frontier:
        raise ValueError("Empty frontier")

    # Best by WFE
    best = frontier[0]

    if previous_epoch is None:
        return {
            "selected": best["epoch"],
            "changed": True,
            "reason": "Initial selection (no previous)",
        }

    # Find previous epoch in results
    prev_result = next(
        (r for r in frontier if r["epoch"] == previous_epoch),
        None
    )

    if prev_result is None:
        # Previous not on frontier - must change
        return {
            "selected": best["epoch"],
            "changed": True,
            "reason": f"Previous epoch {previous_epoch} not on frontier",
        }

    # Check if improvement exceeds threshold
    improvement = (best["wfe"] - prev_result["wfe"]) / prev_result["wfe"]

    if improvement > min_improvement:
        return {
            "selected": best["epoch"],
            "changed": True,
            "reason": f"Improvement {improvement:.1%} > {min_improvement:.0%} threshold",
        }
    else:
        return {
            "selected": previous_epoch,
            "changed": False,
            "reason": f"Improvement {improvement:.1%} < {min_improvement:.0%} threshold",
        }
```

### Node 7: Record and Carry Forward

```python
def record_selection(
    fold_idx: int,
    selected_epoch: int,
    wfe_results: list[dict],
    frontier: list[dict],
    selection_history: list[dict],
) -> dict:
    """Record selection for tracking and analysis."""
    selected_result = next(
        (r for r in wfe_results if r["epoch"] == selected_epoch),
        None
    )

    record = {
        "fold_idx": fold_idx,
        "epoch": selected_epoch,
        "wfe": selected_result["wfe"] if selected_result else None,
        "frontier_epochs": [r["epoch"] for r in frontier],
        "all_wfes": {r["epoch"]: r["wfe"] for r in wfe_results},
        "changed": (
            len(selection_history) == 0 or
            selection_history[-1]["epoch"] != selected_epoch
        ),
    }

    selection_history.append(record)
    return record
```

## Complete Pipeline Example

```python
def run_adaptive_epoch_selection(
    data: pd.DataFrame,
    epoch_configs: list[int] = [400, 800, 1000, 2000],
    n_folds: int = 50,
    min_wfe_improvement: float = 0.10,
) -> dict:
    """Complete AWFES pipeline."""

    # 1. Validate prerequisites
    data_span_years = (data.index[-1] - data.index[0]).days / 365
    is_valid, issues = validate_prerequisites(data_span_years, n_folds, epoch_configs)

    if not is_valid:
        raise ValueError(f"Prerequisites not met: {issues}")

    # Initialize
    selection_history = []
    previous_epoch = None
    fold_results = []

    # Generate folds
    folds = generate_wfo_folds(data, n_folds)

    for fold_idx, fold in enumerate(folds):
        # 2-3. Train all epochs, compute WFE
        epoch_results = []
        for epoch in epoch_configs:
            is_sharpe, oos_sharpe, time_sec = train_and_evaluate(fold, epoch)
            epoch_results.append({
                "epoch": epoch,
                "is_sharpe": is_sharpe,
                "oos_sharpe": oos_sharpe,
                "training_time_sec": time_sec,
            })

        wfe_results = compute_all_wfes(epoch_results)

        # 4. Check threshold
        threshold_check = check_wfe_threshold(wfe_results)

        if threshold_check["decision"] == "REJECT_ALL":
            # Use fallback
            selected = get_fallback_epoch(previous_epoch, epoch_configs, selection_history)
            record = {
                "fold_idx": fold_idx,
                "epoch": selected,
                "wfe": None,
                "status": "FALLBACK",
                "reason": threshold_check["reason"],
            }
        else:
            # 5. Compute frontier
            frontier = find_efficient_frontier(wfe_results)

            # 6. Apply stability penalty
            selection = apply_stability_penalty(frontier, previous_epoch)
            selected = selection["selected"]

            # 7. Record
            record = record_selection(
                fold_idx, selected, wfe_results, frontier, selection_history
            )

        fold_results.append(record)
        previous_epoch = selected

    # Aggregate results
    return {
        "fold_results": fold_results,
        "selection_history": selection_history,
        "summary": summarize_selection_history(selection_history),
    }
```

## Diagnostic Checks

After completing the pipeline, run these diagnostics:

### Check 1: Peak Picking

```python
def diagnose_peak_picking(history: list[dict], epoch_configs: list[int]) -> dict:
    """Check if selections cluster at boundaries."""
    epochs = [h["epoch"] for h in history if h["epoch"] is not None]
    min_e, max_e = min(epoch_configs), max(epoch_configs)

    boundary_count = sum(1 for e in epochs if e in [min_e, max_e])
    boundary_rate = boundary_count / len(epochs) if epochs else 0

    return {
        "boundary_rate": boundary_rate,
        "is_problematic": boundary_rate > 0.5,
        "recommendation": (
            "Expand epoch range" if boundary_rate > 0.5
            else "Range appears adequate"
        ),
    }
```

### Check 2: Selection Stability

```python
def diagnose_stability(history: list[dict]) -> dict:
    """Check selection stability across folds."""
    changes = sum(1 for h in history if h.get("changed", False))
    change_rate = changes / len(history) if history else 0

    epochs = [h["epoch"] for h in history if h["epoch"] is not None]
    epoch_cv = np.std(epochs) / np.mean(epochs) if epochs else 0

    return {
        "change_rate": change_rate,
        "epoch_cv": epoch_cv,
        "is_stable": change_rate < 0.3 and epoch_cv < 0.5,
        "recommendation": (
            "Consider increasing stability penalty" if change_rate > 0.3
            else "Stability acceptable"
        ),
    }
```

### Check 3: WFE Distribution

```python
def diagnose_wfe_distribution(history: list[dict]) -> dict:
    """Analyze WFE distribution across folds."""
    wfes = [h["wfe"] for h in history if h.get("wfe") is not None]

    if not wfes:
        return {"status": "NO_VALID_WFE", "recommendation": "Investigate model"}

    return {
        "mean": np.mean(wfes),
        "median": np.median(wfes),
        "std": np.std(wfes),
        "ci_95": np.percentile(wfes, [2.5, 97.5]).tolist(),
        "below_threshold": sum(1 for w in wfes if w < 0.30) / len(wfes),
        "status": "HEALTHY" if np.median(wfes) >= 0.50 else "CONCERNING",
    }
```

## Summary Flowchart

```
┌────────────────────────────────────────────────────────────────────┐
│                    AWFES DECISION SUMMARY                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Prerequisites OK? ──NO──> Fix data/folds first                   │
│         │                                                          │
│        YES                                                         │
│         │                                                          │
│         ▼                                                          │
│  IS_Sharpe > 1.0? ──NO──> Use fallback epoch                      │
│         │                                                          │
│        YES                                                         │
│         │                                                          │
│         ▼                                                          │
│  Any WFE > 0.30? ──NO──> REJECT: Severe overfitting               │
│         │                                                          │
│        YES                                                         │
│         │                                                          │
│         ▼                                                          │
│  Compute Efficient Frontier                                        │
│         │                                                          │
│         ▼                                                          │
│  Improvement > 10%? ──NO──> Keep previous epoch                   │
│         │                                                          │
│        YES                                                         │
│         │                                                          │
│         ▼                                                          │
│  Select new epoch, record, carry forward                          │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

## Quick Reference: Thresholds

| Threshold         | Value     | Action if Violated          |
| ----------------- | --------- | --------------------------- |
| Data span         | ≥ 2 years | Acquire more data           |
| Folds             | ≥ 30      | Reduce step size            |
| Epoch candidates  | 3-5       | Consolidate similar values  |
| IS_Sharpe         | > 1.0     | Use fallback epoch          |
| WFE hard reject   | < 0.30    | Investigate model           |
| WFE warning       | < 0.50    | Flag for review             |
| WFE target        | ≥ 0.70    | Production ready            |
| Stability penalty | 10%       | Adjust based on change rate |
| Change rate       | < 30%     | Increase penalty if higher  |
| Epoch CV          | < 0.50    | Investigate if higher       |
