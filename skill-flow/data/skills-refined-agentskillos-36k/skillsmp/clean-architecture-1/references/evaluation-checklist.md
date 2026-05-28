# Clean Architecture Evaluation Checklist

Use this checklist to evaluate code quality and architecture compliance.

## 1. Dependency Rule Compliance

### Domain Layer

- [ ] **No framework imports** in domain layer
  - No FastAPI, SQLAlchemy, Redis imports
  - Only standard library and domain modules
- [ ] **No infrastructure imports** in domain layer
  - No database models, external clients
- [ ] **Entities have no ORM decorators**
  - Use separate mapping in infrastructure

```python
# BAD - Domain coupled to SQLAlchemy
from sqlalchemy.orm import Mapped
class User:
    id: Mapped[int]  # Infrastructure leak!

# GOOD - Pure domain entity
@dataclass
class User:
    id: UserId
    email: Email
```

### Application Layer

- [ ] **Only imports from Domain**
- [ ] **No direct infrastructure usage**
  - Uses Ports (interfaces) only
- [ ] **No HTTP/Framework specifics**
  - No FastAPI Response, Request objects

### Infrastructure Layer

- [ ] **Implements Ports correctly**
  - Method signatures match Protocol
- [ ] **No domain logic in adapters**
  - Only data transformation and I/O

### Presentation Layer

- [ ] **Only imports from Application**
- [ ] **No direct domain entity exposure**
  - Uses DTOs for API responses

---

## 2. Port/Adapter Pattern

### Port Definition

- [ ] **Uses Protocol (not ABC)** for structural typing
- [ ] **Single Responsibility** - one purpose per port
- [ ] **Named appropriately**
  - `{Entity}Repository`, `{Action}er`, `{Entity}Gateway`
- [ ] **Returns domain types** (not ORM models)

### Adapter Implementation

- [ ] **Implements all port methods**
- [ ] **Handles technology-specific concerns**
  - Connection management, error translation
- [ ] **Maps between domain and infrastructure types**

```python
# Port
class UserRepository(Protocol):
    async def get_by_id(self, id: UserId) -> User | None: ...

# Adapter - correct implementation
class PostgresUserRepository:
    async def get_by_id(self, id: UserId) -> User | None:
        model = await self._session.get(UserModel, id.value)
        return self._to_entity(model) if model else None
```

---

## 3. CQRS Compliance

### Command Use Cases

- [ ] **Named `{Verb}{Noun}Interactor`**
- [ ] **Has explicit command DTO** as input
- [ ] **Modifies state** (create, update, delete)
- [ ] **Uses write repository/gateway**
- [ ] **Manages transactions** explicitly
- [ ] **Returns ID or void** (not full entity)

### Query Use Cases

- [ ] **Named `{Verb}{Noun}QueryService`**
- [ ] **Has explicit query DTO** as input
- [ ] **Read-only** (no state changes)
- [ ] **Uses read gateway** (not write repository)
- [ ] **No transaction management**
- [ ] **Returns DTO** (not entity)

---

## 4. Value Object Quality

- [ ] **Immutable** (`frozen=True`)
- [ ] **Self-validating** in `__post_init__`
- [ ] **Equality by value** (automatic with dataclass)
- [ ] **No identity** (no ID field)
- [ ] **Encapsulates validation rules**

```python
# GOOD Value Object
@dataclass(frozen=True, slots=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not self._is_valid(self.value):
            raise InvalidEmailError(self.value)

    @staticmethod
    def _is_valid(email: str) -> bool:
        return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))
```

---

## 5. Entity Quality

- [ ] **Has unique identity** (ID field)
- [ ] **Identity is immutable** once set
- [ ] **Equality by ID** (not by value)
- [ ] **Encapsulates business rules**
- [ ] **State changes through methods** (not direct field access)

```python
# GOOD Entity
@dataclass
class Order:
    id: OrderId
    status: OrderStatus
    items: list[OrderItem]

    def cancel(self) -> None:
        if self.status == OrderStatus.SHIPPED:
            raise CannotCancelShippedOrderError()
        self.status = OrderStatus.CANCELLED

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Order) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
```

---

## 6. Use Case Quality

- [ ] **Single responsibility** - one use case per class
- [ ] **Dependencies injected** via constructor
- [ ] **Input is explicit DTO** (not raw dict or kwargs)
- [ ] **Output is explicit DTO** (not entity)
- [ ] **Handles authorization** if needed
- [ ] **Transaction boundaries** are clear

```python
# GOOD Use Case
class CreateOrderInteractor:
    def __init__(
        self,
        order_repo: OrderRepository,
        inventory: InventoryService,
        tx: TransactionManager,
    ):
        self._repo = order_repo
        self._inventory = inventory
        self._tx = tx

    async def execute(self, cmd: CreateOrderCommand) -> OrderId:
        # 1. Validate inventory
        await self._inventory.reserve(cmd.items)

        # 2. Create domain entity
        order = Order.create(customer_id=cmd.customer_id, items=cmd.items)

        # 3. Persist
        await self._repo.save(order)

        # 4. Commit transaction
        await self._tx.commit()

        return order.id
```

---

## 7. Exception Handling

- [ ] **Layer-specific exceptions**
  - Domain: `DomainError`, `InvalidEmailError`
  - Application: `UserNotFoundError`, `AuthorizationError`
  - Infrastructure: `DatabaseConnectionError`
- [ ] **Exceptions don't cross boundaries inappropriately**
- [ ] **Presentation translates to HTTP status codes**

---

## 8. Testing

- [ ] **Domain layer: Unit tests only** (no mocks needed)
- [ ] **Application layer: Unit tests with mocked ports**
- [ ] **Infrastructure layer: Integration tests**
- [ ] **Presentation layer: E2E or integration tests**
- [ ] **Each layer testable independently**

---

## 9. Code Smells to Check

| Smell | Indication | Fix |
|-------|------------|-----|
| **Anemic Domain Model** | Entities with only getters/setters | Add behavior methods |
| **Fat Controller** | Business logic in router | Move to Use Case |
| **Service Locator** | Global container access | Constructor injection |
| **Primitive Obsession** | Raw strings for Email, IDs | Use Value Objects |
| **Leaky Abstraction** | SQLAlchemy types in domain | Create proper mapping |
| **God Object** | One class does everything | Split by responsibility |

---

## 10. Quick Evaluation Questions

1. **Can I test the domain without a database?** → Yes = Good
2. **Can I swap PostgreSQL for MongoDB easily?** → Yes = Good
3. **Does the domain know about HTTP?** → No = Good
4. **Are all dependencies injected?** → Yes = Good
5. **Can I understand the use case without reading infrastructure code?** → Yes = Good

---

## Scoring Guide

| Score | Level | Description |
|-------|-------|-------------|
| 90-100% | Excellent | Production-ready, maintainable |
| 70-89% | Good | Minor improvements needed |
| 50-69% | Fair | Significant refactoring recommended |
| < 50% | Poor | Major architectural issues |
