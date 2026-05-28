# Mock Patterns for Raamattu Nyt Tests

Reusable mock patterns for common dependencies.

## Table of Contents
- [Supabase Client](#supabase-client)
- [useAuth Hook](#useauth-hook)
- [React Query](#react-query)
- [localStorage](#localstorage)
- [Bible Schema Queries](#bible-schema-queries)

---

## Supabase Client

### Basic RPC Mock

```typescript
const mockRpc = vi.fn();

vi.mock("@/integrations/supabase/client", () => ({
  supabase: {
    rpc: (...args: unknown[]) => mockRpc(...args),
  },
}));

// Usage in test
mockRpc.mockResolvedValue({ data: { result: "success" }, error: null });

// With error
mockRpc.mockResolvedValue({ data: null, error: { message: "Database error" } });
```

### Full Auth Mock

```typescript
const mockUnsubscribe = vi.fn();
const mockOnAuthStateChange = vi.fn().mockReturnValue({
  data: { subscription: { unsubscribe: mockUnsubscribe } },
});
const mockGetSession = vi.fn();
const mockSignOut = vi.fn();

vi.mock("@/integrations/supabase/client", () => ({
  supabase: {
    auth: {
      onAuthStateChange: (...args: unknown[]) => mockOnAuthStateChange(...args),
      getSession: () => mockGetSession(),
      signOut: () => mockSignOut(),
    },
  },
}));

// Return authenticated session
mockGetSession.mockResolvedValue({
  data: {
    session: {
      user: { id: "user-123", email: "test@example.com" },
      access_token: "token",
    },
  },
});

// Return no session
mockGetSession.mockResolvedValue({ data: { session: null } });
```

### Schema Query Mock (bible_schema)

```typescript
const mockFrom = vi.fn();
const mockSelect = vi.fn();
const mockEq = vi.fn();
const mockOrder = vi.fn();

vi.mock("@/integrations/supabase/client", () => ({
  supabase: {
    schema: () => ({
      from: (...args: unknown[]) => mockFrom(...args),
    }),
  },
}));

mockFrom.mockReturnValue({
  select: mockSelect.mockReturnValue({
    eq: mockEq.mockReturnValue({
      order: mockOrder.mockResolvedValue({ data: [], error: null }),
    }),
  }),
});
```

---

## useAuth Hook

```typescript
const mockUser = { id: "user-123", email: "test@example.com" };

vi.mock("@shared-auth/hooks/useAuth", () => ({
  useAuth: () => ({
    user: mockUser,
    loading: false,
    session: { user: mockUser, access_token: "token" },
    signOut: vi.fn(),
  }),
}));

// For unauthenticated state
vi.mock("@shared-auth/hooks/useAuth", () => ({
  useAuth: () => ({
    user: null,
    loading: false,
    session: null,
    signOut: vi.fn(),
  }),
}));

// For loading state
vi.mock("@shared-auth/hooks/useAuth", () => ({
  useAuth: () => ({
    user: null,
    loading: true,
    session: null,
    signOut: vi.fn(),
  }),
}));
```

---

## React Query

### Mock QueryClient

```typescript
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={createTestQueryClient()}>
    {children}
  </QueryClientProvider>
);

// Use in renderHook
const { result } = renderHook(() => useMyHook(), { wrapper });
```

### Mock useQuery Result

```typescript
vi.mock("@tanstack/react-query", async () => {
  const actual = await vi.importActual("@tanstack/react-query");
  return {
    ...actual,
    useQuery: vi.fn().mockReturnValue({
      data: mockData,
      isLoading: false,
      error: null,
      refetch: vi.fn(),
    }),
  };
});
```

---

## localStorage

```typescript
const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: vi.fn((key: string) => store[key] || null),
    setItem: vi.fn((key: string, value: string) => {
      store[key] = value;
    }),
    removeItem: vi.fn((key: string) => {
      delete store[key];
    }),
    clear: vi.fn(() => {
      store = {};
    }),
  };
})();

Object.defineProperty(window, "localStorage", { value: localStorageMock });

// Reset in beforeEach
beforeEach(() => {
  localStorageMock.clear();
  vi.clearAllMocks();
});
```

---

## Bible Schema Queries

### Mock subscription_plans query

```typescript
const mockPlans = [
  { id: "1", plan_key: "guest", display_name: "Guest", tokens_per_window: 1000 },
  { id: "2", plan_key: "basic", display_name: "Basic", tokens_per_window: 5000 },
];

mockRpc.mockImplementation((fn: string) => {
  if (fn === "get_user_token_balance") {
    return Promise.resolve({
      data: {
        tokens_used: 500,
        tokens_limit: 5000,
        tokens_remaining: 4500,
        resets_in_minutes: 180,
        plan_key: "basic",
        plan_display_name: "Basic",
      },
      error: null,
    });
  }
  return Promise.resolve({ data: null, error: null });
});
```

### Mock can_use_operation RPC

```typescript
mockRpc.mockImplementation((fn: string, params: { p_operation_key: string }) => {
  if (fn === "can_use_operation") {
    return Promise.resolve({
      data: {
        allowed: true,
        reason: null,
        cost: 100,
        balance_after: 4900,
        operation_display_name: params.p_operation_key,
      },
      error: null,
    });
  }
  return Promise.resolve({ data: null, error: null });
});
```
