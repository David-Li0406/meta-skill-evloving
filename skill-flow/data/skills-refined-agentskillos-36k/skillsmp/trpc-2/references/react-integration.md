# React & Next.js Integration

Complete guide for integrating tRPC with React and Next.js applications.

## Table of Contents

1. [TanStack React Query Setup (Recommended)](#tanstack-react-query-setup)
2. [Classic React Query Setup](#classic-react-query-setup)
3. [Next.js Pages Router](#nextjs-pages-router)
4. [Next.js App Router](#nextjs-app-router)
5. [Usage Patterns](#usage-patterns)

---

## TanStack React Query Setup

The new recommended approach using `@trpc/tanstack-react-query`.

### Installation

```bash
npm install @trpc/server @trpc/client @trpc/tanstack-react-query @tanstack/react-query zod
```

### Setup (utils/trpc.ts)

```typescript
import { createTRPCContext } from '@trpc/tanstack-react-query';
import { httpBatchLink } from '@trpc/client';
import { QueryClient } from '@tanstack/react-query';
import type { AppRouter } from '../server/routers/_app';
import superjson from 'superjson';

// Create query client
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
    },
  },
});

// Create tRPC context
export const { TRPCProvider, useTRPC, useTRPCClient } = createTRPCContext<AppRouter>({
  links: [
    httpBatchLink({
      url: '/api/trpc',
      transformer: superjson,
      headers: () => ({
        authorization: getAuthToken(),
      }),
    }),
  ],
});

// Alternative: Singleton pattern (for simpler apps)
export const trpc = createTRPCContext<AppRouter>({
  links: [httpBatchLink({ url: '/api/trpc', transformer: superjson })],
});
```

### Provider Setup (App.tsx)

```tsx
import { QueryClientProvider } from '@tanstack/react-query';
import { TRPCProvider, queryClient } from './utils/trpc';

export function App({ children }: { children: React.ReactNode }) {
  return (
    <TRPCProvider>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </TRPCProvider>
  );
}
```

### Usage in Components

```tsx
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTRPC } from '../utils/trpc';

export function UserList() {
  const trpc = useTRPC();
  const queryClient = useQueryClient();

  // Query
  const usersQuery = useQuery(trpc.user.list.queryOptions());

  // Query with input
  const userQuery = useQuery(trpc.user.byId.queryOptions({ id: '1' }));

  // Mutation
  const createUser = useMutation(trpc.user.create.mutationOptions({
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: trpc.user.list.queryKey() });
    },
  }));

  // Suspense query (with React Suspense)
  const [users] = useSuspenseQuery(trpc.user.list.queryOptions());

  return (
    <div>
      {usersQuery.data?.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
      <button onClick={() => createUser.mutate({ name: 'New User', email: 'new@example.com' })}>
        Add User
      </button>
    </div>
  );
}
```

---

## Classic React Query Setup

The original approach using `@trpc/react-query`.

### Installation

```bash
npm install @trpc/server @trpc/client @trpc/react-query @tanstack/react-query zod
```

### Setup (utils/trpc.ts)

```typescript
import { createTRPCReact } from '@trpc/react-query';
import type { AppRouter } from '../server/routers/_app';

export const trpc = createTRPCReact<AppRouter>();
```

### Provider Setup

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { httpBatchLink } from '@trpc/client';
import { useState } from 'react';
import { trpc } from './utils/trpc';
import superjson from 'superjson';

export function App() {
  const [queryClient] = useState(() => new QueryClient());
  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        httpBatchLink({
          url: '/api/trpc',
          transformer: superjson,
        }),
      ],
    })
  );

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        {/* App content */}
      </QueryClientProvider>
    </trpc.Provider>
  );
}
```

### Usage

```tsx
import { trpc } from '../utils/trpc';

export function UserList() {
  const users = trpc.user.list.useQuery();
  const user = trpc.user.byId.useQuery({ id: '1' });
  const createUser = trpc.user.create.useMutation();
  const utils = trpc.useUtils();

  const handleCreate = async () => {
    await createUser.mutateAsync({ name: 'John', email: 'john@example.com' });
    utils.user.list.invalidate();
  };

  return (/* ... */);
}
```

---

## Next.js Pages Router

### API Route Handler (pages/api/trpc/[trpc].ts)

```typescript
import { createNextApiHandler } from '@trpc/server/adapters/next';
import { appRouter } from '../../../server/routers/_app';
import { createContext } from '../../../server/context';

export default createNextApiHandler({
  router: appRouter,
  createContext,
  onError: ({ error, path }) => {
    console.error(`tRPC error on ${path}:`, error);
  },
});
```

### _app.tsx Setup

```tsx
import { trpc } from '../utils/trpc';

function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}

export default trpc.withTRPC(MyApp);
```

### utils/trpc.ts for Pages Router

```typescript
import { httpBatchLink } from '@trpc/client';
import { createTRPCNext } from '@trpc/next';
import type { AppRouter } from '../server/routers/_app';
import superjson from 'superjson';

function getBaseUrl() {
  if (typeof window !== 'undefined') return '';
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
  return `http://localhost:${process.env.PORT ?? 3000}`;
}

export const trpc = createTRPCNext<AppRouter>({
  config() {
    return {
      transformer: superjson,
      links: [
        httpBatchLink({
          url: `${getBaseUrl()}/api/trpc`,
        }),
      ],
    };
  },
  ssr: false, // Set true for SSR
});
```

---

## Next.js App Router

### API Route Handler (app/api/trpc/[trpc]/route.ts)

```typescript
import { fetchRequestHandler } from '@trpc/server/adapters/fetch';
import { appRouter } from '@/server/routers/_app';
import { createContext } from '@/server/context';

const handler = (req: Request) =>
  fetchRequestHandler({
    endpoint: '/api/trpc',
    req,
    router: appRouter,
    createContext,
  });

export { handler as GET, handler as POST };
```

### Server-Side Caller (trpc/server.ts)

```typescript
import 'server-only';
import { cache } from 'react';
import { createCallerFactory } from '@trpc/server';
import { appRouter } from '@/server/routers/_app';
import { createContext } from '@/server/context';

const createCaller = createCallerFactory(appRouter);

export const api = cache(async () => {
  const ctx = await createContext();
  return createCaller(ctx);
});
```

### Server Component Usage

```tsx
// app/users/page.tsx
import { api } from '@/trpc/server';

export default async function UsersPage() {
  const caller = await api();
  const users = await caller.user.list();

  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

### Client Component Usage

```tsx
'use client';

import { useQuery, useMutation } from '@tanstack/react-query';
import { useTRPC } from '@/trpc/react';

export function UserList() {
  const trpc = useTRPC();
  
  const users = useQuery(trpc.user.list.queryOptions());
  const createUser = useMutation(trpc.user.create.mutationOptions());

  return (/* ... */);
}
```

### Hydration for Server/Client

```tsx
// trpc/react.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createTRPCContext } from '@trpc/tanstack-react-query';
import { httpBatchLink } from '@trpc/client';
import { useState } from 'react';
import type { AppRouter } from '@/server/routers/_app';
import superjson from 'superjson';

export const { TRPCProvider, useTRPC } = createTRPCContext<AppRouter>();

export function TRPCReactProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <TRPCProvider
      queryClient={queryClient}
      links={[
        httpBatchLink({
          url: '/api/trpc',
          transformer: superjson,
        }),
      ]}
    >
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </TRPCProvider>
  );
}
```

---

## Usage Patterns

### Prefetching

```tsx
// Server Component prefetch
export default async function Page() {
  const caller = await api();
  await caller.user.list(); // Prefetch
  
  return <UserList />;
}

// Client-side prefetch
const trpc = useTRPC();
const queryClient = useQueryClient();

useEffect(() => {
  queryClient.prefetchQuery(trpc.user.byId.queryOptions({ id: nextUserId }));
}, [nextUserId]);
```

### Infinite Queries

```tsx
const postsQuery = useInfiniteQuery(
  trpc.post.infiniteList.infiniteQueryOptions(
    { limit: 10 },
    {
      getNextPageParam: (lastPage) => lastPage.nextCursor,
    }
  )
);
```

### Optimistic Updates

```tsx
const trpc = useTRPC();
const queryClient = useQueryClient();

const updateUser = useMutation(
  trpc.user.update.mutationOptions({
    onMutate: async (newData) => {
      await queryClient.cancelQueries({ queryKey: trpc.user.byId.queryKey({ id: newData.id }) });
      const previous = queryClient.getQueryData(trpc.user.byId.queryKey({ id: newData.id }));
      queryClient.setQueryData(trpc.user.byId.queryKey({ id: newData.id }), (old) => ({
        ...old,
        ...newData,
      }));
      return { previous };
    },
    onError: (err, newData, context) => {
      queryClient.setQueryData(
        trpc.user.byId.queryKey({ id: newData.id }),
        context?.previous
      );
    },
    onSettled: (data, err, newData) => {
      queryClient.invalidateQueries({ queryKey: trpc.user.byId.queryKey({ id: newData.id }) });
    },
  })
);
```

### Error Handling in Components

```tsx
const userQuery = useQuery(trpc.user.byId.queryOptions({ id }));

if (userQuery.error) {
  if (userQuery.error.data?.code === 'NOT_FOUND') {
    return <NotFound />;
  }
  if (userQuery.error.data?.code === 'UNAUTHORIZED') {
    return <Redirect to="/login" />;
  }
  return <Error message={userQuery.error.message} />;
}
```