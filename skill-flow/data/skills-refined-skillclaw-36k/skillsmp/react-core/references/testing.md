# Testing

Comprehensive testing ensures reliability and confidence when refactoring or adding features.

## Testing Pyramid

Follow the testing pyramid: many unit tests, fewer integration tests, minimal E2E tests.

```
     /\
    /E2E\      ← Few (slow, brittle, expensive)
   /------\
  /Integr.\   ← Some (moderate speed/cost)
 /----------\
/   Unit     \ ← Many (fast, cheap, focused)
--------------
```

## Tooling

- **Test Runner**: Vitest (fast, Vite-native, Jest-compatible API)
- **Component Testing**: React Testing Library (user-centric)
- **E2E Testing**: Playwright (cross-browser, reliable)
- **API Mocking**: MSW (Mock Service Worker)

## Unit Testing Components

### React Testing Library Principles

Test components like users interact with them:

```tsx
// ❌ Bad - testing implementation details
expect(wrapper.find('.button').prop('onClick')).toBeDefined();

// ✅ Good - testing behavior
const button = screen.getByRole('button', { name: /submit/i });
fireEvent.click(button);
expect(mockSubmit).toHaveBeenCalled();
```

### Basic Component Test

```tsx
// components/Button/Button.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const handleClick = vi.fn();
    const user = userEvent.setup();

    render(<Button onClick={handleClick}>Click me</Button>);

    await user.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### Testing Hooks

```tsx
// hooks/useCounter.test.ts
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('accepts initial value', () => {
    const { result } = renderHook(() => useCounter(10));
    expect(result.current.count).toBe(10);
  });
});
```

## Integration Testing

Test feature workflows involving multiple components:

```tsx
// features/auth/LoginForm.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { LoginForm } from './LoginForm';
import { server } from '@/testing/mocks/server';
import { http, HttpResponse } from 'msw';

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: false } },
});

function renderWithProviders(ui: React.ReactElement) {
  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>
  );
}

describe('LoginForm', () => {
  it('successfully logs in with valid credentials', async () => {
    const user = userEvent.setup();

    renderWithProviders(<LoginForm />);

    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /log in/i }));

    await waitFor(() => {
      expect(screen.getByText(/welcome/i)).toBeInTheDocument();
    });
  });

  it('shows error message with invalid credentials', async () => {
    server.use(
      http.post('/api/auth/login', () => {
        return HttpResponse.json(
          { message: 'Invalid credentials' },
          { status: 401 }
        );
      })
    );

    const user = userEvent.setup();

    renderWithProviders(<LoginForm />);

    await user.type(screen.getByLabelText(/email/i), 'wrong@example.com');
    await user.type(screen.getByLabelText(/password/i), 'wrongpass');
    await user.click(screen.getByRole('button', { name: /log in/i }));

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });
  });
});
```

## API Mocking with MSW

### Setup

```tsx
// testing/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: '1', name: 'Alice', email: 'alice@example.com' },
      { id: '2', name: 'Bob', email: 'bob@example.com' },
    ]);
  }),

  http.get('/api/users/:id', ({ params }) => {
    const { id } = params;
    return HttpResponse.json({
      id,
      name: 'Alice',
      email: 'alice@example.com',
    });
  }),

  http.post('/api/users', async ({ request }) => {
    const data = await request.json();
    return HttpResponse.json(
      { id: '3', ...data },
      { status: 201 }
    );
  }),
];

// testing/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);

// testing/setup.ts
import { beforeAll, afterEach, afterAll } from 'vitest';
import { server } from './mocks/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

## E2E Testing with Playwright

```tsx
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('user can log in successfully', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.click('button:has-text("Log in")');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('text=Welcome')).toBeVisible();
  });

  test('shows validation errors for invalid input', async ({ page }) => {
    await page.goto('/login');

    await page.click('button:has-text("Log in")');

    await expect(page.locator('text=Email is required')).toBeVisible();
    await expect(page.locator('text=Password is required')).toBeVisible();
  });
});
```

## Test Utilities

Create reusable test utilities:

```tsx
// testing/test-utils.tsx
import { render, type RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
});

function AllTheProviders({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {children}
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export function renderWithProviders(
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { wrapper: AllTheProviders, ...options });
}

export * from '@testing-library/react';
export { renderWithProviders as render };
```

## Best Practices

1. **Test behavior, not implementation** - Test what users see and do
2. **Use semantic queries** - `getByRole`, `getByLabelText` over `getByTestId`
3. **Avoid snapshot tests for components** - Brittle, low value
4. **Mock external dependencies** - Use MSW for API, mock heavy libraries
5. **Test edge cases** - Empty states, loading, errors
6. **Keep tests focused** - One concern per test
7. **Use data-testid sparingly** - Only when semantic queries fail
8. **Test accessibility** - Use `getByRole` queries

## Coverage Goals

Aim for high coverage on critical paths:

- **Business logic**: 90%+ coverage
- **UI components**: 70-80% coverage
- **E2E**: Critical user journeys

Coverage is a guide, not a goal. 100% coverage doesn't mean bug-free code.
