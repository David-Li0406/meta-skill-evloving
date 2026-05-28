# Architecture

## Overview

OctoBot-Backtesting simulates trading strategies against historical market data, enabling strategy validation before live deployment.

## Core Components

### Backtesting Engine

Main orchestrator for simulation execution:

```python
from octobot_backtesting import Backtesting

class Backtesting:
    """Main backtesting engine"""
    
    def __init__(self, config, tentacles_setup_config, data_files):
        self.config = config
        self.tentacles_setup_config = tentacles_setup_config
        self.data_files = data_files
        self.time_manager = None
        self.exchange_managers = {}
        self.trading_mode = None
    
    async def initialize(self):
        """Initialize backtesting environment"""
        await self._initialize_time_manager()
        await self._initialize_exchanges()
        await self._load_data()
    
    async def start(self):
        """Start backtest simulation"""
        while not self.time_manager.finished():
            await self._process_timestamp()
            await self.time_manager.advance()
    
    async def end(self):
        """Finalize backtest and calculate results"""
        await self._calculate_performance()
        await self._cleanup()
```

**Key responsibilities**:
- Coordinate time progression
- Manage simulated exchanges
- Execute trading strategy
- Calculate performance metrics

---

### Time Manager

Controls simulation clock and event scheduling:

```python
from octobot_backtesting.time import TimeManager

class TimeManager:
    """Manages simulation time"""
    
    def __init__(self, timestamps: list):
        self.timestamps = sorted(timestamps)
        self.current_index = 0
        self.current_timestamp = self.timestamps[0] if timestamps else 0
    
    def get_current_timestamp(self) -> float:
        """Get current simulation time"""
        return self.current_timestamp
    
    async def set_current_timestamp(self, timestamp: float):
        """Set simulation time"""
        self.current_timestamp = timestamp
    
    async def advance(self):
        """Move to next timestamp"""
        self.current_index += 1
        if self.current_index < len(self.timestamps):
            self.current_timestamp = self.timestamps[self.current_index]
    
    def finished(self) -> bool:
        """Check if simulation complete"""
        return self.current_index >= len(self.timestamps)
```

**Features**:
- Sequential time progression
- Event synchronization
- Timestamp validation
- Completion detection

---

### Backtest Data Container

Stores and manages historical data:

```python
from octobot_backtesting import BacktestData

class BacktestData:
    """Container for historical data"""
    
    def __init__(self, exchange_name: str, symbol: str, timeframe: str):
        self.exchange_name = exchange_name
        self.symbol = symbol
        self.timeframe = timeframe
        self.candles = []  # [timestamp, open, high, low, close, volume]
        self.trades = []
        self.tickers = []
    
    def add_candle(self, timestamp: float, ohlcv: list):
        """Add OHLCV candle"""
        self.candles.append([timestamp] + ohlcv)
    
    def get_candles_at_timestamp(self, timestamp: float) -> list:
        """Get candles for specific time"""
        return [c for c in self.candles if c[0] <= timestamp]
    
    def get_price_at_timestamp(self, timestamp: float) -> float:
        """Get price at specific time"""
        relevant_candles = self.get_candles_at_timestamp(timestamp)
        return relevant_candles[-1][4] if relevant_candles else 0  # Close price
```

---

## Data Flow

```
┌─────────────────────────┐
│   Historical Data       │
│   (Files/Exchange API)  │
└──────────┬──────────────┘
           │
           ↓
┌─────────────────────────┐
│   Data Importer         │
│   - Fetch from exchange │
│   - Parse files         │
│   - Validate data       │
└──────────┬──────────────┘
           │
           ↓
┌─────────────────────────┐
│   Backtest Data         │
│   - OHLCV candles       │
│   - Trades              │
│   - Order books         │
└──────────┬──────────────┘
           │
           ↓
┌─────────────────────────┐
│   Time Manager          │
│   - Sequence timestamps │
│   - Control progression │
└──────────┬──────────────┘
           │
           ↓
┌─────────────────────────┐
│   Backtesting Engine    │
│   - Process events      │
│   - Execute strategy    │
└──────────┬──────────────┘
           │
           ↓
┌─────────────────────────┐
│   Simulated Exchange    │
│   (OctoBot-Trading)     │
│   - Execute orders      │
│   - Update portfolio    │
└──────────┬──────────────┘
           │
           ↓
┌─────────────────────────┐
│   Performance Metrics   │
│   - Profitability       │
│   - Win rate            │
│   - Drawdown            │
└─────────────────────────┘
```

---

## Simulation Modes

### Full Simulation Mode

Realistic trading environment:
- Order book simulation
- Slippage calculation
- Fee application
- Realistic order fills based on volume

```python
config = {
    "simulation_mode": "full",
    "slippage": 0.1,  # 0.1% slippage
    "fees": {
        "maker": 0.001,  # 0.1%
        "taker": 0.001
    },
    "use_order_book": True
}
```

### Fast Simulation Mode

Simplified for quick iterations:
- Instant order execution
- No slippage
- Simplified fees
- No order book

```python
config = {
    "simulation_mode": "fast",
    "instant_execution": True,
    "simplified_fees": 0.001
}
```

---

## Multi-Timeframe Support

Backtesting handles multiple timeframes simultaneously:

```python
# Import data for multiple timeframes
data_config = {
    "symbols": ["BTC/USDT"],
    "timeframes": ["1m", "5m", "1h", "1d"],
    "start": start_timestamp,
    "end": end_timestamp
}

# Synchronize candles across timeframes
await backtesting.synchronize_timeframes()
```

**Synchronization**:
- Align timestamps across timeframes
- Ensure data consistency
- Handle missing candles
- Update in correct order

---

## Integration with OctoBot-Trading

Backtesting sets trading engine to simulation mode:

```python
# In ExchangeManager
exchange_manager.is_backtesting = True
exchange_manager.is_simulated = True

# Exchange operations use historical data
class SimulatedExchange:
    async def fetch_ohlcv(self, symbol, timeframe, since, limit):
        """Return historical data instead of API call"""
        return backtest_data.get_candles(symbol, timeframe, since, limit)
    
    async def create_order(self, order_type, side, symbol, amount, price):
        """Simulate order execution"""
        current_price = backtest_data.get_price_at_timestamp(
            time_manager.current_timestamp
        )
        # Simulate fill logic
        return self._simulate_order_fill(order_type, side, amount, 
                                        price, current_price)
```

---

## Performance Calculation

Metrics computed after simulation:

```python
class BacktestingMetrics:
    """Calculate backtest performance"""
    
    def calculate_profitability(self, initial_portfolio, final_portfolio):
        """Total profit/loss percentage"""
        initial_value = self._calculate_portfolio_value(initial_portfolio)
        final_value = self._calculate_portfolio_value(final_portfolio)
        return ((final_value - initial_value) / initial_value) * 100
    
    def calculate_sharpe_ratio(self, returns: list, risk_free_rate: float = 0):
        """Risk-adjusted return"""
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        return (mean_return - risk_free_rate) / std_return if std_return > 0 else 0
    
    def calculate_max_drawdown(self, portfolio_values: list):
        """Maximum portfolio decline"""
        peak = portfolio_values[0]
        max_dd = 0
        for value in portfolio_values:
            if value > peak:
                peak = value
            dd = (peak - value) / peak
            if dd > max_dd:
                max_dd = dd
        return max_dd * 100
```

---

## Channels Integration

Backtesting publishes events via Async-Channel:

```python
# Time channel - notifies of time updates
TIME_CHANNEL = "Time"
await time_producer.send({
    "timestamp": current_timestamp,
    "timeframe": "1h"
})

# Candle channel - historical candles
KLINE_CHANNEL = "Kline"
await kline_producer.send({
    "exchange": "binance",
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "candle": [timestamp, open, high, low, close, volume]
})

# Order channel - backtested orders
ORDERS_CHANNEL = "Orders"
await orders_producer.send({
    "order_id": "123",
    "status": "filled",
    "symbol": "BTC/USDT",
    "side": "buy",
    "amount": 1.0,
    "price": 50000.0
})
```

---

## Error Handling

### Data Validation

```python
def validate_data(data: BacktestData):
    """Validate historical data integrity"""
    errors = []
    
    # Check for missing timestamps
    if not data.candles:
        errors.append("No candles found")
    
    # Check for duplicates
    timestamps = [c[0] for c in data.candles]
    if len(timestamps) != len(set(timestamps)):
        errors.append("Duplicate timestamps found")
    
    # Check for invalid OHLCV
    for candle in data.candles:
        if candle[2] < candle[3]:  # high < low
            errors.append(f"Invalid OHLCV at {candle[0]}")
    
    return errors
```

### Simulation Failures

```python
from octobot_backtesting import BacktestingEndedException

try:
    await backtesting.start()
except BacktestingEndedException as e:
    # Normal backtest completion
    logger.info(f"Backtest completed: {e}")
except Exception as e:
    # Unexpected error
    logger.error(f"Backtest failed: {e}")
    await backtesting.cleanup()
```
