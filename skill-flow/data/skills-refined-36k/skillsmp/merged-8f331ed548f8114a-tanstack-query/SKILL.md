---
name: tanstack-query
description: Use this skill when managing server state with TanStack Query v5. Covers query key factories, data transformation, mutations, optimistic updates, authentication, testing with MSW, and best practices for async state management.
---

# TanStack Query v5 - Complete Guide

**TanStack Query v5** (October 2023) is the async state manager for this project. It requires React 18+, features first-class Suspense support, improved TypeScript inference, and a 20% smaller bundle. This section covers production-ready patterns based on official documentation and community best practices.

### Breaking Changes in v5

**Key updates you need to know:**

1. **Single Object Signature**: All hooks now accept one configuration object:
   ```typescript
   // ✅ v5 - single object
   useQuery({ queryKey, queryFn, ...options })

   // ❌ v4 - multiple overloads (deprecated)
   useQuery(queryKey, queryFn, options)
   ```

2. **Renamed Options**:
   - `cacheTime` → `gcTime` (garbage collection time)
   - `keepPreviousData` → `placeholderData: keepPreviousData`
   - `isLoading` now means `isPending && isFetching`

3. **Callbacks Removed from useQuery**:
   - `onSuccess`, `onError`, `onSettled` removed from `useQuery`
   - Use global QueryCache callbacks instead
   - Prevents duplicate executions

4. **Infinite Queries Require initialPageParam**:
   - No default value provided
   - Must explicitly set `initialPageParam` (e.g., `0` or `null`)

5. **First-Class Suspense**:
   - New dedicated hooks: `useSuspenseQuery`, `useSuspenseInfiniteQuery`
   - No experimental flag needed
   - Data is never undefined at type level

**Migration**: Use the official codemod for automatic migration: `npx @tanstack/query-codemods v5/replace-import-specifier`

### Smart Defaults

Query v5 ships with production-ready defaults:

```typescript
{
  staleTime: 0,              // Data instantly stale (refetch on mount)
  gcTime: 5 * 60_000,        // Keep unused cache for 5 minutes
  retry: 3,                  // 3 retries with exponential backoff
  refetchOnWindowFocus: true,// Refetch when user returns to tab
  refetchOnReconnect: true,  // Refetch when network reconnects
}
```

**Philosophy**: React Query is an **async state manager, not a data fetcher**. You provide the Promise; Query manages caching, background updates, and synchronization.

### Client Setup

```typescript
// src/app/providers.tsx
import { QueryClient, QueryClientProvider, QueryCache } from '@tanstack/react-query'
import { toast } from './toast' // Your notification system

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 0,          // Adjust per-query
      gcTime: 5 * 60_000,    // 5 minutes (v5: formerly cacheTime)
      retry: (failureCount, error) => {
        // Don't retry on 401 (authentication errors)
        if (error?.response?.status === 401) return false
        return failureCount < 3
      },
    },
  },
  queryCache: new QueryCache({
    onError: (error, query) => {
      // Only show toast for background errors (when data exists)
      if (query.state.data !== undefined) {
        toast.error(`Something went wrong: ${error.message}`)
      }
    },
  }),
})

export function AppProviders({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}
```

**DevTools Setup** (auto-excluded in production):

```typescript
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

<QueryClientProvider client={queryClient}>
  {children}
  <ReactQueryDevtools initialIsOpen={false} />
</QueryClientProvider>
```

### Architecture: Feature-Based Colocation

**Recommended pattern**: Group queries with related features, not by file type.

```
src/features/
├── Todos/
│   ├── index.tsx           # Feature entry point
│   ├── queries.ts          # All React Query logic (keys, functions, hooks)
│   ├── types.ts            # TypeScript types
│   └── components/         # Feature-specific components
```

**Export only custom hooks** from query files. Keep query functions and keys private:

```typescript
// features/todos/queries.ts

// 1. Query Key Factory (hierarchical structure)
const todoKeys = {
  all: ['todos'] as const,
  lists: () => [...todoKeys.all, 'list'] as const,
  list: (filters: string) => [...todoKeys.lists(), { filters }] as const,
  details: () => [...todoKeys.all, 'detail'] as const,
  detail: (id: number) => [...todoKeys.details(), id] as const,
}

// 2. Query Function (private)
const fetchTodos = async (filters: string): Promise<Todo[]> => {
  const response = await axios.get('/api/todos', { params: { filters } })
  return response.data
}

// 3. Custom Hook (public API)
export const useTodosQuery = (filters: string) => {
  return useQuery({
    queryKey: todoKeys.list(filters),
    queryFn: () => fetchTodos(filters),
    staleTime: 30_000, // Fresh for 30 seconds
  })
}
```

**Benefits**:
- Prevents key/function mismatches
- Clean public API
- Encapsulation and maintainability
- Easy to locate all query logic for a feature

### Query Key Factories (Essential)

**Structure keys hierarchically** from generic to specific:

```typescript
// ✅ Correct hierarchy
['todos']                          // Invalidates everything
['todos', 'list']                  // Invalidates all lists
['todos', 'list', { filters }]     // Invalidates specific list
['todos', 'detail', 1]             // Invalidates specific detail

// ❌ Wrong - flat structure
['todos-list-active']              // Can't partially invalidate
```

**Critical rule**: Query keys must include **ALL variables used in queryFn**. Treat query keys like dependency arrays:

```typescript
// ✅ Correct - includes all variables
const { data } = useQuery({
  queryKey: ['todos', filters, sortBy],
  queryFn: () => fetchTodos(filters, sortBy),
})

// ❌ Wrong - missing variables
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: () => fetchTodos(filters, sortBy), // filters/sortBy not in key!
})
```

**Type consistency matters**: `['todos', '1']` and `['todos', 1]` are **different keys**. Be consistent with types.

### Query Options API (Type Safety)

**The modern pattern** for maximum type safety across your codebase:

```typescript
import { queryOptions } from '@tanstack/react-query'

function todoOptions(id: number) {
  return queryOptions({
    queryKey: ['todos', id],
    queryFn: () => fetchTodo(id),
    staleTime: 5000,
  })
}

// ✅ Use everywhere with full type safety
useQuery(todoOptions(1))
queryClient.prefetchQuery(todoOptions(5))
queryClient.setQueryData(todoOptions(42).queryKey, newTodo)
queryClient.getQueryData(todoOptions(42).queryKey) // Fully typed!
```

**Benefits**:
- Single source of truth for query configuration
- Full TypeScript inference for imperatively accessed data
- Reusable across hooks and imperative methods
- Prevents key/function mismatches

### Data Transformation Strategies

Choose the right approach based on your use case:

**1. Transform in queryFn** - Simple cases where cache should store transformed data:

```typescript
const fetchTodos = async (): Promise<Todo[]> => {
  const response = await axios.get('/api/todos')
  return response.data.map(todo => ({
    ...todo,
    name: todo.name.toUpperCase()
  }))
}
```

**2. Transform with `select` option (RECOMMENDED)** - Enables partial subscriptions:

```typescript
// Only re-renders when filtered data changes
export const useTodosQuery = (filters: string) =>
  useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
    select: (data) => data.filter(todo => todo.status === filters),
  })

// Only re-renders when count changes
export const useTodosCount = () =>
  useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
    select: (data) => data.length,
  })
```

**⚠️ Memoize select functions** to prevent running on every render:

```typescript
// ✅ Stable reference
const transformTodos = (data: Todo[]) => expensiveTransform(data)

const query = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  select: transformTodos, // Stable function reference
})

// ❌ Runs on every render
const query = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  select: (data) => expensiveTransform(data), // New function every render
})
```

### TypeScript Best Practices

**Let TypeScript infer types** from queryFn rather than specifying generics:

```typescript
// ✅ Recommended - inference
const { data } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos, // Returns Promise<Todo[]>
})
// data is Todo[] | undefined

// ❌ Unnecessary - explicit generics
const { data } = useQuery<Todo[]>({
  queryKey: ['todos'],
  queryFn: fetchTodos,
})
```

**Discriminated unions** automatically narrow types:

```typescript
const { data, isSuccess, isError, error } = useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
})

if (isSuccess) {
  // data is Todo[] (never undefined)
}

if (isError) {
  // error is defined
}
```

Use `queryOptions` helper for maximum type safety across imperative methods.

### Custom Hooks Pattern

**Always create custom hooks** even for single queries:

```typescript
// ✅ Recommended - custom hook with encapsulation
export function usePost(
  id: number,
  options?: Omit<UseQueryOptions<Post>, 'queryKey' | 'queryFn'>
) {
  return useQuery({
    queryKey: ['posts', id],
    queryFn: () => getPost(id),
    ...options,
  })
}

// Usage: allows callers to override any option except key/fn
const { data } = usePost(42, { staleTime: 10_000 })
```

**Benefits**:
- Centralizes query logic
- Easy to update all usages
- Consistent configuration
- Better testing

### Error Handling (Multi-Layer Strategy)

**Layer 1: Component-Level** - Specific user feedback:

```typescript
function TodoList() {
  const { data, error, isError, isLoading } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  })

  if (isLoading) return <Spinner />
  if (isError) return <ErrorAlert>{error.message}</ErrorAlert>

  return <ul>{data.map(todo => <TodoItem key={todo.id} {...todo} />)}</ul>
}
```

**Layer 2: Global Error Handling** - Background errors via QueryCache:

```typescript
// Already configured in client setup above
queryCache: new QueryCache({
  onError: (error, query) => {
    if (query.state.data !== undefined) {
      toast.error(`Background error: ${error.message}`)
    }
  },
})
```

**Layer 3: Error Boundaries** - Catch render errors:

```typescript
import { QueryErrorResetBoundary } from '@tanstack/react-query'
import { ErrorBoundary } from 'react-error-boundary'

<QueryErrorResetBoundary>
  {({ reset }) => (
    <ErrorBoundary
      onReset={reset}
      fallbackRender={({ error, resetErrorBoundary }) => (
        <div>
          <p>Error: {error.message}</p>
          <button onClick={resetErrorBoundary}>Try again</button>
        </div>
      )}
    >
      <TodoList />
    </ErrorBoundary>
  )}
</QueryErrorResetBoundary>
```

### Suspense Integration

**First-class Suspense support** in v5 with dedicated hooks:

```typescript
import { useSuspenseQuery } from '@tanstack/react-query'

function TodoList() {
  // data is NEVER undefined (type-safe)
  const { data } = useSuspenseQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  })

  return <ul>{data.map(todo => <TodoItem key={todo.id} {...todo} />)}</ul>
}

// Wrap with Suspense boundary
function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <TodoList />
    </Suspense>
  )
}
```

**Benefits**:
- Eliminates loading state management
- Data always defined (TypeScript enforced)
- Cleaner component code
- Works with React.lazy for code-splitting

### Mutations with Optimistic Updates

**Basic mutation** with cache invalidation:

```typescript
export function useCreateTodo() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (newTodo: CreateTodoDTO) =>
      api.post('/todos', newTodo).then(res => res.data),
    onSuccess: (data) => {
      // Set detail query immediately
      queryClient.setQueryData(['todos', data.id], data)
      // Invalidate list queries
      queryClient.invalidateQueries({ queryKey: ['todos', 'list'] })
    },
  })
}
```

**Simple optimistic updates** using `variables`:

```typescript
const addTodoMutation = useMutation({
  mutationFn: (newTodo: string) => axios.post('/api/todos', { text: newTodo }),
  onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] }),
})

const { isPending, variables, mutate } = addTodoMutation

return (
  <ul>
    {todoQuery.data?.map(todo => <li key={todo.id}>{todo.text}</li>)}
    {isPending && <li style={{ opacity: 0.5 }}>{variables}</li>}
  </ul>
)
```

**Advanced optimistic updates** with rollback:

```typescript
useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    // Cancel outgoing queries (prevent race conditions)
    await queryClient.cancelQueries({ queryKey: ['todos'] })

    // Snapshot current data
    const previousTodos = queryClient.getQueryData(['todos'])

    // Optimistically update cache
    queryClient.setQueryData(['todos'], (old: Todo[]) =>
      old?.map(todo => todo.id === newTodo.id ? newTodo : todo)
    )

    // Return context for rollback
    return { previousTodos }
  },
  onError: (err, newTodo, context) => {
    // Rollback on error
    queryClient.setQueryData(['todos'], context?.previousTodos)
    toast.error('Update failed. Changes reverted.')
  },
  onSettled: () => {
    // Always refetch to ensure consistency
    queryClient.invalidateQueries({ queryKey: ['todos'] })
  },
})
```

**Key principles**:
- Cancel ongoing queries in `onMutate` to prevent race conditions
- Snapshot previous data before updating
- Restore snapshot on error
- Always invalidate in `onSettled` for eventual consistency
- **Never mutate cached data directly** - always use immutable updates

### Authentication Integration

**Handle token refresh at HTTP client level** (not React Query):

```typescript
// src/lib/api-client.ts
import axios from 'axios'
import createAuthRefreshInterceptor from 'axios-auth-refresh'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
})

// Add token to requests
api