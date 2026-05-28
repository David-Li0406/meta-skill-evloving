import { useState, useEffect, useRef } from 'react';
import { Command } from 'cmdk';
import { Search, Loader2 } from 'lucide-react';
import { useApiSearch } from './useApiSearch';
import { ApiResult } from './ApiResult';
import type { SearchResultItem } from './mock-api';

export interface ServerSearchPaletteProps {
  onClose?: () => void;
  onSelect?: (item: SearchResultItem) => void;
  placeholder?: string;
  minQueryLength?: number;
}

export function ServerSearchPalette({
  onClose,
  onSelect,
  placeholder = 'Search...',
  minQueryLength = 3,
}: ServerSearchPaletteProps) {
  const [query, setQuery] = useState('');
  const listRef = useRef<HTMLDivElement>(null);
  const observerTarget = useRef<HTMLDivElement>(null);

  const {
    data,
    isLoading,
    isError,
    error,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    refetch,
  } = useApiSearch(query);

  // Infinite scroll: load more when scrolling to bottom
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasNextPage && !isFetchingNextPage) {
          fetchNextPage();
        }
      },
      { threshold: 0.1 }
    );

    const target = observerTarget.current;
    if (target) {
      observer.observe(target);
    }

    return () => {
      if (target) {
        observer.unobserve(target);
      }
    };
  }, [fetchNextPage, hasNextPage, isFetchingNextPage]);

  // Keyboard shortcuts
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') {
        onClose?.();
      }
    }

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  const handleSelect = (item: SearchResultItem) => {
    onSelect?.(item);
    onClose?.();
  };

  const allResults = data?.pages.flatMap((page) => page.items) ?? [];
  const totalResults = data?.pages[0]?.total ?? 0;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-[20vh] bg-black/50">
      <Command
        className="w-full max-w-2xl bg-white dark:bg-gray-900 rounded-lg shadow-2xl overflow-hidden"
        shouldFilter={false}
      >
        <div className="flex items-center border-b border-gray-200 dark:border-gray-700 px-4">
          <Search className="w-5 h-5 text-gray-400" />
          <Command.Input
            value={query}
            onValueChange={setQuery}
            placeholder={placeholder}
            className="flex-1 px-3 py-4 text-base bg-transparent outline-none placeholder:text-gray-400"
          />
          {isLoading && (
            <Loader2 className="w-5 h-5 text-gray-400 animate-spin" />
          )}
        </div>

        <Command.List
          ref={listRef}
          className="max-h-[400px] overflow-y-auto overscroll-contain"
        >
          {/* Query too short */}
          {query.length > 0 && query.length < minQueryLength && (
            <div className="px-4 py-8 text-center text-sm text-gray-500">
              Type at least {minQueryLength} characters to search
            </div>
          )}

          {/* Loading skeleton */}
          {isLoading && query.length >= minQueryLength && (
            <Command.Loading className="px-4 py-2">
              <div className="space-y-2">
                {Array.from({ length: 5 }).map((_, i) => (
                  <div
                    key={i}
                    className="h-16 bg-gray-100 dark:bg-gray-800 rounded animate-pulse"
                  />
                ))}
              </div>
            </Command.Loading>
          )}

          {/* Error state */}
          {isError && (
            <Command.Empty className="px-4 py-8 text-center">
              <div className="space-y-3">
                <p className="text-sm text-red-600 dark:text-red-400">
                  {error?.message || 'Search failed'}
                </p>
                <button
                  onClick={() => refetch()}
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md transition-colors"
                >
                  Retry
                </button>
              </div>
            </Command.Empty>
          )}

          {/* Empty state */}
          {!isLoading &&
            !isError &&
            query.length >= minQueryLength &&
            allResults.length === 0 && (
              <Command.Empty className="px-4 py-8 text-center text-sm text-gray-500">
                No results found for "{query}"
              </Command.Empty>
            )}

          {/* Results */}
          {!isError && allResults.length > 0 && (
            <Command.Group>
              {/* Results header */}
              <div className="px-4 py-2 text-xs font-medium text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800">
                {totalResults.toLocaleString()} result
                {totalResults !== 1 ? 's' : ''}
              </div>

              {allResults.map((item) => (
                <Command.Item
                  key={item.id}
                  value={item.id}
                  onSelect={() => handleSelect(item)}
                  className="cursor-pointer"
                >
                  <ApiResult item={item} query={query} />
                </Command.Item>
              ))}

              {/* Infinite scroll trigger */}
              <div ref={observerTarget} className="h-4" />

              {/* Loading more indicator */}
              {isFetchingNextPage && (
                <div className="px-4 py-3 text-center text-sm text-gray-500">
                  <Loader2 className="w-4 h-4 inline animate-spin mr-2" />
                  Loading more...
                </div>
              )}

              {/* End of results */}
              {!hasNextPage && allResults.length > 0 && (
                <div className="px-4 py-3 text-center text-xs text-gray-400">
                  End of results
                </div>
              )}
            </Command.Group>
          )}
        </Command.List>
      </Command>
    </div>
  );
}
