# Testing Patterns Reference

## Test Setup

### Fresh QueryClient Per Test

Create a new QueryClient for each test to ensure complete isolation:

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { renderHook, waitFor } from '@testing-library/react';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false, // Disable retries in tests
      },
    },
  });
}

function createWrapper() {
  const queryClient = createTestQueryClient();
  return function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    );
  };
}
```

### Disable Retries

React Query retries failed queries 3 times with exponential backoff by default. This causes test timeouts:

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
    mutations: {
      retry: false,
    },
  },
});
```

## Network Mocking with MSW

Use [Mock Service Worker](https://mswjs.io/) as the single source of truth for API mocking:

```tsx
// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/todos', () => {
    return HttpResponse.json([
      { id: '1', name: 'Learn TanStack Query' },
      { id: '2', name: 'Write tests' },
    ]);
  }),

  http.post('/api/todos', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json({ id: '3', ...body }, { status: 201 });
  }),
];

// src/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

```tsx
// vitest.setup.ts
import { server } from './src/mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

**Benefits of MSW:**

- Works in Node.js tests, browser, and Cypress
- Single source of truth for mocks
- Intercepts actual network requests (not fetch mocks)

## Testing Queries

### Hook Testing

```tsx
import { renderHook, waitFor } from '@testing-library/react';

test('fetches todos successfully', async () => {
  const { result } = renderHook(() => useTodosQuery(), {
    wrapper: createWrapper(),
  });

  // Wait for query to complete
  await waitFor(() => expect(result.current.isSuccess).toBe(true));

  expect(result.current.data).toHaveLength(2);
  expect(result.current.data?.[0].name).toBe('Learn TanStack Query');
});
```

### Component Testing

```tsx
import { render, screen, waitFor } from '@testing-library/react';

test('renders todos', async () => {
  const queryClient = createTestQueryClient();

  render(
    <QueryClientProvider client={queryClient}>
      <TodoList />
    </QueryClientProvider>,
  );

  // Wait for loading to complete
  await waitFor(() => {
    expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
  });

  expect(screen.getByText('Learn TanStack Query')).toBeInTheDocument();
});
```

## Testing Mutations

```tsx
import { renderHook, waitFor, act } from '@testing-library/react';

test('creates todo successfully', async () => {
  const { result } = renderHook(() => useCreateTodoMutation(), {
    wrapper: createWrapper(),
  });

  act(() => {
    result.current.mutate({ name: 'New todo' });
  });

  await waitFor(() => expect(result.current.isSuccess).toBe(true));

  expect(result.current.data?.name).toBe('New todo');
});
```

## Testing Error States

Override handlers for specific tests:

```tsx
import { server } from './mocks/server';
import { http, HttpResponse } from 'msw';

test('handles error state', async () => {
  // Override handler for this test only
  server.use(
    http.get('/api/todos', () => {
      return HttpResponse.json({ message: 'Server error' }, { status: 500 });
    }),
  );

  const { result } = renderHook(() => useTodosQuery(), {
    wrapper: createWrapper(),
  });

  await waitFor(() => expect(result.current.isError).toBe(true));

  expect(result.current.error?.message).toContain('500');
});
```

## Common Testing Mistakes

| Mistake                          | Why It's Wrong                    | Correct Approach                   |
| -------------------------------- | --------------------------------- | ---------------------------------- |
| Shared QueryClient between tests | State leaks between tests         | Create fresh client per test       |
| Not disabling retries            | Tests timeout waiting for retries | Set `retry: false`                 |
| Immediate assertions             | Query hasn't completed            | Use `waitFor` for async            |
| Mocking fetch directly           | Brittle, misses network layer     | Use MSW                            |
| Testing without provider         | Hook throws error                 | Always wrap in QueryClientProvider |

## Testing with Suspense

```tsx
import { Suspense } from 'react';

test('renders with suspense', async () => {
  const queryClient = createTestQueryClient();

  render(
    <QueryClientProvider client={queryClient}>
      <Suspense fallback={<div>Loading...</div>}>
        <SuspenseTodoList />
      </Suspense>
    </QueryClientProvider>,
  );

  // Initially shows loading
  expect(screen.getByText('Loading...')).toBeInTheDocument();

  // Wait for content
  await waitFor(() => {
    expect(screen.getByText('Learn TanStack Query')).toBeInTheDocument();
  });
});
```

## Pre-Populating Cache for Tests

Seed the cache to skip network requests:

```tsx
test('renders with pre-populated cache', async () => {
  const queryClient = createTestQueryClient();

  queryClient.setQueryData(
    ['todos'],
    [{ id: '1', name: 'Pre-populated todo' }],
  );

  render(
    <QueryClientProvider client={queryClient}>
      <TodoList />
    </QueryClientProvider>,
  );

  // Data is immediately available
  expect(screen.getByText('Pre-populated todo')).toBeInTheDocument();
});
```
