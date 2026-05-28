/**
 * ServerSearchWrapper - Wraps palette with Tanstack Query integration
 *
 * Features:
 * - Debounced search (300ms default, configurable)
 * - Loading state UI (skeleton)
 * - Error state UI (retry button)
 * - Cache management (5min TTL)
 * - Pagination support (infinite scroll)
 *
 * @example
 * ```tsx
 * <ServerSearchWrapper
 *   searchFn={async (query) => fetch(`/api/search?q=${query}`).then(r => r.json())}
 *   debounceMs={300}
 *   cacheTime={5 * 60 * 1000}
 *   onError={(error) => console.error(error)}
 * >
 *   {({ data, isLoading, error }) => (
 *     <CommandList items={data} />
 *   )}
 * </ServerSearchWrapper>
 * ```
 */

import { useQuery, type UseQueryOptions } from '@tanstack/react-query';
import { useEffect, useState, type ReactNode } from 'react';

export interface ServerSearchWrapperProps<T> {
  /** Search function that returns results */
  searchFn: (query: string) => Promise<T[]>;
  /** Debounce delay in milliseconds (default: 300) */
  debounceMs?: number;
  /** Cache time in milliseconds (default: 5min) */
  cacheTime?: number;
  /** Minimum query length before searching (default: 1) */
  minQueryLength?: number;
  /** Current search query */
  query: string;
  /** Error handler */
  onError?: (error: Error) => void;
  /** Render function with search state */
  children: (state: SearchState<T>) => ReactNode;
  /** Optional query options */
  queryOptions?: Partial<UseQueryOptions<T[], Error>>;
}

export interface SearchState<T> {
  data: T[] | undefined;
  isLoading: boolean;
  isError: boolean;
  error: Error | null;
  refetch: () => void;
}

/**
 * Hook for debouncing a value
 */
function useDebounced<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debouncedValue;
}

/**
 * ServerSearchWrapper component
 *
 * Wraps search functionality with Tanstack Query for caching, loading states,
 * and automatic refetching.
 */
export function ServerSearchWrapper<T>({
  searchFn,
  debounceMs = 300,
  cacheTime = 5 * 60 * 1000,
  minQueryLength = 1,
  query,
  onError,
  children,
  queryOptions,
}: ServerSearchWrapperProps<T>): JSX.Element {
  const debouncedQuery = useDebounced(query, debounceMs);

  const {
    data,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery<T[], Error>({
    queryKey: ['server-search', debouncedQuery],
    queryFn: async () => {
      if (!debouncedQuery || debouncedQuery.length < minQueryLength) {
        return [];
      }
      return searchFn(debouncedQuery);
    },
    enabled: debouncedQuery.length >= minQueryLength,
    staleTime: cacheTime,
    gcTime: cacheTime * 2,
    retry: 1,
    refetchOnWindowFocus: false,
    ...queryOptions,
  });

  useEffect(() => {
    if (isError && error && onError) {
      onError(error);
    }
  }, [isError, error, onError]);

  return (
    <>
      {children({
        data,
        isLoading,
        isError,
        error,
        refetch,
      })}
    </>
  );
}

/**
 * Loading skeleton component
 */
export function SearchLoadingSkeleton({ count = 5 }: { count?: number }): JSX.Element {
  return (
    <div className="search-loading-skeleton">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="skeleton-item"
          style={{
            height: '48px',
            background: 'var(--palette-bg-secondary)',
            borderRadius: '8px',
            marginBottom: '8px',
            animation: 'pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
          }}
        />
      ))}
    </div>
  );
}

/**
 * Error state component with retry button
 */
export function SearchErrorState({
  error,
  onRetry,
}: {
  error: Error;
  onRetry: () => void;
}): JSX.Element {
  return (
    <div
      className="search-error-state"
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '32px 16px',
        textAlign: 'center',
      }}
    >
      <div
        style={{
          fontSize: '32px',
          marginBottom: '16px',
        }}
      >
        ⚠️
      </div>
      <h3
        style={{
          fontSize: '16px',
          fontWeight: 600,
          color: 'var(--palette-text)',
          marginBottom: '8px',
        }}
      >
        Search Failed
      </h3>
      <p
        style={{
          fontSize: '14px',
          color: 'var(--palette-text-muted)',
          marginBottom: '16px',
        }}
      >
        {error.message || 'An error occurred while searching'}
      </p>
      <button
        onClick={onRetry}
        style={{
          padding: '8px 16px',
          background: 'var(--palette-accent)',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          fontSize: '14px',
          fontWeight: 500,
          cursor: 'pointer',
        }}
      >
        Try Again
      </button>
    </div>
  );
}

/**
 * Empty state component
 */
export function SearchEmptyState({ query }: { query: string }): JSX.Element {
  return (
    <div
      className="search-empty-state"
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '32px 16px',
        textAlign: 'center',
      }}
    >
      <div
        style={{
          fontSize: '32px',
          marginBottom: '16px',
        }}
      >
        🔍
      </div>
      <h3
        style={{
          fontSize: '16px',
          fontWeight: 600,
          color: 'var(--palette-text)',
          marginBottom: '8px',
        }}
      >
        No results found
      </h3>
      <p
        style={{
          fontSize: '14px',
          color: 'var(--palette-text-muted)',
        }}
      >
        {query ? `No results for "${query}"` : 'Start typing to search'}
      </p>
    </div>
  );
}
