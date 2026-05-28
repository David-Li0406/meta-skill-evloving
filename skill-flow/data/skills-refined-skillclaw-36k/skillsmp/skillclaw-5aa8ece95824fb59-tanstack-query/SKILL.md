---
name: tanstack-query
description: Use this skill for managing server state in React applications with TanStack Query, including data fetching, caching, and synchronization.
---

# TanStack Query Best Practices

## Summary

TanStack Query (formerly React Query) is a powerful asynchronous state management library for React that simplifies server-state fetching, caching, synchronization, and updates. It provides built-in features like background refetching, optimistic updates, pagination, and intelligent cache management.

## When to Use

Use TanStack Query when:
- Fetching data from REST APIs, GraphQL, or tRPC endpoints.
- You need automatic background refetching and cache invalidation.
- Building real-time dashboards with polling or websocket data.
- Implementing infinite scroll or pagination.
- You require optimistic UI updates for mutations.
- Managing complex server-state synchronization.
- You need offline support with cache persistence.
- Building applications with frequent data updates.

## Quick Start

### Installation

```bash
npm install @tanstack/react-query
# DevTools (optional but recommended)
npm install @tanstack/react-query-devtools
```

### Basic Setup

```tsx
// app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60 * 1000, // 1 minute
        gcTime: 5 * 60 * 1000, // 5 minutes
        retry: 1,
        refetchOnWindowFocus: false,
      },
    },
  }));

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

## Core Principles

- Use TanStack Query for all server state management and data fetching.
- Minimize the use of `useEffect` and `useState` for server data; favor TanStack Query's built-in state management.
- Implement proper error handling with user-friendly messages.
- Use TypeScript for full type safety with query responses.

## Query Patterns

### Basic Query Hook

Fetch data with automatic caching:

```tsx
import { useQuery } from '@tanstack/react-query';
import { fetchUser, User } from '@/services/api/users';

export function useUser(userId: string) {
  return useQuery<User, Error>(
    ['user', userId],
    () => fetchUser(userId),
    {
      enabled: !!userId,
      staleTime: 1000 * 60 * 10, // 10 minutes
    }
  );
}
```

### Query with Error Handling

Services should throw user-friendly errors that TanStack Query can catch and display:

```typescript
// services/api/users.ts
export async function fetchUser(userId: string): Promise<User> {
  const response = await fetch(`/api/users/${userId}`);
  if (!response.ok) throw new Error('Failed to fetch user');
  return response.json() as Promise<User>;
}
```

## Query Key Organization

Use consistent, hierarchical query keys for efficient cache management:

```typescript
// Query key factory pattern
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
};
```

## Best Practices

- Use arrays for all query keys.
- Order keys from general to specific.
- Handle loading states and errors properly.
- Avoid excessive API calls through proper caching strategies.

## Advanced Topics

- Optimistic updates
- Pagination
- Server-side rendering (SSR) hydration
- Integration patterns
- Performance optimizations