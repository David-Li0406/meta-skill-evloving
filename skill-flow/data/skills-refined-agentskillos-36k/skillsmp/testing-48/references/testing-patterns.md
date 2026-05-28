# Testing Patterns Reference

Comprehensive testing patterns for different testing scenarios.

## Unit Testing Patterns

### Arrange-Act-Assert (AAA)
```javascript
test('calculates order total with discount', () => {
  // Arrange
  const items = [
    { price: 100, quantity: 2 },
    { price: 50, quantity: 1 }
  ];
  const discount = 0.1;

  // Act
  const total = calculateOrderTotal(items, discount);

  // Assert
  expect(total).toBe(225); // (200 + 50) * 0.9
});
```

### Given-When-Then (BDD Style)
```javascript
describe('Order Calculator', () => {
  describe('given items with a discount', () => {
    const items = [{ price: 100, quantity: 2 }];
    const discount = 0.1;

    describe('when calculating total', () => {
      const total = calculateOrderTotal(items, discount);

      it('then applies discount to sum', () => {
        expect(total).toBe(180);
      });
    });
  });
});
```

### Test Doubles

#### Stub - Returns predetermined values
```javascript
const userService = {
  getUser: jest.fn().mockReturnValue({ id: 1, name: 'Test User' })
};
```

#### Mock - Verifies interactions
```javascript
const emailService = {
  sendEmail: jest.fn()
};

await registerUser(userData);

expect(emailService.sendEmail).toHaveBeenCalledWith(
  expect.objectContaining({ to: userData.email })
);
```

#### Fake - Working implementation for testing
```javascript
class FakeUserRepository {
  private users = new Map();

  async save(user) {
    this.users.set(user.id, user);
    return user;
  }

  async findById(id) {
    return this.users.get(id) || null;
  }
}
```

#### Spy - Records calls while using real implementation
```javascript
const spy = jest.spyOn(analytics, 'track');
doSomething();
expect(spy).toHaveBeenCalledWith('action', expect.any(Object));
spy.mockRestore();
```

## Integration Testing Patterns

### Database Testing with Transactions
```javascript
describe('UserRepository', () => {
  let connection;

  beforeAll(async () => {
    connection = await createConnection(testConfig);
  });

  beforeEach(async () => {
    await connection.beginTransaction();
  });

  afterEach(async () => {
    await connection.rollback();
  });

  afterAll(async () => {
    await connection.close();
  });

  test('creates user in database', async () => {
    const repo = new UserRepository(connection);
    const user = await repo.create({ name: 'Test' });

    const found = await repo.findById(user.id);
    expect(found.name).toBe('Test');
  });
});
```

### API Testing with Supertest
```javascript
import request from 'supertest';
import app from '../app';

describe('POST /api/users', () => {
  test('creates user and returns 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Test', email: 'test@example.com' })
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(Number),
      name: 'Test',
      email: 'test@example.com'
    });
  });

  test('returns 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Test', email: 'invalid' })
      .expect(400);

    expect(response.body.error).toContain('email');
  });
});
```

### Testcontainers Pattern
```javascript
import { PostgreSqlContainer } from '@testcontainers/postgresql';

describe('Database integration', () => {
  let container;
  let db;

  beforeAll(async () => {
    container = await new PostgreSqlContainer().start();
    db = await connectToDatabase(container.getConnectionUri());
    await runMigrations(db);
  });

  afterAll(async () => {
    await db.close();
    await container.stop();
  });

  test('performs database operations', async () => {
    // Test with real database
  });
});
```

## E2E Testing Patterns

### Page Object Model
```javascript
// pages/LoginPage.js
class LoginPage {
  constructor(page) {
    this.page = page;
    this.emailInput = page.locator('[data-testid="email"]');
    this.passwordInput = page.locator('[data-testid="password"]');
    this.submitButton = page.locator('[data-testid="login-submit"]');
  }

  async login(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async getErrorMessage() {
    return this.page.locator('[data-testid="error"]').textContent();
  }
}

// tests/login.spec.js
test('successful login redirects to dashboard', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await page.goto('/login');

  await loginPage.login('user@example.com', 'password123');

  await expect(page).toHaveURL('/dashboard');
});
```

### Fixtures and Setup
```javascript
// fixtures.js
import { test as base } from '@playwright/test';

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
    await use(page);
  },

  testUser: async ({}, use) => {
    const user = await createTestUser();
    await use(user);
    await deleteTestUser(user.id);
  }
});

// tests/dashboard.spec.js
test('shows user data on dashboard', async ({ authenticatedPage, testUser }) => {
  await expect(authenticatedPage.locator('.welcome')).toContainText(testUser.name);
});
```

## Snapshot Testing

### Component Snapshots
```javascript
test('renders user card correctly', () => {
  const { container } = render(<UserCard user={testUser} />);
  expect(container).toMatchSnapshot();
});
```

### API Response Snapshots
```javascript
test('GET /api/products returns expected structure', async () => {
  const response = await request(app).get('/api/products');
  expect(response.body).toMatchSnapshot();
});
```

### Inline Snapshots
```javascript
test('formats currency correctly', () => {
  expect(formatCurrency(1234.5)).toMatchInlineSnapshot(`"$1,234.50"`);
});
```

## Property-Based Testing

### With fast-check (JavaScript)
```javascript
import fc from 'fast-check';

test('parseJson(toJson(x)) === x for any valid object', () => {
  fc.assert(
    fc.property(fc.jsonValue(), (value) => {
      const json = JSON.stringify(value);
      const parsed = JSON.parse(json);
      expect(parsed).toEqual(value);
    })
  );
});

test('sort is idempotent', () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      const sorted = [...arr].sort((a, b) => a - b);
      const sortedTwice = [...sorted].sort((a, b) => a - b);
      expect(sortedTwice).toEqual(sorted);
    })
  );
});
```

## Mutation Testing

### Concept
Mutation testing modifies code and checks if tests catch the changes.

```javascript
// Original
function isAdult(age) {
  return age >= 18;
}

// Mutations generated:
return age > 18;   // Boundary mutation
return age <= 18;  // Negation mutation
return true;       // Return value mutation
```

### Tools
- **JavaScript**: Stryker
- **Python**: mutmut
- **Java**: PIT
- **Go**: go-mutesting

## Contract Testing

### Consumer-Driven Contracts (Pact)
```javascript
// Consumer test
describe('User API consumer', () => {
  test('gets user by ID', async () => {
    await provider.addInteraction({
      state: 'user with ID 1 exists',
      uponReceiving: 'a request for user 1',
      withRequest: {
        method: 'GET',
        path: '/users/1'
      },
      willRespondWith: {
        status: 200,
        body: {
          id: 1,
          name: Matchers.string('John')
        }
      }
    });

    const user = await userClient.getUser(1);
    expect(user.name).toBeDefined();
  });
});
```

## Test Data Patterns

### Factory Pattern
```javascript
// factories/user.js
let idCounter = 1;

export function createUser(overrides = {}) {
  return {
    id: idCounter++,
    name: `User ${idCounter}`,
    email: `user${idCounter}@test.com`,
    createdAt: new Date(),
    ...overrides
  };
}

// Usage
const user = createUser({ name: 'Custom Name' });
```

### Builder Pattern
```javascript
class UserBuilder {
  constructor() {
    this.user = {
      id: 1,
      name: 'Default',
      email: 'default@test.com',
      role: 'user'
    };
  }

  withName(name) {
    this.user.name = name;
    return this;
  }

  withRole(role) {
    this.user.role = role;
    return this;
  }

  asAdmin() {
    this.user.role = 'admin';
    return this;
  }

  build() {
    return { ...this.user };
  }
}

// Usage
const admin = new UserBuilder().withName('Admin').asAdmin().build();
```

### Mother Pattern
```javascript
// testMothers/OrderMother.js
export const OrderMother = {
  typical() {
    return {
      id: 'order-1',
      items: [{ productId: 'prod-1', quantity: 1, price: 100 }],
      status: 'pending',
      total: 100
    };
  },

  empty() {
    return { ...this.typical(), items: [], total: 0 };
  },

  completed() {
    return { ...this.typical(), status: 'completed' };
  },

  withDiscount(discount) {
    const order = this.typical();
    order.discount = discount;
    order.total = order.total * (1 - discount);
    return order;
  }
};
```

## Flaky Test Diagnosis

### Common Causes and Fixes

| Cause | Symptom | Fix |
|-------|---------|-----|
| Race conditions | Passes locally, fails in CI | Use proper async/await, waitFor |
| Time dependency | Fails at certain times | Mock Date/Time |
| Order dependency | Fails when run individually | Ensure test isolation |
| Resource exhaustion | Fails after many tests | Clean up resources |
| Network calls | Intermittent failures | Mock external services |
| Random data | Unpredictable failures | Seed random generators |

### Detection Script
```bash
#!/bin/bash
# Run test multiple times to detect flakiness
for i in {1..10}; do
  npm test -- --testNamePattern="suspicious test" || echo "Failed on run $i"
done
```

## Test Organization Anti-Patterns

### Avoid: God Test File
```
tests/
  everything.test.js  # 5000 lines, tests everything
```

### Prefer: Organized by Feature
```
tests/
  unit/
    auth/
      login.test.js
      logout.test.js
    users/
      create.test.js
      update.test.js
  integration/
    api/
      auth.test.js
      users.test.js
```

### Avoid: Test Inheritance
```javascript
// BAD: Complex inheritance
class BaseTest { ... }
class UserTest extends BaseTest { ... }
class AdminUserTest extends UserTest { ... }
```

### Prefer: Composition
```javascript
// GOOD: Shared utilities
const { createAuthenticatedUser, cleanupUsers } = require('./helpers');
```
