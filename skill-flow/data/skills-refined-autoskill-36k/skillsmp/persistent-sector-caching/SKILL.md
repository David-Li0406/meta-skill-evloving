---
name: persistent-sector-caching
description: "Cache yfinance sector data permanently to avoid Yahoo Finance rate limits. Trigger when: (1) 401 errors during sector fetching, (2) sector updates take too long, (3) need selective sector refresh."
author: Claude Code
date: 2026-01-09
---

# Persistent Sector Caching - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-09 |
| **Goal** | Prevent yfinance rate limit errors (401) during sector updates |
| **Environment** | Python 3.10-3.13, yfinance, SQLite |
| **Status** | Success |

## Context

The training notebook was failing during STAGE 1b (sector updates) because Yahoo Finance aggressively rate-limits API requests. With ~11,000 equity symbols needing sector data, the system would hit 401 "Invalid Crumb" errors after fetching ~1,400-1,800 symbols regardless of parallelism or delays.

**Symptoms:**
- `HTTP Error 401: {"finance":{"error":{"code":"Unauthorized","description":"Invalid Crumb"}}}`
- Errors flood after ~12-15% of symbols processed
- Reducing workers from 8 to 3 didn't help
- Adding delays between chunks didn't help
- User had to abort and re-run, losing progress

**Root Cause:**
- Yahoo Finance rate-limits by IP, not by request count
- Multiple workers make rate limiting WORSE (more requests per second)
- Sector data was being re-fetched for ALL symbols every run
- "other" sector symbols were being retried unnecessarily

## The Solution: Persistent Caching

Since sector data rarely changes (companies don't switch sectors often), cache it permanently:

1. **New column:** `sector_last_updated` tracks when each symbol's sector was fetched
2. **Default behavior:** Only fetch sectors for symbols where `sector_last_updated IS NULL`
3. **Failed fetches:** Mark as fetched so we don't retry them
4. **Force refresh:** Optional parameter for manual full refresh

### Database Migration (v3)

```sql
-- Add column for tracking when sector was fetched
ALTER TABLE symbols ADD COLUMN sector_last_updated TEXT;

-- Mark existing non-'other' sectors as already fetched (preserve cache)
UPDATE symbols
SET sector_last_updated = datetime('now')
WHERE sector IS NOT NULL AND sector != 'other';
```

### Modified Query Logic

```python
def _get_symbols_missing_sector(self, force_refresh=False):
    if force_refresh:
        # Force refresh: get all symbols with 'other' or NULL sector
        query = """
            SELECT symbol FROM symbols
            WHERE asset_type = ? AND (sector IS NULL OR sector = 'other')
            AND NOT (symbol LIKE '%.%')
        """
    else:
        # Default: only symbols NEVER fetched (persistent cache)
        query = """
            SELECT symbol FROM symbols
            WHERE asset_type = ? AND sector_last_updated IS NULL
            AND NOT (symbol LIKE '%.%')
        """
```

### Update Logic

```python
# Update sector AND mark as fetched
cursor.execute(
    'UPDATE symbols SET sector = ?, sector_last_updated = ? WHERE symbol = ?',
    (sector, now, symbol)
)

# Mark failed fetches as fetched too (won't retry)
for symbol in failed_symbols:
    cursor.execute(
        'UPDATE symbols SET sector_last_updated = ? WHERE symbol = ? AND sector_last_updated IS NULL',
        (now, symbol)
    )
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| 8 parallel workers | 401 errors after ~1400 symbols | More workers = faster rate limit hit |
| Reduce to 3 workers | 401 errors after ~1800 symbols | Workers don't help, Yahoo limits by IP |
| 100-symbol chunks + 5s delays | Still hit 401 after 15-20% | Delays don't reset Yahoo's rate limit window |
| Longer delays (10-15s) | Too slow (~4 hours for 11k symbols) | Not practical |
| Re-fetch 'other' sectors | Same symbols fail repeatedly | Some symbols just don't have sector data |
| Retry on 401 with backoff | Still fails, wastes time | 401 means "blocked", not "retry" |

## Bug Fix: INSERT OR REPLACE Wipes Sector Cache (2026-01-11)

**Problem:** After implementing persistent caching, sector data was STILL being re-fetched every run.

**Root Cause:** `update_equities()` and `update_crypto()` used `INSERT OR REPLACE` which deletes the entire row before inserting. This wiped out `sector` and `sector_last_updated` columns because they weren't included in the INSERT statement.

**Fix:** Changed to `INSERT ... ON CONFLICT(symbol) DO UPDATE SET ...` which only updates specified columns, preserving sector data.

```python
# BEFORE (broken): Wipes sector columns
cursor.execute('''
    INSERT OR REPLACE INTO symbols (symbol, asset_type, price, ...)
    VALUES (?, ?, ?, ...)
''', ...)

# AFTER (fixed): Preserves sector columns
cursor.execute('''
    INSERT INTO symbols (symbol, asset_type, price, ...)
    VALUES (?, ?, ?, ...)
    ON CONFLICT(symbol) DO UPDATE SET
        asset_type = excluded.asset_type,
        price = excluded.price,
        ...  -- sector and sector_last_updated NOT listed, so preserved
''', ...)
```

**Lesson Learned:** SQLite's `INSERT OR REPLACE` is actually `DELETE` + `INSERT`. Use `INSERT ON CONFLICT DO UPDATE` to preserve columns not in the statement.

## Key Insights

1. **Yahoo rate limits by IP** - No amount of delays or reduced parallelism helps once blocked
2. **Sector data is stable** - Companies rarely change sectors, cache is safe
3. **'other' is a valid result** - Some symbols legitimately have no sector (ETFs, SPACs, etc.)
4. **Mark failures as fetched** - Prevents retrying symbols that will never work
5. **First run is expensive** - Accept that initial population takes 30-60+ min
6. **Subsequent runs are fast** - Only ~100-500 new symbols per day

## Final Parameters

```python
# Database version
DB_VERSION = 3  # Added sector_last_updated

# Workers (doesn't matter much now, few symbols to fetch)
SECTOR_MAX_WORKERS = 3

# Max symbols per session (prevents timeout)
SECTOR_MAX_SYMBOLS = 3000
```

## Timing Expectations

| Scenario | Symbols | Time |
|----------|---------|------|
| First run (empty cache) | ~11,000 | 30-60+ min |
| Typical run (cached) | ~100-500 | 1-5 min |
| After migration | 0 | instant |
| Force refresh (3k limit) | 3,000 | 10-20 min |

## API Usage

```python
from alpaca_trading.selection import SymbolDatabase

db = SymbolDatabase(db_path='data/symbol_database.db')

# Default: only fetch new symbols (persistent cache)
db.update_sectors(verbose=True)

# Check what would be fetched
stats = db.get_sector_cache_stats()
print(f"Never fetched: {stats['never_fetched']}")
print(f"Cached with sector: {stats['with_sector']}")
print(f"Cached as 'other': {stats['cached_other']}")

# Force refresh all 'other' sectors (use sparingly)
db.update_sectors(force_refresh=True, max_symbols=3000)
```

## Files Modified

| File | Changes |
|------|---------|
| `alpaca_trading/selection/symbol_database.py` | Added `sector_last_updated` column, modified `_get_symbols_missing_sector()`, `update_sectors()`, added `get_sector_cache_stats()` |
| `CLAUDE.md` | Added "Persistent Sector Caching" section, updated Common Issues table |

## References

- Skill: `dotted-symbol-exclusion` - Related exclusion of special symbols
- Skill: `selection-data-caching` - Earlier caching attempt (superseded)
- Skill: `persistent-cache-gap-filling` - Similar pattern for OHLCV data
- yfinance rate limiting: https://github.com/ranaroussi/yfinance/issues
