# Next.js Testing Reference

Testing patterns for Next.js App Router applications.

## Testing Server Components

Server Components run on the server and return JSX. Test them as async functions.

```typescript
// app/users/[id]/page.tsx
export default async function UserPage({ params }: { params: { id: string } }) {
  const user = await fetchUser(params.id);
  return <UserProfile user={user} />;
}

// __tests__/UserPage.test.tsx
import { render, screen } from '@testing-library/react';
import UserPage from '@/app/users/[id]/page';

// Mock the data fetching
vi.mock('@/lib/api', () => ({
  fetchUser: vi.fn().mockResolvedValue({
    id: '1',
    name: 'Test User',
    email: 'test@example.com',
  }),
}));

describe('UserPage', () => {
  it('should render user data', async () => {
    // Server component returns JSX directly
    const Component = await UserPage({ params: { id: '1' } });
    render(Component);

    expect(screen.getByText('Test User')).toBeInTheDocument();
  });
});
```

## Testing Client Components

```typescript
// components/Counter.tsx
'use client';

import { useState } from 'react';

export function Counter({ initial = 0 }: { initial?: number }) {
  const [count, setCount] = useState(initial);
  return (
    <div>
      <span data-testid="count">{count}</span>
      <button onClick={() => setCount(c => c + 1)}>Increment</button>
    </div>
  );
}

// __tests__/Counter.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from '@/components/Counter';

describe('Counter', () => {
  it('should increment on click', async () => {
    const user = userEvent.setup();
    render(<Counter initial={5} />);

    expect(screen.getByTestId('count')).toHaveTextContent('5');

    await user.click(screen.getByRole('button'));

    expect(screen.getByTestId('count')).toHaveTextContent('6');
  });
});
```

## Testing API Routes (Route Handlers)

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();
  const user = await db.user.create({ data: body });
  return NextResponse.json(user, { status: 201 });
}

// __tests__/api/users.test.ts
import { GET, POST } from '@/app/api/users/route';

describe('/api/users', () => {
  describe('GET', () => {
    it('should return users', async () => {
      const request = new Request('http://localhost/api/users');
      const response = await GET(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(Array.isArray(data)).toBe(true);
    });
  });

  describe('POST', () => {
    it('should create user', async () => {
      const request = new Request('http://localhost/api/users', {
        method: 'POST',
        body: JSON.stringify({ name: 'New User', email: 'new@test.com' }),
        headers: { 'Content-Type': 'application/json' },
      });

      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(201);
      expect(data.name).toBe('New User');
    });
  });
});
```

## Testing with Route Parameters

```typescript
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await db.user.findUnique({ where: { id: params.id } });
  if (!user) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }
  return NextResponse.json(user);
}

// __tests__/api/users/[id].test.ts
import { GET } from '@/app/api/users/[id]/route';

it('should return 404 for unknown user', async () => {
  const request = new Request('http://localhost/api/users/unknown');
  const response = await GET(request, { params: { id: 'unknown' } });

  expect(response.status).toBe(404);
});
```

## Testing Server Actions

```typescript
// actions/user.ts
'use server';

import { revalidatePath } from 'next/cache';

export async function updateUser(formData: FormData) {
  const id = formData.get('id') as string;
  const name = formData.get('name') as string;

  await db.user.update({ where: { id }, data: { name } });
  revalidatePath('/users');
}

// __tests__/actions/user.test.ts
import { updateUser } from '@/actions/user';

vi.mock('next/cache', () => ({
  revalidatePath: vi.fn(),
}));

describe('updateUser', () => {
  it('should update user and revalidate', async () => {
    const formData = new FormData();
    formData.set('id', '1');
    formData.set('name', 'Updated Name');

    await updateUser(formData);

    expect(db.user.update).toHaveBeenCalledWith({
      where: { id: '1' },
      data: { name: 'Updated Name' },
    });
    expect(revalidatePath).toHaveBeenCalledWith('/users');
  });
});
```

## Testing with Providers

```typescript
// test/utils.tsx
import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });
}

export function renderWithProviders(
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  const queryClient = createTestQueryClient();

  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    );
  }

  return render(ui, { wrapper: Wrapper, ...options });
}

// Usage
import { renderWithProviders } from '@/test/utils';

it('should render with providers', () => {
  renderWithProviders(<MyComponent />);
});
```

## Testing Middleware

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token');

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

// __tests__/middleware.test.ts
import { middleware } from '@/middleware';
import { NextRequest } from 'next/server';

describe('middleware', () => {
  it('should redirect unauthenticated users from dashboard', () => {
    const request = new NextRequest('http://localhost/dashboard');
    const response = middleware(request);

    expect(response.status).toBe(307);
    expect(response.headers.get('location')).toContain('/login');
  });

  it('should allow authenticated users', () => {
    const request = new NextRequest('http://localhost/dashboard', {
      headers: { cookie: 'token=valid-token' },
    });
    const response = middleware(request);

    expect(response.status).toBe(200);
  });
});
```

## Testing with next/navigation

```typescript
// Mock next/navigation
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    back: vi.fn(),
  }),
  usePathname: () => '/current-path',
  useSearchParams: () => new URLSearchParams('?query=test'),
  redirect: vi.fn(),
}));

// Test component using router
import { useRouter } from 'next/navigation';

it('should navigate on submit', async () => {
  const mockPush = vi.fn();
  vi.mocked(useRouter).mockReturnValue({ push: mockPush } as any);

  const user = userEvent.setup();
  render(<SearchForm />);

  await user.type(screen.getByRole('searchbox'), 'query');
  await user.click(screen.getByRole('button', { name: /search/i }));

  expect(mockPush).toHaveBeenCalledWith('/search?q=query');
});
```

## Testing Loading and Error States

```typescript
// app/users/loading.tsx
export default function Loading() {
  return <div role="progressbar">Loading users...</div>;
}

// app/users/error.tsx
'use client';

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div role="alert">
      <p>Error: {error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  );
}

// __tests__/users/error.test.tsx
import Error from '@/app/users/error';

it('should display error and allow retry', async () => {
  const reset = vi.fn();
  const user = userEvent.setup();

  render(<Error error={new Error('Failed to load')} reset={reset} />);

  expect(screen.getByRole('alert')).toHaveTextContent('Failed to load');

  await user.click(screen.getByRole('button', { name: /try again/i }));
  expect(reset).toHaveBeenCalled();
});
```
