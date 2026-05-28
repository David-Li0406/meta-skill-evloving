# REST API Patterns

Implementation patterns and anti-patterns for REST API data fetching.

## Pattern: Always Use useFetch Hook

Use `useFetch()` hook instead of native fetch for OpenTelemetry tracing.

✅ **Good:**
```typescript
import { useFetch } from '@libs/networking-client';

export const useGetProducts = (params: GetProductsRequest) => {
  const fetch = useFetch(); // Provides OpenTelemetry tracing

  return useQuery({
    queryKey: PRODUCT_QUERY_KEYS.list(params),
    queryFn: () => getProducts(params, queryKey, fetch),
  });
};

// Service function receives traced fetch
export const getProducts = async (params, queryKey, fetch) => {
  const response = await fetch('/api/products', queryKey, {
    method: 'GET',
  });
  return await response.json();
};
```

❌ **Bad:**
```typescript
// Native fetch - no tracing, no request IDs
export const useGetProducts = (params) => {
  return useQuery({
    queryKey: ['products', params],
    queryFn: async () => {
      const response = await fetch('/api/products'); // ❌ Missing tracing
      return response.json();
    },
  });
};
```

**Why:** `useFetch`:
- Creates OpenTelemetry spans for distributed tracing
- Adds unique request IDs for debugging
- Handles authentication middleware automatically
- Provides consistent error handling

## Pattern: Hierarchical Query Keys

Use `[domain, operation, params]` structure for precise cache invalidation.

✅ **Good:**
```typescript
export const PRODUCT_QUERY_KEYS = {
  all: ['products'] as const,
  list: (params?) => ['products', 'list', params] as const,
  detail: (id: string) => ['products', 'detail', id] as const,
} as const;

// Invalidate all product queries
queryClient.invalidateQueries({ queryKey: PRODUCT_QUERY_KEYS.all });

// Invalidate only list queries
queryClient.invalidateQueries({ queryKey: PRODUCT_QUERY_KEYS.list() });

// Invalidate specific detail query
queryClient.invalidateQueries({ queryKey: PRODUCT_QUERY_KEYS.detail('123') });
```

❌ **Bad:**
```typescript
// Flat keys - hard to invalidate selectively
const queryKey = ['products']; // Too broad
const queryKey = ['productList']; // Inconsistent naming
const queryKey = ['product', id, 'random']; // Inconsistent structure
```

**Why:** Hierarchical keys enable precise cache control:
- Invalidate all queries for a domain
- Invalidate specific operation types (list vs detail)
- Invalidate specific resources by ID

## Pattern: Localize Params Automatically

Add locale/country params automatically with `useLocalizeParams`.

✅ **Good:**
```typescript
export const useGetProducts = (params: GetProductsRequest) => {
  const fetch = useFetch();
  const localizeParams = useLocalizeParams(); // Adds locale, country
  const requestParams = useMemo(
    () => ({ ...params, ...localizeParams }),
    [params, localizeParams]
  );

  return useQuery({
    queryKey: PRODUCT_QUERY_KEYS.list(requestParams),
    queryFn: () => getProducts(requestParams, queryKey, fetch),
  });
};
```

❌ **Bad:**
```typescript
// Manual locale handling in every hook
export const useGetProducts = (params, locale, country) => {
  return useQuery({
    queryKey: ['products', params, locale, country], // Repetitive
    queryFn: () => getProducts({ ...params, locale, country }),
  });
};
```

**Why:** Automatic localization:
- Reduces boilerplate in every hook
- Ensures consistent locale handling
- Makes hooks easier to use

## Pattern: Infinite Queries for Pagination

Use `useInfiniteQuery` for cursor-based pagination with infinite scroll.

✅ **Good:**
```typescript
export const useGetProductsInfinite = (params: Omit<GetProductsRequest, 'cursor'>) => {
  const fetch = useFetch();
  const localizeParams = useLocalizeParams();
  const baseParams = useMemo(
    () => ({ ...params, ...localizeParams }),
    [params, localizeParams]
  );

  return useInfiniteQuery({
    queryKey: [...PRODUCT_QUERY_KEYS.list(baseParams), 'infinite'],
    queryFn: ({ pageParam }) => {
      const requestParams = { ...baseParams, cursor: pageParam };
      const queryKey = [RequestIds['products.list'], requestParams];
      return getProducts(requestParams, queryKey, fetch);
    },
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (lastPage) => {
      return lastPage.pagination.hasMore
        ? lastPage.pagination.nextCursor
        : undefined;
    },
    staleTime: 5 * 60 * 1000,
  });
};

// Component usage
const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useGetProductsInfinite({ limit: 20 });
const products = data?.pages.flatMap(page => page.data) || [];
```

❌ **Bad:**
```typescript
// Manual pagination state management
const [page, setPage] = useState(1);
const [cursor, setCursor] = useState(undefined);
const { data } = useQuery({
  queryKey: ['products', page],
  queryFn: () => fetchProducts({ cursor }),
});

// Manual page merging
useEffect(() => {
  if (data?.pagination.nextCursor) {
    setCursor(data.pagination.nextCursor);
  }
}, [data]);
```

**Why:** `useInfiniteQuery`:
- Manages pagination state automatically
- Handles page merging
- Provides `hasNextPage` and `fetchNextPage`
- Reduces component complexity

## Pattern: Mutations with Cache Invalidation

Invalidate related queries after successful mutations.

✅ **Good:**
```typescript
export const useCreateProduct = (options?) => {
  const queryClient = useQueryClient();
  const fetch = useFetch();

  return useMutation({
    mutationFn: (params: CreateProductRequest) => {
      return createProduct(params, queryKey, fetch);
    },
    onSuccess: () => {
      // Invalidate list queries to refetch
      queryClient.invalidateQueries({ queryKey: PRODUCT_QUERY_KEYS.all });
    },
    ...options,
  });
};

// Optimistic update for better UX
export const useUpdateProduct = (options?) => {
  const queryClient = useQueryClient();
  const fetch = useFetch();

  return useMutation({
    mutationFn: (params: UpdateProductRequest) => {
      return updateProduct(params, queryKey, fetch);
    },
    onMutate: async (newProduct) => {
      // Cancel ongoing queries
      await queryClient.cancelQueries({ queryKey: PRODUCT_QUERY_KEYS.detail(newProduct.id) });

      // Snapshot previous value
      const previousProduct = queryClient.getQueryData(
        PRODUCT_QUERY_KEYS.detail(newProduct.id)
      );

      // Optimistically update
      queryClient.setQueryData(
        PRODUCT_QUERY_KEYS.detail(newProduct.id),
        newProduct
      );

      return { previousProduct };
    },
    onError: (err, newProduct, context) => {
      // Rollback on error
      queryClient.setQueryData(
        PRODUCT_QUERY_KEYS.detail(newProduct.id),
        context?.previousProduct
      );
    },
    onSettled: (newProduct) => {
      // Refetch after mutation
      queryClient.invalidateQueries({
        queryKey: PRODUCT_QUERY_KEYS.detail(newProduct.id)
      });
    },
    ...options,
  });
};
```

❌ **Bad:**
```typescript
// No cache invalidation - stale data
export const useCreateProduct = () => {
  return useMutation({
    mutationFn: createProduct,
    // Missing onSuccess - cache not updated
  });
};

// Component manually refetches
const { mutate } = useCreateProduct();
const { refetch } = useGetProducts();

mutate(newProduct, {
  onSuccess: () => refetch(), // Manual refetch in every component
});
```

**Why:** Proper cache management:
- Keeps UI in sync with server state
- Reduces manual refetch logic in components
- Enables optimistic updates for better UX

## Pattern: Stale Time Based on Data Volatility

Configure cache timing based on how frequently data changes.

✅ **Good:**
```typescript
// List data changes frequently - 5 minutes
useQuery({
  queryKey: PRODUCT_QUERY_KEYS.list(params),
  queryFn: () => getProducts(params, queryKey, fetch),
  staleTime: 5 * 60 * 1000, // 5 minutes
  gcTime: 10 * 60 * 1000, // 10 minutes - 2x stale time
});

// Detail data is stable - 10 minutes
useQuery({
  queryKey: PRODUCT_QUERY_KEYS.detail(id),
  queryFn: () => getProduct({ id }, queryKey, fetch),
  staleTime: 10 * 60 * 1000, // 10 minutes
  gcTime: 15 * 60 * 1000, // 15 minutes - 1.5x stale time
});

// Configuration data rarely changes - 30 minutes
useQuery({
  queryKey: ['app-config'],
  queryFn: () => getAppConfig(queryKey, fetch),
  staleTime: 30 * 60 * 1000, // 30 minutes
  gcTime: 60 * 60 * 1000, // 1 hour
});
```

❌ **Bad:**
```typescript
// Same timing for all queries
useQuery({
  queryKey: PRODUCT_QUERY_KEYS.list(params),
  queryFn: () => getProducts(params),
  // No stale time - refetches on every mount
});

// Too aggressive caching
useQuery({
  queryKey: PRODUCT_QUERY_KEYS.list(params),
  queryFn: () => getProducts(params),
  staleTime: Infinity, // Never refetches
});
```

**Why:** Tuned cache timing:
- Reduces unnecessary API calls
- Keeps frequently-changing data fresh
- Allows stable data to be cached longer
- `gcTime` should be 1.5x-2x `staleTime`

## Pattern: Domain-Based File Organization

Organize API code by domain with consistent structure.

✅ **Good:**
```
src/data-access/query/
├── products/
│   ├── constants.ts      # Endpoints & query keys
│   ├── service.ts        # Fetch functions
│   ├── schema.ts         # TypeScript types
│   ├── hooks.ts          # TanStack Query hooks
│   ├── hooks.test.ts     # Hook tests
│   └── index.ts          # Exports
├── customers/
│   ├── constants.ts
│   ├── service.ts
│   ├── schema.ts
│   ├── hooks.ts
│   └── index.ts
└── orders/
    ├── constants.ts
    ├── service.ts
    ├── schema.ts
    ├── hooks.ts
    └── index.ts
```

❌ **Bad:**
```
src/data-access/
├── hooks/
│   ├── useGetProducts.ts
│   ├── useGetCustomers.ts
│   └── useGetOrders.ts
├── services/
│   ├── products.ts
│   ├── customers.ts
│   └── orders.ts
└── types/
    ├── products.ts
    ├── customers.ts
    └── orders.ts
```

**Why:** Domain-based organization:
- Keeps related code together
- Easier to find files
- Clearer ownership boundaries
- Simplifies refactoring

## Anti-Pattern: Native Fetch in Components

Never call fetch directly in components or hooks.

❌ **Bad:**
```typescript
// Native fetch in component
const ProductList = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/api/products')
      .then(res => res.json())
      .then(setData);
  }, []);

  return <FlatList data={data} />;
};

// Native fetch in hook
export const useGetProducts = () => {
  return useQuery({
    queryKey: ['products'],
    queryFn: async () => {
      const response = await fetch('/api/products'); // ❌ No tracing
      return response.json();
    },
  });
};
```

✅ **Good:**
```typescript
// Use custom hook with useFetch
export const useGetProducts = (params) => {
  const fetch = useFetch(); // ✓ OpenTelemetry tracing

  return useQuery({
    queryKey: PRODUCT_QUERY_KEYS.list(params),
    queryFn: () => getProducts(params, queryKey, fetch),
  });
};

// Component uses custom hook
const ProductList = () => {
  const { data, isLoading } = useGetProducts({ limit: 20 });

  if (isLoading) return <LoadingSpinner />;
  return <FlatList data={data.data} />;
};
```

**Why:** `useFetch` provides:
- OpenTelemetry tracing
- Request ID generation
- Authentication middleware
- Consistent error handling

## Anti-Pattern: Using REST When GraphQL Exists

Always verify GraphQL schema before using REST.

❌ **Bad:**
```typescript
// REST endpoint for data available in GraphQL
export const useGetUserProfile = (userId: string) => {
  const fetch = useFetch();

  return useQuery({
    queryKey: ['user-profile', userId],
    queryFn: () => fetchUserProfileRest(userId, queryKey, fetch),
  });
};
```

✅ **Good:**
```typescript
// GraphQL query (preferred)
export const useGetUserProfile = (userId: string) => {
  return useQuery(
    gql`
      query GetUserProfile($userId: ID!) {
        user(id: $userId) {
          id
          name
          email
          avatar
        }
      }
    `,
    { userId }
  );
};

// Only use REST if NOT in GraphQL schema
export const useGetExternalRecipes = () => {
  const fetch = useFetch();
  // External recipes not in GraphQL - REST is correct
  return useQuery({
    queryKey: [RequestIds['external-recipes.list']],
    queryFn: () => getExternalRecipes({}, queryKey, fetch),
  });
};
```

**Why:** GraphQL provides:
- Better type safety
- Reduces over-fetching
- Single request for related data
- Automatic schema validation

## Anti-Pattern: Inconsistent Query Keys

Don't use inconsistent query key structures.

❌ **Bad:**
```typescript
// Inconsistent structures
useQuery({ queryKey: ['products'] });
useQuery({ queryKey: ['productList', params] });
useQuery({ queryKey: ['product', id, 'details'] });
useQuery({ queryKey: ['getProduct', id] });
useQuery({ queryKey: ['products', 'list', params, 'random'] });
```

✅ **Good:**
```typescript
// Consistent hierarchical structure
export const PRODUCT_QUERY_KEYS = {
  all: ['products'] as const,
  list: (params?) => ['products', 'list', params] as const,
  detail: (id: string) => ['products', 'detail', id] as const,
} as const;

useQuery({ queryKey: PRODUCT_QUERY_KEYS.all });
useQuery({ queryKey: PRODUCT_QUERY_KEYS.list(params) });
useQuery({ queryKey: PRODUCT_QUERY_KEYS.detail(id) });
```

**Why:** Consistent keys:
- Enable precise cache invalidation
- Make query keys predictable
- Easier to debug caching issues

## Anti-Pattern: Missing Error Handling

Always handle specific error cases in service functions.

❌ **Bad:**
```typescript
// Generic error handling
export const getProduct = async (params, queryKey, fetch) => {
  const response = await fetch(`/api/products/${params.id}`, queryKey);
  return await response.json(); // ❌ Doesn't check response.ok
};
```

✅ **Good:**
```typescript
// Specific error messages for different status codes
export const getProduct = async (params, queryKey, fetch) => {
  const response = await fetch(`/api/products/${params.id}`, queryKey);

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error(`Product ${params.id} not found`);
    }
    if (response.status === 403) {
      throw new Error('Unauthorized to view this product');
    }
    throw new Error(`Failed to fetch product: ${response.status}`);
  }

  return await response.json();
};
```

**Why:** Specific errors:
- Help debugging
- Enable better error messages to users
- Make testing easier

## Summary

**Always:**
- ✅ Use `useFetch()` for OpenTelemetry tracing
- ✅ Use hierarchical query keys `[domain, operation, params]`
- ✅ Localize params automatically with `useLocalizeParams()`
- ✅ Invalidate cache after mutations
- ✅ Tune stale time based on data volatility
- ✅ Organize by domain
- ✅ Handle specific error cases

**Never:**
- ❌ Use native fetch() directly
- ❌ Use REST when GraphQL exists
- ❌ Use inconsistent query keys
- ❌ Forget cache invalidation after mutations
- ❌ Skip error handling
