# Server-Side Search with Tanstack Query

Implementing API-driven search with debouncing, caching, pagination, and infinite scroll.

## Why Tanstack Query

- **Caching:** Automatic request deduplication and caching
- **Background refetching:** Keep data fresh without blocking UI
- **Loading states:** Built-in loading, error, success states
- **Devtools:** Inspect cache and queries
- **Optimistic updates:** Update UI before server responds

## Basic Setup

```typescript
// App.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
      <ReactQueryDevtools />
    </QueryClientProvider>
  );
}
```

## Debounced Search Hook

```typescript
import { useQuery } from '@tanstack/react-query';
import { useState, useEffect } from 'react';

function useDebounced<T>(value: T, delay: number = 300): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

export function useServerSearch(query: string) {
  const debouncedQuery = useDebounced(query, 300);

  return useQuery({
    queryKey: ['search', debouncedQuery],
    queryFn: async () => {
      if (!debouncedQuery || debouncedQuery.length < 3) {
        return [];
      }

      const response = await fetch(
        `/api/search?q=${encodeURIComponent(debouncedQuery)}`
      );

      if (!response.ok) {
        throw new Error('Search failed');
      }

      return response.json();
    },
    enabled: debouncedQuery.length >= 3,
    staleTime: 5 * 60 * 1000,
    keepPreviousData: true, // Show old results while loading new ones
  });
}
```

## Usage in Palette

```typescript
function ServerSearchPalette() {
  const [query, setQuery] = useState('');
  const { data: results, isLoading, isError, error } = useServerSearch(query);

  return (
    <Command>
      <Command.Input
        value={query}
        onValueChange={setQuery}
        placeholder="Search..."
      />

      <Command.List>
        {isLoading && <Command.Loading>Searching...</Command.Loading>}

        {isError && (
          <div className="error">
            Error: {error?.message || 'Search failed'}
          </div>
        )}

        {results?.map((item) => (
          <Command.Item key={item.id} value={item.id}>
            {item.label}
          </Command.Item>
        ))}

        {results?.length === 0 && !isLoading && (
          <Command.Empty>No results found</Command.Empty>
        )}
      </Command.List>
    </Command>
  );
}
```

## Pagination

```typescript
export function usePaginatedSearch(query: string) {
  const debouncedQuery = useDebounced(query);
  const [page, setPage] = useState(1);

  const queryResult = useQuery({
    queryKey: ['search', debouncedQuery, page],
    queryFn: async () => {
      const response = await fetch(
        `/api/search?q=${encodeURIComponent(debouncedQuery)}&page=${page}`
      );
      return response.json();
    },
    enabled: debouncedQuery.length >= 3,
    keepPreviousData: true,
  });

  // Reset page when query changes
  useEffect(() => {
    setPage(1);
  }, [debouncedQuery]);

  return {
    ...queryResult,
    page,
    nextPage: () => setPage((p) => p + 1),
    prevPage: () => setPage((p) => Math.max(1, p - 1)),
    hasMore: queryResult.data?.hasMore || false,
  };
}

// Usage
function PaginatedResults() {
  const { data, nextPage, prevPage, hasMore, page } = usePaginatedSearch(query);

  return (
    <>
      {data?.results.map((item) => <ResultItem key={item.id} {...item} />)}
      <div className="pagination">
        <button onClick={prevPage} disabled={page === 1}>
          Previous
        </button>
        <span>Page {page}</span>
        <button onClick={nextPage} disabled={!hasMore}>
          Next
        </button>
      </div>
    </>
  );
}
```

## Infinite Scroll

```typescript
import { useInfiniteQuery } from '@tanstack/react-query';
import { useInView } from 'react-intersection-observer';

export function useInfiniteSearch(query: string) {
  const debouncedQuery = useDebounced(query);

  return useInfiniteQuery({
    queryKey: ['search-infinite', debouncedQuery],
    queryFn: async ({ pageParam = 0 }) => {
      const response = await fetch(
        `/api/search?q=${encodeURIComponent(debouncedQuery)}&cursor=${pageParam}`
      );
      return response.json();
    },
    getNextPageParam: (lastPage) => lastPage.nextCursor ?? undefined,
    enabled: debouncedQuery.length >= 3,
  });
}

// Usage
function InfiniteResults() {
  const { ref, inView } = useInView();
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
    useInfiniteSearch(query);

  // Fetch next page when bottom is in view
  useEffect(() => {
    if (inView && hasNextPage && !isFetchingNextPage) {
      fetchNextPage();
    }
  }, [inView, hasNextPage, isFetchingNextPage, fetchNextPage]);

  return (
    <div>
      {data?.pages.map((page) =>
        page.results.map((item) => <ResultItem key={item.id} {...item} />)
      )}
      <div ref={ref}>{isFetchingNextPage && 'Loading more...'}</div>
    </div>
  );
}
```

## Error Handling

```typescript
function SearchWithErrorHandling() {
  const { data, error, isError, refetch } = useServerSearch(query);

  if (isError) {
    return (
      <div className="error-state">
        <p>Search failed: {error?.message}</p>
        <button onClick={() => refetch()}>Retry</button>
      </div>
    );
  }

  return <Results data={data} />;
}
```

## Prefetching

```typescript
import { useQueryClient } from '@tanstack/react-query';

function useSearchPrefetch() {
  const queryClient = useQueryClient();

  function prefetchSearch(query: string) {
    if (query.length < 3) return;

    queryClient.prefetchQuery({
      queryKey: ['search', query],
      queryFn: async () => {
        const response = await fetch(`/api/search?q=${query}`);
        return response.json();
      },
    });
  }

  return { prefetchSearch };
}

// Usage: Prefetch on hover
<button onMouseEnter={() => prefetchSearch('react')}>
  Search React
</button>
```

## See Also

- **State Management:** `references/state-management.md`
- **Virtual Scrolling:** `references/virtual-scrolling.md`
- **Testing:** `references/testing.md`
