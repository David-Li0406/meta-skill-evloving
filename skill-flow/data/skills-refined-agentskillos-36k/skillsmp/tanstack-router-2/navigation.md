# Navigation Reference

## Type Safety in Shared Components

When building navigation components used across multiple routes:

```tsx
// Shared breadcrumb component - doesn't know which route it's in
function Breadcrumbs() {
  // Use strict: false to get union of all possible params
  const params = useParams({ strict: false });
  //    ^? { postId?: string, userId?: string, ... }

  // Use strict: false for search too
  const search = useSearch({ strict: false });
  //    ^? Partial<FullSearchSchema>

  return <nav>{/* Build breadcrumbs from available params */}</nav>;
}

function PostNavigation() {
  const navigate = useNavigate({ from: '/posts/$postId' });

  const goToNext = () => {
    navigate({ to: '.', params: { postId: 'next-id' } });
  };
}
```

## Link with Type Inference

```tsx
// TypeScript enforces correct params and search
<Link
  to="/posts/$postId"
  params={{ postId: post.id }}
  search={{ tab: 'comments' }}
  activeProps={{ className: 'font-bold' }}
  activeOptions={{ exact: true }}
>
  View Post
</Link>
```

## Navigate with From Context

```tsx
const navigate = useNavigate({ from: '/posts/$postId' });

// Can use relative navigation
navigate({ to: '..', search: { page: 1 } }); // Go to /posts
navigate({ to: '.', search: (prev) => ({ ...prev, tab: 'edit' }) }); // Stay, update search
```

## Match Route Check

```tsx
import { useMatchRoute } from '@tanstack/react-router';

function Sidebar() {
  const matchRoute = useMatchRoute();

  const isOnDashboard = matchRoute({ to: '/dashboard' });
  const isOnPostsSection = matchRoute({ to: '/posts', fuzzy: true });

  return (
    <nav>
      <Link to="/dashboard" data-active={isOnDashboard}>
        Dashboard
      </Link>
    </nav>
  );
}
```

## Active Link Styling

```tsx
<Link
  to="/dashboard"
  activeProps={{
    className: 'text-primary font-semibold',
  }}
  inactiveProps={{
    className: 'text-muted-foreground',
  }}
>
  Dashboard
</Link>

<Link
  to="/posts"
  className="data-[status=active]:text-primary"
>
  Posts
</Link>
```

## Hash Navigation

```tsx
<Link to="." hash="comments">
  Jump to Comments
</Link>

<Link to="/about" hash="team">
  Meet the Team
</Link>

navigate({ hash: 'section-2' });
```
