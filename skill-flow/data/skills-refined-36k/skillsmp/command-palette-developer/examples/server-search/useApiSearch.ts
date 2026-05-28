import { useInfiniteQuery } from '@tanstack/react-query';
import { useState, useEffect } from 'react';
import { searchApi } from './mock-api';
import type { SearchResponse } from './mock-api';

/**
 * Debounce hook to delay value updates
 * @param value - Value to debounce
 * @param delay - Delay in milliseconds (default: 300ms)
 */
function useDebounced<T>(value: T, delay: number = 300): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(timer);
    };
  }, [value, delay]);

  return debouncedValue;
}

/**
 * API search hook with debouncing, caching, and infinite scroll
 * @param query - Search query string
 * @param minLength - Minimum query length before searching (default: 3)
 */
export function useApiSearch(query: string, minLength: number = 3) {
  const debouncedQuery = useDebounced(query, 300);

  const queryResult = useInfiniteQuery<SearchResponse, Error>({
    queryKey: ['api-search', debouncedQuery],
    queryFn: async ({ pageParam = 0 }) => {
      return await searchApi(debouncedQuery, pageParam as number);
    },
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    enabled: debouncedQuery.length >= minLength,
    staleTime: 5 * 60 * 1000, // Cache for 5 minutes
    gcTime: 10 * 60 * 1000, // Keep in cache for 10 minutes (formerly cacheTime)
    retry: 2, // Retry failed requests twice
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000), // Exponential backoff
  });

  return queryResult;
}

/**
 * Alternative: Paginated search (button-based navigation)
 * Use this instead of useApiSearch for button-based pagination
 */
export function usePaginatedApiSearch(query: string, minLength: number = 3) {
  const debouncedQuery = useDebounced(query, 300);
  const [page, setPage] = useState(0);

  // Reset page when query changes
  useEffect(() => {
    setPage(0);
  }, [debouncedQuery]);

  const queryResult = useInfiniteQuery<SearchResponse, Error>({
    queryKey: ['api-search-paginated', debouncedQuery, page],
    queryFn: async () => {
      return await searchApi(debouncedQuery, page);
    },
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    enabled: debouncedQuery.length >= minLength,
    staleTime: 5 * 60 * 1000,
    gcTime: 10 * 60 * 1000,
  });

  return {
    ...queryResult,
    page,
    nextPage: () => setPage((p) => p + 1),
    prevPage: () => setPage((p) => Math.max(0, p - 1)),
    setPage,
  };
}
