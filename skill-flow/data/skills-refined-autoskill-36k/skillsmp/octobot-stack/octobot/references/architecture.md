# Architecture

## Application Structure

```
OctoBot/
├── start.py                 # Entry point
├── octobot/
│   ├── __init__.py
│   ├── octobot.py          # Main bot class
│   ├── initializer.py      # Initialization logic
│   ├── task_manager.py     # Async task management
│   ├── api/                # Internal API
│   ├── community/          # Community features
│   ├── strategy_optimizer/ # Strategy optimization
│   ├── updater/            # Auto-update system
│   └── constants.py        # Global constants
├── user/                   # User data (gitignored)
│   ├── config.json
│   ├── profiles/
│   └── logs/
├── tentacles/              # Symlink to OctoBot-Tentacles
└── tests/
```

## Main Bot Class

```python
# octobot/octobot.py
class OctoBot:
    """Main bot orchestration class"""
    
    def __init__(self, config_file: str = "user/config.json"):
        self.config = None
        self.config_file = config_file
        self.exchange_producers = {}
        self.exchange_traders = {}
        self.trading_modes = {}
        self.evaluators = {}
        self.service_feeds = {}
        
    async def initialize(self):
        """Initialize all bot components"""
        # Load configuration
        await self._load_config()
        
        # Initialize tentacles
        await self._init_tentacles()
        
        # Initialize exchanges
        await self._init_exchanges()
        
        # Initialize evaluators
        await self._init_evaluators()
        
        # Initialize trading modes
        await self._init_trading_modes()
        
        # Initialize services
        await self._init_services()
        
        # Start web interface
        await self._start_web_interface()
    
    async def start(self):
        """Start bot operations"""
        # Start exchange feeds
        await self._start_exchange_producers()
        
        # Start evaluators
        await self._start_evaluators()
        
        # Start trading modes
        await self._start_trading_modes()
        
        # Start services
        await self._start_services()
```

## Initialization Flow

### 1. Configuration Loading
```python
async def _load_config(self):
    """Load bot configuration from JSON"""
    with open(self.config_file) as f:
        self.config = json.load(f)
    
    # Validate configuration
    self._validate_config()
    
    # Apply environment variables
    self._apply_env_overrides()
```

### 2. Tentacle Loading
```python
async def _init_tentacles(self):
    """Load and initialize tentacles"""
    from octobot_tentacles_manager.api import load_tentacles
    
    # Load tentacles from directory
    self.tentacles = await load_tentacles(
        tentacles_path="tentacles"
    )
    
    # Register tentacles with managers
    await self._register_tentacles()
```

### 3. Exchange Initialization
```python
async def _init_exchanges(self):
    """Initialize configured exchanges"""
    for exchange_name, exchange_config in self.config["exchanges"].items():
        if not exchange_config.get("enabled", False):
            continue
        
        # Create exchange instance
        exchange = await self._create_exchange(
            exchange_name,
            exchange_config
        )
        
        # Create trading instance
        trader = await self._create_trader(exchange)
        
        self.exchange_producers[exchange_name] = exchange
        self.exchange_traders[exchange_name] = trader
```

### 4. Evaluator Initialization
```python
async def _init_evaluators(self):
    """Initialize evaluation system"""
    from octobot_evaluators.api import create_evaluators
    
    for symbol in self.config["crypto-currencies"]:
        # Create evaluator matrix
        matrix = Matrix()
        
        # Initialize technical evaluators
        technical_evaluators = await create_evaluators(
            symbol=symbol,
            evaluator_type="TA"
        )
        
        # Initialize social evaluators
        social_evaluators = await create_evaluators(
            symbol=symbol,
            evaluator_type="Social"
        )
        
        # Initialize strategy evaluators
        strategy_evaluators = await create_evaluators(
            symbol=symbol,
            evaluator_type="Strategy"
        )
        
        self.evaluators[symbol] = {
            "matrix": matrix,
            "technical": technical_evaluators,
            "social": social_evaluators,
            "strategy": strategy_evaluators
        }
```

### 5. Trading Mode Activation
```python
async def _init_trading_modes(self):
    """Initialize trading modes"""
    from octobot_trading.api import create_trading_modes
    
    mode_name = self.config.get("trading-mode", "SimpleTrader")
    
    for exchange_name in self.exchange_traders:
        trader = self.exchange_traders[exchange_name]
        
        # Create trading mode instance
        mode = await create_trading_modes(
            mode_class=mode_name,
            exchange_trader=trader
        )
        
        self.trading_modes[exchange_name] = mode
```

## Component Communication

### Async Channel Integration
```python
# Producer (Exchange) → Channel → Consumer (Evaluator)
from async_channel import Channel, Producer, Consumer

# Exchange produces price updates
price_channel = Channel("price_updates")
exchange_producer = Producer(price_channel)

await exchange_producer.send({
    "symbol": "BTC/USDT",
    "price": 50000,
    "timestamp": time.time()
})

# Evaluator consumes price updates
evaluator_consumer = Consumer(price_channel)
async for price_update in evaluator_consumer:
    await evaluator.process(price_update)
```

## Task Management

```python
class TaskManager:
    """Manage async tasks"""
    
    def __init__(self):
        self.tasks = []
    
    def create_task(self, coro, name: str = None):
        """Create and track async task"""
        task = asyncio.create_task(coro, name=name)
        self.tasks.append(task)
        return task
    
    async def stop_all(self):
        """Cancel all running tasks"""
        for task in self.tasks:
            task.cancel()
        
        await asyncio.gather(*self.tasks, return_exceptions=True)
```

## Error Handling

```python
async def _safe_task_wrapper(self, coro, name: str):
    """Wrap task with error handling"""
    try:
        await coro
    except asyncio.CancelledError:
        self.logger.info(f"Task {name} cancelled")
    except Exception as e:
        self.logger.error(f"Task {name} failed: {e}")
        # Notify user via services
        await self._notify_error(name, e)
```

## Web Interface

```python
async def _start_web_interface(self):
    """Start web dashboard"""
    from octobot.api import WebInterface
    
    self.web_interface = WebInterface(
        bot=self,
        port=self.config.get("web-port", 5001)
    )
    
    await self.web_interface.start()
```
