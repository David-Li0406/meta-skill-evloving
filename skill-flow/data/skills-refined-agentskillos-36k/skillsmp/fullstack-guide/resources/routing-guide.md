# Routing Guide

TanStack Router implementation with folder-based routing and lazy loading patterns.

---

## TanStack Router Overview

**TanStack Router** with file-based routing:
- Folder structure defines routes
- Lazy loading for code splitting
- Type-safe routing
- Breadcrumb loaders

---

## Folder-Based Routing

### Directory Structure

```
routes/
  __root.tsx                    # Root layout
  index.tsx                     # Home route (/)
  posts/
    index.tsx                   # /posts
    create/
      index.tsx                 # /posts/create
    $postId.tsx                 # /posts/:postId (dynamic)
  users/
    index.tsx                   # /users
```

**Pattern**:
- `index.tsx` = Route at that path
- `$param.tsx` = Dynamic parameter
- Nested folders = Nested routes

---

## Basic Route Pattern

### Example Route

```typescript
/**
 * Posts route component
 * Displays the main blog posts list
 */

import { createFileRoute } from '@tanstack/react-router';
import { lazy } from 'react';

// Lazy load the page component
const PostsList = lazy(() =>
    import('@/features/posts/components/PostsList').then(
        (module) => ({ default: module.PostsList })
    )
);

export const Route = createFileRoute('/posts/')({
    component: PostsPage,
    loader: () => ({
        crumb: 'Posts',
    }),
});

function PostsPage() {
    return (
        <SuspenseLoader>
            <PostsList />
        </SuspenseLoader>
    );
}

export default PostsPage;
```

---

## Dynamic Routes

### Parameter Route

```typescript
// routes/users/$userId.tsx
import { createFileRoute } from '@tanstack/react-router';

export const Route = createFileRoute('/users/$userId')({
    component: UserPage,
    loader: () => ({
        crumb: 'User Details',
    }),
});

function UserPage() {
    const { userId } = Route.useParams();

    return (
        <SuspenseLoader>
            <UserProfile userId={userId} />
        </SuspenseLoader>
    );
}
```

---

## Navigation

### useNavigate Hook

```typescript
import { useNavigate } from '@tanstack/react-router';

export const MyComponent: React.FC = () => {
    const navigate = useNavigate();

    const handleClick = () => {
        // Navigate to route
        navigate({ to: '/users' });

        // With params
        navigate({ to: '/users/$userId', params: { userId: '123' } });

        // With query params
        navigate({ to: '/users', search: { page: 1 } });
    };
};
```

### Link Component

```typescript
import { Link } from '@tanstack/react-router';

<Link to="/users">Users</Link>

<Link to="/users/$userId" params={{ userId: '123' }}>
    View User
</Link>
```

---

## Breadcrumb Loaders

### Using loader for Breadcrumbs

```typescript
export const Route = createFileRoute('/posts/$postId')({
    component: PostPage,
    loader: ({ params }) => ({
        crumb: `Post ${params.postId}`,
    }),
});
```

---

## Root Layout

### __root.tsx

```typescript
import { createRootRoute, Outlet } from '@tanstack/react-router';
import { Box } from '@mui/material';
import { CustomAppBar } from '~components/CustomAppBar';

export const Route = createRootRoute({
    component: RootLayout,
});

function RootLayout() {
    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <CustomAppBar />
            <Box component="main" sx={{ flex: 1, p: 2 }}>
                <Outlet />
            </Box>
        </Box>
    );
}
```

---

## Complete Route Example

```typescript
/**
 * User profile route
 * Path: /users/:userId
 */

import { createFileRoute } from '@tanstack/react-router';
import { lazy } from 'react';
import { SuspenseLoader } from '~components/SuspenseLoader';

// Lazy load heavy component
const UserProfile = lazy(() =>
    import('@/features/users/components/UserProfile').then(
        (module) => ({ default: module.UserProfile })
    )
);

export const Route = createFileRoute('/users/$userId')({
    component: UserPage,
    loader: () => ({
        crumb: 'User Profile',
    }),
});

function UserPage() {
    const { userId } = Route.useParams();

    return (
        <SuspenseLoader>
            <UserProfile userId={userId} />
        </SuspenseLoader>
    );
}

export default UserPage;
```

---

## Summary

**Routing Checklist:**
- ✅ Folder-based: `routes/my-route/index.tsx`
- ✅ Lazy load components: `React.lazy(() => import())`
- ✅ Use `createFileRoute` with route path
- ✅ Add breadcrumb in `loader` function
- ✅ Wrap in `SuspenseLoader` for loading states
- ✅ Use `Route.useParams()` for dynamic params
- ✅ Use `useNavigate()` for programmatic navigation

**See Also:**
- [component-patterns.md](component-patterns.md) - Lazy loading patterns
- [loading-and-error-states.md](loading-and-error-states.md) - SuspenseLoader usage
