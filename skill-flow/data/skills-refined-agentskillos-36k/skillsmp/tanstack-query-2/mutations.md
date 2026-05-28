# Mutations Reference

## mutate vs mutateAsync

| Method          | Error Handling      | Return Value     | Use Case                  |
| --------------- | ------------------- | ---------------- | ------------------------- |
| `mutate()`      | Handles internally  | `void`           | Most cases, use callbacks |
| `mutateAsync()` | Must catch manually | `Promise<TData>` | Need to await result      |

```tsx
const mutation = useMutation({ mutationFn: createPost });

// mutate - errors handled internally, use callbacks
mutation.mutate(data, {
  onSuccess: (result) => {
    navigate(`/posts/${result.id}`);
  },
});

// mutateAsync - must handle errors yourself
try {
  const result = await mutation.mutateAsync(data);
  navigate(`/posts/${result.id}`);
} catch (error) {
  // Must catch or error propagates!
  toast.error(error.message);
}
```

**Recommendation:** Prefer `mutate()` with callbacks for cleaner code.

## Single Argument Limitation

Mutations accept only ONE variable argument. Use objects for multiple values:

```tsx
// BAD: Multiple arguments (won't work)
mutation.mutate(id, title, body);

// GOOD: Single object argument
mutation.mutate({ id, title, body });
```

## Callback Execution Order

Callbacks fire in this order:

1. `useMutation.onMutate`
2. `useMutation.onSuccess/onError`
3. `useMutation.onSettled`
4. `mutate.onSuccess/onError`
5. `mutate.onSettled`

**Important:** If component unmounts, `mutate()` callbacks may not fire. Place critical logic in `useMutation()` callbacks.

```tsx
// Separation of concerns
const updatePost = useMutation({
  mutationFn: updatePostFn,
  // Query-related logic here (always runs)
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['posts'] });
  },
});

// UI-specific logic in mutate() (may not run if unmounted)
updatePost.mutate(data, {
  onSuccess: () => {
    toast.success('Post updated!');
    navigate('/posts');
  },
});
```

## Returning Promises from Callbacks

Return `invalidateQueries` to maintain loading state during refetch:

```tsx
const mutation = useMutation({
  mutationFn: createPost,
  onSuccess: () => {
    // Without return: mutation.isPending becomes false immediately
    // With return: mutation.isPending stays true until refetch completes
    return queryClient.invalidateQueries({ queryKey: ['posts'] });
  },
});
```

## Optimistic Updates with Rollback

```tsx
const queryClient = useQueryClient();

const updatePost = useMutation({
  mutationFn: (data: { id: string; title: string }) => updatePostFn({ data }),
  onMutate: async (newData) => {
    // Cancel in-flight queries
    await queryClient.cancelQueries({ queryKey: ['posts', newData.id] });

    // Snapshot for rollback
    const previousPost = queryClient.getQueryData(['posts', newData.id]);

    // Optimistic update
    queryClient.setQueryData(['posts', newData.id], (old) => ({
      ...old,
      ...newData,
    }));

    return { previousPost };
  },
  onError: (error, variables, context) => {
    // Rollback on error
    if (context?.previousPost) {
      queryClient.setQueryData(['posts', variables.id], context.previousPost);
    }
    toast.error('Failed to update post');
  },
  onSettled: (data, error, variables) => {
    // Always refetch to ensure consistency
    queryClient.invalidateQueries({ queryKey: ['posts', variables.id] });
  },
});
```

## Optimistic Add to List

```tsx
const addPost = useMutation({
  mutationFn: createPostFn,
  onMutate: async (newPost) => {
    await queryClient.cancelQueries({ queryKey: ['posts'] });
    const previousPosts = queryClient.getQueryData(['posts']);

    // Optimistically add with temp ID
    const optimisticPost = {
      ...newPost,
      id: `temp-${Date.now()}`,
      createdAt: new Date(),
    };
    queryClient.setQueryData(['posts'], (old: Post[]) => [
      optimisticPost,
      ...old,
    ]);

    return { previousPosts };
  },
  onError: (error, variables, context) => {
    queryClient.setQueryData(['posts'], context?.previousPosts);
  },
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['posts'] });
  },
});
```

## Automatic Invalidation via MutationCache

Global mutation error/success handling:

```tsx
const queryClient = new QueryClient({
  mutationCache: new MutationCache({
    onSuccess: () => {
      // Invalidate everything after any successful mutation
      // Only active queries refetch; others become stale
      queryClient.invalidateQueries();
    },
    onError: (error, variables, context, mutation) => {
      // Global error handling
      if (!mutation.options.onError) {
        toast.error(`Operation failed: ${error.message}`);
      }
    },
  }),
});
```

### Meta-Based Invalidation Tagging

Specify which queries to invalidate per mutation:

```tsx
const updateLabel = useMutation({
  mutationFn: updateLabelFn,
  meta: {
    invalidates: [['issues'], ['labels']],
  },
});

// In MutationCache
const queryClient = new QueryClient({
  mutationCache: new MutationCache({
    onSuccess: async (_data, _variables, _context, mutation) => {
      const invalidates = mutation.meta?.invalidates as string[][] | undefined;

      if (invalidates) {
        for (const queryKey of invalidates) {
          await queryClient.invalidateQueries({ queryKey });
        }
      }
    },
  }),
});
```

## Concurrent Optimistic Updates

Handle rapid mutations with `isMutating()`:

```tsx
const queryClient = useQueryClient();

const updateTodo = useMutation({
  mutationFn: updateTodoFn,
  onMutate: async (newData) => {
    await queryClient.cancelQueries({ queryKey: ['todos', newData.id] });
    const previous = queryClient.getQueryData(['todos', newData.id]);
    queryClient.setQueryData(['todos', newData.id], newData);
    return { previous };
  },
  onError: (_error, variables, context) => {
    queryClient.setQueryData(['todos', variables.id], context?.previous);
  },
  onSettled: (_data, _error, variables) => {
    // Only invalidate when this is the last pending mutation
    // Prevents UI flicker from cascading invalidations
    if (queryClient.isMutating({ mutationKey: ['todos'] }) === 1) {
      queryClient.invalidateQueries({ queryKey: ['todos', variables.id] });
    }
  },
});
```

**Why:** Multiple rapid mutations can cause flickering UI as each invalidation triggers refetch. Using `isMutating()` ensures only the final mutation triggers invalidation.
