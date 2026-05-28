---
name: url-canonicalization
description: Enforce URL rules to prevent SEO issues and cost incidents. CRITICAL - never add searchParams to listing pages ($300 incident).
---

# URL Canonicalization Skill

## Purpose

Enforce URL canonicalization rules to prevent SEO issues and **CRITICAL cost incidents** from dynamic page rendering.

## ⚠️ CRITICAL: Cost Prevention Rule

**NEVER add `searchParams` to page components in `app/[place]/` routes.**

Reading `searchParams` in a page component makes the page **dynamic**, causing OpenNext/SST to create a separate DynamoDB cache entry for every unique URL+query combination.

**Real Incident**: This caused a **$300+ cost spike** on December 28, 2025.

### What NOT To Do

```tsx
// ❌ FORBIDDEN - Makes page dynamic, creates millions of cache entries
export default async function PlacePage({
  params,
  searchParams, // ← NEVER DO THIS in listing pages
}: {
  params: { place: string };
  searchParams: { search?: string; distance?: string };
}) {
  // This will cost you hundreds of dollars
  const events = await fetchEvents({ ...searchParams });
}
```

### What To Do Instead

```tsx
// ✅ CORRECT - Page stays static (ISR)
export default async function PlacePage({
  params,
}: {
  params: { place: string };
}) {
  // Base data fetched server-side (static)
  const initialEvents = await fetchEvents({ place: params.place });

  // Query params handled CLIENT-SIDE via SWR
  return <HybridEventsList initialEvents={initialEvents} />;
}
```

## Canonical URL Rules

### Segment Omission Rules

| Condition                           | Canonical URL          |
| ----------------------------------- | ---------------------- |
| date = `tots` AND category = `tots` | `/place`               |
| date = `tots` AND category ≠ `tots` | `/place/category`      |
| date ≠ `tots` AND category = `tots` | `/place/date`          |
| date ≠ `tots` AND category ≠ `tots` | `/place/date/category` |

### Query Parameter Rules

- `search`, `distance`, `lat`, `lon` → Stay as query params
- `distance` omitted when default (50km)
- Legacy `?category=X&date=Y` → Redirect to path segments

## Middleware Redirects

The proxy (`proxy.ts`) handles canonical redirects via `handleCanonicalRedirects`:

```typescript
// These are handled automatically by middleware:
// /barcelona/tots/concerts → /barcelona/concerts (301)
// /barcelona?category=concerts&date=avui → /barcelona/avui/concerts (301)
// /catalunya/tots/tots → /catalunya (301)
```

## URL Building Functions

### Always Use These Helpers

```typescript
import { buildCanonicalUrl, buildFilterUrl } from "@utils/url-filters";

// ✅ Correct - uses helper that enforces rules
const url = buildCanonicalUrl(filters);

// Alternative for dynamic categories:
// buildCanonicalUrlDynamic(filters, dynamicCategories)

// ❌ Wrong - manual string concatenation
const url = `/${place}/${date}/${category}`;
```

### URL Parsing Helpers

```typescript
import { parseFiltersFromUrl, urlToFilterState } from "@utils/url-parsing";
import { getRedirectUrl } from "@utils/middleware-redirects";
```

## SEO for Filtered URLs

Filtered URLs (with `search`, `distance`) should have `noindex`:

- Handled via `X-Robots-Tag` header in `proxy.ts`
- NOT by making page dynamic with `searchParams`

## Checklist Before Modifying URL Logic

- [ ] Am I reading `searchParams` in a listing page? → **STOP, use client-side SWR**
- [ ] Am I building URLs manually? → Use `buildCanonicalUrlDynamic`
- [ ] Am I adding `/tots/` to URLs? → Check omission rules above
- [ ] Am I adding new query params? → Ensure they don't make pages dynamic

## Files to Reference

- [proxy.ts](../../../proxy.ts) - Canonical redirect logic
- [utils/url-filters.ts](../../../utils/url-filters.ts) - URL building helpers
- [utils/url-parsing.ts](../../../utils/url-parsing.ts) - URL parsing helpers
- [utils/middleware-redirects.ts](../../../utils/middleware-redirects.ts) - Redirect handlers

## Common Mistakes

1. **Adding searchParams to page props** → Use client-side SWR
2. **Manual URL string building** → Use helper functions
3. **Including `/tots/` in URLs** → Gets redirected, use canonical form
4. **Forgetting query param preservation** → Middleware handles this automatically
