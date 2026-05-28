---
name: error-boundaries
description: React error boundaries + fallback UIs. Use for error, catch, boundary, fallback, recovery, crash, ErrorBoundary, errorComponent, reset
---

# Error Boundaries

## Quick Start

TanStack Router provides built-in error handling:

```tsx
import { Button } from '@oakoss/ui';

export const Route = createFileRoute('/posts/$id')({
  errorComponent: ({ error, reset }) => (
    <div className="p-4">
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <Button onPress={reset}>Try again</Button>
    </div>
  ),
});
```

## Error Component Types

| Level     | Component               | Use Case                |
| --------- | ----------------------- | ----------------------- |
| Route     | `errorComponent`        | Route-specific errors   |
| Global    | `defaultErrorComponent` | Fallback for all routes |
| Not Found | `notFoundComponent`     | 404 errors              |

## Route-Level Error Boundary

```tsx
import { Button } from '@oakoss/ui';
import { AlertCircle } from 'lucide-react';

export const Route = createFileRoute('/dashboard')({
  component: DashboardComponent,
  errorComponent: DashboardError,
  pendingComponent: DashboardLoading,
});

function DashboardError({ error, reset }: ErrorComponentProps) {
  return (
    <div className="flex flex-col items-center gap-4 p-8">
      <AlertCircle className="size-12 text-destructive" />
      <h2 className="text-lg font-semibold">Failed to load dashboard</h2>
      <p className="text-muted-foreground">{error.message}</p>
      <Button onPress={reset}>Retry</Button>
    </div>
  );
}
```

## Global Error Boundary

Configure in router setup:

```tsx
// apps/web/src/router.tsx
import { GlobalError } from '@/components/errors/global-error';
import { NotFoundError } from '@/components/errors/not-found-error';

export const getRouter = () =>
  createRouter({
    routeTree,
    defaultErrorComponent: GlobalError,
    defaultNotFoundComponent: NotFoundError,
  });
```

## Error Component Props

```ts
type ErrorComponentProps = {
  error: Error; // The caught error
  reset: () => void; // Retry the operation
  info?: { componentStack: string }; // React error info
};
```

## Fallback UI Patterns

### Minimal Fallback

```tsx
function MinimalError({ error, reset }: ErrorComponentProps) {
  return (
    <div className="p-4 text-center">
      <p>Something went wrong.</p>
      <Button variant="link" onPress={reset}>
        Try again
      </Button>
    </div>
  );
}
```

### Detailed Fallback

```tsx
import { Card, CardHeader, CardContent, CardFooter, Button } from '@oakoss/ui';
import { AlertTriangle } from 'lucide-react';

function DetailedError({ error, reset }: ErrorComponentProps) {
  return (
    <Card className="mx-auto max-w-md">
      <CardHeader>
        <h2 className="flex items-center gap-2 text-lg font-semibold">
          <AlertTriangle className="text-destructive" />
          Error
        </h2>
      </CardHeader>
      <CardContent>
        <p className="text-muted-foreground">{error.message}</p>
        {process.env.NODE_ENV === 'development' && (
          <pre className="mt-4 overflow-auto rounded bg-muted p-2 text-xs">
            {error.stack}
          </pre>
        )}
      </CardContent>
      <CardFooter className="gap-2">
        <Button onPress={reset}>Retry</Button>
        <Button variant="secondary" onPress={() => window.location.reload()}>
          Reload page
        </Button>
      </CardFooter>
    </Card>
  );
}
```

## Not Found Component

```tsx
import { notFound, Link } from '@tanstack/react-router';
import { Button } from '@oakoss/ui';

export const Route = createFileRoute('/posts/$id')({
  loader: async ({ params }) => {
    const post = await getPost(params.id);
    if (!post) throw notFound();
    return post;
  },
  notFoundComponent: () => (
    <div className="p-8 text-center">
      <h2 className="text-xl font-semibold">Post not found</h2>
      <p className="text-muted-foreground">
        The post you're looking for doesn't exist.
      </p>
      <Button className="mt-4" asChild>
        <Link to="/posts">Back to posts</Link>
      </Button>
    </div>
  ),
});
```

## Triggering Not Found

```tsx
import { notFound } from '@tanstack/react-router';

// In loader
export const Route = createFileRoute('/posts/$id')({
  loader: async ({ params }) => {
    const post = await getPost(params.id);
    if (!post) throw notFound();
    return post;
  },
});

// In component
function PostContent() {
  const post = Route.useLoaderData();
  if (!post.published) throw notFound();
  return <article>...</article>;
}
```

## Common Mistakes

| Mistake                       | Correct Pattern                           |
| ----------------------------- | ----------------------------------------- |
| Not providing reset function  | Always include retry/reset button         |
| Catching errors in component  | Let errors bubble to boundary             |
| Missing route error component | Add `errorComponent` to routes            |
| Not logging errors            | Log to console and/or external service    |
| Showing stack trace in prod   | Only show in `NODE_ENV === 'development'` |
| Generic error message         | Show context-specific messages            |
| Missing notFoundComponent     | Handle 404s at route level                |
| Swallowing async errors       | Use error boundaries with Suspense        |
| No reload/escape option       | Provide "Reload page" fallback button     |
| Not handling loader errors    | Loader errors need `errorComponent` too   |

## Delegation

- **Error logging**: For monitoring, consider external services
- **Code review**: After creating error components, delegate to `code-reviewer` agent

## Related Skills

- Server error handling: [server-functions](../server-functions/SKILL.md) - Error codes, structured responses
- Route loaders: [tanstack-router](../tanstack-router/SKILL.md) - Loader errors, notFound()
- Integration flows: [integration-patterns](../integration-patterns/SKILL.md) - Full error handling patterns
