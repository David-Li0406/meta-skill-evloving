import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useApiSearch, usePaginatedApiSearch } from './useApiSearch';
import * as mockApi from './mock-api';

/**
 * Test wrapper with Tanstack Query provider
 */
function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false, // Disable retries in tests
      },
    },
  });

  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

describe('useApiSearch', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('debouncing', () => {
    it('debounces search query (300ms)', async () => {
      vi.useFakeTimers();
      const searchSpy = vi.spyOn(mockApi, 'searchApi');

      const { rerender } = renderHook(
        ({ query }) => useApiSearch(query),
        {
          wrapper: createWrapper(),
          initialProps: { query: '' },
        }
      );

      // Rapidly update query
      rerender({ query: 'r' });
      vi.advanceTimersByTime(100);
      rerender({ query: 're' });
      vi.advanceTimersByTime(100);
      rerender({ query: 'rea' });
      vi.advanceTimersByTime(100);
      rerender({ query: 'react' });

      // Should not call API yet
      expect(searchSpy).not.toHaveBeenCalled();

      // Advance past debounce delay
      vi.advanceTimersByTime(300);

      await waitFor(() => {
        // Should only call API once with final query
        expect(searchSpy).toHaveBeenCalledTimes(1);
        expect(searchSpy).toHaveBeenCalledWith('react', 0);
      });

      vi.useRealTimers();
    });

    it('resets debounce timer on each keystroke', async () => {
      vi.useFakeTimers();
      const searchSpy = vi.spyOn(mockApi, 'searchApi');

      const { rerender } = renderHook(
        ({ query }) => useApiSearch(query),
        {
          wrapper: createWrapper(),
          initialProps: { query: '' },
        }
      );

      // Type "react" with 200ms between keystrokes
      rerender({ query: 'r' });
      vi.advanceTimersByTime(200);
      rerender({ query: 're' });
      vi.advanceTimersByTime(200);
      rerender({ query: 'rea' });
      vi.advanceTimersByTime(200);
      rerender({ query: 'react' });

      // Should not call API (debounce keeps resetting)
      expect(searchSpy).not.toHaveBeenCalled();

      // Advance past debounce delay
      vi.advanceTimersByTime(300);

      await waitFor(() => {
        expect(searchSpy).toHaveBeenCalledTimes(1);
      });

      vi.useRealTimers();
    });
  });

  describe('minimum query length', () => {
    it('does not search when query is too short', () => {
      const { result } = renderHook(() => useApiSearch('ab'), {
        wrapper: createWrapper(),
      });

      expect(result.current.isFetching).toBe(false);
      expect(result.current.data).toBeUndefined();
    });

    it('searches when query meets minimum length', async () => {
      const { result } = renderHook(() => useApiSearch('react'), {
        wrapper: createWrapper(),
      });

      await waitFor(() => {
        expect(result.current.isFetching).toBe(false);
        expect(result.current.data).toBeDefined();
      });
    });

    it('respects custom minimum length', () => {
      const { result } = renderHook(() => useApiSearch('ab', 2), {
        wrapper: createWrapper(),
      });

      // Should start fetching with 2-char query
      expect(result.current.isFetching).toBe(true);
    });
  });

  describe('caching', () => {
    it('caches results for 5 minutes', async () => {
      const searchSpy = vi.spyOn(mockApi, 'searchApi');

      const { result, rerender } = renderHook(
        ({ query }) => useApiSearch(query),
        {
          wrapper: createWrapper(),
          initialProps: { query: 'react' },
        }
      );

      await waitFor(() => {
        expect(result.current.data).toBeDefined();
      });

      expect(searchSpy).toHaveBeenCalledTimes(1);

      // Change query and back to 'react' (within cache TTL)
      rerender({ query: 'typescript' });
      await waitFor(() => {
        expect(result.current.data).toBeDefined();
      });

      rerender({ query: 'react' });

      // Should use cached result, no new API call
      expect(searchSpy).toHaveBeenCalledTimes(2); // Only for typescript
    });
  });

  describe('infinite scroll', () => {
    it('fetches next page when requested', async () => {
      const { result } = renderHook(() => useApiSearch('react'), {
        wrapper: createWrapper(),
      });

      await waitFor(() => {
        expect(result.current.data?.pages).toHaveLength(1);
      });

      // Fetch next page
      result.current.fetchNextPage();

      await waitFor(() => {
        expect(result.current.data?.pages).toHaveLength(2);
      });
    });

    it('indicates when more pages are available', async () => {
      const { result } = renderHook(() => useApiSearch('react'), {
        wrapper: createWrapper(),
      });

      await waitFor(() => {
        expect(result.current.hasNextPage).toBeDefined();
      });
    });

    it('sets isFetchingNextPage during pagination', async () => {
      const { result } = renderHook(() => useApiSearch('react'), {
        wrapper: createWrapper(),
      });

      await waitFor(() => {
        expect(result.current.data?.pages).toHaveLength(1);
      });

      result.current.fetchNextPage();

      // Should be fetching next page
      expect(result.current.isFetchingNextPage).toBe(true);

      await waitFor(() => {
        expect(result.current.isFetchingNextPage).toBe(false);
      });
    });
  });

  describe('error handling', () => {
    it('handles network errors', async () => {
      const searchSpy = vi
        .spyOn(mockApi, 'searchApi')
        .mockRejectedValueOnce(new Error('Network error'));

      const { result } = renderHook(() => useApiSearch('react'), {
        wrapper: createWrapper(),
      });

      await waitFor(() => {
        expect(result.current.isError).toBe(true);
        expect(result.current.error?.message).toBe('Network error');
      });

      searchSpy.mockRestore();
    });

    it('allows retry after error', async () => {
      let callCount = 0;
      const searchSpy = vi.spyOn(mockApi, 'searchApi').mockImplementation(() => {
        callCount++;
        if (callCount === 1) {
          return Promise.reject(new Error('Temporary error'));
        }
        return Promise.resolve({
          items: [],
          total: 0,
          page: 0,
          hasMore: false,
        });
      });

      const { result } = renderHook(() => useApiSearch('react'), {
        wrapper: createWrapper(),
      });

      await waitFor(() => {
        expect(result.current.isError).toBe(true);
      });

      // Retry
      result.current.refetch();

      await waitFor(() => {
        expect(result.current.isError).toBe(false);
        expect(result.current.data).toBeDefined();
      });

      searchSpy.mockRestore();
    });
  });

  describe('loading states', () => {
    it('sets isLoading during initial fetch', () => {
      const { result } = renderHook(() => useApiSearch('react'), {
        wrapper: createWrapper(),
      });

      expect(result.current.isLoading).toBe(true);
    });

    it('clears isLoading after fetch completes', async () => {
      const { result } = renderHook(() => useApiSearch('react'), {
        wrapper: createWrapper(),
      });

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });
    });
  });
});

describe('usePaginatedApiSearch', () => {
  it('starts at page 0', () => {
    const { result } = renderHook(() => usePaginatedApiSearch('react'), {
      wrapper: createWrapper(),
    });

    expect(result.current.page).toBe(0);
  });

  it('increments page on nextPage', async () => {
    const { result } = renderHook(() => usePaginatedApiSearch('react'), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.data).toBeDefined();
    });

    result.current.nextPage();
    expect(result.current.page).toBe(1);
  });

  it('decrements page on prevPage', async () => {
    const { result } = renderHook(() => usePaginatedApiSearch('react'), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.data).toBeDefined();
    });

    result.current.nextPage();
    result.current.nextPage();
    expect(result.current.page).toBe(2);

    result.current.prevPage();
    expect(result.current.page).toBe(1);
  });

  it('does not go below page 0', async () => {
    const { result } = renderHook(() => usePaginatedApiSearch('react'), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.data).toBeDefined();
    });

    result.current.prevPage();
    expect(result.current.page).toBe(0);
  });

  it('resets page when query changes', async () => {
    const { result, rerender } = renderHook(
      ({ query }) => usePaginatedApiSearch(query),
      {
        wrapper: createWrapper(),
        initialProps: { query: 'react' },
      }
    );

    await waitFor(() => {
      expect(result.current.data).toBeDefined();
    });

    result.current.nextPage();
    result.current.nextPage();
    expect(result.current.page).toBe(2);

    // Change query
    rerender({ query: 'typescript' });

    // Page should reset to 0
    await waitFor(() => {
      expect(result.current.page).toBe(0);
    });
  });
});
