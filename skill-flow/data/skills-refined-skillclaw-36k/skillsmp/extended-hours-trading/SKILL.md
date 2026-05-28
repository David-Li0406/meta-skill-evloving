---
name: extended-hours-trading
description: "Extended hours trading support for pre-market and after-hours sessions via Alpaca"
author: Claude Code
date: 2026-01-26
version: 3.6.0
---

# Extended Hours Trading - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2026-01-26 |
| **Goal** | Enable trading during pre-market (4 AM - 9:30 AM ET) and after-hours (4 PM - 8 PM ET) |
| **Environment** | Python 3.10+, alpaca-py |
| **Status** | Success |

## Context
Standard US equity market hours (9:30 AM - 4:00 PM ET) miss important trading opportunities:

| Session | Time (ET) | Key Events |
|---------|-----------|------------|
| Pre-market | 4:00 AM - 9:30 AM | Earnings releases, overnight news, European market influence |
| Regular | 9:30 AM - 4:00 PM | Standard trading |
| After-hours | 4:00 PM - 8:00 PM | After-close earnings, breaking news |
| Closed | 8:00 PM - 4:00 AM | No equity trading (crypto still active) |

**Alpaca Extended Hours Requirements:**
- Order type: **LIMIT only** (market orders rejected)
- `time_in_force='day'` required
- `extended_hours=True` parameter on order request
- Bracket orders and trailing stops NOT supported

## Verified Workflow

### 1. Check if in Extended Session
```python
from alpaca_trading.market_hours import is_extended_hours_session, get_market_session, MarketSession

# Check if currently in extended session
if is_extended_hours_session("AAPL"):
    # Must use limit orders with extended_hours=True
    print("In extended session - use limit orders only")

# Get specific session type
session = get_market_session("AAPL")
# Returns: MarketSession.PRE_MARKET, .REGULAR_HOURS, .AFTER_HOURS, or .CLOSED
```

### 2. Submit Extended Hours Orders
```python
from alpaca_trading.trading.broker import Broker

# Extended hours orders MUST use limit orders
broker.submit_order(
    symbol="AAPL",
    qty=10,
    side="buy",
    type="limit",           # REQUIRED - market orders rejected
    time_in_force="day",    # REQUIRED - automatically enforced
    limit_price=150.0,
    extended_hours=True,    # Enable extended hours
)

# Validation built in - this raises ValueError:
broker.submit_order(
    symbol="AAPL",
    qty=10,
    side="buy",
    type="market",          # NOT ALLOWED
    extended_hours=True,    # Raises: "extended_hours=True requires type='limit'"
)
```

### 3. Live Trader CLI
```bash
# Enable extended hours trading (forces limit orders)
python scripts/live_trader.py --paper 1 --extended-hours 1

# Combined with CCXT for full 24/7 coverage
python scripts/live_trader.py --paper 1 --extended-hours 1 --use-ccxt 1
```

### 4. Capital Shift Timing Adjustment
When extended hours is enabled, capital shift timing changes:

| Mode | Shift Start | Restore Time |
|------|-------------|--------------|
| Regular (`--extended-hours 0`) | 4:15 PM ET | 9:15 AM ET |
| Extended (`--extended-hours 1`) | 8:15 PM ET | 3:45 AM ET |

```python
from alpaca_trading.risk.capital_shift import CapitalShiftConfig, CapitalShiftManager

config = CapitalShiftConfig(
    enabled=True,
    extended_hours_enabled=True,  # Shift at 8:15 PM instead of 4:15 PM
    shift_fraction=0.75,
    max_crypto_allocation=0.50,
)

manager = CapitalShiftManager(config, alpaca_broker=broker)

# is_equity_market_open now considers 4 AM - 8 PM as "open"
is_open = manager.is_equity_market_open()  # True at 6 AM with extended hours
```

### 5. Dashboard Session Display
The web dashboard shows session type in the header:

| Session | Color | Text |
|---------|-------|------|
| Pre-market | Orange | PRE-MARKET |
| Regular | Green | MARKET OPEN |
| After-hours | Purple | AFTER-HOURS |
| Closed | Red | MARKET CLOSED |

API endpoint `/api/v1/market/status` returns:
```json
{
  "equity_market": "closed",
  "equity_session": "pre_market",
  "crypto_market": "open",
  "next_open": "2024-01-16T14:30:00Z",
  "timestamp": "2024-01-16T10:00:00Z"
}
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Market orders in extended hours | Alpaca rejects them outright | Must validate type='limit' before submission |
| time_in_force='gtc' | Alpaca requires 'day' for extended hours | Force time_in_force='day' when extended_hours=True |
| Bracket orders | Not supported in extended hours | Use simple limit orders, manage stops manually |
| Trailing stops | Not supported in extended hours | Implement manual trailing logic |
| Not checking session type | Submitted regular orders during extended session | Check is_extended_hours_session() before order |
| Using Alpaca clock API only | Doesn't distinguish pre/after-hours | Use get_market_session() for session type |
| Capital shift at 4:15 PM | Missed extended hours trading opportunity | Add extended_hours_enabled to CapitalShiftConfig |
| Testing on MLK Day | Jan 15, 2024 is a holiday - all tests failed | Use Jan 16 or other non-holiday dates |

## Final Parameters
```python
# Extended hours validation in broker.py
if extended_hours:
    if str(type).lower() != "limit":
        raise ValueError("extended_hours=True requires type='limit'")
    if time_in_force.lower() != "day":
        logger.warning("extended_hours=True requires time_in_force='day', forcing")
        time_in_force = "day"

# Session time boundaries (market_hours.py)
STOCK_PREMARKET_OPEN = time(4, 0)    # 4:00 AM ET
STOCK_MARKET_OPEN = time(9, 30)       # 9:30 AM ET
STOCK_MARKET_CLOSE = time(16, 0)      # 4:00 PM ET
STOCK_AFTERHOURS_CLOSE = time(20, 0)  # 8:00 PM ET

# Live trader CLI validation
if args.extended_hours and not args.use_limit_orders:
    logger.warning("Extended hours requires limit orders. Forcing --use-limit-orders=1")
    args.use_limit_orders = 1
```

## Key Insights
- **Crypto unaffected**: is_extended_hours_session() returns False for crypto (always tradeable)
- **Weekends**: Extended hours only applies to weekdays - weekends return False
- **Holidays**: Market holidays return CLOSED session regardless of time
- **Order validation**: Validation happens in broker.py before API call - fails fast
- **Dashboard sync**: WebSocket pushes equity_session for real-time UI updates
- **Capital shift integration**: Extended hours extends trading window, delays crypto shift

## Files Created/Modified

| File | Action | Description |
|------|--------|-------------|
| `alpaca_trading/trading/broker.py` | Modified | Added `extended_hours` parameter with validation |
| `alpaca_trading/trading/executor.py` | Modified | Pass-through for `extended_hours` |
| `alpaca_trading/trading/market_hours.py` | Modified | Added `is_extended_hours_session()` |
| `alpaca_trading/risk/capital_shift.py` | Modified | Added `extended_hours_enabled` config |
| `scripts/live_trader.py` | Modified | Added `--extended-hours` CLI flag |
| `alpaca_trading/api/routes/market.py` | Modified | Added `equity_session` to endpoint |
| `alpaca_trading/api/schemas.py` | Modified | Added `MarketStatus` schema |
| `alpaca_trading/api/server.py` | Modified | Added `equity_session` to WebSocket |
| `web/src/App.vue` | Modified | Session display with color coding |
| `tests/test_extended_hours.py` | Created | 17 tests for extended hours |
| `CLAUDE.md` | Modified | Extended hours documentation |

## Testing Checklist
```python
# Verify these scenarios:
1. [x] is_extended_hours_session() returns True at 6 AM for stocks
2. [x] is_extended_hours_session() returns True at 5 PM for stocks
3. [x] is_extended_hours_session() returns False at 10 AM (regular hours)
4. [x] is_extended_hours_session() returns False at 9 PM (closed)
5. [x] is_extended_hours_session() returns False for crypto (always)
6. [x] is_extended_hours_session() returns False on weekends
7. [x] broker.submit_order() raises ValueError for market orders with extended_hours=True
8. [x] broker.submit_order() accepts limit orders with extended_hours=True
9. [x] Capital shift happens at 8:15 PM with extended_hours_enabled
10. [x] Capital restores at 3:45 AM with extended_hours_enabled
11. [x] is_equity_market_open() returns True at 6 AM with extended_hours_enabled
12. [x] Dashboard shows correct session type (PRE-MARKET, AFTER-HOURS, etc.)
13. [x] --extended-hours CLI forces --use-limit-orders
14. [x] executor passes extended_hours to broker
```

## References
- Alpaca Extended Hours: https://docs.alpaca.markets/docs/extended-hours
- Alpaca Order Types: https://docs.alpaca.markets/docs/orders-at-alpaca
- US Market Hours: NYSE/NASDAQ open 9:30 AM - 4:00 PM ET, pre-market 4:00 AM, after-hours until 8:00 PM
