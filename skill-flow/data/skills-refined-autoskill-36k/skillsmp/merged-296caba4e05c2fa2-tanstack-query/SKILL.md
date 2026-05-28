---
name: tanstack-query
description: Use this skill for managing server state with TanStack Query v5, covering data fetching, caching, mutations, optimistic updates, authentication, and best practices.
---

# TanStack Query v5 - Complete Guide

**TanStack Query v5** (October 2023) is the async state manager for this project. It requires React 18+, features first-class Suspense support, improved TypeScript inference, and a 20% smaller bundle. This section covers production-ready patterns based on official documentation and community best practices.

## Core Principles

- Use TanStack Query for all server state management and data fetching.
- Minimize the use of `useEffect` and `useState` for server data; favor TanStack Query's built-in state management.
- Implement proper error handling with user-friendly messages.
- Use TypeScript for full type safety with query responses.

## Project Structure

```
src/
  api/
    client.ts             # API client configuration
    endpoints/
      users.ts            # User-related API calls
      posts.ts            # Post-related API calls
  hooks/
    queries/
      useUsers.ts         # User query hooks
      usePosts.ts         # Post query hooks
    mutations/
      useCreateUser.ts    # User mutation hooks
  providers/
    QueryProvider.tsx     # Query client provider setup
  types/
    api.ts                # API response types
```

## Setup and Configuration

### Query Client Configuration

```typescript
// providers/QueryProvider.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      gcTime: 1000 * 60 * 30,   // 30 minutes (formerly cacheTime)
      retry: 3,
      refetchOnWindowFocus: true,
      refetchOnReconnect: true,
    },
    mutations: {
      retry: 1,
    },
  },
});

export function QueryProvider({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

## Queries

### Basic Query

Fetch data with automatic caching:

```typescript
// hooks/queries/useUser.ts
import { useQuery } from '@tanstack/react-query';
import { fetchUser, User } from '@/api/endpoints/users';

export function useUser(userId: string) {
  return useQuery<User, Error>({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    enabled: !!userId, // Only run if userId exists
    staleTime: 1000 * 60 * 10, // Data fresh for 10 minutes
  });
}
```

### Query with Error Handling

```typescript
// services/api/users.ts
export async function fetchUser(userId: string): Promise<User> {
  const response = await fetch(`/api/users/${userId}`);

  if (!response.ok) {
    throw new Error('Unable to load user profile. Please try again.');
  }

  return response.json();
}

// Component usage
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useUser(userId);

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error.message} />;

  return <ProfileCard user={user} />;
}
```

### Dependent Queries

```typescript
function useUserWithPosts(userId: string) {
  const { data: user } = useUser(userId);

  return useQuery({
    queryKey: ['posts', user?.id],
    queryFn: () => fetchUserPosts(user.id),
    enabled: !!user, // Only run when user data is available
  });
}
```

### Parallel Queries

```typescript
export function Dashboard() {
  const users = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  });

  const posts = useQuery({
    queryKey: ['posts'],
    queryFn: fetchPosts,
  });

  const stats = useQuery({
    queryKey: ['stats'],
    queryFn: fetchStats,
  });

  if (users.isLoading || posts.isLoading || stats.isLoading) {
    return <LoadingSkeleton />;
  }

  return (
    <div>
      <UserList users={users.data} />
      <PostList posts={posts.data} />
      <Stats data={stats.data} />
    </div>
  );
}
```

## Mutations

### Basic Mutation

Modify server data:

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

export function CreatePostForm() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async (newPost: NewPost) => {
      const response = await fetch('/api/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPost),
      });
      if (!response.ok) throw new Error('Failed to create post');
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    },
  });

  const handleSubmit = (data: NewPost) => {
    mutation.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* form fields */}
      {mutation.isPending && <p>Creating post...</p>}
      {mutation.isError && <p>Error: {mutation.error.message}</p>}
      {mutation.isSuccess && <p>Post created!</p>}
    </form>
  );
}
```

### Optimistic Updates

```typescript
const mutation = useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] });

    const previousTodos = queryClient.getQueryData(['todos']);

    queryClient.setQueryData(['todos'], (old: Todo[]) => {
      return old.map((todo) =>
        todo.id === newTodo.id ? newTodo : todo
      );
    });

    return { previousTodos };
  },
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(['todos'], context.previousTodos);
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

## Error Handling

### Global Error Handler

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      onError: (error: Error) => {
        console.error('Query error:', error);
      },
    },
    mutations: {
      onError: (error: Error) => {
        toast.error(error.message);
      },
    },
  },
});
```

### Error Boundaries

```typescript
import { useQuery } from '@tanstack/react-query';
import { useErrorBoundary } from 'react-error-boundary';

export function CriticalData() {
  const { showBoundary } = useErrorBoundary();

  const { data } = useQuery({
    queryKey: ['critical'],
    queryFn: fetchCriticalData,
    throwOnError: true,
  });

  return <div>{/* render data */}</div>;
}
```

## Performance Optimization

### Query Key Best Practices

- Use arrays for all query keys.
- Order from general to specific.
- Include all variables that affect the query.
- Use objects for multiple parameters.
- Keep keys consistent across the app.

### Selective Subscriptions

```typescript
function useUserName(userId: string) {
  return useUser(userId, {
    select: (user) => user.name,
  });
}
```

### Prefetching

```typescript
function UserListItem({ userId }: { userId: string }) {
  const queryClient = useQueryClient();

  const handleMouseEnter = () => {
    queryClient.prefetchQuery({
      queryKey: ['user', userId],
      queryFn: () => fetchUser(userId),
      staleTime: 60000,
    });
  };

  return (
    <Link
      href={`/users/${userId}`}
      onMouseEnter={handleMouseEnter}
      onTouchStart={handleMouseEnter}
    >
      View User
    </Link>
  );
}
```

## Key Conventions

1. Use query keys as array of dependencies.
2. Invalidate queries after mutations.
3. Prefetch on hover for better UX.
4. Use staleTime to reduce unnecessary refetches.
5. Implement optimistic updates for instant feedback.
6. Use enabled option for dependent queries.
7. Keep query functions pure and reusable.

## Anti-Patterns to Avoid

- Do not use `useEffect` for data fetching.
- Do not store server data in `useState`.
- Do not forget loading and error state handling.
- Do not create queries without proper cache invalidation strategies.
- Do not skip the `enabled` option for conditional queries.
- Do not ignore TypeScript types for query responses.