# Modules

## Exchanges Module

### Purpose
Abstracts exchange APIs into a unified interface, enabling OctoBot to trade on multiple exchanges with consistent code.

### Structure
```
exchanges/
├── abstract_exchange.py      # RestExchange base class
├── ccxt_connector.py          # CCXT library integration
├── websockets/                # WebSocket implementations
│   └── abstract_websocket.py
├── connectors/                # Exchange-specific connectors
└── util/                      # Exchange utilities
```

### Key Classes

#### RestExchange
Base class for all exchange implementations:
```python
from octobot_trading.exchanges import RestExchange

class RestExchange:
    """Base class for REST API exchange implementations"""
    
    DESCRIPTION: str = ""
    DEFAULT_CONNECTOR_CLASS = None
    
    @classmethod
    def get_name(cls) -> str:
        """Return lowercase exchange identifier"""
        raise NotImplementedError
    
    async def initialize(self):
        """Initialize exchange connection"""
        pass
    
    async def fetch_balance(self) -> dict:
        """Fetch account balance"""
        return await self.connector.get_balance()
    
    async def create_order(self, order_type: str, side: str, 
                          symbol: str, amount: float, 
                          price: float = None) -> dict:
        """Create new order"""
        return await self.connector.create_order(...)
```

**Key methods**:
- `fetch_balance()` - Get account balances
- `fetch_order(order_id)` - Get order status
- `fetch_orders(symbol)` - Get all orders for symbol
- `create_order()` - Place new order
- `cancel_order(order_id)` - Cancel order
- `fetch_my_trades()` - Get trade history
- `fetch_ohlcv()` - Get candlestick data
- `fetch_ticker()` - Get current price
- `fetch_order_book()` - Get order book

#### CCXTConnector
Wraps CCXT library for exchange API calls:
```python
from octobot_trading.exchanges.connectors import CCXTConnector

class CCXTConnector:
    """CCXT library wrapper"""
    
    def __init__(self, config: dict, exchange_manager):
        self.client = None  # CCXT exchange instance
        self.exchange_manager = exchange_manager
    
    async def initialize(self):
        """Initialize CCXT client"""
        import ccxt.async_support as ccxt
        exchange_class = getattr(ccxt, self.exchange_name)
        self.client = exchange_class(self.config)
    
    async def get_balance(self) -> dict:
        """Fetch balance via CCXT"""
        return await self.client.fetch_balance()
    
    async def create_order(self, **kwargs) -> dict:
        """Create order via CCXT"""
        return await self.client.create_order(**kwargs)
```

**Error handling**:
```python
from ccxt import ExchangeError, NetworkError

try:
    balance = await connector.get_balance()
except NetworkError as e:
    logger.error(f"Network error: {e}")
except ExchangeError as e:
    logger.error(f"Exchange error: {e}")
```

### Custom Connectors
For exchanges needing special handling:
```python
from octobot_trading.exchanges.connectors import CCXTConnector

class BinanceConnector(CCXTConnector):
    """Custom Binance connector"""
    
    async def get_balance(self) -> dict:
        """Override balance fetching for Binance-specific format"""
        raw_balance = await super().get_balance()
        return self._normalize_balance(raw_balance)
    
    def _normalize_balance(self, balance: dict) -> dict:
        """Convert Binance balance format to OctoBot format"""
        normalized = {}
        for currency, data in balance.get('info', {}).items():
            normalized[currency] = {
                'free': float(data.get('free', 0)),
                'used': float(data.get('locked', 0)),
                'total': float(data.get('free', 0)) + float(data.get('locked', 0))
            }
        return normalized
```

---

## Personal Data Module

### Purpose
Manages trading data: orders, positions, trades, and portfolio.

### Structure
```
personal_data/
├── orders/
│   ├── order.py           # Order class
│   ├── order_manager.py   # Order lifecycle management
│   └── order_state.py     # Order states enum
├── positions/
│   ├── position.py        # Position tracking
│   └── position_manager.py
├── portfolio/
│   ├── portfolio.py       # Balance management
│   └── portfolio_manager.py
└── trades/
    ├── trade.py
    └── trade_manager.py
```

### Orders

#### Order Class
```python
from octobot_trading.personal_data import Order

class Order:
    """Represents a trading order"""
    
    def __init__(self, trader):
        self.trader = trader
        self.order_id = None
        self.status = "pending"
        self.order_type = None  # market, limit, stop_loss
        self.side = None  # buy, sell
        self.symbol = None
        self.amount = 0
        self.price = None
        self.filled = 0
        self.remaining = 0
        self.fee = None
        self.timestamp = None
    
    async def initialize(self, order_type: str, side: str, 
                        symbol: str, amount: float, 
                        price: float = None):
        """Initialize order parameters"""
        self.order_type = order_type
        self.side = side
        self.symbol = symbol
        self.amount = amount
        self.price = price
        self.status = "open"
    
    async def update(self, exchange_order: dict):
        """Update order from exchange response"""
        self.order_id = exchange_order['id']
        self.status = exchange_order['status']
        self.filled = exchange_order['filled']
        self.remaining = exchange_order['remaining']
        self.fee = exchange_order.get('fee')
    
    async def cancel(self):
        """Cancel this order"""
        await self.trader.cancel_order(self)
        self.status = "canceled"
```

**Order states**:
- `pending` - Created but not submitted
- `open` - Active on exchange
- `closed` - Fully filled
- `canceled` - Canceled by user/system
- `rejected` - Rejected by exchange

#### OrderManager
```python
from octobot_trading.personal_data import OrderManager

class OrderManager:
    """Manages all orders for an exchange"""
    
    def __init__(self, trader):
        self.trader = trader
        self.orders = {}  # order_id -> Order
    
    async def create_order(self, **order_params) -> Order:
        """Create and submit new order"""
        order = Order(self.trader)
        await order.initialize(**order_params)
        
        # Submit to exchange
        exchange_order = await self.trader.exchange.create_order(
            order.order_type, order.side, order.symbol,
            order.amount, order.price
        )
        await order.update(exchange_order)
        
        self.orders[order.order_id] = order
        return order
    
    async def update_orders(self, symbol: str = None):
        """Update order statuses from exchange"""
        orders = await self.trader.exchange.fetch_orders(symbol)
        for exchange_order in orders:
            if exchange_order['id'] in self.orders:
                await self.orders[exchange_order['id']].update(exchange_order)
```

### Portfolio

#### Portfolio Class
```python
from octobot_trading.personal_data import Portfolio

class Portfolio:
    """Tracks account balances and values"""
    
    def __init__(self, trader):
        self.trader = trader
        self.portfolio = {}  # currency -> {free, used, total}
        self.initial_portfolio = {}
        self.origin_crypto_currencies_values = {}
    
    async def update_portfolio_balance(self):
        """Fetch and update balances"""
        balance = await self.trader.exchange.fetch_balance()
        for currency, amounts in balance.items():
            if currency not in self.portfolio:
                self.portfolio[currency] = {}
            self.portfolio[currency]['free'] = amounts['free']
            self.portfolio[currency]['used'] = amounts['used']
            self.portfolio[currency]['total'] = amounts['total']
    
    def get_currency_portfolio(self, currency: str) -> dict:
        """Get portfolio for specific currency"""
        return self.portfolio.get(currency, {'free': 0, 'used': 0, 'total': 0})
    
    def calculate_pnl(self, reference_currency: str = "USDT") -> float:
        """Calculate profit/loss in reference currency"""
        current_value = self._calculate_total_value(reference_currency)
        initial_value = self._calculate_initial_value(reference_currency)
        return current_value - initial_value
```

### Positions

#### Position Class
For leveraged/futures trading:
```python
from octobot_trading.personal_data import Position

class Position:
    """Represents a leveraged position"""
    
    def __init__(self, trader):
        self.trader = trader
        self.symbol = None
        self.side = None  # long, short
        self.size = 0
        self.entry_price = 0
        self.mark_price = 0
        self.liquidation_price = 0
        self.unrealized_pnl = 0
        self.leverage = 1
        self.margin = 0
    
    async def update(self, position_data: dict):
        """Update position from exchange data"""
        self.symbol = position_data['symbol']
        self.side = position_data['side']
        self.size = position_data['contracts']
        self.entry_price = position_data['entryPrice']
        self.mark_price = position_data['markPrice']
        self.unrealized_pnl = position_data['unrealizedPnl']
    
    def calculate_pnl(self) -> float:
        """Calculate position PNL"""
        if self.side == 'long':
            return (self.mark_price - self.entry_price) * self.size
        else:
            return (self.entry_price - self.mark_price) * self.size
```

---

## Modes Module

### Purpose
Trading modes define high-level strategies and execution logic.

### Structure
```
modes/
├── abstract_mode.py       # Base trading mode
├── mode_creator.py        # Mode instantiation
└── script_keywords/       # Scripting support
```

### AbstractTradingMode
```python
from octobot_trading.modes import AbstractTradingMode

class AbstractTradingMode:
    """Base class for trading strategies"""
    
    def __init__(self, config, exchange_manager):
        self.config = config
        self.exchange_manager = exchange_manager
        self.traders = []
    
    @classmethod
    def get_mode_name(cls) -> str:
        """Return mode identifier"""
        raise NotImplementedError
    
    async def create_new_orders(self, symbol: str, exchange: str):
        """Generate and place orders - implemented by subclasses"""
        raise NotImplementedError
    
    async def cancel_orders(self, symbol: str):
        """Cancel existing orders"""
        pass
```

### Example: Grid Trading Mode
```python
class GridTradingMode(AbstractTradingMode):
    """Grid trading strategy"""
    
    @classmethod
    def get_mode_name(cls) -> str:
        return "grid_trading"
    
    async def create_new_orders(self, symbol: str, exchange: str):
        """Create grid of buy/sell orders"""
        current_price = await self.get_current_price(symbol)
        grid_levels = self._calculate_grid_levels(current_price)
        
        for level in grid_levels:
            if level < current_price:
                # Buy order below current price
                await self.create_order("limit", "buy", symbol, 
                                       self.order_size, level)
            elif level > current_price:
                # Sell order above current price
                await self.create_order("limit", "sell", symbol,
                                       self.order_size, level)
    
    def _calculate_grid_levels(self, current_price: float) -> list:
        """Calculate grid price levels"""
        grid_spacing = current_price * 0.01  # 1% spacing
        levels = []
        for i in range(-5, 6):  # 5 levels above/below
            levels.append(current_price + (i * grid_spacing))
        return levels
```

---

## Signals Module

### Purpose
Trading signal system for strategy communication.

### Structure
```
signals/
├── signal_builder.py
└── signal_publisher.py
```

### Signal System
```python
from octobot_trading.signals import Signal

class Signal:
    """Trading signal"""
    
    def __init__(self, topic: str, content: dict):
        self.topic = topic
        self.content = content
        self.timestamp = time.time()
    
    @property
    def signal_type(self) -> str:
        """Signal type (buy, sell, neutral)"""
        return self.content.get('type')
    
    @property
    def symbol(self) -> str:
        """Target symbol"""
        return self.content.get('symbol')
```

---

## Storage Module

### Purpose
Data persistence for historical data, backtesting, and analysis.

### Key Features
- Historical OHLCV data storage
- Order history
- Trade logs
- Performance metrics

---

## Util Module

### Purpose
Shared utilities for trading operations.

### Key Utilities

#### Order Utilities
```python
from octobot_trading.util import parse_order_type, parse_order_status

order_type = parse_order_type("limit")  # Normalize order type
status = parse_order_status("closed")   # Normalize status
```

#### Price Utilities
```python
from octobot_trading.util import adapt_price, adapt_quantity

# Adapt to exchange precision
price = adapt_price(symbol_market, 50000.123456)
quantity = adapt_quantity(symbol_market, 0.123456789)
```
