# TanStack Query API Reference

**Version**: 5.59.16 (formerly React Query)

## Official Documentation

- **Overview**: https://tanstack.com/query/latest/docs/framework/react/overview
- **Queries**: https://tanstack.com/query/latest/docs/framework/react/guides/queries
- **Mutations**: https://tanstack.com/query/latest/docs/framework/react/guides/mutations
- **Query Invalidation**: https://tanstack.com/query/latest/docs/framework/react/guides/query-invalidation
- **Testing**: https://tanstack.com/query/latest/docs/framework/react/guides/testing

## Core Hooks

### useQuery

Fetch and cache server state with automatic background refetching.

```typescript
const { data, isLoading, error, refetch, isError } = useQuery({
  queryKey: ['recipes', id],
  queryFn: () => fetchRecipe(id),
  enabled: !!id,
  staleTime: 5 * 60 * 1000,
  gcTime: 10 * 60 * 1000,
  retry: 3,
  refetchOnWindowFocus: true,
  refetchOnReconnect: true,
});
```

**Key Options**:
- `queryKey` - Unique array key for caching (required)
- `queryFn` - Function that returns a Promise (required)
- `enabled` - Boolean to enable/disable query
- `staleTime` - Time before data considered stale (ms)
- `gcTime` - Garbage collection time for unused cache (ms, formerly `cacheTime`)
- `retry` - Number of retry attempts or retry function
- `retryDelay` - Delay between retries (ms or function)
- `refetchOnWindowFocus` - Refetch on window focus
- `refetchOnReconnect` - Refetch on network reconnect
- `refetchInterval` - Polling interval (ms)
- `select` - Transform/select data

**Return Values**:
- `data` - Query result data
- `isLoading` - True on first fetch (no cached data)
- `isFetching` - True during any fetch (including background)
- `isError` - True if query failed
- `error` - Error object if query failed
- `status` - `'pending'` | `'error'` | `'success'`
- `refetch()` - Manual refetch function
- `fetchStatus` - `'fetching'` | `'paused'` | `'idle'`

### useMutation

Execute mutations with automatic cache invalidation.

```typescript
const { mutate, mutateAsync, isPending, isError } = useMutation({
  mutationFn: (data) => createRecipe(data),
  onSuccess: (data, variables, context) => {
    queryClient.invalidateQueries({ queryKey: ['recipes'] });
  },
  onError: (error, variables, context) => {
    console.error(error);
  },
  onMutate: async (variables) => {
    // Optimistic update
    await queryClient.cancelQueries({ queryKey: ['recipes'] });
    const previous = queryClient.getQueryData(['recipes']);
    queryClient.setQueryData(['recipes'], (old) => [...old, variables]);
    return { previous };
  },
  retry: 3,
});

// Execute mutation
mutate({ title: 'New Recipe' });

// With promise
const data = await mutateAsync({ title: 'New Recipe' });
```

**Key Options**:
- `mutationFn` - Function that performs mutation (required)
- `onSuccess` - Success callback with data, variables, context
- `onError` - Error callback with error, variables, context
- `onMutate` - Pre-mutation callback for optimistic updates
- `onSettled` - Always runs after success or error
- `retry` - Number of retry attempts
- `retryDelay` - Delay between retries (ms)

**Return Values**:
- `mutate()` - Execute mutation (fire-and-forget)
- `mutateAsync()` - Execute mutation (returns promise)
- `isPending` - Mutation in progress
- `isError` - Mutation failed
- `isSuccess` - Mutation succeeded
- `error` - Error object
- `data` - Mutation result data
- `reset()` - Reset mutation state
- `status` - `'idle'` | `'pending'` | `'error'` | `'success'`

### useInfiniteQuery

Pagination and infinite scrolling queries.

```typescript
const {
  data,
  fetchNextPage,
  hasNextPage,
  isFetchingNextPage,
} = useInfiniteQuery({
  queryKey: ['recipes', 'infinite'],
  queryFn: ({ pageParam }) => fetchRecipes(pageParam),
  initialPageParam: 0,
  getNextPageParam: (lastPage, pages) => lastPage.nextCursor,
  getPreviousPageParam: (firstPage, pages) => firstPage.prevCursor,
});
```

**Key Options**:
- `initialPageParam` - Initial page parameter (required in v5)
- `getNextPageParam` - Function to get next page param
- `getPreviousPageParam` - Function to get previous page param
- All `useQuery` options apply

**Return Values**:
- `data.pages` - Array of page results
- `data.pageParams` - Array of page params used
- `fetchNextPage()` - Fetch next page
- `fetchPreviousPage()` - Fetch previous page
- `hasNextPage` - Whether next page exists
- `hasPreviousPage` - Whether previous page exists
- `isFetchingNextPage` - Fetching next page
- `isFetchingPreviousPage` - Fetching previous page

## Query Client

### Creating Query Client

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      gcTime: 10 * 60 * 1000,
      retry: 3,
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 3,
    },
  },
});

<QueryClientProvider client={queryClient}>
  <App />
</QueryClientProvider>
```

### Query Invalidation

```typescript
// Invalidate all queries
queryClient.invalidateQueries();

// Invalidate specific queries
queryClient.invalidateQueries({ queryKey: ['recipes'] });

// Invalidate with exact match
queryClient.invalidateQueries({
  queryKey: ['recipes', id],
  exact: true
});

// Invalidate and refetch
queryClient.invalidateQueries({
  queryKey: ['recipes'],
  refetchType: 'active' // 'active' | 'inactive' | 'all' | 'none'
});
```

### Manual Cache Updates

```typescript
// Set query data
queryClient.setQueryData(['recipes', id], newData);

// Update query data
queryClient.setQueryData(['recipes'], (old) => {
  return old.map(recipe =>
    recipe.id === id ? { ...recipe, ...updates } : recipe
  );
});

// Get query data
const data = queryClient.getQueryData(['recipes', id]);

// Cancel queries
queryClient.cancelQueries({ queryKey: ['recipes'] });

// Remove queries from cache
queryClient.removeQueries({ queryKey: ['recipes', id] });

// Reset queries
queryClient.resetQueries({ queryKey: ['recipes'] });

// Refetch queries
queryClient.refetchQueries({ queryKey: ['recipes'] });
```

### Prefetching

```typescript
// Prefetch query
await queryClient.prefetchQuery({
  queryKey: ['recipe', id],
  queryFn: () => fetchRecipe(id),
  staleTime: 5 * 60 * 1000,
});

// Prefetch infinite query
await queryClient.prefetchInfiniteQuery({
  queryKey: ['recipes', 'infinite'],
  queryFn: ({ pageParam }) => fetchRecipes(pageParam),
  initialPageParam: 0,
});
```

## Query Keys

### Key Structure

```typescript
// Simple key
['recipes']

// Key with ID
['recipes', id]

// Key with filters
['recipes', { status: 'active', category: 'dinner' }]

// Nested keys
['users', userId, 'recipes', recipeId]
```

### Key Matching

```typescript
// Exact match
['recipes', '123']

// Partial match (matches all recipes queries)
['recipes']

// With filters
['recipes', { status: 'active' }] // matches any query starting with ['recipes']
```

## Error Handling

### Retry Configuration

```typescript
useQuery({
  queryKey: ['recipe', id],
  queryFn: fetchRecipe,
  retry: (failureCount, error) => {
    // Don't retry on 404
    if (error.status === 404) return false;
    // Retry up to 3 times
    return failureCount < 3;
  },
  retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
});
```

### Global Error Handler

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      throwOnError: false,
      retry: (failureCount, error) => {
        if (error.status === 404 || error.status === 403) return false;
        return failureCount < 3;
      },
    },
  },
});
```

## Optimistic Updates

```typescript
useMutation({
  mutationFn: updateRecipe,
  onMutate: async (newRecipe) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['recipes', newRecipe.id] });

    // Snapshot previous value
    const previousRecipe = queryClient.getQueryData(['recipes', newRecipe.id]);

    // Optimistically update
    queryClient.setQueryData(['recipes', newRecipe.id], newRecipe);

    // Return context with snapshot
    return { previousRecipe };
  },
  onError: (err, newRecipe, context) => {
    // Rollback on error
    queryClient.setQueryData(
      ['recipes', newRecipe.id],
      context.previousRecipe
    );
  },
  onSettled: (newRecipe) => {
    // Refetch after error or success
    queryClient.invalidateQueries({ queryKey: ['recipes', newRecipe.id] });
  },
});
```

## Testing Patterns

### Creating Test Query Client

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      gcTime: Infinity,
    },
    mutations: {
      retry: false,
    },
  },
  logger: {
    log: console.log,
    warn: console.warn,
    error: () => {}, // Silence errors in tests
  },
});

const wrapper = ({ children }) => (
  <QueryClientProvider client={createTestQueryClient()}>
    {children}
  </QueryClientProvider>
);

render(<Component />, { wrapper });
```

### Waiting for Queries

```typescript
import { waitFor } from '@testing-library/react-native';

await waitFor(() => {
  expect(screen.getByText('Recipe Title')).toBeTruthy();
});
```

## Common Patterns

### Dependent Queries

```typescript
const { data: user } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
});

const { data: recipes } = useQuery({
  queryKey: ['recipes', user?.id],
  queryFn: () => fetchUserRecipes(user.id),
  enabled: !!user?.id, // Only run when user is loaded
});
```

### Parallel Queries

```typescript
const queries = useQueries({
  queries: [
    { queryKey: ['recipe', id1], queryFn: () => fetchRecipe(id1) },
    { queryKey: ['recipe', id2], queryFn: () => fetchRecipe(id2) },
  ],
});

const isLoading = queries.some(q => q.isLoading);
const data = queries.map(q => q.data);
```

### Select Data Transformation

```typescript
const { data: recipeTitles } = useQuery({
  queryKey: ['recipes'],
  queryFn: fetchRecipes,
  select: (data) => data.map(recipe => recipe.title),
});
```

## Version 5 Breaking Changes

**Key Changes from v4 to v5**:
- `cacheTime` renamed to `gcTime`
- `isLoading` and `isFetching` are now separate states
- `initialPageParam` required for infinite queries
- Query keys must be arrays (no single string keys)
- `onSuccess`, `onError`, `onSettled` callbacks moved from query to mutation only
- `useErrorBoundary` renamed to `throwOnError`

## Key Considerations

- Always use array query keys for consistency
- Invalidate queries after mutations for fresh data
- Use `select` for data transformation to avoid unnecessary re-renders
- Leverage `staleTime` to reduce network requests
- Use `enabled` for dependent queries
- Implement optimistic updates for better UX
- Test with custom query client that disables retries
- Use `gcTime` to manage memory for cached data
