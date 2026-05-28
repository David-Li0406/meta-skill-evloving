/**
 * Virtual List Command Palette Demo
 *
 * Performance demonstration with 100,000 items using Tanstack Virtual.
 * Maintains 60fps scrolling with smooth keyboard navigation.
 */

import { useState, useMemo, useCallback, useEffect } from 'react';
import { useVirtualList, useVirtualListMetrics } from './useVirtualList';
import { ListItem } from './ListItem';
import { generateMockItems, filterItems, type MockItem } from './generate-mock-data';

export interface VirtualListPaletteProps {
  /** Initial item count (default: 100,000) */
  initialItemCount?: number;

  /** Whether to show performance metrics (default: true) */
  showMetrics?: boolean;

  /** Callback when item is selected */
  onSelect?: (item: MockItem, index: number) => void;
}

/**
 * Virtual List Command Palette
 *
 * Demonstrates virtual scrolling performance with 100k items:
 * - Smooth 60fps scrolling
 * - Real-time search with debouncing
 * - Keyboard navigation (arrow keys, Enter)
 * - Performance metrics display
 * - Scroll to index functionality
 *
 * @example
 * ```tsx
 * <VirtualListPalette
 *   initialItemCount={100_000}
 *   showMetrics={true}
 *   onSelect={(item) => console.log('Selected:', item)}
 * />
 * ```
 */
export function VirtualListPalette({
  initialItemCount = 100_000,
  showMetrics = true,
  onSelect,
}: VirtualListPaletteProps) {
  // Generate mock data (memoized to prevent regeneration)
  const allItems = useMemo(
    () => generateMockItems(initialItemCount),
    [initialItemCount]
  );

  // Search state
  const [searchQuery, setSearchQuery] = useState('');
  const [debouncedQuery, setDebouncedQuery] = useState('');

  // Selection state
  const [selectedIndex, setSelectedIndex] = useState(0);

  // FPS tracking
  const [fps, setFps] = useState(60);

  // Debounce search query (150ms)
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(searchQuery);
    }, 150);

    return () => clearTimeout(timer);
  }, [searchQuery]);

  // Filter items based on search
  const filteredItems = useMemo(() => {
    return filterItems(allItems, debouncedQuery);
  }, [allItems, debouncedQuery]);

  // Virtual list setup
  const {
    parentRef,
    virtualizer,
    scrollToIndex,
    visibleRange,
    totalSize,
    virtualItems,
  } = useVirtualList({
    itemCount: filteredItems.length,
    itemHeight: 48, // Fixed height for performance
    overscan: 5,
    containerHeight: 600,
  });

  // Performance metrics
  const metrics = useVirtualListMetrics(virtualizer);

  // Track FPS
  useEffect(() => {
    let frameCount = 0;
    let lastTime = performance.now();
    let animationId: number;

    const trackFPS = () => {
      frameCount++;
      const currentTime = performance.now();

      if (currentTime >= lastTime + 1000) {
        setFps(Math.round((frameCount * 1000) / (currentTime - lastTime)));
        frameCount = 0;
        lastTime = currentTime;
      }

      animationId = requestAnimationFrame(trackFPS);
    };

    animationId = requestAnimationFrame(trackFPS);

    return () => cancelAnimationFrame(animationId);
  }, []);

  // Handle search change
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
    setSelectedIndex(0); // Reset selection on search
  };

  // Handle item selection
  const handleSelectItem = useCallback((item: MockItem, index: number) => {
    setSelectedIndex(index);
    onSelect?.(item, index);
  }, [onSelect]);

  // Keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => {
          const next = Math.min(prev + 1, filteredItems.length - 1);
          scrollToIndex(next, { align: 'center', behavior: 'smooth' });
          return next;
        });
        break;

      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => {
          const next = Math.max(prev - 1, 0);
          scrollToIndex(next, { align: 'center', behavior: 'smooth' });
          return next;
        });
        break;

      case 'Enter':
        e.preventDefault();
        if (filteredItems[selectedIndex]) {
          handleSelectItem(filteredItems[selectedIndex], selectedIndex);
        }
        break;

      case 'Home':
        e.preventDefault();
        setSelectedIndex(0);
        scrollToIndex(0, { align: 'start' });
        break;

      case 'End':
        e.preventDefault();
        const lastIndex = filteredItems.length - 1;
        setSelectedIndex(lastIndex);
        scrollToIndex(lastIndex, { align: 'end' });
        break;
    }
  };

  // Scroll to index controls
  const scrollToRandom = () => {
    const randomIndex = Math.floor(Math.random() * filteredItems.length);
    setSelectedIndex(randomIndex);
    scrollToIndex(randomIndex, { align: 'center' });
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-4">
      {/* Header */}
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-gray-900">
          Virtual List Performance Demo
        </h2>
        <p className="text-sm text-gray-600">
          Smoothly scroll through {allItems.length.toLocaleString()} items at 60fps using Tanstack Virtual
        </p>
      </div>

      {/* Performance Metrics */}
      {showMetrics && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 p-4 bg-gray-50 rounded-lg">
          <Metric label="Total Items" value={metrics.totalCount.toLocaleString()} />
          <Metric label="Rendered" value={metrics.renderedCount.toString()} />
          <Metric label="Memory Saved" value={metrics.memorySavedMB} />
          <Metric label="FPS" value={fps.toString()} color={fps >= 55 ? 'green' : fps >= 45 ? 'yellow' : 'red'} />
          <Metric label="Visible Range" value={`${visibleRange.start}-${visibleRange.end}`} />
        </div>
      )}

      {/* Search Input */}
      <div className="space-y-2">
        <input
          type="text"
          value={searchQuery}
          onChange={handleSearchChange}
          onKeyDown={handleKeyDown}
          placeholder="Search through 100,000 items..."
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          autoFocus
        />

        <div className="flex gap-2 text-xs text-gray-600">
          <span>↑↓ Navigate</span>
          <span>•</span>
          <span>Enter Select</span>
          <span>•</span>
          <span>Home/End Jump</span>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="flex gap-2">
        <button
          onClick={scrollToRandom}
          className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
        >
          Jump to Random
        </button>
        <button
          onClick={() => scrollToIndex(0, { align: 'start' })}
          className="px-3 py-1 text-sm bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
        >
          Jump to Start
        </button>
        <button
          onClick={() => scrollToIndex(filteredItems.length - 1, { align: 'end' })}
          className="px-3 py-1 text-sm bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors"
        >
          Jump to End
        </button>
      </div>

      {/* Virtual List */}
      <div className="border border-gray-200 rounded-lg overflow-hidden">
        <div
          ref={parentRef}
          className="h-[600px] overflow-auto"
          style={{ contain: 'strict' }} // CSS containment for better performance
        >
          <div
            style={{
              height: `${totalSize}px`,
              width: '100%',
              position: 'relative',
            }}
          >
            {virtualItems.map((virtualItem) => {
              const item = filteredItems[virtualItem.index];
              const isSelected = virtualItem.index === selectedIndex;

              return (
                <div
                  key={virtualItem.key}
                  data-index={virtualItem.index}
                  style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: `${virtualItem.size}px`,
                    transform: `translateY(${virtualItem.start}px)`,
                  }}
                >
                  <ListItem
                    item={item}
                    index={virtualItem.index}
                    isSelected={isSelected}
                    onClick={handleSelectItem}
                  />
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Results Info */}
      <div className="text-sm text-gray-600 text-center">
        {filteredItems.length === allItems.length ? (
          `Showing all ${filteredItems.length.toLocaleString()} items`
        ) : (
          `Found ${filteredItems.length.toLocaleString()} items matching "${debouncedQuery}"`
        )}
      </div>
    </div>
  );
}

/**
 * Metric display component
 */
function Metric({
  label,
  value,
  color = 'default'
}: {
  label: string;
  value: string;
  color?: 'default' | 'green' | 'yellow' | 'red';
}) {
  const colorClasses = {
    default: 'text-gray-900',
    green: 'text-green-600',
    yellow: 'text-yellow-600',
    red: 'text-red-600',
  };

  return (
    <div className="space-y-1">
      <div className="text-xs text-gray-500 uppercase tracking-wide">
        {label}
      </div>
      <div className={`text-lg font-bold ${colorClasses[color]}`}>
        {value}
      </div>
    </div>
  );
}
