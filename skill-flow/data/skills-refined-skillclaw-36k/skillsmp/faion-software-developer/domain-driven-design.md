---
id: domain-driven-design
name: "Domain-Driven Design"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Domain-Driven Design

## Overview

Domain-Driven Design (DDD) is an approach to software development that focuses on the core domain and domain logic. It emphasizes collaboration between technical and domain experts to create a shared understanding through a ubiquitous language.

## When to Use

- Complex business domains
- Large-scale enterprise applications
- Projects with evolving requirements
- Teams working closely with domain experts
- Systems with multiple bounded contexts

## Key Principles

1. **Ubiquitous language** - Shared vocabulary between developers and domain experts
2. **Bounded contexts** - Explicit boundaries for domain models
3. **Entities** - Objects with identity that persists over time
4. **Value objects** - Immutable objects defined by their attributes
5. **Aggregates** - Clusters of entities with a root entity

## Best Practices

### Strategic Design Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                    Context Map                               │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Sales Context │  Shipping       │   Billing Context       │
│                 │  Context        │                         │
│  - Order        │  - Shipment     │  - Invoice              │
│  - Customer     │  - Delivery     │  - Payment              │
│  - Product      │  - Address      │  - Account              │
└────────┬────────┴────────┬────────┴────────────┬────────────┘
         │                 │                      │
         │   Shared Kernel │                      │
         └────────────────────────────────────────┘

Relationships:
- Customer/Supplier: One context provides, another consumes
- Shared Kernel: Shared subset of the domain model
- Anti-Corruption Layer: Translation between contexts
- Conformist: Downstream adopts upstream model
```

### Bounded Context Implementation

```python
# Order context - order/domain/entities/order.py
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List
from uuid import UUID, uuid4

from .value_objects import Money, Address
from .events import OrderPlaced, OrderShipped


class OrderStatus(Enum):
    DRAFT = "draft"
    PLACED = "placed"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class OrderLine:
    """Value object representing an order line item."""
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: Money

    @property
    def total(self) -> Money:
        return Money(self.unit_price.amount * self.quantity, self.unit_price.currency)


@dataclass
class Order:
    """Order aggregate root."""

    id: UUID = field(default_factory=uuid4)
    customer_id: UUID = field(default=None)
    status: OrderStatus = OrderStatus.DRAFT
    lines: List[OrderLine] = field(default_factory=list)
    shipping_address: Address = None
    placed_at: datetime = None
    _events: List = field(default_factory=list, repr=False)

    def add_line(self, product_id: UUID, name: str, quantity: int, price: Money) -> None:
        """Add a line item to the order."""
        if self.status != OrderStatus.DRAFT:
            raise DomainError("Cannot modify a placed order")

        if quantity <= 0:
            raise DomainError("Quantity must be positive")

        # Check if product already in order
        for line in self.lines:
            if line.product_id == product_id:
                raise DomainError("Product already in order")

        self.lines.append(OrderLine(product_id, name, quantity, price))

    def remove_line(self, product_id: UUID) -> None:
        """Remove a line item from the order."""
        if self.status != OrderStatus.DRAFT:
            raise DomainError("Cannot modify a placed order")

        self.lines = [l for l in self.lines if l.product_id != product_id]

    def place(self, shipping_address: Address) -> None:
        """Place the order."""
        if self.status != OrderStatus.DRAFT:
            raise DomainError("Order already placed")

        if not self.lines:
            raise DomainError("Cannot place empty order")

        self.shipping_address = shipping_address
        self.status = OrderStatus.PLACED
        self.placed_at = datetime.utcnow()

        self._events.append(OrderPlaced(
            order_id=self.id,
            customer_id=self.customer_id,
            total=self.total,
        ))

    def mark_paid(self) -> None:
        """Mark order as paid."""
        if self.status != OrderStatus.PLACED:
            raise DomainError("Order must be placed before payment")
        self.status = OrderStatus.PAID

    def ship(self, tracking_number: str) -> None:
        """Ship the order."""
        if self.status != OrderStatus.PAID:
            raise DomainError("Order must be paid before shipping")

        self.status = OrderStatus.SHIPPED
        self._events.append(OrderShipped(
            order_id=self.id,
            tracking_number=tracking_number,
        ))

    def cancel(self) -> None:
        """Cancel the order."""
        if self.status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            raise DomainError("Cannot cancel shipped order")
        self.status = OrderStatus.CANCELLED

    @property
    def total(self) -> Money:
        """Calculate order total."""
        if not self.lines:
            return Money(Decimal("0"), "USD")

        total = sum(line.total.amount for line in self.lines)
        return Money(total, self.lines[0].unit_price.currency)

    def collect_events(self) -> List:
        events = self._events.copy()
        self._events.clear()
        return events
```

### Value Objects

```python
# order/domain/value_objects.py
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
import re


@dataclass(frozen=True)
class Money:
    """Value object representing monetary amount."""

    amount: Decimal
    currency: str

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if len(self.currency) != 3:
            raise ValueError("Currency must be 3-letter code")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, multiplier: int) -> "Money":
        return Money(self.amount * multiplier, self.currency)


@dataclass(frozen=True)
class Address:
    """Value object representing a shipping address."""

    street: str
    city: str
    state: str
    postal_code: str
    country: str

    def __post_init__(self):
        if not all([self.street, self.city, self.postal_code, self.country]):
            raise ValueError("Address fields cannot be empty")

    def format(self) -> str:
        return f"{self.street}, {self.city}, {self.state} {self.postal_code}, {self.country}"


@dataclass(frozen=True)
class Email:
    """Value object representing an email address."""

    value: str

    def __post_init__(self):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, self.value):
            raise ValueError(f"Invalid email: {self.value}")
        object.__setattr__(self, 'value', self.value.lower())


@dataclass(frozen=True)
class PhoneNumber:
    """Value object representing a phone number."""

    country_code: str
    number: str

    def __post_init__(self):
        # Remove non-digits
        cleaned = re.sub(r'\D', '', self.number)
        if len(cleaned) < 10:
            raise ValueError("Phone number too short")
        object.__setattr__(self, 'number', cleaned)

    def format(self) -> str:
        return f"+{self.country_code} {self.number}"
```

### Domain Events

```python
# order/domain/events.py
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class DomainEvent:
    """Base class for domain events."""
    occurred_at: datetime = None

    def __post_init__(self):
        if self.occurred_at is None:
            object.__setattr__(self, 'occurred_at', datetime.utcnow())


@dataclass(frozen=True)
class OrderPlaced(DomainEvent):
    """Event raised when an order is placed."""
    order_id: UUID
    customer_id: UUID
    total: "Money"


@dataclass(frozen=True)
class OrderShipped(DomainEvent):
    """Event raised when an order is shipped."""
    order_id: UUID
    tracking_number: str


@dataclass(frozen=True)
class OrderCancelled(DomainEvent):
    """Event raised when an order is cancelled."""
    order_id: UUID
    reason: str


# Event handlers (application layer)
class OrderPlacedHandler:
    """Handle order placed event."""

    def __init__(self, email_service, inventory_service):
        self._email_service = email_service
        self._inventory_service = inventory_service

    async def handle(self, event: OrderPlaced) -> None:
        # Send confirmation email
        await self._email_service.send_order_confirmation(
            order_id=event.order_id,
            customer_id=event.customer_id,
        )

        # Reserve inventory
        await self._inventory_service.reserve(event.order_id)
```

### Repository Pattern

```python
# order/domain/repositories.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from .entities.order import Order


class OrderRepository(ABC):
    """Repository interface for Order aggregate."""

    @abstractmethod
    async def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """Find order by ID."""
        pass

    @abstractmethod
    async def find_by_customer(self, customer_id: UUID) -> List[Order]:
        """Find all orders for a customer."""
        pass

    @abstractmethod
    async def save(self, order: Order) -> None:
        """Save order (insert or update)."""
        pass

    @abstractmethod
    async def delete(self, order: Order) -> None:
        """Delete order."""
        pass


# order/infrastructure/repositories.py
class SQLAlchemyOrderRepository(OrderRepository):
    """SQLAlchemy implementation of OrderRepository."""

    def __init__(self, session):
        self._session = session

    async def find_by_id(self, order_id: UUID) -> Optional[Order]:
        model = await self._session.get(OrderModel, order_id)
        return self._to_entity(model) if model else None

    async def save(self, order: Order) -> None:
        model = self._to_model(order)
        self._session.add(model)
        # Events will be dispatched after commit

    def _to_entity(self, model: OrderModel) -> Order:
        return Order(
            id=model.id,
            customer_id=model.customer_id,
            status=OrderStatus(model.status),
            lines=[
                OrderLine(
                    product_id=line.product_id,
                    product_name=line.product_name,
                    quantity=line.quantity,
                    unit_price=Money(line.unit_price, line.currency),
                )
                for line in model.lines
            ],
            shipping_address=Address(
                street=model.shipping_street,
                city=model.shipping_city,
                state=model.shipping_state,
                postal_code=model.shipping_postal,
                country=model.shipping_country,
            ) if model.shipping_street else None,
            placed_at=model.placed_at,
        )
```

### Domain Services

```python
# order/domain/services.py
from decimal import Decimal
from typing import List

from .entities.order import Order, OrderLine
from .value_objects import Money


class PricingService:
    """Domain service for pricing calculations."""

    def __init__(self, discount_rules: List["DiscountRule"]):
        self._discount_rules = discount_rules

    def calculate_total(self, order: Order) -> Money:
        """Calculate order total with applicable discounts."""
        subtotal = order.total

        # Apply discount rules
        discount = Decimal("0")
        for rule in self._discount_rules:
            if rule.applies_to(order):
                discount += rule.calculate_discount(subtotal)

        final_amount = subtotal.amount - discount
        return Money(max(final_amount, Decimal("0")), subtotal.currency)


class ShippingService:
    """Domain service for shipping calculations."""

    def calculate_shipping_cost(self, order: Order) -> Money:
        """Calculate shipping cost based on destination and weight."""
        # Business rules for shipping
        base_cost = Decimal("5.99")

        # Free shipping for orders over $50
        if order.total.amount >= Decimal("50"):
            return Money(Decimal("0"), order.total.currency)

        return Money(base_cost, order.total.currency)
```

### Anti-Corruption Layer

```python
# order/infrastructure/acl/inventory_adapter.py
from uuid import UUID

from order.domain.interfaces import InventoryChecker
from external.inventory_api import InventoryApiClient


class InventoryAdapter(InventoryChecker):
    """Anti-corruption layer for external inventory service."""

    def __init__(self, client: InventoryApiClient):
        self._client = client

    async def check_availability(self, product_id: UUID, quantity: int) -> bool:
        """Check if product is available in required quantity."""
        try:
            # External API uses different terminology
            response = await self._client.get_stock_level(str(product_id))

            # Translate external model to our domain concepts
            available_quantity = response.get("availableUnits", 0)
            return available_quantity >= quantity

        except ExternalApiError:
            # Fail safely - assume available
            return True

    async def reserve(self, product_id: UUID, quantity: int) -> str:
        """Reserve inventory for order."""
        response = await self._client.create_reservation({
            "sku": str(product_id),
            "units": quantity,
            "type": "CUSTOMER_ORDER",
        })

        return response["reservationId"]
```

## Anti-patterns

### Avoid: Anemic Domain Model

```python
# BAD - just data, no behavior
class Order:
    def __init__(self):
        self.id = None
        self.status = None
        self.lines = []

class OrderService:
    def place_order(self, order):
        order.status = "placed"
        # All logic in service

# GOOD - rich domain model
class Order:
    def place(self, shipping_address):
        if self.status != OrderStatus.DRAFT:
            raise DomainError("Order already placed")
        self.status = OrderStatus.PLACED
        self.shipping_address = shipping_address
        self._events.append(OrderPlaced(self.id))
```

### Avoid: Crossing Aggregate Boundaries

```python
# BAD - reaching into another aggregate
class Order:
    def place(self):
        # Don't access other aggregate internals
        if self.customer.wallet.balance < self.total:
            raise Error("Insufficient funds")

# GOOD - use domain events or application service
class PlaceOrderUseCase:
    async def execute(self, order_id, customer_id):
        order = await self.order_repo.find(order_id)
        customer = await self.customer_repo.find(customer_id)

        if not customer.can_afford(order.total):
            raise InsufficientFundsError()

        order.place()
```

## References

- [Domain-Driven Design by Eric Evans](https://www.domainlanguage.com/ddd/)
- [Implementing Domain-Driven Design by Vaughn Vernon](https://www.oreilly.com/library/view/implementing-domain-driven-design/9780133039900/)
- [DDD Reference](https://www.domainlanguage.com/ddd/reference/)
- [Martin Fowler's DDD Articles](https://martinfowler.com/tags/domain%20driven%20design.html)
