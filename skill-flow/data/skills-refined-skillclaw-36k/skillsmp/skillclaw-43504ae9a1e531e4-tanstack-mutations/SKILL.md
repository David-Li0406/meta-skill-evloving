---
name: tanstack-mutations
description: Use this skill when you need guidance on "useMutation", "mutations", "query invalidation", "optimistic updates", "cache updates", and related patterns in TanStack Query.
---

# TanStack Query Mutation Patterns

This skill provides guidance for working with mutations in TanStack Query, covering invalidation strategies, optimistic updates, and cache synchronization based on best practices.

## Understanding Mutations

Mutations are functions with side effects that modify server state. Unlike queries (declarative, automatic), mutations are imperative—invoke them when needed.

### Key Differences from Queries

| Aspect        | useQuery                      | useMutation                  |
| ------------- | ----------------------------- | ---------------------------- |
| Execution     | Automatic, declarative        | Manual, imperative           |
| State Sharing | Cached and shared             | Not shared between instances |
| Lifecycle     | Controlled by component mount | Controlled by mutate() calls |

## Basic Mutation Setup

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query'

function TodoItem({ todo }: { todo: Todo }) {
  const queryClient = useQueryClient()

  const updateMutation = useMutation({
    mutationFn: (updates: Partial<Todo>) =>
      api.patch(`/todos/${todo.id}`, updates),

    onSuccess: () => {
      // Invalidate related queries after successful mutation
      queryClient.invalidateQueries({ queryKey: ['todos'] })
    },
  })

  return (
    <button
      onClick={() => updateMutation.mutate({ completed: true })}
      disabled={updateMutation.isPending}
    >
      Complete
    </button>
  )
}
```

## Cache Synchronization Strategies

### Strategy 1: Query Invalidation

Invalidate queries to trigger refetch. Best for most cases:

```typescript
const deleteMutation = useMutation({
  mutationFn: (id: string) => api.delete(`/todos/${id}`),

  onSuccess: () => {
    // Fuzzy matching - invalidates all queries starting with ['todos']
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

**Key behaviors:**
- Fuzzy matching: `['todos']` invalidates `['todos', 'list']`, `['todos', 'detail', id]`, etc.
- Only active queries refetch immediately.
- Inactive queries marked stale until reused.

### Strategy 2: Direct Cache Updates

Update cache directly when mutation returns complete data:

```typescript
const updateMutation = useMutation({
  mutationFn: (updates: Partial<Todo>) => api.patch(`/todos/${todo.id}`, updates),

  onSuccess: (data) => {
    // Update the cache directly with the new data
    queryClient.setQueryData(['todos', todo.id], data);
  },
});
```