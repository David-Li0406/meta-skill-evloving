---
name: "pydantic-model"
description: "Use this skill ONLY when creating Pydantic data models, configs, or event types. Do not use for database models or other schemas."
---

# Scope Constraint

**CRITICAL:** You are executing from the repository root.

- Trading data models go in `src/alpacalyzer/data/models.py`
- Strategy configs go in `src/alpacalyzer/strategies/config.py` (Phase 1 migration)
- Event models go in `src/alpacalyzer/events/models.py` (Phase 3 migration)
- Execution state models go in `src/alpacalyzer/execution/models.py` (Phase 2 migration)

# Pydantic Overview

Alpacalyzer uses **Pydantic v2** for data validation, serialization, and type safety. Models are used for:

- API responses (Alpaca, OpenAI)
- Configuration (strategies, agents)
- Events (logging, analytics)
- Internal state (positions, signals)

# Procedural Steps

## 1. Determine Model Location

**Decision tree**:

| Model Purpose                     | Module                 | Example                      |
| --------------------------------- | ---------------------- | ---------------------------- |
| Trading data (signals, positions) | `data/models.py`       | TradingSignals, Position     |
| Strategy configuration            | `strategies/config.py` | StrategyConfig               |
| Event types (logging)             | `events/models.py`     | EntryEvent, ExitEvent        |
| Execution state                   | `execution/models.py`  | TrackedPosition, SignalQueue |
| Agent responses                   | `data/models.py`       | AgentResponse                |

**For new modules** (during migration): Create `models.py` in the module directory.

## 2. Review Existing Models

```bash
# See existing trading models
cat src/alpacalyzer/data/models.py

# See strategy config (if Phase 1 complete)
cat src/alpacalyzer/strategies/config.py

# See model patterns
grep -A 10 "class.*BaseModel" src/alpacalyzer/data/models.py
```

**Common patterns**:

- Inherit from `pydantic.BaseModel`
- Use `Field()` for validation and documentation
- Add docstrings for classes and complex fields
- Use type hints for all fields

## 3. Create Basic Model

**Template**:

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class <Model>Model(BaseModel):
    """
    <Brief description of what this model represents>.

    Used for: <use case>
    """

    # Required fields
    field1: str = Field(
        ...,  # ... means required
        description="Description of field1"
    )

    field2: int = Field(
        ...,
        gt=0,  # Greater than 0
        description="Description of field2"
    )

    # Optional fields
    field3: Optional[str] = Field(
        default=None,
        description="Description of field3"
    )

    # Fields with defaults
    field4: bool = Field(
        default=False,
        description="Description of field4"
    )

    # Timestamp fields
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="When this model was created"
    )

    class Config:
        """Pydantic configuration."""
        # For Pydantic v2, use ConfigDict instead
        from pydantic import ConfigDict
        model_config = ConfigDict(
            str_strip_whitespace=True,  # Strip whitespace from strings
            validate_assignment=True,    # Validate on field assignment
            arbitrary_types_allowed=False  # Strict type checking
        )
```

## 4. Add Field Validation

**Pydantic v2 validation**:

```python
from pydantic import BaseModel, Field, field_validator, model_validator


class TradingSignal(BaseModel):
    """Trading signal with validation."""

    symbol: str = Field(..., min_length=1, max_length=5)
    price: float = Field(..., gt=0)
    score: float = Field(..., ge=0.0, le=1.0)
    momentum: float

    @field_validator('symbol')
    @classmethod
    def symbol_must_be_uppercase(cls, v: str) -> str:
        """Ensure symbol is uppercase."""
        return v.upper()

    @field_validator('momentum')
    @classmethod
    def momentum_must_be_reasonable(cls, v: float) -> float:
        """Ensure momentum is within reasonable bounds."""
        if abs(v) > 100:
            raise ValueError("Momentum cannot exceed ±100%")
        return v

    @model_validator(mode='after')
    def validate_signal_consistency(self) -> 'TradingSignal':
        """Validate signal makes sense as a whole."""
        if self.score > 0.8 and self.momentum < -10:
            # High score but negative momentum - questionable
            pass  # Could raise ValueError or adjust score
        return self
```

## 5. Add Complex Field Types

**Using TypedDict, Literal, Union**:

```python
from typing import Literal, Union
from pydantic import BaseModel, Field


class OrderParams(BaseModel):
    """Parameters for placing an order."""

    side: Literal["buy", "sell"] = Field(..., description="Order side")

    order_type: Literal["market", "limit", "stop", "stop_limit"] = Field(
        default="market",
        description="Order type"
    )

    time_in_force: Literal["day", "gtc", "ioc", "fok"] = Field(
        default="day",
        description="Time in force"
    )

    quantity: int = Field(..., gt=0, description="Number of shares")

    limit_price: Optional[float] = Field(
        default=None,
        gt=0,
        description="Limit price (required for limit orders)"
    )

    stop_price: Optional[float] = Field(
        default=None,
        gt=0,
        description="Stop price (required for stop orders)"
    )

    @model_validator(mode='after')
    def validate_order_prices(self) -> 'OrderParams':
        """Validate prices match order type."""
        if self.order_type == "limit" and self.limit_price is None:
            raise ValueError("limit_price required for limit orders")
        if self.order_type == "stop" and self.stop_price is None:
            raise ValueError("stop_price required for stop orders")
        return self
```

## 6. Create Configuration Models

**For strategies, agents, etc.**:

```python
from dataclasses import dataclass, field
from pydantic import BaseModel, Field


class StrategyConfig(BaseModel):
    """Configuration for a trading strategy."""

    name: str = Field(..., description="Strategy name")
    description: str = Field(default="", description="Strategy description")

    # Position sizing
    max_position_pct: float = Field(
        default=0.05,
        ge=0.01,
        le=0.2,
        description="Max position size as % of portfolio (1-20%)"
    )

    # Risk management
    stop_loss_pct: float = Field(
        default=0.03,
        ge=0.005,
        le=0.1,
        description="Stop loss as % (0.5-10%)"
    )

    target_pct: float = Field(
        default=0.09,
        ge=0.01,
        le=0.5,
        description="Target profit as % (1-50%)"
    )

    # Strategy-specific parameters
    params: dict[str, Union[str, int, float, bool]] = Field(
        default_factory=dict,
        description="Additional strategy parameters"
    )

    @field_validator('target_pct')
    @classmethod
    def target_exceeds_stop(cls, v: float, info) -> float:
        """Ensure target is larger than stop loss."""
        stop_loss = info.data.get('stop_loss_pct', 0)
        if v <= stop_loss:
            raise ValueError("target_pct must exceed stop_loss_pct")
        return v
```

## 7. Create Event Models (Phase 3 Migration)

**For structured logging**:

```python
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class EventType(str, Enum):
    """Event types for logging."""
    SCAN_COMPLETE = "scan_complete"
    SIGNAL_GENERATED = "signal_generated"
    ENTRY_TRIGGERED = "entry_triggered"
    EXIT_TRIGGERED = "exit_triggered"
    ORDER_FILLED = "order_filled"


class BaseEvent(BaseModel):
    """Base class for all events."""

    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: Optional[str] = None


class EntryTriggeredEvent(BaseEvent):
    """Event when entry conditions are met."""

    event_type: EventType = EventType.ENTRY_TRIGGERED

    ticker: str
    strategy: str
    entry_price: float
    quantity: int
    stop_loss: float
    target: float
    reason: str
    confidence: Optional[float] = None

    def to_log_string(self) -> str:
        """Convert to human-readable log string."""
        return (
            f"[ENTRY] {self.ticker} @ ${self.entry_price:.2f} "
            f"({self.quantity} shares, {self.strategy} strategy) - {self.reason}"
        )
```

## 8. Test Models

**Location**: `tests/test_<module>_models.py`

**Test template**:

```python
"""Tests for <module> Pydantic models."""

import pytest
from pydantic import ValidationError

from alpacalyzer.<module>.models import <Model>


def test_<model>_valid_creation():
    """Test creating valid model instance."""

    model = <Model>(
        field1="value1",
        field2=42,
        field3="optional"
    )

    assert model.field1 == "value1"
    assert model.field2 == 42
    assert model.field3 == "optional"


def test_<model>_required_fields():
    """Test model requires necessary fields."""

    # Missing required field should raise error
    with pytest.raises(ValidationError) as exc_info:
        <Model>(field1="value1")  # Missing field2

    # Check error message
    errors = exc_info.value.errors()
    assert any(e['loc'] == ('field2',) for e in errors)


def test_<model>_field_validation():
    """Test field validators work correctly."""

    # Invalid value should raise error
    with pytest.raises(ValidationError) as exc_info:
        <Model>(
            field1="value1",
            field2=-1  # Assuming field2 must be > 0
        )

    errors = exc_info.value.errors()
    assert any('field2' in str(e) for e in errors)


def test_<model>_defaults():
    """Test default values are set correctly."""

    model = <Model>(
        field1="value1",
        field2=42
        # field3 and field4 should use defaults
    )

    assert model.field3 is None
    assert model.field4 is False


def test_<model>_serialization():
    """Test model serialization to dict/JSON."""

    model = <Model>(field1="value1", field2=42)

    # To dict
    data = model.model_dump()
    assert isinstance(data, dict)
    assert data['field1'] == "value1"

    # To JSON
    json_str = model.model_dump_json()
    assert isinstance(json_str, str)

    # From dict
    model2 = <Model>.model_validate(data)
    assert model2.field1 == model.field1


def test_<model>_model_validator():
    """Test cross-field validation works."""

    # Create scenario that should trigger model validator
    with pytest.raises(ValidationError):
        <Model>(
            field1="value1",
            field2=10,
            # ... fields that violate cross-field constraint
        )
```

## 9. Export Models

Add to module's `__init__.py`:

```python
from alpacalyzer.<module>.models import <Model>, <AnotherModel>

__all__ = [
    "<Model>",
    "<AnotherModel>",
]
```

## 10. Document Models

Add comprehensive docstrings:

```python
class TradingSignal(BaseModel):
    """
    Trading signal representing a potential trading opportunity.

    This model encapsulates technical analysis results, price data,
    and derived metrics used to evaluate entry/exit conditions.

    Attributes:
        symbol: Stock ticker symbol (1-5 uppercase letters)
        price: Current market price in USD (must be positive)
        score: Technical analysis score 0.0-1.0 (higher = more bullish)
        momentum: Price momentum as percentage (-100 to +100)
        signals: List of technical indicator signals
        atr: Average True Range for volatility measurement

    Example:
        >>> signal = TradingSignal(
        ...     symbol="AAPL",
        ...     price=150.00,
        ...     score=0.75,
        ...     momentum=5.2,
        ...     signals=["Golden Cross", "RSI Bullish"],
        ...     atr=3.0
        ... )
        >>> signal.symbol
        'AAPL'
    """
```

# Reference: Existing Models

- `src/alpacalyzer/data/models.py` - TradingSignals, Position, AgentResponse, TradingStrategy
- `migration_roadmap.md` Phase 1 - StrategyConfig, MarketContext, EntryDecision, ExitDecision
- `migration_roadmap.md` Phase 3 - Event models

# Special Considerations

1. **Pydantic v2**: Use `model_dump()`, `model_validate()`, `ConfigDict` (not v1 syntax)

2. **Type Safety**: Use proper type hints. Pydantic enforces them at runtime.

3. **Validation**: Use validators for business logic constraints, not just type checking.

4. **Serialization**: Models should serialize cleanly to JSON for logging/API responses.

5. **Performance**: Pydantic validation has overhead. Cache validated instances when possible.

6. **Migration**: New models for migration phases should follow the architecture in `migration_roadmap.md`.

7. **Testing**: Always test validation logic, especially custom validators and cross-field constraints.

## Pydantic v2 Migration Notes

If updating v1 models to v2:

```python
# v1 (OLD)
class OldModel(BaseModel):
    field: int

    class Config:
        validate_assignment = True

# v2 (NEW)
from pydantic import ConfigDict

class NewModel(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    field: int

# v1 validators (OLD)
@validator('field')
def validate_field(cls, v):
    return v

# v2 validators (NEW)
@field_validator('field')
@classmethod
def validate_field(cls, v: int) -> int:
    return v
```
