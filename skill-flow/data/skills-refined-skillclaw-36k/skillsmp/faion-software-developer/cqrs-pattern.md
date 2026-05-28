---
id: cqrs-pattern
name: "CQRS Pattern"
domain: DEV
skill: faion-software-developer
category: "development"
---

# CQRS Pattern

## Overview

Command Query Responsibility Segregation (CQRS) separates read and write operations into different models. Commands change state, queries return data. This pattern enables optimization of each side independently and works well with event sourcing.

## When to Use

- High read/write ratio with different optimization needs
- Complex domain with separate read models
- Systems requiring audit trails
- Applications with eventual consistency requirements
- Microservices with event-driven architecture

## Key Principles

1. **Separate models** - Commands and queries use different models
2. **Commands change state** - Commands return void or ID, never data
3. **Queries return data** - Queries never modify state
4. **Eventual consistency** - Read models may lag behind writes
5. **Projections** - Build read models from events

## Best Practices

### CQRS Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                             │
└───────────────┬─────────────────────────┬───────────────────┘
                │                         │
       ┌────────▼────────┐       ┌────────▼────────┐
       │   Command Side   │       │   Query Side    │
       │                  │       │                 │
       │  ┌────────────┐  │       │  ┌───────────┐  │
       │  │  Commands  │  │       │  │  Queries  │  │
       │  └─────┬──────┘  │       │  └─────┬─────┘  │
       │        │         │       │        │        │
       │  ┌─────▼──────┐  │       │  ┌─────▼─────┐  │
       │  │  Handlers  │  │       │  │  Handlers │  │
       │  └─────┬──────┘  │       │  └─────┬─────┘  │
       │        │         │       │        │        │
       │  ┌─────▼──────┐  │       │  ┌─────▼─────┐  │
       │  │  Domain    │  │       │  │Read Model │  │
       │  │  Model     │  │       │  │           │  │
       │  └─────┬──────┘  │       │  └─────┬─────┘  │
       │        │         │       │        │        │
       │  ┌─────▼──────┐  │       │  ┌─────▼─────┐  │
       │  │Write Store │  │       │  │Read Store │  │
       │  │(PostgreSQL)│  │       │  │  (Redis)  │  │
       │  └────────────┘  │       │  └───────────┘  │
       └──────────────────┘       └─────────────────┘
                │                         ▲
                │       Events            │
                └─────────────────────────┘
```

### Command Implementation

```python
# application/commands/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic
from uuid import UUID

T = TypeVar('T')


@dataclass
class Command(ABC):
    """Base class for all commands."""
    pass


class CommandHandler(ABC, Generic[T]):
    """Base class for command handlers."""

    @abstractmethod
    async def handle(self, command: T) -> None:
        pass


# application/commands/orders/place_order.py
from dataclasses import dataclass
from typing import List
from uuid import UUID

from domain.orders.order import Order
from domain.orders.repository import OrderRepository
from domain.orders.events import OrderPlaced
from infrastructure.event_bus import EventBus


@dataclass
class PlaceOrderCommand(Command):
    """Command to place an order."""
    order_id: UUID
    customer_id: UUID
    items: List[dict]
    shipping_address: dict


class PlaceOrderHandler(CommandHandler[PlaceOrderCommand]):
    """Handler for PlaceOrderCommand."""

    def __init__(
        self,
        order_repository: OrderRepository,
        event_bus: EventBus,
    ):
        self._order_repository = order_repository
        self._event_bus = event_bus

    async def handle(self, command: PlaceOrderCommand) -> None:
        # Create order aggregate
        order = Order.create(
            id=command.order_id,
            customer_id=command.customer_id,
        )

        # Add items
        for item in command.items:
            order.add_item(
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"],
            )

        # Place order (domain logic)
        order.place(
            shipping_address=Address(**command.shipping_address)
        )

        # Persist
        await self._order_repository.save(order)

        # Publish events
        for event in order.collect_events():
            await self._event_bus.publish(event)


# application/commands/orders/cancel_order.py
@dataclass
class CancelOrderCommand(Command):
    """Command to cancel an order."""
    order_id: UUID
    reason: str


class CancelOrderHandler(CommandHandler[CancelOrderCommand]):
    """Handler for CancelOrderCommand."""

    def __init__(
        self,
        order_repository: OrderRepository,
        event_bus: EventBus,
    ):
        self._order_repository = order_repository
        self._event_bus = event_bus

    async def handle(self, command: CancelOrderCommand) -> None:
        order = await self._order_repository.find_by_id(command.order_id)

        if not order:
            raise OrderNotFoundError(command.order_id)

        order.cancel(command.reason)

        await self._order_repository.save(order)

        for event in order.collect_events():
            await self._event_bus.publish(event)
```

### Query Implementation

```python
# application/queries/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')
R = TypeVar('R')


@dataclass
class Query(ABC):
    """Base class for all queries."""
    pass


class QueryHandler(ABC, Generic[T, R]):
    """Base class for query handlers."""

    @abstractmethod
    async def handle(self, query: T) -> R:
        pass


# application/queries/orders/get_order.py
from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class GetOrderQuery(Query):
    """Query to get order details."""
    order_id: UUID


@dataclass
class OrderDto:
    """Read model for order details."""
    id: UUID
    customer_id: UUID
    status: str
    items: list
    total: float
    shipping_address: dict
    placed_at: Optional[str]
    created_at: str


class GetOrderHandler(QueryHandler[GetOrderQuery, OrderDto]):
    """Handler for GetOrderQuery."""

    def __init__(self, read_store: ReadStore):
        self._read_store = read_store

    async def handle(self, query: GetOrderQuery) -> OrderDto:
        # Read from optimized read store
        data = await self._read_store.get(f"order:{query.order_id}")

        if not data:
            raise OrderNotFoundError(query.order_id)

        return OrderDto(**data)


# application/queries/orders/list_orders.py
@dataclass
class ListOrdersQuery(Query):
    """Query to list orders for a customer."""
    customer_id: UUID
    status: Optional[str] = None
    page: int = 1
    page_size: int = 20


@dataclass
class OrderListDto:
    """Paginated list of orders."""
    items: list[OrderSummaryDto]
    total: int
    page: int
    page_size: int


class ListOrdersHandler(QueryHandler[ListOrdersQuery, OrderListDto]):
    """Handler for ListOrdersQuery."""

    def __init__(self, read_store: ReadStore):
        self._read_store = read_store

    async def handle(self, query: ListOrdersQuery) -> OrderListDto:
        # Query optimized read model
        orders = await self._read_store.query(
            index="orders_by_customer",
            customer_id=str(query.customer_id),
            status=query.status,
            offset=(query.page - 1) * query.page_size,
            limit=query.page_size,
        )

        total = await self._read_store.count(
            index="orders_by_customer",
            customer_id=str(query.customer_id),
            status=query.status,
        )

        return OrderListDto(
            items=[OrderSummaryDto(**o) for o in orders],
            total=total,
            page=query.page,
            page_size=query.page_size,
        )
```

### Read Model Projections

```python
# infrastructure/projections/order_projection.py
from domain.orders.events import OrderPlaced, OrderShipped, OrderCancelled


class OrderProjection:
    """Projects order events to read model."""

    def __init__(self, read_store: ReadStore):
        self._read_store = read_store

    async def handle(self, event) -> None:
        """Route event to appropriate handler."""
        handlers = {
            OrderPlaced: self._on_order_placed,
            OrderShipped: self._on_order_shipped,
            OrderCancelled: self._on_order_cancelled,
        }

        handler = handlers.get(type(event))
        if handler:
            await handler(event)

    async def _on_order_placed(self, event: OrderPlaced) -> None:
        """Project OrderPlaced event."""
        order_data = {
            "id": str(event.order_id),
            "customer_id": str(event.customer_id),
            "status": "placed",
            "items": event.items,
            "total": float(event.total),
            "shipping_address": event.shipping_address,
            "placed_at": event.occurred_at.isoformat(),
            "created_at": event.occurred_at.isoformat(),
        }

        # Store in read model
        await self._read_store.set(
            key=f"order:{event.order_id}",
            value=order_data,
        )

        # Update customer's order index
        await self._read_store.add_to_index(
            index="orders_by_customer",
            key=str(event.customer_id),
            value=str(event.order_id),
            score=event.occurred_at.timestamp(),
        )

    async def _on_order_shipped(self, event: OrderShipped) -> None:
        """Update order status when shipped."""
        await self._read_store.update(
            key=f"order:{event.order_id}",
            updates={
                "status": "shipped",
                "tracking_number": event.tracking_number,
                "shipped_at": event.occurred_at.isoformat(),
            },
        )

    async def _on_order_cancelled(self, event: OrderCancelled) -> None:
        """Update order status when cancelled."""
        await self._read_store.update(
            key=f"order:{event.order_id}",
            updates={
                "status": "cancelled",
                "cancellation_reason": event.reason,
                "cancelled_at": event.occurred_at.isoformat(),
            },
        )


# infrastructure/read_store/redis_read_store.py
import json
from typing import Optional, List
import redis.asyncio as redis


class RedisReadStore:
    """Redis implementation of read store."""

    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client

    async def get(self, key: str) -> Optional[dict]:
        data = await self._redis.get(key)
        return json.loads(data) if data else None

    async def set(self, key: str, value: dict, ttl: int = None) -> None:
        data = json.dumps(value)
        if ttl:
            await self._redis.setex(key, ttl, data)
        else:
            await self._redis.set(key, data)

    async def update(self, key: str, updates: dict) -> None:
        data = await self.get(key)
        if data:
            data.update(updates)
            await self.set(key, data)

    async def add_to_index(
        self,
        index: str,
        key: str,
        value: str,
        score: float,
    ) -> None:
        await self._redis.zadd(f"{index}:{key}", {value: score})

    async def query(
        self,
        index: str,
        key: str = None,
        offset: int = 0,
        limit: int = 20,
        **filters,
    ) -> List[dict]:
        # Get IDs from sorted set
        ids = await self._redis.zrevrange(
            f"{index}:{key}",
            offset,
            offset + limit - 1,
        )

        # Fetch full objects
        results = []
        for id_ in ids:
            data = await self.get(f"order:{id_}")
            if data:
                # Apply filters
                if all(data.get(k) == v for k, v in filters.items() if v):
                    results.append(data)

        return results
```

### Command/Query Bus

```python
# infrastructure/bus/mediator.py
from typing import Dict, Type, TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')


class Mediator:
    """Mediator for dispatching commands and queries."""

    def __init__(self):
        self._command_handlers: Dict[Type, CommandHandler] = {}
        self._query_handlers: Dict[Type, QueryHandler] = {}

    def register_command_handler(
        self,
        command_type: Type[Command],
        handler: CommandHandler,
    ) -> None:
        self._command_handlers[command_type] = handler

    def register_query_handler(
        self,
        query_type: Type[Query],
        handler: QueryHandler,
    ) -> None:
        self._query_handlers[query_type] = handler

    async def send(self, command: Command) -> None:
        """Dispatch command to handler."""
        handler = self._command_handlers.get(type(command))
        if not handler:
            raise HandlerNotFoundError(f"No handler for {type(command)}")
        await handler.handle(command)

    async def query(self, query: Query) -> T:
        """Dispatch query to handler."""
        handler = self._query_handlers.get(type(query))
        if not handler:
            raise HandlerNotFoundError(f"No handler for {type(query)}")
        return await handler.handle(query)


# API usage
@router.post("/orders")
async def place_order(
    request: PlaceOrderRequest,
    mediator: Mediator = Depends(get_mediator),
):
    command = PlaceOrderCommand(
        order_id=uuid4(),
        customer_id=request.customer_id,
        items=request.items,
        shipping_address=request.shipping_address,
    )

    await mediator.send(command)

    return {"order_id": str(command.order_id)}


@router.get("/orders/{order_id}")
async def get_order(
    order_id: UUID,
    mediator: Mediator = Depends(get_mediator),
):
    query = GetOrderQuery(order_id=order_id)
    order = await mediator.query(query)
    return order
```

## Anti-patterns

### Avoid: Commands Returning Data

```python
# BAD - command returns data
class CreateOrderHandler:
    async def handle(self, command) -> OrderDto:  # Wrong!
        order = Order.create(...)
        await self._repo.save(order)
        return OrderDto.from_entity(order)

# GOOD - command returns only ID or void
class CreateOrderHandler:
    async def handle(self, command) -> UUID:
        order = Order.create(id=command.order_id, ...)
        await self._repo.save(order)
        return order.id  # Or return None
```

### Avoid: Queries Modifying State

```python
# BAD - query has side effects
class GetOrderHandler:
    async def handle(self, query):
        order = await self._read_store.get(query.order_id)
        order["view_count"] += 1  # Side effect!
        await self._read_store.set(order)
        return order

# GOOD - queries are pure
class GetOrderHandler:
    async def handle(self, query):
        return await self._read_store.get(query.order_id)
```

## References

- [CQRS by Martin Fowler](https://martinfowler.com/bliki/CQRS.html)
- [Microsoft CQRS Pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/cqrs)
- [Greg Young on CQRS](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
