# Advanced Features Reference

## Route Masks

Hide sensitive route info from URL:

```tsx
<Link
  to="/posts/$postId"
  params={{ postId: '123' }}
  mask={{ to: '/posts', search: { preview: '123' } }}
>
  Preview Post
</Link>

// URL shows: /posts?preview=123
// Router navigates to: /posts/123
```

## Code Splitting

Routes are automatically code-split. For explicit control:

```tsx
export const Route = createFileRoute('/heavy-page')({
  component: lazyRouteComponent(
    () => import('./heavy-page-component'),
    'HeavyPageComponent',
  ),
});
```

## Router State Hooks

```tsx
import { useRouterState, useRouter } from '@tanstack/react-router';

function Component() {
  const isLoading = useRouterState({ select: (s) => s.isLoading });
  const currentPath = useRouterState({ select: (s) => s.location.pathname });
  const pendingMatches = useRouterState({ select: (s) => s.pendingMatches });

  const router = useRouter();

  const refresh = () => router.invalidate();
  const preload = () => router.preloadRoute({ to: '/posts' });
}
```

## Scroll Restoration

### Default Behavior

TanStack Router automatically restores scroll position when navigating back/forward:

```tsx
export const getRouter = () =>
  createRouter({
    routeTree,
    scrollRestoration: true, // Default: true
    defaultPreloadStaleTime: 0,
  });
```

### Custom Scroll Behavior

```tsx
export const Route = createFileRoute('/posts')({
  component: PostsPage,
  scrollRestoration: {
    // Restore scroll based on element, not window
    getElement: () => document.getElementById('posts-container'),
  },
});
```

### Scroll to Top on Navigation

```tsx
<Link to="/posts" resetScroll>
  Posts
</Link>;

navigate({ to: '/posts', resetScroll: true });
```

### Preserve Scroll on Filter Changes

```tsx
const navigate = useNavigate();

const setFilter = (filter: string) => {
  navigate({
    search: (prev) => ({ ...prev, filter }),
    resetScroll: false, // Don't reset scroll
  });
};
```

## Preloading Strategies

### Link Preloading

```tsx
// Preload on hover (default)
<Link to="/posts" preload="intent">Posts</Link>

// Preload when link renders
<Link to="/posts" preload="render">Posts</Link>

// Preload when link enters viewport
<Link to="/posts" preload="viewport">Posts</Link>

// Disable preloading
<Link to="/posts" preload={false}>Posts</Link>
```

### Programmatic Preloading

```tsx
const router = useRouter();

await router.preloadRoute({ to: '/posts/$postId', params: { postId: '123' } });

const handleMouseEnter = () => {
  router.preloadRoute({ to: '/dashboard' });
};
```

### Preload Stale Time

```tsx
export const getRouter = () =>
  createRouter({
    routeTree,
    // How long preloaded data stays fresh
    defaultPreloadStaleTime: 30_000, // 30 seconds
  });
```

## Navigation Guards

### Block Navigation (Dirty Form)

```tsx
import { useBlocker } from '@tanstack/react-router';

function EditForm() {
  const [isDirty, setIsDirty] = useState(false);

  useBlocker({
    shouldBlockFn: () => {
      if (!isDirty) return false;
      const shouldLeave = window.confirm(
        'You have unsaved changes. Leave anyway?',
      );
      return !shouldLeave; // Return true to BLOCK, false to allow
    },
  });

  return <form>{/* ... */}</form>;
}
```

## History State

Store ephemeral state that survives navigation:

```tsx
navigate({
  to: '/posts/$postId',
  params: { postId: '123' },
  state: { fromFeed: true, scrollPosition: 500 },
});

function PostPage() {
  const state = useRouterState({ select: (s) => s.location.state });
  const fromFeed = state?.fromFeed;
}
```

## Type Utilities

```tsx
import type {
  RouteIds,
  RegisteredRouter,
  ParseRoute,
} from '@tanstack/react-router';

type AllRouteIds = RouteIds<RegisteredRouter['routeTree']>;

type PostParams = ParseRoute<
  RegisteredRouter['routeTree'],
  '/posts/$postId'
>['params'];
```
