# Tentacles

## Overview

Tentacles are OctoBot's plugin system - self-contained modules that extend functionality without modifying core code. They enable community contributions and customization.

## Tentacle Structure

Every tentacle must follow this structure:

```
my_exchange/
├── __init__.py              # Required: Package marker
├── my_exchange_exchange.py  # Main class file
├── metadata.json            # Required: Tentacle metadata
├── resources/               # Optional: Icons, configs
│   └── icon.png
└── tests/                   # Recommended: Test suite
    ├── __init__.py
    └── test_my_exchange.py
```

### Required Files

#### `__init__.py`
Empty file or imports for package initialization:
```python
# __init__.py - can be empty or export main classes
from .my_exchange_exchange import MyExchange
```

#### Main Class File
Named `{tentacle_name}_{tentacle_type}.py`:
- Exchange: `binance_exchange.py`
- WebSocket: `binance_websocket.py`
- Connector: `binance_connector.py`
- Mode: `grid_trading_mode.py`

#### `metadata.json`
**Must be JSON, not YAML**:
```json
{
  "version": "1.0.0",
  "origin_package": "OctoBot-Default-Tentacles",
  "tentacles": ["MyExchange"],
  "requirements": ["ccxt>=4.0.0"],
  "tentacles-requirements": []
}
```

**Critical**: `origin_package` must be `"OctoBot-Default-Tentacles"` for official tentacles.

---

## Exchange Tentacles

Exchange tentacles connect OctoBot to cryptocurrency exchanges.

### Minimal Exchange Tentacle

```python
# binance_exchange.py
from octobot_trading.exchanges import RestExchange

class Binance(RestExchange):
    DESCRIPTION = "Binance exchange connector"
    DEFAULT_CONNECTOR_CLASS = None  # Or custom connector
    
    @classmethod
    def get_name(cls) -> str:
        """Return lowercase exchange name matching CCXT identifier"""
        return "binance"
```

### Key Components

#### Base Class
Inherit from `RestExchange`:
```python
from octobot_trading.exchanges import RestExchange

class MyExchange(RestExchange):
    pass
```

#### Required Attributes
1. **DESCRIPTION** (str): Human-readable description
2. **DEFAULT_CONNECTOR_CLASS**: Connector class or `None` for CCXT default

#### Required Methods
1. **get_name()** - Return lowercase exchange identifier
   ```python
   @classmethod
   def get_name(cls) -> str:
       return "myexchange"  # Must match CCXT exchange ID
   ```

### Optional Overrides

#### Custom Authentication
```python
async def get_adapter_class(self, adapter_class):
    """Override for custom authentication"""
    return CustomAuthAdapter
```

#### Rate Limiting
```python
async def get_rate_limit(self):
    """Custom rate limiting"""
    return 50  # requests per second
```

#### Market Filters
```python
def get_market_filter(self, symbol: str, config: dict) -> bool:
    """Filter tradeable markets"""
    return "SPOT" in config.get("market_type", "")
```

---

## WebSocket Tentacles

WebSocket tentacles provide real-time data feeds.

### Minimal WebSocket Tentacle

```python
# binance_websocket.py
from octobot_trading.exchanges.websockets import AbstractWebSocket

class BinanceWebSocket(AbstractWebSocket):
    EXCHANGE_FEEDS = {
        "trades": "trade",
        "kline": "kline",
        "ticker": "ticker"
    }
    
    @classmethod
    def get_name(cls) -> str:
        return "binance"
    
    async def _handle_trade_update(self, data: dict):
        """Process trade updates"""
        await self.push_to_channel("trades", data)
```

### Feed Configuration
Map internal feed names to exchange-specific endpoints:
```python
EXCHANGE_FEEDS = {
    "trades": "trade",       # Trade stream
    "kline": "kline_1m",     # Candlestick data
    "ticker": "ticker",      # Price ticker
    "book": "depth20"        # Order book
}
```

---

## Connector Tentacles

Connectors handle exchange-specific API quirks.

### CCXT Connector

Most exchanges use the default CCXT connector:
```python
class Binance(RestExchange):
    DEFAULT_CONNECTOR_CLASS = None  # Uses CCXTConnector automatically
```

### Custom Connector

For exchanges needing special handling:
```python
# binance_connector.py
from octobot_trading.exchanges.connectors import CCXTConnector

class BinanceConnector(CCXTConnector):
    async def get_balance(self):
        """Override balance fetching"""
        raw_balance = await super().get_balance()
        return self._transform_balance(raw_balance)
    
    def _transform_balance(self, balance: dict) -> dict:
        """Custom balance transformation"""
        # Handle Binance-specific balance format
        return transformed_balance
```

Then reference it:
```python
class Binance(RestExchange):
    DEFAULT_CONNECTOR_CLASS = BinanceConnector
```

---

## Mode Tentacles

Trading strategies and execution modes.

### Minimal Mode Tentacle

```python
# grid_trading_mode.py
from octobot_trading.modes import AbstractTradingMode

class GridTradingMode(AbstractTradingMode):
    @classmethod
    def get_mode_name(cls) -> str:
        return "grid_trading"
    
    async def create_new_orders(self, symbol: str, exchange: str):
        """Generate grid orders"""
        grid_orders = self._calculate_grid(symbol)
        for order in grid_orders:
            await self.create_order(order)
```

---

## Evaluator Tentacles

Signal generators and technical indicators.

```python
# rsi_evaluator.py
from octobot_evaluators.evaluators import TechnicalEvaluator

class RSIEvaluator(TechnicalEvaluator):
    async def eval_impl(self):
        """Calculate RSI and generate signal"""
        rsi = self._calculate_rsi()
        if rsi < 30:
            await self.evaluation_completed(1)  # Buy signal
        elif rsi > 70:
            await self.evaluation_completed(-1)  # Sell signal
```

---

## Service Tentacles

External integrations (notifications, webhooks, etc.).

```python
# telegram_service.py
from octobot_services.services import AbstractService

class TelegramService(AbstractService):
    async def send_notification(self, message: str):
        """Send Telegram notification"""
        await self.telegram_api.send_message(message)
```

---

## Tentacle Testing

### Test Structure
Place tests alongside tentacle code:
```
binance/
├── __init__.py
├── binance_exchange.py
├── metadata.json
└── tests/
    ├── __init__.py
    └── test_binance_exchange.py
```

### Test Imports
Use **relative imports** to reference tentacle classes:
```python
# test_binance_exchange.py
import pytest
from ...binance import Binance  # Relative import

@pytest.mark.asyncio
async def test_exchange_initialization():
    exchange = Binance()
    assert exchange.get_name() == "binance"
```

### Fixtures
```python
@pytest.fixture
def mock_exchange_config():
    return {
        "api_key": "test_key",
        "api_secret": "test_secret"
    }
```

### Run Tests
```bash
cd OctoBot-Tentacles/Trading/Exchange/binance/tests
pytest
```

---

## Tentacle Generation

Export tentacles to a package:
```bash
cd OctoBot
python start.py tentacles -p ../../tentacles_default_export.zip -d ../OctoBot-Tentacles
```

**Parameters**:
- `-p`: Output package path
- `-d`: Source tentacles directory

---

## Tentacle Installation

Install tentacles from a package:
```bash
python start.py tentacles --install --all
```

Install specific tentacles:
```bash
python start.py tentacles --install binance coinbase
```

---

## Common Patterns

### Exchange Configuration
```python
class MyExchange(RestExchange):
    @classmethod
    def get_exchange_config(cls, config: dict) -> dict:
        """Merge tentacle config with default config"""
        return {
            **super().get_exchange_config(config),
            "enableRateLimit": True,
            "options": {
                "defaultType": "spot"
            }
        }
```

### Error Handling
```python
from octobot_trading.errors import ExchangeError

class MyExchange(RestExchange):
    async def fetch_balance(self):
        try:
            return await super().fetch_balance()
        except ExchangeError as e:
            self.logger.error(f"Balance fetch failed: {e}")
            return {}
```

### Async Initialization
```python
async def initialize_impl(self):
    """Custom initialization"""
    await super().initialize_impl()
    self.custom_data = await self._load_custom_data()
```

---

## Debugging Tentacles

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### VS Code Launch Config
Use "OctoBot with tentacles" launch configuration with `PYTHONPATH` set.

### Common Issues

#### Import Errors
- Check `PYTHONPATH` includes tentacle directories
- Verify `__init__.py` files exist
- Use correct import patterns (absolute for code, relative for tests)

#### Tentacle Not Found
- Ensure `metadata.json` exists and is valid JSON
- Check `origin_package` matches expected value
- Verify tentacle is registered in tentacles config

#### Test Failures
- Use relative imports: `from ...tentacle_name import Class`
- Mock external dependencies (exchanges, APIs)
- Run with `pytest -v` for verbose output
