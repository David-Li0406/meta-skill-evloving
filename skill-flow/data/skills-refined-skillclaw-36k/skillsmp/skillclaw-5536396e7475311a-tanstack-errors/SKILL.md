---
name: tanstack-errors
description: Use this skill when you need guidance on error handling strategies and patterns in TanStack Query, including local error states, error boundaries, and global error callbacks.
---

# TanStack Query Error Handling Patterns

This skill provides guidance for error handling in TanStack Query, covering local vs global strategies, Error Boundaries, and best practices based on recommendations.

## Three Approaches to Error Handling

### 1. Local Error State

Check the `error` property directly in components:

```typescript
function TodoList() {
  const { data, error, isError } = useQuery(todoQueries.all());

  if (isError) {
    return <ErrorMessage error={error} />;
  }

  return <ul>{data?.map(todo => <TodoItem key={todo.id} todo={todo} />)}</ul>;
}
```

**Pros:** Simple, explicit, component controls its error UI  
**Cons:** Repetitive across many components

### 2. Error Boundaries

Propagate errors to Error Boundaries using `throwOnError`:

```typescript
// Component throws errors to boundary
function TodoList() {
  const { data } = useQuery({
    ...todoQueries.all(),
    throwOnError: true, // Throws on error
  });

  return <ul>{data.map(todo => <TodoItem key={todo.id} todo={todo} />)}</ul>;
}

// Parent catches with Error Boundary
<ErrorBoundary fallback={<ErrorPage />}>
  <TodoList />
</ErrorBoundary>
```

### 3. Global Error Callbacks

Handle errors at the QueryCache level:

```typescript
const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error, query) => {
      // Global error handling
      if (query.state.data !== undefined) {
        // Only show toast if we already have data (background refetch failed)
        toast.error(`Background update failed: ${error.message}`);
      }
    },
  }),
});
```

## Choosing the Right Approach

| Scenario                    | Recommended Approach          |
| --------------------------- | ----------------------------- |
| Critical page data          | Error Boundary                |
| Background refetch failures | Global callbacks with toast   |
| Form validation errors      | Local error state             |
| 404 errors                  | Local error state or boundary |
| 5xx server errors           | Error Boundary                |
| Network errors              | Global callbacks              |