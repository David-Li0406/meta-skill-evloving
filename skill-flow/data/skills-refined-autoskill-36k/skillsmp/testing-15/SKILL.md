---
name: testing
description: Write tests with Vitest and Testing Library. Use when creating tests, writing specs, mocking, or setting up test coverage.
---

# Vitest + Testing Library

## Running Tests

```sh
pnpm test            # Run all
pnpm test:watch      # Watch mode
pnpm test:coverage   # With coverage
```

## Basic Test

```tsx
import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { Button } from '@oakoss/ui';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(
      screen.getByRole('button', { name: /click me/i }),
    ).toBeInTheDocument();
  });
});
```

## User Interactions

```tsx
import userEvent from '@testing-library/user-event';

it('handles click', async () => {
  const user = userEvent.setup();
  const onClick = vi.fn();

  render(<Button onPress={onClick}>Click</Button>);
  await user.click(screen.getByRole('button'));

  expect(onClick).toHaveBeenCalled();
});
```

## Query Priority

1. `getByRole` - Accessible elements
2. `getByLabelText` - Form inputs
3. `getByText` - Text content
4. `getByTestId` - Last resort

## Mocking

```ts
const mockFn = vi.fn().mockReturnValue('result');

vi.mock('@oakoss/ui', () => ({
  Button: vi.fn(({ children }) => <button>{children}</button>),
}));

const spy = vi.spyOn(utils, 'cn');
```

## Async

```tsx
await screen.findByText('Loaded');

await waitFor(() => {
  expect(screen.getByRole('list')).toHaveTextContent('Item');
});
```

## Testing TanStack Query

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });
}

function renderWithQuery(ui: React.ReactElement) {
  const queryClient = createTestQueryClient();
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>,
  );
}

it('loads and displays data', async () => {
  vi.mock('@/lib/api', () => ({
    getPosts: vi.fn().mockResolvedValue([{ id: '1', title: 'Test' }]),
  }));

  renderWithQuery(<PostList />);
  expect(await screen.findByText('Test')).toBeInTheDocument();
});
```

## Testing TanStack Form

```tsx
import userEvent from '@testing-library/user-event';

it('validates and submits form', async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();

  render(<LoginForm onSubmit={onSubmit} />);

  await user.type(screen.getByLabelText(/email/i), 'test@example.com');
  await user.type(screen.getByLabelText(/password/i), 'password123');
  await user.click(screen.getByRole('button', { name: /submit/i }));

  await waitFor(() => {
    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });
});

it('shows validation errors', async () => {
  const user = userEvent.setup();
  render(<LoginForm />);

  await user.click(screen.getByRole('button', { name: /submit/i }));

  expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
});
```

## Testing with Router Context

```tsx
import { RouterProvider, createMemoryHistory } from '@tanstack/react-router';

function renderWithRouter(ui: React.ReactElement, { route = '/' } = {}) {
  const history = createMemoryHistory({ initialEntries: [route] });
  const router = createRouter({ routeTree, history });

  return render(<RouterProvider router={router}>{ui}</RouterProvider>);
}

it('navigates on click', async () => {
  const user = userEvent.setup();
  renderWithRouter(<Navigation />, { route: '/' });

  await user.click(screen.getByRole('link', { name: /about/i }));

  expect(window.location.pathname).toBe('/about');
});
```

## Mocking Server Functions

```tsx
vi.mock('@/lib/server-functions', () => ({
  getUser: vi.fn(),
  updateUser: vi.fn(),
}));

import { getUser, updateUser } from '@/lib/server-functions';

beforeEach(() => {
  vi.mocked(getUser).mockResolvedValue({ id: '1', name: 'Test User' });
});

it('loads user data', async () => {
  render(<UserProfile userId="1" />);
  expect(await screen.findByText('Test User')).toBeInTheDocument();
  expect(getUser).toHaveBeenCalledWith({ data: { id: '1' } });
});
```

## Common Mistakes

| Mistake                         | Correct Pattern                          |
| ------------------------------- | ---------------------------------------- |
| Using `getBy` for async content | Use `findBy` or `waitFor` for async      |
| Testing implementation details  | Test behavior, not internal state        |
| Using `getByTestId` first       | Prefer `getByRole`, `getByLabelText`     |
| Missing `userEvent.setup()`     | Always call `userEvent.setup()` first    |
| Not wrapping in act             | Use `userEvent` which handles this       |
| Mocking too much                | Only mock external dependencies          |
| Not cleaning up mocks           | Use `vi.clearAllMocks()` in `beforeEach` |
| Shared QueryClient in tests     | Create fresh QueryClient per test        |
| Retry enabled in test queries   | Set `retry: false` in test QueryClient   |
| Testing third-party components  | Trust the library, test your usage       |

## Delegation

- **Test discovery**: For finding untested code paths, use `Explore` agent
- **Coverage analysis**: For comprehensive coverage review, use `Task` agent
- **Code review**: After writing tests, delegate to `code-reviewer` agent

## Related Skills

| Task                    | Skill                                                    |
| ----------------------- | -------------------------------------------------------- |
| Query testing patterns  | [tanstack-query](../tanstack-query/SKILL.md)             |
| Form testing patterns   | [tanstack-form](../tanstack-form/SKILL.md)               |
| Router testing patterns | [tanstack-router](../tanstack-router/SKILL.md)           |
| Error boundary testing  | [error-boundaries](../error-boundaries/SKILL.md)         |
| Integration flows       | [integration-patterns](../integration-patterns/SKILL.md) |
