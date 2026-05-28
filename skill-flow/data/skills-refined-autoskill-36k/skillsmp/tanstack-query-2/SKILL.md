---
name: tanstack-query
description: Use TanStack Query for data fetching and caching. Use when implementing queries, mutations, infinite queries, or cache invalidation.
---

# TanStack Query

## Mental Model

TanStack Query is an **async state manager**, NOT a data fetching library. It doesn't fetch data - you provide a `queryFn` that returns a Promise. React Query handles caching, deduplication, background updates, and stale data management.

**Key distinctions:**

| Concept      | Client State           | Server State (React Query) |
| ------------ | ---------------------- | -------------------------- |
| Ownership    | You control completely | Persisted remotely         |
| Availability | Synchronous            | Asynchronous               |
| Updates      | Predictable            | Can become outdated        |
| Management   | useState/Zustand       | TanStack Query             |

**Query keys = dependency array:** Parameters used in your `queryFn` must appear in the `queryKey`. This ensures automatic refetches when dependencies change and prevents stale closure bugs.

## Basic Query

```tsx
import { useQuery } from '@tanstack/react-query';

const { data, error, isPending, isFetching } = useQuery({
  queryKey: ['posts'],
  queryFn: async () => {
    const res = await fetch('/api/posts');
    if (!res.ok) throw new Error('Failed to fetch');
    return res.json();
  },
  staleTime: 1000 * 60, // Fresh for 1 minute
  gcTime: 1000 * 60 * 5, // Cache for 5 minutes
  select: (data) => data.slice(0, 10), // Transform data (optional)
});

// Data-first rendering pattern
if (data) return <PostList posts={data} />;
if (error) return <Error message={error.message} />;
return <Skeleton />;
```

## Query Options Helper

```tsx
import { queryOptions, useQuery, useQueryClient } from '@tanstack/react-query';

function postOptions(id: string) {
  return queryOptions({
    queryKey: ['posts', id],
    queryFn: () => fetchPost(id),
    staleTime: 1000 * 60,
  });
}

// Usage - same options everywhere
useQuery(postOptions('123'));
useSuspenseQuery(postOptions('456'));
queryClient.prefetchQuery(postOptions('789'));
queryClient.invalidateQueries({ queryKey: postOptions('123').queryKey });
```

## Query Key Factory (TkDodo Pattern)

For granular cache invalidation, separate keys from options:

```tsx
// apps/web/src/modules/posts/hooks/post-queries.ts
export const postKeys = {
  all: ['posts'] as const,
  lists: () => [...postKeys.all, 'list'] as const,
  list: (filters: PostFilters) => [...postKeys.lists(), filters] as const,
  details: () => [...postKeys.all, 'detail'] as const,
  detail: (id: string) => [...postKeys.details(), id] as const,
};

export const postQueries = {
  list: (filters: PostFilters) =>
    queryOptions({
      queryKey: postKeys.list(filters),
      queryFn: () => getPosts({ data: filters }),
    }),
  detail: (id: string) =>
    queryOptions({
      queryKey: postKeys.detail(id),
      queryFn: () => getPost({ data: { id } }),
    }),
};

// Granular invalidation
queryClient.invalidateQueries({ queryKey: postKeys.all }); // All posts
queryClient.invalidateQueries({ queryKey: postKeys.lists() }); // All lists
queryClient.invalidateQueries({ queryKey: postKeys.detail('123') }); // One post
```

See [Query Patterns](query-patterns.md) for more key factory patterns.

## Mutations

```tsx
const queryClient = useQueryClient();

const mutation = useMutation({
  mutationFn: async (newPost: { title: string; body: string }) => {
    const res = await fetch('/api/posts', {
      method: 'POST',
      body: JSON.stringify(newPost),
    });
    return res.json();
  },
  onSuccess: async () => {
    await queryClient.invalidateQueries({ queryKey: ['posts'] });
  },
});

mutation.mutate(data);
// Or: await mutation.mutateAsync(data);
```

## Query with Server Functions

```tsx
import { createServerFn } from '@tanstack/react-start';

const getPosts = createServerFn({ method: 'GET' }).handler(async () => {
  return await db.query.posts.findMany();
});

function postsOptions() {
  return queryOptions({
    queryKey: ['posts'],
    queryFn: () => getPosts(),
  });
}

// Prefetch in loader
export const Route = createFileRoute('/posts')({
  loader: async ({ context }) => {
    await context.queryClient.ensureQueryData(postsOptions());
  },
});
```

## Cache Operations

```tsx
const queryClient = useQueryClient();

// Invalidate
queryClient.invalidateQueries({ queryKey: ['posts'] });
queryClient.invalidateQueries({ queryKey: ['posts', '123'] });

// Set data directly
queryClient.setQueryData(['posts', '123'], newPost);

// Prefetch
await queryClient.prefetchQuery(postOptions('456'));
```

## State Comparison

| State        | Meaning                                  |
| ------------ | ---------------------------------------- |
| `isPending`  | No data yet (first load or disabled)     |
| `isLoading`  | First load, fetching, no cached data     |
| `isFetching` | Any fetch (including background refetch) |
| `isSuccess`  | Query succeeded, data available          |
| `isError`    | Query failed                             |

## Common Options

| Option                 | Default | Description                         |
| ---------------------- | ------- | ----------------------------------- |
| `staleTime`            | `0`     | Time until data is considered stale |
| `gcTime`               | 5 min   | Time to keep unused data in cache   |
| `retry`                | `3`     | Number of retry attempts            |
| `refetchOnWindowFocus` | `true`  | Refetch when window regains focus   |
| `enabled`              | `true`  | Whether query should execute        |

## Forms Integration (Brief)

Two approaches to combine forms with server state:

**Copy to Form State (Simple):**

```tsx
const { data } = useQuery(userOptions(id));
const [name, setName] = useState(data?.name ?? '');
// Form now independent of server state - loses background updates
```

**Derived State (Advanced):**

```tsx
const { data } = useQuery(userOptions(id));
const [nameOverride, setNameOverride] = useState<string>();
// Show user's input if changed, otherwise server value
<input
  value={nameOverride ?? data?.name}
  onChange={(e) => setNameOverride(e.target.value)}
/>;
```

See [tanstack-form skill](../tanstack-form/SKILL.md) for full form patterns.

## Common Mistakes

| Mistake                                        | Correct Pattern                                           |
| ---------------------------------------------- | --------------------------------------------------------- |
| Checking `isPending` before `data`             | Data-first: check `data` → `error` → `isPending`          |
| Copying server state to local useState         | Use data directly or derived state pattern                |
| Creating QueryClient in component              | Create once outside component or in useState              |
| Using `refetch()` for parameter changes        | Include params in queryKey, let it refetch automatically  |
| Same key for useQuery and useInfiniteQuery     | Use distinct key segments (different cache structures)    |
| Inline select without memoization              | Extract to stable function or useCallback                 |
| Using `catch` without re-throwing              | Throw errors in queryFn (fetch doesn't reject on 4xx/5xx) |
| Manual generics on useQuery                    | Type the queryFn return, let inference work               |
| Destructuring query for type narrowing         | Keep query object intact for proper narrowing             |
| Relying on deprecated onSuccess for state sync | Use the data directly from useQuery                       |
| Premature render optimization                  | Focus on correctness first, optimize later                |

## Delegation

- **Query pattern discovery**: For finding existing query implementations, use `Explore` agent
- **Cache strategy review**: For comprehensive cache analysis, use `Task` agent
- **Code review**: After implementing queries, delegate to `code-reviewer` agent

## Topic References

### Core Patterns

- [Query Patterns](query-patterns.md) - Key factories, dependent/parallel queries, context
- [Mutations](mutations.md) - Optimistic updates, auto-invalidation, callbacks
- [Caching Patterns](caching-patterns.md) - staleTime, gcTime, cache seeding, placeholderData
- [Infinite Queries](infinite-queries.md) - Cursor, offset, intersection observer

### Advanced Topics

- [Data Transformations](data-transformations.md) - select option, memoization, four approaches
- [Error Handling](error-handling.md) - Error boundaries, global handling, fetch errors
- [TypeScript Patterns](typescript-patterns.md) - Inference, skipToken, Zod validation
- [SSR Patterns](ssr-patterns.md) - Prefetching, hydration, React 19 Suspense
- [Testing Patterns](testing-patterns.md) - Isolation, MSW, async assertions
- [Advanced Patterns](advanced-patterns.md) - Offline, WebSockets, architecture
