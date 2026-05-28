---
title: TanStack Query Patterns
impact: HIGH
impactDescription: Proper server state management - ensures cache consistency, prevents redundant fetches, optimizes UX
tags: tanstack-query, react-query, server-state, caching, data-fetching
---

# TanStack Query Patterns (HIGH)

TanStack Query (React Query) patterns for efficient server state management.

## Rule 1: Query Key Factory Pattern

**Always use centralized query key factories:**

```typescript
// ❌ INCORRECT - scattered string keys
const { data } = useQuery({
  queryKey: ['users'],
  queryFn: getUsers,
})

const { data } = useQuery({
  queryKey: ['users', id],
  queryFn: () => getUser(id),
})

// ✅ CORRECT - centralized factory
// src/api/queryKeys.ts
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
}

// Usage
const { data } = useQuery({
  queryKey: userKeys.list({ page: 1 }),
  queryFn: () => getUsers({ page: 1 }),
})
```

## Rule 2: Mutation with Cache Invalidation

**Always invalidate related queries after mutations:**

```typescript
// ❌ INCORRECT - no cache invalidation
const mutation = useMutation({
  mutationFn: createUser,
})

// ✅ CORRECT - invalidate related queries
const mutation = useMutation({
  mutationFn: createUser,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: userKeys.lists() })
  },
})

// ✅ BETTER - parallel invalidation for multiple related queries
const mutation = useMutation({
  mutationFn: updateUser,
  onSuccess: async (_, variables) => {
    await Promise.all([
      queryClient.invalidateQueries({ queryKey: userKeys.detail(variables.id) }),
      queryClient.invalidateQueries({ queryKey: userKeys.lists() }),
    ])
  },
})
```

## Rule 3: Optimistic Updates

**Use optimistic updates for better UX:**

```typescript
// ✅ CORRECT - optimistic update pattern
const mutation = useMutation({
  mutationFn: updateUser,
  onMutate: async (newUser) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: userKeys.detail(newUser.id) })

    // Snapshot previous value
    const previousUser = queryClient.getQueryData(userKeys.detail(newUser.id))

    // Optimistically update
    queryClient.setQueryData(userKeys.detail(newUser.id), newUser)

    return { previousUser }
  },
  onError: (err, newUser, context) => {
    // Rollback on error
    queryClient.setQueryData(
      userKeys.detail(newUser.id),
      context?.previousUser
    )
  },
  onSettled: (_, __, variables) => {
    // Always refetch after error or success
    queryClient.invalidateQueries({ queryKey: userKeys.detail(variables.id) })
  },
})
```

## Rule 4: Proper Loading/Error States

**Always handle all query states:**

```typescript
// ❌ INCORRECT - missing states
function UserList() {
  const { data } = useQuery({...})
  return <List items={data?.users ?? []} />
}

// ✅ CORRECT - handle all states
function UserList() {
  const { data, isLoading, isError, error } = useQuery({...})

  if (isLoading) return <Skeleton />
  if (isError) return <ErrorState message={error.message} />
  if (!data?.users?.length) return <EmptyState />

  return <List items={data.users} />
}
```

## Rule 5: Stale Time Configuration

**Configure staleTime based on data characteristics:**

```typescript
// ❌ INCORRECT - default staleTime (0) causes unnecessary refetches
const { data } = useQuery({
  queryKey: userKeys.detail(id),
  queryFn: () => getUser(id),
})

// ✅ CORRECT - appropriate staleTime
const { data } = useQuery({
  queryKey: userKeys.detail(id),
  queryFn: () => getUser(id),
  staleTime: 1000 * 60, // 1 minute for user data
})

// Static data - longer staleTime
const { data: categories } = useQuery({
  queryKey: ['categories'],
  queryFn: getCategories,
  staleTime: 1000 * 60 * 30, // 30 minutes for static data
})
```

## Rule 6: Enabled Flag for Dependent Queries

**Use enabled to prevent unnecessary fetches:**

```typescript
// ❌ INCORRECT - fetches with undefined id
const { data } = useQuery({
  queryKey: userKeys.detail(userId),
  queryFn: () => getUser(userId),
})

// ✅ CORRECT - only fetch when id exists
const { data } = useQuery({
  queryKey: userKeys.detail(userId),
  queryFn: () => getUser(userId),
  enabled: !!userId,
})

// Dependent queries
const { data: user } = useQuery({
  queryKey: userKeys.detail(userId),
  queryFn: () => getUser(userId),
})

const { data: posts } = useQuery({
  queryKey: postKeys.list({ userId: user?.id }),
  queryFn: () => getPosts(user!.id),
  enabled: !!user?.id, // Only fetch when user is loaded
})
```

## Rule 7: Select for Data Transformation

**Use select to transform/filter data:**

```typescript
// ❌ INCORRECT - transform in component
function ActiveUsers() {
  const { data } = useQuery({
    queryKey: userKeys.list(),
    queryFn: getUsers,
  })
  const activeUsers = data?.filter(u => u.isActive) // Runs every render

  return <List items={activeUsers} />
}

// ✅ CORRECT - transform in select (memoized)
function ActiveUsers() {
  const { data: activeUsers } = useQuery({
    queryKey: userKeys.list(),
    queryFn: getUsers,
    select: (data) => data.filter(u => u.isActive),
  })

  return <List items={activeUsers} />
}
```

## Rule 8: Toast Notifications for Mutations

**Always provide user feedback for mutations:**

```typescript
// ❌ INCORRECT - silent mutation
const mutation = useMutation({
  mutationFn: deleteUser,
})

// ✅ CORRECT - user feedback
const { t } = useTranslation()
const mutation = useMutation({
  mutationFn: deleteUser,
  onSuccess: () => {
    toast.success(t('users.deleteSuccess'))
    queryClient.invalidateQueries({ queryKey: userKeys.lists() })
  },
  onError: (error) => {
    toast.error(t('common.error'))
    console.error('Delete failed:', error)
  },
})
```

## Compliance Checklist

Before submitting code:

- [ ] Query keys use factory pattern
- [ ] Mutations invalidate related queries
- [ ] Loading/error/empty states handled
- [ ] Appropriate staleTime configured
- [ ] Dependent queries use enabled flag
- [ ] Mutations show toast notifications
