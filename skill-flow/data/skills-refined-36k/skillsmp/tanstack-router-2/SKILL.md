---
name: tanstack-router
description: TanStack Router file-based routing. Use for routes, params, search params, navigation, loaders, auth guards, layouts, nested routes, redirect
---

# TanStack Router

## File-Based Routing

```sh
routes/
├── __root.tsx        # Root layout (meta, providers)
├── index.tsx         # / (homepage)
├── _app.tsx          # Layout for /_app/* routes
├── _app/
│   ├── index.tsx     # /app
│   └── settings.tsx  # /app/settings
├── posts.tsx         # /posts (list)
├── posts/
│   └── $id.tsx       # /posts/:id (detail)
└── api/
    └── auth/$.tsx    # /api/auth/* (catch-all)
```

## Route Definition

```tsx
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/posts/$id')({
  component: PostPage,
  loader: async ({ params }) => fetchPost(params.id),
  validateSearch: z.object({ tab: z.string().optional() }),
  errorComponent: PostError,
  pendingComponent: PostSkeleton,
});

function PostPage() {
  const post = Route.useLoaderData();
  const { tab } = Route.useSearch();
  const { id } = Route.useParams();
  return <Post data={post} />;
}
```

## Route Context Pattern

```tsx
// __root.tsx
import { createRootRouteWithContext } from '@tanstack/react-router';

type RouterContext = {
  queryClient: QueryClient;
};

export const Route = createRootRouteWithContext<RouterContext>()({
  component: RootLayout,
});

// router.tsx
export const getRouter = () =>
  createRouter({
    routeTree,
    context: { queryClient },
  });
```

## Auth Guard (beforeLoad)

```tsx
export const Route = createFileRoute('/_app')({
  beforeLoad: async ({ context }) => {
    const session = await auth.api.getSession({
      headers: context.request.headers,
    });

    if (!session) {
      throw redirect({ to: '/login' });
    }

    return { user: session.user };
  },
  component: AppLayout,
});
```

## Navigation

```tsx
import { Link, useNavigate } from '@tanstack/react-router';

// Link component
<Link to="/posts/$id" params={{ id: '123' }} search={{ tab: 'comments' }}>
  View Post
</Link>;

// Programmatic navigation
const navigate = useNavigate();
navigate({ to: '/posts', search: { page: 2 } });
navigate({ to: '..', search: (prev) => ({ ...prev }) }); // Relative
```

## Search Params with Zod

```tsx
import { zodValidator } from '@tanstack/zod-adapter';
import { stripSearchParams } from '@tanstack/react-router';

const defaults = { page: 1, sort: 'newest' as const };

const searchSchema = z.object({
  page: z.number().default(defaults.page),
  sort: z.enum(['newest', 'oldest']).default(defaults.sort),
  filter: z.string().optional(),
});

export const Route = createFileRoute('/posts')({
  validateSearch: zodValidator(searchSchema),
  search: { middlewares: [stripSearchParams(defaults)] },
  component: PostsPage,
});

function PostsPage() {
  const { page, sort, filter } = Route.useSearch();
  const navigate = useNavigate();

  const setPage = (newPage: number) => {
    navigate({ search: (prev) => ({ ...prev, page: newPage }) });
  };
}
```

## Layout Routes

```tsx
// _app.tsx - Pathless layout
export const Route = createFileRoute('/_app')({
  component: AppLayout,
});

function AppLayout() {
  return (
    <div className="flex">
      <Sidebar />
      <main>
        <Outlet /> {/* Child routes render here */}
      </main>
    </div>
  );
}
```

## Loader with TanStack Query

```tsx
export const Route = createFileRoute('/posts')({
  loader: async ({ context }) => {
    await context.queryClient.ensureQueryData(postsOptions());
  },
  component: PostsPage,
});

function PostsPage() {
  const { data } = useSuspenseQuery(postsOptions());
  return <PostList posts={data} />;
}
```

## Common Mistakes

| Mistake                                | Correct Pattern                         |
| -------------------------------------- | --------------------------------------- |
| Using `validateSearch` without adapter | Use `zodValidator(schema)`              |
| Auth check in component                | Use `beforeLoad` for route guards       |
| Not awaiting `ensureQueryData`         | Await to block navigation until ready   |
| Forgetting `Outlet` in layouts         | Layout components need `<Outlet />`     |
| Hardcoding paths in navigate           | Use type-safe `to` with params          |
| Missing `$` prefix for dynamic routes  | Use `$id.tsx` not `id.tsx`              |
| Route params without validation        | Validate with Zod in loader             |
| Not using `search` middleware          | Use `stripSearchParams` for clean URLs  |
| Circular redirects in beforeLoad       | Check current location before redirect  |
| Not handling 404 in loader             | Use `throw notFound()` for missing data |

## Delegation

- **Query patterns**: For data fetching in loaders, see [tanstack-query](../tanstack-query/SKILL.md) skill
- **Server functions**: For API calls, see [tanstack-start](../tanstack-start/SKILL.md) skill
- **Auth patterns**: For authentication, see [auth](../auth/SKILL.md) skill
- **Code review**: After implementing routes, delegate to `code-reviewer` agent

## Topic References

- [Route Context](route-context.md) - Context inheritance, beforeLoad, nested layouts
- [Search Params](search-params.md) - zodValidator, stripSearchParams, URL state
- [Navigation](navigation.md) - Link, useNavigate, active states, type safety
- [Loaders & Errors](loaders-errors.md) - Data loading, error boundaries, Suspense
- [Advanced Features](advanced-features.md) - Preloading, scroll restoration, code splitting
