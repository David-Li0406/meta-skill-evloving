---
id: test-fixtures
name: "Test Fixtures"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Test Fixtures

## Overview

Test fixtures provide consistent, reusable test data and setup procedures. They ensure tests have predictable starting conditions, reduce code duplication, and make tests more readable and maintainable.

## When to Use

- Multiple tests need similar setup
- Complex object creation for testing
- Database seeding for integration tests
- External service configuration
- Shared cleanup procedures

## Key Principles

- **Isolation**: Each test gets fresh fixture state
- **Reusability**: Share common setup across tests
- **Readability**: Fixtures should be self-documenting
- **Minimal scope**: Create only what's needed
- **Deterministic**: Same fixture produces same result

## Best Practices

### Pytest Fixtures - Basic Usage

```python
import pytest
from datetime import datetime, timedelta
from decimal import Decimal

# Simple fixture
@pytest.fixture
def sample_user():
    return User(
        id="user-123",
        email="test@example.com",
        name="Test User",
        created_at=datetime(2024, 1, 15, 10, 30, 0)
    )

# Fixture with factory function
@pytest.fixture
def user_factory():
    def create_user(**overrides):
        defaults = {
            "id": f"user-{uuid4().hex[:8]}",
            "email": f"user-{uuid4().hex[:8]}@example.com",
            "name": "Test User",
            "created_at": datetime.utcnow()
        }
        return User(**{**defaults, **overrides})
    return create_user

# Using fixtures in tests
def test_user_full_name(sample_user):
    assert sample_user.full_name == "Test User"

def test_multiple_users(user_factory):
    user1 = user_factory(name="Alice")
    user2 = user_factory(name="Bob")

    assert user1.id != user2.id
    assert user1.name == "Alice"
    assert user2.name == "Bob"
```

### Fixture Scopes

```python
import pytest

# Function scope (default) - new fixture for each test
@pytest.fixture(scope="function")
def fresh_user():
    """Created for each test function."""
    return User(id="fresh", name="Fresh User")

# Class scope - shared within test class
@pytest.fixture(scope="class")
def shared_service():
    """Created once per test class."""
    service = ExpensiveService()
    service.initialize()
    return service

# Module scope - shared within test module
@pytest.fixture(scope="module")
def database_connection():
    """Created once per test module."""
    conn = create_connection()
    yield conn
    conn.close()

# Session scope - shared across entire test session
@pytest.fixture(scope="session")
def docker_container():
    """Created once for entire test run."""
    container = start_postgres_container()
    yield container
    container.stop()

# Example usage with scope
class TestUserService:
    def test_create_user(self, shared_service, fresh_user):
        # shared_service is reused, fresh_user is new
        pass

    def test_update_user(self, shared_service, fresh_user):
        # same shared_service, different fresh_user
        pass
```

### Fixture with Setup and Teardown

```python
import pytest
import tempfile
import shutil
from pathlib import Path

@pytest.fixture
def temp_directory():
    """Fixture with automatic cleanup."""
    # Setup
    temp_dir = Path(tempfile.mkdtemp())

    yield temp_dir

    # Teardown - always runs, even if test fails
    shutil.rmtree(temp_dir)

@pytest.fixture
def populated_temp_dir(temp_directory):
    """Fixture that depends on another fixture."""
    # Create test files
    (temp_directory / "config.json").write_text('{"key": "value"}')
    (temp_directory / "data.csv").write_text("a,b,c\n1,2,3")

    return temp_directory

def test_file_processor(populated_temp_dir):
    processor = FileProcessor(populated_temp_dir)
    result = processor.process_all()

    assert len(result) == 2

# Using built-in tmp_path fixture
def test_with_builtin_tmpdir(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    assert test_file.exists()
    # Automatically cleaned up
```

### Database Fixtures

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def engine():
    """Create database engine for test session."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="session")
def session_factory(engine):
    """Create session factory."""
    return sessionmaker(bind=engine)

@pytest.fixture
def db_session(session_factory):
    """Create a transactional session that rolls back after each test."""
    session = session_factory()
    session.begin_nested()  # Start savepoint

    yield session

    session.rollback()  # Rollback to savepoint
    session.close()

# Fixture composing other fixtures
@pytest.fixture
def db_with_users(db_session, user_factory):
    """Database pre-populated with test users."""
    users = [
        user_factory(name="Alice", role="admin"),
        user_factory(name="Bob", role="user"),
        user_factory(name="Charlie", role="user"),
    ]
    for user in users:
        db_session.add(user)
    db_session.flush()

    return {"session": db_session, "users": users}

def test_find_admins(db_with_users):
    repo = UserRepository(db_with_users["session"])

    admins = repo.find_by_role("admin")

    assert len(admins) == 1
    assert admins[0].name == "Alice"
```

### Parametrized Fixtures

```python
import pytest

@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database_type(request):
    """Run tests with different database types."""
    return request.param

@pytest.fixture
def db_connection(database_type):
    """Create connection based on parametrized type."""
    if database_type == "sqlite":
        conn = create_sqlite_connection()
    elif database_type == "postgresql":
        conn = create_postgres_connection()
    else:
        conn = create_mysql_connection()

    yield conn
    conn.close()

def test_query_execution(db_connection, database_type):
    """This test runs 3 times - once for each database type."""
    result = db_connection.execute("SELECT 1")
    assert result is not None

# Parametrized fixture with IDs
@pytest.fixture(params=[
    pytest.param({"role": "admin", "permissions": ["read", "write", "delete"]}, id="admin"),
    pytest.param({"role": "editor", "permissions": ["read", "write"]}, id="editor"),
    pytest.param({"role": "viewer", "permissions": ["read"]}, id="viewer"),
])
def user_role_config(request):
    return request.param

def test_permission_check(user_role_config):
    user = User(role=user_role_config["role"])
    assert user.permissions == user_role_config["permissions"]
```

### Factory Fixtures with Faker

```python
import pytest
from faker import Faker
from typing import Optional
from datetime import datetime

fake = Faker()

@pytest.fixture
def fake_user_factory(db_session):
    """Factory for creating realistic fake users."""
    created_users = []

    def create(
        name: Optional[str] = None,
        email: Optional[str] = None,
        age: Optional[int] = None,
        **kwargs
    ) -> User:
        user = User(
            id=str(uuid4()),
            name=name or fake.name(),
            email=email or fake.email(),
            age=age or fake.random_int(18, 80),
            address=fake.address(),
            phone=fake.phone_number(),
            created_at=datetime.utcnow(),
            **kwargs
        )
        db_session.add(user)
        db_session.flush()
        created_users.append(user)
        return user

    yield create

    # Cleanup all created users
    for user in created_users:
        db_session.delete(user)

@pytest.fixture
def fake_order_factory(db_session, fake_user_factory):
    """Factory for orders with user dependency."""
    def create(user: Optional[User] = None, **kwargs) -> Order:
        if user is None:
            user = fake_user_factory()

        order = Order(
            id=str(uuid4()),
            user_id=user.id,
            total=Decimal(fake.pydecimal(min_value=10, max_value=1000)),
            status="pending",
            **kwargs
        )
        db_session.add(order)
        db_session.flush()
        return order

    return create

# Using factories
def test_user_order_relationship(fake_user_factory, fake_order_factory):
    user = fake_user_factory(name="Test Customer")
    order1 = fake_order_factory(user=user)
    order2 = fake_order_factory(user=user)

    assert len(user.orders) == 2
```

### conftest.py Organization

```python
# tests/conftest.py - Root conftest for shared fixtures

import pytest

@pytest.fixture(scope="session")
def app_config():
    """Application configuration for tests."""
    return {
        "DATABASE_URL": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret-key",
        "DEBUG": True
    }

@pytest.fixture(scope="session")
def app(app_config):
    """Create application instance."""
    from myapp import create_app
    app = create_app(app_config)
    return app

# tests/unit/conftest.py - Unit test specific fixtures

@pytest.fixture
def mock_repository():
    """Mock repository for unit tests."""
    return Mock(spec=UserRepository)

# tests/integration/conftest.py - Integration test fixtures

@pytest.fixture(scope="module")
def test_database():
    """Real database for integration tests."""
    db = create_test_database()
    yield db
    db.drop_all()

# tests/e2e/conftest.py - E2E test fixtures

@pytest.fixture(scope="session")
def browser():
    """Browser instance for E2E tests."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()
```

### TypeScript/Jest Fixtures

```typescript
// __fixtures__/users.ts
import { User } from '../types';

export const testUsers = {
  admin: {
    id: 'user-admin',
    email: 'admin@example.com',
    name: 'Admin User',
    role: 'admin',
  } as User,

  regularUser: {
    id: 'user-regular',
    email: 'user@example.com',
    name: 'Regular User',
    role: 'user',
  } as User,
};

export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: `user-${Date.now()}`,
    email: `user-${Date.now()}@example.com`,
    name: 'Test User',
    role: 'user',
    createdAt: new Date(),
    ...overrides,
  };
}

// __fixtures__/orders.ts
import { Order, OrderItem } from '../types';
import { createUser } from './users';

export function createOrder(overrides: Partial<Order> = {}): Order {
  return {
    id: `order-${Date.now()}`,
    userId: createUser().id,
    items: [],
    total: 0,
    status: 'pending',
    createdAt: new Date(),
    ...overrides,
  };
}

export function createOrderItem(overrides: Partial<OrderItem> = {}): OrderItem {
  return {
    id: `item-${Date.now()}`,
    productId: `product-${Date.now()}`,
    quantity: 1,
    price: 29.99,
    ...overrides,
  };
}

// Usage in tests
import { createUser, createOrder, createOrderItem, testUsers } from '../__fixtures__';

describe('OrderService', () => {
  it('should calculate order total', () => {
    const order = createOrder({
      items: [
        createOrderItem({ quantity: 2, price: 10 }),
        createOrderItem({ quantity: 1, price: 20 }),
      ],
    });

    const total = orderService.calculateTotal(order);

    expect(total).toBe(40);
  });

  it('should allow admin to cancel any order', () => {
    const order = createOrder({ userId: 'other-user' });

    const result = orderService.cancel(order, testUsers.admin);

    expect(result.status).toBe('cancelled');
  });
});
```

### Builder Pattern for Complex Fixtures

```python
from dataclasses import dataclass, field
from typing import Optional, List
from decimal import Decimal

@dataclass
class OrderBuilder:
    """Builder pattern for creating test orders."""

    _id: str = field(default_factory=lambda: str(uuid4()))
    _user_id: str = "default-user"
    _items: List[OrderItem] = field(default_factory=list)
    _status: str = "pending"
    _discount: Optional[Decimal] = None
    _shipping_address: Optional[Address] = None

    def with_id(self, id: str) -> "OrderBuilder":
        self._id = id
        return self

    def for_user(self, user_id: str) -> "OrderBuilder":
        self._user_id = user_id
        return self

    def with_item(
        self,
        sku: str = "SKU-001",
        quantity: int = 1,
        price: Decimal = Decimal("10.00")
    ) -> "OrderBuilder":
        self._items.append(OrderItem(sku=sku, quantity=quantity, price=price))
        return self

    def with_discount(self, discount: Decimal) -> "OrderBuilder":
        self._discount = discount
        return self

    def with_status(self, status: str) -> "OrderBuilder":
        self._status = status
        return self

    def shipped_to(self, address: Address) -> "OrderBuilder":
        self._shipping_address = address
        return self

    def build(self) -> Order:
        return Order(
            id=self._id,
            user_id=self._user_id,
            items=self._items,
            status=self._status,
            discount=self._discount,
            shipping_address=self._shipping_address
        )

# Fixture using builder
@pytest.fixture
def order_builder():
    return OrderBuilder()

# Usage
def test_order_with_multiple_items(order_builder):
    order = (order_builder
        .for_user("user-123")
        .with_item(sku="A", quantity=2, price=Decimal("15.00"))
        .with_item(sku="B", quantity=1, price=Decimal("30.00"))
        .with_discount(Decimal("5.00"))
        .build())

    assert order.subtotal == Decimal("60.00")
    assert order.total == Decimal("55.00")
```

## Anti-patterns

- **God fixtures**: Fixtures that set up everything
- **Tight coupling**: Tests depending on fixture internal state
- **Fixture reuse abuse**: Using session scope when function scope needed
- **Hidden dependencies**: Fixtures that secretly depend on global state
- **Over-engineering**: Complex fixtures for simple test data
- **Missing cleanup**: Resources leaking between tests

## References

- [pytest Fixtures Documentation](https://docs.pytest.org/en/latest/how-to/fixtures.html)
- [Factory Boy for Django](https://factoryboy.readthedocs.io/)
- [Faker Library](https://faker.readthedocs.io/)
- [Test Data Builders](https://www.natpryce.com/articles/000714.html)
