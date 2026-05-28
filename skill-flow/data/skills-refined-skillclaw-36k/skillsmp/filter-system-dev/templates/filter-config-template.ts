/**
 * Filter Configuration Template
 *
 * Copy this template when adding a new filter to the system.
 * Replace ALL_CAPS placeholders with your filter's values.
 *
 * Add the resulting config to config/filters.ts in the FILTER_CONFIGURATIONS array.
 *
 * NOTE: This is a documentation template. When implementing, import actual types from:
 * - types/filters.ts (FilterState, FilterConfig, FilterDisplayState)
 * - types/url-filters.ts (URLFilterState, URLQueryParams, RouteSegments)
 */

// =============================================================================
// Type definitions (SIMPLIFIED for reference only)
// In actual code, import canonical types from:
// - types/filters.ts (FilterState, FilterConfig, FilterDisplayState)
// - types/url-filters.ts (URLFilterState, URLQueryParams, RouteSegments)
// These reference types may not include all fields (e.g., extraData, computed)
// =============================================================================

/** Filter state from URL parsing (simplified) */
interface URLFilterState {
  place: string;
  byDate: string;
  category: string;
  searchTerm?: string;
  distance?: string;
  lat?: string;
  lon?: string;
}

/** Query parameters from URL */
interface URLQueryParams {
  search?: string;
  distance?: string;
  lat?: string;
  lon?: string;
  from?: string;
  to?: string;
}

/** Route path segments */
interface RouteSegments {
  place: string;
  byDate?: string;
  category?: string;
}

/** Display state passed to filter config functions */
interface FilterDisplayState {
  filters: URLFilterState;
  queryParams: URLQueryParams;
  segments: RouteSegments;
}

// =============================================================================
// Template: Copy and modify this for your new filter
// =============================================================================

export const exampleFilterConfig = {
  /**
   * Unique identifier for this filter.
   * Use camelCase. Examples: 'price', 'accessibility', 'venueType'
   */
  key: "FILTER_KEY" as keyof URLFilterState,

  /**
   * Display name for the filter (used in UI).
   */
  displayName: "Filter Display Name",

  /**
   * Default value when filter is not specified.
   * This value will be OMITTED from canonical URLs.
   * Common defaults: 'all', 'tots', 0, false
   */
  defaultValue: "DEFAULT_VALUE",

  /**
   * Filter type for categorization.
   */
  type: "search" as const,

  /**
   * Conditional enablement logic.
   * Return true if filter should be available given current filter state.
   *
   * Examples:
   * - Always enabled: (_state) => true
   * - Requires location: (state) => Boolean(state.filters.lat && state.filters.lon)
   * - Mutually exclusive: (state) => !state.filters.otherFilter
   */
  isEnabled: (_state: FilterDisplayState): boolean => true,

  /**
   * Human-readable display text for the filter value.
   * Used in UI pills, labels, and aria-labels.
   * Should be in Catalan for this project.
   *
   * Example for price filter:
   * getDisplayText: (state) => {
   *   const labels: Record<string, string> = {
   *     all: 'Tots els preus',
   *     free: 'Gratuït',
   *     paid: 'De pagament',
   *   };
   *   return labels[state.filters.price] || state.filters.price;
   * }
   */
  getDisplayText: (state: FilterDisplayState): string | undefined => {
    const labels: Record<string, string> = {
      DEFAULT_VALUE: "LABEL_FOR_DEFAULT",
      // Add more value → label mappings
    };
    const value = state.filters.YOUR_FILTER_KEY; // Replace YOUR_FILTER_KEY with your filter key
    return value ? labels[value] || value : undefined;
  },

  /**
   * Define what changes when this filter is removed.
   * Return an object with the filter keys to clear.
   *
   * IMPORTANT: If this filter has dependencies, remove them too!
   *
   * Examples:
   *
   * Simple filter:
   * getRemovalChanges: () => ({ FILTER_KEY: undefined })
   *
   * Filter with dependencies (e.g., distance requires lat/lon):
   * getRemovalChanges: () => ({
   *   distance: undefined,
   *   lat: undefined,
   *   lon: undefined,
   * })
   */
  getRemovalChanges: (): Partial<URLFilterState> => ({
    YOUR_FILTER_KEY: undefined, // Replace YOUR_FILTER_KEY with your filter key
  }),

  /**
   * OPTIONAL: List of other filters this filter depends on.
   * When those are removed, this filter should also be removed.
   *
   * Example:
   * dependencies: ['lat', 'lon']
   *
   * Remove this property if no dependencies.
   */
  dependencies: ["lat", "lon"] as Array<keyof URLFilterState>,

  /**
   * OPTIONAL: Special case logic for complex scenarios.
   *
   * Example: Redirect to home when specific filter combination
   * specialCases: {
   *   homeRedirect: (segments) =>
   *     segments.byDate === 'avui' &&
   *     segments.place === 'catalunya' &&
   *     segments.category === 'tots'
   * }
   *
   * Remove this property if no special cases.
   */
  specialCases: {
    homeRedirect: (_segments: RouteSegments): boolean => {
      // Your custom logic here
      return false;
    },
  },
};
