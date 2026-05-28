# Architecture

## Repository Structure and Layers

OctoBot Stack follows a strict layered architecture where each layer can only depend on layers below it.

### Core Layer (Foundational)

These repositories provide fundamental functionality and have **no dependencies** on higher layers.

#### OctoBot-Commons
**Purpose**: Shared utilities and common functionality used across all repositories.

**Key modules**:
- `configuration/` - Config file parsing, validation, and management
- `logging/` - Centralized logging setup
- `channels_name.py` - Channel naming constants for async messaging
- `databases/` - Database abstractions
- `dataclasses/` - Shared data structures (`UpdatableDataclass`, `ProfileData`)
- `tentacles_management/` - Tentacle loading and management
- `symbols/` - Symbol parsing and normalization
- `cryptography/` - AES, RSA, ECDSA encryption functions
- `time_frame_manager.py` - Time frame handling utilities
- `authentication.py` - Auth helpers
- Utility modules: `data_util.py`, `dict_util.py`, `list_util.py`, `number_util.py`, etc.

**Import example**:
```python
import octobot_commons.configuration as configuration
import octobot_commons.logging as logging
import octobot_commons.tentacles_management as tentacles_management
```

**When to modify**: Adding shared utilities, config formats, or data structures used by multiple repos.

---

#### Async-Channel
**Purpose**: Asynchronous message passing system for decoupled component communication.

**Key concepts**:
- Channels for pub/sub messaging
- Producers/consumers pattern
- Event-driven architecture

**Usage**: When components need to communicate without direct coupling (e.g., exchange updates triggering strategy evaluations).

---

#### OctoBot-Trading
**Purpose**: Core trading engine - handles exchange connections, order management, portfolio tracking.

**Key modules**:
- `exchanges/` - Exchange API abstractions
  - `abstract_exchange.py` - Base `RestExchange` class
  - `ccxt_connector.py` - CCXT library integration
  - Specific exchange implementations (via tentacles)
- `personal_data/` - Orders, trades, positions, portfolio
  - `orders/order.py` - Order lifecycle management
  - `portfolio/portfolio.py` - Balance and PNL tracking
  - `positions/position.py` - Leveraged positions
- `modes/` - Trading mode framework
- `signals/` - Trading signal system
- `accounts/` - Account management
- `blockchain_wallets/` - Blockchain wallet integration (abstract classes)
- `storage/` - Data persistence
- `util/` - Trading utilities

**Import example**:
```python
import octobot_trading.exchanges as exchanges
import octobot_trading.personal_data as personal_data
```

**When to modify**: Adding exchange features, order types, portfolio calculations, or trading execution logic.

---

#### OctoBot-Evaluators
**Purpose**: Strategy and indicator evaluation framework.

**Key concepts**:
- Evaluator base classes
- Matrix evaluations
- Signal generation

**When to modify**: Adding new evaluation frameworks or indicator types (actual evaluators are in tentacles).

---

#### OctoBot-Backtesting
**Purpose**: Historical data simulation engine.

**Key modules**:
- Data collection and replay
- Exchange simulators
- Performance metrics

**When to modify**: Improving backtesting accuracy, adding new data sources, or performance metrics.

---

#### trading-backend
**Purpose**: Backend services for web interfaces and APIs.

**When to modify**: Adding API endpoints or backend services.

---

### Extension Layer (Tentacles)

#### OctoBot-Tentacles
**Purpose**: Plugin system for exchanges, strategies, evaluators, and services.

**Structure**:
```
OctoBot-Tentacles/
├── Trading/
│   ├── Exchange/         # Exchange connectors
│   │   ├── binance/
│   │   ├── coinbase/
│   │   ├── polymarket/
│   │   └── ...
│   └── Mode/             # Trading strategies
├── Evaluator/            # Strategy evaluators
│   ├── TA/               # Technical analysis
│   └── ...
├── Services/             # External services (Telegram, Twitter, etc.)
└── Meta/                 # Metadata and configs
```

**Tentacle types**:
- **Exchange tentacles**: Connect to crypto exchanges (Binance, Coinbase, etc.)
- **Mode tentacles**: Trading strategies (grid trading, arbitrage, etc.)
- **Evaluator tentacles**: Technical indicators, signal generators
- **Service tentacles**: Integrations (notifications, webhooks)

**When to modify**: Adding new exchanges, strategies, or services.

---

### Application Layer

These are end-user applications that orchestrate the core and extension layers.

#### OctoBot
**Purpose**: Main bot application with CLI, web interface, and orchestration.

**Key modules**:
- `octobot.py` - Main bot class
- `initializer.py` - Startup initialization
- `cli.py` - Command-line interface
- `api/` - REST API
- `community/` - Community features
- `automation/` - Automation framework
- `strategy_optimizer/` - Strategy optimization
- `backtesting/` - Backtesting orchestration
- `updater/` - Auto-update system

**When to modify**: Adding UI features, CLI commands, or high-level orchestration.

---

#### Specialized Applications
- **OctoBot-Script**: Lightweight scripting interface
- **OctoBot-Binary**: Compiled distribution
- **OctoBot-Market-Making**: Market making bot
- **OctoBot-Prediction-Market**: Prediction market bot (e.g., Polymarket)

---

### Tooling Layer

#### OctoBot-Tentacles-Manager
**Purpose**: Tentacle installation, updates, and management.

**Usage**: `python start.py tentacles --install --all`

---

#### Package-Version-Manager
**Purpose**: Version synchronization across repositories.

---

## Dependency Rules

### ✅ Allowed Dependencies
- Core → Core (e.g., OctoBot-Trading can import OctoBot-Commons)
- Extension → Core (e.g., Tentacles can import OctoBot-Trading)
- Application → Extension (e.g., OctoBot can import tentacles)
- Application → Core (e.g., OctoBot can import OctoBot-Trading)

### ❌ Forbidden Dependencies
- Core → Extension or Application (breaks modularity)
- Extension → Application (tentacles must be reusable)

### Import Pattern
Always use absolute imports with `octobot_` prefix:
```python
# ✅ Correct
import octobot_trading.exchanges as exchanges
from octobot_commons.configuration import Configuration

# ❌ Wrong
from exchanges import RestExchange  # Ambiguous
import OctoBot.cli  # Core importing Application
```

---

## Communication Patterns

### Async Channels
Components communicate via `Async-Channel` for loose coupling:
```python
# Producer
from async_channel import Channel, Producer
channel = Channel()
producer = Producer(channel)
await producer.send(data)

# Consumer
from async_channel import Consumer
consumer = Consumer(channel)
async for message in consumer:
    process(message)
```

### Direct Calls
Within the same layer, direct function calls are acceptable:
```python
from octobot_trading.exchanges import RestExchange
exchange = RestExchange()
await exchange.fetch_balance()
```

---

## Data Flow

```
External Exchange APIs
         ↓
   OctoBot-Trading (via CCXT)
         ↓
   Async-Channel messages
         ↓
   OctoBot-Evaluators
         ↓
   Trading Signals
         ↓
   OctoBot (orchestration)
         ↓
   Order Execution (back to OctoBot-Trading)
```

---

## Integration Points

### CCXT Library
OctoBot uses CCXT for standardized exchange APIs:
- TypeScript source: `ccxt/ts/src/*.ts`
- Transpiled to Python: `ccxt/python/ccxt/`
- Connected via `CCXTConnector` in OctoBot-Trading

### Tentacle Loading
1. OctoBot-Tentacles-Manager installs tentacles as Python packages
2. OctoBot-Commons loads tentacles dynamically at runtime
3. Application layer registers tentacles with their respective frameworks

### Backtesting Integration
- OctoBot-Backtesting replays historical data
- OctoBot-Trading operates in simulation mode
- Exchange APIs return historical data instead of live data

---

## Configuration Management

**Config hierarchy**:
1. Global config: `OctoBot/user/config.json`
2. Profile configs: `OctoBot/user/profiles/*/`
3. Tentacle-specific configs: `OctoBot/user/tentacles_config.json`

**Config loading**:
```python
from octobot_commons.configuration import Configuration
config = Configuration()
config.load()
```

---

## Testing Architecture

Each repository has its own test suite:
- Unit tests: `tests/` directories
- Integration tests: `additional_tests/`
- Use `pytest` with fixtures and parameterization
- Mock external dependencies (exchanges, APIs)

**Test coverage goals**: >80% for core modules, >60% for application code.
