---
name: test-driven-development-workflow
description: Use this skill when implementing new features, fixing bugs, or refactoring code to enforce Test-Driven Development (TDD) principles, ensuring comprehensive test coverage of at least 80%.
---

# Test-Driven Development (TDD) Workflow

This skill ensures that all code development adheres to TDD principles and maintains comprehensive test coverage.

## When to Activate

- Implementing new features or functionalities
- Fixing bugs or issues
- Refactoring existing code
- Adding API endpoints
- Creating new components

## Core Principles

### 1. Write Tests Before Code
Always write tests first, then implement code to make the tests pass.

### 2. Coverage Requirements
- Minimum 80% coverage (unit + integration + E2E)
- Cover all edge cases
- Test error scenarios
- Validate boundary conditions

### 3. Types of Tests

#### Unit Tests
- Independent functions and utilities
- Component logic
- Pure functions
- Helper functions and utilities

#### Integration Tests
- API endpoints
- Database operations
- Service interactions
- External API calls

#### E2E Tests (Playwright)
- Key user flows
- Complete workflows
- Browser automation
- UI interactions

## TDD Workflow Steps

### Step 1: Write User Journeys
```
As a [role], I want to [action] so that [benefit]

Example:
As a user, I want to perform semantic market searches,
so that I can find relevant markets even without exact keywords.
```

### Step 2: Generate Test Cases
Create comprehensive test cases for each user journey:

```typescript
describe('Semantic Search', () => {
  it('returns relevant markets for query', async () => {
    // Test implementation
  });

  it('handles empty query gracefully', async () => {
    // Test edge case
  });

  it('falls back to substring search when Redis unavailable', async () => {
    // Test fallback behavior
  });

  it('sorts results by similarity score', async () => {
    // Test sorting logic
  });
});
```

### Step 3: Run Tests (They Should Fail)
```bash
npm test
# Tests should fail - we haven't implemented yet
```

### Step 4: Implement Code
Write the minimal code necessary to pass the tests:

```typescript
// Implementation guided by tests
export async function searchMarkets(query: string) {
  // Implementation here
}
```

### Step 5: Run Tests Again
```bash
npm test
# Tests should now pass
```

### Step 6: Refactor
Improve code quality while keeping tests green:
- Eliminate duplication
- Improve naming
- Optimize performance
- Enhance readability

### Step 7: Verify Coverage
```bash
npm run test:coverage
# Verify that coverage is 80%+
```

## Testing Patterns

### Unit Test Pattern (Jest/Vitest)
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button Component', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click</Button>);

    fireEvent.click(screen.getByRole('button'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### API Integration Test Pattern
```typescript
import { NextRequest } from 'next/server';
import { GET } from './route';

describe('GET /api/markets', () => {
  it('returns markets successfully', async () => {
    const request = new NextRequest('http://localhost/api/markets');
    const response = await GET(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data.success).toBe(true);
    expect(Array.isArray(data.data)).toBe(true);
  });

  it('validates query parameters', async () => {
    const request = new NextRequest('http://localhost/api/markets?limit=invalid');
    const response = await GET(request);

    expect(response.status).toBe(400);
  });

  it('handles database errors gracefully', async () => {
    // Simulate database failure
    const request = new NextRequest('http://localhost/api/markets');
    // Test error handling
  });
});
```

### E2E Test Pattern (Playwright)
```typescript
import { test, expect } from '@playwright/test';

test('user can search and filter markets', async ({ page }) => {
  await page.goto('/');
  await page.click('a[href="/markets"]');

  await expect(page.locator('h1')).toContainText('Markets');

  await page.fill('input[placeholder="Search markets"]', 'election');
  await page.waitForTimeout(600);

  const results = page.locator('[data-testid="market-card"]');
  await expect(results).toHaveCount(5, { timeout: 5000 });

  const firstResult = results.first();
  await expect(firstResult).toContainText('election', { ignoreCase: true });

  await page.click('button:has-text("Active")');
  await expect(results).toHaveCount(3);
});

test('user can create a new market', async ({ page }) => {
  await page.goto('/creator-dashboard');

  await page.fill('input[name="name"]', 'Test Market');
  await page.fill('textarea[name="description"]', 'Test description');
  await page.fill('input[name="endDate"]', '2025-12-31');

  await page.click('button[type="submit"]');

  await expect(page.locator('text=Market created successfully')).toBeVisible();
  await expect(page).toHaveURL(/\/markets\/test-market/);
});
```

## Test File Organization

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx          # Unit test
│   │   └── Button.stories.tsx       # Storybook
│   └── MarketCard/
│       ├── MarketCard.tsx
│       └── MarketCard.test.tsx
├── app/
│   └── api/
│       └── markets/
│           ├── route.ts
│           └── route.test.ts         # Integration test
└── e2e/
    ├── markets.spec.ts               # E2E test
    ├── trading.spec.ts
    └── auth.spec.ts
```

## Mocking External Services

### Supabase Mock
```typescript
jest.mock('@/lib/supabase', () => ({
  supabase: {
    from: jest.fn(() => ({
      select: jest.fn(() => ({
        eq: jest.fn(() => Promise.resolve({
          data: [{ id: 1, name: 'Test Market' }],
          error: null
        }))
      }))
    }))
  }
}));
```

### Redis Mock
```typescript
jest.mock('@/lib/redis', () => ({
  searchMarketsByVector: jest.fn(() => Promise.resolve([
    { slug: 'test-market', similarity_score: 0.95 }
  ])),
  checkRedisHealth: jest.fn(() => Promise.resolve({ connected: true }))
}));
```

### OpenAI Mock
```typescript
jest.mock('@/lib/openai', () => ({
  generateEmbedding: jest.fn(() => Promise.resolve(
    new Array(1536).fill(0.1) // Simulate 1536-dimensional embedding
  ))
}));
```

## Test Coverage Verification

### Run Coverage Report
```bash
npm run test:coverage
```

### Coverage Threshold
```json
{
  "jest": {
    "coverageThresholds": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

## Common Testing Errors to Avoid

### ❌ Error: Testing Implementation Details
```typescript
// Do not test internal state
expect(component.state.count).toBe(5);
```

### ✅ Correct: Testing User-Visible Behavior
```typescript
// Test what the user sees
expect(screen.getByText('Count: 5')).toBeInTheDocument();
```

### ❌ Error: Fragile Selectors
```typescript
// Prone to breakage
await page.click('.css-class-xyz');
```

### ✅ Correct: Semantic Selectors
```typescript
// Resilient to changes
await page.click('button:has-text("Submit")');
await page.click('[data-testid="submit-button"]');
```

### ❌ Error: No Test Isolation
```typescript
// Tests dependent on each other
test('creates user', () => { /* ... */ });
test('updates same user', () => { /* depends on previous test */ });
```

### ✅ Correct: Independent Tests
```typescript
// Each test sets up its own data
test('creates user', () => {
  const user = createTestUser();
  // Test logic
});

test('updates user', () => {
  const user = createTestUser();
  // Update logic
});
```

## Continuous Testing

### Watch Mode During Development
```bash
npm test -- --watch
# Automatically run tests on file changes
```

### Pre-Commit Hook
```bash
# Run before each commit
npm test && npm run lint
```

### CI/CD Integration
```yaml
# GitHub Actions
- name: Run Tests
  run: npm test -- --coverage
- name: Upload Coverage
  uses: codecov/codecov-action@v3
```

## Best Practices

1. **Write Tests First** - Always adhere to TDD.
2. **One Assertion Per Test** - Focus on a single behavior.
3. **Descriptive Test Names** - Explain what the test does.
4. **Arrange-Act-Assert Structure** - Clear test structure.
5. **Mock External Dependencies** - Isolate unit tests.
6. **Test Edge Cases** - Null, undefined, empty, large values.
7. **Test Error Paths** - Not just happy paths.
8. **Keep Tests Fast** - Unit tests under 50ms each.
9. **Clean Up After Tests** - No side effects.
10. **Review Coverage Reports** - Identify gaps.

## Success Metrics

- Achieve 80%+ code coverage.
- All tests pass (green).
- No skipped or disabled tests.
- Fast test execution (unit tests < 30 seconds).
- E2E tests cover key user flows.
- Tests catch bugs before production.

---

**Remember**: Testing is not optional. They are the safety net that supports confident refactoring, rapid development, and production reliability.