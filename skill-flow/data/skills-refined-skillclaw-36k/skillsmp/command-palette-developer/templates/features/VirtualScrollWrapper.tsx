/**
 * VirtualScrollWrapper - Wraps any command list with Tanstack Virtual for performance
 *
 * Features:
 * - Auto-calculates item heights
 * - Supports dynamic heights
 * - Overscan: 5 items before/after viewport
 * - Smooth scrolling
 * - Works with all layout types
 *
 * @example
 * ```tsx
 * <VirtualScrollWrapper
 *   items={commands}
 *   renderItem={(item, index) => <CommandItem key={item.id} {...item} />}
 *   estimatedHeight={48}
 *   containerHeight={400}
 * />
 * ```
 */

import { useVirtualizer } from '@tanstack/react-virtual';
import { useRef, type ReactNode } from 'react';

export interface VirtualScrollWrapperProps<T> {
  /** Array of items to render */
  items: T[];
  /** Render function for each item */
  renderItem: (item: T, index: number) => ReactNode;
  /** Estimated height of each item in pixels (default: 48) */
  estimatedHeight?: number;
  /** Container height in pixels (default: 400) */
  containerHeight?: number;
  /** Number of items to render outside viewport (default: 5) */
  overscan?: number;
  /** Optional className for container */
  className?: string;
  /** Enable dynamic height measurement */
  dynamicHeight?: boolean;
}

/**
 * VirtualScrollWrapper component
 *
 * Renders a virtualized list of items for optimal performance with large datasets.
 * Uses Tanstack Virtual to only render visible items plus overscan.
 */
export function VirtualScrollWrapper<T>({
  items,
  renderItem,
  estimatedHeight = 48,
  containerHeight = 400,
  overscan = 5,
  className = '',
  dynamicHeight = false,
}: VirtualScrollWrapperProps<T>): JSX.Element {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => estimatedHeight,
    overscan,
    ...(dynamicHeight && {
      measureElement:
        typeof window !== 'undefined' && 'ResizeObserver' in window
          ? (element) => element?.getBoundingClientRect().height ?? estimatedHeight
          : undefined,
    }),
  });

  const virtualItems = virtualizer.getVirtualItems();

  return (
    <div
      ref={parentRef}
      className={`virtual-scroll-container ${className}`.trim()}
      style={{
        height: `${containerHeight}px`,
        overflow: 'auto',
        contain: 'strict',
      }}
    >
      <div
        style={{
          height: `${virtualizer.getTotalSize()}px`,
          width: '100%',
          position: 'relative',
        }}
      >
        {virtualItems.map((virtualItem) => {
          const item = items[virtualItem.index];
          if (!item) return null;

          return (
            <div
              key={virtualItem.key}
              data-index={virtualItem.index}
              ref={dynamicHeight ? virtualizer.measureElement : undefined}
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                transform: `translateY(${virtualItem.start}px)`,
              }}
            >
              {renderItem(item, virtualItem.index)}
            </div>
          );
        })}
      </div>
    </div>
  );
}

/**
 * Hook for accessing virtualizer state
 *
 * @example
 * ```tsx
 * const { scrollToIndex, scrollToOffset } = useVirtualScrollState(virtualizerRef);
 * scrollToIndex(10, { align: 'center' });
 * ```
 */
export function useVirtualScrollState(parentRef: React.RefObject<HTMLDivElement>) {
  const scrollToIndex = (index: number, options?: { align?: 'start' | 'center' | 'end' }) => {
    const parent = parentRef.current;
    if (!parent) return;

    const itemHeight = 48; // This should match estimatedHeight
    const scrollOffset = index * itemHeight;
    parent.scrollTo({ top: scrollOffset, behavior: 'smooth' });
  };

  const scrollToOffset = (offset: number, behavior: ScrollBehavior = 'smooth') => {
    const parent = parentRef.current;
    if (!parent) return;
    parent.scrollTo({ top: offset, behavior });
  };

  return { scrollToIndex, scrollToOffset };
}
