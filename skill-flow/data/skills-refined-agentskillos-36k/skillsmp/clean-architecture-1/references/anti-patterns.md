# Clean Architecture Anti-Patterns

Patterns to avoid when implementing Clean Architecture.

## 1. Domain Layer Violations

### Anemic Domain Model

```python
# BAD - Entity with no behavior (just data container)
@dataclass
class Order:
    id: OrderId
    status: str
    total: float
    items: list[OrderItem]

# Service does all the work
class OrderService:
    def cancel_order(self, order: Order) -> None:
        if order.status == "shipped":
            raise Exception("Cannot cancel")
        order.status = "cancelled"  # Direct mutation

# GOOD - Rich domain model with behavior
@dataclass
class Order:
    id: OrderId
    status: OrderStatus
    items: list[OrderItem]

    def cancel(self) -> None:
        """Domain logic encapsulated in entity"""
        if self.status == OrderStatus.SHIPPED:
            raise CannotCancelShippedOrderError()
        self.status = OrderStatus.CANCELLED

    @property
    def total(self) -> Money:
        return sum((item.subtotal for item in self.items), Money.zero())
```

### Infrastructure Leakage

```python
# BAD - Domain entity with SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

class User:
    id: Mapped[int] = mapped_column(primary_key=True)  # ORM in domain!
    email: Mapped[str]

# GOOD - Pure domain entity
@dataclass
class User:
    id: UserId
    email: Email

# Mapping in infrastructure layer
class UserModel(Base):  # ORM model separate from domain
    __tablename__ = "users"
    id = Column(UUID, primary_key=True)
    email = Column(String)
```

### Primitive Obsession

```python
# BAD - Using primitives for domain concepts
class User:
    def __init__(self, email: str, phone: str):
        self.email = email  # No validation
        self.phone = phone

# GOOD - Value Objects for domain concepts
@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not self._is_valid(self.value):
            raise InvalidEmailError(self.value)

class User:
    def __init__(self, email: Email, phone: PhoneNumber):
        self.email = email  # Type-safe, validated
        self.phone = phone
```

---

## 2. Application Layer Violations

### Fat Use Case

```python
# BAD - Use case doing too much
class CreateOrderInteractor:
    async def execute(self, cmd: CreateOrderCommand) -> OrderId:
        # Validation (should be in Value Object)
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', cmd.email):
            raise InvalidEmailError()

        # Infrastructure concern (should be in adapter)
        async with self._session.begin():
            ...

        # Notification (should be separate use case or event)
        await self._email_service.send_confirmation(...)

        # Logging (cross-cutting concern)
        logger.info(f"Order created: {order.id}")

        return order.id

# GOOD - Focused use case
class CreateOrderInteractor:
    async def execute(self, cmd: CreateOrderCommand) -> OrderId:
        # 1. Create domain entity (validation in Value Objects)
        order = Order.create(
            customer=CustomerId(cmd.customer_id),
            items=[OrderItem(p, q) for p, q in cmd.items],
        )

        # 2. Persist
        await self._repo.save(order)

        # 3. Commit
        await self._tx.commit()

        # 4. Publish event (for notifications, etc.)
        await self._events.publish(OrderCreated(order.id))

        return order.id
```

### Direct Infrastructure Access

```python
# BAD - Use case using infrastructure directly
from sqlalchemy.ext.asyncio import AsyncSession

class GetUserInteractor:
    def __init__(self, session: AsyncSession):  # Infrastructure type!
        self._session = session

    async def execute(self, user_id: UUID) -> UserDTO:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )  # SQL in application layer!
        ...

# GOOD - Use case using ports
class GetUserInteractor:
    def __init__(self, user_repo: UserRepository):  # Port (interface)
        self._repo = user_repo

    async def execute(self, user_id: UUID) -> UserDTO:
        user = await self._repo.get_by_id(UserId(user_id))
        ...
```

---

## 3. Infrastructure Layer Violations

### Business Logic in Adapter

```python
# BAD - Business rules in repository
class PostgresOrderRepository:
    async def save(self, order: Order) -> None:
        # Business logic in infrastructure!
        if order.total.value > 10000:
            order.status = OrderStatus.REQUIRES_APPROVAL

        model = self._to_model(order)
        self._session.add(model)

# GOOD - Repository only handles persistence
class PostgresOrderRepository:
    async def save(self, order: Order) -> None:
        model = self._to_model(order)
        self._session.add(model)
        await self._session.flush()
```

### Returning ORM Models

```python
# BAD - Repository returns ORM model
class PostgresUserRepository:
    async def get_by_id(self, id: UUID) -> UserModel | None:  # ORM type!
        return await self._session.get(UserModel, id)

# GOOD - Repository returns domain entity
class PostgresUserRepository:
    async def get_by_id(self, id: UserId) -> User | None:
        model = await self._session.get(UserModel, id.value)
        return self._to_entity(model) if model else None
```

---

## 4. Presentation Layer Violations

### Business Logic in Controller

```python
# BAD - Controller with business logic
@router.post("/orders")
async def create_order(request: CreateOrderRequest):
    # Business logic in controller!
    if request.total > 10000:
        raise HTTPException(400, "Order requires approval")

    items = []
    for item in request.items:
        product = await product_repo.get(item.product_id)
        if product.stock < item.quantity:
            raise HTTPException(400, "Insufficient stock")
        items.append(OrderItem(product, item.quantity))

    order = Order(items=items)
    await order_repo.save(order)
    return {"id": order.id}

# GOOD - Controller delegates to use case
@router.post("/orders")
async def create_order(
    request: CreateOrderRequest,
    interactor: CreateOrderInteractor = Depends(get_create_order),
):
    try:
        order_id = await interactor.execute(
            CreateOrderCommand(
                customer_id=request.customer_id,
                items=request.items,
            )
        )
        return {"id": order_id}
    except InsufficientStockError as e:
        raise HTTPException(400, str(e))
```

### Exposing Domain Entities

```python
# BAD - Returning domain entity directly
@router.get("/users/{user_id}")
async def get_user(user_id: UUID) -> User:  # Domain entity exposed!
    return await user_service.get_by_id(user_id)

# GOOD - Using DTO/Response schema
@router.get("/users/{user_id}")
async def get_user(
    user_id: UUID,
    service: GetUserQueryService = Depends(get_user_service),
) -> UserResponse:
    user_dto = await service.execute(GetUserQuery(user_id))
    if not user_dto:
        raise HTTPException(404, "User not found")
    return UserResponse.from_dto(user_dto)
```

---

## 5. Dependency Violations

### Service Locator Pattern

```python
# BAD - Service locator (global container access)
class CreateUserInteractor:
    async def execute(self, cmd: CreateUserCommand) -> UserId:
        repo = Container.get(UserRepository)  # Global access!
        hasher = Container.get(PasswordHasher)
        ...

# GOOD - Constructor injection
class CreateUserInteractor:
    def __init__(
        self,
        repo: UserRepository,
        hasher: PasswordHasher,
    ):
        self._repo = repo
        self._hasher = hasher

    async def execute(self, cmd: CreateUserCommand) -> UserId:
        ...
```

### Circular Dependencies

```python
# BAD - Circular dependency
# user_service.py
from order_service import OrderService

class UserService:
    def __init__(self, order_service: OrderService):
        self._orders = order_service

# order_service.py
from user_service import UserService

class OrderService:
    def __init__(self, user_service: UserService):  # Circular!
        self._users = user_service

# GOOD - Break cycle with ports
# ports/user_provider.py
class UserProvider(Protocol):
    async def get_user(self, id: UserId) -> User | None: ...

# order_service.py
class OrderService:
    def __init__(self, user_provider: UserProvider):  # Depends on interface
        self._users = user_provider
```

---

## 6. Testing Anti-Patterns

### Testing Implementation Details

```python
# BAD - Testing internal implementation
def test_user_repository_uses_select():
    repo = PostgresUserRepository(mock_session)
    await repo.get_by_id(user_id)

    # Testing SQLAlchemy internals!
    mock_session.execute.assert_called_with(
        select(UserModel).where(UserModel.id == user_id)
    )

# GOOD - Testing behavior
async def test_user_repository_returns_user():
    # Setup with real test database
    repo = PostgresUserRepository(test_session)
    user = create_test_user()
    await repo.save(user)

    # Test behavior
    result = await repo.get_by_id(user.id)

    assert result is not None
    assert result.email == user.email
```

### Not Testing in Isolation

```python
# BAD - Use case test hits real database
async def test_create_user():
    session = create_real_session()
    repo = PostgresUserRepository(session)
    interactor = CreateUserInteractor(repo, ...)

    result = await interactor.execute(cmd)  # Hits real DB!

# GOOD - Use case test with mocks
async def test_create_user():
    repo = MockUserRepository()
    hasher = MockPasswordHasher()
    interactor = CreateUserInteractor(repo, hasher, MockTx())

    result = await interactor.execute(cmd)  # No external dependencies

    assert result is not None
    assert len(repo.saved_users) == 1
```

---

## Quick Reference: What Goes Where

| Concern | Correct Layer | Wrong Layer |
|---------|--------------|-------------|
| Validation rules | Domain (Value Objects) | Controller |
| Business rules | Domain (Entities, Services) | Repository |
| Transaction management | Application (Use Case) | Repository |
| SQL queries | Infrastructure (Adapter) | Application |
| HTTP status codes | Presentation | Application |
| Logging | Cross-cutting (Middleware) | Use Case |
| Authentication | Presentation/Middleware | Domain |
| Authorization | Application | Controller |
