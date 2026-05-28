---
name: crypto-database-population
description: "Populate symbol database with crypto symbols before training. Trigger when: (1) live trader fails with 'CRYPTO VIOLATION', (2) no crypto models in models/rl_symbols/, (3) db.get_candidates(asset_types=['crypto']) returns 0, (4) starting fresh training without crypto."
author: Claude Code
date: 2026-01-24
---

# Crypto Database Population

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-24 |
| **Goal** | Ensure crypto symbols are in the database before selection/training |
| **Environment** | scripts/live_trader.py, alpaca_trading/selection/symbol_database.py |
| **Status** | Success |

## Context

Live trader failed to start with error:
```
CRYPTO VIOLATION: Required min_crypto_positions=1, but portfolio has 0 crypto symbols
```

Investigation revealed:
1. `SelectionConfig.min_crypto_positions` defaults to 1 (for 24/7 trading coverage)
2. The symbol database had 0 crypto symbols
3. Training on Colab used the same empty database, so no crypto models were trained
4. Live trader only loads models that exist, so no crypto models = no crypto trading

## The Data Flow

```
Symbol Database (must have crypto)
    → Selection (picks best symbols including crypto)
    → Training (produces models for selected symbols)
    → Models (BTCUSD_1Hour.pt, ETHUSD_1Hour.pt, etc.)
    → Live Trader (loads models that exist)
```

**If crypto is missing at ANY step, the chain breaks.**

## Solution: Two-Part Fix

### Part 1: Populate Database with Crypto (Before Training)

```python
from alpaca_trading.selection.symbol_database import SymbolDatabase

db = SymbolDatabase('data/trading.db')
count = db.update_crypto(verbose=True)
print(f'Added {count} crypto symbols')

# Verify
crypto = db.get_candidates(asset_types=['crypto'], skip_volume_filter_for_crypto=True)
print(f'Crypto in database: {len(crypto)}')
# Expected: 25 symbols (BTC/USD, ETH/USD, SOL/USD, etc.)
```

### Part 2: Live Trader Graceful Fallback (When No Crypto Models)

In `scripts/live_trader.py`, detect if crypto models exist and adjust config:

```python
# Detect crypto models (symbols ending with 'USD' or containing '/')
model_symbols_list = list(available_predictors)
crypto_models = [s for s in model_symbols_list if s.endswith('USD') or '/' in s]
has_crypto_models = len(crypto_models) > 0

selection_config = SelectionConfig(
    max_correlation=config.max_correlation,
    min_crypto_positions=1 if has_crypto_models else 0,  # Graceful fallback
)
```

**Key insight**: The live trader should work with whatever models exist, not fail because training didn't include crypto.

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Set `min_crypto_positions=0` globally | Defeats purpose of 24/7 trading coverage | Only set to 0 when no crypto models exist |
| Assume database has crypto | Database starts empty | Always verify with `db.get_candidates()` |
| Add crypto to selection without database | Selection only sees symbols in database | Database is the source of truth |
| Skip selection validation | Silent failures are worse | Keep validation, add graceful fallback |

## Crypto Symbols Available (Alpaca API)

The Alpaca API provides 25 USD trading pairs:

| Major | DeFi | Meme/Other |
|-------|------|------------|
| BTC/USD | UNI/USD | DOGE/USD |
| ETH/USD | AAVE/USD | SHIB/USD |
| SOL/USD | LINK/USD | PEPE/USD |
| XRP/USD | SUSHI/USD | TRUMP/USD |
| LTC/USD | CRV/USD | SKY/USD |
| BCH/USD | YFI/USD | |
| AVAX/USD | GRT/USD | |
| DOT/USD | | |

## Workflow for Training with Crypto

1. **Before zipping for Colab**, verify database has crypto:
   ```python
   from alpaca_trading.selection.symbol_database import SymbolDatabase
   db = SymbolDatabase('data/trading.db')

   # Check current state
   crypto = db.get_candidates(asset_types=['crypto'], skip_volume_filter_for_crypto=True)
   print(f'Crypto in database: {len(crypto)}')

   # Populate if needed
   if len(crypto) == 0:
       db.update_crypto(verbose=True)
   ```

2. **Zip and upload to Colab** - database now includes crypto

3. **Run selection** - crypto symbols will be included in candidates

4. **Train** - will produce `BTCUSD_1Hour.pt`, `ETHUSD_1Hour.pt`, etc.

5. **Download models** to `models/rl_symbols/`

6. **Live trader** will automatically:
   - Detect crypto models (symbols ending in `USD` or containing `/`)
   - Set `min_crypto_positions=1`
   - Trade crypto 24/7 when equity markets closed

## Key Insights

1. **Database is source of truth**: Selection only sees symbols that are in the database
2. **Graceful degradation > hard failure**: Live trader should work with available models
3. **Validation still matters**: Keep the CRYPTO VIOLATION check, but handle gracefully
4. **24/7 trading requires crypto**: `min_crypto_positions=1` ensures coverage when markets closed

## Files Modified

```
scripts/live_trader.py:
  - Line 2174-2182: Detect crypto models, set min_crypto_positions accordingly

alpaca_trading/selection/symbol_database.py:
  - update_crypto(): Populates database with crypto symbols from Alpaca API
```

## Related Skills

- `selection-diversity-validation`: The validation that catches missing crypto
- `crypto-hard-filter-simplification`: Why crypto fails filters (yfinance data issues)
- `data-source-priority`: Alpaca API has better crypto data than yfinance

## References

- `alpaca_trading/selection/symbol_database.py`: `update_crypto()` method
- `alpaca_trading/data/pipeline.py`: `list_crypto_symbols()` function
- `scripts/live_trader.py`: Lines 2174-2182 (crypto model detection)
