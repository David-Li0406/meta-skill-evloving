---
name: selection-progress-reporting
description: "Progress reporting for universe selection phases. Trigger when: (1) selection appears to stall/hang, (2) no output after data fetching, (3) need visibility into hard filter or scoring phases."
author: Claude Code
date: 2026-01-12
---

# Selection Progress Reporting - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-12 |
| **Goal** | Add progress reporting to silent phases of universe selection |
| **Environment** | Python 3.10-3.13, Jupyter notebooks, Colab |
| **Status** | Success |

## Context

Universe selection with `USE_EMPIRICAL_THRESHOLDS=True` appeared to stall after fetching market data. The last output was "fetching data from CRV/USD" followed by 15+ minutes of silence.

**Symptoms:**
- Selection appears to hang after data fetching completes
- No output for 10-20+ minutes
- User cannot tell if process is stuck or working
- INFO level logging enabled but still no output

**Root Cause:**
The `select_universe()` method had progress callbacks for parallel phases (data fetch, analysis), but:
1. `select_compatible_universe()` didn't expose or pass `progress_callback`
2. `run_universe_selection()` didn't create a callback
3. Hard filter phase (sequential loop) had no progress output
4. Scoring phase (sequential loop) had no progress output

## The Solution: End-to-End Progress Reporting

### Fix 1: Add progress_callback to select_compatible_universe()

```python
def select_compatible_universe(
    candidates: List[str],
    data_fetcher: Any,
    config: Optional[SelectionConfig] = None,
    target_size: int = 5,
    lookback_days: int = 365,
    progress_callback: Optional[Callable[[str, int, int], None]] = None,  # NEW
    n_workers: int = 4,  # NEW
) -> Tuple[List[str], UniverseSelectionResult]:
    ...
    selector = AdvancedUniverseSelector(config=config, n_workers=n_workers)
    result = selector.select_universe(
        ...
        progress_callback=progress_callback,  # Pass through
    )
```

### Fix 2: Add progress to hard filter phase

```python
# Phase 1b: Apply hard filters (sequential, CPU-bound, fast)
hard_filter_count = 0
hard_filter_total = len(candidates)
for symbol in candidates:
    hard_filter_count += 1
    if progress_callback and hard_filter_count % 100 == 0:
        progress_callback("Hard filters", hard_filter_count, hard_filter_total)
    # ... rest of loop
```

### Fix 3: Add progress to scoring phase

```python
# Step 3: Calculate composite scores
scoring_count = 0
scoring_total = len(passed_hard_filter)

for symbol in passed_hard_filter:
    scoring_count += 1
    if progress_callback and scoring_count % 50 == 0:
        progress_callback("Scoring", scoring_count, scoring_total)
    # ... rest of loop
```

### Fix 4: Create default callback in selection_runner.py

```python
def create_progress_callback(verbose: bool = True) -> Callable[[str, int, int], None]:
    """
    Create a progress callback that prints updates to stdout.
    Uses carriage return for in-place updates and flushes stdout
    for notebook compatibility.
    """
    last_phase = [None]  # Mutable container to track phase changes

    def callback(phase: str, current: int, total: int) -> None:
        if not verbose:
            return

        pct = 100 * current / total if total > 0 else 0

        # Print newline when phase changes
        if last_phase[0] != phase:
            if last_phase[0] is not None:
                print()  # Complete previous line
            last_phase[0] = phase

        # Use carriage return for in-place updates
        print(f'\r  {phase}: {current:,}/{total:,} ({pct:.0f}%)', end='')
        sys.stdout.flush()  # CRITICAL for notebooks

        # Print newline when complete
        if current >= total:
            print()
            sys.stdout.flush()

    return callback
```

### Fix 5: Auto-create callback in run_universe_selection()

```python
# Create progress callback for visibility
progress_callback = create_progress_callback(verbose=verbose)

# Run selection
selected_symbols, result = select_compatible_universe(
    ...
    progress_callback=progress_callback,
)
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Checking logging level | User had INFO enabled, still no output | Problem wasn't logging, it was missing callbacks |
| Looking only at parallel phases | Hard filter and scoring are sequential | Sequential phases need progress too |
| print() without flush | Output buffered in notebooks | Always use sys.stdout.flush() for notebooks |
| Modifying notebook directly | Would require user to update | Better to fix in library code for auto-benefit |

## Key Insights

1. **Parallel != only slow phases** - Sequential loops through 1500+ symbols can take significant time
2. **Progress callbacks must be passed through** - Adding callback to inner function is useless if outer functions don't expose it
3. **sys.stdout.flush() is critical** - Jupyter notebooks buffer output; flush ensures immediate display
4. **Carriage return for in-place updates** - `\r` with `end=''` gives clean progress display
5. **Phase tracking in closure** - Use mutable container `[None]` to track phase changes across calls

## Progress Phases (Now Visible)

| Phase | Update Frequency | Previously Silent? |
|-------|------------------|-------------------|
| Fetched data | Every symbol | No (but needed callback) |
| Hard filters | Every 100 symbols | **Yes** |
| Analyzed | Every symbol | No (but needed callback) |
| Scoring | Every 50 symbols | **Yes** |

## Expected Output

```
STAGE 3-4: Downloading data and running analysis...
  Fetched data: 500/1,500 (33%)
  Fetched data: 1,000/1,500 (67%)
  Fetched data: 1,500/1,500 (100%)
  Hard filters: 500/1,500 (33%)
  Hard filters: 1,000/1,500 (67%)
  Hard filters: 1,500/1,500 (100%)
  Analyzed: 100/300 (33%)
  Analyzed: 200/300 (67%)
  Analyzed: 300/300 (100%)
  Scoring: 150/300 (50%)
  Scoring: 300/300 (100%)
```

## Files Modified

| File | Changes |
|------|---------|
| `alpaca_trading/selection/universe.py` | Added progress to hard filters + scoring, exposed callback in `select_compatible_universe()` |
| `alpaca_trading/selection/selection_runner.py` | Added `create_progress_callback()`, auto-creates callback in `run_universe_selection()` |

## References

- Skill: `parallel-universe-selection` - Related parallel processing optimization
- Skill: `empirical-config-builder` - Empirical threshold derivation (triggers large candidate sets)
- Commit: `81663a4` - feat: Add progress reporting to universe selection
