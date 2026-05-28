/**
 * Generate mock data for virtual list performance testing
 *
 * Creates realistic item data at scale (up to 100,000 items)
 * with minimal memory overhead and fast generation time.
 */

export interface MockItem {
  id: string;
  title: string;
  icon?: string;
  category: string;
  searchableText: string;
}

// Icon options for variety (using lucide-react icon names)
const ICONS = [
  'file-text',
  'folder',
  'code',
  'image',
  'video',
  'music',
  'database',
  'settings',
  'user',
  'mail',
  'calendar',
  'star',
  'heart',
  'bookmark',
  'tag',
] as const;

// Categories for grouping
const CATEGORIES = [
  'Documents',
  'Projects',
  'Media',
  'Settings',
  'Communication',
  'Development',
  'Personal',
  'Archive',
] as const;

// Title templates for realistic content
const TITLE_TEMPLATES = [
  (n: number) => `Document ${n}`,
  (n: number) => `Project Report ${n}`,
  (n: number) => `Meeting Notes ${n}`,
  (n: number) => `Design Mockup ${n}`,
  (n: number) => `Code Review ${n}`,
  (n: number) => `Feature Spec ${n}`,
  (n: number) => `Bug Report ${n}`,
  (n: number) => `User Story ${n}`,
  (n: number) => `API Documentation ${n}`,
  (n: number) => `Architecture Diagram ${n}`,
  (n: number) => `Test Plan ${n}`,
  (n: number) => `Release Notes ${n}`,
  (n: number) => `Product Roadmap ${n}`,
  (n: number) => `Sprint Planning ${n}`,
  (n: number) => `Status Update ${n}`,
];

/**
 * Generate mock items for testing
 *
 * Performance optimized:
 * - Pre-computed templates avoid repeated string operations
 * - Modulo arithmetic for cycling through options
 * - Direct array construction (no push in loop)
 *
 * @param count Number of items to generate (default: 100,000)
 * @returns Array of mock items
 *
 * @example
 * ```ts
 * // Generate 100k items
 * const items = generateMockItems(100_000);
 *
 * // Generate smaller test set
 * const testItems = generateMockItems(1000);
 * ```
 */
export function generateMockItems(count: number = 100_000): MockItem[] {
  const items: MockItem[] = new Array(count);

  const startTime = performance.now();

  for (let i = 0; i < count; i++) {
    // Cycle through templates for variety
    const templateIndex = i % TITLE_TEMPLATES.length;
    const title = TITLE_TEMPLATES[templateIndex](i + 1);

    // Assign category and icon
    const category = CATEGORIES[i % CATEGORIES.length];
    const icon = ICONS[i % ICONS.length];

    // Create searchable text (lowercase for case-insensitive search)
    const searchableText = `${title} ${category}`.toLowerCase();

    items[i] = {
      id: `item-${i}`,
      title,
      icon,
      category,
      searchableText,
    };
  }

  const endTime = performance.now();
  const duration = endTime - startTime;

  console.log(`Generated ${count.toLocaleString()} items in ${duration.toFixed(2)}ms`);

  return items;
}

/**
 * Filter items by search query
 *
 * Performance optimized for 100k items:
 * - Uses pre-computed searchableText field
 * - Simple includes() check (faster than regex for large datasets)
 * - Early termination possible with max results limit
 *
 * @param items Items to filter
 * @param query Search query (case-insensitive)
 * @param maxResults Maximum results to return (optional, for performance)
 * @returns Filtered items matching query
 *
 * @example
 * ```ts
 * const items = generateMockItems(100_000);
 * const results = filterItems(items, 'meeting', 100);
 * ```
 */
export function filterItems(
  items: MockItem[],
  query: string,
  maxResults?: number
): MockItem[] {
  if (!query.trim()) {
    return items;
  }

  const searchQuery = query.toLowerCase();
  const results: MockItem[] = [];

  for (let i = 0; i < items.length; i++) {
    if (items[i].searchableText.includes(searchQuery)) {
      results.push(items[i]);

      // Early termination if max results reached
      if (maxResults && results.length >= maxResults) {
        break;
      }
    }
  }

  return results;
}

/**
 * Get items by category
 *
 * @param items Items to filter
 * @param category Category to filter by
 * @returns Items in the specified category
 */
export function getItemsByCategory(
  items: MockItem[],
  category: string
): MockItem[] {
  return items.filter(item => item.category === category);
}

/**
 * Get category statistics
 *
 * @param items Items to analyze
 * @returns Object mapping category names to item counts
 */
export function getCategoryStats(items: MockItem[]): Record<string, number> {
  const stats: Record<string, number> = {};

  for (const item of items) {
    stats[item.category] = (stats[item.category] || 0) + 1;
  }

  return stats;
}
