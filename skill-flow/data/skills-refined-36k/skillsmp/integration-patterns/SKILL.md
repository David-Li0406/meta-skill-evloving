---
name: integration-patterns
description: Complete flow examples combining TanStack Form, Query, Router, and Start. Use when implementing end-to-end features that span multiple systems.
---

# Integration Patterns

Quick reference for common full-stack flows. Each flow has a dedicated file with complete copy-paste examples.

## Flow Overview

| Flow                                               | Components                       | Use Case                      |
| -------------------------------------------------- | -------------------------------- | ----------------------------- |
| [Suspense Query + Loader](#suspense-query--loader) | useSuspenseQuery, Router, Loader | SSR-ready data fetching       |
| [Form → Server → Query](#form--server--query)      | Form, Server Function, Query     | Create/update resources       |
| [Infinite List](#infinite-list)                    | Infinite Query, Server Function  | Paginated feeds, timelines    |
| [Paginated Table](#paginated-table)                | Table, Query, Router Search      | Admin dashboards, data grids  |
| [Auth → Protected Route](#auth--protected-route)   | Auth Client, Middleware, Router  | Login, session, guards        |
| [Error Handling](#error-handling)                  | Error Boundaries, Toast          | Error recovery, user feedback |

---

## Hook Placement

Custom hooks should be placed based on their scope:

| Location                        | When to Use                           | Example                      |
| ------------------------------- | ------------------------------------- | ---------------------------- |
| `packages/*/src/hooks/`         | Shared across apps, tied to package   | `@oakoss/auth` session hooks |
| `apps/web/src/modules/*/hooks/` | Module-specific, reused within module | `usePostFilters` in posts    |
| `apps/web/src/hooks/`           | App-wide, used by multiple modules    | `useAppForm`, `useToast`     |

```sh
# Package hooks - exported from package
packages/auth/src/hooks/use-session.ts     # @oakoss/auth/hooks

# Module hooks - domain-specific
apps/web/src/modules/posts/hooks/use-posts-query.ts
apps/web/src/modules/users/hooks/use-user-options.ts

# Global app hooks - app-wide utilities
apps/web/src/hooks/use-app-form.ts
apps/web/src/hooks/form-context.ts
```

**Decision tree:**

1. Is it tied to a package's domain (auth, database)? → `packages/*/src/hooks/`
2. Is it only used within one module? → `apps/web/src/modules/*/hooks/`
3. Is it used across multiple modules? → `apps/web/src/hooks/`

---

## Suspense Query + Loader

The preferred pattern for SSR-ready data fetching: use `useSuspenseQuery` with route loaders to ensure data is ready before render.

**Key pieces:**

```tsx
// 1. Query options hook (apps/web/src/modules/posts/hooks/use-posts-options.ts)
import { queryOptions } from '@tanstack/react-query';
import { getPosts } from '../server/get-posts';

export function postsOptions() {
  return queryOptions({
    queryKey: ['posts'],
    queryFn: () => getPosts(),
    staleTime: 1000 * 60, // 1 minute
  });
}

export function postOptions(id: string) {
  return queryOptions({
    queryKey: ['posts', id],
    queryFn: () => getPost({ data: { id } }),
    staleTime: 1000 * 60,
  });
}

// 2. Route with loader ensures data is cached before render
export const Route = createFileRoute('/_app/posts')({
  loader: async ({ context }) => {
    await context.queryClient.ensureQueryData(postsOptions());
  },
  component: PostsPage,
});

// 3. Component uses useSuspenseQuery - data is guaranteed
import { useSuspenseQuery } from '@tanstack/react-query';

function PostsPage() {
  const { data: posts } = useSuspenseQuery(postsOptions());
  // posts is always defined - no loading state needed here
  return <PostList posts={posts} />;
}
```

**With route params:**

```tsx
// Route with dynamic param
export const Route = createFileRoute('/_app/posts/$id')({
  loader: async ({ context, params }) => {
    await context.queryClient.ensureQueryData(postOptions(params.id));
  },
  component: PostPage,
});

function PostPage() {
  const { id } = Route.useParams();
  const { data: post } = useSuspenseQuery(postOptions(id));
  return <PostDetail post={post} />;
}
```

**With beforeLoad for auth + data:**

```tsx
export const Route = createFileRoute('/_app/dashboard')({
  beforeLoad: async ({ context }) => {
    const session = await auth.api.getSession({
      headers: context.request.headers,
    });
    if (!session) throw redirect({ to: '/login' });
    return { user: session.user };
  },
  loader: async ({ context }) => {
    // User is guaranteed to exist after beforeLoad
    await context.queryClient.ensureQueryData(dashboardOptions());
  },
  component: DashboardPage,
});

function DashboardPage() {
  const { user } = Route.useRouteContext();
  const { data } = useSuspenseQuery(dashboardOptions());
  return <Dashboard user={user} data={data} />;
}
```

**Pattern summary:**

| Step          | Purpose                                  | Location            |
| ------------- | ---------------------------------------- | ------------------- |
| `beforeLoad`  | Auth guards, redirect, inject context    | Route definition    |
| `loader`      | Ensure query data is cached (SSR-ready)  | Route definition    |
| Query options | Define queryKey, queryFn, staleTime      | Module hooks folder |
| Component     | Use `useSuspenseQuery` with same options | Route component     |

---

## Form → Server → Query

Creates a resource with validation, server mutation, and cache invalidation.

**Key pieces:**

```tsx
import { createServerFn } from '@tanstack/react-start';
import { db } from '@oakoss/database';
import { auth } from '@oakoss/auth/server';

// 1. Server function with auth + validation
export const createPost = createServerFn({ method: 'POST' })
  .inputValidator(createPostSchema)
  .handler(async ({ data, request }) => {
    const session = await auth.api.getSession({ headers: request.headers });
    if (!session) return { error: 'Unauthorized', code: 'AUTH_REQUIRED' };
    // ... insert and return
  });

// 2. Form with mutation
const mutation = useMutation({
  mutationFn: (values) => createPost({ data: values }),
  onSuccess: (result) => {
    if (result.success) {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      toast.success('Created!');
    }
  },
});

// 3. Handle server errors in form
if (result.error) {
  form.setErrorMap({ onServer: result.error });
}
```

---

## Infinite List

Cursor-based pagination with intersection observer auto-loading.

**Key pieces:**

```tsx
import { createServerFn } from '@tanstack/react-start';
import { db, lt } from '@oakoss/database';
import { posts } from '@oakoss/database/schema';

// 1. Server function returns { items, nextCursor }
export const getPostsInfinite = createServerFn({ method: 'GET' })
  .inputValidator(
    z.object({ cursor: z.string().optional(), limit: z.number() }),
  )
  .handler(async ({ data }) => {
    const items = await db.query.posts.findMany({
      where: data.cursor
        ? lt(posts.createdAt, new Date(data.cursor))
        : undefined,
      limit: data.limit + 1,
    });
    const hasMore = items.length > data.limit;
    return {
      items: hasMore ? items.slice(0, -1) : items,
      nextCursor: hasMore ? items.at(-1)?.createdAt.toISOString() : undefined,
    };
  });

// 2. Infinite query options
export function postsInfiniteOptions() {
  return {
    queryKey: ['posts', 'infinite'],
    queryFn: ({ pageParam }) =>
      getPostsInfinite({ data: { cursor: pageParam } }),
    initialPageParam: undefined,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
  };
}

// 3. Auto-fetch on scroll
const { ref, inView } = useInView();
useEffect(() => {
  if (inView && hasNextPage) fetchNextPage();
}, [inView, hasNextPage]);
```

---

## Paginated Table

Server-side pagination with URL state synchronization.

**Key pieces:**

```tsx
import { zodValidator } from '@tanstack/zod-adapter';

// 1. Route validates search params
export const Route = createFileRoute('/_app/admin/users')({
  validateSearch: zodValidator(
    z.object({
      page: z.number().default(1),
      size: z.number().default(10),
      sort: z.enum(['name', 'email', 'createdAt']).default('createdAt'),
    }),
  ),
  loaderDeps: ({ search }) => search,
  loader: ({ context, deps }) =>
    context.queryClient.ensureQueryData(usersQueryOptions(deps)),
});

// 2. Update URL on table state change
const handlePaginationChange = (pagination: PaginationState) => {
  navigate({
    search: (prev) => ({
      ...prev,
      page: pagination.pageIndex + 1,
      size: pagination.pageSize,
    }),
  });
};

// 3. Server function returns { items, meta: { total, totalPages } }
```

---

## Auth → Protected Route

Login flow with session and route protection.

**Key pieces:**

```tsx
import { authClient } from '@oakoss/auth/client';
import { auth } from '@oakoss/auth/server';
import { createMiddleware } from '@tanstack/react-start';

// 1. Login with Better Auth client
const result = await authClient.signIn.email({ email, password });
if (result.error) form.setErrorMap({ onServer: result.error.message });

// 2. Auth middleware
export const authMiddleware = createMiddleware().server(
  async ({ request, next }) => {
    const session = await auth.api.getSession({ headers: request.headers });
    if (!session) throw redirect({ to: '/login' });
    return next({ context: { session } });
  },
);

// 3. Protected layout applies middleware
export const Route = createFileRoute('/_app')({
  server: { middleware: [authMiddleware] },
  component: AppLayout,
});

// 4. Access session in components
const { session } = Route.useRouteContext();
```

---

## Error Handling

Structured errors with boundaries and recovery.

**Key pieces:**

```tsx
import { Button } from '@oakoss/ui';

// 1. Return structured errors from server
return { error: 'Not found', code: 'NOT_FOUND' };

// 2. Handle in mutation onSuccess
if ('error' in result) {
  switch (result.code) {
    case 'AUTH_REQUIRED':
      navigate({ to: '/login' });
      break;
    case 'VALIDATION_ERROR':
      form.setFieldMeta(...);
      break;
    default:
      toast.error(result.error);
  }
}

// 3. Route error boundaries
export const Route = createFileRoute('...')({
  errorComponent: ({ error, reset }) => (
    <div>
      <p>{error.message}</p>
      <Button onPress={reset}>Try Again</Button>
    </div>
  ),
  notFoundComponent: () => <NotFoundMessage />,
});
```

---

## Common Mistakes

| Mistake                                              | Correct Pattern                                                   |
| ---------------------------------------------------- | ----------------------------------------------------------------- |
| Using `useQuery` without loader                      | Use `useSuspenseQuery` + `ensureQueryData` in loader for SSR      |
| Checking `isPending` in Suspense components          | `useSuspenseQuery` guarantees data - no pending state             |
| Hooks in wrong location                              | Package hooks → module hooks → global hooks (see placement guide) |
| Duplicating query options                            | Create options hook once, reuse in loader and component           |
| Not invalidating cache after mutation                | Use `queryClient.invalidateQueries({ queryKey })` in onSuccess    |
| Missing auth check in server function                | Always verify session from `request.headers`                      |
| Form not showing server errors                       | Use `form.setErrorMap({ onServer: error })`                       |
| Infinite query without proper cursor                 | Provide `initialPageParam` and `getNextPageParam`                 |
| Not prefetching for SSR                              | Use `ensureQueryData` in route loaders                            |
| Table state not synced to URL                        | Use `validateSearch` + navigate on change                         |
| Handling error in onError instead of checking result | Server functions return errors in result, not thrown              |
| Not resetting page on filter change                  | Set `page: 1` when search/filter changes                          |
| Missing loading states                               | Show skeletons during `isPending`, overlays during `isFetching`   |
| No error boundary on routes                          | Add `errorComponent` and `notFoundComponent`                      |

---

## Delegation

- **Pattern discovery**: For finding existing implementations, use `Explore` agent
- **Code review**: After implementing flows, delegate to `code-reviewer` agent
- **Security audit**: For auth flows, delegate to `security-auditor` agent

## Related Skills

| Skill                                            | Use For                                              |
| ------------------------------------------------ | ---------------------------------------------------- |
| [tanstack-query](../tanstack-query/SKILL.md)     | Query patterns, caching, mutations, infinite queries |
| [tanstack-form](../tanstack-form/SKILL.md)       | Form validation, field components, composable forms  |
| [tanstack-router](../tanstack-router/SKILL.md)   | Route guards, loaders, search params, navigation     |
| [tanstack-start](../tanstack-start/SKILL.md)     | Server functions, API routes, middleware             |
| [server-functions](../server-functions/SKILL.md) | createServerFn patterns, validation, auth            |
| [error-boundaries](../error-boundaries/SKILL.md) | Route errors, global errors, recovery                |
| [auth](../auth/SKILL.md)                         | Better Auth, sessions, protected routes              |
| [database](../database/SKILL.md)                 | Drizzle ORM, queries, relations                      |
