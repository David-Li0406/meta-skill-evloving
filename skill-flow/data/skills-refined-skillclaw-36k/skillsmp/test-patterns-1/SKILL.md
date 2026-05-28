---
name: test-patterns
description: "WHAT: Test React Native with MockedProvider for GraphQL and isolated QueryClient for TanStack Query. WHEN: testing components with server data, GraphQL operations, mutations, loading and error states. KEYWORDS: MockedProvider, QueryClient, renderHook, waitFor, act, GraphQL, TanStack Query, async, Jest."
---

# Testing Patterns for React Native

## Core Principles

**Test in isolation with proper mocking.** Use MockedProvider for GraphQL, create isolated query clients for TanStack Query, and mock native modules globally to prevent test failures.

**Why**: Isolated tests are fast, reliable, and don't depend on external services or native platform code.

## When to Use This Skill

Use these patterns when testing:

- React Native components with server data
- GraphQL operations with Apollo Client
- TanStack Query hooks and mutations
- Components with loading and error states
- Async operations and state updates
- Native module integrations

## Test Environment Setup

Mock native modules globally in `jest.setup.ts` to prevent test failures:

```typescript
// jest.setup.ts
import '@testing-library/jest-native/extend-expect';

jest.mock('@libs/native-modules/events', () => ({
  sendEvent: jest.fn(),
  SharedModulesEventEmitter: {
    addListener: jest.fn(() => ({ remove: jest.fn() })),
  },
}));
```

**Why**: React Native tests fail without native module mocks. Global setup prevents repetition.

## GraphQL Testing with MockedProvider

Use `MockedProvider` to intercept and mock GraphQL queries:

```typescript
import { MockedProvider } from '@apollo/client/testing';
import { render, screen, waitFor } from '@testing-library/react-native';

const mockResponse = {
  request: {
    query: GetProductDetailsDocument,
    variables: { productId: 'product-123' },
  },
  result: {
    data: {
      product: {
        id: 'product-123',
        name: 'Test Product',
        price: { amount: 1299, currency: 'USD' },
      },
    },
  },
};

describe('ProductDetails', () => {
  it('should display product when loaded', async () => {
    render(
      <MockedProvider mocks={[mockResponse]} addTypename={false}>
        <ProductDetails productId="product-123" />
      </MockedProvider>
    );

    // Check loading state
    expect(screen.getByTestId('loading-spinner')).toBeTruthy();

    // Wait for data to load
    await waitFor(() => {
      expect(screen.getByText('Test Product')).toBeTruthy();
      expect(screen.getByText('$12.99')).toBeTruthy();
    });
  });

  it('should handle GraphQL errors', async () => {
    const errorMock = {
      request: {
        query: GetProductDetailsDocument,
        variables: { productId: 'product-123' },
      },
      error: new Error('Product not found'),
    };

    render(
      <MockedProvider mocks={[errorMock]} addTypename={false}>
        <ProductDetails productId="product-123" />
      </MockedProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Error loading product')).toBeTruthy();
    });
  });
});
```

**Key points**:
- `MockedProvider` wraps component under test
- `addTypename={false}` simplifies mocks
- Always test loading and error states
- Use `waitFor()` for async operations

## TanStack Query Testing

Create isolated query clients for each test to prevent pollution:

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { renderHook, waitFor } from '@testing-library/react-native';

// Create test query client with disabled retries and caching
export const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });

// Wrapper component for tests
export const QueryWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const queryClient = createTestQueryClient();
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
};

// Mock the fetch function
jest.mock('@libs/query/client', () => ({
  fetchRepository: jest.fn(),
}));

const mockFetchRepository = require('@libs/query/client').fetchRepository;

describe('usePlanQuery', () => {
  it('should return plan data when available', async () => {
    const mockPlanData = {
      currentPlan: { id: 'plan-123', type: 'MEALKIT' },
      selection: { config: { minMealsSize: 2 } },
    };

    mockFetchRepository.mockResolvedValue(mockPlanData);

    const { result } = renderHook(() => usePlanQuery(), {
      wrapper: QueryWrapper,
    });

    // Initially loading
    expect(result.current.isLoading).toBe(true);

    // Wait for data
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
      expect(result.current.data).toEqual(mockPlanData);
    });
  });

  it('should handle fetch errors', async () => {
    const mockError = new Error('Failed to fetch plan');
    mockFetchRepository.mockRejectedValue(mockError);

    const { result } = renderHook(() => usePlanQuery(), {
      wrapper: QueryWrapper,
    });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
      expect(result.current.error).toEqual(mockError);
    });
  });
});
```

**Why**:
- Isolated clients prevent test pollution
- Disabled retries make tests faster
- `gcTime: 0` prevents caching between tests

## Testing Mutations

Test mutations with `act()` and `waitFor()`:

```typescript
import { renderHook, act, waitFor } from '@testing-library/react-native';

jest.mock('@data-access/native', () => ({
  PlanDataAccess: {
    events: {
      updatePlan: jest.fn(),
    },
  },
}));

describe('useMutatePlan', () => {
  const mockUpdatePlan = require('@data-access/native').PlanDataAccess.events.updatePlan;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should successfully mutate plan', async () => {
    mockUpdatePlan.mockResolvedValue({ success: true });

    const { result } = renderHook(() => useMutatePlan(), {
      wrapper: QueryWrapper,
    });

    // Trigger mutation inside act()
    await act(async () => {
      result.current.mutate({
        planId: 'plan-123',
        updates: { mealSize: 4 },
      });
    });

    // Verify mutation succeeded
    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
      expect(mockUpdatePlan).toHaveBeenCalledWith({
        planId: 'plan-123',
        updates: { mealSize: 4 },
      });
    });
  });

  it('should handle mutation errors', async () => {
    const mockError = new Error('Update failed');
    mockUpdatePlan.mockRejectedValue(mockError);

    const { result } = renderHook(() => useMutatePlan(), {
      wrapper: QueryWrapper,
    });

    await act(async () => {
      result.current.mutate({ planId: 'plan-123', updates: {} });
    });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
      expect(result.current.error).toEqual(mockError);
    });
  });
});
```

**Why**:
- `act()` ensures state updates complete
- `waitFor()` handles async operations
- `clearAllMocks()` prevents test pollution

## Mock Data Patterns

Create reusable mock factories for maintainability:

```typescript
// mocks/graphql/productMocks.ts

export const createProductMock = (
  productId: string,
  overrides?: Partial<Product>
): GetProductDetailsQuery => ({
  customer: {
    plans: [
      {
        items: [
          {
            product: {
              id: productId,
              name: 'Test Product',
              price: { amount: 1299, currency: 'USD' },
              description: 'Test description',
              inStock: true,
              ...overrides,
            },
          },
        ],
      },
    ],
  },
});

// Usage in tests
describe('ProductList', () => {
  it('should display out of stock message', async () => {
    const outOfStockProduct = createProductMock('product-123', {
      inStock: false,
    });

    const mockResponse = {
      request: { query: GetProductsDocument },
      result: { data: outOfStockProduct },
    };

    render(
      <MockedProvider mocks={[mockResponse]} addTypename={false}>
        <ProductList />
      </MockedProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('Out of Stock')).toBeTruthy();
    });
  });

  it('should display custom product name', async () => {
    const customProduct = createProductMock('product-456', {
      name: 'Premium Meal Kit',
    });

    // ... rest of test
  });
});
```

**Why**: Parametric factories reduce duplication and make tests more maintainable.

## Testing Async Operations

Always use `waitFor()` for async behavior:

```typescript
describe('AsyncComponent', () => {
  // ❌ BAD - Will fail or be flaky
  it('should display loaded data', () => {
    render(<AsyncComponent />);
    expect(screen.getByText('Data loaded')).toBeTruthy(); // Fails - data not loaded yet
  });

  // ✅ GOOD - Waits for async operation
  it('should display loaded data', async () => {
    render(<AsyncComponent />);

    await waitFor(() => {
      expect(screen.getByText('Data loaded')).toBeTruthy();
    });
  });

  // ✅ GOOD - Check loading state first, then loaded state
  it('should show loading then data', async () => {
    render(<AsyncComponent />);

    // Check initial loading state
    expect(screen.getByTestId('loading-spinner')).toBeTruthy();

    // Wait for data to load
    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).toBeNull();
      expect(screen.getByText('Data loaded')).toBeTruthy();
    });
  });
});
```

## Common Mistakes to Avoid

❌ **Don't share query clients across tests**:

```typescript
// BAD - Causes test pollution
const globalQueryClient = new QueryClient();

describe('MyTests', () => {
  it('test 1', () => {
    // Uses global client - cached data affects other tests
  });
});
```

❌ **Don't mock Apollo Client directly**:

```typescript
// BAD - Breaks abstraction
jest.mock('@apollo/client', () => ({
  useQuery: jest.fn(),
}));
```

❌ **Don't ignore async operations**:

```typescript
// BAD - Race condition
it('should display data', () => {
  render(<Component />);
  expect(screen.getByText('Loaded')).toBeTruthy(); // Fails
});
```

✅ **Do use proper async testing**:

```typescript
// GOOD
it('should display data', async () => {
  render(<Component />);
  await waitFor(() => {
    expect(screen.getByText('Loaded')).toBeTruthy();
  });
});
```

✅ **Do create isolated query clients**:

```typescript
// GOOD - Each test gets fresh client
const QueryWrapper = ({ children }) => {
  const queryClient = createTestQueryClient();
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
};
```

✅ **Do use MockedProvider for GraphQL**:

```typescript
// GOOD
render(
  <MockedProvider mocks={[mockResponse]} addTypename={false}>
    <Component />
  </MockedProvider>
);
```

## Testing Checklist

For each test, verify:

- [ ] Native modules mocked in jest.setup.ts
- [ ] GraphQL tests use MockedProvider
- [ ] TanStack Query tests use isolated QueryClient
- [ ] All async operations use waitFor()
- [ ] Both loading and error states tested
- [ ] Mutations tested with act()
- [ ] Mock data uses parametric factories
- [ ] No shared state between tests

## Quick Reference

**GraphQL**: Use `MockedProvider` with `addTypename={false}`

**TanStack Query**: Create isolated `QueryClient` with `retry: false, gcTime: 0`

**Async Testing**: Always use `waitFor()` for async operations

**Mutations**: Wrap in `act()` and verify with `waitFor()`

**Mock Data**: Use parametric factory functions

**Key Libraries**:
- Jest 29.7.0
- @testing-library/react-native 12.9.0
- Apollo Client 3.13.6
- TanStack Query 5.59.16

For production examples, see [references/examples.md](references/examples.md).
For testing library docs, see [references/api-docs.md](references/api-docs.md).
