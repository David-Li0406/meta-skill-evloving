# Error Handling Reference

## Three Error Handling Strategies

### 1. Direct Error State Checking

Check the `isError` flag returned by `useQuery`:

```tsx
function TodoList() {
  const { data, isError, error } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  });

  if (isError) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <ul>
      {data?.map((todo) => (
        <li key={todo.id}>{todo.name}</li>
      ))}
    </ul>
  );
}
```

**Limitation:** Replaces entire component with error UI, even during background refetch failures when stale data is available.

### 2. Error Boundaries with throwOnError

Enable errors to propagate to React Error Boundaries:

```tsx
// Boolean: throw all errors
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  throwOnError: true,
});

// Function: selective error throwing
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  throwOnError: (error) => error.response?.status >= 500,
});
```

**When to use:** Critical data where the component can't render without it.

### 3. Global QueryCache Callbacks (Recommended)

Handle errors application-wide, especially for background refetches:

```tsx
const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error, query) => {
      // Only show toast for background refetches (when stale data exists)
      if (query.state.data !== undefined) {
        toast.error(`Background update failed: ${error.message}`);
      }
    },
  }),
});
```

**Key benefit:** Triggers once per failed request, not per Observer.

## Background vs Foreground Errors

| Error Type                 | Data Available | Recommended UI                 |
| -------------------------- | -------------- | ------------------------------ |
| Initial load failure       | No             | Error boundary or inline error |
| Background refetch failure | Yes (stale)    | Toast notification             |
| Mutation failure           | Varies         | Toast + rollback if optimistic |

### Data-First Error Pattern

Always check for data before showing error UI:

```tsx
function TodoList() {
  const { data, isError, error, isFetching } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  });

  // Data-first: show stale data even if refetch failed
  if (data) {
    return (
      <>
        <ul>
          {data.map((todo) => (
            <li key={todo.id}>{todo.name}</li>
          ))}
        </ul>
        {isError && <Banner>Update failed - showing cached data</Banner>}
        {isFetching && <Spinner />}
      </>
    );
  }

  // Only show error UI when no data at all
  if (isError) {
    return <div>Error: {error.message}</div>;
  }

  return <Skeleton />;
}
```

## fetch API Error Handling

The native `fetch` API does NOT reject on 4xx/5xx status codes. You must throw manually:

```tsx
const fetchTodos = async (): Promise<Todo[]> => {
  const response = await fetch('/api/todos');

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
};
```

**Common mistake:** Using `catch` without re-throwing returns a successful Promise:

```tsx
// BAD: Error is swallowed, returns undefined as success
const fetchTodos = async () => {
  try {
    const response = await fetch('/api/todos');
    return response.json();
  } catch (error) {
    console.error(error); // Error swallowed!
  }
};

// GOOD: Re-throw to let React Query handle it
const fetchTodos = async () => {
  try {
    const response = await fetch('/api/todos');
    return response.json();
  } catch (error) {
    console.error(error);
    throw error; // Re-throw!
  }
};
```

## Error Type Safety

Handle errors defensively since JavaScript allows throwing any value:

```tsx
if (query.error instanceof Error) {
  return <div>Error: {query.error.message}</div>;
}

// Or with type guard
function isError(error: unknown): error is Error {
  return error instanceof Error;
}
```

## Retry Configuration

React Query retries failed queries 3 times by default with exponential backoff:

```tsx
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  retry: 3, // Default
  retry: false, // Disable retries
  retry: (failureCount, error) => {
    // Custom retry logic
    if (error.response?.status === 404) return false;
    return failureCount < 3;
  },
  retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
});
```

## MutationCache for Mutation Errors

Global error handling for mutations:

```tsx
const queryClient = new QueryClient({
  mutationCache: new MutationCache({
    onError: (error, variables, context, mutation) => {
      // Global mutation error handling
      if (mutation.options.onError) {
        // Let local handler take precedence
        return;
      }
      toast.error(`Operation failed: ${error.message}`);
    },
  }),
});
```
