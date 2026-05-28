# Development Workflows

## Environment Setup

### Initial Setup

1. **Clone all repositories**:
   ```bash
   git clone --recursive https://github.com/Drakkar-Software/OctoBot-Stack-VS-Workspace.git
   cd OctoBot-Stack-VS-Workspace
   ```

2. **Setup PYTHONPATH**:
   Run the VS Code task "Setup PYTHONPATH" or manually:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)/Async-Channel:$(pwd)/OctoBot-Commons:$(pwd)/OctoBot-Trading:$(pwd)/OctoBot"
   ```

3. **Link tentacles**:
   ```bash
   ln -s $(pwd)/OctoBot-Tentacles/ OctoBot/tentacles
   ln -s $(pwd)/OctoBot-Tentacles/ OctoBot-Trading/tentacles
   ```

4. **Install dependencies**:
   ```bash
   cd OctoBot
   pip install -r requirements.txt
   ```

---

## CCXT Exchange Integration

OctoBot uses CCXT for exchange API standardization. New exchanges require editing CCXT source and transpiling.

### Adding a New Exchange

#### 1. Edit TypeScript Source
Edit `ccxt/ts/src/{exchange}.ts`:
```typescript
// ccxt/ts/src/polymarket.ts
import Exchange from './abstract/polymarket.js';

export default class polymarket extends Exchange {
    describe() {
        return this.deepExtend(super.describe(), {
            'id': 'polymarket',
            'name': 'Polymarket',
            'countries': ['US'],
            'rateLimit': 100,
            'has': {
                'fetchBalance': true,
                'fetchMarkets': true,
                'fetchTicker': true,
            },
        });
    }
}
```

#### 2. CRITICAL: Transpilation Rules
**Never use these in CCXT TypeScript** (breaks transpilation to Python/Go/PHP/C#):
- ❌ Ternary operators: `a ? b : c`
- ❌ Type annotations: `let x: string = "hello"`
- ❌ Optional chaining: `obj?.prop`
- ❌ Nullish coalescing: `a ?? b`

**Use these instead**:
- ✅ If statements: `if (a) { return b; } else { return c; }`
- ✅ No type annotations: `let x = "hello"`
- ✅ Safe access: `this.safeString(obj, 'prop')`
- ✅ Fallbacks: `a || b`

#### 3. Error Handling
Use `handleErrors` method:
```typescript
handleErrors(code, reason, url, method, headers, body, response, requestHeaders, requestBody) {
    if (response === undefined) {
        return undefined;
    }
    
    const error = this.safeString(response, 'error');
    if (error !== undefined) {
        const feedback = this.id + ' ' + body;
        this.throwExactlyMatchedException(this.exceptions['exact'], error, feedback);
        this.throwBroadlyMatchedException(this.exceptions['broad'], error, feedback);
    }
}
```

Define exceptions:
```typescript
this.exceptions = {
    'exact': {
        'INSUFFICIENT_BALANCE': InsufficientFunds,
        'INVALID_ORDER': InvalidOrder,
    },
    'broad': {
        'balance': InsufficientFunds,
        'order': InvalidOrder,
    },
};
```

#### 4. Transpile to Python
```bash
cd ccxt
nvm use 24  # Ensure Node.js 24.x
npm run emitAPI polymarket
npm run transpileRest polymarket
npm run transpileWs polymarket  # If WebSocket supported
```

**Output**: Generates `ccxt/python/ccxt/polymarket.py`

#### 5. Test CCXT Exchange
```bash
cd ccxt
python3 -c "import ccxt; exchange = ccxt.polymarket(); print(exchange.has)"
```

---

### CCXT Build Task
Use the VS Code task "CCXT: Build polymarket exchange python":
```json
{
  "label": "CCXT: Build polymarket exchange python",
  "type": "shell",
  "command": "nvm use 24 && npm run emitAPI polymarket && npm run transpileRest polymarket && npm run transpileWs polymarket",
  "options": {
    "cwd": "${workspaceFolder}/ccxt"
  }
}
```

---

## Tentacle Development

### Create New Exchange Tentacle

#### 1. Scaffold Structure
```bash
mkdir -p OctoBot-Tentacles/Trading/Exchange/myexchange/tests
touch OctoBot-Tentacles/Trading/Exchange/myexchange/__init__.py
touch OctoBot-Tentacles/Trading/Exchange/myexchange/myexchange_exchange.py
touch OctoBot-Tentacles/Trading/Exchange/myexchange/metadata.json
```

#### 2. Implement Exchange Class
```python
# myexchange_exchange.py
from octobot_trading.exchanges import RestExchange

class MyExchange(RestExchange):
    DESCRIPTION = "MyExchange connector"
    DEFAULT_CONNECTOR_CLASS = None
    
    @classmethod
    def get_name(cls) -> str:
        return "myexchange"  # Must match CCXT exchange ID
```

#### 3. Create Metadata
```json
{
  "version": "1.0.0",
  "origin_package": "OctoBot-Default-Tentacles",
  "tentacles": ["MyExchange"],
  "requirements": [],
  "tentacles-requirements": []
}
```

#### 4. Write Tests
```python
# tests/test_myexchange_exchange.py
import pytest
from ...myexchange import MyExchange

@pytest.mark.asyncio
async def test_exchange_name():
    assert MyExchange.get_name() == "myexchange"
```

#### 5. Export Tentacles
```bash
cd OctoBot
python start.py tentacles -p ../../tentacles_default_export.zip -d ../OctoBot-Tentacles
```

---

## Running OctoBot

### Development Mode
```bash
cd OctoBot
python start.py
```

### Backtesting Mode
```bash
python start.py backtesting -f data_files/BTC_USDT_1h.data
```

### Strategy Optimization
```bash
python start.py strategy_optimizer -s grid_trading
```

---

## Testing Workflows

### Run All Tests
```bash
# From repository root
pytest
```

### Run Specific Test File
```bash
pytest tests/test_exchange.py
```

### Run with Coverage
```bash
pytest --cov=octobot_trading --cov-report=html
```

### Test Tentacles
```bash
cd OctoBot-Tentacles/Trading/Exchange/binance/tests
pytest -v
```

---

## Debugging

### VS Code Launch Configurations

#### Debug OctoBot
```json
{
  "name": "OctoBot",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/OctoBot/start.py",
  "console": "integratedTerminal",
  "env": {
    "PYTHONPATH": "${workspaceFolder}/Async-Channel:${workspaceFolder}/OctoBot-Trading"
  }
}
```

#### Debug Tests
```json
{
  "name": "Python: Pytest",
  "type": "python",
  "request": "launch",
  "module": "pytest",
  "args": ["-v", "${file}"],
  "console": "integratedTerminal"
}
```

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Git Workflows

### Feature Branch Workflow
```bash
# Create feature branch
git checkout -b feature/add-new-exchange

# Make changes and commit
git add .
git commit -m "[Exchange] Add MyExchange connector"

# Push and create PR
git push origin feature/add-new-exchange
```

### Commit Message Format
Follow conventional commits:
```
[Module] Short description

Detailed explanation if needed.

- List of changes
- Another change
```

Examples:
- `[Exchange] Add Polymarket support`
- `[Trading] Fix order cancellation bug`
- `[Tests] Add integration tests for Binance`

---

## Async Patterns

### Entry Points
Use `asyncio.run()` for top-level async entry:
```python
import asyncio

async def main():
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
```

### Concurrent Tasks
Use `asyncio.create_task()` for background tasks:
```python
task1 = asyncio.create_task(fetch_balance())
task2 = asyncio.create_task(fetch_orders())
results = await asyncio.gather(task1, task2)
```

### Avoiding Blocking
Never use blocking operations in async code:
```python
# ❌ Wrong - blocks event loop
import time
time.sleep(1)

# ✅ Correct - async sleep
await asyncio.sleep(1)
```

---

## Configuration Management

### User Config Location
```
OctoBot/user/
├── config.json              # Global config
├── tentacles_config.json    # Tentacle configs
└── profiles/                # Trading profiles
    └── default/
        └── profile.json
```

### Modify Config Programmatically
```python
from octobot_commons.configuration import Configuration

config = Configuration()
config.load()
config.config["exchanges"]["binance"]["api_key"] = "new_key"
config.save()
```

---

## Common Issues

### Import Errors
**Problem**: `ModuleNotFoundError: No module named 'octobot_trading'`

**Solution**:
1. Check PYTHONPATH includes all repos
2. Run "Setup PYTHONPATH" task
3. Verify symlinks exist for tentacles

---

### Tentacle Not Loading
**Problem**: Tentacle not recognized by OctoBot

**Solution**:
1. Check `metadata.json` is valid JSON (not YAML)
2. Verify `origin_package` is correct
3. Regenerate tentacles package
4. Check tentacle is listed in `tentacles_config.json`

---

### CCXT Transpilation Fails
**Problem**: `npm run transpileRest` fails with syntax error

**Solution**:
1. Remove ternary operators
2. Remove type annotations
3. Use CCXT safe methods (`safeString`, `safeInteger`)
4. Check Node.js version (use 24.x)

---

### Test Failures
**Problem**: Import errors in tests

**Solution**:
Use relative imports:
```python
# ✅ Correct
from ...binance import Binance

# ❌ Wrong
from binance import Binance
```

---

## CI/CD Integration

### GitHub Actions Workflow
```yaml
name: OctoBot-CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov
```

---

## Performance Optimization

### Profiling
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()
await bot.start()
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)
```

### Memory Profiling
```bash
pip install memory_profiler
python -m memory_profiler start.py
```

---

## Documentation

### Generate API Docs
```bash
pip install pdoc3
pdoc --html --output-dir docs octobot_trading
```

### Update README
Keep README.md synchronized with:
- Version numbers
- Feature additions
- Breaking changes
- Installation instructions
