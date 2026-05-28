# Exchange Tentacles

## Creating Exchange Connector

### Directory Structure
```
Trading/Exchange/my_exchange/
├── __init__.py
├── my_exchange.py
├── metadata.json
└── tests/
    └── test_my_exchange.py
```

### Basic Exchange Implementation

```python
# my_exchange.py
from octobot_trading.exchanges import RestExchange

class MyExchange(RestExchange):
    DESCRIPTION = "MyExchange cryptocurrency exchange"
    
    # Optional: specify if not using CCXT
    DEFAULT_CONNECTOR_CLASS = None
    
    @classmethod
    def get_name(cls):
        """Return lowercase exchange name (must match CCXT)"""
        return "myexchange"
    
    @classmethod
    def is_supporting_exchange(cls, exchange_candidate_name: str) -> bool:
        """Check if this tentacle handles given exchange"""
        return cls.get_name() == exchange_candidate_name
    
    def get_adapter_class(self):
        """Return adapter for exchange-specific features"""
        from octobot_trading.exchanges.adapters import MyExchangeAdapter
        return MyExchangeAdapter
```

### Custom Connector

If exchange requires custom CCXT connector:

```python
from octobot_trading.exchanges.connectors import CCXTConnector

class MyExchangeConnector(CCXTConnector):
    @classmethod
    def get_name(cls):
        return "myexchange"
    
    async def create_order(self, order_type, symbol, quantity, price=None):
        """Custom order creation logic"""
        # Custom implementation
        return await super().create_order(order_type, symbol, quantity, price)
```

## Exchange Adapter

Adapters handle exchange-specific quirks.

```python
# my_exchange_adapter.py
from octobot_trading.exchanges.adapters import ExchangeAdapter

class MyExchangeAdapter(ExchangeAdapter):
    def adapt_order(self, order):
        """Convert OctoBot order format to exchange format"""
        adapted = order.copy()
        # Exchange-specific adaptations
        if order['type'] == 'limit':
            adapted['timeInForce'] = 'GTC'
        return adapted
    
    def parse_balance(self, balance):
        """Parse exchange-specific balance format"""
        return {
            'free': float(balance.get('available', 0)),
            'used': float(balance.get('locked', 0)),
            'total': float(balance.get('total', 0))
        }
    
    def fix_market_status(self, market_status):
        """Handle exchange-specific market info"""
        # Some exchanges have different precision formats
        market_status['precision'] = {
            'amount': 8,
            'price': 2
        }
        return market_status
```

## WebSocket Support

### WebSocket Tentacle

```python
from octobot_trading.exchanges import ExchangeWebSocketConnector

class MyExchangeWebSocket(ExchangeWebSocketConnector):
    DESCRIPTION = "MyExchange WebSocket feed"
    
    @classmethod
    def get_name(cls):
        return "myexchange_websocket"
    
    async def _subscribe_channels(self):
        """Subscribe to WebSocket channels"""
        for symbol in self.symbols:
            await self.subscribe_ticker(symbol)
            await self.subscribe_trades(symbol)
            await self.subscribe_order_book(symbol)
    
    async def _handle_message(self, message):
        """Process incoming WebSocket messages"""
        if message['type'] == 'ticker':
            await self._handle_ticker(message)
        elif message['type'] == 'trade':
            await self._handle_trade(message)
```

## Testing Exchange Tentacles

```python
# tests/test_my_exchange.py
import pytest
from ...my_exchange import MyExchange

@pytest.mark.asyncio
async def test_exchange_initialization():
    exchange = MyExchange()
    assert exchange.get_name() == "myexchange"

@pytest.mark.asyncio
async def test_order_creation():
    exchange = MyExchange()
    # Mock exchange connection
    exchange.connector = MockConnector()
    
    order = await exchange.create_market_order(
        symbol="BTC/USDT",
        side="buy",
        amount=0.001
    )
    assert order is not None
```

## Integration with CCXT

### Using Existing CCXT Exchange

```python
class Binance(RestExchange):
    DESCRIPTION = "Binance exchange"
    
    @classmethod
    def get_name(cls):
        return "binance"  # Must match CCXT exchange ID
    
    @property
    def connector_class(self):
        from octobot_trading.exchanges.connectors import CCXTConnector
        return CCXTConnector
```

### Custom CCXT Modifications

If CCXT needs patching for specific exchange:

```python
class MyExchange(RestExchange):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply CCXT patches
        self._apply_ccxt_patches()
    
    def _apply_ccxt_patches(self):
        """Patch CCXT for exchange quirks"""
        # Example: fix fee structure
        self.connector.client.fees = {
            'trading': {
                'maker': 0.001,
                'taker': 0.002
            }
        }
```

## Metadata Example

```json
{
    "version": "1.5.2",
    "origin_package": "OctoBot-Default-Tentacles",
    "tentacles": ["MyExchange", "MyExchangeWebSocket"],
    "tentacles-requirements": [],
    "requirements": []
}
```
