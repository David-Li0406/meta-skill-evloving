---
id: microservices-design
name: "Microservices Design"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Microservices Design

## Overview

Microservices architecture structures an application as a collection of loosely coupled, independently deployable services. Each service owns its data and business logic, communicating through well-defined APIs.

## When to Use

- Large applications requiring independent scaling
- Multiple teams working on different features
- Systems needing technology diversity
- Applications requiring high availability
- Organizations practicing continuous deployment

## Key Principles

1. **Single responsibility** - Each service does one thing well
2. **Loose coupling** - Services are independent
3. **High cohesion** - Related functionality grouped together
4. **Decentralized data** - Each service owns its data
5. **Design for failure** - Assume services will fail

## Best Practices

### Service Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        API Gateway                               │
│  (Authentication, Rate Limiting, Routing)                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  User Service │   │ Order Service │   │Product Service│
│               │   │               │   │               │
│  ┌─────────┐  │   │  ┌─────────┐  │   │  ┌─────────┐  │
│  │   API   │  │   │  │   API   │  │   │  │   API   │  │
│  └────┬────┘  │   │  └────┬────┘  │   │  └────┬────┘  │
│       │       │   │       │       │   │       │       │
│  ┌────▼────┐  │   │  ┌────▼────┐  │   │  ┌────▼────┐  │
│  │ Domain  │  │   │  │ Domain  │  │   │  │ Domain  │  │
│  └────┬────┘  │   │  └────┬────┘  │   │  └────┬────┘  │
│       │       │   │       │       │   │       │       │
│  ┌────▼────┐  │   │  ┌────▼────┐  │   │  ┌────▼────┐  │
│  │PostgreSQL│ │   │  │ MongoDB │  │   │  │  Redis  │  │
│  └─────────┘  │   │  └─────────┘  │   │  └─────────┘  │
└───────────────┘   └───────────────┘   └───────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             ▼
                    ┌───────────────┐
                    │  Message Bus  │
                    │   (RabbitMQ)  │
                    └───────────────┘
```

### Service Structure

```
services/
├── user-service/
│   ├── src/
│   │   ├── api/
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── domain/
│   │   │   ├── entities.py
│   │   │   ├── services.py
│   │   │   └── events.py
│   │   ├── infrastructure/
│   │   │   ├── database.py
│   │   │   └── message_bus.py
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── order-service/
│   └── ... (similar structure)
│
├── product-service/
│   └── ...
│
└── shared/
    ├── messaging/
    └── observability/
```

### Service Implementation

```python
# user-service/src/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.routes import router
from infrastructure.database import init_db, close_db
from infrastructure.message_bus import init_message_bus, close_message_bus
from infrastructure.health import health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await init_message_bus()
    yield
    # Shutdown
    await close_message_bus()
    await close_db()


app = FastAPI(
    title="User Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health_router, tags=["health"])
app.include_router(router, prefix="/api/v1", tags=["users"])


# user-service/src/api/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from domain.services import UserService
from api.schemas import CreateUserRequest, UserResponse
from infrastructure.dependencies import get_user_service

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    service: UserService = Depends(get_user_service),
):
    try:
        user = await service.create_user(
            email=request.email,
            name=request.name,
        )
        return UserResponse.from_entity(user)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
):
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserResponse.from_entity(user)
```

### Inter-Service Communication

```python
# Synchronous - HTTP/REST
from httpx import AsyncClient


class OrderServiceClient:
    """Client for Order Service."""

    def __init__(self, base_url: str):
        self._base_url = base_url
        self._client = AsyncClient(base_url=base_url, timeout=10.0)

    async def get_orders_for_user(self, user_id: UUID) -> list:
        response = await self._client.get(
            f"/api/v1/orders",
            params={"user_id": str(user_id)},
        )
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self._client.aclose()


# Asynchronous - Message Bus
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
import json

import aio_pika


@dataclass
class UserCreatedEvent:
    user_id: UUID
    email: str
    name: str
    occurred_at: datetime


class MessagePublisher:
    """Publish events to message bus."""

    def __init__(self, channel: aio_pika.Channel):
        self._channel = channel

    async def publish(self, event: UserCreatedEvent) -> None:
        exchange = await self._channel.get_exchange("events")

        message = aio_pika.Message(
            body=json.dumps({
                "type": "user.created",
                "data": {
                    "user_id": str(event.user_id),
                    "email": event.email,
                    "name": event.name,
                },
                "occurred_at": event.occurred_at.isoformat(),
            }).encode(),
            content_type="application/json",
        )

        await exchange.publish(
            message,
            routing_key="user.created",
        )


class MessageConsumer:
    """Consume events from message bus."""

    def __init__(self, channel: aio_pika.Channel):
        self._channel = channel
        self._handlers = {}

    def register(self, event_type: str, handler):
        self._handlers[event_type] = handler

    async def start(self, queue_name: str) -> None:
        queue = await self._channel.declare_queue(queue_name, durable=True)

        async with queue.iterator() as messages:
            async for message in messages:
                async with message.process():
                    data = json.loads(message.body)
                    handler = self._handlers.get(data["type"])
                    if handler:
                        await handler(data["data"])
```

### Service Discovery

```python
# Using Consul for service discovery
from consul.aio import Consul


class ServiceRegistry:
    """Service registry using Consul."""

    def __init__(self, consul_host: str = "localhost", consul_port: int = 8500):
        self._consul = Consul(host=consul_host, port=consul_port)

    async def register(
        self,
        service_name: str,
        service_id: str,
        address: str,
        port: int,
        health_check_url: str,
    ) -> None:
        """Register service with health check."""
        await self._consul.agent.service.register(
            name=service_name,
            service_id=service_id,
            address=address,
            port=port,
            check={
                "http": health_check_url,
                "interval": "10s",
                "timeout": "5s",
            },
        )

    async def deregister(self, service_id: str) -> None:
        await self._consul.agent.service.deregister(service_id)

    async def get_service(self, service_name: str) -> list:
        """Get healthy instances of a service."""
        _, services = await self._consul.health.service(
            service_name, passing=True
        )
        return [
            {
                "address": s["Service"]["Address"],
                "port": s["Service"]["Port"],
            }
            for s in services
        ]


# Load balancing
import random


class LoadBalancer:
    """Simple round-robin load balancer."""

    def __init__(self, registry: ServiceRegistry):
        self._registry = registry
        self._index = {}

    async def get_instance(self, service_name: str) -> dict:
        instances = await self._registry.get_service(service_name)
        if not instances:
            raise ServiceUnavailableError(service_name)

        # Round-robin selection
        idx = self._index.get(service_name, 0)
        instance = instances[idx % len(instances)]
        self._index[service_name] = idx + 1

        return instance
```

### Circuit Breaker

```python
# Circuit breaker pattern for resilience
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Callable, TypeVar
import asyncio

T = TypeVar('T')


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    recovery_timeout: timedelta = timedelta(seconds=30)
    half_open_max_calls: int = 3


class CircuitBreaker:
    """Circuit breaker for handling service failures."""

    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self._config = config or CircuitBreakerConfig()
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None
        self._half_open_calls = 0

    @property
    def state(self) -> CircuitState:
        if self._state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._state = CircuitState.HALF_OPEN
                self._half_open_calls = 0
        return self._state

    async def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute function through circuit breaker."""
        if self.state == CircuitState.OPEN:
            raise CircuitOpenError(self.name)

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self) -> None:
        if self._state == CircuitState.HALF_OPEN:
            self._half_open_calls += 1
            if self._half_open_calls >= self._config.half_open_max_calls:
                self._state = CircuitState.CLOSED
                self._failure_count = 0
        else:
            self._failure_count = 0

    def _on_failure(self) -> None:
        self._failure_count += 1
        self._last_failure_time = datetime.utcnow()

        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.OPEN
        elif self._failure_count >= self._config.failure_threshold:
            self._state = CircuitState.OPEN

    def _should_attempt_reset(self) -> bool:
        if self._last_failure_time is None:
            return True
        return datetime.utcnow() - self._last_failure_time > self._config.recovery_timeout


# Usage with HTTP client
class ResilientServiceClient:
    def __init__(self, base_url: str):
        self._client = AsyncClient(base_url=base_url)
        self._circuit_breaker = CircuitBreaker("order-service")

    async def get_orders(self, user_id: UUID) -> list:
        return await self._circuit_breaker.call(
            self._fetch_orders, user_id
        )

    async def _fetch_orders(self, user_id: UUID) -> list:
        response = await self._client.get(f"/orders?user_id={user_id}")
        response.raise_for_status()
        return response.json()
```

### Saga Pattern for Distributed Transactions

```python
# Choreography-based saga
from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class SagaState(Enum):
    STARTED = "started"
    PROCESSING = "processing"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"


@dataclass
class CreateOrderSaga:
    """Saga for creating an order across services."""

    order_id: UUID
    user_id: UUID
    items: list
    state: SagaState = SagaState.STARTED


class OrderSagaOrchestrator:
    """Orchestrates the order creation saga."""

    def __init__(
        self,
        order_service: OrderServiceClient,
        inventory_service: InventoryServiceClient,
        payment_service: PaymentServiceClient,
        message_bus: MessagePublisher,
    ):
        self._order_service = order_service
        self._inventory_service = inventory_service
        self._payment_service = payment_service
        self._message_bus = message_bus

    async def execute(self, saga: CreateOrderSaga) -> None:
        """Execute saga steps with compensation on failure."""
        steps_completed = []

        try:
            # Step 1: Reserve inventory
            await self._inventory_service.reserve(saga.order_id, saga.items)
            steps_completed.append("inventory")

            # Step 2: Process payment
            await self._payment_service.charge(saga.user_id, saga.total)
            steps_completed.append("payment")

            # Step 3: Create order
            await self._order_service.create(saga.order_id, saga.items)
            steps_completed.append("order")

            saga.state = SagaState.COMPLETED

        except Exception as e:
            # Compensate completed steps
            saga.state = SagaState.COMPENSATING
            await self._compensate(saga, steps_completed)
            saga.state = SagaState.FAILED
            raise

    async def _compensate(
        self,
        saga: CreateOrderSaga,
        steps: list,
    ) -> None:
        """Compensate completed steps in reverse order."""
        for step in reversed(steps):
            try:
                if step == "order":
                    await self._order_service.cancel(saga.order_id)
                elif step == "payment":
                    await self._payment_service.refund(saga.user_id)
                elif step == "inventory":
                    await self._inventory_service.release(saga.order_id)
            except Exception:
                # Log compensation failure
                pass
```

## Anti-patterns

### Avoid: Distributed Monolith

```python
# BAD - services tightly coupled via synchronous calls
class OrderService:
    def create_order(self, data):
        user = user_service.get_user(data.user_id)  # Sync call
        product = product_service.get_product(data.product_id)  # Sync call
        inventory = inventory_service.check(data.product_id)  # Sync call
        # All services must be up

# GOOD - async events, local data caching
class OrderService:
    def create_order(self, data):
        # Use cached/local data
        user_valid = await self.user_cache.exists(data.user_id)
        product = await self.product_cache.get(data.product_id)

        order = Order.create(data)
        await self.repository.save(order)

        # Publish event for other services
        await self.event_bus.publish(OrderCreated(order))
```

### Avoid: Shared Database

```python
# BAD - multiple services access same database
# user-service and order-service both query 'users' table

# GOOD - each service owns its data
# user-service owns 'users' table
# order-service has 'customer_info' with denormalized user data
```

## References

- [Building Microservices by Sam Newman](https://samnewman.io/books/building_microservices_2nd_edition/)
- [Microservices Patterns by Chris Richardson](https://microservices.io/patterns/)
- [Martin Fowler - Microservices](https://martinfowler.com/articles/microservices.html)
- [12-Factor App](https://12factor.net/)
