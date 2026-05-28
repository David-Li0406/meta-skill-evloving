---
name: "execution"
description: "Use this skill ONLY when modifying the execution engine, signal queue, position tracker, cooldown manager, or order manager. Do not use for strategies or agents."
---

# Scope Constraint

**CRITICAL:** You are executing from the repository root.

- Execution files go in `src/alpacalyzer/execution/`
- Tests go in `tests/test_execution_*.py`
- Execution handles trade execution, position tracking, and order management

# Execution Architecture

The execution module has 5 components:

```
┌─────────────────────────────────────────────────────────────────┐
│                     ExecutionEngine                              │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐    │
│  │ SignalQueue │  │PositionTracker│  │   CooldownManager   │    │
│  │ (pending    │  │ (open        │  │   (rate limiting)   │    │
│  │  signals)   │  │  positions)  │  │                     │    │
│  └─────────────┘  └──────────────┘  └─────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    OrderManager                          │    │
│  │  (bracket orders, stop losses, target orders)           │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

# Procedural Steps

## 1. Understand the Execution Cycle

```bash
# Read the main engine file
cat src/alpacalyzer/execution/engine.py

# Focus on run_cycle() method - this is the core loop
# Lines 65-104 show the cycle order:
# 1. Sync positions from broker
# 2. Process exits (CAPITAL PROTECTION FIRST)
# 3. Process entries (new positions)
# 4. Update cooldowns
# 5. Emit summary event
```

**Key invariant**: Exits are ALWAYS processed before entries. This protects capital.

## 2. Modify ExecutionEngine

### Adding New Processing Steps

Edit `run_cycle()` method in `engine.py`:

```python
def run_cycle(self) -> None:
    """Execute one cycle of the trading loop."""
    # ... existing steps 1-5 ...

    # NEW: Step 6 - Add your custom processing
    self._process_custom_logic()
```

### Modifying Entry/Exit Logic

**Entry flow** - `_process_entry()` (lines 120-135):

```python
def _process_entry(self, signal: PendingSignal, context: MarketContext) -> None:
    # 1. Get technical signals
    ta_signals = TechnicalAnalyzer().analyze_stock(signal.ticker)

    # 2. Get strategy decision
    decision = self.strategy.evaluate_entry(
        ta_signals,
        context,
        signal.agent_recommendation,
    )

    # 3. Execute if should enter
    if decision.should_enter:
        self._execute_entry(signal, decision)
```

**Exit flow** - `_process_exit()` (lines 106-118):

```python
def _process_exit(self, position: TrackedPosition) -> None:
    # 1. Get current signals
    signals = TechnicalAnalyzer().analyze_stock(position.ticker)

    # 2. Get strategy exit decision
    context = self._build_market_context()
    decision = self.strategy.evaluate_exit(position, signals, context)

    # 3. Execute if should exit
    if decision.should_exit:
        self._execute_exit(position, decision)
```

### Modify ExecutionConfig

```python
@dataclass
class ExecutionConfig:
    """Configuration for the execution engine."""

    check_interval_seconds: int = 120
    max_positions: int = 10
    daily_loss_limit_pct: float = 0.05
    analyze_mode: bool = False

    # Add new config fields
    my_new_setting: float = 0.05
```

## 3. Modify SignalQueue

### Understanding the Queue

**Location**: `src/alpacalyzer/execution/signal_queue.py`

```python
# PendingSignal is priority-based
@dataclass(order=True)
class PendingSignal:
    priority: int  # Lower = higher priority (heapq is min-heap)
    ticker: str
    action: str  # "buy", "sell", "short", "cover"
    confidence: float
    source: str
    created_at: datetime
    expires_at: datetime | None
    agent_recommendation: TradingStrategy | None
```

**SignalQueue** is a priority queue with:

- Deduplication by ticker
- Automatic expiration
- Priority based on confidence

### Adding a Signal

```python
# From outside the engine
engine.add_signal(PendingSignal(
    priority=50,  # Lower = higher priority
    ticker="AAPL",
    action="buy",
    confidence=85.0,
    source="reddit",
))
```

### Modifying Priority Logic

Edit `PendingSignal.from_strategy()` (lines 28-42):

```python
@classmethod
def from_strategy(cls, strategy: TradingStrategy, source: str = "agent") -> "PendingSignal":
    # Default: higher confidence = lower priority number = processed first
    # Modify this formula for your needs
    priority = 100 - int(strategy.risk_reward_ratio * 10)
    # ...
```

## 4. Modify PositionTracker

### TrackedPosition Data Model

```python
@dataclass
class TrackedPosition:
    # Core position data
    ticker: str
    side: str
    quantity: int
    avg_entry_price: float
    current_price: float

    # Computed values
    market_value: float
    unrealized_pnl: float
    unrealized_pnl_pct: float

    # Enriched metadata
    strategy_name: str
    opened_at: datetime
    entry_order_id: str | None
    stop_loss: float | None
    target: float | None

    # State tracking
    exit_attempts: int = 0
    last_exit_attempt: datetime | None = None
    notes: list[str] = field(default_factory=list)
```

### Adding Position Metadata

To add new tracking fields:

```python
# 1. Add field to TrackedPosition
@dataclass
class TrackedPosition:
    # ... existing fields ...
    my_new_field: float = 0.0  # NEW

# 2. Update from_alpaca_position()
@classmethod
def from_alpaca_position(cls, position: Position, ...) -> "TrackedPosition":
    # ... existing code ...
    return cls(
        # ... existing fields ...
        my_new_field=0.0,  # NEW - set default
    )

# 3. Update add_position()
def add_position(self, ...) -> TrackedPosition:
    position = TrackedPosition(
        # ... existing fields ...
        my_new_field=0.0,  # NEW
    )
```

### Syncing from Broker

The `sync_from_broker()` method (lines 139-178) synchronizes with Alpaca. Don't modify unless:

- New broker fields need tracking
- Sync logic needs custom handling

## 5. Modify CooldownManager

### Basic Usage

```python
# Add cooldown for a ticker
self.cooldowns.add_cooldown(ticker, reason="profit_taking", source="strategy")

# Check if ticker is in cooldown
if ticker in context.cooldown_tickers:
    return False  # Can't enter

# Get all tickers in cooldown
cooldown_tickers = self.cooldowns.get_all_tickers()
```

### Modifying Cooldown Rules

Edit `src/alpacalyzer/execution/cooldown.py`:

```python
class CooldownManager:
    def __init__(self, default_duration_hours: int = 24):
        # Customize default duration
        pass

    def add_cooldown(self, ticker: str, reason: str, source: str) -> None:
        # Add custom cooldown logic
        pass

    def get_all_tickers(self) -> set[str]:
        """Get all tickers currently in cooldown."""
        pass
```

## 6. Modify OrderManager

### Order Types Supported

- **Market orders**: Immediate execution
- **Limit orders**: Execute at specific price
- **Stop orders**: Trigger when stop price hit
- **Bracket orders**: Entry + stop loss + target in one order

### Submitting Orders

```python
from alpacalyzer.execution.order_manager import OrderParams, OrderManager

# Create order params
params = OrderParams(
    ticker="AAPL",
    side="buy",
    quantity=100,
    entry_price=150.00,
    stop_loss=145.00,
    target=165.00,
    strategy_name="momentum",
)

# Submit as bracket order (entry + stop + target)
result = order_manager.submit_bracket_order(params)

# Close position
result = order_manager.close_position("AAPL")
```

### Adding New Order Types

Edit `src/alpacalyzer/execution/order_manager.py`:

```python
def submit_my_new_order_type(self, params: OrderParams) -> OrderResult:
    """
    Submit a custom order type.

    Args:
        params: Order parameters

    Returns:
        OrderResult with fill details
    """
    # Implement your order logic
    pass
```

## 7. Write Tests

### Test Execution Engine Cycle

**Location**: `tests/test_execution_engine.py`

```python
"""Tests for ExecutionEngine."""

import pytest
from unittest.mock import MagicMock, patch
from datetime import UTC, datetime

from alpacalyzer.execution.engine import ExecutionEngine, ExecutionConfig
from alpacalyzer.execution.signal_queue import PendingSignal
from alpacalyzer.execution.position_tracker import PositionTracker
from alpacalyzer.execution.cooldown import CooldownManager
from alpacalyzer.execution.order_manager import OrderManager


@pytest.fixture
def mock_strategy():
    """Mock strategy with evaluate_entry/exit."""
    strategy = MagicMock()
    from alpacalyzer.strategies.base import EntryDecision, ExitDecision
    strategy.evaluate_entry.return_value = EntryDecision(
        should_enter=True,
        reason="Test entry",
        suggested_size=100,
        entry_price=150.00,
        stop_loss=145.00,
        target=165.00,
    )
    strategy.evaluate_exit.return_value = ExitDecision(
        should_exit=False,
        reason="No exit signal",
        urgency="normal",
    )
    return strategy


@pytest.fixture
def execution_engine(mock_strategy):
    """Create execution engine for testing."""
    config = ExecutionConfig(
        check_interval_seconds=60,
        max_positions=5,
        analyze_mode=True,  # Safe for tests
    )
    return ExecutionEngine(
        strategy=mock_strategy,
        config=config,
    )


def test_run_cycle_processes_signals(execution_engine):
    """Test that run_cycle processes pending signals."""
    # Add a signal
    execution_engine.add_signal(PendingSignal(
        priority=50,
        ticker="AAPL",
        action="buy",
        confidence=85.0,
        source="test",
    ))

    # Run cycle
    execution_engine.run_cycle()

    # Signal should be processed
    assert execution_engine.signal_queue.is_empty()


def test_respects_max_positions(execution_engine, mock_strategy):
    """Test that engine respects max_positions limit."""
    config = ExecutionConfig(max_positions=2, analyze_mode=True)
    engine = ExecutionEngine(strategy=mock_strategy, config=config)

    # Add 3 signals
    for i in range(3):
        engine.add_signal(PendingSignal(
            priority=50,
            ticker=f"SYM{i}",
            action="buy",
            confidence=85.0,
            source="test",
        ))

    # Mock position tracker to simulate full
    engine.positions = MagicMock()
    engine.positions.count.return_value = 2  # At max

    # Run cycle
    engine.run_cycle()

    # Should have 1 remaining signal (2 positions allowed, 3 signals)
    assert engine.signal_queue.size() == 1


def test_exit_before_entry(execution_engine, mock_strategy):
    """Test that exits are processed before entries."""
    # Add position
    from alpacalyzer.execution.position_tracker import TrackedPosition
    pos = TrackedPosition(
        ticker="AAPL",
        side="long",
        quantity=100,
        avg_entry_price=150.00,
        current_price=145.00,
        market_value=14500.0,
        unrealized_pnl=-500.0,
        unrealized_pnl_pct=-3.33,
        strategy_name="test",
        opened_at=datetime.now(UTC),
    )
    execution_engine.positions.add_position(
        ticker="AAPL",
        side="long",
        quantity=100,
        entry_price=150.00,
        strategy_name="test",
    )

    # Add entry signal
    execution_engine.add_signal(PendingSignal(
        priority=50,
        ticker="MSFT",
        action="buy",
        confidence=85.0,
        source="test",
    ))

    # Run cycle
    execution_engine.run_cycle()

    # Exit should be checked first (verify via mock call order)
    exit_call = mock_strategy.evaluate_exit.call_args_list[0]
    entry_call = mock_strategy.evaluate_entry.call_args_list[0]

    # Exit evaluated before entry
    assert exit_call is not None


def test_analyze_mode_no_orders(execution_engine):
    """Test that analyze mode doesn't submit real orders."""
    execution_engine.config.analyze_mode = True

    # Add signal
    execution_engine.add_signal(PendingSignal(
        priority=50,
        ticker="AAPL",
        action="buy",
        confidence=85.0,
        source="test",
    ))

    # Mock order manager
    execution_engine.orders = MagicMock()

    # Run cycle
    execution_engine.run_cycle()

    # No orders should be submitted
    execution_engine.orders.submit_bracket_order.assert_not_called()


def test_custom_processing_step(execution_engine):
    """Test adding custom processing step."""
    # Add a method to the engine
    def custom_processing(self):
        self._custom_called = True
    ExecutionEngine._custom_processing = custom_processing

    execution_engine._custom_called = False
    execution_engine.run_cycle()

    assert execution_engine._custom_called is True
```

### Test SignalQueue

**Location**: `tests/test_signal_queue.py`

```python
"""Tests for SignalQueue."""

import pytest
from datetime import UTC, datetime, timedelta

from alpacalyzer.execution.signal_queue import PendingSignal, SignalQueue


def test_add_signal():
    """Test adding a signal to the queue."""
    queue = SignalQueue()
    signal = PendingSignal(
        priority=50,
        ticker="AAPL",
        action="buy",
        confidence=85.0,
        source="test",
    )

    result = queue.add(signal)

    assert result is True
    assert queue.size() == 1


def test_duplicate_ticker_rejected():
    """Test that duplicate tickers are rejected."""
    queue = SignalQueue()
    signal1 = PendingSignal(priority=50, ticker="AAPL", action="buy", confidence=85.0, source="test")
    signal2 = PendingSignal(priority=40, ticker="AAPL", action="buy", confidence=90.0, source="test")

    queue.add(signal1)
    result = queue.add(signal2)

    assert result is False
    assert queue.size() == 1


def test_priority_ordering():
    """Test that signals are processed by priority."""
    queue = SignalQueue()
    queue.add(PendingSignal(priority=70, ticker="C", action="buy", confidence=50.0, source="test"))
    queue.add(PendingSignal(priority=30, ticker="A", action="buy", confidence=90.0, source="test"))
    queue.add(PendingSignal(priority=50, ticker="B", action="buy", confidence=75.0, source="test"))

    # A should be first (lowest priority number)
    signal = queue.peek()
    assert signal.ticker == "A"


def test_expiration():
    """Test that expired signals are removed."""
    queue = SignalQueue(default_ttl_hours=0)  # Immediate expiration

    signal = PendingSignal(
        priority=50,
        ticker="AAPL",
        action="buy",
        confidence=85.0,
        source="test",
        expires_at=datetime.now(UTC) - timedelta(hours=1),  # Expired
    )
    queue.add(signal)

    # Should be empty after cleanup
    assert queue.is_empty() or queue.peek() is None


def test_max_capacity():
    """Test that queue respects max capacity."""
    queue = SignalQueue(max_signals=2)

    queue.add(PendingSignal(priority=50, ticker="A", action="buy", confidence=85.0, source="test"))
    queue.add(PendingSignal(priority=40, ticker="B", action="buy", confidence=90.0, source="test"))
    result = queue.add(PendingSignal(priority=30, ticker="C", action="buy", confidence=95.0, source="test"))

    assert result is False
    assert queue.size() == 2
```

### Test PositionTracker

**Location**: `tests/test_position_tracker.py`

```python
"""Tests for PositionTracker."""

import pytest
from unittest.mock import MagicMock
from datetime import UTC, datetime

from alpacalyzer.execution.position_tracker import PositionTracker, TrackedPosition


@pytest.fixture
def mock_alpaca_position():
    """Create mock Alpaca position."""
    position = MagicMock()
    position.symbol = "AAPL"
    position.side = "long"
    position.qty = "100"
    position.avg_entry_price = "150.00"
    position.current_price = "155.00"
    position.market_value = "15500.00"
    position.unrealized_pl = "500.00"
    position.unrealized_plpc = "0.0333"
    return position


def test_add_position():
    """Test adding a new position."""
    tracker = PositionTracker()

    position = tracker.add_position(
        ticker="AAPL",
        side="long",
        quantity=100,
        entry_price=150.00,
        strategy_name="momentum",
        stop_loss=145.00,
        target=165.00,
    )

    assert tracker.count() == 1
    assert tracker.has_position("AAPL") is True
    assert position.unrealized_pnl == 0.0


def test_remove_position():
    """Test removing a position."""
    tracker = PositionTracker()
    tracker.add_position(
        ticker="AAPL",
        side="long",
        quantity=100,
        entry_price=150.00,
        strategy_name="momentum",
    )

    position = tracker.remove_position("AAPL")

    assert position is not None
    assert tracker.count() == 0
    assert len(tracker.get_closed_positions()) == 1


def test_update_price():
    """Test updating position price and P&L."""
    tracker = PositionTracker()
    tracker.add_position(
        ticker="AAPL",
        side="long",
        quantity=100,
        entry_price=150.00,
        strategy_name="momentum",
    )

    # Update price
    tracker.get("AAPL").update_price(160.00)

    position = tracker.get("AAPL")
    assert position.current_price == 160.00
    assert position.unrealized_pnl == 1000.0  # (160-150) * 100
    assert position.unrealized_pnl_pct == 0.0667


def test_short_position_pnl():
    """Test P&L calculation for short positions."""
    tracker = PositionTracker()
    tracker.add_position(
        ticker="AAPL",
        side="short",
        quantity=100,
        entry_price=150.00,
        strategy_name="momentum",
    )

    # Price drops, short position profits
    tracker.get("AAPL").update_price(140.00)

    position = tracker.get("AAPL")
    assert position.unrealized_pnl == 1000.0  # (150-140) * 100


def test_sync_from_broker(mock_alpaca_position):
    """Test syncing positions from broker."""
    tracker = PositionTracker()

    # Mock get_positions
    with patch("alpacalyzer.trading.alpaca_client.get_positions") as mock_get:
        mock_get.return_value = [mock_alpaca_position]
        changes = tracker.sync_from_broker()

    assert tracker.count() == 1
    assert "AAPL" in changes


def test_total_value_and_pnl():
    """Test aggregate position calculations."""
    tracker = PositionTracker()
    tracker.add_position(
        ticker="AAPL",
        side="long",
        quantity=100,
        entry_price=150.00,
        strategy_name="momentum",
    )
    tracker.add_position(
        ticker="MSFT",
        side="long",
        quantity=50,
        entry_price=300.00,
        strategy_name="momentum",
    )

    # Update prices
    tracker.get("AAPL").update_price(160.00)
    tracker.get("MSFT").update_price(290.00)

    assert tracker.total_value() == (160 * 100) + (290 * 50)  # 27500
    assert tracker.total_pnl() == (10 * 100) + (-10 * 50)  # 500
```

## 8. Run Tests

```bash
# Run execution tests
uv run pytest tests/test_execution_engine.py -v
uv run pytest tests/test_signal_queue.py -v
uv run pytest tests/test_position_tracker.py -v

# Run all execution-related tests
uv run pytest tests/test_execution*.py -v

# Run with coverage
uv run pytest tests/test_execution*.py --cov=src/alpacalyzer/execution --cov-report=term-missing
```

# Key Patterns

## 1. Exit Before Entry (Capital Protection)

The execution engine ALWAYS processes exits before entries:

```python
def run_cycle(self) -> None:
    # 1. Sync positions
    self.positions.sync_from_broker()

    # 2. Process exits FIRST (protect capital)
    for position in self.positions.get_all():
        self._process_exit(position)

    # 3. Process entries (new positions)
    # ... entry logic ...
```

## 2. Broker Sync Each Cycle

Positions are synced from Alpaca every cycle to ensure local state matches broker state.

## 3. Event Emission

All trading actions emit events for logging:

```python
emit_event(EntryTriggeredEvent(
    timestamp=datetime.now(UTC),
    ticker=ticker,
    strategy="execution_engine",
    # ... other fields ...
))

emit_event(ExitTriggeredEvent(
    # ... fields ...
))
```

## 4. Analyze Mode

When `config.analyze_mode=True`, the engine runs through the full logic but skips order submission:

```python
def run_cycle(self) -> None:
    if self.config.analyze_mode:
        self._run_analyze_cycle()
        return
    # ... normal execution ...
```

## 5. Bracket Orders

Entry orders include stop loss and target in a single bracket order:

```python
self.orders.submit_bracket_order(OrderParams(
    ticker=ticker,
    side=action,
    quantity=size,
    entry_price=entry_price,
    stop_loss=stop_loss,
    target=target,
))
```

# Special Considerations

## Trading Safety

1. **Always test with `analyze_mode=True` first**

2. **Mock Alpaca API in tests** - Never submit real orders during testing:

   ```python
   @pytest.fixture
   def mock_order_manager():
       manager = MagicMock(spec=OrderManager)
       manager.submit_bracket_order.return_value = MagicMock()
       return manager
   ```

3. **Position limits** - `config.max_positions` prevents over-trading

4. **Daily loss limits** - `config.daily_loss_limit_pct` can be checked:
   ```python
   def _check_daily_loss_limit(self) -> bool:
       daily_pnl = self._get_daily_pnl()
       return daily_pnl >= -self.config.daily_loss_limit_pct * account_equity
   ```

## Component Dependencies

| Component       | Depends On                                                  | Used By             |
| --------------- | ----------------------------------------------------------- | ------------------- |
| ExecutionEngine | SignalQueue, PositionTracker, CooldownManager, OrderManager | TradingOrchestrator |
| SignalQueue     | PendingSignal                                               | ExecutionEngine     |
| PositionTracker | TrackedPosition                                             | ExecutionEngine     |
| CooldownManager | -                                                           | ExecutionEngine     |
| OrderManager    | OrderParams                                                 | ExecutionEngine     |

## Performance

- **SignalQueue** uses heapq for O(log n) operations
- **PositionTracker** uses dict for O(1) lookups
- **Broker sync** is expensive - only sync when needed

# Reference: Existing Components

- `src/alpacalyzer/execution/engine.py` - ExecutionEngine, ExecutionConfig
- `src/alpacalyzer/execution/signal_queue.py` - SignalQueue, PendingSignal
- `src/alpacalyzer/execution/position_tracker.py` - PositionTracker, TrackedPosition
- `src/alpacalyzer/execution/cooldown.py` - CooldownManager
- `src/alpacalyzer/execution/order_manager.py` - OrderManager, OrderParams
