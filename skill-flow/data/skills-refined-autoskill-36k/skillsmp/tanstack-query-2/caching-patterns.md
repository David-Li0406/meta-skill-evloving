# Caching Patterns Reference

## staleTime vs gcTime

```tsx
// staleTime: How long data is considered "fresh"
// - Fresh data won't trigger background refetch
// - Default: 0 (always stale)

// gcTime (garbage collection time): How long unused data stays in cache
// - After component unmounts, data stays in cache for this duration
// - Default: 5 minutes

// Static data (rarely changes)
queryOptions({
  queryKey: ['categories'],
  queryFn: getCategories,
  staleTime: 1000 * 60 * 60, // Fresh for 1 hour
  gcTime: 1000 * 60 * 60 * 24, // Keep in cache for 24 hours
});

// Frequently updated data
queryOptions({
  queryKey: ['notifications'],
  queryFn: getNotifications,
  staleTime: 1000 * 30, // Fresh for 30 seconds
  gcTime: 1000 * 60 * 5, // 5 minutes (default)
  refetchInterval: 1000 * 60, // Poll every minute
});

// User-specific data (balance between fresh and performance)
queryOptions({
  queryKey: ['user', 'profile'],
  queryFn: getProfile,
  staleTime: 1000 * 60 * 5, // Fresh for 5 minutes
  refetchOnWindowFocus: true, // Refetch when user returns
});
```

## Query Key Scoping

```tsx
// Hierarchical key structure enables smart invalidation
const queryKeys = {
  posts: {
    all: ['posts'] as const,
    lists: () => [...queryKeys.posts.all, 'list'] as const,
    list: (filters: PostFilters) =>
      [...queryKeys.posts.lists(), filters] as const,
    details: () => [...queryKeys.posts.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.posts.details(), id] as const,
  },
} as const;

// Usage
useQuery({
  queryKey: queryKeys.posts.detail('123'),
  queryFn: () => getPost('123'),
});

// Invalidation patterns
queryClient.invalidateQueries({ queryKey: queryKeys.posts.all }); // All posts queries
queryClient.invalidateQueries({ queryKey: queryKeys.posts.lists() }); // All list queries
queryClient.invalidateQueries({ queryKey: queryKeys.posts.detail('123') }); // Single post
```

## Background Refetch Patterns

```tsx
// Refetch strategies
queryOptions({
  queryKey: ['data'],
  queryFn: fetchData,

  // Refetch when window regains focus (default: true)
  refetchOnWindowFocus: true,

  // Refetch when network reconnects (default: true)
  refetchOnReconnect: true,

  // Refetch when component mounts (default: true)
  refetchOnMount: true,

  // Polling interval (disabled by default)
  refetchInterval: 1000 * 60, // Every minute

  // Only poll when window is focused
  refetchIntervalInBackground: false,
});

// Conditional polling
const { data } = useQuery({
  queryKey: ['job', jobId],
  queryFn: () => getJobStatus(jobId),
  refetchInterval: (query) => {
    // Stop polling when job is complete
    return query.state.data?.status === 'completed' ? false : 1000;
  },
});
```

## Query Invalidation

```tsx
const queryClient = useQueryClient();

// Invalidate single query
queryClient.invalidateQueries({ queryKey: ['posts', '123'] });

// Invalidate all posts queries
queryClient.invalidateQueries({ queryKey: ['posts'] });

// Invalidate with exact match
queryClient.invalidateQueries({ queryKey: ['posts'], exact: true });

// Invalidate multiple query types
await Promise.all([
  queryClient.invalidateQueries({ queryKey: ['posts'] }),
  queryClient.invalidateQueries({ queryKey: ['comments'] }),
]);

// Control refetch behavior
queryClient.invalidateQueries({
  queryKey: ['posts'],
  refetchType: 'active', // 'active' | 'inactive' | 'all' | 'none'
});
```

## placeholderData vs initialData

| Aspect           | placeholderData                      | initialData                |
| ---------------- | ------------------------------------ | -------------------------- |
| Level            | Observer (component)                 | Cache (global)             |
| Persistence      | Never cached                         | Persisted to cache         |
| Refetch Behavior | Always triggers background refetch   | Respects `staleTime`       |
| Error Handling   | Becomes `undefined` on fetch failure | Remains available on error |
| Flag             | `isPlaceholderData: true`            | No special flag            |

### initialData (Cache-Level)

Data "as good as if fetched from backend" - persisted and respects staleness:

```tsx
useQuery({
  queryKey: ['todo', id],
  queryFn: () => fetchTodo(id),
  initialData: { id, name: 'Loading...', completed: false },
  staleTime: 1000 * 60, // Won't refetch for 1 minute!
});
```

**Warning:** With `staleTime`, initial data is considered "fresh" - no immediate refetch.

### placeholderData (Observer-Level)

Temporary "fake" data shown while real data loads:

```tsx
const { data, isPlaceholderData } = useQuery({
  queryKey: ['todo', id],
  queryFn: () => fetchTodo(id),
  placeholderData: { id, name: 'Loading...', completed: false },
});

// Can style differently based on placeholder state
<div className={isPlaceholderData ? 'opacity-50' : ''}>{data?.name}</div>;
```

### initialDataUpdatedAt

Tell React Query when initial data was last updated for staleness calculation:

```tsx
useQuery({
  queryKey: ['todo', id],
  queryFn: () => fetchTodo(id),
  initialData: cachedTodo,
  initialDataUpdatedAt: cachedTodo.lastUpdated, // Timestamp
  staleTime: 1000 * 60,
});
```

## Cache Seeding

### Pull Approach: initialData from Cache

Look up existing cache data when rendering detail views:

```tsx
function useTodo(id: string) {
  const queryClient = useQueryClient();

  return useQuery({
    queryKey: ['todos', 'detail', id],
    queryFn: () => fetchTodo(id),
    initialData: () => {
      // Pull from list cache if available
      const todos = queryClient.getQueryData<Todo[]>(['todos', 'list']);
      return todos?.find((todo) => todo.id === id);
    },
    initialDataUpdatedAt: () => {
      // Use list query's update time for staleness
      return queryClient.getQueryState(['todos', 'list'])?.dataUpdatedAt;
    },
  });
}
```

**Pros:** Just-in-time seeding, no wasted cache entries
**Cons:** Requires manual staleness management

### Push Approach: setQueryData in queryFn

Populate detail caches when fetching list data:

```tsx
function useTodos() {
  const queryClient = useQueryClient();

  return useQuery({
    queryKey: ['todos', 'list'],
    queryFn: async () => {
      const todos = await fetchTodos();

      // Push each todo into detail cache
      for (const todo of todos) {
        queryClient.setQueryData(['todos', 'detail', todo.id], todo);
      }

      return todos;
    },
  });
}
```

**Pros:** Automatic staleness tracking from fetch time
**Cons:** Creates cache entries that may never be used

### Preventing Suspense Waterfalls

Use `prefetchQuery` to avoid sequential suspensions:

```tsx
// In route loader
async function loader({ context: { queryClient } }) {
  // Start both fetches in parallel
  await Promise.all([
    queryClient.prefetchQuery(todosOptions()),
    queryClient.prefetchQuery(userOptions()),
  ]);
}

// In component - both resolve together
function Dashboard() {
  const todos = useSuspenseQuery(todosOptions());
  const user = useSuspenseQuery(userOptions());
  // ...
}
```
