# Query Patterns Reference

## Dependent Queries

```tsx
// Prevent waterfall with parallel where possible
function UserDashboard({ userId }: { userId: string }) {
  // These can run in parallel
  const [user, stats, activity] = useSuspenseQueries({
    queries: [
      userOptions(userId),
      userStatsOptions(userId),
      userActivityOptions(userId),
    ],
  });

  // This depends on user data
  const recommendations = useQuery({
    ...recommendationsOptions(user.data.preferences),
    enabled: !!user.data,
  });
}
```

## Parallel Queries

```tsx
import { useQueries, useSuspenseQueries } from '@tanstack/react-query';

// Dynamic parallel queries
function TeamMembers({ memberIds }: { memberIds: string[] }) {
  const members = useQueries({
    queries: memberIds.map((id) => userOptions(id)),
    combine: (results) => ({
      data: results.map((r) => r.data).filter(Boolean),
      isLoading: results.some((r) => r.isLoading),
      error: results.find((r) => r.error)?.error,
    }),
  });

  if (members.isLoading) return <Spinner />;
  return <MemberList members={members.data} />;
}
```

## Query Factories

### Pattern 1: queryOptions Factory (Simple)

Best for most use cases - co-locates keys with query configuration:

```tsx
// Centralized query definitions
export const queries = {
  posts: {
    all: () =>
      queryOptions({
        queryKey: ['posts'],
        queryFn: getPosts,
      }),
    detail: (id: string) =>
      queryOptions({
        queryKey: ['posts', id],
        queryFn: () => getPost({ data: { id } }),
        staleTime: 1000 * 60 * 5,
      }),
    infinite: (filters?: PostFilters) => ({
      queryKey: ['posts', 'infinite', filters],
      queryFn: ({ pageParam }) =>
        getPostsInfinite({ data: { cursor: pageParam, ...filters } }),
      initialPageParam: undefined as string | undefined,
      getNextPageParam: (lastPage: PostsResponse) => lastPage.nextCursor,
    }),
  },
  users: {
    current: () =>
      queryOptions({
        queryKey: ['user', 'current'],
        queryFn: getCurrentUser,
        staleTime: 1000 * 60 * 10,
      }),
    detail: (id: string) =>
      queryOptions({
        queryKey: ['users', id],
        queryFn: () => getUser({ data: { id } }),
      }),
  },
} as const;

// Usage
useQuery(queries.posts.detail('123'));
useInfiniteQuery(queries.posts.infinite({ status: 'published' }));
queryClient.invalidateQueries({ queryKey: queries.posts.all().queryKey });
```

### Pattern 2: Hierarchical Key Factory (Advanced)

TkDodo's pattern - enables granular invalidation at any level:

```tsx
// Separate keys from query options for maximum flexibility
export const postKeys = {
  all: ['posts'] as const,
  lists: () => [...postKeys.all, 'list'] as const,
  list: (filters: PostFilters) => [...postKeys.lists(), filters] as const,
  details: () => [...postKeys.all, 'detail'] as const,
  detail: (id: string) => [...postKeys.details(), id] as const,
};

// Query options use the key factory
export const postQueries = {
  list: (filters: PostFilters) =>
    queryOptions({
      queryKey: postKeys.list(filters),
      queryFn: () => fetchPosts(filters),
    }),
  detail: (id: string) =>
    queryOptions({
      queryKey: postKeys.detail(id),
      queryFn: () => fetchPost(id),
    }),
};

// Granular invalidation
queryClient.invalidateQueries({ queryKey: postKeys.all }); // All posts
queryClient.invalidateQueries({ queryKey: postKeys.lists() }); // All list queries
queryClient.invalidateQueries({ queryKey: postKeys.detail('123') }); // Single post
```

**When to use each:**

- **Pattern 1:** Most applications, simpler mental model
- **Pattern 2:** Complex invalidation needs, large-scale applications

## Query Function Context

Extract parameters from context instead of closures:

```tsx
import { type QueryFunctionContext } from '@tanstack/react-query';

// Define key factory with types
const todoKeys = {
  list: (filters: { status: string }) => ['todos', 'list', filters] as const,
};

type TodoListKey = ReturnType<typeof todoKeys.list>;

// Use context to access queryKey
async function fetchTodos({
  queryKey,
  signal,
}: QueryFunctionContext<TodoListKey>) {
  const [, , { status }] = queryKey; // Fully typed!
  const response = await fetch(`/api/todos?status=${status}`, { signal });
  return response.json();
}

// Usage
useQuery({
  queryKey: todoKeys.list({ status: 'active' }),
  queryFn: fetchTodos,
});
```

**Benefits:**

- Automatic abort signal handling
- Type-safe parameter extraction
- No closure variables to track

### Object-Based Keys

Use objects for named property access instead of array indices:

```tsx
// Array-based (positional - error prone)
const key = ['todos', 'list', status, sorting] as const;
const [, , statusParam, sortingParam] = key; // Easy to misalign

// Object-based (named - safer)
const key = ['todos', 'list', { status, sorting }] as const;
const [, , { status, sorting }] = key; // Self-documenting

// Full example
function todoListOptions(filters: { status: string; sorting: string }) {
  return queryOptions({
    queryKey: ['todos', 'list', filters] as const,
    queryFn: ({ queryKey }) => {
      const [, , { status, sorting }] = queryKey;
      return fetchTodos({ status, sorting });
    },
  });
}
```

## setQueryDefaults

Configure defaults for query key hierarchies:

```tsx
const queryClient = new QueryClient();

// Set defaults for all 'posts' queries
queryClient.setQueryDefaults(['posts'], {
  staleTime: 1000 * 60 * 5, // 5 minutes
  gcTime: 1000 * 60 * 30, // 30 minutes
});

// Set defaults for specific subset
queryClient.setQueryDefaults(['posts', 'detail'], {
  staleTime: 1000 * 60 * 10, // 10 minutes for details
});

// Individual queries inherit these defaults
useQuery({
  queryKey: ['posts', 'list'],
  queryFn: fetchPosts,
  // Inherits staleTime: 5 min from ['posts'] defaults
});
```

## Key Colocation Principle

Keep query keys alongside their queries, not in a central file:

```sh
src/
├── features/
│   ├── posts/
│   │   ├── queries.ts      # postKeys + postQueries
│   │   └── components/
│   └── users/
│       ├── queries.ts      # userKeys + userQueries
│       └── components/
```

**Why:** Modifying a query and its key happens together. Co-location reduces cognitive overhead.

## ESLint Rules (`@tanstack/eslint-plugin-query`)

- **exhaustive-deps** - Ensures query dependencies are properly included
- **stable-query-client** - QueryClient must remain stable across renders
- **no-rest-destructuring** - Prevents problematic rest destructuring
- **no-unstable-deps** - Flags unstable dependencies causing re-renders
- **infinite-query-property-order** - Validates property ordering
