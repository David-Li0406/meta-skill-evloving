/**
 * Virtual List Performance Demo
 *
 * Barrel export for all virtual list components and utilities.
 */

export { VirtualListPalette } from './VirtualListPalette';
export type { VirtualListPaletteProps } from './VirtualListPalette';

export { ListItem, ListItemCompact } from './ListItem';
export type { ListItemProps } from './ListItem';

export { useVirtualList, useVirtualListMetrics } from './useVirtualList';
export type { VirtualListConfig, VirtualListReturn } from './useVirtualList';

export {
  generateMockItems,
  filterItems,
  getItemsByCategory,
  getCategoryStats,
} from './generate-mock-data';
export type { MockItem } from './generate-mock-data';
