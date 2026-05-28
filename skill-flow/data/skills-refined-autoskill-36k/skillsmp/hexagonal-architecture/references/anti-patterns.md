# Anti-Patterns and Architectural Drift

## Dependency Rule Violations

### Infrastructure in Domain

**Symptom:** Domain entities decorated with ORM or serialization annotations.

```python
# BAD: SQLAlchemy in domain
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(String)
```

**Fix:** Separate domain model from persistence model:

```python
# domain/model/order.py
@dataclass
class Order:
    id: OrderId
    customer_id: CustomerId
    items: list[OrderItem]
    status: OrderStatus

# adapters/persistence/models.py
class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True)
    customer_id = Column(String)
    status = Column(String)
    
    def to_domain(self) -> Order:
        return Order(
            id=OrderId(self.id),
            customer_id=CustomerId(self.customer_id),
            items=self._load_items(),
            status=OrderStatus(self.status),
        )
    
    @classmethod
    def from_domain(cls, order: Order) -> "OrderModel":
        return cls(
            id=str(order.id),
            customer_id=str(order.customer_id),
            status=order.status.value,
        )
```

### Framework Types in Port Signatures

**Symptom:** Ports return or accept framework-specific types.

```python
# BAD: Flask request in application layer
class CreateUserUseCase:
    def execute(self, request: flask.Request) -> flask.Response:
        ...
```

**Fix:** Use domain DTOs:

```python
# application/commands.py
@dataclass(frozen=True)
class CreateUserCommand:
    email: str
    name: str

@dataclass(frozen=True)
class CreateUserResult:
    user_id: str
    success: bool

# application/create_user.py
class CreateUserUseCase:
    def execute(self, command: CreateUserCommand) -> CreateUserResult:
        ...

# adapters/inbound/http/users.py
@app.post("/users")
def create_user():
    command = CreateUserCommand(
        email=request.json["email"],
        name=request.json["name"],
    )
    result = use_case.execute(command)
    return jsonify({"user_id": result.user_id}), 201
```

### Direct Infrastructure Calls from Domain

**Symptom:** Domain services make HTTP calls, database queries, or filesystem operations directly.

```python
# BAD: HTTP call in domain service
class PricingService:
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        response = requests.get(f"https://api.exchange.com/{from_currency}/{to_currency}")
        return response.json()["rate"]
```

**Fix:** Inject via port:

```python
# domain/ports/exchange.py
class ExchangeRatePort(ABC):
    @abstractmethod
    def get_rate(self, from_currency: Currency, to_currency: Currency) -> Decimal:
        ...

# domain/services/pricing.py
class PricingService:
    def __init__(self, exchange_rates: ExchangeRatePort):
        self._exchange_rates = exchange_rates
    
    def convert(self, amount: Money, to_currency: Currency) -> Money:
        rate = self._exchange_rates.get_rate(amount.currency, to_currency)
        return Money(amount.value * rate, to_currency)
```

## Adapter Coupling

### Adapters Calling Adapters

**Symptom:** One adapter directly invokes another, bypassing the domain.

```python
# BAD: HTTP adapter calls notification adapter directly
@app.post("/orders")
def create_order():
    order = process_order(request.json)
    email_adapter.send_confirmation(order)  # Direct coupling
    return jsonify(order.to_dict())
```

**Fix:** Coordinate through application service or domain events:

```python
# Option 1: Application service orchestrates
class PlaceOrderUseCase:
    def __init__(self, orders: OrderRepository, notifications: NotificationPort):
        self._orders = orders
        self._notifications = notifications
    
    def execute(self, command: PlaceOrderCommand) -> PlaceOrderResult:
        order = Order.create(...)
        self._orders.save(order)
        self._notifications.send_order_confirmation(order)
        return PlaceOrderResult.success(order.id)

# Option 2: Domain events (decoupled)
class PlaceOrderUseCase:
    def execute(self, command: PlaceOrderCommand) -> PlaceOrderResult:
        order = Order.create(...)  # Emits OrderPlaced event
        self._orders.save(order)
        self._event_publisher.publish(order.pending_events)
        return PlaceOrderResult.success(order.id)

# Separate handler listens for OrderPlaced, sends notification
```

### Shared Adapter State

**Symptom:** Adapters share mutable state outside the domain.

```python
# BAD: Shared cache between adapters
_cache = {}

class ProductApiAdapter:
    def get_product(self, sku: str):
        if sku in _cache:
            return _cache[sku]
        ...

class InventoryApiAdapter:
    def check_stock(self, sku: str):
        product = _cache.get(sku)  # Depends on ProductApiAdapter having populated cache
        ...
```

**Fix:** Cache within individual adapters or use explicit caching port:

```python
class CachingPort(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]: ...
    @abstractmethod
    def set(self, key: str, value: Any, ttl: timedelta) -> None: ...

class ProductApiAdapter:
    def __init__(self, cache: CachingPort):
        self._cache = cache
```

## Abstraction Leaks

### Leaking Implementation Through Port Interface

**Symptom:** Port methods expose implementation details.

```python
# BAD: Port reveals it's backed by SQL
class OrderRepository(ABC):
    @abstractmethod
    def find_by_query(self, sql: str, params: dict) -> list[Order]:
        ...

# BAD: Port reveals pagination implementation
class OrderRepository(ABC):
    @abstractmethod
    def find_page(self, offset: int, limit: int) -> tuple[list[Order], int]:
        ...  # Offset pagination couples to SQL-style storage
```

**Fix:** Express intent in domain terms:

```python
class OrderRepository(ABC):
    @abstractmethod
    def find_by_criteria(self, criteria: OrderSearchCriteria) -> list[Order]:
        ...
    
    @abstractmethod
    def find_recent(self, customer_id: CustomerId, max_results: int) -> list[Order]:
        ...

# If pagination is genuinely needed:
@dataclass(frozen=True)
class PageRequest:
    cursor: Optional[str]  # Opaque cursor, works with any storage
    size: int

@dataclass(frozen=True)
class Page[T]:
    items: list[T]
    next_cursor: Optional[str]
    has_more: bool
```

### Adapter Logic Containing Business Rules

**Symptom:** Adapters make business decisions.

```python
# BAD: Business rule in adapter
class PostgresOrderRepository(OrderRepository):
    def save(self, order: Order) -> None:
        # Business rule leaked into adapter
        if order.total > Money(10000):
            order.status = OrderStatus.REQUIRES_APPROVAL
        self._session.add(OrderModel.from_domain(order))
```

**Fix:** Business rules belong in domain:

```python
# domain/model/order.py
class Order:
    def confirm(self) -> None:
        if self.total > Money(10000):
            self._status = OrderStatus.REQUIRES_APPROVAL
        else:
            self._status = OrderStatus.CONFIRMED
```

## Drift Detection Checklist

Run periodically during code review and CI:

### Import Analysis

```bash
# Find domain files importing infrastructure
grep -r "from adapters" src/domain/
grep -r "import sqlalchemy" src/domain/
grep -r "import requests" src/domain/
grep -r "import flask" src/domain/ src/application/
```

### Decorator Scan

```bash
# Find ORM/framework decorators in domain
grep -r "@Column" src/domain/
grep -r "@relationship" src/domain/
grep -r "@validator" src/domain/  # Pydantic in domain (debatable)
grep -r "@app\." src/domain/ src/application/  # Flask routes
```

### Test Dependency Check

```bash
# Domain tests should not need fixtures
grep -r "pytest.fixture" tests/domain/
grep -r "@pytest.mark.integration" tests/domain/

# Check for infrastructure imports in domain tests
grep -r "import sqlalchemy" tests/domain/
grep -r "from adapters" tests/domain/
```

## Refactoring Patterns

### Extract Port from Direct Dependency

When you find a direct infrastructure call in the domain:

1. Identify the capability needed (what does the call provide?)
2. Define port interface using domain language
3. Create adapter implementing the port
4. Inject port into domain code
5. Update tests to use mocks/fakes

### Consolidate Scattered Adapters

When similar infrastructure code appears in multiple adapters:

1. Identify the shared concern (connection management, serialization, etc.)
2. Extract to shared infrastructure utility (not a port—utilities are adapter-internal)
3. Each adapter remains responsible for its own port implementation

### Split Oversized Port

When a port interface grows beyond 7 methods:

1. Group methods by cohesion (read vs write, entity type, frequency of change)
2. Define new port interfaces for each group
3. Update adapters to implement multiple ports if needed
4. Update application services to depend on specific ports they need
