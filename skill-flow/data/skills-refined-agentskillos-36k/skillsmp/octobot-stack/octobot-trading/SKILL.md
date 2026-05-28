---
name: octobot-trading
description: Core trading engine for OctoBot. Handles exchange connections, order execution, portfolio management, and trading modes. Use when modifying trading logic, adding exchanges, or working with orders and positions.
version: 1.0.0
license: MIT
---

# OctoBot-Trading Development

Help developers work with OctoBot's core trading engine - the foundational library for exchange integration, order management, and portfolio tracking.

## References

Consult these resources as needed:
- ./references/modules.md -- Detailed module documentation (exchanges, orders, portfolio, modes)
- ./references/integrations.md -- CCXT integration, exchange connectors, WebSocket feeds
- ./references/testing.md -- Testing patterns, fixtures, and async test strategies

## Overview

OctoBot-Trading is a **Core Layer** library providing:
- Exchange API abstractions (via CCXT)
- Order lifecycle management
- Portfolio and position tracking
- Trading mode framework
- Signal system for strategy coordination
- Blockchain wallet integration (abstract classes)

**Layer Position**: Core (no dependencies on Application or Extension layers)
**Used By**: OctoBot, OctoBot-Backtesting, OctoBot-Evaluators, tentacles

## Module Structure

```
octobot_trading/
├── exchanges/           # Exchange API abstractions
│   ├── abstract_exchange.py      # RestExchange base class
│   ├── ccxt_connector.py          # CCXT integration
│   └── connectors/                # Exchange-specific connectors
├── personal_data/       # Trading data management
│   ├── orders/         # Order lifecycle
│   ├── portfolio/      # Balance tracking
│   ├── positions/      # Leveraged positions
│   └── trades/         # Trade history
├── modes/              # Trading mode framework
├── signals/            # Trading signal system
├── accounts/           # Account management
├── blockchain_wallets/ # Blockchain wallet abstractions
├── storage/            # Data persistence
└── util/              # Trading utilities
```

## Key Concepts

### Exchanges
Unified interface for cryptocurrency exchange APIs:
```python
from octobot_trading.exchanges import RestExchange

class MyExchange(RestExchange):
    @classmethod
    def get_name(cls):
        return "myexchange"
    
    async def fetch_balance(self):
        return await self.connector.get_balance()
```

### Orders
Order lifecycle management with states (pending, open, filled, canceled):
```python
from octobot_trading.personal_data import Order

order = Order(trader)
await order.initialize(order_type="limit", side="buy", 
                       symbol="BTC/USDT", amount=1.0, price=50000)
await order.update(status="filled")
```

### Portfolio
Real-time balance and PNL tracking:
```python
from octobot_trading.personal_data import Portfolio

portfolio = Portfolio(trader)
balance = await portfolio.get_balance()
pnl = portfolio.calculate_pnl()
```

### Modes
High-level trading strategies:
```python
from octobot_trading.modes import AbstractTradingMode

class GridMode(AbstractTradingMode):
    async def create_new_orders(self, symbol, exchange):
        # Generate grid orders
        pass
```

## Common Tasks

### Add New Exchange
1. Create exchange tentacle in OctoBot-Tentacles
2. Inherit from `RestExchange`
3. Implement `get_name()` classmethod
4. Optional: Create custom connector

See [references/integrations.md](./references/integrations.md) for details.

### Modify Order Execution
Orders are managed in `personal_data/orders/`:
- `order.py` - Core Order class
- `order_manager.py` - Order execution coordinator
- Test changes with order fixtures

### Extend Portfolio Tracking
Portfolio logic in `personal_data/portfolio/`:
- `portfolio.py` - Balance management
- `position.py` - Leveraged positions
- `portfolio_manager.py` - Multi-exchange coordination

### Add Trading Mode
1. Inherit from `AbstractTradingMode`
2. Implement `create_new_orders()`
3. Register mode in tentacles
4. Add configuration schema

## Integration Points

### CCXT Library
OctoBot-Trading uses CCXT for exchange standardization:
- **Connector**: `ccxt_connector.py` wraps CCXT calls
- **Error Handling**: Maps CCXT exceptions to OctoBot errors
- **Rate Limiting**: Respects exchange rate limits

### Async-Channel
Decoupled messaging for components:
```python
from async_channel import Channel, Producer
channel = Channel()
producer = Producer(channel)
await producer.send({"event": "order_filled", "order_id": "123"})
```

### OctoBot-Backtesting
Trading engine operates in simulation mode:
- Exchange APIs return historical data
- Orders executed against simulated order book
- Portfolio tracks paper trading balances

## Quick Reference

### Import Patterns
```python
# Exchanges
import octobot_trading.exchanges as exchanges
from octobot_trading.exchanges import RestExchange

# Orders
import octobot_trading.personal_data as personal_data
from octobot_trading.personal_data import Order

# Modes
from octobot_trading.modes import AbstractTradingMode
```

### Async Patterns
```python
# Entry point
asyncio.run(main())

# Concurrent operations
tasks = [
    asyncio.create_task(fetch_balance()),
    asyncio.create_task(fetch_orders())
]
results = await asyncio.gather(*tasks)
```

### Testing
```python
import pytest

@pytest.fixture
def mock_exchange():
    return MockExchange()

@pytest.mark.asyncio
async def test_order_creation(mock_exchange):
    order = Order(mock_exchange)
    await order.initialize()
    assert order.status == "pending"
```

## Checklist

Before committing changes:
- [ ] Imports use `octobot_trading.*` pattern
- [ ] Async operations use `asyncio` correctly
- [ ] Tests added for new functionality
- [ ] Error handling follows CCXT patterns
- [ ] No dependencies on Application/Extension layers
- [ ] Documentation updated for public APIs