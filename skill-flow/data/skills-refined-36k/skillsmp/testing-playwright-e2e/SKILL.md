---
name: testing-playwright-e2e
description: >
  Writes end-to-end tests with Playwright for the layered Express API.
  To be used for writing tests that validate the full HTTP stack, acceptance criteria, and business logic.
---

# Playwright E2E Testing Skill

Write end-to-end tests with Playwright that validate the complete API stack, from HTTP layer through business logic to data storage. Tests verify acceptance criteria, HTTP contracts, and boundary conditions.

## Testing the Layered Architecture

The AstroBookings API uses a layered architecture with clear HTTP contracts:

```
HTTP Request → Routes Layer (validation, status codes) → 
  Services Layer (business logic) → Data Storage → HTTP Response
```

Tests validate each layer's behavior:
- **HTTP Layer**: Status codes (201, 200, 204, 400, 404), response format
- **Service Layer**: Business logic, validation rules, error handling
- **Data Flow**: Request transforms through layers to response

## Project Structure

Organize tests by technical layer, mirroring the API structure:

```
tests/
├── smoke.spec.ts           # Basic health and connectivity checks
└── resource.spec.ts        # Resource-specific tests (rockets, launches, etc.)

specs/
└── resource.spec.md        # Human-readable acceptance criteria
```

### File Naming
- Use kebab-case with `.spec.ts` suffix: `rockets.spec.ts`, `launches.spec.ts`
- Create one test file per API resource
- Mirror the routes layer structure for clarity

## Test Structure

### Test Suites with describe()

Organize tests into logical suites grouped by HTTP method and business context:

```typescript
describe('Rockets - HTTP Endpoints', () => {
  // Tests for GET, POST, PUT, DELETE operations
});

describe('Rockets - Validation', () => {
  // Tests for validation rules and error cases
});

describe('Rockets - Business Logic', () => {
  // Tests for domain-specific rules and constraints
});
```

### Test Cases with test()

Each test case focuses on a single scenario:

```typescript
test('POST /rockets returns 201 with created rocket', async ({ request }) => {
  // Arrange, Act, Assert
});

test('GET /rockets/:id returns 404 when rocket does not exist', async ({ request }) => {
  // Arrange, Act, Assert
});
```

## Test Patterns

### Arrange-Act-Assert (AAA) Pattern

Structure each test with three clear phases:

```typescript
test('PUT /rockets/:id updates rocket and returns 200', async ({ request }) => {
  // Arrange: Set up initial state
  const created = await request.post('/rockets', {
    data: { name: 'Falcon', price: 50_000_000 }
  });
  const rocketId = (await created.json()).id;

  // Act: Perform the action being tested
  const response = await request.put(`/rockets/${rocketId}`, {
    data: { name: 'Falcon Heavy', price: 90_000_000 }
  });

  // Assert: Verify expected outcomes
  expect(response.status()).toBe(200);
  const body = await response.json();
  expect(body.name).toBe('Falcon Heavy');
  expect(body.price).toBe(90_000_000);
});
```

### HTTP Contracts

Test that endpoints return correct status codes for each scenario:

| Method | Success | Validation Error | Not Found | Status |
|--------|---------|------------------|-----------|--------|
| POST   | 201     | 400              | N/A       | Created |
| GET    | 200     | N/A              | 404       | OK |
| PUT    | 200     | 400              | 404       | OK |
| DELETE | 204     | N/A              | 404       | No Content |

### Validation Error Format

Validate that error responses match the expected structure:

```typescript
test('POST /rockets with invalid data returns 400 with error array', async ({ request }) => {
  const response = await request.post('/rockets', {
    data: { name: '' } // Invalid: empty name
  });

  expect(response.status()).toBe(400);
  const body = await response.json();
  expect(Array.isArray(body.errors)).toBe(true);
  expect(body.errors[0]).toHaveProperty('field');
  expect(body.errors[0]).toHaveProperty('message');
});
```

### Acceptance Criteria Tests

Map tests directly to requirements in `specs/resource.spec.md`:

```typescript
describe('Rockets - Acceptance Criteria', () => {
  test('User can create a rocket with valid data', async ({ request }) => {
    // Maps to spec: "User can add a new rocket with required properties"
  });

  test('System prevents duplicate rocket names', async ({ request }) => {
    // Maps to spec: "System ensures rocket names are unique"
  });

  test('User can list all rockets sorted by creation date', async ({ request }) => {
    // Maps to spec: "System returns all rockets in order"
  });
});
```

### Boundary Testing

Test edge cases and limits:

```typescript
describe('Rockets - Boundaries', () => {
  test('Handles minimum valid price', async ({ request }) => {
    const response = await request.post('/rockets', {
      data: { name: 'Micro', price: 1 }
    });
    expect(response.status()).toBe(201);
  });

  test('Rejects negative price', async ({ request }) => {
    const response = await request.post('/rockets', {
      data: { name: 'Invalid', price: -1000 }
    });
    expect(response.status()).toBe(400);
  });

  test('Handles very long names', async ({ request }) => {
    const longName = 'A'.repeat(1000);
    const response = await request.post('/rockets', {
      data: { name: longName, price: 1000000 }
    });
    // Assert behavior matches spec
  });
});
```

### Service Layer Validation

Test that business rules are enforced:

```typescript
test('Service validates all required fields before creation', async ({ request }) => {
  const response = await request.post('/rockets', {
    data: { name: 'Falcon' } // Missing: price
  });

  expect(response.status()).toBe(400);
  const body = await response.json();
  expect(body.errors.some((e: any) => e.field === 'price')).toBe(true);
});

test('Service returns multiple validation errors in single response', async ({ request }) => {
  const response = await request.post('/rockets', {
    data: {} // Missing: name, price
  });

  expect(response.status()).toBe(400);
  const body = await response.json();
  expect(body.errors.length).toBeGreaterThanOrEqual(2);
});
```

## Running Tests

### Setup

Ensure the server is running before tests execute:

```bash
# Terminal 1: Start the server
npm run dev

# Terminal 2: Run tests
npm run test
```

### Commands

```bash
# Run all tests
npm run test

# Run tests in UI mode (interactive debugging)
npm run test:ui

# Run specific test file
npx playwright test tests/rockets.spec.ts

# Run tests matching a pattern
npx playwright test --grep "Validation"

# Run with verbose output
npx playwright test --reporter=verbose
```

### Test Lifecycle

1. **Before All**: Server should be running
2. **Each Test**: Independent, uses fresh HTTP requests
3. **After All**: Server should remain running for next test run
4. **Cleanup**: Stop server when all tests complete to free resources

## Best Practices

### Independence
- Each test should be independent and runnable in any order
- Avoid test interdependencies (don't rely on data from previous tests)
- Use unique data per test to prevent conflicts

### Clarity
- Use descriptive test names that explain what is being tested
- Include the HTTP method and path in test descriptions
- Clearly state the expected behavior

### Coverage
- Test all happy paths (successful operations)
- Test all validation rules (error cases)
- Test boundary conditions (edge cases)
- Test all HTTP status code scenarios

### Maintainability
- Keep tests focused on a single behavior
- Avoid complex test logic; use simple, linear flows
- Use helper functions for repeated setup (e.g., creating test data)
- Comment non-obvious test logic

### Data Management
- Use in-memory storage for test isolation
- Reset data between test runs (server restart between runs)
- Create unique test data to avoid conflicts
- Don't assume data persistence across tests
  