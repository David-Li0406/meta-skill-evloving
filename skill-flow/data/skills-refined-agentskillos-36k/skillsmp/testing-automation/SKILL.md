---
name: Testing Automation
description: This skill should be used when the user asks to "write tests", "test automation", "E2E testing", "load testing", "performance testing", "chaos engineering", "test coverage", "integration tests", "unit tests", "Playwright", "Jest", "pytest", or needs help with testing strategies and automation.
version: 1.0.0
---

# Testing Automation

Comprehensive guidance for automated testing, performance testing, and chaos engineering.

## Testing Pyramid

```
       /\
      /  \     E2E Tests (few)
     /----\
    /      \   Integration Tests (some)
   /--------\
  /          \ Unit Tests (many)
 /____________\
```

## Unit Testing

### Jest (JavaScript)

```javascript
// user.test.js
describe('UserService', () => {
  let userService;

  beforeEach(() => {
    userService = new UserService(mockDb);
  });

  test('creates user with valid data', async () => {
    const user = await userService.create({
      email: 'test@example.com',
      name: 'Test User'
    });

    expect(user.id).toBeDefined();
    expect(user.email).toBe('test@example.com');
  });

  test('throws error for duplicate email', async () => {
    await userService.create({ email: 'test@example.com' });

    await expect(
      userService.create({ email: 'test@example.com' })
    ).rejects.toThrow('Email already exists');
  });
});
```

### pytest (Python)

```python
# test_user.py
import pytest
from services.user import UserService

@pytest.fixture
def user_service(mock_db):
    return UserService(mock_db)

def test_create_user_with_valid_data(user_service):
    user = user_service.create(
        email="test@example.com",
        name="Test User"
    )

    assert user.id is not None
    assert user.email == "test@example.com"

def test_duplicate_email_raises_error(user_service):
    user_service.create(email="test@example.com")

    with pytest.raises(ValueError, match="Email already exists"):
        user_service.create(email="test@example.com")
```

## E2E Testing

### Playwright

```javascript
// e2e/login.spec.js
import { test, expect } from '@playwright/test';

test.describe('Login Flow', () => {
  test('successful login redirects to dashboard', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[data-testid="email"]', 'user@example.com');
    await page.fill('[data-testid="password"]', 'password123');
    await page.click('[data-testid="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Welcome');
  });

  test('invalid credentials show error', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[data-testid="email"]', 'wrong@example.com');
    await page.fill('[data-testid="password"]', 'wrongpassword');
    await page.click('[data-testid="submit"]');

    await expect(page.locator('.error')).toBeVisible();
  });
});
```

## Load Testing

### k6

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },   // Ramp up
    { duration: '3m', target: 50 },   // Stay at 50 users
    { duration: '1m', target: 100 },  // Ramp up more
    { duration: '3m', target: 100 },  // Stay at 100 users
    { duration: '1m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

```bash
# Run load test
k6 run load-test.js

# Run with cloud output
k6 run --out cloud load-test.js
```

## Chaos Engineering

### Chaos Monkey Principles

1. Define steady state
2. Hypothesize about steady state continuity
3. Inject real-world events
4. Disprove hypothesis

### Litmus Chaos

```yaml
apiVersion: litmuschaos.io/v1alpha1
kind: ChaosExperiment
metadata:
  name: pod-delete
spec:
  definition:
    scope: Namespaced
    permissions:
      - apiGroups: [""]
        resources: ["pods"]
        verbs: ["delete"]
    env:
      - name: TOTAL_CHAOS_DURATION
        value: "30"
      - name: CHAOS_INTERVAL
        value: "10"
```

## Test Coverage

```bash
# JavaScript
npm test -- --coverage

# Python
pytest --cov=src --cov-report=html

# Go
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## CI Integration

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v4

  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
```

## Additional Resources

### Reference Files
- **`references/testing-patterns.md`** - Test pattern catalog
- **`references/mocking-strategies.md`** - Mocking best practices

### Example Files
- **`examples/playwright-config.ts`** - Playwright configuration
- **`examples/k6-scenarios/`** - Load test scenarios
