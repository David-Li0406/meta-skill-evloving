# Vitest Testing Patterns

Next.js/TypeScript 프로젝트를 위한 Vitest 테스팅 패턴.

## Mocking Patterns

### Module Mock

```typescript
// Mock entire module
vi.mock('~/lib/api', () => ({
  fetchUsers: vi.fn(() => Promise.resolve([{ id: 1, name: 'John' }])),
}));

// Reset mocks
afterEach(() => {
  vi.clearAllMocks();
});
```

### Partial Mock

```typescript
// Keep original, mock specific exports
vi.mock('~/lib/utils', async () => {
  const actual = await vi.importActual('~/lib/utils');
  return {
    ...actual,
    formatDate: vi.fn(() => '2024-01-01'),
  };
});
```

### External Library Mock

```typescript
// next/navigation
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    back: vi.fn(),
  }),
  usePathname: () => '/test',
  useSearchParams: () => new URLSearchParams(),
}));

// next-auth
vi.mock('next-auth/react', () => ({
  useSession: () => ({
    data: { user: { name: 'Test User' } },
    status: 'authenticated',
  }),
  signIn: vi.fn(),
  signOut: vi.fn(),
}));
```

---

## Async Testing

### Promises

```typescript
it('fetches data successfully', async () => {
  const data = await fetchData();
  expect(data).toEqual({ id: 1 });
});
```

### waitFor

```typescript
import { waitFor } from '@testing-library/react';

it('shows loading then content', async () => {
  render(<AsyncComponent />);

  // Initially loading
  expect(screen.getByText('Loading...')).toBeInTheDocument();

  // Wait for content
  await waitFor(() => {
    expect(screen.getByText('Content loaded')).toBeInTheDocument();
  });
});
```

### findBy queries

```typescript
it('renders async content', async () => {
  render(<UserProfile userId="1" />);

  // findBy waits for element
  const name = await screen.findByText('John Doe');
  expect(name).toBeInTheDocument();
});
```

---

## Form Testing

### With React Hook Form + Zod

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('shows validation errors', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={vi.fn()} />);

    // Submit empty form
    await user.click(screen.getByRole('button', { name: /submit/i }));

    // Check validation errors
    await waitFor(() => {
      expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    });
  });

  it('submits valid data', async () => {
    const user = userEvent.setup();
    const handleSubmit = vi.fn();
    render(<LoginForm onSubmit={handleSubmit} />);

    // Fill form
    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');

    // Submit
    await user.click(screen.getByRole('button', { name: /submit/i }));

    await waitFor(() => {
      expect(handleSubmit).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      });
    });
  });
});
```

---

## Server Component Testing

### Page Component

```typescript
// app/users/page.test.tsx
import { render, screen } from '@testing-library/react';
import UsersPage from './page';

// Mock data fetching
vi.mock('~/lib/db', () => ({
  getUsers: vi.fn(() => Promise.resolve([
    { id: 1, name: 'John' },
    { id: 2, name: 'Jane' },
  ])),
}));

describe('UsersPage', () => {
  it('renders user list', async () => {
    const page = await UsersPage();
    render(page);

    expect(screen.getByText('John')).toBeInTheDocument();
    expect(screen.getByText('Jane')).toBeInTheDocument();
  });
});
```

---

## Snapshot Testing

```typescript
it('matches snapshot', () => {
  const { container } = render(<Card title="Test" />);
  expect(container).toMatchSnapshot();
});

// Inline snapshot
it('matches inline snapshot', () => {
  const { container } = render(<Badge variant="success">OK</Badge>);
  expect(container.innerHTML).toMatchInlineSnapshot(`
    "<span class="badge badge-success">OK</span>"
  `);
});
```

---

## Test Organization

### File Structure

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx    # Co-located test
│   │   └── index.ts
├── hooks/
│   ├── useAuth.ts
│   └── useAuth.test.ts
├── lib/
│   ├── utils.ts
│   └── utils.test.ts
└── __tests__/                  # Integration tests
    └── api/
        └── users.test.ts
```

### Naming Convention

```typescript
// ✅ Good
describe('ComponentName', () => {
  describe('when condition', () => {
    it('should behavior', () => {});
  });
});

// ✅ Also good (AAA pattern)
describe('formatPrice', () => {
  it('formats positive numbers with currency', () => {
    // Arrange
    const input = 1000;

    // Act
    const result = formatPrice(input);

    // Assert
    expect(result).toBe('$1,000');
  });
});
```

---

## Debugging Tips

### Debug Output

```typescript
import { screen } from '@testing-library/react';

it('debug example', () => {
  render(<Component />);

  // Print DOM
  screen.debug();

  // Print specific element
  screen.debug(screen.getByRole('button'));
});
```

### Testing Playground

```typescript
import { screen } from '@testing-library/react';

it('find query', () => {
  render(<Component />);

  // Open testing playground
  screen.logTestingPlaygroundURL();
});
```
