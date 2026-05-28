---
name: testing-patterns
description: Comprehensive guide for writing unit tests, integration tests, and E2E tests using Vitest, Playwright, and React Testing Library.
---

# Testing Patterns & Best Practices

## Overview

This skill provides a comprehensive guide for testing strategies focusing on Vitest for unit/integration tests and Playwright for E2E tests. Use this when writing tests, setting up test infrastructure, or debugging test failures.

## Testing Principles

### 1. Test Behavior, Not Implementation
- Focus on what the code does, not how it does it.
- Tests shouldn't break when refactoring.
- Concentrate on inputs and outputs.

### 2. Arrange-Act-Assert (AAA)
```typescript
// Arrange - Set up test data
const user = { name: 'John', email: 'john@example.com' };

// Act - Execute the code
const result = validateUser(user);

// Assert - Verify the outcome
expect(result.isValid).toBe(true);
```

### 3. Test Isolation
- Each test should be independent.
- No shared state between tests.
- Clean up after each test.

## Test Stack

| Tool                  | Purpose                | Config                 |
| --------------------- | ---------------------- | ---------------------- |
| Vitest                | Unit/integration tests | `vitest.config.ts`     |
| React Testing Library | Component tests        | Via Vitest             |
| Playwright            | E2E tests              | `playwright.config.ts` |
| jsdom                 | DOM environment        | Vitest config          |

## Unit Testing Patterns

### Basic Test Structure
```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';

describe('UserService', () => {
  let service: UserService;

  beforeEach(() => {
    service = new UserService();
    vi.clearAllMocks();
  });

  it('creates user with valid data', async () => {
    const user = await service.create({ email: 'test@example.com' });
    expect(user).toMatchObject({ email: 'test@example.com' });
  });

  it('throws on duplicate email', async () => {
    await service.create({ email: 'test@example.com' });
    await expect(service.create({ email: 'test@example.com' }))
      .rejects.toThrow('already exists');
  });
});
```

### Mocking Patterns
```typescript
// Mock a module
vi.mock('@/lib/db', () => ({
  db: {
    user: {
      create: vi.fn(),
      findUnique: vi.fn(),
    },
  },
}));

// Mock implementation per test
it('handles not found', async () => {
  vi.mocked(db.user.findUnique).mockResolvedValue(null);
  await expect(getUser('123')).rejects.toThrow('Not found');
});
```

## React Testing Library Patterns

### Component Testing
```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

it('submits form with valid data', async () => {
  const onSubmit = vi.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  await userEvent.type(screen.getByLabelText(/email/i), 'test@example.com');
  await userEvent.type(screen.getByLabelText(/password/i), 'password123');
  await userEvent.click(screen.getByRole('button', { name: /submit/i }));

  await waitFor(() => {
    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });
});
```

## Playwright E2E Patterns

### Page Object Model
```typescript
// tests/pages/login.page.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('[name="email"]', email);
    await this.page.fill('[name="password"]', password);
    await this.page.click('button[type="submit"]');
  }

  async expectError(message: string) {
    await expect(this.page.getByText(message)).toBeVisible();
  }
}

// tests/auth.spec.ts
test('user can login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@example.com', 'password');
  await expect(page).toHaveURL('/dashboard');
});
```

## Test Organization
```
tests/
├── unit/              # Pure function tests
├── integration/       # Component + dependency tests
├── e2e/              # Playwright tests
│   ├── fixtures/
│   ├── pages/        # Page objects
│   └── *.spec.ts
└── setup.ts          # Global setup
```

## Coverage Requirements
- Aim for meaningful coverage on new code.
- Run `yarn test:coverage` to check.
- Focus on critical paths (filters, URLs, API calls).

## Checklist Before Writing Tests
- [ ] Unit test in `test/` directory?
- [ ] E2E test in `e2e/` directory?
- [ ] Using correct file naming convention?
- [ ] Mocking external dependencies?
- [ ] Testing both success and error cases?
- [ ] Running `yarn test` before committing?

## Anti-Patterns to Avoid
- Testing implementation details.
- No test isolation leading to flaky tests.
- Hardcoded delays instead of waiting for conditions.
- Mocking everything, making tests meaningless.