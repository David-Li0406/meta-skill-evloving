# v5 Migration & Breaking Changes (TanStack Query 2026)

Migrating to v5 is mandatory for React 19 compatibility. This guide covers the most critical breaking changes and how to resolve them.

## 1. Positional Arguments Removed
In v5, all hooks only accept a single configuration object.

```tsx
// ❌ v4 (Removed)
useQuery(['key'], fetchFn, options);

// ✅ v5 (Correct)
useQuery({ queryKey: ['key'], queryFn: fetchFn, ...options });
```

## 2. Query Callbacks Removed
The `onSuccess`, `onError`, and `onSettled` callbacks were removed from `useQuery`. This change was made to ensure consistency with how state is managed in React 18 and 19.

### Resolution: use useEffect
```tsx
const { data } = useQuery({ queryKey: ['todo'], queryFn: fetchTodo });

useEffect(() => {
  if (data) {
    doSomething(data);
  }
}, [data]);
```

### Resolution: Mutation Callbacks (Still Work!)
Callbacks are still supported in `useMutation` because mutations have a clear start and end lifecycle.

## 3. Renamed Properties
- **cacheTime** → **gcTime**: Better reflects that this time controls Garbage Collection.
- **useErrorBoundary** → **throwOnError**: More descriptive of what the option actually does.

## 4. Status Renaming
- `status: 'loading'` is now `status: 'pending'`.
- `isLoading` property now means `isPending && isFetching`. Use `isPending` for initial loading states.

---
*Updated: January 23, 2026*
