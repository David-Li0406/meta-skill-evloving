# Test Pyramid & Strategy Guide

Practical guide to structuring tests for maximum effectiveness.

## The Test Pyramid

```
        /\
       /  \      E2E Tests (few, slow, expensive)
      /----\
     /      \    Integration Tests (some)
    /--------\
   /          \  Unit Tests (many, fast, cheap)
  /____________\
```

### Recommended Ratios

| Type | Percentage | Speed | Scope |
|------|------------|-------|-------|
| Unit | 70% | < 10ms | Single function/class |
| Integration | 20% | < 1s | Multiple components |
| E2E | 10% | > 1s | Full system |

## Unit Tests

### What to Test
- Pure functions with business logic
- Edge cases and boundary conditions
- Error handling paths
- Complex algorithms

### Example Structure

```typescript
// user-service.test.ts
describe('UserService', () => {
  describe('validateEmail', () => {
    it('should accept valid email', () => {
      expect(validateEmail('user@example.com')).toBe(true);
    });

    it('should reject email without @', () => {
      expect(validateEmail('userexample.com')).toBe(false);
    });

    it('should reject email without domain', () => {
      expect(validateEmail('user@')).toBe(false);
    });

    it('should handle null/undefined', () => {
      expect(validateEmail(null)).toBe(false);
      expect(validateEmail(undefined)).toBe(false);
    });
  });
});
```

### Unit Test Best Practices

```typescript
// ❌ BAD: Testing implementation details
it('should call _privateMethod', () => {
  const spy = jest.spyOn(service, '_privateMethod');
  service.process();
  expect(spy).toHaveBeenCalled();
});

// ✅ GOOD: Testing behavior
it('should return processed result', () => {
  const result = service.process(input);
  expect(result).toEqual(expectedOutput);
});

// ❌ BAD: Multiple assertions testing different things
it('should work correctly', () => {
  expect(add(1, 2)).toBe(3);
  expect(subtract(5, 3)).toBe(2);
  expect(multiply(2, 4)).toBe(8);
});

// ✅ GOOD: One logical assertion per test
it('should add two numbers', () => {
  expect(add(1, 2)).toBe(3);
});
```

## Integration Tests

### What to Test
- Database operations
- API endpoints
- Service interactions
- External service integrations (with mocks)

### Example: API Integration Test

```typescript
describe('POST /api/users', () => {
  let app: Express;
  let db: Database;

  beforeAll(async () => {
    db = await createTestDatabase();
    app = createApp(db);
  });

  afterAll(async () => {
    await db.close();
  });

  beforeEach(async () => {
    await db.clear();  // Clean slate each test
  });

  it('should create user and return 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test User' });

    expect(response.status).toBe(201);
    expect(response.body).toMatchObject({
      email: 'test@example.com',
      name: 'Test User'
    });
    expect(response.body.id).toBeDefined();
  });

  it('should return 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'invalid', name: 'Test' });

    expect(response.status).toBe(400);
    expect(response.body.error).toContain('email');
  });

  it('should return 409 for duplicate email', async () => {
    await db.users.create({ email: 'test@example.com', name: 'Existing' });

    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'New User' });

    expect(response.status).toBe(409);
  });
});
```

### Database Integration Pattern

```typescript
// test-utils.ts
export async function withTestTransaction<T>(
  db: Database,
  fn: (tx: Transaction) => Promise<T>
): Promise<T> {
  const tx = await db.beginTransaction();
  try {
    const result = await fn(tx);
    await tx.rollback();  // Always rollback, even on success
    return result;
  } catch (error) {
    await tx.rollback();
    throw error;
  }
}

// user-repository.test.ts
it('should save user to database', async () => {
  await withTestTransaction(db, async (tx) => {
    const repo = new UserRepository(tx);
    const user = await repo.save({ email: 'test@example.com' });

    const found = await repo.findById(user.id);
    expect(found).toEqual(user);
  });
  // Transaction rolled back, no cleanup needed
});
```

## E2E Tests

### What to Test
- Critical user journeys
- Authentication flows
- Payment/checkout processes
- Cross-feature interactions

### Example: Playwright E2E Test

```typescript
// auth-flow.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('should allow user to sign up, login, and logout', async ({ page }) => {
    // Sign up
    await page.goto('/signup');
    await page.fill('[name="email"]', 'newuser@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="welcome"]')).toContainText('Welcome');

    // Logout
    await page.click('[data-testid="logout-button"]');
    await expect(page).toHaveURL('/');

    // Login
    await page.goto('/login');
    await page.fill('[name="email"]', 'newuser@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('/dashboard');
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'wrong@example.com');
    await page.fill('[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-message')).toBeVisible();
    await expect(page).toHaveURL('/login');
  });
});
```

## Test Coverage Guidelines

### Coverage Targets

| Type | Target | Critical Path |
|------|--------|---------------|
| Statement | 80% | 95% |
| Branch | 75% | 90% |
| Function | 85% | 95% |

### What NOT to Test for Coverage

```typescript
// ❌ Don't test just to hit coverage
it('should cover this line', () => {
  const obj = new MyClass();  // Just instantiation
  expect(obj).toBeDefined();
});

// ❌ Don't test getters/setters
it('should set name', () => {
  user.name = 'Test';
  expect(user.name).toBe('Test');
});

// ❌ Don't test framework code
it('should render component', () => {
  const { container } = render(<Button />);
  expect(container).toBeTruthy();
});
```

### Focus Coverage On

- Business logic functions
- Error handling paths
- Edge cases and boundary conditions
- Security-sensitive code

## Mocking Strategy

### When to Mock

| Mock | Don't Mock |
|------|------------|
| External APIs | Your own code |
| Database (in unit tests) | Pure functions |
| Time/dates | Simple dependencies |
| File system | In-memory alternatives |
| Network requests | Test doubles you control |

### Mock Examples

```typescript
// Mock external API
jest.mock('./payment-gateway', () => ({
  charge: jest.fn().mockResolvedValue({ success: true, id: 'ch_123' })
}));

// Mock time
beforeEach(() => {
  jest.useFakeTimers();
  jest.setSystemTime(new Date('2024-01-15T10:00:00Z'));
});

afterEach(() => {
  jest.useRealTimers();
});

// Mock with different responses
it('should handle payment failure', async () => {
  paymentGateway.charge.mockRejectedValueOnce(new Error('Card declined'));

  await expect(service.processOrder(order)).rejects.toThrow('Payment failed');
});
```

## Test Naming Conventions

```typescript
// Pattern: should [expected behavior] when [condition]
it('should return empty array when no users exist', () => {});
it('should throw ValidationError when email is invalid', () => {});
it('should send welcome email when user signs up', () => {});

// Or: [method] [expected behavior] [condition]
it('findById returns null for non-existent user', () => {});
it('createUser throws if email already exists', () => {});
```

## Test Organization

```
tests/
├── unit/
│   ├── services/
│   │   └── user-service.test.ts
│   └── utils/
│       └── validation.test.ts
├── integration/
│   ├── api/
│   │   └── users.test.ts
│   └── repositories/
│       └── user-repository.test.ts
├── e2e/
│   ├── auth.spec.ts
│   └── checkout.spec.ts
└── fixtures/
    ├── users.json
    └── orders.json
```
