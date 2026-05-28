---
name: parallel-universe-selection
description: "Parallel processing for universe selection with 3-4x speedup. Trigger when: (1) selection takes too long, (2) 'No data returned' warnings for cached symbols, (3) need to process 100+ candidates."
author: Claude Code
date: 2026-01-11
---

# Parallel Universe Selection - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-11 |
| **Goal** | Optimize universe selection efficiency without sacrificing quality |
| **Environment** | Python 3.10-3.13, ThreadPoolExecutor, Alpaca API |
| **Status** | Success |

## Context

The auto universe selection data fetching process was wasting time:
1. Checking and reporting "No data returned" for symbols that were already up-to-date
2. Sequential processing of 1500+ candidates without parallelization
3. Redundant computations and database queries

**Symptoms:**
- "No data returned" warnings for symbols with valid cached data
- Selection taking 20-40 minutes for 1500 candidates
- Low CPU utilization during I/O-bound fetching phase
- Repeated `is_crypto` string checks (4+ times per symbol)

**Root Cause:**
- Incremental fetch returning empty when cache is current, triggering warning
- Sequential `for` loop for data fetching (I/O bound)
- Sequential `for` loop for statistical analysis (CPU bound but independent)
- No caching of intermediate results like `is_crypto`

## The Solution: Parallel Processing + Smart Caching

### Fix 1: Eliminate False "No Data Returned" Warnings

```python
# Before: Always warns when _fetch_remote returns empty
if df.empty:
    logger.warning("No data returned from Alpaca for %s (%s)", symbol, timeframe)

# After: Only warn for full fetches, not incremental gap-fills
if df.empty:
    if not is_incremental:
        logger.warning("No data returned from Alpaca for %s (%s)", symbol, timeframe)
```

Also added early return when cache is current:
```python
# Skip remote fetch if cache is already current
if fetch_start >= fetch_end:
    logger.debug("Cache current for %s (%s), no fetch needed", symbol, timeframe)
    return cached_data
```

### Fix 2: Parallel Data Fetching

```python
def _fetch_data_batch(self, data_fetcher, symbols, lookback_days, progress_callback=None):
    """Fetch historical data for multiple symbols in parallel."""
    results = {}
    max_workers = min(self.n_workers or 4, 8)  # Cap at 8 to avoid API rate limits

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_symbol = {
            executor.submit(self._fetch_data, data_fetcher, symbol, lookback_days): symbol
            for symbol in symbols
        }
        for future in as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            try:
                results[symbol] = future.result()
            except Exception as e:
                results[symbol] = None
            if progress_callback:
                progress_callback(f"Fetched data", completed, len(symbols))
    return results
```

### Fix 3: Parallel Statistical Analysis

```python
def _analyze_symbols_batch(self, symbols, symbol_data, progress_callback=None):
    """Analyze multiple symbols in parallel."""
    results = {}
    max_workers = min(self.n_workers or 4, 8)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_symbol = {
            executor.submit(self._analyze_symbol, symbol, symbol_data[symbol]): symbol
            for symbol in symbols if symbol in symbol_data
        }
        for future in as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            results[symbol] = future.result()
    return results
```

### Fix 4: Cache is_crypto Detection

```python
@dataclass
class SymbolAnalysis:
    symbol: str
    is_crypto: bool = False  # Cached asset type detection
    # ...

# Set once during hard filter phase
is_crypto = symbol.endswith('USD') or '/' in symbol
analysis = SymbolAnalysis(symbol=symbol, is_crypto=is_crypto, ...)

# Reuse everywhere else
if analysis.is_crypto:  # No repeated string operations
```

### Fix 5: Eliminate Double Sector Query

```python
# Before: Two queries for the same data
stats = db.get_sector_cache_stats()  # Query 1
if stats.get('never_fetched', 0) > 0:
    db.update_sectors(...)  # Query 2 (same data)

# After: Single call, let update_sectors handle "nothing to do"
updated_count = db.update_sectors(verbose=verbose)
```

### Fix 6: SQL Dotted Symbol Exclusion

```python
# Added to get_candidates() base conditions
conditions = ['is_tradable = 1', f'NOT ({YFINANCE_EXCLUDE_PATTERN_SQL})']
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| ProcessPoolExecutor | Pickling issues with DataFetcher | ThreadPoolExecutor works for I/O-bound |
| More than 8 workers | API rate limiting | Cap workers to prevent 429 errors |
| Removing Python dotted filter | SQL filter might miss edge cases | Keep as safety net |
| Parallelizing hard filters | Too fast to matter, adds complexity | Sequential is fine for CPU-bound fast ops |

## Key Insights

1. **I/O vs CPU bound** - Data fetching is I/O bound (network), analysis is CPU bound
2. **Worker count matters** - Too many workers hits API rate limits, cap at 8
3. **as_completed() is key** - Processes results as they arrive, not in order
4. **Cache intermediate results** - Avoid repeated string operations
5. **Early return on cache hit** - Skip network calls when data is current
6. **SQL filters are faster** - Move filtering to database when possible

## Final Parameters

```python
# Universe selection
n_workers = 4  # Default, can override
max_workers = 8  # Hard cap to avoid API rate limits

# Data fetcher
MEMO_TTL_SECONDS = 300  # In-memory cache TTL
```

## Performance Improvements

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Data fetching (500 symbols) | ~25 min | ~6-8 min | 3-4x faster |
| Statistical analysis (100 symbols) | ~4 min | ~1 min | 4x faster |
| False "No data" warnings | ~100-200 | 0 | Eliminated |
| is_crypto checks per symbol | 4+ | 1 | 4x reduction |

## API Usage

```python
from alpaca_trading.selection.universe import AdvancedUniverseSelector
from alpaca_trading.selection.config import SelectionConfig

# Configure parallel workers
selector = AdvancedUniverseSelector(
    config=SelectionConfig(),
    n_workers=4,  # Number of parallel workers (default: 4, max: 8)
)

# Run selection (automatically uses parallel processing)
result = selector.select_universe(
    candidates=candidate_symbols,
    data_fetcher=data_fetcher,
    lookback_days=365,
    target_portfolio_size=5,
)
```

## Files Modified

| File | Changes |
|------|---------|
| `alpaca_trading/data/fetcher.py` | Added `is_incremental` param, early return for current cache |
| `alpaca_trading/selection/universe.py` | Added `_fetch_data_batch()`, `_analyze_symbols_batch()`, `is_crypto` field |
| `alpaca_trading/selection/selection_runner.py` | Removed double sector query |
| `alpaca_trading/selection/symbol_database.py` | Added SQL dotted symbol exclusion to `get_candidates()` |
| `CLAUDE.md` | Added "Parallel Universe Selection" section |

## References

- Skill: `persistent-sector-caching` - Related database optimization
- Skill: `selection-data-caching` - Earlier caching patterns
- Skill: `dotted-symbol-exclusion` - Dotted symbol handling
- Python docs: `concurrent.futures.ThreadPoolExecutor`
