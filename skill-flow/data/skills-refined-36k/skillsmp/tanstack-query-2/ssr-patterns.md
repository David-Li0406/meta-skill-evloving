# SSR Patterns Reference

## Prefetching in Route Loaders

```tsx
// Route with SSR prefetch
export const Route = createFileRoute('/posts')({
  loader: async ({ context }) => {
    // Prefetch ensures data is ready before render
    await context.queryClient.ensureQueryData(postsOptions());
  },
  component: PostsPage,
});

function PostsPage() {
  // Data is already in cache from loader - no loading state needed
  const { data } = useSuspenseQuery(postsOptions());
  return <PostList posts={data} />;
}
```

## Prefetching with Search Params

```tsx
const searchSchema = z.object({
  page: z.number().default(1),
  sort: z.enum(['newest', 'oldest']).default('newest'),
});

export const Route = createFileRoute('/posts')({
  validateSearch: searchSchema,
  loaderDeps: ({ search }) => ({ page: search.page, sort: search.sort }),
  loader: async ({ context, deps }) => {
    await context.queryClient.ensureQueryData(
      postsOptions({ page: deps.page, sort: deps.sort }),
    );
  },
});
```

## Hydration Pattern

```tsx
// Server: Prefetch data
export const Route = createFileRoute('/posts/$id')({
  loader: async ({ context, params }) => {
    await context.queryClient.ensureQueryData(postOptions(params.id));
  },
});

// Client: Use prefetched data (no flash of loading)
function PostPage() {
  const { id } = Route.useParams();
  const { data } = useSuspenseQuery(postOptions(id));
  // Data is immediately available from SSR
  return <PostDetail post={data} />;
}
```

## Router Integration: Cache-First Resolution

Return cached data immediately, only fetch if cache is empty:

```tsx
export const Route = createFileRoute('/posts/$id')({
  loader: async ({ context, params }) => {
    const { queryClient } = context;
    const options = postOptions(params.id);

    // Return cached data OR fetch if not available
    return (
      queryClient.getQueryData(options.queryKey) ??
      (await queryClient.fetchQuery(options))
    );
  },
});
```

## Await as a Control Lever

Control navigation behavior by awaiting or not:

```tsx
export const Route = createFileRoute('/posts')({
  loader: async ({ context }) => {
    // WITH await: Block navigation until data loads
    // User sees previous page until new data is ready
    await context.queryClient.ensureQueryData(postsOptions());

    // WITHOUT await: Navigate immediately, show loading state
    // Useful for non-critical data
    context.queryClient.prefetchQuery(recommendationsOptions());
  },
});
```

## Action-Based Invalidation

Invalidate queries in route actions (mutations):

```tsx
export const Route = createFileRoute('/posts/$id/edit')({
  // Action handles form submission
  action: async ({ context, params, request }) => {
    const formData = await request.formData();
    const updates = Object.fromEntries(formData);

    // Perform mutation
    await updatePost(params.id, updates);

    // Invalidate related queries
    await context.queryClient.invalidateQueries({ queryKey: ['posts'] });

    // Redirect after successful mutation
    throw redirect({ to: `/posts/${params.id}` });
  },
});
```

## React 19 Suspense Considerations

React 19 changed how Suspense works with sibling components:

### The Problem: Sequential Waterfalls

React 19 no longer pre-renders siblings when one component suspends:

```tsx
// These fetch sequentially in React 19 (waterfall)
function Dashboard() {
  return (
    <Suspense fallback={<Loading />}>
      <Posts /> {/* Suspends first */}
      <Comments /> {/* Waits for Posts to complete */}
    </Suspense>
  );
}
```

### The Solution: Prefetch in Loaders

Start fetches before render to avoid waterfalls:

```tsx
export const Route = createFileRoute('/dashboard')({
  loader: async ({ context: { queryClient } }) => {
    // Start both fetches in parallel
    await Promise.all([
      queryClient.prefetchQuery(postsOptions()),
      queryClient.prefetchQuery(commentsOptions()),
    ]);
  },
  component: Dashboard,
});

function Dashboard() {
  // Both queries resolve together
  const posts = useSuspenseQuery(postsOptions());
  const comments = useSuspenseQuery(commentsOptions());
  // ...
}
```

### Alternative: Fire-and-Forget Prefetch

Don't await if you want immediate navigation:

```tsx
loader: ({ context: { queryClient } }) => {
  // Fire both prefetches, don't await
  queryClient.prefetchQuery(postsOptions());
  queryClient.prefetchQuery(commentsOptions());
};
```

### Key Principle

**Decouple data fetching from rendering.** Initiate fetches in loaders, not components. Components should be pure consumers of already-started promises.
