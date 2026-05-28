# Integrations

## CCXT Integration

### Overview
OctoBot-Trading uses CCXT (CryptoCurrency eXchange Trading Library) for standardized exchange API access.

### Architecture
```
OctoBot-Trading
    ↓
CCXTConnector (octobot_trading/exchanges/connectors/ccxt_connector.py)
    ↓
CCXT Library (ccxt/python/ccxt/)
    ↓
Exchange REST APIs
```

### CCXT Installation
CCXT is included in OctoBot requirements:
```bash
pip install ccxt
```

For custom CCXT build (with new exchanges):
```bash
cd ccxt
npm run build
```

---

## Exchange Connectors

### Default CCXT Connector
Most exchanges use the standard CCXT connector:
```python
from octobot_trading.exchanges.connectors import CCXTConnector

class CCXTConnector:
    """Standard CCXT connector"""
    
    def __init__(self, config: dict, exchange_manager):
        self.exchange_name = exchange_manager.exchange_name
        self.config = self._format_config(config)
        self.client = None
    
    async def initialize(self):
        """Initialize CCXT client"""
        import ccxt.async_support as ccxt
        exchange_class = getattr(ccxt, self.exchange_name)
        self.client = exchange_class(self.config)
    
    def _format_config(self, config: dict) -> dict:
        """Format config for CCXT"""
        return {
            'apiKey': config.get('api_key'),
            'secret': config.get('api_secret'),
            'password': config.get('password'),  # For some exchanges
            'enableRateLimit': True,
            'options': config.get('options', {})
        }
```

### Custom Connectors
For exchanges with special requirements:

#### Example: Binance Custom Connector
```python
from octobot_trading.exchanges.connectors import CCXTConnector

class BinanceConnector(CCXTConnector):
    """Binance-specific connector"""
    
    async def get_balance(self) -> dict:
        """Fetch balance with Binance-specific handling"""
        raw_balance = await self.client.fetch_balance()
        
        # Binance returns extra fields we need to filter
        return self._normalize_binance_balance(raw_balance)
    
    def _normalize_binance_balance(self, balance: dict) -> dict:
        """Convert Binance balance format"""
        normalized = {}
        info = balance.get('info', {})
        
        if 'balances' in info:  # Spot balance
            for item in info['balances']:
                asset = item['asset']
                normalized[asset] = {
                    'free': float(item['free']),
                    'used': float(item['locked']),
                    'total': float(item['free']) + float(item['locked'])
                }
        
        return normalized
    
    async def get_account_type(self) -> str:
        """Get account type (spot, margin, futures)"""
        account_info = await self.client.fapiPrivateGetAccount()
        return account_info.get('accountType', 'spot')
```

### Connector Configuration
```python
# In exchange tentacle
class Binance(RestExchange):
    DEFAULT_CONNECTOR_CLASS = BinanceConnector  # Use custom connector
    
    @classmethod
    def get_exchange_config(cls, config: dict) -> dict:
        """Merge config with Binance defaults"""
        return {
            **config,
            'options': {
                'defaultType': 'spot',  # spot, margin, future
                'adjustForTimeDifference': True
            }
        }
```

---

## WebSocket Feeds

### Purpose
Real-time market data via WebSocket connections.

### WebSocket Structure
```python
from octobot_trading.exchanges.websockets import AbstractWebSocket

class AbstractWebSocket:
    """Base WebSocket feed"""
    
    EXCHANGE_FEEDS = {}  # Feed name mappings
    
    def __init__(self, exchange_manager):
        self.exchange_manager = exchange_manager
        self.feeds = []
    
    @classmethod
    def get_name(cls) -> str:
        """Return exchange name"""
        raise NotImplementedError
    
    async def start(self):
        """Start WebSocket connections"""
        await self._init_feeds()
        await self._subscribe_feeds()
    
    async def _handle_message(self, message: dict):
        """Process WebSocket message"""
        raise NotImplementedError
```

### Example: Binance WebSocket
```python
from octobot_trading.exchanges.websockets import AbstractWebSocket

class BinanceWebSocket(AbstractWebSocket):
    """Binance WebSocket feed"""
    
    EXCHANGE_FEEDS = {
        "trades": "trade",
        "kline_1m": "kline_1m",
        "ticker": "miniTicker",
        "book": "depth20"
    }
    
    @classmethod
    def get_name(cls) -> str:
        return "binance"
    
    async def _handle_message(self, message: dict):
        """Process Binance WebSocket message"""
        event_type = message.get('e')
        
        if event_type == 'trade':
            await self._handle_trade(message)
        elif event_type == 'kline':
            await self._handle_kline(message)
        elif event_type == '24hrMiniTicker':
            await self._handle_ticker(message)
    
    async def _handle_trade(self, data: dict):
        """Process trade update"""
        trade = {
            'symbol': data['s'],
            'price': float(data['p']),
            'amount': float(data['q']),
            'timestamp': data['T'],
            'side': 'buy' if data['m'] else 'sell'
        }
        await self.push_to_channel("trades", trade)
    
    async def _handle_kline(self, data: dict):
        """Process candlestick update"""
        kline = data['k']
        candle = {
            'symbol': data['s'],
            'timestamp': kline['t'],
            'open': float(kline['o']),
            'high': float(kline['h']),
            'low': float(kline['l']),
            'close': float(kline['c']),
            'volume': float(kline['v'])
        }
        await self.push_to_channel("kline", candle)
```

### WebSocket Subscriptions
```python
async def _subscribe_feeds(self):
    """Subscribe to WebSocket feeds"""
    for feed_name, exchange_feed in self.EXCHANGE_FEEDS.items():
        if self._should_subscribe(feed_name):
            await self._subscribe(exchange_feed)

def _should_subscribe(self, feed_name: str) -> bool:
    """Check if feed should be enabled"""
    return feed_name in self.exchange_manager.config.get('feeds', [])
```

---

## Async-Channel Integration

### Purpose
Decoupled messaging between OctoBot components.

### Producer Pattern
```python
from async_channel import Channel, Producer

# Create channel
channel = Channel()

# Produce messages
producer = Producer(channel)
await producer.send({
    "event": "order_filled",
    "order_id": "123",
    "symbol": "BTC/USDT",
    "amount": 1.0
})
```

### Consumer Pattern
```python
from async_channel import Consumer

# Consume messages
consumer = Consumer(channel)
async for message in consumer:
    if message["event"] == "order_filled":
        await handle_order_filled(message)
```

### Channel Names
Defined in `octobot_commons.channels_name`:
```python
# Exchange channels
TICKER_CHANNEL = "Ticker"
RECENT_TRADES_CHANNEL = "RecentTrades"
ORDER_BOOK_CHANNEL = "OrderBook"
KLINE_CHANNEL = "Kline"

# Trading channels
ORDERS_CHANNEL = "Orders"
TRADES_CHANNEL = "Trades"
BALANCE_CHANNEL = "Balance"
POSITIONS_CHANNEL = "Positions"
```

---

## Exchange Manager

### Purpose
Coordinates exchange operations and manages connectors.

### ExchangeManager Class
```python
from octobot_trading.exchanges import ExchangeManager

class ExchangeManager:
    """Manages exchange connection and operations"""
    
    def __init__(self, config: dict, exchange_name: str):
        self.config = config
        self.exchange_name = exchange_name
        self.exchange = None  # RestExchange instance
        self.exchange_connector = None  # Connector instance
        self.is_simulated = config.get('simulated', False)
    
    async def initialize(self):
        """Initialize exchange and connector"""
        # Create exchange instance
        exchange_class = self._get_exchange_class()
        self.exchange = exchange_class(self.config, self)
        
        # Initialize connector
        connector_class = exchange_class.DEFAULT_CONNECTOR_CLASS or CCXTConnector
        self.exchange_connector = connector_class(self.config, self)
        await self.exchange_connector.initialize()
    
    def _get_exchange_class(self):
        """Load exchange class from tentacles"""
        from octobot_tentacles_manager.api import get_tentacle_class
        return get_tentacle_class(self.exchange_name, "Exchange")
```

---

## Backtesting Integration

### Simulation Mode
OctoBot-Trading operates in simulation mode during backtesting:
```python
class SimulatedExchange(RestExchange):
    """Exchange simulator for backtesting"""
    
    def __init__(self, config, exchange_manager):
        super().__init__(config, exchange_manager)
        self.simulated_orders = {}
        self.simulated_balance = config.get('initial_balance', {})
    
    async def create_order(self, order_type, side, symbol, 
                          amount, price=None):
        """Simulate order execution"""
        order_id = self._generate_order_id()
        current_price = await self._get_simulated_price(symbol)
        
        # Simulate immediate fill for market orders
        if order_type == 'market':
            status = 'closed'
            filled = amount
        else:
            status = 'open'
            filled = 0
        
        order = {
            'id': order_id,
            'type': order_type,
            'side': side,
            'symbol': symbol,
            'amount': amount,
            'price': price or current_price,
            'filled': filled,
            'remaining': amount - filled,
            'status': status
        }
        
        self.simulated_orders[order_id] = order
        return order
```

### Historical Data
```python
async def fetch_ohlcv(self, symbol: str, timeframe: str, 
                     since: int = None, limit: int = None):
    """Fetch historical candlestick data"""
    if self.is_simulated:
        # Return data from backtesting database
        return await self.backtesting_importer.get_ohlcv(
            symbol, timeframe, since, limit
        )
    else:
        # Return live data from exchange
        return await self.connector.fetch_ohlcv(
            symbol, timeframe, since, limit
        )
```

---

## Error Handling

### CCXT Error Mapping
```python
from ccxt import (
    ExchangeError, NetworkError, InvalidOrder,
    InsufficientFunds, OrderNotFound, RateLimitExceeded
)
from octobot_trading.errors import (
    ExchangeConnectionError, OrderError
)

def map_ccxt_error(error: Exception):
    """Map CCXT errors to OctoBot errors"""
    if isinstance(error, NetworkError):
        return ExchangeConnectionError(str(error))
    elif isinstance(error, InvalidOrder):
        return OrderError(str(error))
    elif isinstance(error, InsufficientFunds):
        return OrderError("Insufficient balance")
    elif isinstance(error, RateLimitExceeded):
        return ExchangeConnectionError("Rate limit exceeded")
    else:
        return ExchangeError(str(error))
```

### Retry Logic
```python
async def fetch_with_retry(self, fetch_func, max_retries=3):
    """Retry failed requests"""
    for attempt in range(max_retries):
        try:
            return await fetch_func()
        except NetworkError as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

---

## Rate Limiting

### CCXT Rate Limiting
```python
# Enable in connector config
config = {
    'apiKey': 'key',
    'secret': 'secret',
    'enableRateLimit': True  # CCXT handles rate limits
}
```

### Custom Rate Limiting
```python
import asyncio
from datetime import datetime, timedelta

class RateLimiter:
    """Custom rate limiter"""
    
    def __init__(self, max_requests: int, period: float):
        self.max_requests = max_requests
        self.period = period  # seconds
        self.requests = []
    
    async def acquire(self):
        """Wait if rate limit reached"""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.period)
        
        # Remove old requests
        self.requests = [t for t in self.requests if t > cutoff]
        
        if len(self.requests) >= self.max_requests:
            # Wait until oldest request expires
            sleep_time = (self.requests[0] - cutoff).total_seconds()
            await asyncio.sleep(sleep_time)
        
        self.requests.append(now)
```
