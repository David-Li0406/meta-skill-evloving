# Configuration

## Config File Structure

### user/config.json
```json
{
    "crypto-currencies": {
        "Bitcoin": {
            "pairs": ["BTC/USDT"],
            "enabled": true
        },
        "Ethereum": {
            "pairs": ["ETH/USDT", "ETH/BTC"],
            "enabled": true
        }
    },
    "exchanges": {
        "binance": {
            "enabled": true,
            "exchange-type": "spot",
            "api-key": "YOUR_API_KEY",
            "api-secret": "YOUR_API_SECRET",
            "sandboxed": false
        }
    },
    "trading": {
        "enabled": true,
        "risk": 0.1
    },
    "trader-simulator": {
        "enabled": true,
        "starting-portfolio": {
            "USDT": 10000
        }
    },
    "trading-mode": "DipAnalyzerTradingMode",
    "tentacles-config": {
        "RSIEvaluator": {
            "period": 14,
            "overbought": 70,
            "oversold": 30
        }
    },
    "notification": {
        "notification-type": ["web"],
        "telegram": {
            "enabled": false,
            "token": "",
            "chat-id": ""
        }
    },
    "web-interface": {
        "enabled": true,
        "port": 5001
    }
}
```

## Profile System

### Directory Structure
```
user/profiles/
├── aggressive/
│   ├── profile.json
│   └── tentacles_config.json
├── conservative/
│   ├── profile.json
│   └── tentacles_config.json
└── default/
    ├── profile.json
    └── tentacles_config.json
```

### profile.json
```json
{
    "name": "aggressive",
    "description": "High-risk high-reward strategy",
    "trading-mode": "GridTradingMode",
    "risk": 0.3,
    "exchanges": ["binance"],
    "crypto-currencies": {
        "Bitcoin": {
            "pairs": ["BTC/USDT"]
        }
    }
}
```

### tentacles_config.json
```json
{
    "GridTradingMode": {
        "grid_levels": 10,
        "spread": 0.01,
        "reinvest_profits": true
    },
    "RSIEvaluator": {
        "period": 7,
        "overbought": 75,
        "oversold": 25
    }
}
```

## Environment Variables

### PYTHONPATH Setup
```bash
export PYTHONPATH="${PYTHONPATH}:\
/path/to/OctoBot-Stack/Async-Channel:\
/path/to/OctoBot-Stack/OctoBot-Commons:\
/path/to/OctoBot-Stack/OctoBot-Trading:\
/path/to/OctoBot-Stack/OctoBot-Evaluators:\
/path/to/OctoBot-Stack/OctoBot-Backtesting:\
/path/to/OctoBot-Stack/trading-backend:\
/path/to/OctoBot-Stack/OctoBot"
```

### Configuration Overrides
```bash
# Override exchange API credentials
export OCTOBOT_BINANCE_API_KEY="your_key"
export OCTOBOT_BINANCE_API_SECRET="your_secret"

# Override trading mode
export OCTOBOT_TRADING_MODE="DCAMode"

# Enable/disable simulator
export OCTOBOT_SIMULATOR="true"
```

## Exchange Configuration

### Spot Trading
```json
{
    "binance": {
        "enabled": true,
        "exchange-type": "spot",
        "api-key": "YOUR_KEY",
        "api-secret": "YOUR_SECRET",
        "sandboxed": false
    }
}
```

### Futures Trading
```json
{
    "binance": {
        "enabled": true,
        "exchange-type": "future",
        "api-key": "YOUR_KEY",
        "api-secret": "YOUR_SECRET",
        "sandboxed": false,
        "leverage": 10
    }
}
```

### Multiple Exchanges
```json
{
    "exchanges": {
        "binance": {
            "enabled": true,
            "exchange-type": "spot"
        },
        "coinbase": {
            "enabled": true,
            "exchange-type": "spot"
        },
        "kraken": {
            "enabled": false
        }
    }
}
```

## Trading Configuration

### Risk Management
```json
{
    "trading": {
        "enabled": true,
        "risk": 0.1,
        "max-open-orders": 5,
        "max-portfolio-percentage-per-trade": 0.2,
        "stop-loss-percentage": 0.05,
        "take-profit-percentage": 0.1
    }
}
```

### Paper Trading
```json
{
    "trader-simulator": {
        "enabled": true,
        "starting-portfolio": {
            "USDT": 10000,
            "BTC": 0.1
        },
        "fees": {
            "maker": 0.001,
            "taker": 0.002
        }
    }
}
```

## Tentacle Configuration

### Global Tentacle Settings
```json
{
    "tentacles-config": {
        "RSIEvaluator": {
            "period": 14,
            "timeframes": ["1h", "4h", "1d"]
        },
        "MACDEvaluator": {
            "fast_period": 12,
            "slow_period": 26,
            "signal_period": 9
        },
        "DipAnalyzerTradingMode": {
            "buy_dip_threshold": 0.03,
            "minimal_price_change": 0.01
        }
    }
}
```

## Notification Configuration

### Telegram
```json
{
    "notification": {
        "telegram": {
            "enabled": true,
            "token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
            "chat-id": "987654321",
            "notifications": [
                "trade",
                "orders",
                "portfolio"
            ]
        }
    }
}
```

### Discord
```json
{
    "notification": {
        "discord": {
            "enabled": true,
            "token": "YOUR_BOT_TOKEN",
            "channel-id": "123456789012345678"
        }
    }
}
```

## Loading Profiles

### From Command Line
```bash
# Use specific profile
python start.py -p aggressive

# Use default profile
python start.py -p default
```

### Programmatically
```python
from octobot.configuration import Configuration

config = Configuration("user/config.json")
await config.load_profile("aggressive")
```

## Configuration Validation

```python
from octobot.configuration import ConfigValidator

validator = ConfigValidator()
errors = validator.validate(config)

if errors:
    for error in errors:
        print(f"Config error: {error}")
```
