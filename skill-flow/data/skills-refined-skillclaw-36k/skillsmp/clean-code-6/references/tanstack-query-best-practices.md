# TanStack Query v5 Best Practices

## Data Fetching Principles

- **Use @tanstack/react-query**: For all server state management
- **Handle States**: Always handle loading and error states
- **TypeScript**: Define data shape with TypeScript types
- **Auto Invalidation**: Configure query client to invalidate/refetch after mutations
- **Request Batching**: Batch API requests when possible
- **Optimistic UI**: Use optimistic UI updates for better perceived performance
- **Offline Sync**: Store critical data locally and sync when back online

---

## Setup with Next.js App Router

### Provider Configuration

```typescript
// app/providers.tsx
'use client';

import {
  isServer,
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000, // 1 minute
        retry: 1,
        refetchOnWindowFocus: false,
      },
    },
  });
}

let browserQueryClient: QueryClient | undefined = undefined;

function getQueryClient() {
  if (isServer) {
    return makeQueryClient(); // New client for each request
  } else {
    if (!browserQueryClient) browserQueryClient = makeQueryClient();
    return browserQueryClient; // Reuse in browser
  }
}

export default function Providers({ children }: { children: React.ReactNode }) {
  const queryClient = getQueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

```typescript
// app/layout.tsx
import Providers from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

---

## Migrating from useEffect

### Before (useEffect)

```typescript
// ❌ OLD PATTERN
function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    setIsLoading(true);
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setIsLoading(false));
  }, [userId]);

  if (isLoading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  return <ProfileCard user={user} />;
}
```

### After (TanStack Query)

```typescript
// ✅ NEW PATTERN
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  if (isLoading) return <Spinner />;
  if (error) return <Error message={error.message} />;
  return <ProfileCard user={user} />;
}
```

---

## useSuspenseQuery (v5 Preferred)

Use with Suspense boundaries for cleaner loading states:

```typescript
'use client';

import { useSuspenseQuery } from '@tanstack/react-query';

function UserProfile({ userId }: { userId: string }) {
  // Data is guaranteed to exist - no loading checks needed
  const { data: user } = useSuspenseQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  return <ProfileCard user={user} />;
}

// In parent component
import { Suspense } from 'react';

export default function Page() {
  return (
    <Suspense fallback={<ProfileSkeleton />}>
      <UserProfile userId="123" />
    </Suspense>
  );
}
```

---

## Prefetching Patterns

### Server Component with await

```typescript
// app/posts/page.tsx
import { dehydrate, HydrationBoundary, QueryClient } from '@tanstack/react-query';
import PostList from './post-list';

export default async function PostsPage() {
  const queryClient = new QueryClient();

  await queryClient.prefetchQuery({
    queryKey: ['posts'],
    queryFn: getPosts,
  });

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <PostList />
    </HydrationBoundary>
  );
}
```

### Streaming (Without await)

```typescript
// Allows streaming - doesn't block render
export default function PostsPage() {
  const queryClient = getQueryClient();

  // No await - shows loading on client
  queryClient.prefetchQuery({
    queryKey: ['posts'],
    queryFn: getPosts,
  });

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <PostList />
    </HydrationBoundary>
  );
}
```

---

## Custom Query Hooks

### Create Reusable Hooks

```typescript
// hooks/useUser.ts
export function useUser(userId: string) {
  return useQuery({
    queryKey: ['user', userId],
    queryFn: () => api.getUser(userId),
    enabled: !!userId,
  });
}

// hooks/useUsers.ts
export function useUsers(filters?: UserFilters) {
  return useQuery({
    queryKey: ['users', filters],
    queryFn: () => api.getUsers(filters),
  });
}

// Usage
function UserCard({ userId }: { userId: string }) {
  const { data: user, isLoading } = useUser(userId);
  if (isLoading) return <Skeleton />;
  return <Card user={user} />;
}
```

---

## Query Key Factories

Ensure consistency across your app:

```typescript
// lib/query-keys.ts
export const userKeys = {
  all: ["users"] as const,
  lists: () => [...userKeys.all, "list"] as const,
  list: (filters: string) => [...userKeys.lists(), { filters }] as const,
  details: () => [...userKeys.all, "detail"] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};

export const postKeys = {
  all: ["posts"] as const,
  lists: () => [...postKeys.all, "list"] as const,
  list: (filters?: PostFilters) => [...postKeys.lists(), filters] as const,
  detail: (id: string) => [...postKeys.all, "detail", id] as const,
  byUser: (userId: string) => [...postKeys.all, "user", userId] as const,
};
```

### Usage

```typescript
// In components
useQuery({ queryKey: userKeys.detail(userId), queryFn: () => getUser(userId) });
useQuery({
  queryKey: postKeys.byUser(userId),
  queryFn: () => getUserPosts(userId),
});

// Invalidation
queryClient.invalidateQueries({ queryKey: userKeys.all }); // All users
queryClient.invalidateQueries({ queryKey: userKeys.detail(id) }); // Specific user
queryClient.invalidateQueries({ queryKey: postKeys.byUser(userId) }); // User's posts
```

---

## Mutations

### Basic Mutation

```typescript
const mutation = useMutation({
  mutationFn: (newUser: CreateUser) => api.createUser(newUser),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: userKeys.all });
  },
});

// Usage
<button onClick={() => mutation.mutate({ name: 'John' })}>
  {mutation.isPending ? 'Creating...' : 'Create User'}
</button>
```

### Optimistic Updates

```typescript
const updateUserMutation = useMutation({
  mutationFn: updateUser,

  onMutate: async (newUser) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: userKeys.detail(newUser.id) });

    // Snapshot previous value
    const previousUser = queryClient.getQueryData(userKeys.detail(newUser.id));

    // Optimistically update
    queryClient.setQueryData(userKeys.detail(newUser.id), newUser);

    return { previousUser };
  },

  onError: (err, newUser, context) => {
    // Rollback on error
    queryClient.setQueryData(
      userKeys.detail(newUser.id),
      context?.previousUser,
    );
  },

  onSettled: (data, error, variables) => {
    // Always refetch to ensure consistency
    queryClient.invalidateQueries({ queryKey: userKeys.detail(variables.id) });
  },
});
```

### Form Mutation Hook

```typescript
export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: UpdateUser) => api.updateUser(data),
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: userKeys.detail(variables.id) });
      queryClient.invalidateQueries({ queryKey: userKeys.lists() });
    },
  });
}

// Usage in form
function EditUserForm({ userId }: { userId: string }) {
  const { data: user } = useUser(userId);
  const updateUser = useUpdateUser();

  const handleSubmit = (formData: FormData) => {
    updateUser.mutate({
      id: userId,
      name: formData.get('name') as string,
    });
  };

  return (
    <form action={handleSubmit}>
      <input name="name" defaultValue={user?.name} />
      <button disabled={updateUser.isPending}>
        {updateUser.isPending ? 'Saving...' : 'Save'}
      </button>
    </form>
  );
}
```

---

## Infinite Queries

```typescript
function ProjectList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['projects'],
    queryFn: ({ pageParam }) => fetchProjects(pageParam),
    initialPageParam: 0,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    maxPages: 5, // Limit memory usage
  });

  return (
    <>
      {data?.pages.map((page, i) => (
        <Fragment key={i}>
          {page.data.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </Fragment>
      ))}

      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage
          ? 'Loading...'
          : hasNextPage
            ? 'Load More'
            : 'No more projects'}
      </button>
    </>
  );
}
```

---

## Server Component Integration

### Shared Query Options

```typescript
// queries/posts.ts
export const postsOptions = {
  queryKey: ["posts"] as const,
  queryFn: async () => {
    const response = await fetch("/api/posts");
    return response.json();
  },
  staleTime: 60 * 1000,
};
```

### Server Prefetch

```typescript
// app/posts/page.tsx (Server Component)
import { dehydrate, HydrationBoundary } from '@tanstack/react-query';
import { getQueryClient } from '@/app/get-query-client';
import { postsOptions } from '@/queries/posts';
import PostList from './post-list';

export default async function PostsPage() {
  const queryClient = getQueryClient();
  await queryClient.prefetchQuery(postsOptions);

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <PostList />
    </HydrationBoundary>
  );
}
```

### Client Consumption

```typescript
// app/posts/post-list.tsx (Client Component)
'use client';

import { useQuery } from '@tanstack/react-query';
import { postsOptions } from '@/queries/posts';

export function PostList() {
  const { data: posts } = useQuery(postsOptions);

  return (
    <ul>
      {posts?.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

---

## Query Invalidation Strategies

```typescript
// After mutation - invalidate related queries
const mutation = useMutation({
  mutationFn: createPost,
  onSuccess: () => {
    // Invalidate all posts
    queryClient.invalidateQueries({ queryKey: ["posts"] });

    // Invalidate specific user's posts
    queryClient.invalidateQueries({ queryKey: ["posts", "user", userId] });

    // Invalidate exact match only
    queryClient.invalidateQueries({ queryKey: ["posts"], exact: true });
  },
});

// Refetch vs Invalidate
queryClient.invalidateQueries({ queryKey: ["posts"] }); // Mark stale, fetch on next use
queryClient.refetchQueries({ queryKey: ["posts"] }); // Fetch immediately
```

---

## Configuration Options

| Option                 | Default | Recommended   |
| ---------------------- | ------- | ------------- |
| `staleTime`            | 0       | 60000 (1 min) |
| `gcTime`               | 5 min   | Keep default  |
| `retry`                | 3       | 1             |
| `refetchOnWindowFocus` | true    | false         |
| `refetchOnReconnect`   | true    | true          |

---

## Best Practices Summary

### Do's ✅

- Use `getQueryClient()` pattern for SSR
- Set `staleTime > 0` to prevent immediate refetch
- Use `HydrationBoundary` to bridge server/client
- Implement query key factories
- Use `useSuspenseQuery` with Suspense boundaries
- Cancel queries before optimistic updates
- Always invalidate after mutations
- Use `maxPages` for infinite queries

### Don'ts ❌

- Don't fetch in useEffect
- Don't store query data in useState
- Don't use string-only query keys
- Don't forget to invalidate after mutations
- Don't ignore loading/error states
- Don't skip error boundaries
