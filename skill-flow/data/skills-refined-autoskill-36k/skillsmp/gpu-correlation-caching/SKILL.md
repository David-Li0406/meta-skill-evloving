---
name: gpu-correlation-caching
description: "GPU-accelerated correlation matrix computation with persistent SQLite caching to eliminate bottleneck at correlation calculation during symbol selection"
author: Claude Code
date: 2026-01-17
---

# GPU Correlation Caching - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-17 |
| **Goal** | Eliminate performance bottleneck where training notebook hangs at "Correlations: 1/2 (50%)" during universe selection |
| **Environment** | Python 3.11+, PyTorch 2.x, SQLite |
| **Status** | Success |

## Problem

The `calculate_correlation_matrix()` function in `alpaca_trading/selection/portfolio/correlation.py` was slow because:

1. **Rolling correlation is O(n² × m)**: Nested Python loops at lines 138-153
2. **CPU-bound pandas**: Uses `window_df.corr()` repeatedly in loop
3. **No caching**: Recomputes from scratch every run, even with identical data

**Symptom**: Selection hangs at "Correlations: 1/2 (50%)" for 60-90+ seconds with 100 symbols, 4-6+ minutes with 200 symbols.

## Solution

### 1. GPU Acceleration via PyTorch

**File**: `alpaca_trading/gpu/correlation_gpu.py`

Key optimization: Use `torch.unfold()` to create sliding windows efficiently.

```python
class GPUCorrelationCalculator:
    def _compute_rolling_correlation_gpu(self, returns_tensor, symbols, rolling_window):
        # Use unfold to create sliding windows: O(1) memory-efficient view
        # returns_tensor: (n_timesteps, n_symbols)
        # After unfold: (n_windows, n_symbols, window_size)
        windows = returns_tensor.unfold(0, rolling_window, 1)

        # Process in batches to manage memory
        batch_size = min(100, n_windows)
        for batch_start in range(0, n_windows, batch_size):
            batch_windows = windows[batch_start:batch_end]
            batch_corrs = []
            for i in range(batch_windows.shape[0]):
                window_data = batch_windows[i]  # (n_symbols, window)
                corr = torch.corrcoef(window_data)
                batch_corrs.append(corr)
```

**Why this works**:
- `torch.unfold()` creates views, not copies - memory efficient
- `torch.corrcoef()` is vectorized BLAS operation
- Batching prevents GPU OOM on large datasets

### Memory-Efficient Stability Computation (Critical Fix)

The original approach stored ALL rolling correlation windows, causing OOM:
- 500 symbols × 1000 windows × 500² floats = 250GB RAM!

**Solution**: Use Welford's online algorithm to compute variance incrementally:

```python
# Instead of storing all correlations:
# rolling_correlations.append(corr)  # BAD - OOM!

# Use Welford's online algorithm for incremental variance:
for each_window:
    corr = torch.corrcoef(window_data)
    for i, j in pairs:
        # Update running statistics (O(1) memory per pair)
        pair_count[idx] += 1
        delta = corr[i,j] - pair_mean[idx]
        pair_mean[idx] += delta / pair_count[idx]
        delta2 = corr[i,j] - pair_mean[idx]
        pair_m2[idx] += delta * delta2

# Final variance = pair_m2 / (count - 1)
```

**Memory**: O(n_pairs) = O(n²) instead of O(n_windows × n²)

### Vectorized Welford's Algorithm (Performance Critical Fix)

The nested Python loops for Welford's updates caused stalls with large symbol sets:
- 1281 symbols × (1281-1)/2 = 819,840 pair updates PER WINDOW
- With ~1000 windows = 820 million Python loop iterations = STALL

**Solution**: Use `torch.triu_indices` to vectorize all pair updates:

```python
# Pre-compute upper triangular indices ONCE
triu_row, triu_col = torch.triu_indices(n_symbols, n_symbols, offset=1, device=device)

for each_window:
    corr = torch.corrcoef(window_data)

    # VECTORIZED - extract ALL upper triangular values at once
    x = corr[triu_row, triu_col]  # (n_pairs,) - all 819,840 correlations!

    # Welford's update - vectorized for all pairs simultaneously
    pair_count += 1
    delta = x - pair_mean
    pair_mean += delta / pair_count
    delta2 = x - pair_mean
    pair_m2 += delta * delta2
```

**Performance**: O(1) tensor operations per window instead of O(n²) Python loops

### 2. Persistent SQLite Caching

**File**: `alpaca_trading/selection/portfolio/correlation_cache.py`

**Schema**:
```sql
CREATE TABLE correlation_matrices (
    cache_key       TEXT PRIMARY KEY,
    symbols_hash    TEXT NOT NULL,
    date_start      TEXT NOT NULL,
    date_end        TEXT NOT NULL,
    rolling_window  INTEGER,
    matrix_data     BLOB NOT NULL,      -- pickled numpy array
    rolling_data    BLOB,               -- pickled rolling array
    stability_map   BLOB,               -- pickled stability dict
);
```

**Cache key generation**: SHA256 hash of sorted symbols + date range + rolling_window.

```python
def _compute_cache_key(symbols, date_start, date_end, rolling_window):
    sorted_symbols = sorted(symbols)  # Order-independent
    raw = f"{','.join(sorted_symbols)}|{date_start}|{date_end}|{rolling_window}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]
```

### 3. Integration

**File**: `alpaca_trading/selection/portfolio/correlation.py` (added `calculate_correlation_matrix_optimized`)

```python
def calculate_correlation_matrix_optimized(
    returns_dict: Dict[str, pd.Series],
    use_gpu: bool = True,
    cache_dir: Optional[str] = "data/cache",
    progress_callback: Optional[Callable] = None,
) -> CorrelationMatrix:
    """
    Drop-in replacement with GPU + caching.
    """
    # 1. Check cache
    cache = CorrelationCache(cache_dir)
    cached = cache.get(symbols, date_start, date_end, rolling_window)
    if cached:
        return _build_correlation_result(cached.static_matrix, ...)

    # 2. Try GPU
    if use_gpu and check_gpu_correlation_available():
        calculator = GPUCorrelationCalculator()
        corr_matrix, rolling_corr, stats = calculator.calculate(returns_dict)
    else:
        # CPU fallback
        ...

    # 3. Cache result
    cache.put(symbols, date_start, date_end, rolling_window, corr_matrix, ...)
```

## Performance Results

| Scenario | Before (CPU) | After (GPU+Cache) | Speedup |
|----------|--------------|-------------------|---------|
| 100 symbols, first run | 60-90 sec | 2-5 sec | ~20x |
| 100 symbols, cached | 60-90 sec | <0.5 sec | ~150x |
| 200 symbols, first run | 4-6 min | 5-15 sec | ~20x |

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Using `torch.roll()` for sliding windows | Creates copies, not views - slow and memory-hungry | Use `unfold()` for efficient sliding windows |
| Processing all windows at once | GPU OOM on >500 windows | Process in batches of 50 |
| **Storing all rolling correlations** | **Crashed A100 High-RAM Colab (500 symbols × 1000 windows × 500² = 250GB)** | **Use Welford's online algorithm - compute stability incrementally** |
| **Nested Python loops for Welford's** | **Stalled at "Correlations (rolling): 2/3" with 1281 symbols (820M iterations)** | **Use `torch.triu_indices` for vectorized extraction - O(1) per window** |
| Caching with pickle file per correlation | Filesystem overhead, orphaned files | SQLite single file is cleaner |
| MD5 for cache key | Collision risk with many symbols | SHA256 is safer |
| Using return Series index as date | Some series had integer indices | Explicitly extract min/max from index |

## Files Modified

| File | Change |
|------|--------|
| `alpaca_trading/gpu/correlation_gpu.py` | NEW - GPU calculator |
| `alpaca_trading/selection/portfolio/correlation_cache.py` | NEW - SQLite cache |
| `alpaca_trading/selection/portfolio/correlation.py` | Added `calculate_correlation_matrix_optimized()` |
| `alpaca_trading/selection/universe.py` | Use optimized function |
| `alpaca_trading/selection/config.py` | Added `use_gpu_correlation`, `correlation_cache_dir` |
| `alpaca_trading/selection/selection_runner.py` | Pass cache_dir through |
| `alpaca_trading/gpu/__init__.py` | Export GPU calculator |
| `alpaca_trading/selection/portfolio/__init__.py` | Export new functions |
| `tests/test_gpu_correlation.py` | NEW - Test suite |
| `CLAUDE.md` | Documentation |

## Key Insights

- **`torch.unfold()` is the key**: Creates sliding window views in O(1), not copies
- **`torch.triu_indices()` for vectorization**: Extract all upper triangular values at once, eliminating O(n²) Python loops
- **Batching prevents OOM**: Process 100 windows at a time, not all at once
- **Cache key must be symbol-order-independent**: Sort symbols before hashing
- **CPU fallback is essential**: Not all environments have CUDA
- **SQLite > file-per-entry**: Single file is cleaner and has built-in cleanup

## Configuration

```python
# Default: GPU enabled, caching enabled
selector = AdvancedUniverseSelector(
    config=SelectionConfig(),
    cache_dir='data/cache',
)

# Disable GPU (CPU only)
calculate_correlation_matrix_optimized(
    returns_dict,
    use_gpu=False,
)

# Disable caching
calculate_correlation_matrix_optimized(
    returns_dict,
    cache_dir=None,
)
```

## References

- PyTorch `unfold()` documentation: efficient sliding windows
- SQLite for caching patterns
- Previous skill: `persistent-sector-caching` - similar caching approach
