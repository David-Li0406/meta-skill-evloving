# Data Fetching with React Query

## Core Concepts

React Query (TanStack Query) provides:

- Caching and synchronization
- Background refetching
- Optimistic updates
- Request deduplication
- Automatic retries

## Query Client Setup

```typescript
// src/providers/QueryProvider.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 1000 * 60 * 5, // 5 minutes
        cacheTime: 1000 * 60 * 30, // 30 minutes
        retry: 2,
        refetchOnWindowFocus: false,
      },
    },
  }));

  const showDevtools = process.env.NODE_ENV === 'development' &&
    process.env.NEXT_PUBLIC_ENABLE_RQ_DEVTOOLS === '1';

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {showDevtools && <ReactQueryDevtools initialIsOpen={false} />}
    </QueryClientProvider>
  );
}
```

## Basic Queries

### useQuery Hook

```typescript
// src/hooks/queries/usePortfolioQuery.ts
import { useQuery } from '@tanstack/react-query';
import * as analyticsService from '@/services/analyticsService';

export function usePortfolioQuery(userId: string) {
  return useQuery({
    queryKey: ['portfolio', userId],
    queryFn: () => analyticsService.getPortfolioData(userId),
    staleTime: 1000 * 60 * 5, // 5 minutes
    enabled: !!userId, // Only run if userId exists
  });
}

// Usage in component
function PortfolioCard({ userId }: { userId: string }) {
  const { data, isLoading, error } = usePortfolioQuery(userId);

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return <PortfolioDisplay data={data} />;
}
```

### useSuspenseQuery Hook

```typescript
// src/hooks/queries/usePortfolioSuspenseQuery.ts
import { useSuspenseQuery } from '@tanstack/react-query';

export function usePortfolioSuspenseQuery(userId: string) {
  return useSuspenseQuery({
    queryKey: ['portfolio', userId],
    queryFn: () => analyticsService.getPortfolioData(userId),
  });
}

// Usage with Suspense boundary
function PortfolioPage() {
  return (
    <Suspense fallback={<PortfolioSkeleton />}>
      <PortfolioContent />
    </Suspense>
  );
}

function PortfolioContent() {
  // No loading state needed - Suspense handles it
  const { data } = usePortfolioSuspenseQuery(userId);
  return <PortfolioDisplay data={data} />;
}
```

## Mutations

### useMutation Hook

```typescript
// src/hooks/mutations/useExecuteZapIn.ts
import { useMutation, useQueryClient } from '@tanstack/react-query';
import * as intentService from '@/services/intentService';

export function useExecuteZapIn() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: intentService.executeZapIn,
    onSuccess: (data, variables) => {
      // Invalidate and refetch portfolio data
      queryClient.invalidateQueries({
        queryKey: ['portfolio', variables.userId]
      });

      // Invalidate pool performance
      queryClient.invalidateQueries({
        queryKey: ['pool-performance', variables.userId]
      });
    },
    onError: (error) => {
      console.error('ZapIn failed:', error);
    },
  });
}

// Usage in component
function ZapInButton({ userId, poolId }: Props) {
  const { mutate, isPending } = useExecuteZapIn();

  const handleZapIn = () => {
    mutate({
      userId,
      poolId,
      amount: '1000',
      slippage: 0.5,
    });
  };

  return (
    <button
      onClick={handleZapIn}
      disabled={isPending}
    >
      {isPending ? 'Processing...' : 'Zap In'}
    </button>
  );
}
```

### Optimistic Updates

```typescript
export function useOptimizePortfolio() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: intentService.executeOptimize,
    onMutate: async variables => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({
        queryKey: ["portfolio", variables.userId],
      });

      // Snapshot current value
      const previousPortfolio = queryClient.getQueryData(["portfolio", variables.userId]);

      // Optimistically update
      queryClient.setQueryData(["portfolio", variables.userId], (old: any) => ({
        ...old,
        optimizing: true,
      }));

      return { previousPortfolio };
    },
    onError: (err, variables, context) => {
      // Rollback on error
      queryClient.setQueryData(["portfolio", variables.userId], context?.previousPortfolio);
    },
    onSettled: (data, error, variables) => {
      // Refetch after success or error
      queryClient.invalidateQueries({
        queryKey: ["portfolio", variables.userId],
      });
    },
  });
}
```

## Query Keys

### Hierarchical Keys

```typescript
// Good: Structured query keys for easy invalidation
["portfolio", userId][("portfolio", userId, "apr")][("portfolio", userId, "pools")][ // All portfolio data // APR data // Pools data
  ("portfolio", userId, "pools", poolId)
]; // Specific pool

// Invalidate all portfolio data
queryClient.invalidateQueries({ queryKey: ["portfolio", userId] });

// Invalidate only APR data
queryClient.invalidateQueries({ queryKey: ["portfolio", userId, "apr"] });
```

### Query Key Factory

```typescript
// src/hooks/queries/queryKeys.ts
export const queryKeys = {
  portfolio: {
    all: ["portfolio"] as const,
    byUser: (userId: string) => [...queryKeys.portfolio.all, userId] as const,
    apr: (userId: string) => [...queryKeys.portfolio.byUser(userId), "apr"] as const,
    pools: (userId: string) => [...queryKeys.portfolio.byUser(userId), "pools"] as const,
    pool: (userId: string, poolId: string) =>
      [...queryKeys.portfolio.pools(userId), poolId] as const,
  },
  analytics: {
    all: ["analytics"] as const,
    poolPerformance: (userId: string) =>
      [...queryKeys.analytics.all, "pool-performance", userId] as const,
  },
};

// Usage
export function usePortfolioAPRQuery(userId: string) {
  return useQuery({
    queryKey: queryKeys.portfolio.apr(userId),
    queryFn: () => analyticsService.getPortfolioAPR(userId),
  });
}
```

## Dependent Queries

```typescript
function UserPortfolio({ userId }: { userId: string }) {
  // First query: Get user account
  const { data: account } = useQuery({
    queryKey: ['account', userId],
    queryFn: () => accountService.getAccount(userId),
  });

  // Second query: Depends on account data
  const { data: portfolio } = useQuery({
    queryKey: ['portfolio', account?.id],
    queryFn: () => analyticsService.getPortfolio(account!.id),
    enabled: !!account, // Only run when account exists
  });

  return <PortfolioDisplay portfolio={portfolio} />;
}
```

## Parallel Queries

```typescript
function PortfolioDashboard({ userId }: { userId: string }) {
  const portfolioQuery = usePortfolioQuery(userId);
  const aprQuery = usePortfolioAPRQuery(userId);
  const poolsQuery = usePoolPerformanceQuery(userId);

  // All queries run in parallel
  const isLoading = portfolioQuery.isLoading || aprQuery.isLoading || poolsQuery.isLoading;

  if (isLoading) return <LoadingSpinner />;

  return (
    <div>
      <PortfolioSummary data={portfolioQuery.data} />
      <APRMetrics data={aprQuery.data} />
      <PoolsList data={poolsQuery.data} />
    </div>
  );
}
```

## Infinite Queries

```typescript
export function useInfinitePoolsQuery(userId: string) {
  return useInfiniteQuery({
    queryKey: ['pools', userId, 'infinite'],
    queryFn: ({ pageParam = 0 }) =>
      analyticsService.getPools(userId, { page: pageParam, limit: 20 }),
    getNextPageParam: (lastPage, pages) =>
      lastPage.hasMore ? pages.length : undefined,
  });
}

// Usage
function InfinitePoolsList({ userId }: { userId: string }) {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfinitePoolsQuery(userId);

  return (
    <div>
      {data?.pages.map((page, i) => (
        <div key={i}>
          {page.pools.map(pool => (
            <PoolCard key={pool.id} pool={pool} />
          ))}
        </div>
      ))}
      <button
        onClick={() => fetchNextPage()}
        disabled={!hasNextPage || isFetchingNextPage}
      >
        {isFetchingNextPage
          ? 'Loading more...'
          : hasNextPage
          ? 'Load More'
          : 'No more pools'}
      </button>
    </div>
  );
}
```

## Polling and Refetching

```typescript
// Auto-refetch every 30 seconds
export function useRealtimePortfolioQuery(userId: string) {
  return useQuery({
    queryKey: ['portfolio', userId, 'realtime'],
    queryFn: () => analyticsService.getPortfolioData(userId),
    refetchInterval: 1000 * 30, // 30 seconds
    refetchIntervalInBackground: false,
  });
}

// Refetch on window focus
export function usePortfolioQuery(userId: string) {
  return useQuery({
    queryKey: ['portfolio', userId],
    queryFn: () => analyticsService.getPortfolioData(userId),
    refetchOnWindowFocus: true,
  });
}

// Manual refetch
function PortfolioCard({ userId }: { userId: string }) {
  const { data, refetch } = usePortfolioQuery(userId);

  return (
    <div>
      <PortfolioDisplay data={data} />
      <button onClick={() => refetch()}>Refresh</button>
    </div>
  );
}
```

## Error Handling

```typescript
export function usePortfolioQuery(userId: string) {
  return useQuery({
    queryKey: ['portfolio', userId],
    queryFn: () => analyticsService.getPortfolioData(userId),
    retry: (failureCount, error: any) => {
      // Don't retry on 404
      if (error?.status === 404) return false;

      // Retry up to 3 times for other errors
      return failureCount < 3;
    },
    onError: (error) => {
      console.error('Failed to fetch portfolio:', error);
      // You could also show a toast notification here
    },
  });
}

// Component-level error handling
function PortfolioCard({ userId }: { userId: string }) {
  const { data, error, isError } = usePortfolioQuery(userId);

  if (isError) {
    return (
      <ErrorMessage
        title="Failed to load portfolio"
        message={error.message}
        retry={() => queryClient.invalidateQueries({ queryKey: ['portfolio', userId] })}
      />
    );
  }

  return <PortfolioDisplay data={data} />;
}
```

## Caching Strategies

```typescript
// Long cache for static data
export function useTokenMetadataQuery(address: string) {
  return useQuery({
    queryKey: ["token", address],
    queryFn: () => tokenService.getMetadata(address),
    staleTime: Infinity, // Never becomes stale
    cacheTime: 1000 * 60 * 60 * 24, // 24 hours
  });
}

// Short cache for volatile data
export function useGasPriceQuery() {
  return useQuery({
    queryKey: ["gas-price"],
    queryFn: () => web3Service.getGasPrice(),
    staleTime: 1000 * 10, // 10 seconds
    refetchInterval: 1000 * 30, // Refetch every 30 seconds
  });
}

// No cache for one-time data
export function useTransactionStatusQuery(txHash: string) {
  return useQuery({
    queryKey: ["transaction", txHash],
    queryFn: () => web3Service.getTransactionStatus(txHash),
    staleTime: 0, // Always stale
    cacheTime: 0, // Don't cache
  });
}
```

## Prefetching

```typescript
// Prefetch on hover
function PoolLink({ poolId }: { poolId: string }) {
  const queryClient = useQueryClient();

  const prefetchPool = () => {
    queryClient.prefetchQuery({
      queryKey: ['pool', poolId],
      queryFn: () => poolService.getPoolDetails(poolId),
    });
  };

  return (
    <Link
      href={`/pool/${poolId}`}
      onMouseEnter={prefetchPool}
    >
      View Pool
    </Link>
  );
}
```

## Best Practices

1. **Query Keys**: Use structured, hierarchical query keys
2. **Stale Time**: Configure based on data volatility
3. **Error Handling**: Always handle errors gracefully
4. **Loading States**: Provide feedback during data fetching
5. **Mutations**: Invalidate related queries after mutations
6. **Optimistic Updates**: For better UX in write operations
7. **Suspense**: Use `useSuspenseQuery` with Suspense boundaries
8. **Devtools**: Enable React Query Devtools in development
