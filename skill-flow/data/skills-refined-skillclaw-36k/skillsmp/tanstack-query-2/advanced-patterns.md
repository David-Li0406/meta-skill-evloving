# Advanced Patterns Reference

## Offline Mode

### Network Mode Options

React Query v4+ provides three `networkMode` settings:

| Mode               | Behavior                                               |
| ------------------ | ------------------------------------------------------ |
| `online` (default) | Queries pause when offline, resume when online         |
| `always`           | Queries always fire regardless of network              |
| `offlineFirst`     | First request always fires, retries pause when offline |

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      networkMode: 'offlineFirst', // Good for service workers
    },
    mutations: {
      networkMode: 'offlineFirst',
    },
  },
});
```

### Paused State

New `fetchStatus` distinguishes query execution state:

| fetchStatus | Meaning                |
| ----------- | ---------------------- |
| `fetching`  | Request in-flight      |
| `paused`    | Query halted (offline) |
| `idle`      | Not currently running  |

```tsx
const { data, isPaused, fetchStatus } = useQuery({
  queryKey: ['posts'],
  queryFn: fetchPosts,
});

if (isPaused) {
  return <OfflineBanner>Waiting for connection...</OfflineBanner>;
}
```

**Key insight:** `status` describes the **data** state; `fetchStatus` describes the **queryFn** execution state.

## WebSocket Integration

### Pattern 1: Event-Based Invalidation (Recommended)

WebSocket events trigger query invalidation:

```tsx
function useRealtimeSubscription() {
  const queryClient = useQueryClient();

  useEffect(() => {
    const ws = new WebSocket('wss://api.example.com/events');

    ws.onmessage = (event) => {
      const { entity, id } = JSON.parse(event.data);
      // Construct queryKey from event data
      const queryKey = id ? [entity, id] : [entity];
      queryClient.invalidateQueries({ queryKey });
    };

    return () => ws.close();
  }, [queryClient]);
}

// Event format examples:
// { "entity": "posts" } → invalidates all post queries
// { "entity": "posts", "id": "123" } → invalidates specific post
```

**Benefits:**

- Only active queries refetch
- Works with existing query setup
- Minimal code changes

### Pattern 2: Direct Cache Updates

For high-frequency updates, modify cache directly:

```tsx
ws.onmessage = (event) => {
  const { entity, id, payload } = JSON.parse(event.data);

  queryClient.setQueriesData({ queryKey: [entity] }, (old: unknown) => {
    if (Array.isArray(old)) {
      return old.map((item) =>
        item.id === id ? { ...item, ...payload } : item,
      );
    }
    return old;
  });
};
```

**Trade-offs:** More complex, less type-safe, requires compatible data structures.

### Configuration with WebSockets

Set high `staleTime` when WebSockets handle freshness:

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: Infinity, // WebSocket keeps data fresh
      refetchOnWindowFocus: false,
      refetchOnReconnect: false,
    },
  },
});
```

## Architecture Internals

Understanding React Query's structure helps debug issues:

```sh
QueryClient
├── QueryCache (stores Query instances)
│   └── Query (state machine for one queryKey)
│       └── QueryObserver (created by useQuery)
└── MutationCache (stores Mutation instances)
    └── Mutation (state machine for one mutation)
```

### Key Relationships

**QueryClient:** Container for caches + default options. Distributed via Context but doesn't trigger re-renders itself.

**QueryCache:** In-memory storage mapping `queryKeyHash` → `Query`. Data only stored in memory by default.

**Query:** Core logic layer containing state, retry logic, deduplication. Notifies observers of changes.

**QueryObserver:** Bridge between Query and component. Created per `useQuery` call. Tracks which properties the component uses to minimize re-renders.

### Active vs Inactive Queries

- **Active:** Has at least one observer (component using it)
- **Inactive:** No observers, kept in cache for `gcTime`

React Query DevTools shows this distinction visually.

### Framework-Agnostic Core

The heavy lifting happens in `@tanstack/query-core`. Framework adapters (React, Solid, Vue) are ~100 lines each, just connecting observers to the framework's reactive system.

## Mutation Persistence

Persist mutations across page reloads/app restarts:

```tsx
const queryClient = new QueryClient();

// Define mutation with defaults
queryClient.setMutationDefaults(['addTodo'], {
  mutationFn: addTodo,
  onMutate: async (variables, context) => {
    await context.client.cancelQueries({ queryKey: ['todos'] });
    const previous = context.client.getQueryData(['todos']);
    context.client.setQueryData(['todos'], (old) => [...old, variables]);
    return { previous };
  },
  onError: (_error, _variables, result, context) => {
    context.client.setQueryData(['todos'], result?.previous);
  },
  retry: 3,
});

// Dehydrate state (e.g., on app background)
const state = dehydrate(queryClient);
localStorage.setItem('queryState', JSON.stringify(state));

// Hydrate on app start
const savedState = JSON.parse(localStorage.getItem('queryState'));
hydrate(queryClient, savedState);

// Resume paused mutations
queryClient.resumePausedMutations();
```

## When NOT to Use React Query

React Query excels at async/server state but isn't ideal for:

| Scenario                     | Better Alternative       |
| ---------------------------- | ------------------------ |
| Purely synchronous state     | useState, Zustand, Jotai |
| Normalized caching (GraphQL) | Apollo Client, urql      |
| Server Components only       | Native fetch + caching   |
| Simple fetch-and-display     | Server Components        |

React Query shines for:

- Infinite scrolling
- Offline-first apps
- Auto-refetching on focus/reconnect
- Complex cache invalidation
- React Native
- Hybrid server/client apps
