/**
 * Custom hook for virtual scrolling with Tanstack Virtual
 *
 * Wraps @tanstack/react-virtual with optimized configuration
 * for large lists (100k+ items) with fixed item heights.
 */

import { useVirtualizer } from '@tanstack/react-virtual';
import { useRef, useMemo, type RefObject } from 'react';

export interface VirtualListConfig {
  /** Total number of items in the list */
  itemCount: number;

  /** Fixed height of each item in pixels */
  itemHeight: number;

  /** Number of items to render outside the visible viewport (default: 5) */
  overscan?: number;

  /** Container height in pixels (default: 600) */
  containerHeight?: number;
}

export interface VirtualListReturn<T extends HTMLElement = HTMLDivElement> {
  /** Ref to attach to the scrollable container */
  parentRef: RefObject<T>;

  /** Virtualizer instance from Tanstack Virtual */
  virtualizer: ReturnType<typeof useVirtualizer>;

  /** Scroll to a specific index */
  scrollToIndex: (index: number, options?: { align?: 'start' | 'center' | 'end'; behavior?: ScrollBehavior }) => void;

  /** Get the currently visible range */
  visibleRange: { start: number; end: number };

  /** Total size of the virtual list */
  totalSize: number;

  /** Currently rendered virtual items */
  virtualItems: ReturnType<typeof useVirtualizer>['getVirtualItems'];
}

/**
 * Hook for virtual scrolling with fixed-height items
 *
 * Optimized for 100,000+ items with smooth 60fps scrolling.
 * Uses fixed item heights for maximum performance.
 *
 * @param config Virtual list configuration
 * @returns Virtual list utilities and state
 *
 * @example
 * ```tsx
 * function MyList({ items }: { items: Item[] }) {
 *   const {
 *     parentRef,
 *     virtualizer,
 *     scrollToIndex,
 *     visibleRange
 *   } = useVirtualList({
 *     itemCount: items.length,
 *     itemHeight: 48,
 *     overscan: 5,
 *   });
 *
 *   return (
 *     <div ref={parentRef} style={{ height: 600, overflow: 'auto' }}>
 *       <div style={{ height: virtualizer.getTotalSize() }}>
 *         {virtualizer.getVirtualItems().map((virtualItem) => (
 *           <div
 *             key={virtualItem.key}
 *             style={{
 *               height: virtualItem.size,
 *               transform: `translateY(${virtualItem.start}px)`,
 *             }}
 *           >
 *             {items[virtualItem.index].title}
 *           </div>
 *         ))}
 *       </div>
 *     </div>
 *   );
 * }
 * ```
 */
export function useVirtualList<T extends HTMLElement = HTMLDivElement>(
  config: VirtualListConfig
): VirtualListReturn<T> {
  const {
    itemCount,
    itemHeight,
    overscan = 5,
    containerHeight = 600,
  } = config;

  // Ref for the scrollable parent element
  const parentRef = useRef<T>(null);

  // Create virtualizer with optimized settings
  const virtualizer = useVirtualizer({
    count: itemCount,
    getScrollElement: () => parentRef.current,
    estimateSize: () => itemHeight, // Fixed size for performance
    overscan, // Number of items to render outside viewport

    // Performance optimizations
    measureElement: undefined, // Disable measurement (we use fixed heights)

    // Smooth scrolling configuration
    scrollPaddingStart: 0,
    scrollPaddingEnd: 0,
  });

  // Scroll to specific index
  const scrollToIndex = (
    index: number,
    options?: { align?: 'start' | 'center' | 'end'; behavior?: ScrollBehavior }
  ) => {
    virtualizer.scrollToIndex(index, {
      align: options?.align ?? 'start',
      behavior: options?.behavior ?? 'smooth',
    });
  };

  // Calculate visible range
  const visibleRange = useMemo(() => {
    const items = virtualizer.getVirtualItems();
    if (items.length === 0) {
      return { start: 0, end: 0 };
    }

    return {
      start: items[0].index,
      end: items[items.length - 1].index,
    };
  }, [virtualizer.getVirtualItems()]);

  // Total size of the scrollable area
  const totalSize = virtualizer.getTotalSize();

  // Virtual items to render
  const virtualItems = virtualizer.getVirtualItems();

  return {
    parentRef,
    virtualizer,
    scrollToIndex,
    visibleRange,
    totalSize,
    virtualItems,
  };
}

/**
 * Hook for tracking scroll performance metrics
 *
 * Useful for debugging and performance monitoring.
 *
 * @param virtualizer Virtualizer instance
 * @returns Performance metrics
 *
 * @example
 * ```tsx
 * const { parentRef, virtualizer } = useVirtualList(config);
 * const metrics = useVirtualListMetrics(virtualizer);
 *
 * return (
 *   <div>
 *     <div>FPS: {metrics.fps}</div>
 *     <div>Rendered: {metrics.renderedCount} / {metrics.totalCount}</div>
 *   </div>
 * );
 * ```
 */
export function useVirtualListMetrics(
  virtualizer: ReturnType<typeof useVirtualizer>
) {
  const virtualItems = virtualizer.getVirtualItems();
  const totalCount = virtualizer.options.count;
  const renderedCount = virtualItems.length;

  // Calculate percentage rendered
  const percentageRendered = totalCount > 0
    ? ((renderedCount / totalCount) * 100).toFixed(2)
    : '0';

  // Memory saved estimation (rough calculation)
  // Assumes ~1KB per DOM node
  const memorySavedKB = Math.max(0, totalCount - renderedCount);
  const memorySavedMB = (memorySavedKB / 1024).toFixed(2);

  return {
    totalCount,
    renderedCount,
    percentageRendered: `${percentageRendered}%`,
    memorySavedMB: `${memorySavedMB} MB`,
  };
}
