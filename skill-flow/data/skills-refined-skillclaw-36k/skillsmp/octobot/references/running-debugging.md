# Running & Debugging

## Starting OctoBot

### Basic Start
```bash
cd OctoBot
python start.py
```

### Common Options
```bash
# Use specific profile
python start.py -p my_profile

# Enable backtesting
python start.py --backtesting

# Start data collector
python start.py --data_collector

# Strategy optimizer
python start.py --strategy_optimizer

# Specify config file
python start.py -c /path/to/config.json

# Enable simulator (paper trading)
python start.py --simulate-trading

# Update tentacles
python start.py tentacles --install --all
```

## Development Setup

### 1. Setup PYTHONPATH
Run the VS Code task:
```
Command Palette → Tasks: Run Task → Setup PYTHONPATH
```

Or manually:
```bash
export PYTHONPATH="${PYTHONPATH}:\
$(pwd)/Async-Channel:\
$(pwd)/OctoBot-Commons:\
$(pwd)/OctoBot-Trading:\
$(pwd)/OctoBot-Evaluators:\
$(pwd)/OctoBot-Backtesting:\
$(pwd)/OctoBot-Services:\
$(pwd)/trading-backend:\
$(pwd)/OctoBot"
```

### 2. Link Tentacles
```bash
# From workspace root
cd OctoBot
ln -s ../OctoBot-Tentacles tentacles

# Also link in Trading/Backtesting if needed
cd ../OctoBot-Trading
ln -s ../OctoBot-Tentacles tentacles
```

### 3. Install Dependencies
```bash
# OctoBot main
cd OctoBot
pip install -r requirements.txt
pip install -r dev_requirements.txt

# Repeat for other repos
cd ../OctoBot-Trading
pip install -r requirements.txt
```

## VS Code Debugging

### launch.json Configuration
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "OctoBot: Run",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/OctoBot/start.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/OctoBot",
            "env": {
                "PYTHONPATH": "${env:PYTHONPATH}:${workspaceFolder}/Async-Channel:${workspaceFolder}/OctoBot-Commons:${workspaceFolder}/OctoBot-Trading:${workspaceFolder}/OctoBot-Evaluators:${workspaceFolder}/OctoBot-Backtesting:${workspaceFolder}/OctoBot-Services:${workspaceFolder}/trading-backend:${workspaceFolder}/OctoBot"
            },
            "justMyCode": false
        },
        {
            "name": "OctoBot: Backtesting",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/OctoBot/start.py",
            "args": ["--backtesting"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/OctoBot",
            "env": {
                "PYTHONPATH": "${env:PYTHONPATH}:..."
            }
        },
        {
            "name": "OctoBot: Specific Profile",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/OctoBot/start.py",
            "args": ["-p", "aggressive"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/OctoBot"
        }
    ]
}
```

### Setting Breakpoints
1. Open file in VS Code
2. Click left of line number to add breakpoint
3. Run debugger (F5)
4. Use Debug Console to inspect variables

## Logging

### Log Files
```
OctoBot/user/logs/
├── octobot.log           # Main log
├── trading.log           # Trading operations
├── evaluators.log        # Evaluator signals
└── errors.log            # Errors only
```

### Log Levels
```python
# In code
import logging
logger = logging.getLogger(__name__)

logger.debug("Detailed debug info")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical failure")
```

### Configure Logging
```python
# user/config.json
{
    "logs": {
        "level": "INFO",
        "file-level": "DEBUG",
        "max-file-size": 10000000,
        "max-file-count": 10
    }
}
```

## Common Issues

### Import Errors
```bash
# Problem: ModuleNotFoundError: No module named 'octobot_commons'
# Solution: Setup PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/OctoBot-Commons:..."
```

### Tentacles Not Found
```bash
# Problem: No tentacles loaded
# Solution: Symlink tentacles directory
cd OctoBot
ln -s ../OctoBot-Tentacles tentacles
```

### Exchange Connection Issues
```bash
# Problem: Exchange authentication failed
# Solution: Check API credentials in config.json
# Enable sandbox mode for testing:
{
    "exchanges": {
        "binance": {
            "sandboxed": true
        }
    }
}
```

### Port Already in Use
```bash
# Problem: Web interface port 5001 in use
# Solution: Change port in config
{
    "web-interface": {
        "port": 5002
    }
}
```

## Testing

### Run All Tests
```bash
cd OctoBot
pytest
```

### Run Specific Test
```bash
pytest tests/test_octobot.py::test_initialization
```

### Run with Coverage
```bash
pytest --cov=octobot --cov-report=html
```

### Test in Different Modes
```bash
# Test backtesting
pytest tests/backtesting/

# Test trading modes
pytest tests/trading_modes/

# Test evaluators
pytest tests/evaluators/
```

## Performance Profiling

### CPU Profiling
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Run bot
await bot.start()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumtime')
stats.print_stats(20)
```

### Memory Profiling
```python
from memory_profiler import profile

@profile
async def start_bot():
    bot = OctoBot()
    await bot.initialize()
    await bot.start()
```

## Monitoring

### Access Web Interface
```
http://localhost:5001
```

### API Endpoints
```bash
# Get bot status
curl http://localhost:5001/api/status

# Get portfolio
curl http://localhost:5001/api/portfolio

# Get open orders
curl http://localhost:5001/api/orders
```

### Real-time Logs
```bash
tail -f user/logs/octobot.log
```
