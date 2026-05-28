# Test Generation with Claude Code

Patterns for generating quality unit, integration, and end-to-end tests.

## Test Generation Strategies

### Strategy 1: Analyze Then Generate

```
First, analyze this function and identify:
1. All code paths (branches, conditions)
2. Input validation requirements
3. Error conditions
4. Side effects

[paste code]

Then generate comprehensive tests.
```

### Strategy 2: Specification-Driven

```
Given this specification:
[paste spec or requirements]

Generate tests that verify each requirement is met.
Include test IDs that map to requirement IDs.
```

### Strategy 3: Behavior-Driven

```
Generate tests for [component] using Given-When-Then format:
- Given [precondition]
- When [action]
- Then [expected outcome]
```

## Unit Test Generation

### Prompt: Generate Unit Tests

```
Generate comprehensive unit tests for this function:

[paste function]

Include tests for:
- Normal operation (happy path)
- Edge cases (empty, null, boundaries)
- Error conditions (invalid input, exceptions)
- Return value verification
- Side effect verification (if any)

Use [Jest/Vitest/pytest] with [TypeScript/JavaScript/Python].
```

### Example: Testing a Utility Function

**Input:**
```typescript
function calculateDiscount(price: number, discountPercent: number): number {
  if (price < 0) throw new Error('Price cannot be negative');
  if (discountPercent < 0 || discountPercent > 100) {
    throw new Error('Discount must be between 0 and 100');
  }
  return price * (1 - discountPercent / 100);
}
```

**Generated Tests:**
```typescript
import { describe, it, expect } from 'vitest';
import { calculateDiscount } from './pricing';

describe('calculateDiscount', () => {
  describe('valid inputs', () => {
    it('should calculate 10% discount correctly', () => {
      expect(calculateDiscount(100, 10)).toBe(90);
    });

    it('should calculate 50% discount correctly', () => {
      expect(calculateDiscount(200, 50)).toBe(100);
    });

    it('should return original price for 0% discount', () => {
      expect(calculateDiscount(100, 0)).toBe(100);
    });

    it('should return 0 for 100% discount', () => {
      expect(calculateDiscount(100, 100)).toBe(0);
    });

    it('should handle decimal prices', () => {
      expect(calculateDiscount(99.99, 10)).toBeCloseTo(89.99, 2);
    });

    it('should handle decimal discounts', () => {
      expect(calculateDiscount(100, 33.33)).toBeCloseTo(66.67, 2);
    });
  });

  describe('edge cases', () => {
    it('should handle zero price', () => {
      expect(calculateDiscount(0, 50)).toBe(0);
    });

    it('should handle very small prices', () => {
      expect(calculateDiscount(0.01, 10)).toBeCloseTo(0.009, 3);
    });

    it('should handle very large prices', () => {
      expect(calculateDiscount(1000000, 10)).toBe(900000);
    });
  });

  describe('invalid inputs', () => {
    it('should throw for negative price', () => {
      expect(() => calculateDiscount(-100, 10))
        .toThrow('Price cannot be negative');
    });

    it('should throw for negative discount', () => {
      expect(() => calculateDiscount(100, -10))
        .toThrow('Discount must be between 0 and 100');
    });

    it('should throw for discount over 100', () => {
      expect(() => calculateDiscount(100, 150))
        .toThrow('Discount must be between 0 and 100');
    });
  });
});
```

## Integration Test Generation

### Prompt: API Integration Tests

```
Generate integration tests for this API endpoint:

Endpoint: [method] [path]
Request body: [schema]
Response: [schema]
Auth: [requirements]

Test scenarios:
- Successful request
- Validation errors
- Authentication failures
- Database errors
- Rate limiting

Use [supertest/axios] with [Jest/Vitest].
Include setup and teardown.
```

### Example: Testing a REST API

**Generated Tests:**
```typescript
import { describe, it, expect, beforeAll, afterAll, beforeEach } from 'vitest';
import request from 'supertest';
import { app } from '../app';
import { db } from '../database';
import { createTestUser, generateToken } from './helpers';

describe('POST /api/users', () => {
  let authToken: string;

  beforeAll(async () => {
    await db.connect();
    const admin = await createTestUser({ role: 'admin' });
    authToken = generateToken(admin);
  });

  afterAll(async () => {
    await db.disconnect();
  });

  beforeEach(async () => {
    await db.users.deleteMany({ email: /@test\.com$/ });
  });

  describe('successful creation', () => {
    it('should create user and return 201', async () => {
      const userData = {
        email: 'newuser@test.com',
        name: 'New User',
        password: 'SecurePass123!'
      };

      const response = await request(app)
        .post('/api/users')
        .set('Authorization', `Bearer ${authToken}`)
        .send(userData);

      expect(response.status).toBe(201);
      expect(response.body).toMatchObject({
        id: expect.any(String),
        email: userData.email,
        name: userData.name
      });
      expect(response.body).not.toHaveProperty('password');
    });

    it('should store user in database', async () => {
      const userData = {
        email: 'stored@test.com',
        name: 'Stored User',
        password: 'SecurePass123!'
      };

      await request(app)
        .post('/api/users')
        .set('Authorization', `Bearer ${authToken}`)
        .send(userData);

      const stored = await db.users.findOne({ email: userData.email });
      expect(stored).toBeDefined();
      expect(stored.name).toBe(userData.name);
    });
  });

  describe('validation errors', () => {
    it('should return 400 for invalid email', async () => {
      const response = await request(app)
        .post('/api/users')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          email: 'invalid-email',
          name: 'Test User',
          password: 'SecurePass123!'
        });

      expect(response.status).toBe(400);
      expect(response.body.errors).toContainEqual(
        expect.objectContaining({ field: 'email' })
      );
    });

    it('should return 400 for missing required fields', async () => {
      const response = await request(app)
        .post('/api/users')
        .set('Authorization', `Bearer ${authToken}`)
        .send({});

      expect(response.status).toBe(400);
      expect(response.body.errors.length).toBeGreaterThan(0);
    });

    it('should return 400 for weak password', async () => {
      const response = await request(app)
        .post('/api/users')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          email: 'user@test.com',
          name: 'Test User',
          password: '123'
        });

      expect(response.status).toBe(400);
      expect(response.body.errors).toContainEqual(
        expect.objectContaining({ field: 'password' })
      );
    });
  });

  describe('authentication', () => {
    it('should return 401 without auth token', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'user@test.com',
          name: 'Test User',
          password: 'SecurePass123!'
        });

      expect(response.status).toBe(401);
    });

    it('should return 401 with invalid token', async () => {
      const response = await request(app)
        .post('/api/users')
        .set('Authorization', 'Bearer invalid-token')
        .send({
          email: 'user@test.com',
          name: 'Test User',
          password: 'SecurePass123!'
        });

      expect(response.status).toBe(401);
    });
  });

  describe('conflict handling', () => {
    it('should return 409 for duplicate email', async () => {
      await createTestUser({ email: 'duplicate@test.com' });

      const response = await request(app)
        .post('/api/users')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          email: 'duplicate@test.com',
          name: 'Another User',
          password: 'SecurePass123!'
        });

      expect(response.status).toBe(409);
      expect(response.body.message).toContain('email');
    });
  });
});
```

## E2E Test Generation

### Prompt: Generate E2E Tests

```
Generate end-to-end tests for this user flow:

Flow: [describe flow]
Pages involved: [list pages]
User actions: [list actions]
Expected outcomes: [list outcomes]

Use [Playwright/Cypress] with [TypeScript/JavaScript].
Include:
- Page navigation
- Form interactions
- Assertions on UI state
- Error handling
- Accessibility checks (optional)
```

### Example: Testing a Login Flow

**Generated Tests (Playwright):**
```typescript
import { test, expect } from '@playwright/test';

test.describe('Login Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('should display login form', async ({ page }) => {
    await expect(page.getByRole('heading', { name: 'Login' })).toBeVisible();
    await expect(page.getByLabel('Email')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Sign In' })).toBeVisible();
  });

  test('should login successfully with valid credentials', async ({ page }) => {
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('validpassword');
    await page.getByRole('button', { name: 'Sign In' }).click();

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Welcome back')).toBeVisible();
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('wrongpassword');
    await page.getByRole('button', { name: 'Sign In' }).click();

    await expect(page.getByRole('alert')).toContainText('Invalid credentials');
    await expect(page).toHaveURL('/login');
  });

  test('should show validation error for invalid email', async ({ page }) => {
    await page.getByLabel('Email').fill('invalid-email');
    await page.getByLabel('Password').fill('password');
    await page.getByRole('button', { name: 'Sign In' }).click();

    await expect(page.getByText('Please enter a valid email')).toBeVisible();
  });

  test('should disable submit button while loading', async ({ page }) => {
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('validpassword');

    const submitButton = page.getByRole('button', { name: 'Sign In' });
    await submitButton.click();

    await expect(submitButton).toBeDisabled();
    await expect(page.getByText('Signing in...')).toBeVisible();
  });

  test('should navigate to forgot password page', async ({ page }) => {
    await page.getByRole('link', { name: 'Forgot password?' }).click();

    await expect(page).toHaveURL('/forgot-password');
    await expect(page.getByRole('heading', { name: 'Reset Password' })).toBeVisible();
  });

  test('should persist session after page reload', async ({ page }) => {
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('validpassword');
    await page.getByRole('button', { name: 'Sign In' }).click();

    await expect(page).toHaveURL('/dashboard');

    await page.reload();

    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Welcome back')).toBeVisible();
  });
});
```

## Framework-Specific Patterns

### Jest Patterns

```typescript
// Setup and teardown
beforeAll(() => { /* global setup */ });
afterAll(() => { /* global cleanup */ });
beforeEach(() => { /* test setup */ });
afterEach(() => { /* test cleanup */ });

// Assertions
expect(value).toBe(expected);           // Exact equality
expect(value).toEqual(expected);        // Deep equality
expect(value).toBeTruthy();             // Truthy check
expect(value).toContain(item);          // Array/string contains
expect(fn).toThrow(Error);              // Throws error
expect(fn).toHaveBeenCalledWith(args);  // Mock called with

// Async
await expect(promise).resolves.toBe(value);
await expect(promise).rejects.toThrow();

// Snapshots
expect(component).toMatchSnapshot();
expect(data).toMatchInlineSnapshot();
```

### Vitest Patterns

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mocking
vi.mock('./module');
const mockFn = vi.fn();
vi.spyOn(object, 'method');

// Fake timers
vi.useFakeTimers();
vi.advanceTimersByTime(1000);
vi.useRealTimers();

// Same assertions as Jest
expect(value).toBe(expected);
```

### pytest Patterns

```python
import pytest

# Fixtures
@pytest.fixture
def user():
    return User(name="Test User")

@pytest.fixture(scope="module")
def db():
    connection = create_connection()
    yield connection
    connection.close()

# Parametrized tests
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected

# Exception testing
def test_raises():
    with pytest.raises(ValueError, match="invalid"):
        validate("")

# Async tests
@pytest.mark.asyncio
async def test_async_operation():
    result = await async_function()
    assert result == expected
```

### Playwright Patterns

```typescript
// Locators (preferred)
page.getByRole('button', { name: 'Submit' });
page.getByLabel('Email');
page.getByText('Welcome');
page.getByTestId('submit-btn');

// Assertions
await expect(page).toHaveURL('/dashboard');
await expect(locator).toBeVisible();
await expect(locator).toHaveText('content');
await expect(locator).toBeDisabled();

// Actions
await locator.click();
await locator.fill('text');
await locator.selectOption('value');
await locator.check();

// Waiting
await page.waitForURL('/target');
await expect(locator).toBeVisible({ timeout: 10000 });
```

### Cypress Patterns

```typescript
// Commands
cy.visit('/page');
cy.get('[data-testid="element"]');
cy.contains('text');

// Assertions
cy.get('input').should('have.value', 'text');
cy.url().should('include', '/dashboard');
cy.get('.error').should('not.exist');

// Interactions
cy.get('input').type('text');
cy.get('button').click();
cy.get('select').select('option');

// API mocking
cy.intercept('GET', '/api/users', { fixture: 'users.json' });
```

## Generating Tests from Types

### TypeScript Types to Tests

```
Generate tests based on these TypeScript types:

[paste types]

Create tests that verify:
- Functions accept the correct input types
- Functions return the correct output types
- Required fields are enforced
- Optional fields work correctly
- Discriminated unions are handled
```

### Zod Schema to Tests

```
Generate tests based on this Zod schema:

[paste schema]

Test that validation:
- Accepts valid data
- Rejects invalid data with correct errors
- Handles all field constraints
- Transforms data correctly
```

## Test Data Generation

### Prompt: Generate Test Fixtures

```
Generate test fixtures for [entity]:

Schema:
[paste schema]

Generate:
- 5 valid examples
- Edge case examples (min/max values)
- Invalid examples with specific errors

Output as TypeScript objects.
```

### Factory Pattern

```
Create a test factory for [entity] that:
- Generates valid instances with defaults
- Allows overriding specific fields
- Supports building related entities

Example usage:
const user = userFactory.build({ name: 'Custom Name' });
const userWithPosts = userFactory.build({ posts: 3 });
```

## Test Quality Checklist

- [ ] Tests are independent (no shared mutable state)
- [ ] Tests are deterministic (same result every run)
- [ ] Tests are fast (mock slow operations)
- [ ] Tests are readable (clear names, AAA pattern)
- [ ] Tests cover happy path
- [ ] Tests cover error paths
- [ ] Tests cover edge cases
- [ ] Tests use appropriate assertion methods
- [ ] Tests clean up after themselves
- [ ] Tests don't depend on execution order

## Common Test Generation Prompts

### Generate Missing Tests

```
Analyze this test file and the source code it tests.
Identify test cases that are missing and generate them.

Test file:
[paste test file]

Source code:
[paste source code]
```

### Generate Tests from Examples

```
Given these example inputs and outputs:

Input: [example 1] -> Output: [result 1]
Input: [example 2] -> Output: [result 2]

Generate parameterized tests that verify each case.
Add additional edge cases you identify.
```

### Generate Regression Tests

```
This bug was fixed:
[describe bug and fix]

Generate regression tests that:
1. Would have caught this bug
2. Prevent it from recurring
3. Test related edge cases
```
