---
name: octobot-backtesting
description: Historical data simulation engine for OctoBot. Handles data collection, exchange simulation, and strategy validation. Use when implementing backtesting features, adding data sources, or testing trading strategies.
version: 1.0.0
license: MIT
---

# OctoBot-Backtesting Development

Help developers work with OctoBot's backtesting engine - the system for simulating trading strategies against historical data.

## References

Consult these resources as needed:
- ./references/architecture.md -- Core components, data flow, simulation modes
- ./references/data-management.md -- Data importers, collectors, converters, storage

## Overview

OctoBot-Backtesting is a **Core Layer** library providing:
- Historical data collection and storage
- Exchange behavior simulation
- Time-based event replay
- Performance metrics calculation
- Multi-timeframe backtesting
- Data format conversion

**Layer Position**: Core (no dependencies on Application or Extension layers)
**Used By**: OctoBot, OctoBot-Trading (simulation mode), strategy optimizers

## Module Structure

```
octobot_backtesting/
├── backtesting.py          # Main backtesting orchestrator
├── backtest_data.py        # Data container
├── importers/              # Data import from exchanges/files
│   ├── data_importer.py
│   └── exchange_importer.py
├── collectors/             # Real-time data collection
│   └── data_collector.py
├── converters/             # Data format converters
│   └── data_converter.py
├── data/                   # Data persistence
│   └── database.py
├── time/                   # Time management
│   └── time_manager.py
└── util/                   # Backtesting utilities
```

## Key Concepts

### Backtesting Engine
Orchestrates strategy simulation:
```python
from octobot_backtesting import Backtesting

backtesting = Backtesting(config, tentacles_setup)
await backtesting.initialize()
await backtesting.start()
await backtesting.end()
```

### Data Importers
Load historical data from exchanges:
```python
from octobot_backtesting.importers import ExchangeDataImporter

importer = ExchangeDataImporter(config)
await importer.import_data("binance", ["BTC/USDT"], ["1h"], 
                           start_timestamp, end_timestamp)
```

### Time Manager
Controls simulation time progression:
```python
from octobot_backtesting.time import TimeManager

time_manager = TimeManager()
await time_manager.set_current_timestamp(timestamp)
current_time = time_manager.get_current_timestamp()
```

### Simulated Exchanges
Mock exchange operations during backtesting:
```python
# OctoBot-Trading uses simulated mode
exchange_manager.is_backtesting = True
# Orders executed against historical data
order = await exchange.create_order(...)  # Simulated
```

## Common Tasks

### Run Backtesting
```python
from octobot_backtesting import run_backtesting

results = await run_backtesting(
    config=config,
    data_files=["BTC_USDT_1h.data"],
    tentacles_setup=tentacles
)
```

### Import Historical Data
```bash
# Via CLI
python -m octobot_backtesting import --exchange binance --symbol BTC/USDT --timeframe 1h
```

### Add Data Collector
Collect data in real-time for future backtests:
```python
from octobot_backtesting.collectors import DataCollector

collector = DataCollector(exchange, symbols, timeframes)
await collector.start()
```

### Convert Data Formats
```python
from octobot_backtesting.converters import DataConverter

converter = DataConverter()
await converter.convert(input_file, output_file, target_format)
```

## Integration Points

### OctoBot-Trading Integration
Backtesting sets trading engine to simulation mode:
- Exchange operations use historical data
- Orders execute against simulated order book
- Portfolio tracks paper trading balances
- No real API calls made

### Data Flow
```
Historical Data Files
         ↓
Data Importer
         ↓
Backtesting Engine
         ↓
Time Manager (controls simulation clock)
         ↓
OctoBot-Trading (simulation mode)
         ↓
Strategy Execution
         ↓
Performance Metrics
```

### Async-Channel Integration
Backtesting uses channels for event distribution:
```python
# Publish historical candle data
await producer.send({
    "exchange": "binance",
    "symbol": "BTC/USDT",
    "timeframe": "1h",
    "candle": ohlcv_data
})
```

## Quick Reference

### Import Patterns
```python
# Main backtesting
from octobot_backtesting import Backtesting, BacktestingEndedException

# Data management
from octobot_backtesting.importers import ExchangeDataImporter
from octobot_backtesting.collectors import DataCollector

# Time
from octobot_backtesting.time import TimeManager
```

### Data File Formats
```python
# Standard OctoBot format (.data files)
{
    "exchange": "binance",
    "symbol": "BTC/USDT",
    "time_frame": "1h",
    "candles": [
        [timestamp, open, high, low, close, volume],
        ...
    ]
}
```

### Performance Metrics
```python
from octobot_backtesting.api import calculate_backtesting_profitability

profitability = calculate_backtesting_profitability(
    initial_portfolio,
    final_portfolio,
    market_delta
)
```

## Backtesting Modes

### Full Mode
Simulates complete trading environment:
- Order execution with slippage
- Fees calculation
- Realistic fills based on volume
- Order book simulation

### Fast Mode
Simplified simulation for quick iterations:
- Instant order fills
- No order book simulation
- Faster execution, less accurate

## Checklist

Before committing changes:
- [ ] Imports follow `octobot_backtesting.*` pattern
- [ ] Time management preserves simulation clock integrity
- [ ] Data importers handle all edge cases (missing data, format errors)
- [ ] No real exchange API calls during simulation
- [ ] Performance metrics accurately reflect simulated trading
- [ ] Tests verify backtest reproducibility
- [ ] Data files properly formatted and validated
