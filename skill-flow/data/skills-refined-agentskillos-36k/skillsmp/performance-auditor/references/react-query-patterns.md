# React Query Optimization Patterns

Strategies for optimal caching, stale times, and query management.

## Table of Contents
1. [Cache Configuration](#cache-configuration)
2. [Query-Specific Optimization](#query-specific-optimization)
3. [Performance Monitoring](#performance-monitoring)
4. [Anti-Patterns](#anti-patterns)

## Cache Configuration

Recommended React Query default configuration:

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,       // 5 minutes
      gcTime: 10 * 60 * 1000,         // 10 minutes (formerly cacheTime)
      retry: 1,
      refetchOnWindowFocus: false,
      refetchOnMount: false,
    },
  },
});
```

## Query-Specific Optimization

Different data types need different cache strategies:

### Static Bible Content (Long Cache)
```typescript
// Bible verses - rarely change
const { data: verses } = useQuery({
  queryKey: ['chapter', book, chapter, version],
  queryFn: () => fetchChapter(book, chapter, version),
  staleTime: 30 * 60 * 1000,      // 30 minutes
  gcTime: 60 * 60 * 1000,         // 1 hour
});
```

### User Data (Short Cache)
```typescript
// User bookmarks - may change frequently
const { data: bookmarks } = useQuery({
  queryKey: ['bookmarks', userId],
  queryFn: () => fetchBookmarks(userId),
  staleTime: 1 * 60 * 1000,       // 1 minute
  gcTime: 5 * 60 * 1000,          // 5 minutes
});
```

### AI Results (Aggressive Cache)
```typescript
// AI translations - expensive, never change
const { data: translation } = useQuery({
  queryKey: ['translation', term],
  queryFn: () => translateTerm(term),
  staleTime: Infinity,             // Never goes stale
  gcTime: 24 * 60 * 60 * 1000,    // 24 hours
});
```

## Performance Monitoring

Monitor React Query cache statistics:

```typescript
import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';

export const usePerformanceMonitor = () => {
  const queryClient = useQueryClient();

  useEffect(() => {
    // Log cache statistics
    const cache = queryClient.getQueryCache();
    const queries = cache.getAll();

    console.log('React Query Cache Stats:', {
      totalQueries: queries.length,
      activeQueries: queries.filter(q => q.state.fetchStatus === 'fetching').length,
      staleQueries: queries.filter(q => q.isStale()).length,
      cacheSize: JSON.stringify(queries).length / 1024 + ' KB'
    });

    // Monitor slow queries
    queries.forEach(query => {
      if (query.state.dataUpdateCount > 0) {
        const lastFetchTime = query.state.dataUpdatedAt - (query.state.dataUpdatedAt - 1000);
        if (lastFetchTime > 1000) {
          console.warn('Slow query detected:', {
            queryKey: query.queryKey,
            fetchTime: lastFetchTime + 'ms'
          });
        }
      }
    });
  }, [queryClient]);
};

// Usage in main component
import { usePerformanceMonitor } from '@/hooks/usePerformanceMonitor';

function App() {
  usePerformanceMonitor(); // Monitor in dev mode
  return <></>;
}
```

## Anti-Patterns

### ❌ Unnecessary Refetching
```typescript
// Bad: Query refetches on every mount
const { data } = useQuery({
  queryKey: ['data'],
  queryFn: fetchData,
  refetchOnMount: true,  // Forces refetch every time component mounts
});
```

**Better:**
```typescript
const { data } = useQuery({
  queryKey: ['data'],
  queryFn: fetchData,
  staleTime: 5 * 60 * 1000,    // Stay fresh for 5 minutes
  refetchOnMount: false,       // Don't refetch on mount
});
```

### ❌ Overly Aggressive Staleness
```typescript
// Bad: Cache never gets used
const { data } = useQuery({
  queryKey: ['expensive-api'],
  queryFn: expensiveCall,
  staleTime: 0,  // Always stale, always refetches
});
```

**Better:**
```typescript
const { data } = useQuery({
  queryKey: ['expensive-api'],
  queryFn: expensiveCall,
  staleTime: 10 * 60 * 1000,   // Cache for 10 minutes
  gcTime: 20 * 60 * 1000,      // Keep in memory for 20 minutes
});
```

### ❌ Forgetting to Invalidate on Mutation
```typescript
// Bad: Data gets stale after mutation
const { mutate } = useMutation(updateVerse);

const handleUpdate = () => {
  mutate({ id: 1, data: newData });
  // Data is now stale but React Query doesn't know
};
```

**Better:**
```typescript
const queryClient = useQueryClient();

const { mutate } = useMutation(
  updateVerse,
  {
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['verse', verseId] });
    }
  }
);
```

## Cache Size Management

Monitor cache size to prevent memory bloat:

```typescript
const cache = queryClient.getQueryCache();
const allQueries = cache.getAll();
const cacheSize = JSON.stringify(allQueries).length / 1024; // KB

if (cacheSize > 5000) {  // 5MB threshold
  console.warn('Cache growing too large:', cacheSize + 'MB');

  // Clear old, unused queries
  queryClient.removeQueries({
    queryKey: ['old-data'],
    type: 'inactive',
  });
}
```
