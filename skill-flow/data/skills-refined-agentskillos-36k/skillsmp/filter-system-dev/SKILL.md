---
name: filter-system-dev
description: Guide for working with the configuration-driven filter system. Use when adding/modifying filters, updating URL parsing, debugging filter-related issues, or working with config/filters.ts.
license: MIT
---

# Filter System Development Guide

This skill helps you navigate the **most complex domain logic** in this codebase: the configuration-driven URL-first filtering system for event discovery.

## When to Use This Skill

- Adding a new filter (e.g., price, accessibility, venue type)
- Modifying existing filter behavior (dependencies, special cases)
- Debugging URL parsing or canonicalization issues
- Understanding filter removal chains
- Working with `config/filters.ts` or `utils/filter-operations.ts`
- Implementing filter UI components

---

## Core Architecture

The filter system has **one canonical source of truth**: `config/filters.ts`

All filter logic flows through `FilterOperations` class which auto-integrates any filter added to the config.

### Key Files

- **`config/filters.ts`** - Single source of truth (ADD NEW FILTERS HERE)
- **`utils/filter-operations.ts`** - Auto-integration logic (DO NOT modify for new filters)
- **`utils/url-filters.ts`** - URL building (uses FilterOperations)
- **`utils/url-parsing.ts`** - URL parsing (uses FilterOperations)
- **`test/filter-system.test.ts`** - Validation tests

**IMPORTANT**: Do NOT create a `utils/filter-config.ts` file. All filter logic must go through `config/filters.ts`.

---

## Filter Configuration Anatomy

```typescript
{
  key: 'filterName',           // Unique identifier (camelCase)
  defaultValue: 'all',         // Default state (omitted from URL)
  isEnabled: (filters) => true, // Conditional enablement
  getDisplayText: (value) => getLabel(value), // Human-readable text
  getRemovalChanges: (value, segments, queryParams) => ({
    // What to change when filter is removed
    queryParams: { ...queryParams, filterName: undefined }
  }),
  dependencies: ['lat', 'lon'], // Optional: filters this depends on
  specialCases: {               // Optional: custom redirect logic
    shouldRedirectToHome: (filters) => ...
  }
}
```

---

## Step-by-Step: Adding a New Filter

### 1. Define Filter Configuration

Add to `config/filters.ts` in the `FILTER_CONFIGURATIONS` array:

```typescript
{
  key: 'price',
  defaultValue: 'all',
  isEnabled: (filters) => true,
  getDisplayText: (value) => {
    const labels = {
      all: 'Tots els preus',
      free: 'Gratuït',
      paid: 'De pagament',
    };
    return labels[value] || value;
  },
  getRemovalChanges: (value, segments, queryParams) => ({
    queryParams: { ...queryParams, price: undefined }
  }),
}
```

### 2. Auto-Integration (No Action Needed)

Once in `config/filters.ts`, `FilterOperations` automatically provides:

- `getAllConfigurations()` - includes your filter
- `getConfiguration('price')` - retrieves config
- `getRemovalUrl('price', ...)` - builds removal URL
- `isFilterActive('price', ...)` - checks active state
- `getDefaultValue('price')` - returns default

**No manual wiring needed in utils/filter-operations.ts!**

### 3. URL Strategy Decision

Choose where your filter lives in the URL:

#### Path Segment (e.g., `/barcelona/avui/musica`)

**Use when:**

- Core filtering dimensions (place, date, category)
- Important for SEO
- Limited set of values
- Omitted when default for canonical URLs

#### Query Parameter (e.g., `?search=jazz&distance=10`)

**Use when:**

- User input (search term, location)
- Optional filters (distance, accessibility)
- Many possible values
- Omitted when default to reduce URL bloat

**Decision tree for your filter:**

1. Is it core to SEO? → Path segment
2. Is it user-driven input? → Query param
3. Does it have limited values? → Path segment
4. Is it optional enhancement? → Query param

### 4. Implement Dependencies

If your filter depends on others:

```typescript
{
  key: 'distance',
  defaultValue: 50,
  dependencies: ['lat', 'lon'], // Distance requires location
  getRemovalChanges: (value, segments, queryParams) => ({
    queryParams: {
      ...queryParams,
      distance: undefined,
      lat: undefined,  // Remove dependencies too!
      lon: undefined,
    }
  }),
}
```

**Critical**: When removing a filter, always remove its dependencies to avoid invalid states.

### 5. Special Cases (If Needed)

For complex redirect logic:

```typescript
{
  key: 'category',
  // ...
  specialCases: {
    shouldRedirectToHome: (filters) =>
      filters.byDate &&
      filters.place === 'catalunya' &&
      filters.category === 'tots'
  }
}
```

This handles edge cases like "all categories in all of Catalunya by date" → redirect to home.

### 6. Run Validation Tests

```bash
yarn test test/filter-system.test.ts
```

If tests fail:

- Check that your `defaultValue` matches expected behavior
- Verify `getRemovalChanges` returns correct shape
- Update test expectations if you intentionally changed behavior

---

## Common Pitfalls

### ❌ Encoding Default Values in URLs

```typescript
// WRONG: Includes default 'all' in URL
const url = `/barcelona?price=all`;

// CORRECT: Omits default (canonical URL)
const url = `/barcelona`; // price defaults to 'all'
```

**Fix**: Use `buildCanonicalUrlDynamic` which auto-omits defaults based on `FILTER_CONFIGURATIONS`.

### ❌ Forgetting Dependent Filters

```typescript
// WRONG: Only removes distance
getRemovalChanges: (value, segments, queryParams) => ({
  queryParams: { ...queryParams, distance: undefined },
});

// CORRECT: Removes distance + dependencies
getRemovalChanges: (value, segments, queryParams) => ({
  queryParams: {
    ...queryParams,
    distance: undefined,
    lat: undefined, // Dependency
    lon: undefined, // Dependency
  },
});
```

**Why**: Leaving `lat/lon` without `distance` creates invalid state.

### ❌ Duplicating Logic in Multiple Files

**DO NOT** add filter-specific logic to:

- `utils/url-parsing.ts` (uses `FilterOperations.getAllConfigurations()`)
- `utils/url-filters.ts` (uses `FilterOperations.getConfiguration()`)
- Individual page components (import `FilterOperations`)

**Single source of truth**: `config/filters.ts` → everything else reads from it.

### ❌ Using Legacy Filter Patterns

```typescript
// WRONG: Creating separate filter config files
// Do NOT create files like: utils/filter-config.ts
export const PRICE_FILTER = { ... }

// CORRECT: Add to canonical config
// File: config/filters.ts
export const FILTER_CONFIGURATIONS = [
  { key: 'price', ... }
]
```

**Note**: Never create standalone filter config files. All filter configurations must go in `config/filters.ts`.

### ❌ Creating /tots/ URLs

```typescript
// WRONG: Includes 'tots' in canonical URL
const url = `/barcelona/tots/musica`;

// CORRECT: Omits 'tots' when it's a default
const url = `/barcelona/musica`; // date defaults to 'tots'
```

**SEO impact**: `/tots/` segments bloat URLs and dilute SEO value. Canonical URLs omit defaults.

---

## URL Canonicalization Rules

**Critical for SEO and avoiding $300 cost spikes** (see Section 12 in AGENTS.md):

1. **Default omission**:

   - `date === 'tots'` AND `category === 'tots'` → `/place`
   - `date === 'tots'` and `category !== 'tots'` → `/place/category`
   - `date !== 'tots'` and `category === 'tots'` → `/place/date`

2. **Query params**:

   - Only for: `search`, `distance`, `lat`, `lon`
   - Omit `distance` when default (50)

3. **Legacy redirects** (handled by middleware):
   - `?category=X&date=Y` → `/place/date/category` (301)
   - `/place/tots/category` → `/place/category` (301)

**NEVER read `searchParams` in `app/[place]/*` pages** - causes DynamoDB explosion (ISR caching per unique URL+query).

---

## Example: Adding a "Price" Filter

See [examples/add-price-filter-example.md](./examples/add-price-filter-example.md) for full walkthrough.

**Quick summary**:

1. Add config to `config/filters.ts`
2. Create UI component reading `FilterOperations.getConfiguration('price')`
3. Build URLs with `buildCanonicalUrlDynamic({ price: 'free' })`
4. Test with `yarn test test/filter-system.test.ts`

---

## Testing Your Filter

### Unit Tests

```bash
yarn test test/filter-system.test.ts
```

Validates:

- Filter configuration structure
- Default value handling
- Removal URL generation
- Active state detection

### E2E Tests

```bash
yarn test:e2e e2e/filters.flow.spec.ts
```

Validates:

- URL construction in real navigation
- Filter UI interactions
- Canonical URL redirects

### Manual Testing Checklist

- [ ] Filter defaults to correct value
- [ ] Removing filter returns to canonical URL
- [ ] Dependencies removed when filter removed
- [ ] URL omits default values
- [ ] No `/tots/` segments in canonical URLs
- [ ] Special cases trigger correct redirects

---

## Filter UI Patterns

### Reading Filter State

```typescript
import { FilterOperations } from "@utils/filter-operations";

const config = FilterOperations.getConfiguration("price");
const isActive = FilterOperations.isFilterActive("price", currentFilters);
const displayText = config.getDisplayText("free");
```

### Building Removal URL

```typescript
const removalUrl = FilterOperations.getRemovalUrl(
  "price",
  segments, // { place, date, category }
  queryParams // { search, distance, lat, lon }
);
```

### Checking if Filter Enabled

```typescript
const config = FilterOperations.getConfiguration("price");
const enabled = config.isEnabled(currentFilters);
```

---

## Integration with API Layer

Filters must be translated to API query params:

```typescript
// Client-side filter state
const filters = { price: "free", place: "barcelona" };

// API query building (uses buildEventsQuery from utils/api-helpers.ts)
const query = buildEventsQuery({
  place: filters.place,
  price: filters.price === "free" ? 0 : undefined, // API expects numeric
});
```

**Important**: Filter keys in UI may differ from API param names. Map them in `buildEventsQuery`.

---

## Resources

### Templates

- [filter-config-template.ts](./templates/filter-config-template.ts) - Boilerplate for new filters

### Examples

- [add-price-filter-example.md](./examples/add-price-filter-example.md) - Complete walkthrough

### Reference Files

- `config/filters.ts` - Canonical source of truth
- `utils/filter-operations.ts` - Auto-integration logic
- `utils/url-filters.ts` - URL building
- `test/filter-system.test.ts` - Test suite

---

## FAQ

**Q: Should my filter be a path segment or query param?**  
A: Path segment if core/SEO-important, query param if optional/user-input.

**Q: Do I need to modify `filter-operations.ts`?**  
A: No. Just add to `config/filters.ts` and everything auto-integrates.

**Q: What if my filter depends on another?**  
A: Add `dependencies: ['filterKey']` and include removals in `getRemovalChanges`.

**Q: How do I test my filter?**  
A: Run `yarn test test/filter-system.test.ts` for unit tests, `yarn test:e2e e2e/filters.flow.spec.ts` for E2E.

**Q: Why does URL building omit my filter?**  
A: It matches your `defaultValue`. This is correct for canonical URLs.

**Q: Can I override URL building for my filter?**  
A: No. Canonical URL building is centralized for SEO consistency. Special cases go in `specialCases` config.

---

## Troubleshooting

### Filter not appearing in UI

1. Check `isEnabled` returns `true` for current filter state
2. Verify UI component imports `FilterOperations.getConfiguration('yourFilter')`
3. Confirm filter key matches exactly (case-sensitive)

### URL includes default value

1. Check `defaultValue` in config matches the value you're seeing
2. Verify you're using `buildCanonicalUrlDynamic` (not manual concatenation)
3. Ensure `getRemovalChanges` sets filter to `undefined` (not default value)

### Filter removal doesn't work

1. Check `getRemovalChanges` returns correct shape
2. Verify dependencies are also removed
3. Test removal URL with `FilterOperations.getRemovalUrl()`

### Tests failing after adding filter

1. Update test expectations if you intentionally changed behavior
2. Verify config structure matches schema in tests
3. Check that default value is handled correctly

---

**Last Updated**: January 15, 2026  
**Maintainer**: Development Team  
**Related Skills**: `url-canonicalization`, `api-layer-patterns`
