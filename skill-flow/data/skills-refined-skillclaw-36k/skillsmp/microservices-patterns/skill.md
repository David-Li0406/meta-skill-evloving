---
name: microservices-patterns
description: Implement microservices patterns including service decomposition, communication patterns, saga patterns, circuit breakers, and API gateways. Use when designing distributed systems or decomposing monoliths into microservices.
---

# Microservices Patterns

Master proven microservices patterns to build scalable, resilient, and maintainable distributed systems that can evolve independently.

## When to Use This Skill

- Decomposing monolithic applications into microservices
- Designing inter-service communication strategies
- Implementing distributed transactions and data consistency
- Building resilient systems with fault tolerance
- Creating API gateways and service mesh architectures
- Establishing service boundaries and ownership
- Managing distributed data and eventual consistency

## Core Concepts

### 1. Service Decomposition Strategies

**By Business Capability:**
- Group services around business functions (orders, payments, inventory)
- Each service owns its data and business logic
- Aligned with organizational structure (Conway's Law)

**By Subdomain (DDD):**
- Identify bounded contexts
- Core domain vs. supporting subdomains
- Context mapping for service relationships

**By Transaction Boundaries:**
- Services that change together should be together
- Minimize distributed transactions
- Aggregate boundaries become service boundaries

### 2. Communication Patterns

**Synchronous (Request-Response):**
- REST APIs over HTTP
- gRPC for high-performance RPC
- GraphQL for flexible queries
- Use for queries and immediate responses

**Asynchronous (Event-Driven):**
- Message queues (RabbitMQ, AWS SQS)
- Event streaming (Kafka, AWS Kinesis)
- Pub/Sub patterns
- Use for eventual consistency and decoupling

### 3. Data Management Patterns

**Database per Service:**
- Each service owns its database
- No shared databases between services
- Different storage technologies per service needs

**Saga Pattern:**
- Distributed transactions across services
- Compensating transactions for rollback
- Orchestration vs. Choreography

**CQRS (Command Query Responsibility Segregation):**
- Separate read and write models
- Optimized for different access patterns
- Often paired with Event Sourcing

## Service Decomposition Pattern

### Pattern 1: By Business Capability

```
# Service structure for e-commerce platform

services/
├── user-service/           # User management
│   ├── domain/
│   │   ├── user.py
│   │   └── profile.py
│   └── api/
│       └── user_api.py
├── order-service/          # Order processing
│   ├── domain/
│   │   ├── order.py
│   │   └── order_item.py
│   └── api/
│       └── order_api.py
├── payment-service/        # Payment processing
│   ├── domain/
│   │   ├── payment.py
│   │   └── transaction.py
│   └── api/
│       └── payment_api.py
├── inventory-service/      # Inventory management
│   ├── domain/
│   │   ├── product.py
│   │   └── stock.py
│   └── api/
│       └── inventory_api.py
└── notification-service/   # Notifications
    ├── domain/
    │   └── notification.py
    └── api/
        └── notification_api.py
```

### Pattern 2: Service Implementation

```python
# order-service/domain/order.py
from dataclasses import dataclass
from typing import List
from enum import Enum
from datetime import datetime

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

@dataclass
class OrderItem:
    product_id: str
    quantity: int
    price: float

@dataclass
class Order:
    """Order aggregate - owns order lifecycle."""
    id: str
    user_id: str
    items: List[OrderItem]
    status: OrderStatus
    total: float
    created_at: datetime
    updated_at: datetime

    def calculate_total(self) -> float:
        """Business logic within service."""
        return sum(item.quantity * item.price for item in self.items)

    def can_cancel(self) -> bool:
        """Business rule: can only cancel pending/confirmed orders."""
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]

# order-service/api/order_api.py
from fastapi import FastAPI, HTTPException, Depends
from typing import List

app = FastAPI()

@app.post("/orders")
async def create_order(order_data: dict):
    """Create new order - may call other services."""
    # 1. Validate inventory (call inventory-service)
    inventory_available = await check_inventory(order_data["items"])
    if not inventory_available:
        raise HTTPException(400, "Insufficient inventory")

    # 2. Create order
    order = await order_repository.create(order_data)

    # 3. Publish event (asynchronous communication)
    await event_bus.publish("order.created", order)

    return {"order_id": order.id}

@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    """Query order by ID."""
    order = await order_repository.find_by_id(order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    return order
```

## Communication Patterns

### Pattern 1: Synchronous REST Communication

```python
# order-service calling inventory-service
import httpx
from typing import List, Optional

class InventoryClient:
    """Client for synchronous inventory service calls."""

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=timeout)

    async def check_availability(
        self,
        items: List[dict]
    ) -> dict:
        """Check if products are available."""
        try:
            response = await self.client.post(
                f"{self.base_url}/inventory/check",
                json={"items": items}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            # Handle failures gracefully
            raise ServiceUnavailableError(f"Inventory service error: {e}")

    async def reserve_inventory(
        self,
        order_id: str,
        items: List[dict]
    ) -> bool:
        """Reserve inventory for order."""
        response = await self.client.post(
            f"{self.base_url}/inventory/reserve",
            json={"order_id": order_id, "items": items}
        )
        return response.status_code == 200
```

### Pattern 2: Asynchronous Event-Driven Communication

```python
# Event publishing and consuming with Kafka
from kafka import KafkaProducer, KafkaConsumer
import json
from typing import Callable, Dict
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class DomainEvent:
    """Base domain event."""
    event_id: str
    event_type: str
    timestamp: datetime
    payload: dict

class EventBus:
    """Event bus for asynchronous communication."""

    def __init__(self, bootstrap_servers: List[str]):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    async def publish(self, event_type: str, payload: dict):
        """Publish event to Kafka topic."""
        event = DomainEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            timestamp=datetime.now(),
            payload=payload
        )

        topic = event_type.replace(".", "_")  # order.created -> order_created
        self.producer.send(topic, value=asdict(event))
        self.producer.flush()

class EventConsumer:
    """Event consumer for service-to-service communication."""

    def __init__(self, bootstrap_servers: List[str], group_id: str):
        self.handlers: Dict[str, Callable] = {}
        self.consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    def subscribe(self, event_type: str, handler: Callable):
        """Register event handler."""
        self.handlers[event_type] = handler
        topic = event_type.replace(".", "_")
        self.consumer.subscribe([topic])

    async def start(self):
        """Start consuming events."""
        for message in self.consumer:
            event = message.value
            handler = self.handlers.get(event["event_type"])
            if handler:
                await handler(event["payload"])

# Usage in notification-service
event_consumer = EventConsumer(
    bootstrap_servers=["kafka:9092"],
    group_id="notification-service"
)

async def handle_order_created(payload: dict):
    """Handle order.created event."""
    order_id = payload["order_id"]
    user_id = payload["user_id"]

    # Send notification to user
    await send_notification(
        user_id=user_id,
        message=f"Order {order_id} created successfully"
    )

event_consumer.subscribe("order.created", handle_order_created)
await event_consumer.start()
```

## Saga Pattern (Distributed Transactions)

### Pattern 1: Orchestration-Based Saga

```python
from enum import Enum
from typing import List, Callable, Optional
from dataclasses import dataclass

class SagaStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    FAILED = "failed"

@dataclass
class SagaStep:
    """Single step in saga."""
    name: str
    action: Callable
    compensation: Callable

class OrderFulfillmentSaga:
    """Orchestrated saga for order fulfillment."""

    def __init__(
        self,
        order_service,
        inventory_service,
        payment_service,
        shipping_service
    ):
        self.order_service = order_service
        self.inventory_service = inventory_service
        self.payment_service = payment_service
        self.shipping_service = shipping_service

        # Define saga steps
        self.steps: List[SagaStep] = [
            SagaStep(
                name="create_order",
                action=self.create_order,
                compensation=self.cancel_order
            ),
            SagaStep(
                name="reserve_inventory",
                action=self.reserve_inventory,
                compensation=self.release_inventory
            ),
            SagaStep(
                name="process_payment",
                action=self.process_payment,
                compensation=self.refund_payment
            ),
            SagaStep(
                name="arrange_shipping",
                action=self.arrange_shipping,
                compensation=self.cancel_shipping
            ),
        ]

    async def execute(self, order_data: dict) -> dict:
        """Execute saga with automatic compensation on failure."""
        completed_steps = []
        context = {"order_data": order_data}

        try:
            # Execute forward steps
            for step in self.steps:
                print(f"Executing step: {step.name}")
                result = await step.action(context)
                context[step.name] = result
                completed_steps.append(step)

            return {"status": "success", "order_id": context["create_order"]["order_id"]}

        except Exception as e:
            print(f"Saga failed at step: {step.name}, error: {e}")

            # Execute compensation in reverse order
            for step in reversed(completed_steps):
                try:
                    print(f"Compensating step: {step.name}")
                    await step.compensation(context)
                except Exception as comp_error:
                    print(f"Compensation failed: {step.name}, error: {comp_error}")
                    # Log and alert - manual intervention may be needed

            return {"status": "failed", "error": str(e)}

    # Forward actions
    async def create_order(self, context: dict) -> dict:
        """Step 1: Create order."""
        order = await self.order_service.create(context["order_data"])
        return {"order_id": order["id"]}

    async def reserve_inventory(self, context: dict) -> dict:
        """Step 2: Reserve inventory."""
        order_id = context["create_order"]["order_id"]
        items = context["order_data"]["items"]
        result = await self.inventory_service.reserve(order_id, items)
        return {"reservation_id": result["reservation_id"]}

    async def process_payment(self, context: dict) -> dict:
        """Step 3: Process payment."""
        order_id = context["create_order"]["order_id"]
        amount = context["order_data"]["total"]
        result = await self.payment_service.charge(order_id, amount)
        return {"transaction_id": result["transaction_id"]}

    async def arrange_shipping(self, context: dict) -> dict:
        """Step 4: Arrange shipping."""
        order_id = context["create_order"]["order_id"]
        result = await self.shipping_service.schedule(order_id)
        return {"shipment_id": result["shipment_id"]}

    # Compensating actions
    async def cancel_order(self, context: dict):
        """Compensate: Cancel order."""
        order_id = context["create_order"]["order_id"]
        await self.order_service.cancel(order_id)

    async def release_inventory(self, context: dict):
        """Compensate: Release inventory reservation."""
        reservation_id = context["reserve_inventory"]["reservation_id"]
        await self.inventory_service.release(reservation_id)

    async def refund_payment(self, context: dict):
        """Compensate: Refund payment."""
        transaction_id = context["process_payment"]["transaction_id"]
        await self.payment_service.refund(transaction_id)

    async def cancel_shipping(self, context: dict):
        """Compensate: Cancel shipment."""
        shipment_id = context["arrange_shipping"]["shipment_id"]
        await self.shipping_service.cancel(shipment_id)

# Usage
saga = OrderFulfillmentSaga(
    order_service=order_service,
    inventory_service=inventory_service,
    payment_service=payment_service,
    shipping_service=shipping_service
)

result = await saga.execute({
    "user_id": "user-123",
    "items": [{"product_id": "prod-1", "quantity": 2}],
    "total": 99.99
})
```

### Pattern 2: Choreography-Based Saga

```python
# Event-driven saga without central orchestrator

# In order-service
@event_consumer.subscribe("payment.completed")
async def on_payment_completed(payload: dict):
    """React to payment completion."""
    order_id = payload["order_id"]

    # Update order status
    await order_repository.update_status(order_id, OrderStatus.PAID)

    # Publish next event
    await event_bus.publish("order.paid", {"order_id": order_id})

@event_consumer.subscribe("payment.failed")
async def on_payment_failed(payload: dict):
    """React to payment failure - compensate."""
    order_id = payload["order_id"]
    reservation_id = payload["reservation_id"]

    # Cancel order
    await order_repository.update_status(order_id, OrderStatus.CANCELLED)

    # Publish compensation event
    await event_bus.publish("inventory.release", {"reservation_id": reservation_id})

# In inventory-service
@event_consumer.subscribe("order.created")
async def on_order_created(payload: dict):
    """Reserve inventory when order created."""
    order_id = payload["order_id"]
    items = payload["items"]

    try:
        reservation = await inventory_repository.reserve(order_id, items)
        await event_bus.publish("inventory.reserved", {
            "order_id": order_id,
            "reservation_id": reservation.id
        })
    except InsufficientInventoryError:
        await event_bus.publish("inventory.reservation_failed", {
            "order_id": order_id,
            "reason": "insufficient_inventory"
        })

# In payment-service
@event_consumer.subscribe("inventory.reserved")
async def on_inventory_reserved(payload: dict):
    """Process payment when inventory reserved."""
    order_id = payload["order_id"]
    reservation_id = payload["reservation_id"]

    try:
        transaction = await payment_gateway.charge(order_id)
        await event_bus.publish("payment.completed", {
            "order_id": order_id,
            "transaction_id": transaction.id
        })
    except PaymentError as e:
        await event_bus.publish("payment.failed", {
            "order_id": order_id,
            "reservation_id": reservation_id,
            "reason": str(e)
        })
```

## Resilience Patterns

### Pattern 1: Circuit Breaker

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Optional
import asyncio

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing - reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """Circuit breaker pattern for resilient service calls."""

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout_seconds: int = 60,
        half_open_max_calls: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.half_open_max_calls = half_open_max_calls

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.half_open_calls = 0

    async def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            # Check if timeout expired
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
            else:
                raise CircuitBreakerOpenError("Circuit breaker is OPEN")

        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls >= self.half_open_max_calls:
                raise CircuitBreakerOpenError("Circuit breaker in HALF_OPEN, max calls reached")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _on_success(self):
        """Handle successful call."""
        if self.state == CircuitState.HALF_OPEN:
            self.half_open_calls += 1
            if self.half_open_calls >= self.half_open_max_calls:
                # Service recovered
                self.state = CircuitState.CLOSED
                self.failure_count = 0
        else:
            self.failure_count = 0

    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _should_attempt_reset(self) -> bool:
        """Check if timeout expired to try half-open."""
        if not self.last_failure_time:
            return False

        elapsed = datetime.now() - self.last_failure_time
        return elapsed.total_seconds() >= self.timeout_seconds

# Usage
payment_circuit = CircuitBreaker(
    failure_threshold=5,
    timeout_seconds=60
)

async def call_payment_service(order_id: str):
    """Call payment service with circuit breaker."""
    try:
        return await payment_circuit.call(
            payment_service.charge,
            order_id=order_id
        )
    except CircuitBreakerOpenError:
        # Fallback: queue for later processing
        await payment_queue.enqueue(order_id)
        return {"status": "queued", "message": "Payment service unavailable"}
```

### Pattern 2: Retry with Exponential Backoff

```python
import asyncio
from typing import TypeVar, Callable
import random

T = TypeVar('T')

async def retry_with_backoff(
    func: Callable[..., T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True
) -> T:
    """Retry function with exponential backoff."""

    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e

            # Calculate delay with exponential backoff
            delay = min(base_delay * (exponential_base ** attempt), max_delay)

            # Add jitter to prevent thundering herd
            if jitter:
                delay = delay * (0.5 + random.random())

            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay:.2f}s...")
            await asyncio.sleep(delay)

# Usage
async def call_external_api():
    """Call external API with retry."""
    return await retry_with_backoff(
        lambda: httpx.get("https://api.example.com/data"),
        max_retries=3,
        base_delay=1.0
    )
```

### Pattern 3: Bulkhead Pattern

```python
import asyncio
from typing import Callable, TypeVar

T = TypeVar('T')

class Bulkhead:
    """Bulkhead pattern to isolate resources."""

    def __init__(self, max_concurrent_calls: int):
        self.semaphore = asyncio.Semaphore(max_concurrent_calls)

    async def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute function with concurrency limit."""
        async with self.semaphore:
            return await func(*args, **kwargs)

# Create separate bulkheads for different services
payment_bulkhead = Bulkhead(max_concurrent_calls=10)
inventory_bulkhead = Bulkhead(max_concurrent_calls=20)
notification_bulkhead = Bulkhead(max_concurrent_calls=50)

# Usage
async def process_order(order_id: str):
    """Process order with bulkhead isolation."""
    # Each service call is isolated
    payment_result = await payment_bulkhead.call(
        payment_service.charge,
        order_id
    )

    inventory_result = await inventory_bulkhead.call(
        inventory_service.reserve,
        order_id
    )

    # Notification failures won't affect critical services
    await notification_bulkhead.call(
        notification_service.send,
        order_id
    )
```

## API Gateway Pattern

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import httpx
from typing import Optional

app = FastAPI(title="API Gateway")

# Service registry
SERVICES = {
    "users": "http://user-service:8001",
    "orders": "http://order-service:8002",
    "payments": "http://payment-service:8003",
    "inventory": "http://inventory-service:8004"
}

class APIGateway:
    """API Gateway with routing, auth, and rate limiting."""

    def __init__(self):
        self.client = httpx.AsyncClient()
        self.circuit_breakers = {
            service: CircuitBreaker() for service in SERVICES
        }

    async def route_request(
        self,
        service: str,
        path: str,
        method: str,
        headers: dict,
        body: Optional[dict] = None
    ) -> dict:
        """Route request to appropriate service."""

        if service not in SERVICES:
            raise HTTPException(404, f"Service {service} not found")

        # Get service URL
        base_url = SERVICES[service]
        url = f"{base_url}{path}"

        # Add correlation ID for tracing
        headers["X-Correlation-ID"] = headers.get("X-Correlation-ID", str(uuid.uuid4()))

        # Call service with circuit breaker
        circuit = self.circuit_breakers[service]

        try:
            response = await circuit.call(
                self._make_request,
                method=method,
                url=url,
                headers=headers,
                json=body
            )
            return response
        except CircuitBreakerOpenError:
            raise HTTPException(503, f"Service {service} unavailable")

    async def _make_request(
        self,
        method: str,
        url: str,
        headers: dict,
        json: Optional[dict]
    ) -> dict:
        """Make HTTP request to service."""
        response = await self.client.request(
            method=method,
            url=url,
            headers=headers,
            json=json,
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()

gateway = APIGateway()

# Gateway endpoints
@app.api_route("/api/{service}/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def gateway_route(
    service: str,
    path: str,
    request: Request
):
    """Gateway entry point - route to services."""

    # Authentication (simplified)
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(401, "Authentication required")

    # Rate limiting (simplified)
    # await rate_limiter.check(request.client.host)

    # Get request body
    body = await request.json() if request.method in ["POST", "PUT", "PATCH"] else None

    # Route to service
    result = await gateway.route_request(
        service=service,
        path=f"/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body
    )

    return result
```

## Best Practices

1. **Service Boundaries**: Design services around business capabilities, not technical layers
2. **Data Ownership**: Each service owns its data; no shared databases
3. **Communication**: Use asynchronous messaging for loose coupling
4. **Resilience**: Implement circuit breakers, retries, and bulkheads
5. **Observability**: Distributed tracing, centralized logging, metrics
6. **API Versioning**: Version APIs to allow independent evolution
7. **Idempotency**: Design operations to be safely retryable
8. **Backwards Compatibility**: Never break existing clients

## Common Pitfalls

- **Distributed Monolith**: Too many dependencies between services
- **Chatty Services**: Excessive inter-service communication
- **Shared Database**: Services sharing same database violates autonomy
- **Synchronous Chains**: Long chains of synchronous calls reduce resilience
- **Missing Compensation**: Distributed transactions without rollback strategy
- **Poor Service Boundaries**: Services too fine-grained or too coarse
- **Neglecting Observability**: Can't debug what you can't see
