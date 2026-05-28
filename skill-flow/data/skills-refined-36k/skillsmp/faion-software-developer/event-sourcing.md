---
id: event-sourcing
name: "Event Sourcing"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Event Sourcing

## Overview

Event Sourcing persists the state of an entity as a sequence of state-changing events. Instead of storing current state, you store all events that led to it. The current state is derived by replaying events.

## When to Use

- Complete audit trail required
- Complex domain with temporal queries
- Event-driven architectures
- Systems requiring state reconstruction
- Financial or compliance-heavy applications

## Key Principles

1. **Events are immutable** - Once stored, events never change
2. **Events are the source of truth** - State is derived from events
3. **Event order matters** - Events must be applied in sequence
4. **Snapshots for performance** - Periodically save state snapshots
5. **Projections for queries** - Build read models from events

## Best Practices

### Event Sourcing Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Command Handler                          │
│  1. Load events from store                                    │
│  2. Reconstruct aggregate                                     │
│  3. Execute command (generate new events)                     │
│  4. Persist new events                                        │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                       Event Store                             │
│  ┌─────────┬─────────┬───────────┬──────────────────────┐    │
│  │ EventId │ StreamId│  Version  │     Event Data        │    │
│  ├─────────┼─────────┼───────────┼──────────────────────┤    │
│  │    1    │ order-1 │     1     │ OrderCreated {...}   │    │
│  │    2    │ order-1 │     2     │ ItemAdded {...}      │    │
│  │    3    │ order-1 │     3     │ ItemAdded {...}      │    │
│  │    4    │ order-1 │     4     │ OrderPlaced {...}    │    │
│  └─────────┴─────────┴───────────┴──────────────────────┘    │
└───────────────────────────┬──────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                      Projections                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Order Details│  │ Customer     │  │ Analytics    │       │
│  │ Projection   │  │ Orders List  │  │ Projection   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└──────────────────────────────────────────────────────────────┘
```

### Event Definitions

```python
# domain/events/base.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Event:
    """Base class for all domain events."""
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict = field(default_factory=dict)


# domain/events/order_events.py
from dataclasses import dataclass
from decimal import Decimal
from typing import List
from uuid import UUID


@dataclass(frozen=True)
class OrderCreated(Event):
    """Event when order is created."""
    order_id: UUID
    customer_id: UUID


@dataclass(frozen=True)
class OrderItemAdded(Event):
    """Event when item is added to order."""
    order_id: UUID
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: Decimal


@dataclass(frozen=True)
class OrderItemRemoved(Event):
    """Event when item is removed from order."""
    order_id: UUID
    product_id: UUID


@dataclass(frozen=True)
class OrderPlaced(Event):
    """Event when order is placed."""
    order_id: UUID
    shipping_address: dict
    total_amount: Decimal


@dataclass(frozen=True)
class OrderShipped(Event):
    """Event when order is shipped."""
    order_id: UUID
    tracking_number: str
    carrier: str


@dataclass(frozen=True)
class OrderDelivered(Event):
    """Event when order is delivered."""
    order_id: UUID
    delivered_at: datetime
    signature: Optional[str] = None


@dataclass(frozen=True)
class OrderCancelled(Event):
    """Event when order is cancelled."""
    order_id: UUID
    reason: str
    cancelled_by: UUID
```

### Event-Sourced Aggregate

```python
# domain/aggregates/order.py
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID

from domain.events.order_events import *


class OrderStatus(Enum):
    DRAFT = "draft"
    PLACED = "placed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class OrderItem:
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: Decimal

    @property
    def total(self) -> Decimal:
        return self.unit_price * self.quantity


@dataclass
class Order:
    """Event-sourced Order aggregate."""

    id: UUID
    customer_id: UUID = None
    status: OrderStatus = OrderStatus.DRAFT
    items: List[OrderItem] = field(default_factory=list)
    shipping_address: dict = None
    tracking_number: str = None
    version: int = 0
    _pending_events: List[Event] = field(default_factory=list, repr=False)

    @classmethod
    def create(cls, order_id: UUID, customer_id: UUID) -> "Order":
        """Factory method - creates new order with initial event."""
        order = cls(id=order_id)
        order._apply(OrderCreated(order_id=order_id, customer_id=customer_id))
        return order

    @classmethod
    def from_events(cls, order_id: UUID, events: List[Event]) -> "Order":
        """Reconstruct order from event history."""
        order = cls(id=order_id)
        for event in events:
            order._apply(event, is_new=False)
        return order

    def add_item(
        self,
        product_id: UUID,
        product_name: str,
        quantity: int,
        unit_price: Decimal,
    ) -> None:
        """Add item to order."""
        if self.status != OrderStatus.DRAFT:
            raise DomainError("Cannot modify placed order")

        if quantity <= 0:
            raise DomainError("Quantity must be positive")

        # Check if already in order
        if any(item.product_id == product_id for item in self.items):
            raise DomainError("Product already in order")

        self._apply(OrderItemAdded(
            order_id=self.id,
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            unit_price=unit_price,
        ))

    def remove_item(self, product_id: UUID) -> None:
        """Remove item from order."""
        if self.status != OrderStatus.DRAFT:
            raise DomainError("Cannot modify placed order")

        if not any(item.product_id == product_id for item in self.items):
            raise DomainError("Product not in order")

        self._apply(OrderItemRemoved(order_id=self.id, product_id=product_id))

    def place(self, shipping_address: dict) -> None:
        """Place the order."""
        if self.status != OrderStatus.DRAFT:
            raise DomainError("Order already placed")

        if not self.items:
            raise DomainError("Cannot place empty order")

        self._apply(OrderPlaced(
            order_id=self.id,
            shipping_address=shipping_address,
            total_amount=self.total,
        ))

    def ship(self, tracking_number: str, carrier: str) -> None:
        """Ship the order."""
        if self.status != OrderStatus.PLACED:
            raise DomainError("Order must be placed before shipping")

        self._apply(OrderShipped(
            order_id=self.id,
            tracking_number=tracking_number,
            carrier=carrier,
        ))

    def cancel(self, reason: str, cancelled_by: UUID) -> None:
        """Cancel the order."""
        if self.status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            raise DomainError("Cannot cancel shipped order")

        self._apply(OrderCancelled(
            order_id=self.id,
            reason=reason,
            cancelled_by=cancelled_by,
        ))

    @property
    def total(self) -> Decimal:
        return sum(item.total for item in self.items)

    def _apply(self, event: Event, is_new: bool = True) -> None:
        """Apply event to aggregate state."""
        # Route to appropriate handler
        handler_name = f"_on_{self._to_snake_case(type(event).__name__)}"
        handler = getattr(self, handler_name, None)

        if handler:
            handler(event)

        self.version += 1

        if is_new:
            self._pending_events.append(event)

    def _on_order_created(self, event: OrderCreated) -> None:
        self.customer_id = event.customer_id
        self.status = OrderStatus.DRAFT

    def _on_order_item_added(self, event: OrderItemAdded) -> None:
        self.items.append(OrderItem(
            product_id=event.product_id,
            product_name=event.product_name,
            quantity=event.quantity,
            unit_price=event.unit_price,
        ))

    def _on_order_item_removed(self, event: OrderItemRemoved) -> None:
        self.items = [i for i in self.items if i.product_id != event.product_id]

    def _on_order_placed(self, event: OrderPlaced) -> None:
        self.shipping_address = event.shipping_address
        self.status = OrderStatus.PLACED

    def _on_order_shipped(self, event: OrderShipped) -> None:
        self.tracking_number = event.tracking_number
        self.status = OrderStatus.SHIPPED

    def _on_order_cancelled(self, event: OrderCancelled) -> None:
        self.status = OrderStatus.CANCELLED

    def collect_pending_events(self) -> List[Event]:
        """Get and clear pending events."""
        events = self._pending_events.copy()
        self._pending_events.clear()
        return events

    @staticmethod
    def _to_snake_case(name: str) -> str:
        import re
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
```

### Event Store

```python
# infrastructure/event_store/event_store.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.events.base import Event


class EventStore(ABC):
    """Abstract event store interface."""

    @abstractmethod
    async def append(
        self,
        stream_id: str,
        events: List[Event],
        expected_version: int,
    ) -> None:
        """Append events to stream with optimistic concurrency."""
        pass

    @abstractmethod
    async def read_stream(
        self,
        stream_id: str,
        from_version: int = 0,
    ) -> List[Event]:
        """Read all events from a stream."""
        pass

    @abstractmethod
    async def read_all(
        self,
        from_position: int = 0,
        batch_size: int = 100,
    ) -> List[Event]:
        """Read all events across all streams."""
        pass


# infrastructure/event_store/postgres_event_store.py
import json
from typing import List
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class PostgresEventStore(EventStore):
    """PostgreSQL implementation of event store."""

    def __init__(self, session: AsyncSession):
        self._session = session
        self._serializers: dict = {}

    def register_serializer(self, event_type: type, serializer) -> None:
        self._serializers[event_type] = serializer

    async def append(
        self,
        stream_id: str,
        events: List[Event],
        expected_version: int,
    ) -> None:
        """Append events with optimistic concurrency check."""

        # Check current version
        result = await self._session.execute(
            text("""
                SELECT COALESCE(MAX(version), 0) as version
                FROM events WHERE stream_id = :stream_id
            """),
            {"stream_id": stream_id},
        )
        current_version = result.scalar()

        if current_version != expected_version:
            raise ConcurrencyError(
                f"Expected version {expected_version}, got {current_version}"
            )

        # Insert events
        for i, event in enumerate(events):
            version = expected_version + i + 1
            await self._session.execute(
                text("""
                    INSERT INTO events (
                        event_id, stream_id, version, event_type,
                        event_data, metadata, occurred_at
                    ) VALUES (
                        :event_id, :stream_id, :version, :event_type,
                        :event_data, :metadata, :occurred_at
                    )
                """),
                {
                    "event_id": str(event.event_id),
                    "stream_id": stream_id,
                    "version": version,
                    "event_type": type(event).__name__,
                    "event_data": json.dumps(self._serialize(event)),
                    "metadata": json.dumps(event.metadata),
                    "occurred_at": event.occurred_at,
                },
            )

        await self._session.commit()

    async def read_stream(
        self,
        stream_id: str,
        from_version: int = 0,
    ) -> List[Event]:
        """Read events from stream."""
        result = await self._session.execute(
            text("""
                SELECT event_type, event_data, metadata, occurred_at
                FROM events
                WHERE stream_id = :stream_id AND version > :from_version
                ORDER BY version ASC
            """),
            {"stream_id": stream_id, "from_version": from_version},
        )

        events = []
        for row in result:
            event = self._deserialize(
                event_type=row.event_type,
                data=json.loads(row.event_data),
                metadata=json.loads(row.metadata),
                occurred_at=row.occurred_at,
            )
            events.append(event)

        return events

    def _serialize(self, event: Event) -> dict:
        """Serialize event to dict."""
        serializer = self._serializers.get(type(event))
        if serializer:
            return serializer.serialize(event)

        # Default: use dataclass fields
        return {
            k: str(v) if isinstance(v, UUID) else v
            for k, v in event.__dict__.items()
            if k not in ('event_id', 'occurred_at', 'metadata')
        }

    def _deserialize(
        self,
        event_type: str,
        data: dict,
        metadata: dict,
        occurred_at: datetime,
    ) -> Event:
        """Deserialize event from stored data."""
        # Get event class from registry
        event_class = EVENT_REGISTRY.get(event_type)
        if not event_class:
            raise UnknownEventType(event_type)

        return event_class(**data, metadata=metadata, occurred_at=occurred_at)
```

### Snapshots

```python
# infrastructure/event_store/snapshot_store.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import json


@dataclass
class Snapshot:
    stream_id: str
    version: int
    state: dict
    created_at: datetime


class SnapshotStore:
    """Store for aggregate snapshots."""

    def __init__(self, session):
        self._session = session

    async def save(self, snapshot: Snapshot) -> None:
        await self._session.execute(
            text("""
                INSERT INTO snapshots (stream_id, version, state, created_at)
                VALUES (:stream_id, :version, :state, :created_at)
                ON CONFLICT (stream_id) DO UPDATE SET
                    version = :version,
                    state = :state,
                    created_at = :created_at
            """),
            {
                "stream_id": snapshot.stream_id,
                "version": snapshot.version,
                "state": json.dumps(snapshot.state),
                "created_at": snapshot.created_at,
            },
        )

    async def get(self, stream_id: str) -> Optional[Snapshot]:
        result = await self._session.execute(
            text("SELECT * FROM snapshots WHERE stream_id = :stream_id"),
            {"stream_id": stream_id},
        )
        row = result.fetchone()
        if row:
            return Snapshot(
                stream_id=row.stream_id,
                version=row.version,
                state=json.loads(row.state),
                created_at=row.created_at,
            )
        return None


# Repository with snapshot support
class EventSourcedOrderRepository:
    SNAPSHOT_FREQUENCY = 50  # Snapshot every 50 events

    def __init__(
        self,
        event_store: EventStore,
        snapshot_store: SnapshotStore,
    ):
        self._event_store = event_store
        self._snapshot_store = snapshot_store

    async def get(self, order_id: UUID) -> Optional[Order]:
        stream_id = f"order-{order_id}"

        # Try to load from snapshot
        snapshot = await self._snapshot_store.get(stream_id)

        if snapshot:
            # Load events after snapshot
            events = await self._event_store.read_stream(
                stream_id, from_version=snapshot.version
            )
            order = Order(**snapshot.state)
            order.version = snapshot.version
        else:
            # Load all events
            events = await self._event_store.read_stream(stream_id)
            order = Order(id=order_id)

        # Apply events
        for event in events:
            order._apply(event, is_new=False)

        return order if order.version > 0 else None

    async def save(self, order: Order) -> None:
        stream_id = f"order-{order.id}"
        events = order.collect_pending_events()

        if not events:
            return

        expected_version = order.version - len(events)

        await self._event_store.append(stream_id, events, expected_version)

        # Create snapshot if needed
        if order.version % self.SNAPSHOT_FREQUENCY == 0:
            await self._snapshot_store.save(Snapshot(
                stream_id=stream_id,
                version=order.version,
                state=self._serialize_order(order),
                created_at=datetime.utcnow(),
            ))
```

## Anti-patterns

### Avoid: Mutable Events

```python
# BAD - modifying event data
event = OrderCreated(order_id=order_id)
event.customer_id = new_customer_id  # Never do this!

# GOOD - events are immutable
@dataclass(frozen=True)
class OrderCreated(Event):
    order_id: UUID
    customer_id: UUID
```

### Avoid: Large Events

```python
# BAD - entire state in one event
@dataclass
class OrderUpdated(Event):
    entire_order_data: dict  # Contains everything

# GOOD - specific events for each change
@dataclass
class OrderItemAdded(Event):
    product_id: UUID
    quantity: int

@dataclass
class ShippingAddressChanged(Event):
    new_address: Address
```

## References

- [Event Sourcing by Martin Fowler](https://martinfowler.com/eaaDev/EventSourcing.html)
- [Greg Young - Event Sourcing](https://www.youtube.com/watch?v=8JKjvY4etTY)
- [EventStoreDB](https://www.eventstore.com/)
- [Marten Events](https://martendb.io/events/)
