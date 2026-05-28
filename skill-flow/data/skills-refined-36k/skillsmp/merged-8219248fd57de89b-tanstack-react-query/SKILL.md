---
name: tanstack-react-query
description: Use this skill for effective server state management, data fetching, caching, and synchronization in React applications using TanStack Query (formerly React Query).
---

# TanStack Query Best Practices

You are an expert in TanStack Query, TypeScript, and React development. TanStack Query simplifies data fetching logic with built-in caching, background updates, and stale data management.

## Core Principles

- Use TanStack Query for all server state management and data fetching.
- Minimize the use of `useEffect` and `useState` for server data; favor TanStack Query's built-in state management.
- Implement proper error handling with user-friendly messages.
- Use TypeScript for full type safety with query responses.
- Avoid excessive API calls through proper caching strategies.

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

## Query Patterns

### Basic Query Hook

```typescript
import { useQuery } from '@tanstack/react-query';
import { fetchUser, User } from '@/api/endpoints/users';

export function useUser(userId: string) {
  return useQuery<User, Error>(
    ['user', userId],
    () => fetchUser(userId),
    {
      enabled: !!userId,
      staleTime: 1000 * 60 * 10, // 10 minutes
    }
  );
}
```

### Dependent Queries

Handle queries that depend on other data:

```typescript
function useUserWithPosts(userId: string) {
  const userQuery = useUser(userId);

  const postsQuery = useQuery(
    ['posts', userId],
    () => fetchUserPosts(userId),
    {
      enabled: !!userQuery.data,
    }
  );

  return { userQuery, postsQuery };
}
```

### Paginated Queries

```typescript
function usePaginatedUsers(page: number, limit: number = 10) {
  return useQuery(
    ['users', 'list', { page, limit }],
    () => fetchUsers({ page, limit }),
    {
      keepPreviousData: true,
    }
  );
}
```

### Infinite Queries

Load more data as user scrolls:

```typescript
import { useInfiniteQuery } from '@tanstack/react-query';

export function useInfinitePosts() {
  return useInfiniteQuery({
    queryKey: ['posts', 'infinite'],
    queryFn: async ({ pageParam }) => {
      const response = await fetch(`/api/posts?page=${pageParam}`);
      return response.json();
    },
    initialPageParam: 1,
    getNextPageParam: (lastPage, allPages) => {
      return lastPage.hasMore ? allPages.length + 1 : undefined;
    },
  });
}
```

## Mutation Patterns

### Basic Mutation

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';

function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation(createUser, {
    onSuccess: () => {
      queryClient.invalidateQueries(['users']);
    },
    onError: (error: Error) => {
      toast.error(error.message);
    },
  });
}
```

### Optimistic Updates

Provide instant feedback while mutations are in flight:

```typescript
function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateUser,
    onMutate: async (newUser) => {
      await queryClient.cancelQueries(['user', newUser.id]);

      const previousUser = queryClient.getQueryData(['user', newUser.id]);

      queryClient.setQueryData(['user', newUser.id], newUser);

      return { previousUser };
    },
    onError: (err, newUser, context) => {
      queryClient.setQueryData(['user', newUser.id], context?.previousUser);
    },
    onSettled: (data, error, variables) => {
      queryClient.invalidateQueries(['user', variables.id]);
    },
  });
}
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
import { ErrorBoundary } from 'react-error-boundary';

function App() {
  return (
    <ErrorBoundary fallback={<ErrorFallback />}>
      <UserProfile userId="123" />
    </ErrorBoundary>
  );
}
```

## Key Conventions

1. Use React Query DevTools to inspect cache and track query status.
2. Group query hooks within feature-specific directories.
3. Always handle errors properly with user-friendly messages and retry options.
4. Fetch only required data - use API parameters to reduce data transfer.
5. Avoid deeply nesting queries - flatten when possible for better performance.
6. Use local state for component-specific data, global state for shared data.
7. Leverage TanStack Query's built-in caching and state management capabilities.

## Anti-Patterns to Avoid

- Do not use `useEffect` for data fetching.
- Do not store server data in `useState`.
- Do not forget loading and error state handling.
- Do not create queries without proper cache invalidation strategies.
- Do not skip the `enabled` option for conditional queries.
- Do not ignore TypeScript types for query responses.