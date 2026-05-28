---
name: OctoBot
description: Main OctoBot application orchestrating trading, evaluation, backtesting, and services
version: 1.0.0
license: GPL-3.0
---

# OctoBot Development

## Overview

OctoBot is the main application that orchestrates all components: initializes exchanges, loads tentacles, manages trading modes, runs evaluators, handles backtesting, and provides web interface. It's the entry point that ties together all other OctoBot repositories.

## References

- **[Architecture](references/architecture.md)**: Application structure, initialization flow, component management
- **[Configuration](references/configuration.md)**: Config files, profiles, environment variables
- **[Running & Debugging](references/running-debugging.md)**: Launch commands, debugging setup, logs

## Key Concepts

### Bot Lifecycle
1. Load configuration
2. Initialize exchanges
3. Load tentacles
4. Start evaluators
5. Activate trading modes
6. Launch web interface

### Tentacle Loading
OctoBot loads tentacles from `tentacles/` directory (symlink to OctoBot-Tentacles during dev).

### Configuration Profiles
Multiple trading strategies via profile system in `user/profiles/`.

### Web Interface
Built-in dashboard for monitoring and control.

## Common Tasks

### Run OctoBot
```bash
cd OctoBot
python start.py
```

### Run with Specific Profile
```bash
python start.py -p my_profile
```

### Enable Backtesting
```bash
python start.py --backtesting
```

### Configure Exchange
```python
# user/config.json
{
    "exchanges": {
        "binance": {
            "enabled": true,
            "exchange-type": "spot",
            "api-key": "YOUR_KEY",
            "api-secret": "YOUR_SECRET"
        }
    }
}
```

### Link Tentacles for Development
```bash
# From OctoBot-Stack-VS-Workspace/
ln -s $(pwd)/OctoBot-Tentacles/ OctoBot/tentacles
```

### Custom Bot Initialization
```python
from octobot import OctoBot

async def run_custom_bot():
    bot = OctoBot(config_file="my_config.json")
    await bot.initialize()
    await bot.start()
    await bot.wait_for_stop()

import asyncio
asyncio.run(run_custom_bot())
```

## Integration Points

- **OctoBot-Trading**: Trading engine integration
- **OctoBot-Evaluators**: Evaluator framework
- **OctoBot-Backtesting**: Historical simulation
- **OctoBot-Services**: Service integrations
- **OctoBot-Tentacles**: Plugin loading
- **trading-backend**: Web API server

## Quick Reference

### Directory Structure
```
OctoBot/
├── start.py              # Entry point
├── octobot/
│   ├── __init__.py
│   ├── octobot.py        # Main bot class
│   ├── initializer.py    # Initialization logic
│   ├── community/        # Community features
│   ├── strategy_optimizer/
│   └── updater/
├── user/
│   ├── config.json       # Main config
│   ├── profiles/         # Trading profiles
│   └── logs/
├── tentacles/            # Symlink to OctoBot-Tentacles
└── tests/
```

### Environment Variables
```bash
PYTHONPATH=..:../OctoBot-Commons:../OctoBot-Trading:...
```

### Common Start Commands
```bash
# Normal mode
python start.py

# Backtesting
python start.py --backtesting

# Data collector
python start.py --data_collector

# Strategy optimizer
python start.py --strategy_optimizer

# Update tentacles
python start.py tentacles --install --all
```

### Configuration Keys
- `crypto-currencies`: Traded pairs
- `exchanges`: Exchange configs
- `trading-mode`: Active trading mode
- `trader-simulator`: Paper trading settings
- `notification`: Service notifications

## Checklist

- [ ] Setup PYTHONPATH with all repositories
- [ ] Symlink OctoBot-Tentacles to OctoBot/tentacles
- [ ] Create/edit user/config.json with exchange credentials
- [ ] Configure crypto-currencies to trade
- [ ] Select trading mode in config
- [ ] Test with simulator enabled first
- [ ] Verify web interface accessible at localhost:5001
- [ ] Check logs/ directory for errors
- [ ] Configure notification services
- [ ] Test emergency stop functionality
- [ ] Backup user/ directory regularly
