---
name: dotted-symbol-exclusion
description: "Exclude ALL dotted symbols from yfinance sector lookups and training. Trigger when: (1) yfinance errors on warrants/units/class shares, (2) training notebook fails on excluded symbol types, (3) adding new symbol exclusion patterns."
author: Claude Code
date: 2026-01-08
---

# Dotted Symbol Exclusion - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-08 |
| **Goal** | Prevent yfinance sector lookup errors on special security types |
| **Environment** | Python 3.10-3.13, yfinance, SQLite |
| **Status** | Success |

## Context

The training notebook was erroring during yfinance sector checks because special security types (warrants, units, preferred shares, class shares) don't exist on Yahoo Finance. The original code only excluded specific patterns like `.WS`, `.PR*`, `.U`, `.R`, `.W` but missed others like `.A`, `.B`, `.V` class shares.

**Symptoms:**
- yfinance returning empty/error for symbols like `BRK.A`, `GOOGL.V`, `ACHR.WS`
- Training notebook logging warnings about symbols that should have been filtered
- Inconsistency between notebook filtering (STAGE 2b) and database filtering (STAGE 1b)

## Verified Workflow

### 1. Understanding Dotted Symbols

Symbols containing a dot (`.`) typically represent:

| Suffix | Type | Example | Yahoo Finance? |
|--------|------|---------|----------------|
| `.A`, `.B`, `.V` | Class shares | BRK.A, BRK.B | Sometimes |
| `.PR*` | Preferred shares | ATH.PRD, NLY.PRF | No |
| `.WS`, `.WSA` | Warrants | ACHR.WS, IAUX.WS | No |
| `.U` | Units | HYAC.U | No |
| `.R` | Rights | BRDG.R | No |
| `.W` | When-issued | AAPL.W | No |

### 2. The Fix: Exclude ALL Dotted Symbols

Instead of maintaining a complex list of patterns, exclude ANY symbol with a dot:

```python
# In alpaca_trading/selection/symbol_database.py

# SQL pattern for database queries
YFINANCE_EXCLUDE_PATTERN_SQL = "symbol LIKE '%.%'"

# Python function for code filtering
def is_dotted_symbol(symbol: str) -> bool:
    """Check if symbol contains a dot (special security type)."""
    return '.' in symbol
```

### 3. Database Query Update

```python
def _get_symbols_missing_sector(self, asset_type: str = 'equity') -> List[str]:
    """Get symbols that don't have sector data."""
    query = f"""
        SELECT symbol FROM symbols
        WHERE asset_type = ?
        AND (sector IS NULL OR sector = 'other')
        AND NOT ({YFINANCE_EXCLUDE_PATTERN_SQL})
    """
    cursor.execute(query, (asset_type,))
    return [row[0] for row in cursor.fetchall()]
```

### 4. Code Filtering Update

```python
def update_sectors(self, symbols=None, ...):
    if symbols is None:
        symbols = self._get_symbols_missing_sector()
    else:
        # Filter out ALL dotted symbols
        symbols = [s for s in symbols if not is_dotted_symbol(s)]
```

### 5. Training Notebook Alignment

The notebook already has `EXCLUDE_DOTTED_SYMBOLS = True` in STAGE 2b, but this happens AFTER sector updates in STAGE 1b. The database-level fix ensures consistency:

```python
# STAGE 1b: Sector update (database already excludes dotted)
if ENABLE_SECTOR_FILTERING:
    db.update_sectors()  # Now excludes ALL dotted symbols

# STAGE 2b: Candidate filtering (redundant but kept for safety)
if EXCLUDE_DOTTED_SYMBOLS:
    candidates = [s for s in candidates if '.' not in s]
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Specific patterns (`.PR*`, `.WS`) | Missed `.A`, `.B`, `.V` class shares | Pattern list incomplete |
| Adding new patterns incrementally | New types keep appearing | Exclude ALL dots instead |
| Filtering only in notebook | Database sector update ran first | Must filter at database level |
| Complex regex patterns | Hard to maintain, error-prone | Simple `'.' in symbol` is enough |

## Final Parameters

```python
# SQL pattern - excludes ANY symbol with a dot
YFINANCE_EXCLUDE_PATTERN_SQL = "symbol LIKE '%.%'"

# Python check - simple and effective
def is_dotted_symbol(symbol: str) -> bool:
    return '.' in symbol
```

## Key Insights

- **ALL dotted symbols are special** - No regular stock ticker has a dot
- **yfinance fails silently** - Returns empty dict or raises exception
- **Database filtering prevents API calls** - Filter BEFORE calling yfinance
- **Notebook and database must align** - Same exclusion logic in both places
- **Crypto symbols use `/`** - `BTC/USD` has slash not dot, so safe

## Files Modified

| File | Changes |
|------|---------|
| `alpaca_trading/selection/symbol_database.py` | Simplified to exclude ALL dotted symbols; parallel sector fetching |
| `notebooks/training.ipynb` | Already has `EXCLUDE_DOTTED_SYMBOLS=True` (unchanged) |

## Performance Optimization

The original `update_sectors()` was slow (~10+ min for 3k symbols) because:
1. `yf.Tickers()` doesn't actually batch API calls
2. Each `ticker.info` call makes an individual HTTP request
3. Sequential processing + 0.5s sleep per batch

**Fix:** Use `ThreadPoolExecutor` for parallel fetching:

```python
# Before: ~10+ minutes for 3000 symbols (sequential)
# After: ~1-2 minutes for 3000 symbols (20 parallel workers)

SECTOR_MAX_WORKERS = 20  # Parallel threads

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = {executor.submit(self._fetch_single_sector, sym): sym for sym in symbols}
    for future in as_completed(futures):
        symbol, sector = future.result()
        # ...
```

**Result:** ~10x speedup (from 10+ min to 1-2 min)

## Testing Verification

```python
# Verify dotted symbols are excluded
from alpaca_trading.selection.symbol_database import is_dotted_symbol

assert is_dotted_symbol('BRK.A') == True   # Class A
assert is_dotted_symbol('BRK.B') == True   # Class B
assert is_dotted_symbol('ACHR.WS') == True # Warrant
assert is_dotted_symbol('ATH.PRD') == True # Preferred
assert is_dotted_symbol('AAPL') == False   # Normal
assert is_dotted_symbol('BTCUSD') == False # Crypto
```

## References

- Skill: `per-sector-candidate-filtering` - Related sector filtering
- yfinance documentation: https://pypi.org/project/yfinance/
- Alpaca symbol conventions: https://alpaca.markets/docs/api-documentation/
