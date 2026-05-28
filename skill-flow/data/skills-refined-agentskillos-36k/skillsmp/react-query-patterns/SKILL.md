---
name: react-query-patterns
description: TanStack React Query v5 patterns for server state management
---

# TanStack React Query Patterns

## Setup

### Query Client

```tsx
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1 minute
            gcTime: 5 * 60 * 1000, // 5 minutes (formerly cacheTime)
            retry: 1,
            refetchOnWindowFocus: false,
          },
        },
      })
  );

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

```tsx
'use client';

import { useQuery } from '@tanstack/react-query';

interface User {
  id: string;
  name: string;
  email: string;
}

export function UserProfile({ userId }: { userId: string }) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: async () => {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) throw new Error('Failed to fetch user');
      return response.json() as Promise<User>;
    },
  });

  if (isLoading) return <LoadingSkeleton />;
  if (error) return <ErrorMessage error={error} />;

  return <div>{data.name}</div>;
}
```

### Query with Options

```tsx
const { data, isLoading, error, refetch } = useQuery({
  queryKey: ['posts', { page, filter }],
  queryFn: () => fetchPosts(page, filter),
  enabled: !!userId, // Only run if userId exists
  staleTime: 5 * 60 * 1000, // Data fresh for 5 minutes
  gcTime: 10 * 60 * 1000, // Keep in cache for 10 minutes
  retry: 3, // Retry failed requests 3 times
  refetchInterval: 30 * 1000, // Refetch every 30 seconds
  refetchOnWindowFocus: true, // Refetch when window regains focus
});
```

## Query Keys

### Structure

Hierarchical query key organization:

| Pattern | Example |
|---------|---------|
| Simple | `['users']` |
| With ID | `['users', userId]` |
| With params | `['posts', { page, filter }]` |
| Nested | `['users', userId, 'posts']` |

### Best Practices

- Use arrays for all query keys
- Order from general to specific
- Include all variables that affect the query
- Use objects for multiple parameters
- Keep keys consistent across the app

### Query Key Factory

```tsx
// Query key organization
const queryKeys = {
  users: ['users'] as const,
  user: (id: string) => ['users', id] as const,
  userPosts: (id: string) => ['users', id, 'posts'] as const,
  posts: {
    all: ['posts'] as const,
    lists: () => ['posts', 'list'] as const,
    list: (filters: PostFilters) => ['posts', 'list', filters] as const,
    detail: (id: string) => ['posts', id] as const,
  },
};

// Usage
const { data } = useQuery({
  queryKey: queryKeys.user(userId),
  queryFn: () => fetchUser(userId),
});
```

## Mutations

### Basic Mutation

Modify server data:

```tsx
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
      // Invalidate and refetch posts query
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

Update UI immediately before server responds:

```tsx
const mutation = useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['todos'] });

    // Snapshot current value
    const previousTodos = queryClient.getQueryData(['todos']);

    // Optimistically update
    queryClient.setQueryData(['todos'], (old: Todo[]) => {
      return old.map((todo) =>
        todo.id === newTodo.id ? newTodo : todo
      );
    });

    // Return context with snapshot
    return { previousTodos };
  },
  onError: (err, newTodo, context) => {
    // Rollback on error
    queryClient.setQueryData(['todos'], context.previousTodos);
  },
  onSettled: () => {
    // Refetch after error or success
    queryClient.invalidateQueries({ queryKey: ['todos'] });
  },
});
```

### Mutation with Invalidation

```tsx
const mutation = useMutation({
  mutationFn: deletePost,
  onSuccess: (_, deletedPostId) => {
    // Invalidate list query
    queryClient.invalidateQueries({ queryKey: ['posts', 'list'] });

    // Remove deleted post from cache
    queryClient.removeQueries({ queryKey: ['posts', deletedPostId] });

    // Or update cache manually
    queryClient.setQueryData(['posts', 'list'], (old: Post[]) => {
      return old.filter((post) => post.id !== deletedPostId);
    });
  },
});
```

## Infinite Queries

Load more data as user scrolls:

```tsx
import { useInfiniteQuery } from '@tanstack/react-query';

export function InfinitePostList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading,
  } = useInfiniteQuery({
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

  if (isLoading) return <LoadingSkeleton />;

  return (
    <div>
      {data.pages.map((page, i) => (
        <div key={i}>
          {page.posts.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}
        </div>
      ))}
      {hasNextPage && (
        <button onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
          {isFetchingNextPage ? 'Loading...' : 'Load More'}
        </button>
      )}
    </div>
  );
}
```

## Prefetching

### Hover Prefetch

Prefetch data on hover for instant navigation:

```tsx
import { useQueryClient } from '@tanstack/react-query';

export function PostLink({ postId }: { postId: string }) {
  const queryClient = useQueryClient();

  const prefetchPost = () => {
    queryClient.prefetchQuery({
      queryKey: ['posts', postId],
      queryFn: () => fetchPost(postId),
      staleTime: 60 * 1000, // Keep for 1 minute
    });
  };

  return (
    <Link
      href={`/posts/${postId}`}
      onMouseEnter={prefetchPost}
      onTouchStart={prefetchPost}
    >
      View Post
    </Link>
  );
}
```

### Page Prefetch

```tsx
const { data } = useQuery({
  queryKey: ['posts', page],
  queryFn: () => fetchPosts(page),
});

// Prefetch next page
useEffect(() => {
  if (data?.hasMore) {
    queryClient.prefetchQuery({
      queryKey: ['posts', page + 1],
      queryFn: () => fetchPosts(page + 1),
    });
  }
}, [data, page, queryClient]);
```

## Dependent Queries

Query depends on result of previous query:

```tsx
// First query
const { data: user } = useQuery({
  queryKey: ['user', userId],
  queryFn: () => fetchUser(userId),
});

// Second query depends on first
const { data: projects } = useQuery({
  queryKey: ['projects', user?.id],
  queryFn: () => fetchUserProjects(user.id),
  enabled: !!user, // Only run when user exists
});
```

## Parallel Queries

### Multiple Independent Queries

```tsx
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

### useQueries for Dynamic Queries

```tsx
import { useQueries } from '@tanstack/react-query';

export function MultiUserView({ userIds }: { userIds: string[] }) {
  const userQueries = useQueries({
    queries: userIds.map((id) => ({
      queryKey: ['user', id],
      queryFn: () => fetchUser(id),
    })),
  });

  const isLoading = userQueries.some((query) => query.isLoading);
  const users = userQueries.map((query) => query.data);

  if (isLoading) return <LoadingSkeleton />;

  return (
    <div>
      {users.map((user) => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  );
}
```

## Error Handling

### Retry Logic

```tsx
const { data, error } = useQuery({
  queryKey: ['posts'],
  queryFn: fetchPosts,
  retry: (failureCount, error) => {
    // Don't retry on 404
    if (error.status === 404) return false;
    // Retry up to 3 times
    return failureCount < 3;
  },
  retryDelay: (attemptIndex) => {
    // Exponential backoff: 1s, 2s, 4s
    return Math.min(1000 * 2 ** attemptIndex, 30000);
  },
});
```

### Error Boundaries

```tsx
import { useQuery } from '@tanstack/react-query';
import { useErrorBoundary } from 'react-error-boundary';

export function CriticalData() {
  const { showBoundary } = useErrorBoundary();

  const { data } = useQuery({
    queryKey: ['critical'],
    queryFn: fetchCriticalData,
    throwOnError: true, // Throw errors to Error Boundary
  });

  return <div>{/* render data */}</div>;
}
```

## Best Practices

### Do

- Use query keys as array of dependencies
- Invalidate queries after mutations
- Prefetch on hover for better UX
- Use staleTime to reduce unnecessary refetches
- Implement optimistic updates for instant feedback
- Use enabled option for dependent queries
- Keep query functions pure and reusable

### Don't

- Don't use query keys as strings (use arrays)
- Don't mutate query data directly
- Don't forget to handle loading and error states
- Don't set staleTime too low (causes excessive requests)
- Don't invalidate all queries (be specific)
- Don't put business logic in queryFn (use services)

## Performance

### Optimization

- Set appropriate staleTime (avoid unnecessary refetches)
- Use gcTime to control cache memory usage
- Implement pagination or infinite queries for large lists
- Prefetch predictable user navigation
- Use select option to subscribe to only needed data

### Monitoring

- Enable React Query Devtools in development
- Monitor network requests in DevTools
- Check query cache size regularly
- Measure query execution time
