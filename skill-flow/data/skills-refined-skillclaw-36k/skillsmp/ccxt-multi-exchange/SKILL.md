---
name: ccxt-multi-exchange
description: "CCXT multi-exchange crypto broker integration for better liquidity during after-hours capital shift"
author: Claude Code
date: 2026-01-26
version: 3.5.0
---

# CCXT Multi-Exchange Integration - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-26 |
| **Goal** | Improve crypto liquidity during after-hours by routing to multiple US-regulated exchanges |
| **Environment** | Python 3.11+, ccxt>=4.0.0 |
| **Status** | Success |

## Context
Alpaca reports **platform-specific volume**, not global exchange volume:

| Metric | Alpaca Platform | Global Exchange |
|--------|-----------------|-----------------|
| BTC/USD daily volume | ~$250k-$750k | ~$30B |
| Hourly liquidity | ~5-15 BTC | Effectively unlimited |
| Impact | Slippage risk, partial fills | Minimal |

**Additional Alpaca Limitations:**
- Long-only (no crypto shorting)
- 25 pairs only
- No trailing stops for crypto

**Solution:** Use CCXT unified library to route to US-regulated exchanges with better liquidity during capital shift (after-hours/weekends).

## Verified Workflow

### 1. Architecture
```
Market Hours (9:30-4:00 ET):
  └── Alpaca (equities + crypto)

After Hours / Weekends (shifted):
  └── CCXT Unified Interface
        ├── Coinbase (primary - best compliance)
        ├── Kraken (secondary - lower fees)
        └── Binance.US (tertiary - if needed)
```

### 2. CCXTBroker Class (AlpacaBroker Interface)
```python
from alpaca_trading.trading.ccxt_broker import CCXTBroker, CCXTBrokerConfig

config = CCXTBrokerConfig(
    exchanges=['coinbase', 'kraken'],
    keys_file='API_key_CCXT.txt',
    sandbox=False,
    rate_limit_buffer_ms=100,
    max_retries=3,
)

broker = CCXTBroker(config)

# AlpacaBroker-compatible interface
account = broker.get_account()        # Aggregated across exchanges
positions = broker.get_positions()    # All exchange positions
order = broker.submit_order(          # Routes to best exchange
    symbol='BTC/USD',
    qty=0.01,
    side='buy',
    type='limit',
    limit_price=50000,
)
```

### 3. Exchange Selection Logic
```python
from alpaca_trading.trading.exchange_selector import ExchangeSelector

selector = ExchangeSelector(
    broker=ccxt_broker,
    min_balance_buffer=100.0,  # Keep $100 buffer
    prefer_maker=True,          # Prioritize lower maker fees
)

# Find best exchange for a trade
result = selector.select_exchange(
    symbol='BTC/USD',
    side='buy',
    notional=10000,  # $10k trade
)
# Returns: ExchangeScore(exchange_id='coinbase', score=145.0, ...)
```

### 4. Capital Shift Integration
```python
from alpaca_trading.risk.capital_shift import CapitalShiftManager, CapitalShiftConfig

config = CapitalShiftConfig(
    enabled=True,
    shift_fraction=0.75,
    max_crypto_allocation=0.50,
    use_ccxt_when_shifted=True,     # Enable CCXT routing
    ccxt_keys_file='API_key_CCXT.txt',
)

shift_mgr = CapitalShiftManager(
    config,
    alpaca_broker=alpaca_broker,
    ccxt_broker=ccxt_broker,
)

# Get appropriate broker based on shift status
allocation = shift_mgr.calculate_asset_allocations(...)
crypto_broker = shift_mgr.get_crypto_broker(allocation)
# Returns CCXT broker when shifted, Alpaca otherwise
```

### 5. Credentials File Format
```
# API_key_CCXT.txt (NOT in git)
coinbase_api_key=your_api_key_here
coinbase_secret=your_secret_here
kraken_api_key=your_api_key_here
kraken_secret=your_secret_here
binanceus_api_key=your_api_key_here
binanceus_secret=your_secret_here
```

### 6. CLI Usage
```bash
# Enable CCXT for after-hours crypto
python scripts/live_trader.py --paper 1 --use-ccxt 1 --ccxt-keys-file API_key_CCXT.txt

# Without CCXT (Alpaca only)
python scripts/live_trader.py --paper 1 --capital-shift 1
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Single exchange only | Insufficient funds during large trades | Multi-exchange failover essential |
| Using non-US exchanges | Regulatory compliance issues | Stick to Coinbase, Kraken, Binance.US |
| Hardcoded symbol mapping | BTC/USD vs BTC/USDT varies by exchange | Dynamic symbol mapping per exchange |
| No rate limit handling | 429 errors during high activity | Use CCXT's built-in rate limiting + buffer |
| Immediate failover | Network glitches caused unnecessary switches | Retry 3x before failover |
| Not checking balance before routing | Insufficient funds errors after exchange selection | Balance-aware exchange selection |
| Same credentials file as Alpaca | Confusing, different key formats | Separate API_key_CCXT.txt file |
| Not handling sandbox mode | Test orders hit live exchanges | Pass sandbox=True in config |

## Final Parameters
```python
# Recommended CCXT configuration
CCXTBrokerConfig(
    exchanges=['coinbase', 'kraken'],  # US-regulated only
    sandbox=False,                      # True for testing
    rate_limit_buffer_ms=100,           # Extra safety margin
    max_retries=3,                      # Before exchange failover
)

# Exchange priority and fees
EXCHANGE_PRIORITY = {
    'coinbase': 1,      # Primary - best US compliance
    'kraken': 2,        # Secondary - lower fees (0.16%)
    'binanceus': 3,     # Tertiary - regulatory concerns
}

EXCHANGE_FEES = {
    'coinbase': {'maker': 0.004, 'taker': 0.006},  # 0.4%/0.6%
    'kraken': {'maker': 0.0016, 'taker': 0.0026},  # 0.16%/0.26%
    'binanceus': {'maker': 0.001, 'taker': 0.001}, # 0.1%/0.1%
}
```

## Key Insights
- **AlpacaBroker interface**: CCXTBroker mirrors Alpaca's interface for drop-in replacement
- **Lazy initialization**: CCXT broker only created when first needed during shift
- **Position aggregation**: `get_positions()` returns positions from ALL exchanges
- **Symbol mapping**: BTC/USD on Alpaca may be BTC/USDT on Binance.US
- **Error handling**: Catch `ccxt.InsufficientFunds`, `ccxt.RateLimitExceeded`, `ccxt.NetworkError`
- **Sandbox support**: Coinbase has sandbox, Kraken/Binance.US don't - use small amounts
- **Reconciliation**: Must reconcile positions across BOTH Alpaca and CCXT

## Files Created/Modified

| File | Action | Description |
|------|--------|-------------|
| `alpaca_trading/trading/ccxt_broker.py` | Created | CCXT broker wrapper |
| `alpaca_trading/trading/exchange_selector.py` | Created | Exchange routing logic |
| `alpaca_trading/data/fetcher.py` | Modified | Added `fetch_crypto_ohlcv_ccxt()` |
| `alpaca_trading/risk/capital_shift.py` | Modified | Dual broker support, `get_crypto_broker()` |
| `scripts/live_trader.py` | Modified | `--use-ccxt`, `--ccxt-keys-file` args |
| `config/requirements.txt` | Modified | Added `ccxt>=4.0.0` |
| `CLAUDE.md` | Modified | CCXT documentation section |

## Testing Checklist
```python
# Verify these scenarios:
1. [ ] CCXT broker initializes with valid credentials
2. [ ] Exchange failover on InsufficientFunds
3. [ ] get_positions() aggregates across exchanges
4. [ ] submit_order() routes to best exchange
5. [ ] Capital shift activates CCXT when shifted
6. [ ] Capital shift uses Alpaca when not shifted
7. [ ] Symbol mapping works (BTC/USD -> BTC/USDT)
8. [ ] Sandbox mode prevents live orders during testing
9. [ ] Position reconciliation across both brokers
10. [ ] Rate limiting prevents 429 errors
```

## References
- CCXT Library: https://github.com/ccxt/ccxt
- CCXT Documentation: https://docs.ccxt.com/
- Coinbase Advanced Trade API: https://docs.cdp.coinbase.com/
- Kraken API: https://docs.kraken.com/
- Binance.US API: https://docs.binance.us/
