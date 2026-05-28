# Route Context Reference

## Context Inheritance Philosophy

TanStack Router enables **type-safe state accumulation** across nested routes. Three things inherit automatically:

| Inheritance   | Source                     | Example                                           |
| ------------- | -------------------------- | ------------------------------------------------- |
| Path params   | Parent routes              | `dashboardId: number` from parent → child         |
| Search params | Global + route-specific    | `debug: boolean` at root merges with route search |
| Route context | `beforeLoad` return values | `{ user, permissions }` flows to all children     |

Types compose from the **entire parent hierarchy** automatically - no manual type annotations needed.

## Defining Context in Root

```tsx
// src/routes/__root.tsx
import { createRootRouteWithContext } from '@tanstack/react-router';
import type { QueryClient } from '@tanstack/react-query';

type RouterContext = {
  queryClient: QueryClient;
  auth: {
    getSession: () => Promise<Session | null>;
  };
};

export const Route = createRootRouteWithContext<RouterContext>()({
  component: RootComponent,
});
```

## Providing Context

```tsx
// src/router.tsx
export const getRouter = () =>
  createRouter({
    routeTree,
    context: {
      queryClient,
      auth: {
        getSession: () => auth.api.getSession({ headers: getHeaders() }),
      },
    },
  });
```

## Using Context in Routes

```tsx
export const Route = createFileRoute('/dashboard')({
  beforeLoad: async ({ context }) => {
    const session = await context.auth.getSession();
    // context.queryClient available too
  },
  loader: async ({ context }) => {
    return context.queryClient.ensureQueryData(dashboardOptions());
  },
});
```

## beforeLoad Hook

Runs before loader, ideal for auth checks and redirects.

```tsx
export const Route = createFileRoute('/_app')({
  beforeLoad: async ({ context, location }) => {
    const session = await context.auth.getSession();

    if (!session) {
      throw redirect({
        to: '/login',
        search: { redirect: location.href },
      });
    }

    // Return data to extend context for child routes
    return {
      user: session.user,
      permissions: session.permissions,
    };
  },
});

// Child routes receive extended context
export const Route = createFileRoute('/_app/admin')({
  beforeLoad: async ({ context }) => {
    // context.user and context.permissions available
    if (!context.permissions.includes('admin')) {
      throw redirect({ to: '/unauthorized' });
    }
  },
});
```

## Nested Layouts

### Pathless Layout Routes

```sh
src/routes/
├── _app.tsx           # Layout for authenticated routes
├── _app/
│   ├── dashboard.tsx  # /dashboard
│   ├── settings.tsx   # /settings
│   └── profile.tsx    # /profile
├── _public.tsx        # Layout for public routes
└── _public/
    ├── login.tsx      # /login
    └── register.tsx   # /register
```

### Layout Component Pattern

```tsx
// src/routes/_app.tsx
import { Outlet } from '@tanstack/react-router';

export const Route = createFileRoute('/_app')({
  component: AppLayout,
  beforeLoad: async ({ context }) => {
    // Auth check for all child routes
  },
});

function AppLayout() {
  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1">
        <Outlet /> {/* Child routes render here */}
      </main>
    </div>
  );
}
```
