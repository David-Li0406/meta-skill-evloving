---
name: tanstack-query
description: TanStack Query v5 patterns and common pitfalls. Use when implementing data fetching, cache invalidation, or debugging stale data issues. Triggers on useQuery, useMutation, queryKey, invalidate, TanStack, React Query, data fetching, server state.
---

# TanStack Query v5 Patterns

Common pitfalls and correct patterns for TanStack Query v5 in Next.js applications.

## When to Use

- Implementing data fetching with useQuery
- Setting up mutations with useMutation
- Debugging stale data or cache issues
- Reviewing code that uses TanStack Query
- Building infinite scroll or pagination

## Workflow

### Step 1: Check Query Keys

Verify query keys use full URL paths for proper deduplication.

### Step 2: Verify Invalidation

Ensure mutations invalidate relevant queries on success.

### Step 3: Check v5 Patterns

Verify v5-specific patterns (isPending vs isLoading).

---

## Correct Usage

```typescript
// CORRECT: Full URL path in queryKey
const { data } = useQuery({
  queryKey: ['/api/v1/resources', resourceId],
  queryFn: () => api.get(`/api/v1/resources/${resourceId}`),
});

// CORRECT: Invalidate after mutation
const mutation = useMutation({
  mutationFn: (data) => api.post('/api/v1/resources', data),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['/api/v1/resources'] });
  },
});

// CORRECT: Type responses with schema types
import type { Resource } from '@/lib/api';
const { data } = useQuery<{ data: Resource[] }>({
  queryKey: ['/api/v1/resources'],
  queryFn: fetchResources,
});
```

## Anti-Patterns

```typescript
// WRONG: Short queryKey
queryKey: ['resources']  // Won't dedupe properly

// WRONG: Forgetting to invalidate
onSuccess: () => { router.push('/'); }  // Stale cache!

// WRONG: Using isLoading for mutations
mutation.isLoading  // Use isPending in v5
```

## Vibe4Vets Patterns

### Resource List with Filters

```typescript
// hooks/useResources.ts
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

interface ResourceFilters {
  category?: string;
  state?: string;
  limit?: number;
  offset?: number;
}

export function useResources(filters: ResourceFilters = {}) {
  return useQuery({
    queryKey: ['/api/v1/resources', filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters.category) params.set('category', filters.category);
      if (filters.state) params.set('state', filters.state);
      if (filters.limit) params.set('limit', String(filters.limit));
      if (filters.offset) params.set('offset', String(filters.offset));

      const response = await api.get(`/api/v1/resources?${params}`);
      return response.data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
```

### Infinite Scroll for Discovery Feed

```typescript
// hooks/useResourcesInfinite.ts
import { useInfiniteQuery } from '@tanstack/react-query';
import { api } from '@/lib/api';

export function useResourcesInfinite(filters: ResourceFilters = {}) {
  return useInfiniteQuery({
    queryKey: ['/api/v1/resources', 'infinite', filters],
    queryFn: async ({ pageParam = 0 }) => {
      const params = new URLSearchParams();
      params.set('offset', String(pageParam));
      params.set('limit', '20');
      if (filters.category) params.set('category', filters.category);

      const response = await api.get(`/api/v1/resources?${params}`);
      return response.data;
    },
    getNextPageParam: (lastPage, allPages) => {
      if (lastPage.length < 20) return undefined;
      return allPages.flat().length;
    },
    initialPageParam: 0,
  });
}
```

### Search with Debounce

```typescript
// hooks/useSearch.ts
import { useQuery } from '@tanstack/react-query';
import { useDebouncedValue } from '@/hooks/useDebouncedValue';

export function useSearch(query: string) {
  const debouncedQuery = useDebouncedValue(query, 300);

  return useQuery({
    queryKey: ['/api/v1/search', debouncedQuery],
    queryFn: async () => {
      if (!debouncedQuery || debouncedQuery.length < 2) return [];
      const response = await api.get(`/api/v1/search?q=${encodeURIComponent(debouncedQuery)}`);
      return response.data;
    },
    enabled: debouncedQuery.length >= 2,
    staleTime: 10 * 60 * 1000, // Cache search results for 10 min
  });
}
```

### Admin Mutations

```typescript
// hooks/useReviewResource.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';

export function useReviewResource() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ resourceId, approved }: { resourceId: number; approved: boolean }) => {
      const response = await api.post(`/api/v1/admin/review/${resourceId}`, { approved });
      return response.data;
    },
    onSuccess: (_, { resourceId }) => {
      // Invalidate the specific resource and the review queue
      queryClient.invalidateQueries({ queryKey: ['/api/v1/resources', resourceId] });
      queryClient.invalidateQueries({ queryKey: ['/api/v1/admin/review-queue'] });
    },
    onError: (error) => {
      toast.error('Failed to review resource');
    },
  });
}
```

## Optimistic Updates

```typescript
// Update UI immediately, rollback on error
const mutation = useMutation({
  mutationFn: updateResource,
  onMutate: async (newData) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['/api/v1/resources', id] });

    // Snapshot previous value
    const previous = queryClient.getQueryData(['/api/v1/resources', id]);

    // Optimistic update
    queryClient.setQueryData(['/api/v1/resources', id], newData);

    return { previous };
  },
  onError: (err, newData, context) => {
    // Rollback on error
    queryClient.setQueryData(['/api/v1/resources', id], context?.previous);
    toast.error('Update failed');
  },
  onSettled: () => {
    // Always refetch after error or success
    queryClient.invalidateQueries({ queryKey: ['/api/v1/resources', id] });
  },
});
```

## Provider Setup

```typescript
// components/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1 minute
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

## Quick Checklist

- [ ] QueryKeys use full URL paths (e.g., `/api/v1/resources`)
- [ ] Mutations invalidate relevant queries
- [ ] Using `isPending` (not `isLoading`) for mutations in v5
- [ ] Responses typed with proper TypeScript types
- [ ] `staleTime` set appropriately for data freshness needs
- [ ] `enabled` option used for conditional queries
- [ ] Error handling with `onError` callbacks
- [ ] Optimistic updates for better UX where appropriate
