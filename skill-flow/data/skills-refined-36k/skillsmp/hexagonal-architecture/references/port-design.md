# Port Design Patterns

## Driven Port Patterns

### Repository Pattern

Repositories abstract persistence. They speak domain language and return domain types.

**Minimal interface:**

```python
from abc import ABC, abstractmethod
from typing import Optional
from domain.model import Order, OrderId

class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: OrderId) -> Optional[Order]:
        """Return None if not found. Never raise for missing entities."""
        ...
    
    @abstractmethod
    def save(self, order: Order) -> None:
        """Persist order. Handles insert/update transparently."""
        ...
```

**Extended interface (when needed):**

```python
class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: OrderId) -> Optional[Order]: ...
    
    @abstractmethod
    def find_by_customer(self, customer_id: CustomerId) -> list[Order]: ...
    
    @abstractmethod
    def find_pending_before(self, cutoff: datetime) -> list[Order]: ...
    
    @abstractmethod
    def save(self, order: Order) -> None: ...
    
    @abstractmethod
    def delete(self, order_id: OrderId) -> None: ...
```

**Anti-patterns to avoid:**

```python
# BAD: Leaking query implementation
class OrderRepository(ABC):
    @abstractmethod
    def find_by_sql(self, query: str) -> list[Order]: ...

# BAD: Exposing ORM concerns
class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: OrderId, session: Session) -> Order: ...

# BAD: Returning infrastructure types
class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: str) -> dict: ...  # Should be OrderId, Order
```

### Gateway Pattern

Gateways abstract external service calls. Model the domain's view of the external capability, not the external API's structure.

```python
class PaymentGateway(ABC):
    @abstractmethod
    def charge(
        self, 
        amount: Money, 
        payment_method: PaymentMethodToken
    ) -> PaymentResult:
        """
        Returns PaymentResult with success/failure and transaction reference.
        Adapter handles API specifics, retries, error mapping.
        """
        ...
    
    @abstractmethod
    def refund(
        self, 
        transaction_id: TransactionId, 
        amount: Money
    ) -> RefundResult:
        ...
```

**Domain types for gateway results:**

```python
@dataclass(frozen=True)
class PaymentResult:
    success: bool
    transaction_id: Optional[TransactionId]
    failure_reason: Optional[PaymentFailureReason]

class PaymentFailureReason(Enum):
    INSUFFICIENT_FUNDS = "insufficient_funds"
    CARD_DECLINED = "card_declined"
    GATEWAY_UNAVAILABLE = "gateway_unavailable"
    UNKNOWN = "unknown"
```

### Clock and Randomness

Abstract non-deterministic operations for testability:

```python
class Clock(ABC):
    @abstractmethod
    def now(self) -> datetime: ...
    
    @abstractmethod
    def today(self) -> date: ...

class IdGenerator(ABC):
    @abstractmethod
    def generate(self) -> str: ...
```

Production implementations:

```python
class SystemClock(Clock):
    def now(self) -> datetime:
        return datetime.now(timezone.utc)
    
    def today(self) -> date:
        return date.today()

class UUIDGenerator(IdGenerator):
    def generate(self) -> str:
        return str(uuid4())
```

Test implementations:

```python
class FixedClock(Clock):
    def __init__(self, fixed_time: datetime):
        self._time = fixed_time
    
    def now(self) -> datetime:
        return self._time
    
    def today(self) -> date:
        return self._time.date()
    
    def advance(self, delta: timedelta) -> None:
        self._time += delta
```

## Driving Port Patterns

### Application Service / Use Case

Application services orchestrate domain logic. One public method per use case.

```python
class PlaceOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepository,
        inventory_service: InventoryService,
        payment_gateway: PaymentGateway,
        clock: Clock,
    ):
        self._orders = order_repository
        self._inventory = inventory_service
        self._payments = payment_gateway
        self._clock = clock
    
    def execute(self, command: PlaceOrderCommand) -> PlaceOrderResult:
        # 1. Validate inventory
        availability = self._inventory.check_availability(command.items)
        if not availability.all_available:
            return PlaceOrderResult.failed(availability.unavailable_items)
        
        # 2. Create domain object
        order = Order.create(
            customer_id=command.customer_id,
            items=command.items,
            created_at=self._clock.now(),
        )
        
        # 3. Process payment
        payment_result = self._payments.charge(
            amount=order.total,
            payment_method=command.payment_method,
        )
        if not payment_result.success:
            return PlaceOrderResult.payment_failed(payment_result.failure_reason)
        
        # 4. Confirm and persist
        order.confirm(payment_result.transaction_id)
        self._orders.save(order)
        
        return PlaceOrderResult.success(order.id)
```

### Command and Query Objects

Commands represent intent, queries represent information requests:

```python
@dataclass(frozen=True)
class PlaceOrderCommand:
    customer_id: CustomerId
    items: list[OrderItem]
    payment_method: PaymentMethodToken
    
    def validate(self) -> list[str]:
        """Return validation errors. Empty list if valid."""
        errors = []
        if not self.items:
            errors.append("Order must contain at least one item")
        return errors

@dataclass(frozen=True)
class GetOrderQuery:
    order_id: OrderId
    requesting_user: UserId  # For authorization context
```

## Port Granularity Guidelines

**Split ports when:**
- Operations have different consistency requirements
- Operations have different failure modes
- Operations are used by different application services
- Interface exceeds 5-7 methods

**Keep unified when:**
- Operations always occur together
- Splitting would require coordination between ports
- Domain concept is inherently cohesive

**Example split:**

```python
# Instead of one large CustomerRepository:
class CustomerRepository(ABC):
    """Core customer persistence."""
    @abstractmethod
    def find_by_id(self, id: CustomerId) -> Optional[Customer]: ...
    @abstractmethod
    def save(self, customer: Customer) -> None: ...

class CustomerSearchPort(ABC):
    """Customer search capabilities (may use different storage)."""
    @abstractmethod
    def search(self, criteria: SearchCriteria) -> list[CustomerSummary]: ...

class CustomerPreferencesPort(ABC):
    """Preferences may live in different store."""
    @abstractmethod
    def get_preferences(self, id: CustomerId) -> Preferences: ...
    @abstractmethod
    def update_preferences(self, id: CustomerId, prefs: Preferences) -> None: ...
```
