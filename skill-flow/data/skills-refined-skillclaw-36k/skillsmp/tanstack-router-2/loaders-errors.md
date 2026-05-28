# Loaders & Error Handling Reference

## Automatic Suspense & Error Boundaries

Every TanStack Router route automatically wraps in `<Suspense>` and `<ErrorBoundary>`. This means:

```tsx
// With Suspense, data is NEVER undefined
function PostPage() {
  const { data } = useSuspenseQuery(postOptions(postId));
  //      ^? Post (guaranteed, never undefined)

  // No defensive checks needed!
  return <h1>{data.title}</h1>;
}

// WITHOUT Suspense (traditional approach) - requires checks
function PostPage() {
  const { data, isLoading } = useQuery(postOptions(postId));

  if (isLoading) return <Skeleton />;
  if (!data) return null; // Defensive check

  return <h1>{data.title}</h1>;
}
```

**Key insight:** Route components can focus on **happy-path rendering**. Suspense handles loading, ErrorBoundary handles errors.

## Loader with Abort Signal

```tsx
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params, abortController }) => {
    const response = await fetch(`/api/posts/${params.postId}`, {
      signal: abortController.signal,
    });

    if (!response.ok) {
      if (response.status === 404) throw notFound();
      throw new Error('Failed to fetch post');
    }

    return response.json();
  },
});
```

## Parallel Data Loading

```tsx
export const Route = createFileRoute('/dashboard')({
  loader: async ({ context }) => {
    const [user, stats, notifications] = await Promise.all([
      context.queryClient.ensureQueryData(userOptions()),
      context.queryClient.ensureQueryData(statsOptions()),
      context.queryClient.ensureQueryData(notificationsOptions()),
    ]);

    return { user, stats, notifications };
  },
});
```

## Deferred Data (Streaming)

```tsx
import { defer } from '@tanstack/react-router';

export const Route = createFileRoute('/dashboard')({
  loader: async () => {
    // Critical data - await immediately
    const user = await fetchUser();

    // Non-critical data - defer loading
    const statsPromise = fetchStats();
    const activityPromise = fetchActivity();

    return {
      user,
      stats: defer(statsPromise),
      activity: defer(activityPromise),
    };
  },
});

function Dashboard() {
  const { user, stats, activity } = Route.useLoaderData();

  return (
    <div>
      <h1>Welcome, {user.name}</h1>

      <Suspense fallback={<StatsSkeletons />}>
        <Await promise={stats}>{(data) => <StatsDisplay data={data} />}</Await>
      </Suspense>

      <Suspense fallback={<ActivitySkeleton />}>
        <Await promise={activity}>
          {(data) => <ActivityFeed data={data} />}
        </Await>
      </Suspense>
    </div>
  );
}
```

## Route-Level Error Boundary

```tsx
export const Route = createFileRoute('/posts/$postId')({
  errorComponent: PostErrorBoundary,
  loader: async ({ params }) => {
    const post = await fetchPost(params.id);
    if (!post) throw notFound();
    return post;
  },
  notFoundComponent: () => (
    <div className="text-center py-10">
      <h2>Post not found</h2>
      <Link to="/posts">Back to posts</Link>
    </div>
  ),
});

function PostErrorBoundary({ error, reset }: ErrorComponentProps) {
  return (
    <div className="p-4 border border-destructive rounded">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <Button onClick={reset}>Try Again</Button>
    </div>
  );
}
```

## Loader Dependencies

```tsx
export const Route = createFileRoute('/posts')({
  validateSearch: z.object({ page: z.number().default(1) }),

  // Declare what search params the loader depends on
  loaderDeps: ({ search }) => ({
    page: search.page,
  }),

  // Loader only re-runs when deps change
  loader: async ({ deps }) => {
    return fetchPosts({ page: deps.page });
  },
});
```
