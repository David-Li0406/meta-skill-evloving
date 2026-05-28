# Data Transformations Reference

## Four Approaches to Transform Data

### 1. Backend Transformation (Ideal)

Transform data where it originates. Have your backend return exactly what the frontend needs.

**Pros:** No frontend transformation overhead
**Cons:** May not be feasible with public APIs or shared backends

### 2. In the queryFn

Transform immediately after fetching, before caching:

```tsx
const fetchTodos = async (): Promise<string[]> => {
  const response = await fetch('/api/todos');
  const data = await response.json();
  return data.map((todo: Todo) => todo.name.toUpperCase());
};

useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
});
```

**Pros:** Co-located with fetching logic
**Cons:** Runs on every fetch; transformed structure obscures original data

### 3. In the Render Function (useMemo)

Transform within the component using memoization:

```tsx
function useTodosQuery() {
  const queryInfo = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
  });

  return {
    ...queryInfo,
    data: useMemo(
      () => queryInfo.data?.map((todo) => todo.name.toUpperCase()),
      [queryInfo.data], // Depend on .data specifically, not queryInfo
    ),
  };
}
```

**Pros:** Original data preserved in cache
**Cons:** Transformation runs on component re-renders

### 4. Using select (Recommended)

The most powerful approach with partial subscriptions:

```tsx
useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  select: (data) => data.map((todo) => todo.name.toUpperCase()),
});
```

**Pros:**

- Structural sharing preserves referential identity
- Partial subscriptions: components only re-render when selected data changes
- Original data preserved in cache

**Cons:** Inline functions run every render (requires memoization)

## select Best Practices

### Single Property Selection

```tsx
// Component only re-renders when title changes
const { data: title } = useQuery({
  queryKey: ['post', id],
  queryFn: () => fetchPost(id),
  select: (data) => data.title,
});
```

### Multiple Properties with Structural Sharing

```tsx
// Referential stability maintained via structural sharing
const { data } = useQuery({
  queryKey: ['post', id],
  queryFn: () => fetchPost(id),
  select: (data) => ({
    title: data.title,
    author: data.author,
  }),
});
```

### Memoization for Expensive Transforms

**Option 1: useCallback**

```tsx
const selectUppercaseTodos = useCallback(
  (data: Todo[]) => data.map((todo) => todo.name.toUpperCase()),
  [],
);

useQuery({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  select: selectUppercaseTodos,
});
```

**Option 2: Extract to Stable Function**

```tsx
// Defined outside component - stable reference
const selectUppercaseTodos = (data: Todo[]) =>
  data.map((todo) => todo.name.toUpperCase());

function TodoList() {
  const { data } = useQuery({
    queryKey: ['todos'],
    queryFn: fetchTodos,
    select: selectUppercaseTodos,
  });
}
```

**Option 3: External Memoization (fast-memoize)**

```tsx
import memoize from 'fast-memoize';

const selectUppercaseTodos = memoize((data: Todo[]) =>
  data.map((todo) => todo.name.toUpperCase()),
);
```

## Type-Safe Selector Abstractions

Create reusable query options that accept custom selectors:

```tsx
function postOptions<TData = Post>(id: string, select?: (data: Post) => TData) {
  return queryOptions({
    queryKey: ['posts', id],
    queryFn: () => fetchPost(id),
    select,
  });
}

// Usage with full data
useQuery(postOptions('123'));

// Usage with selector
useQuery(postOptions('123', (data) => data.title));
```

## When to Use Each Approach

| Scenario                              | Recommended Approach        |
| ------------------------------------- | --------------------------- |
| Simple display transformation         | `select` option             |
| Expensive computation                 | `select` with memoization   |
| Need original data elsewhere          | `select` (preserves cache)  |
| Transformation for multiple consumers | `queryFn` transformation    |
| Backend control available             | Backend transformation      |
| Depends on component props            | `select` with `useCallback` |
