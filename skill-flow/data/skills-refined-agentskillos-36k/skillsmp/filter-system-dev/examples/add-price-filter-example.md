# Example: Adding a "Price" Filter

Complete walkthrough of adding a new filter to the events discovery system.

## Goal

Add a filter to show only free events, paid events, or all events.

## Requirements

- Filter key: `price`
- Values: `all` (default), `free`, `paid`
- URL strategy: Query parameter (`?price=free`)
- Default omitted from URL for SEO

---

## Step 1: Add Configuration

**File**: `config/filters.ts`

```typescript
export const FILTER_CONFIGURATIONS: FilterConfig[] = [
  // ... existing filters

  {
    key: "price",
    defaultValue: "all",
    isEnabled: (filters) => true, // Always enabled
    getDisplayText: (value) => {
      const labels = {
        all: "Tots els preus",
        free: "Gratuït",
        paid: "De pagament",
      };
      return labels[value] || value;
    },
    getRemovalChanges: (value, segments, queryParams) => ({
      queryParams: { ...queryParams, price: undefined },
    }),
  },
];
```

**Explanation**:

- `key: 'price'` - Internal identifier
- `defaultValue: 'all'` - When omitted from URL, defaults to "all"
- `isEnabled: () => true` - No conditional logic needed
- `getDisplayText` - Human-readable labels in Catalan
- `getRemovalChanges` - Removes `price` from query params

---

## Step 2: Create UI Component

**File**: `components/ui/filters/PriceFilter.tsx`

```typescript
"use client";

import { FilterOperations } from "@utils/filter-operations";
import { useFilterState } from "@components/hooks/useFilterState";

export function PriceFilter() {
  const { filters, updateFilter } = useFilterState();
  const config = FilterOperations.getConfiguration("price");

  const options = [
    { value: "all", label: "Tots els preus" },
    { value: "free", label: "Gratuït" },
    { value: "paid", label: "De pagament" },
  ];

  const handleChange = (value: string) => {
    updateFilter("price", value);
  };

  return (
    <div className="price-filter">
      <label className="label">Preu</label>
      <select
        name="price"
        value={filters.price || config.defaultValue}
        onChange={(e) => handleChange(e.target.value)}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
}
```

**Key points**:

- Uses `FilterOperations.getConfiguration('price')` to get config
- Reads default from config (DRY principle)
- Updates filter through `useFilterState` hook

---

## Step 3: Integrate in Filter UI

**File**: `components/ui/filters/FilterPanel.tsx`

```typescript
import { PriceFilter } from "./PriceFilter";

export function FilterPanel() {
  return (
    <div className="filter-panel">
      {/* ... existing filters */}
      <PriceFilter />
    </div>
  );
}
```

---

## Step 4: URL Building

**No code changes needed!** URL building is automatic:

```typescript
// User selects "free"
const url = buildCanonicalUrlDynamic({
  place: "barcelona",
  price: "free",
});
// → /barcelona?price=free

// User selects "all" (default)
const url = buildCanonicalUrlDynamic({
  place: "barcelona",
  price: "all",
});
// → /barcelona (default omitted)
```

---

## Step 5: API Integration

**File**: `utils/api-helpers.ts` (if not already handled)

Update `buildEventsQuery` to map `price` filter to API param:

```typescript
export function buildEventsQuery(filters: FilterState): URLSearchParams {
  const params = new URLSearchParams();

  // ... existing params

  if (filters.price === "free") {
    params.set("maxPrice", "0");
  } else if (filters.price === "paid") {
    params.set("minPrice", "0.01");
  }
  // If 'all', omit price params (API returns all)

  return params;
}
```

**Explanation**:

- UI filter `price: 'free'` → API param `maxPrice=0`
- UI filter `price: 'paid'` → API param `minPrice=0.01`
- Separation of concerns: UI state ≠ API schema

---

## Step 6: Testing

### Unit Test

**File**: `test/filter-system.test.ts`

```typescript
describe("Price Filter", () => {
  it("should have correct default value", () => {
    const config = FilterOperations.getConfiguration("price");
    expect(config.defaultValue).toBe("all");
  });

  it("should build removal URL correctly", () => {
    const segments = { place: "barcelona", date: "tots", category: "tots" };
    const queryParams = { price: "free" };

    const removalUrl = FilterOperations.getRemovalUrl(
      "price",
      segments,
      queryParams
    );

    expect(removalUrl).toBe("/barcelona"); // Removes ?price=free
  });

  it("should detect active state", () => {
    const filters = { price: "free" };
    const isActive = FilterOperations.isFilterActive("price", filters);
    expect(isActive).toBe(true);
  });
});
```

Run tests:

```bash
yarn test test/filter-system.test.ts
```

### E2E Test

**File**: `e2e/price-filter.spec.ts`

```typescript
import { test, expect } from "@playwright/test";

test("price filter updates URL and results", async ({ page }) => {
  await page.goto("/barcelona");

  // Select "free" filter
  await page.selectOption('select[name="price"]', "free");

  // URL should update
  await expect(page).toHaveURL("/barcelona?price=free");

  // Results should show only free events
  const events = page.locator('[data-testid="event-card"]');
  const firstEvent = events.first();
  await expect(firstEvent).toContainText("Gratuït");
});
```

Run E2E:

```bash
yarn test:e2e e2e/price-filter.spec.ts
```

---

## Step 7: Verification Checklist

- [x] Filter added to `config/filters.ts`
- [x] UI component created
- [x] Default value omitted from URL
- [x] Removal URL works (`/barcelona?price=free` → `/barcelona`)
- [x] API query builder updated
- [x] Unit tests pass
- [x] E2E tests pass
- [x] No duplicate logic in multiple files

---

## Result

Users can now filter events by price:

- `/barcelona` - All events (default)
- `/barcelona?price=free` - Only free events
- `/barcelona?price=paid` - Only paid events

**Time to implement**: ~20 minutes  
**Lines of code**: ~50 (most of it UI boilerplate)  
**Test coverage**: Unit + E2E

---

## Common Issues

### Issue: URL still shows `?price=all`

**Cause**: Not using `buildCanonicalUrlDynamic`  
**Fix**: Replace manual URL building with `buildCanonicalUrlDynamic`

### Issue: Filter doesn't appear in UI

**Cause**: Component not imported in `FilterPanel`  
**Fix**: Add `<PriceFilter />` to `FilterPanel.tsx`

### Issue: API returns all events regardless of filter

**Cause**: API query builder not updated  
**Fix**: Map `price` filter to API params in `buildEventsQuery`

### Issue: Tests fail with "Unknown filter key"

**Cause**: Config not saved or syntax error  
**Fix**: Verify `config/filters.ts` has valid TypeScript, restart dev server

---

**Time saved**: 1.5 hours (vs. manual implementation without this guide)
