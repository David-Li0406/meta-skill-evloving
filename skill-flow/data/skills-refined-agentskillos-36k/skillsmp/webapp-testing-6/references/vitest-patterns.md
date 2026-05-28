# Vitest Testing Patterns for LucidData

Comprehensive guide to unit and integration testing patterns using Vitest 3.2.4 with React Testing Library.

## Table of Contents

1. [Component Testing](#component-testing)
2. [Mocking Prisma Client](#mocking-prisma-client)
3. [Mocking Supabase Client](#mocking-supabase-client)
4. [Testing React Hooks](#testing-react-hooks)
5. [Testing API Route Handlers](#testing-api-route-handlers)
6. [Async Testing Patterns](#async-testing-patterns)
7. [Best Practices](#best-practices)

## Component Testing

### Basic Component Test

```typescript
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Button } from '@/components/ui/button';

describe('Button', () => {
  it('should render with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument();
  });

  it('should apply variant styles', () => {
    render(<Button variant="destructive">Delete</Button>);
    const button = screen.getByRole('button', { name: 'Delete' });
    expect(button).toHaveClass('bg-destructive');
  });

  it('should be disabled when prop is set', () => {
    render(<Button disabled>Disabled</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

### Testing User Interactions

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';

describe('LoginForm', () => {
  it('should call onSubmit with form data', async () => {
    const user = userEvent.setup();
    const handleSubmit = vi.fn();

    render(<LoginForm onSubmit={handleSubmit} />);

    await user.type(screen.getByLabelText('Email'), 'test@example.com');
    await user.type(screen.getByLabelText('Password'), 'password123');
    await user.click(screen.getByRole('button', { name: 'Sign In' }));

    expect(handleSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });

  it('should display validation errors', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={vi.fn()} />);

    // Submit without filling fields
    await user.click(screen.getByRole('button', { name: 'Sign In' }));

    expect(screen.getByText('Email is required')).toBeInTheDocument();
    expect(screen.getByText('Password is required')).toBeInTheDocument();
  });
});
```

### Testing Components with React Query

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect, beforeEach } from 'vitest';
import { VaultList } from '@/components/vault/vault-list';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        cacheTime: 0,
        staleTime: 0,
      },
    },
    logger: {
      log: console.log,
      warn: console.warn,
      error: () => {}, // Suppress error logs in tests
    },
  });
}

function renderWithQueryClient(ui: React.ReactElement) {
  const queryClient = createTestQueryClient();
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>
  );
}

describe('VaultList', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should display loading state', () => {
    renderWithQueryClient(<VaultList />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('should display vault entries after loading', async () => {
    // Mock API response
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            data: [
              { id: '1', label: 'Entry 1', category: 'Identity' },
              { id: '2', label: 'Entry 2', category: 'Financial' },
            ],
          }),
      })
    ) as any;

    renderWithQueryClient(<VaultList />);

    await waitFor(() => {
      expect(screen.getByText('Entry 1')).toBeInTheDocument();
      expect(screen.getByText('Entry 2')).toBeInTheDocument();
    });
  });

  it('should display error state on fetch failure', async () => {
    global.fetch = vi.fn(() =>
      Promise.reject(new Error('Network error'))
    ) as any;

    renderWithQueryClient(<VaultList />);

    await waitFor(() => {
      expect(screen.getByText(/error loading/i)).toBeInTheDocument();
    });
  });
});
```

## Mocking Prisma Client

### Setup Prisma Mock

```typescript
// test/mocks/prisma.ts
import { PrismaClient } from '@prisma/client';
import { mockDeep, mockReset, DeepMockProxy } from 'vitest-mock-extended';

export const prismaMock = mockDeep<PrismaClient>() as DeepMockProxy<PrismaClient>;

beforeEach(() => {
  mockReset(prismaMock);
});
```

### Mock Prisma in Tests

```typescript
// lib/repositories/__tests__/vault.repository.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { VaultRepository } from '../vault.repository';
import { prismaMock } from '@/test/mocks/prisma';

vi.mock('@/lib/db/prisma', () => ({
  prisma: prismaMock,
}));

describe('VaultRepository', () => {
  let repository: VaultRepository;

  beforeEach(() => {
    repository = new VaultRepository();
    vi.clearAllMocks();
  });

  it('should find vault entries by user ID', async () => {
    const mockEntries = [
      {
        id: '1',
        userId: 'user-123',
        label: 'Entry 1',
        category: 'Identity',
        encryptedData: 'encrypted',
        iv: 'iv',
        tag: 'tag',
        encryptionKeyId: 'v2',
        metadata: null,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
    ];

    prismaMock.vaultData.findMany.mockResolvedValue(mockEntries);

    const result = await repository.findByUserId('user-123');

    expect(result).toEqual(mockEntries);
    expect(prismaMock.vaultData.findMany).toHaveBeenCalledWith({
      where: { userId: 'user-123' },
      orderBy: { createdAt: 'desc' },
    });
  });

  it('should create vault entry', async () => {
    const input = {
      userId: 'user-123',
      label: 'Test Entry',
      category: 'Identity',
      encryptedData: 'encrypted',
      iv: 'iv',
      tag: 'tag',
      encryptionKeyId: 'v2',
    };

    const mockCreated = { id: 'new-id', ...input, createdAt: new Date(), updatedAt: new Date(), metadata: null };

    prismaMock.vaultData.create.mockResolvedValue(mockCreated);

    const result = await repository.create(input);

    expect(result).toEqual(mockCreated);
    expect(prismaMock.vaultData.create).toHaveBeenCalledWith({
      data: input,
    });
  });

  it('should update vault entry', async () => {
    const mockUpdated = {
      id: '1',
      userId: 'user-123',
      label: 'Updated Entry',
      category: 'Financial',
      encryptedData: 'new-encrypted',
      iv: 'new-iv',
      tag: 'new-tag',
      encryptionKeyId: 'v2',
      metadata: null,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    prismaMock.vaultData.update.mockResolvedValue(mockUpdated);

    const result = await repository.update('1', {
      label: 'Updated Entry',
      category: 'Financial',
    });

    expect(result).toEqual(mockUpdated);
    expect(prismaMock.vaultData.update).toHaveBeenCalledWith({
      where: { id: '1' },
      data: { label: 'Updated Entry', category: 'Financial' },
    });
  });

  it('should delete vault entry', async () => {
    prismaMock.vaultData.delete.mockResolvedValue({} as any);

    await repository.delete('1');

    expect(prismaMock.vaultData.delete).toHaveBeenCalledWith({
      where: { id: '1' },
    });
  });
});
```

## Mocking Supabase Client

### Setup Supabase Mock

```typescript
// test/mocks/supabase.ts
import { vi } from 'vitest';

export const mockSupabaseClient = {
  auth: {
    getUser: vi.fn(),
    signUp: vi.fn(),
    signInWithPassword: vi.fn(),
    signOut: vi.fn(),
    onAuthStateChange: vi.fn(() => ({
      data: { subscription: { unsubscribe: vi.fn() } },
    })),
  },
  from: vi.fn(() => ({
    select: vi.fn(() => ({
      eq: vi.fn(() => ({
        single: vi.fn(),
      })),
    })),
    insert: vi.fn(),
    update: vi.fn(),
    delete: vi.fn(),
  })),
};

export function createMockSupabaseClient() {
  return mockSupabaseClient;
}
```

### Mock Supabase in Tests

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mockSupabaseClient } from '@/test/mocks/supabase';

vi.mock('@/lib/supabase/server', () => ({
  createClient: () => mockSupabaseClient,
}));

describe('Auth API', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should authenticate user', async () => {
    mockSupabaseClient.auth.signInWithPassword.mockResolvedValue({
      data: {
        user: { id: 'user-123', email: 'test@example.com' },
        session: { access_token: 'token', refresh_token: 'refresh' },
      },
      error: null,
    });

    // Test your auth logic
  });

  it('should handle authentication error', async () => {
    mockSupabaseClient.auth.signInWithPassword.mockResolvedValue({
      data: { user: null, session: null },
      error: { message: 'Invalid credentials' },
    });

    // Test error handling
  });
});
```

## Testing React Hooks

### Testing Custom Hooks

```typescript
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { describe, it, expect, vi } from 'vitest';
import { useVault } from '@/lib/hooks/useVault';

function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

describe('useVault', () => {
  it('should fetch vault entries', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            data: [{ id: '1', label: 'Entry 1' }],
          }),
      })
    ) as any;

    const { result } = renderHook(() => useVault.useList(), {
      wrapper: createWrapper(),
    });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toEqual([{ id: '1', label: 'Entry 1' }]);
  });

  it('should create vault entry', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            data: { id: 'new-id', label: 'New Entry' },
          }),
      })
    ) as any;

    const { result } = renderHook(() => useVault.useCreate(), {
      wrapper: createWrapper(),
    });

    result.current.mutate({ label: 'New Entry', category: 'Identity' });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));

    expect(result.current.data).toEqual({ id: 'new-id', label: 'New Entry' });
  });
});
```

### Testing useEffect and State Updates

```typescript
import { renderHook, act } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { useState, useEffect } from 'react';

function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);

  useEffect(() => {
    // Simulate side effect
    console.log(`Count: ${count}`);
  }, [count]);

  const increment = () => setCount((c) => c + 1);
  const decrement = () => setCount((c) => c - 1);

  return { count, increment, decrement };
}

describe('useCounter', () => {
  it('should initialize with default value', () => {
    const { result } = renderHook(() => useCounter());
    expect(result.current.count).toBe(0);
  });

  it('should increment count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('should decrement count', () => {
    const { result } = renderHook(() => useCounter(5));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(4);
  });
});
```

## Testing API Route Handlers

### Testing Next.js API Routes

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { NextRequest } from 'next/server';
import { POST } from '@/app/api/vault/route';
import { prismaMock } from '@/test/mocks/prisma';
import { mockSupabaseClient } from '@/test/mocks/supabase';

vi.mock('@/lib/db/prisma', () => ({ prisma: prismaMock }));
vi.mock('@/lib/supabase/server', () => ({
  createClient: () => mockSupabaseClient,
}));

describe('/api/vault POST', () => {
  beforeEach(() => {
    vi.clearAllMocks();

    // Mock authenticated user
    mockSupabaseClient.auth.getUser.mockResolvedValue({
      data: { user: { id: 'user-123', email: 'test@example.com' } },
      error: null,
    });
  });

  it('should create vault entry', async () => {
    const mockCreated = {
      id: 'new-id',
      userId: 'user-123',
      label: 'Test Entry',
      category: 'Identity',
      encryptedData: 'encrypted',
      iv: 'iv',
      tag: 'tag',
      encryptionKeyId: 'v2',
      metadata: null,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    prismaMock.vaultData.create.mockResolvedValue(mockCreated);

    const request = new NextRequest('http://localhost:3000/api/vault', {
      method: 'POST',
      body: JSON.stringify({
        label: 'Test Entry',
        category: 'Identity',
        metadata: { key: 'value' },
      }),
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(201);
    expect(data.success).toBe(true);
    expect(data.data).toEqual(mockCreated);
  });

  it('should return 401 when not authenticated', async () => {
    mockSupabaseClient.auth.getUser.mockResolvedValue({
      data: { user: null },
      error: { message: 'Unauthorized' },
    });

    const request = new NextRequest('http://localhost:3000/api/vault', {
      method: 'POST',
      body: JSON.stringify({}),
    });

    const response = await POST(request);

    expect(response.status).toBe(401);
  });

  it('should return 400 on validation error', async () => {
    const request = new NextRequest('http://localhost:3000/api/vault', {
      method: 'POST',
      body: JSON.stringify({
        // Missing required fields
        label: '',
      }),
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(400);
    expect(data.success).toBe(false);
    expect(data.error).toBeDefined();
  });
});
```

## Async Testing Patterns

### Testing Promises

```typescript
it('should resolve promise', async () => {
  const promise = Promise.resolve('success');
  await expect(promise).resolves.toBe('success');
});

it('should reject promise', async () => {
  const promise = Promise.reject(new Error('Failed'));
  await expect(promise).rejects.toThrow('Failed');
});
```

### Waiting for Async Updates

```typescript
import { waitFor } from '@testing-library/react';

it('should update after async operation', async () => {
  render(<AsyncComponent />);

  await waitFor(() => {
    expect(screen.getByText('Loaded')).toBeInTheDocument();
  });
});

it('should wait with custom timeout', async () => {
  render(<SlowComponent />);

  await waitFor(
    () => {
      expect(screen.getByText('Ready')).toBeInTheDocument();
    },
    { timeout: 5000 }
  );
});
```

### Testing Debounced/Throttled Functions

```typescript
import { vi } from 'vitest';

it('should debounce function calls', async () => {
  vi.useFakeTimers();
  const debouncedFn = vi.fn();

  render(<SearchComponent onSearch={debouncedFn} />);

  const input = screen.getByRole('textbox');

  await user.type(input, 'search term');

  // Function shouldn't be called immediately
  expect(debouncedFn).not.toHaveBeenCalled();

  // Fast-forward time
  vi.advanceTimersByTime(500);

  expect(debouncedFn).toHaveBeenCalledWith('search term');

  vi.useRealTimers();
});
```

## Best Practices

### 1. AAA Pattern (Arrange-Act-Assert)

```typescript
it('should calculate total', () => {
  // Arrange: Set up test data
  const items = [{ price: 10 }, { price: 20 }, { price: 30 }];

  // Act: Execute the function
  const total = calculateTotal(items);

  // Assert: Verify the result
  expect(total).toBe(60);
});
```

### 2. One Assertion Per Test (when possible)

```typescript
// Good: Focused test
it('should return user name', () => {
  const user = { name: 'John', email: 'john@example.com' };
  expect(getUserName(user)).toBe('John');
});

// Acceptable: Multiple related assertions
it('should create user object', () => {
  const user = createUser('John', 'john@example.com');
  expect(user.name).toBe('John');
  expect(user.email).toBe('john@example.com');
  expect(user.id).toBeDefined();
});
```

### 3. Use Descriptive Test Names

```typescript
// Good
it('should return error when email is invalid')
it('should create vault entry with encrypted data')
it('should redirect to login when session expires')

// Bad
it('works')
it('test validation')
it('handles error')
```

### 4. Clean Up After Tests

```typescript
beforeEach(() => {
  vi.clearAllMocks();
});

afterEach(() => {
  vi.restoreAllMocks();
  cleanup(); // From @testing-library/react
});
```

### 5. Mock Only What's Necessary

```typescript
// Good: Mock external dependency
vi.mock('@/lib/db/prisma', () => ({ prisma: prismaMock }));

// Bad: Mocking internal logic defeats the purpose of integration tests
vi.mock('@/lib/utils', () => ({ someUtil: vi.fn() }));
```

### 6. Test Edge Cases

```typescript
describe('validateEmail', () => {
  it('should accept valid email', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });

  it('should reject email without @', () => {
    expect(validateEmail('testexample.com')).toBe(false);
  });

  it('should reject email without domain', () => {
    expect(validateEmail('test@')).toBe(false);
  });

  it('should handle empty string', () => {
    expect(validateEmail('')).toBe(false);
  });

  it('should handle null', () => {
    expect(validateEmail(null as any)).toBe(false);
  });
});
```

### 7. Use Test Fixtures

```typescript
import { mockVaultEntry } from '@/test/fixtures/vault-data';

it('should display vault entry', () => {
  render(<VaultCard entry={mockVaultEntry} />);
  expect(screen.getByText(mockVaultEntry.label)).toBeInTheDocument();
});
```

### 8. Avoid Testing Implementation Details

```typescript
// Good: Test behavior
it('should increment counter when button is clicked', async () => {
  render(<Counter />);
  await user.click(screen.getByRole('button', { name: 'Increment' }));
  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});

// Bad: Test implementation
it('should call setState when button is clicked', async () => {
  const { result } = renderHook(() => useState(0));
  // Testing internal React state is an implementation detail
});
```

### 9. Use screen Queries Over container

```typescript
// Good
expect(screen.getByText('Hello')).toBeInTheDocument();

// Avoid
const { container } = render(<Component />);
expect(container.querySelector('.hello')).toBeTruthy();
```

### 10. Prefer User Event Over fireEvent

```typescript
// Good: Simulates real user interaction
await user.click(button);
await user.type(input, 'text');

// Acceptable: When userEvent doesn't support the event
fireEvent.focus(input);
```

---

**For more information:**
- [Vitest Documentation](https://vitest.dev)
- [React Testing Library](https://testing-library.com/react)
- [LucidData Test Data Reference](test-data.md)
