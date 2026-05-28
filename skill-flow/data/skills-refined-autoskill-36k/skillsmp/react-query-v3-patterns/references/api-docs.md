# React Query v3 API Reference

**Version**: react-query v3.39.0 (NOT TanStack Query v5!)

## Official Documentation

- **v3 Docs**: https://react-query-v3.tanstack.com/
- **Guides**: https://react-query-v3.tanstack.com/guides/queries
- **API Reference**: https://react-query-v3.tanstack.com/reference/useQuery

**IMPORTANT**: This codebase uses react-query v3.39.0. DO NOT use TanStack Query v5 documentation.

## Core Imports

```typescript
// v3 imports (correct for this codebase)
import { useQuery, useMutation, useQueryClient } from 'react-query';

// ❌ Wrong - v5 syntax
import { useQuery } from '@tanstack/react-query';
```

## useQuery

Fetch and cache data.

```typescript
const {
  data,
  error,
  isLoading,
  isFetching,
  isSuccess,
  isError,
  refetch,
} = useQuery(queryKey, queryFn, options);
```

**Parameters**:
- `queryKey: string | [string, object]` - Unique key for caching
- `queryFn: () => Promise<T>` - Function that returns Promise
- `options?: UseQueryOptions` - Configuration

**Returns**:
- `data: T | undefined` - Query data
- `error: Error | null` - Query error
- `isLoading: boolean` - Initial load (no cached data)
- `isFetching: boolean` - Fetching (includes background refetch)
- `isSuccess: boolean` - Query succeeded
- `isError: boolean` - Query failed
- `status: 'idle' | 'loading' | 'error' | 'success'`
- `refetch: () => Promise` - Manual refetch
- `remove: () => void` - Remove query from cache

### Options

```typescript
{
  // Conditional execution
  enabled: boolean,

  // Cache behavior
  staleTime: number, // ms until data considered stale
  cacheTime: number, // ms to keep unused data in cache

  // Refetch behavior
  refetchOnMount: boolean | 'always',
  refetchOnWindowFocus: boolean | 'always',
  refetchOnReconnect: boolean | 'always',
  refetchInterval: number | false,

  // Retry
  retry: number | boolean,
  retryDelay: (attemptIndex: number) => number,

  // Callbacks
  onSuccess: (data: T) => void,
  onError: (error: Error) => void,
  onSettled: (data: T | undefined, error: Error | null) => void,

  // Advanced
  select: (data: T) => TSelected,
  keepPreviousData: boolean,
  placeholderData: T | (() => T),
  initialData: T | (() => T),
}
```

### Examples

```typescript
// Basic query
const { data, isLoading } = useQuery('todos', fetchTodos);

// With structured key
const { data } = useQuery(['todo', id], () => fetchTodo(id));

// With options
const { data } = useQuery(
  ['todo', id],
  () => fetchTodo(id),
  {
    enabled: !!id,
    staleTime: 5 * 60 * 1000,
    retry: 2,
  }
);

// With select transformation
const { data: todoTitle } = useQuery(
  ['todo', id],
  () => fetchTodo(id),
  {
    select: (data) => data.title,
  }
);
```

## useMutation

Mutate data (POST, PUT, DELETE).

```typescript
const {
  mutate,
  mutateAsync,
  data,
  error,
  isLoading,
  isSuccess,
  isError,
  reset,
} = useMutation(mutationFn, options);
```

**Parameters**:
- `mutationFn: (variables: TVariables) => Promise<TData>`
- `options?: UseMutationOptions`

**Returns**:
- `mutate: (variables, options?) => void` - Trigger mutation
- `mutateAsync: (variables, options?) => Promise` - Async version
- `data: TData | undefined` - Mutation result
- `error: Error | null` - Mutation error
- `isLoading: boolean` - Mutation in progress
- `isSuccess: boolean` - Mutation succeeded
- `isError: boolean` - Mutation failed
- `reset: () => void` - Reset mutation state

### Options

```typescript
{
  // Callbacks
  onSuccess: (data, variables, context) => void,
  onError: (error, variables, context) => void,
  onSettled: (data, error, variables, context) => void,
  onMutate: (variables) => Promise<TContext> | TContext,

  // Advanced
  retry: number | boolean,
  retryDelay: (attemptIndex: number) => number,
}
```

### Examples

```typescript
// Basic mutation
const mutation = useMutation((newTodo) => axios.post('/todos', newTodo));

mutation.mutate({ title: 'New Todo' });

// With callbacks
const mutation = useMutation(createTodo, {
  onSuccess: (data) => {
    queryClient.invalidateQueries(['todos']);
  },
  onError: (error) => {
    toast.error(error.message);
  },
});

// Async version
const mutation = useMutation(createTodo);

try {
  const data = await mutation.mutateAsync({ title: 'Todo' });
  console.log('Created:', data);
} catch (error) {
  console.error('Failed:', error);
}
```

## useQueryClient

Access QueryClient for manual cache manipulation.

```typescript
const queryClient = useQueryClient();
```

### Methods

```typescript
// Invalidate queries (trigger refetch)
queryClient.invalidateQueries('todos');
queryClient.invalidateQueries(['todos', { status: 'done' }]);

// Set query data manually
queryClient.setQueryData(['todo', id], newTodo);
queryClient.setQueryData(['todo', id], (old) => ({ ...old, done: true }));

// Get query data
const todo = queryClient.getQueryData(['todo', id]);

// Refetch queries
await queryClient.refetchQueries('todos');
await queryClient.refetchQueries({ stale: true });

// Remove queries
queryClient.removeQueries('todos');

// Cancel queries
await queryClient.cancelQueries('todos');

// Prefetch
await queryClient.prefetchQuery('todos', fetchTodos);

// Set default options
queryClient.setDefaultOptions({
  queries: {
    staleTime: 60 * 1000,
  },
});
```

## QueryClientProvider

Provide QueryClient to app.

```typescript
import { QueryClient, QueryClientProvider } from 'react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,
      retry: 2,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Routes />
    </QueryClientProvider>
  );
}
```

## Query Keys

### Structure

```typescript
// Simple string
useQuery('todos', fetchTodos);

// Array with ID
useQuery(['todo', id], () => fetchTodo(id));

// Array with object (automatically serialized)
useQuery(
  ['todos', { status: 'done', page: 1 }],
  () => fetchTodos({ status: 'done', page: 1 })
);

// Nested arrays (all values considered)
useQuery(
  [['todos', 'list'], { filter: 'done' }],
  fetchFilteredTodos
);
```

### Best Practices

```typescript
// ✅ Include all dependencies in key
useQuery(
  ['todo', id, userId],
  () => fetchTodo(id, userId)
);

// ❌ Missing dependencies
useQuery('todo', () => fetchTodo(id, userId));

// ✅ Structured format
useQuery([RequestIds['todos.list'], { status, page }], fetchTodos);
```

## Pagination

### keepPreviousData

```typescript
const [page, setPage] = useState(1);

const { data, isPreviousData } = useQuery(
  ['todos', page],
  () => fetchTodos(page),
  {
    keepPreviousData: true, // Keep old data while fetching new
  }
);

return (
  <div>
    {data?.items.map((item) => <div key={item.id}>{item.title}</div>)}

    <button
      onClick={() => setPage((old) => old - 1)}
      disabled={page === 1}
    >
      Previous
    </button>

    <button
      onClick={() => setPage((old) => old + 1)}
      disabled={isPreviousData || !data?.hasMore}
    >
      Next
    </button>
  </div>
);
```

### fetchMore (v3 syntax)

```typescript
const { data, fetchMore } = useQuery(
  'todos',
  fetchTodos,
  {
    getFetchMore: (lastPage) => lastPage.nextCursor,
  }
);

await fetchMore({ pageParam: nextCursor });
```

## Optimistic Updates

```typescript
const mutation = useMutation(updateTodo, {
  // Store current value before mutation
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries(['todos', newTodo.id]);

    const previousTodo = queryClient.getQueryData(['todos', newTodo.id]);

    queryClient.setQueryData(['todos', newTodo.id], newTodo);

    return { previousTodo };
  },

  // Revert on error
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(
      ['todos', newTodo.id],
      context.previousTodo
    );
  },

  // Refetch on success or error
  onSettled: (newTodo) => {
    queryClient.invalidateQueries(['todos', newTodo.id]);
  },
});
```

## DevTools

```typescript
import { ReactQueryDevtools } from 'react-query/devtools';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Routes />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

## TypeScript

```typescript
// Query with types
const { data } = useQuery<Todo, Error>(
  ['todo', id],
  () => fetchTodo(id)
);

// Mutation with types
const mutation = useMutation<Todo, Error, NewTodo>(
  (newTodo) => createTodo(newTodo)
);

// QueryClient methods
queryClient.setQueryData<Todo>(['todo', id], newTodo);
```

## Key Differences: v3 vs v5

**v3 (this codebase)**:
```typescript
import { useQuery } from 'react-query';

useQuery('key', fetchFn);
useQuery(['key', params], fetchFn);
```

**v5 (DON'T use)**:
```typescript
import { useQuery } from '@tanstack/react-query';

useQuery({ queryKey: ['key'], queryFn: fetchFn });
```

## Common Options

- `staleTime: 0` - Data immediately stale (default)
- `cacheTime: 5 * 60 * 1000` - Cache for 5 minutes (default)
- `enabled: false` - Don't auto-run query
- `retry: 3` - Retry failed queries 3 times (default)
- `refetchOnMount: true` - Refetch on mount if stale
- `refetchOnWindowFocus: true` - Refetch on window focus
- `keepPreviousData: false` - Don't keep old data (default)

## Key Considerations

- Use v3 syntax (NOT v5)
- Import from `'react-query'` (NOT `'@tanstack/react-query'`)
- Structured query keys: `[RequestId, params]`
- Always handle `isLoading` and `error` states
- Use `staleTime` and `cacheTime` appropriately
- Invalidate queries after mutations
- Use `keepPreviousData` for pagination
- Type your queries with TypeScript
