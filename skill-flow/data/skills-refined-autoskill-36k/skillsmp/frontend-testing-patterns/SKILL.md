---
name: frontend-testing-patterns
description: Provides comprehensive testing strategies and patterns for React applications. This skill should be used when writing tests, setting up testing infrastructure, or deciding what to test.
---

# Frontend Testing Patterns

This skill provides testing strategies and patterns for React applications, based on Bulletproof React best practices.

## Testing Philosophy

**Focus on integration tests over unit tests.** Integration tests provide more confidence that your application works correctly while being less brittle than unit tests.

> "Write tests. Not too many. Mostly integration." - Guillermo Rauch

## Testing Pyramid

```
         /\ 
        /  \
       /    \
      /      \
     /  E2E   \
    /----------\
   /            \
  /  Integration \
 /----------------\
/    Unit Tests    \
--------------------
```

**Distribution**:
- **70%** Integration tests - Test features as users would use them
- **20%** Unit tests - Test complex logic in isolation
- **10%** E2E tests - Test critical user flows

## Test Types

### 1. Integration Tests

**What**: Test components with their dependencies (hooks, context, API calls).

**When to use**:
- Testing user interactions
- Testing component behavior with real hooks
- Testing data fetching with mocked APIs

**Tools**:
- **Vitest** - Test runner (already configured in Eridu)
- **Testing Library** - Component testing utilities
- **MSW** (Mock Service Worker) - API mocking

**Example** (Component with API):

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import { UserProfile } from './UserProfile';

// Setup MSW server
const server = setupServer(
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'John Doe',
      email: 'john@example.com',
    });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('displays user profile after loading', async () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  render(
    <QueryClientProvider client={queryClient}>
      <UserProfile userId="123" />
    </QueryClientProvider>
  );

  // Loading state
  expect(screen.getByText(/loading/i)).toBeInTheDocument();

  // Wait for data to load
  await waitFor(() => {
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });

  expect(screen.getByText('john@example.com')).toBeInTheDocument();
});

test('handles error when user not found', async () => {
  // Override handler for this test
  server.use(
    http.get('/api/users/:id', () => {
      return new HttpResponse(null, { status: 404 });
    })
  );

  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  render(
    <QueryClientProvider client={queryClient}>
      <UserProfile userId="999" />
    </QueryClientProvider>
  );

  await waitFor(() => {
    expect(screen.getByText(/user not found/i)).toBeInTheDocument();
  });
});
```

**Example** (User Interaction):

```typescript
import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { CreateDiscussionForm } from './CreateDiscussionForm';

test('submits form with valid data', async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();

  render(<CreateDiscussionForm onSubmit={onSubmit} />);

  // Fill out form
  await user.type(screen.getByLabelText(/title/i), 'My Discussion');
  await user.type(screen.getByLabelText(/body/i), 'This is the discussion body');

  // Submit
  await user.click(screen.getByRole('button', { name: /create/i }));

  // Verify submission
  expect(onSubmit).toHaveBeenCalledWith({
    title: 'My Discussion',
    body: 'This is the discussion body',
  });
});

test('shows validation errors for invalid data', async () => {
  const user = userEvent.setup();

  render(<CreateDiscussionForm onSubmit={vi.fn()} />);

  // Submit without filling form
  await user.click(screen.getByRole('button', { name: /create/i }));

  // Verify validation errors
  expect(screen.getByText(/title is required/i)).toBeInTheDocument();
  expect(screen.getByText(/body must be at least 10 characters/i)).toBeInTheDocument();
});
```

### 2. Unit Tests

**What**: Test individual functions or hooks in isolation.

**When to use**:
- Complex utility functions
- Custom hooks with complex logic
- Business logic functions

**Example** (Utility Function):

```typescript
// src/utils/format-date.ts
export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(date);
}

// src/utils/format-date.test.ts
import { formatDate } from './format-date';

test('formats date correctly', () => {
  const date = new Date('2024-01-15');
  expect(formatDate(date)).toBe('January 15, 2024');
});
```

**Example** (Custom Hook):

```typescript
// src/hooks/useDebounce.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { useDebounce } from './useDebounce';

test('debounces value', async () => {
  const { result, rerender } = renderHook(
    ({ value, delay }) => useDebounce(value, delay),
    {
      initialProps: { value: 'initial', delay: 500 },
    }
  );

  expect(result.current).toBe('initial');

  // Update value
  rerender({ value: 'updated', delay: 500 });

  // Value should not change immediately
  expect(result.current).toBe('initial');

  // Wait for debounce
  await waitFor(
    () => {
      expect(result.current).toBe('updated');
    },
    { timeout: 600 }
  );
});
```

### 3. E2E Tests

**What**: Test complete user flows in a real browser.

**When to use**:
- Critical user flows (login, checkout, etc.)
- Cross-page interactions
- Testing with real backend

**Tools**:
- **Playwright** - Modern E2E testing framework
- **Cypress** - Alternative E2E framework

**Example** (Playwright):

```typescript
// tests/e2e/login.spec.ts
import { test, expect } from '@playwright/test';

test('user can log in', async ({ page }) => {
  // Navigate to login page
  await page.goto('/login');

  // Fill in credentials
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('password123');

  // Submit form
  await page.getByRole('button', { name: /log in/i }).click();

  // Verify redirect to dashboard
  await expect(page).toHaveURL('/dashboard');

  // Verify user is logged in
  await expect(page.getByText(/welcome back/i)).toBeVisible();
});

test('shows error for invalid credentials', async ({ page }) => {
  await page.goto('/login');

  await page.getByLabel('Email').fill('wrong@example.com');
  await page.getByLabel('Password').fill('wrongpassword');

  await page.getByRole('button', { name: /log in/i }).click();

  // Verify error message
  await expect(page.getByText(/invalid email or password/i)).toBeVisible();

  // Verify still on login page
  await expect(page).toHaveURL('/login');
});
```

## Test Organization

### Colocation

Keep tests close to the code they test:

```
src/features/discussions/
├── components/
│   ├── DiscussionList.tsx
│   ├── DiscussionList.test.tsx
│   ├── DiscussionForm.tsx
│   └── DiscussionForm.test.tsx
├── api/
│   ├── get-discussions.ts
│   └── get-discussions.test.ts
└── utils/
    ├── format-discussion.ts
    └── format-discussion.test.ts
```

### Test Utilities

Create shared test utilities:

```typescript
// src/testing/test-utils.tsx
import { render, type RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { type ReactElement } from 'react';

// Create wrapper with common providers
function AllTheProviders({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

// Custom render function
export function renderWithProviders(
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { wrapper: AllTheProviders, ...options });
}

// Re-export everything
export * from '@testing-library/react';
```

**Usage**:

```typescript
import { renderWithProviders, screen } from '@/testing/test-utils';

test('my test', () => {
  renderWithProviders(<MyComponent />);
  // ...
});
```

## API Mocking with MSW

**Setup** (`src/testing/mocks/server.ts`):

```typescript
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

**Handlers** (`src/testing/mocks/handlers.ts`):

```typescript
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/discussions', () => {
    return HttpResponse.json({
      data: [
        { id: '1', title: 'Discussion 1', body: 'Body 1' },
        { id: '2', title: 'Discussion 2', body: 'Body 2' },
      ],
      total: 2,
    });
  }),

  http.post('/api/discussions', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({
      id: '3',
      ...body,
    });
  }),
];
```

**Setup in tests** (`src/testing/setup.ts`):

```typescript
import { afterAll, afterEach, beforeAll } from 'vitest';
import { server } from './mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

## Best Practices

1. **Test user behavior, not implementation** - Focus on what users see and do
2. **Use Testing Library queries correctly**:
   - Prefer `getByRole` over `getByTestId`
   - Use `findBy` for async elements
   - Use `queryBy` when checking for absence
3. **Avoid testing implementation details** - Don't test state, props, or internal functions
4. **Mock external dependencies** - Use MSW for API calls
5. **Keep tests simple and readable** - Tests are documentation
6. **Test error states** - Don't just test the happy path
7. **Use meaningful assertions** - Be specific about what you're testing

## Common Patterns

### Testing Forms

```typescript
test('validates form input', async () => {
  const user = userEvent.setup();
  render(<MyForm />);

  // Submit empty form
  await user.click(screen.getByRole('button', { name: /submit/i }));

  // Check for validation errors
  expect(screen.getByText(/email is required/i)).toBeInTheDocument();
});
```

### Testing Loading States

```typescript
test('shows loading spinner', () => {
  render(<MyComponent />);
  expect(screen.getByRole('status')).toBeInTheDocument();
});
```

### Testing Error States

```typescript
test('shows error message on failure', async () => {
  server.use(
    http.get('/api/data', () => {
      return new HttpResponse(null, { status: 500 });
    })
  );

  render(<MyComponent />);

  await waitFor(() => {
    expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
  });
});
```

## Checklist

- [ ] Integration tests cover main user flows
- [ ] Unit tests cover complex utility functions
- [ ] E2E tests cover critical paths
- [ ] API calls are mocked with MSW
- [ ] Tests use Testing Library best practices
- [ ] Tests are colocated with code
- [ ] Test utilities are shared
- [ ] Error states are tested
- [ ] Loading states are tested
- [ ] Tests are readable and maintainable
