# Pattern: Test Fixtures

> Standard patterns for setting up test data, mocks, and cleanup.

---

## When to Use This Pattern

- Writing unit tests that need consistent test data
- Creating integration tests with database state
- Mocking external services (APIs, file systems)
- Building reusable test utilities

**Do NOT use when:**
- Simple assertions that don't need setup
- End-to-end tests that use production-like data

---

## The Pattern

### TypeScript/JavaScript (Jest)

```typescript
// fixtures/users.ts - Test data factories
import { faker } from '@faker-js/faker';

export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user' | 'guest';
  createdAt: Date;
}

// Factory function with defaults and overrides
export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: faker.string.uuid(),
    email: faker.internet.email(),
    name: faker.person.fullName(),
    role: 'user',
    createdAt: new Date(),
    ...overrides,
  };
}

// Predefined fixtures for common scenarios
export const fixtures = {
  adminUser: createUser({ role: 'admin', email: 'admin@test.com' }),
  guestUser: createUser({ role: 'guest', email: 'guest@test.com' }),
  users: {
    withOrders: createUser({ email: 'orders@test.com' }),
    withoutOrders: createUser({ email: 'no-orders@test.com' }),
  },
};

// Builder pattern for complex objects
export class UserBuilder {
  private user: Partial<User> = {};

  withEmail(email: string): this {
    this.user.email = email;
    return this;
  }

  withRole(role: User['role']): this {
    this.user.role = role;
    return this;
  }

  asAdmin(): this {
    return this.withRole('admin');
  }

  build(): User {
    return createUser(this.user);
  }
}

// Usage: new UserBuilder().asAdmin().withEmail('admin@test.com').build()

// mocks/api.ts - API mocking
import nock from 'nock';

export function mockStripeApi() {
  const scope = nock('https://api.stripe.com')
    .persist()
    .post('/v1/payment_intents')
    .reply(200, {
      id: 'pi_test_123',
      status: 'succeeded',
      amount: 1000,
    });

  return {
    scope,
    cleanup: () => nock.cleanAll(),
  };
}

export function mockStripeError(statusCode: number, error: object) {
  return nock('https://api.stripe.com')
    .post('/v1/payment_intents')
    .reply(statusCode, { error });
}

// db/test-helpers.ts - Database fixtures
import { prisma } from '../src/db';

export async function cleanDatabase() {
  // Delete in correct order to respect foreign keys
  await prisma.$transaction([
    prisma.orderItem.deleteMany(),
    prisma.order.deleteMany(),
    prisma.user.deleteMany(),
  ]);
}

export async function seedDatabase() {
  const user = await prisma.user.create({
    data: createUser(),
  });

  const order = await prisma.order.create({
    data: {
      userId: user.id,
      status: 'pending',
      total: 100,
    },
  });

  return { user, order };
}

// Setup/teardown hooks
export function setupTestDatabase() {
  beforeAll(async () => {
    await cleanDatabase();
  });

  afterEach(async () => {
    await cleanDatabase();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });
}

// test-utils.ts - Common test utilities
import { render, RenderOptions } from '@testing-library/react';
import { ReactElement } from 'react';

// Custom render with providers
const AllProviders = ({ children }: { children: React.ReactNode }) => {
  return (
    <AuthProvider>
      <ThemeProvider>
        {children}
      </ThemeProvider>
    </AuthProvider>
  );
};

export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { wrapper: AllProviders, ...options });
}

// Wait for async operations
export async function waitForCondition(
  condition: () => boolean | Promise<boolean>,
  timeout: number = 5000,
  interval: number = 100
): Promise<void> {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    if (await condition()) return;
    await new Promise(r => setTimeout(r, interval));
  }
  throw new Error('Condition not met within timeout');
}
```

### Python (pytest)

```python
# conftest.py - Shared fixtures
import pytest
from faker import Faker
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

fake = Faker()

# Database fixtures
@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(db_engine) -> Generator[Session, None, None]:
    """Create a new database session for each test."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

# Factory fixtures
@pytest.fixture
def user_factory(db_session):
    """Factory for creating test users."""
    def _create_user(**kwargs):
        defaults = {
            'email': fake.email(),
            'name': fake.name(),
            'role': 'user',
        }
        defaults.update(kwargs)
        user = User(**defaults)
        db_session.add(user)
        db_session.commit()
        return user
    return _create_user

@pytest.fixture
def admin_user(user_factory):
    """Pre-built admin user fixture."""
    return user_factory(role='admin', email='admin@test.com')

@pytest.fixture
def sample_users(user_factory):
    """Collection of sample users."""
    return {
        'admin': user_factory(role='admin'),
        'user': user_factory(role='user'),
        'guest': user_factory(role='guest'),
    }

# Mock fixtures
@pytest.fixture
def mock_stripe(mocker):
    """Mock Stripe API calls."""
    mock = mocker.patch('stripe.PaymentIntent.create')
    mock.return_value = {
        'id': 'pi_test_123',
        'status': 'succeeded',
        'amount': 1000,
    }
    return mock

@pytest.fixture
def mock_http_client(mocker):
    """Mock HTTP client for external API calls."""
    mock = mocker.patch('requests.Session.request')

    def configure_response(status_code=200, json_data=None):
        response = mocker.Mock()
        response.status_code = status_code
        response.json.return_value = json_data or {}
        mock.return_value = response
        return mock

    return configure_response

# Async fixtures (pytest-asyncio)
@pytest.fixture
async def async_client(app):
    """Async HTTP client for testing FastAPI."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# fixtures/data.py - Test data builders
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

@dataclass
class UserBuilder:
    email: str = field(default_factory=lambda: fake.email())
    name: str = field(default_factory=lambda: fake.name())
    role: str = 'user'

    def as_admin(self) -> 'UserBuilder':
        self.role = 'admin'
        return self

    def with_email(self, email: str) -> 'UserBuilder':
        self.email = email
        return self

    def build(self) -> dict:
        return {
            'email': self.email,
            'name': self.name,
            'role': self.role,
        }

@dataclass
class OrderBuilder:
    user_id: Optional[str] = None
    items: List[dict] = field(default_factory=list)
    status: str = 'pending'

    def with_items(self, *items) -> 'OrderBuilder':
        self.items.extend(items)
        return self

    def as_completed(self) -> 'OrderBuilder':
        self.status = 'completed'
        return self

    def build(self) -> dict:
        return {
            'user_id': self.user_id,
            'items': self.items,
            'status': self.status,
        }

# Usage in tests
def test_create_order(user_factory, db_session):
    user = user_factory()
    order_data = (
        OrderBuilder()
        .with_items({'product': 'Widget', 'quantity': 2})
        .build()
    )
    order_data['user_id'] = user.id

    order = Order(**order_data)
    db_session.add(order)
    db_session.commit()

    assert order.status == 'pending'
    assert len(order.items) == 1
```

### Database Test Isolation

```typescript
// Transactional tests - rollback after each test
import { PrismaClient } from '@prisma/client';

let prisma: PrismaClient;

beforeAll(() => {
  prisma = new PrismaClient();
});

beforeEach(async () => {
  // Start transaction
  await prisma.$executeRaw`BEGIN`;
});

afterEach(async () => {
  // Rollback transaction - clean slate for next test
  await prisma.$executeRaw`ROLLBACK`;
});

afterAll(async () => {
  await prisma.$disconnect();
});

// Alternative: Truncate tables
async function truncateAllTables() {
  const tables = ['order_items', 'orders', 'users'];
  for (const table of tables) {
    await prisma.$executeRawUnsafe(`TRUNCATE TABLE ${table} CASCADE`);
  }
}
```

---

## Common Mistakes to Avoid

### 1. Shared Mutable State Between Tests
```typescript
// BAD - shared state leaks between tests
const sharedUser = createUser();

test('test 1', () => {
  sharedUser.role = 'admin';  // Modifies shared state
});

test('test 2', () => {
  expect(sharedUser.role).toBe('user');  // FAILS!
});

// GOOD - create fresh data per test
test('test 1', () => {
  const user = createUser();
  user.role = 'admin';
});

test('test 2', () => {
  const user = createUser();
  expect(user.role).toBe('user');  // Works!
});
```

### 2. Not Cleaning Up After Tests
```typescript
// BAD - leaves test data in database
test('creates user', async () => {
  await prisma.user.create({ data: createUser() });
  // No cleanup - pollutes database
});

// GOOD - clean up in afterEach
afterEach(async () => {
  await prisma.user.deleteMany();
});
```

### 3. Hardcoded Test Data
```typescript
// BAD - hardcoded values make tests brittle
test('finds user by email', async () => {
  await createUser({ email: 'john@example.com' });
  const user = await findByEmail('john@example.com');
  expect(user).toBeDefined();
});

// GOOD - use generated data with reference
test('finds user by email', async () => {
  const testUser = await createUser();
  const user = await findByEmail(testUser.email);
  expect(user.id).toBe(testUser.id);
});
```

### 4. Over-Mocking
```typescript
// BAD - mocks everything, test doesn't verify real behavior
test('creates order', async () => {
  jest.mock('../db');
  jest.mock('../validation');
  jest.mock('../pricing');

  const result = await createOrder(data);
  expect(result).toBeDefined();  // What does this even test?
});

// GOOD - mock only external boundaries
test('creates order', async () => {
  mockStripeApi();  // Only mock external service

  const result = await createOrder(validOrderData);

  expect(result.status).toBe('pending');
  expect(await db.orders.findById(result.id)).toBeDefined();
});
```

### 5. Flaky Async Tests
```typescript
// BAD - race condition, might pass or fail
test('async operation completes', async () => {
  startAsyncOperation();
  expect(getResult()).toBeDefined();  // Might not be ready!
});

// GOOD - wait for completion
test('async operation completes', async () => {
  startAsyncOperation();
  await waitFor(() => getResult() !== undefined);
  expect(getResult()).toBeDefined();
});
```

---

## Validation Commands

```bash
# Run all tests with fixtures
npm test

# Run tests with coverage
npm test -- --coverage

# Check for test isolation issues (run tests in random order)
npm test -- --randomize

# Find tests without cleanup
grep -rn "afterEach\|afterAll" tests/ | wc -l

# Check for hardcoded test data
grep -rn "@test.com\|test123\|password" tests/

# Verify mock cleanup
grep -rn "mockReset\|mockClear\|nock.cleanAll" tests/
```

---

## Related Conventions

- **Isolation**: Each test MUST be independent and isolated
- **Cleanup**: Always clean up database/mock state after tests
- **Factories**: Use factory functions instead of hardcoded data
- **Naming**: Test files should mirror source files (user.ts → user.test.ts)
- **Coverage**: Maintain minimum 80% code coverage

---

## See Also

- [Database Patterns](database-patterns.md) - For database test setup
- [API Client](api-client.md) - For mocking API clients
- [Error Handling](error-handling.md) - For testing error scenarios
