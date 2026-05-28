# Server Search Example

Production-ready API integration with Tanstack Query, debouncing, caching, error handling, and infinite scroll pagination.

## Features Demonstrated

- **Tanstack Query** integration for server-side search
- **Debouncing** to reduce API calls (300ms delay)
- **Loading states** with skeleton UI
- **Error handling** with retry functionality
- **Cache management** for instant results on repeat searches (5 min TTL)
- **Infinite scroll** pagination for seamless browsing
- **Result highlighting** to emphasize matching terms
- **Relevance scoring** for better search results
- **Minimum query length** validation (3 characters)

## Quick Start

### Installation

```bash
pnpm add @tanstack/react-query cmdk lucide-react
```

### Setup Tanstack Query

```tsx
// App.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <YourApp />
    </QueryClientProvider>
  );
}
```

### Basic Usage

```tsx
import { ServerSearchPalette } from './ServerSearchPalette';
import { useState } from 'react';

function MyApp() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button onClick={() => setIsOpen(true)}>Open Search</button>
      {isOpen && (
        <ServerSearchPalette
          onClose={() => setIsOpen(false)}
          onSelect={(item) => {
            console.log('Selected:', item);
            setIsOpen(false);
          }}
          placeholder="Search users, posts, products..."
          minQueryLength={3}
        />
      )}
    </>
  );
}
```

## Architecture

### Component Structure

```
ServerSearchPalette.tsx     Main palette component (modal variant)
├── ApiResult.tsx           Result item with highlighting
├── useApiSearch.ts         Tanstack Query hook with debouncing
└── mock-api.ts             Simulated API (replace with real API)
```

### Data Flow

```
User types → Debounce (300ms) → API call → Cache → Display results
                                    ↓
                              Infinite scroll → Load more
```

## Key Implementation Details

### Debounced Search

The `useDebounced` hook delays API calls until the user stops typing:

```typescript
function useDebounced<T>(value: T, delay: number = 300): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}
```

**Benefits:**
- Reduces API calls by ~90%
- Improves perceived performance
- Reduces server load

### Tanstack Query Integration

```typescript
export function useApiSearch(query: string, minLength: number = 3) {
  const debouncedQuery = useDebounced(query, 300);

  return useInfiniteQuery<SearchResponse, Error>({
    queryKey: ['api-search', debouncedQuery],
    queryFn: async ({ pageParam = 0 }) => {
      return await searchApi(debouncedQuery, pageParam as number);
    },
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    enabled: debouncedQuery.length >= minLength,
    staleTime: 5 * 60 * 1000, // Cache for 5 minutes
    retry: 2,
  });
}
```

**Features:**
- Automatic caching (5 min TTL)
- Request deduplication
- Retry with exponential backoff
- Infinite scroll support
- Loading/error states

### Infinite Scroll

Uses Intersection Observer API to detect when user scrolls to bottom:

```typescript
useEffect(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting && hasNextPage && !isFetchingNextPage) {
        fetchNextPage();
      }
    },
    { threshold: 0.1 }
  );

  if (observerTarget.current) {
    observer.observe(observerTarget.current);
  }

  return () => observer.disconnect();
}, [fetchNextPage, hasNextPage, isFetchingNextPage]);
```

### Error Handling

Comprehensive error handling with user-friendly retry:

```tsx
{isError && (
  <Command.Empty>
    <div className="space-y-3">
      <p className="text-sm text-red-600">
        {error?.message || 'Search failed'}
      </p>
      <button onClick={() => refetch()}>Retry</button>
    </div>
  </Command.Empty>
)}
```

**Error scenarios covered:**
- Network failures (with retry)
- Server errors (5xx)
- Timeouts
- Invalid responses

### Result Highlighting

Highlights matching terms in title and description:

```tsx
function HighlightedText({ text, query }: { text: string; query: string }) {
  const terms = query.trim().split(/\s+/);
  const regex = new RegExp(`(${terms.join('|')})`, 'gi');
  const parts = text.split(regex);

  return (
    <>
      {parts.map((part, i) =>
        isMatch(part, terms) ? (
          <mark key={i} className="bg-yellow-200">{part}</mark>
        ) : (
          <span key={i}>{part}</span>
        )
      )}
    </>
  );
}
```

## Mock API

The example includes a simulated API with 1000 mock items:

**Features:**
- Realistic network delays (200-500ms)
- Random errors (5% chance)
- Fuzzy search with relevance scoring
- Pagination (20 items per page)
- Multiple content types (users, posts, products)

**Replace with your API:**

```typescript
// Replace searchApi function in mock-api.ts
export async function searchApi(
  query: string,
  page: number = 0
): Promise<SearchResponse> {
  const response = await fetch(
    `/api/search?q=${encodeURIComponent(query)}&page=${page}`
  );

  if (!response.ok) {
    throw new Error('Search failed');
  }

  return response.json();
}
```

## Cache Management

Tanstack Query provides automatic cache management:

```typescript
queryClient: new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,    // Fresh for 5 minutes
      gcTime: 10 * 60 * 1000,       // Keep in memory for 10 minutes
      refetchOnWindowFocus: false,  // Don't refetch on focus
    },
  },
});
```

**Manual cache operations:**

```typescript
import { useQueryClient } from '@tanstack/react-query';

const queryClient = useQueryClient();

// Invalidate cache
queryClient.invalidateQueries({ queryKey: ['api-search'] });

// Clear cache
queryClient.removeQueries({ queryKey: ['api-search'] });

// Prefetch
queryClient.prefetchQuery({
  queryKey: ['api-search', 'react'],
  queryFn: () => searchApi('react', 0),
});
```

## Pagination Strategies

### Infinite Scroll (Recommended)

Best for discovery-focused search:

```typescript
const { fetchNextPage, hasNextPage, isFetchingNextPage } = useApiSearch(query);
```

**Pros:**
- Seamless browsing experience
- Natural on mobile
- Encourages exploration

**Cons:**
- Can't jump to specific page
- Harder to bookmark results

### Button Pagination (Alternative)

Better for precise navigation:

```typescript
const { page, nextPage, prevPage, setPage } = usePaginatedApiSearch(query);

return (
  <>
    <Results />
    <button onClick={prevPage} disabled={page === 0}>Previous</button>
    <span>Page {page + 1}</span>
    <button onClick={nextPage}>Next</button>
  </>
);
```

**Pros:**
- Precise page navigation
- Easier to bookmark
- Clear position in results

**Cons:**
- Requires extra UI
- More clicks required

## Performance Optimization

### Debounce Delay

Adjust based on your API latency:

```typescript
// Fast API (<100ms)
const debouncedQuery = useDebounced(query, 200);

// Normal API (100-300ms)
const debouncedQuery = useDebounced(query, 300);

// Slow API (>300ms)
const debouncedQuery = useDebounced(query, 500);
```

### Cache Duration

Balance freshness vs performance:

```typescript
staleTime: 1 * 60 * 1000,  // 1 min - Real-time data
staleTime: 5 * 60 * 1000,  // 5 min - Default (recommended)
staleTime: 30 * 60 * 1000, // 30 min - Rarely changing data
```

### Virtual Scrolling

For very large result sets (>1000 items), use virtual scrolling:

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

const virtualizer = useVirtualizer({
  count: allResults.length,
  getScrollElement: () => listRef.current,
  estimateSize: () => 64, // Height of each item
});
```

See `examples/virtual-list` for complete implementation.

## Testing

Unit tests for the search hook:

```typescript
// useApiSearch.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useApiSearch } from './useApiSearch';

describe('useApiSearch', () => {
  it('debounces search query', async () => {
    const { result, rerender } = renderHook(
      ({ query }) => useApiSearch(query),
      {
        wrapper: ({ children }) => (
          <QueryClientProvider client={new QueryClient()}>
            {children}
          </QueryClientProvider>
        ),
        initialProps: { query: '' },
      }
    );

    // Update query multiple times
    rerender({ query: 'r' });
    rerender({ query: 're' });
    rerender({ query: 'rea' });
    rerender({ query: 'react' });

    // Should only make one API call after debounce delay
    await waitFor(() => {
      expect(result.current.isFetching).toBe(true);
    });
  });

  it('requires minimum query length', () => {
    const { result } = renderHook(() => useApiSearch('ab'), {
      wrapper: createWrapper(),
    });

    expect(result.current.isFetching).toBe(false);
  });

  it('handles errors gracefully', async () => {
    // Mock API to throw error
    vi.mock('./mock-api', () => ({
      searchApi: vi.fn().mockRejectedValue(new Error('Network error')),
    }));

    const { result } = renderHook(() => useApiSearch('react'), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
      expect(result.current.error?.message).toBe('Network error');
    });
  });
});
```

See `useApiSearch.test.ts` for complete test suite.

## Usage Patterns

### User Search

```tsx
<ServerSearchPalette
  onSelect={(item) => {
    if (item.type === 'user') {
      navigate(`/users/${item.id}`);
    }
  }}
  placeholder="Search users..."
/>
```

### Product Catalog

```tsx
<ServerSearchPalette
  onSelect={(item) => {
    if (item.type === 'product') {
      addToCart(item.id);
    }
  }}
  placeholder="Search products..."
/>
```

### Document Library

```tsx
<ServerSearchPalette
  onSelect={(item) => {
    if (item.type === 'post') {
      openDocument(item.id);
    }
  }}
  placeholder="Search documents..."
/>
```

## Adapting for Your Use Case

### 1. Replace Mock API

Update `mock-api.ts` with your real API endpoint:

```typescript
export async function searchApi(
  query: string,
  page: number = 0
): Promise<SearchResponse> {
  const response = await fetch(`/api/search?q=${query}&page=${page}`);
  return response.json();
}
```

### 2. Customize Result Type

Update `SearchResultItem` interface:

```typescript
export interface SearchResultItem {
  id: string;
  type: string;
  title: string;
  // Add your custom fields
  customField1?: string;
  customField2?: number;
}
```

### 3. Adjust Styling

Customize Tailwind classes:

```tsx
// Change modal background
className="bg-white dark:bg-gray-900"

// Change result hover color
className="hover:bg-gray-50 dark:hover:bg-gray-800"
```

### 4. Add Authentication

Add auth headers to API calls:

```typescript
export async function searchApi(query: string, page: number) {
  const token = localStorage.getItem('auth_token');

  const response = await fetch(`/api/search?q=${query}&page=${page}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  return response.json();
}
```

## Related Examples

- **File Search** - Local search with fuzzy matching
- **Virtual List** - Handle 10,000+ results with virtual scrolling
- **Multi-Step** - Drill-down search with multiple levels

## See Also

- **Server-Side Search:** `references/server-side-search.md`
- **State Management:** `references/state-management.md`
- **Testing:** `references/testing.md`
