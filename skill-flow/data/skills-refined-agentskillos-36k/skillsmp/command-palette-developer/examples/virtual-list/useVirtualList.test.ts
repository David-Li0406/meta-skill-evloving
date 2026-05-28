/**
 * Unit tests for useVirtualList hook
 *
 * Tests virtual scrolling functionality, scroll to index,
 * visible range calculation, and performance metrics.
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useVirtualList, useVirtualListMetrics } from './useVirtualList';

describe('useVirtualList', () => {
  describe('initialization', () => {
    it('should initialize with correct configuration', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 100,
          itemHeight: 48,
          overscan: 5,
        })
      );

      expect(result.current.parentRef).toBeDefined();
      expect(result.current.virtualizer).toBeDefined();
      expect(result.current.scrollToIndex).toBeDefined();
      expect(result.current.totalSize).toBeGreaterThan(0);
    });

    it('should calculate total size correctly', () => {
      const itemCount = 1000;
      const itemHeight = 48;

      const { result } = renderHook(() =>
        useVirtualList({
          itemCount,
          itemHeight,
        })
      );

      // Total size should be itemCount * itemHeight
      expect(result.current.totalSize).toBe(itemCount * itemHeight);
    });

    it('should use default overscan value', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 100,
          itemHeight: 48,
        })
      );

      expect(result.current.virtualizer.options.overscan).toBe(5);
    });

    it('should use custom overscan value', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 100,
          itemHeight: 48,
          overscan: 10,
        })
      );

      expect(result.current.virtualizer.options.overscan).toBe(10);
    });
  });

  describe('visible range', () => {
    it('should return visible range with items', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 1000,
          itemHeight: 48,
        })
      );

      const { visibleRange } = result.current;

      expect(visibleRange.start).toBeGreaterThanOrEqual(0);
      expect(visibleRange.end).toBeGreaterThanOrEqual(visibleRange.start);
      expect(visibleRange.end).toBeLessThan(1000);
    });

    it('should return 0 range for empty list', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 0,
          itemHeight: 48,
        })
      );

      const { visibleRange } = result.current;

      expect(visibleRange.start).toBe(0);
      expect(visibleRange.end).toBe(0);
    });
  });

  describe('scrollToIndex', () => {
    it('should provide scrollToIndex function', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 100,
          itemHeight: 48,
        })
      );

      expect(typeof result.current.scrollToIndex).toBe('function');
    });

    it('should not throw when scrolling to valid index', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 100,
          itemHeight: 48,
        })
      );

      expect(() => {
        result.current.scrollToIndex(50);
      }).not.toThrow();
    });

    it('should accept alignment options', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 100,
          itemHeight: 48,
        })
      );

      expect(() => {
        result.current.scrollToIndex(50, { align: 'center' });
      }).not.toThrow();

      expect(() => {
        result.current.scrollToIndex(50, { align: 'start' });
      }).not.toThrow();

      expect(() => {
        result.current.scrollToIndex(50, { align: 'end' });
      }).not.toThrow();
    });

    it('should accept behavior options', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 100,
          itemHeight: 48,
        })
      );

      expect(() => {
        result.current.scrollToIndex(50, { behavior: 'smooth' });
      }).not.toThrow();

      expect(() => {
        result.current.scrollToIndex(50, { behavior: 'auto' });
      }).not.toThrow();
    });
  });

  describe('virtual items', () => {
    it('should return virtual items array', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 100,
          itemHeight: 48,
        })
      );

      expect(Array.isArray(result.current.virtualItems)).toBe(true);
    });

    it('should return empty array for zero items', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 0,
          itemHeight: 48,
        })
      );

      expect(result.current.virtualItems).toHaveLength(0);
    });

    it('should return limited items based on viewport', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 10000,
          itemHeight: 48,
          containerHeight: 600,
          overscan: 5,
        })
      );

      // Should render roughly viewport items + overscan
      // 600px viewport / 48px height = ~12 items + 5 overscan = ~17 items
      expect(result.current.virtualItems.length).toBeLessThan(50);
      expect(result.current.virtualItems.length).toBeGreaterThan(0);
    });
  });

  describe('large datasets', () => {
    it('should handle 100,000 items without crashing', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 100_000,
          itemHeight: 48,
        })
      );

      expect(result.current.totalSize).toBe(100_000 * 48);
      expect(result.current.virtualizer.options.count).toBe(100_000);
    });

    it('should maintain performance with large datasets', () => {
      const startTime = performance.now();

      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 100_000,
          itemHeight: 48,
        })
      );

      const endTime = performance.now();
      const renderTime = endTime - startTime;

      // Initialization should be fast (<100ms)
      expect(renderTime).toBeLessThan(100);
      expect(result.current.virtualItems.length).toBeLessThan(100);
    });
  });

  describe('edge cases', () => {
    it('should handle single item', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 1,
          itemHeight: 48,
        })
      );

      expect(result.current.totalSize).toBe(48);
      expect(result.current.visibleRange.start).toBe(0);
    });

    it('should handle zero height items', () => {
      const { result } = renderHook(() =>
        useVirtualList({
          itemCount: 100,
          itemHeight: 0,
        })
      );

      expect(result.current.totalSize).toBe(0);
    });

    it('should update when item count changes', () => {
      const { result, rerender } = renderHook(
        ({ itemCount }) =>
          useVirtualList({
            itemCount,
            itemHeight: 48,
          }),
        { initialProps: { itemCount: 100 } }
      );

      const initialSize = result.current.totalSize;

      // Update item count
      rerender({ itemCount: 200 });

      expect(result.current.totalSize).toBe(initialSize * 2);
    });
  });
});

describe('useVirtualListMetrics', () => {
  it('should calculate metrics correctly', () => {
    const { result: listResult } = renderHook(() =>
      useVirtualList({
        itemCount: 10000,
        itemHeight: 48,
        containerHeight: 600,
        overscan: 5,
      })
    );

    const { result: metricsResult } = renderHook(() =>
      useVirtualListMetrics(listResult.current.virtualizer)
    );

    const metrics = metricsResult.current;

    expect(metrics.totalCount).toBe(10000);
    expect(metrics.renderedCount).toBeGreaterThan(0);
    expect(metrics.renderedCount).toBeLessThan(100); // Should be small
    expect(typeof metrics.percentageRendered).toBe('string');
    expect(typeof metrics.memorySavedMB).toBe('string');
  });

  it('should calculate percentage rendered correctly', () => {
    const { result: listResult } = renderHook(() =>
      useVirtualList({
        itemCount: 100,
        itemHeight: 48,
        containerHeight: 480, // Exactly 10 items visible
        overscan: 0,
      })
    );

    const { result: metricsResult } = renderHook(() =>
      useVirtualListMetrics(listResult.current.virtualizer)
    );

    const metrics = metricsResult.current;

    // Should render small percentage of total
    const percentage = parseFloat(metrics.percentageRendered);
    expect(percentage).toBeLessThan(100);
    expect(percentage).toBeGreaterThan(0);
  });

  it('should handle empty list', () => {
    const { result: listResult } = renderHook(() =>
      useVirtualList({
        itemCount: 0,
        itemHeight: 48,
      })
    );

    const { result: metricsResult } = renderHook(() =>
      useVirtualListMetrics(listResult.current.virtualizer)
    );

    const metrics = metricsResult.current;

    expect(metrics.totalCount).toBe(0);
    expect(metrics.renderedCount).toBe(0);
    expect(metrics.percentageRendered).toBe('0%');
  });

  it('should show memory savings for large lists', () => {
    const { result: listResult } = renderHook(() =>
      useVirtualList({
        itemCount: 100_000,
        itemHeight: 48,
        containerHeight: 600,
        overscan: 5,
      })
    );

    const { result: metricsResult } = renderHook(() =>
      useVirtualListMetrics(listResult.current.virtualizer)
    );

    const metrics = metricsResult.current;

    // With 100k items and ~20 rendered, memory savings should be significant
    const memorySavedMB = parseFloat(metrics.memorySavedMB);
    expect(memorySavedMB).toBeGreaterThan(50); // At least 50MB saved
  });
});
