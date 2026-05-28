---
name: api-layer-patterns
description: Enforce the internal API proxy layer pattern. Use when adding API endpoints, fetching data from backend, implementing HMAC signing, or working with lib/api/* or app/api/*.
license: MIT
---

# API Layer Patterns Guide

This skill enforces the **internal API proxy layer architecture** - a critical security and performance pattern in this Next.js application.

## When to Use This Skill

- Adding a new API endpoint
- Fetching data from the backend
- Implementing HMAC authentication
- Working with `lib/api/*` or `app/api/*`
- Debugging API calls or caching issues
- Implementing query builders

---

## Core Architecture: The Proxy Pattern

**CRITICAL**: Never call external API directly from pages/components. Always use the three-layer pattern.

```text
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Client Code (Pages/Components)                    │
│ - Calls internal API routes only                           │
│ - Uses getInternalApiUrl() for URL construction            │
│ - No HMAC signing (server-side only)                       │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: Internal API Routes (app/api/*)                   │
│ - Next.js route handlers (edge-friendly)                   │
│ - Call external wrappers                                   │
│ - Set cache headers (s-maxage, stale-while-revalidate)     │
│ - Return safe fallbacks on errors                          │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: External Wrappers (lib/api/*-external.ts)         │
│ - HMAC signing via fetchWithHmac                           │
│ - Env guard (NEXT_PUBLIC_API_URL check)                    │
│ - Zod parsing for type safety                              │
│ - Safe fallback DTOs on failure                            │
│ - Call NEXT_PUBLIC_API_URL directly                        │
└─────────────────────────────────────────────────────────────┘
```

**Why this pattern?**

- **Security**: HMAC signing happens server-side only
- **Caching**: Internal routes set optimal cache headers
- **Resilience**: Graceful degradation when backend unavailable
- **DRY**: Shared logic in wrappers, reused across routes

---

## Layer 1: Client Code

### Fetching Data from Pages/Components

**DO**:

```typescript
// In a Server Component
import { fetchEvents } from "@lib/api/events";

export default async function EventsPage() {
  const events = await fetchEvents({ place: "barcelona" });
  return <EventList events={events} />;
}

// In a Client Component (with SWR)
import useSWR from "swr";
import { getInternalApiUrl } from "@utils/api-helpers";

function EventsFeed() {
  const { data } = useSWR(
    getInternalApiUrl("/api/events", { place: "barcelona" }),
    fetcher
  );
  return <EventList events={data?.content || []} />;
}
```

**DON'T**:

```typescript
// ❌ WRONG: Direct external API call
const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/events`);

// ❌ WRONG: Manual HMAC signing in client code
const signature = createHmacSignature(url, secret); // NEVER expose secret!

// ❌ WRONG: Hardcoded internal URL
const { data } = useSWR("/api/events?place=barcelona", fetcher);
// Use getInternalApiUrl() instead
```

### Using Query Builders

**DO**:

```typescript
import { buildEventsQuery, buildNewsQuery } from "@utils/api-helpers";

// Build query params for events
const params = buildEventsQuery({
  place: "barcelona",
  byDate: "avui",
  searchTerm: "jazz",
  distance: 10,
  lat: 41.3851,
  lon: 2.1734,
});

const url = `/api/events?${params.toString()}`;
```

**DON'T**:

```typescript
// ❌ WRONG: Manual URLSearchParams construction
const params = new URLSearchParams();
params.set("place", "barcelona");
params.set("searchTerm", "jazz"); // Wrong! API expects 'term' not 'searchTerm'
// Manual construction duplicates logic and is error-prone - use query builders
```

---

## Layer 2: Internal API Routes

### File Structure

```text
app/api/
├── events/
│   ├── route.ts              # GET /api/events
│   ├── [slug]/route.ts       # GET /api/events/[slug]
│   └── categorized/route.ts  # GET /api/events/categorized
├── news/
│   ├── route.ts              # GET /api/news
│   └── [slug]/route.ts       # GET /api/news/[slug]
├── categories/
│   ├── route.ts              # GET /api/categories
│   └── [id]/route.ts         # GET /api/categories/[id]
└── visits/
    └── route.ts              # POST /api/visits
```

### Route Template

**File**: `app/api/YOUR_RESOURCE/route.ts`

```typescript
import { NextRequest, NextResponse } from "next/server";
import { fetchYourResourceExternal } from "@lib/api/your-resource-external";
import { buildYourResourceQuery } from "@utils/api-helpers";

export const runtime = "edge"; // Edge-friendly

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;

  // Build query using query builder
  const query = buildYourResourceQuery({
    param1: searchParams.get("param1") || undefined,
    param2: searchParams.get("param2") || undefined,
  });

  // Call external wrapper
  const data = await fetchYourResourceExternal(query);

  // Set cache headers
  return NextResponse.json(data, {
    headers: {
      "Cache-Control": "s-maxage=600, stale-while-revalidate=3600",
    },
  });
}
```

### Cache Headers Strategy

| Resource   | s-maxage     | stale-while-revalidate | Rationale          |
| ---------- | ------------ | ---------------------- | ------------------ |
| Events     | 600s (10m)   | 3600s (1h)             | Frequently updated |
| News       | 60s (1m)     | 300s (5m)              | Very dynamic       |
| Categories | 3600s (1h)   | 86400s (24h)           | Rarely change      |
| Sitemaps   | 86400s (24h) | 604800s (7d)           | Static structure   |

**Template**:

```typescript
headers: {
  'Cache-Control': 's-maxage=<SECONDS>, stale-while-revalidate=<SECONDS>',
}
```

---

## Layer 3: External Wrappers

### External Wrapper File Structure

```text
lib/api/
├── events-external.ts
├── news-external.ts
├── categories-external.ts
├── cities-external.ts
├── regions-external.ts
└── places-external.ts
```

### Wrapper Template (Guarded Pattern)

**File**: `lib/api/your-resource-external.ts`

```typescript
import { fetchWithHmac } from "@lib/api/fetch-wrapper";
import { z } from "zod";
import type {
  YourResourceDTO,
  PagedYourResourceDTO,
} from "types/api/your-resource";

// Zod schema for runtime validation (single item)
const YourResourceSchema = z.object({
  id: z.number(),
  name: z.string(),
  // ... other fields
});

// Paged response schema
const PagedResponseSchema = z.object({
  content: z.array(YourResourceSchema),
  currentPage: z.number(),
  pageSize: z.number(),
  totalElements: z.number(),
  totalPages: z.number(),
  last: z.boolean(),
});

export async function fetchYourResourceExternal(
  query?: URLSearchParams
): Promise<PagedYourResourceDTO> {
  // 1. ENV GUARD (critical for preview environments)
  if (!process.env.NEXT_PUBLIC_API_URL) {
    console.warn(
      "[YourResource] NEXT_PUBLIC_API_URL not set, returning empty data"
    );
    return {
      content: [],
      currentPage: 0,
      pageSize: 20,
      totalElements: 0,
      totalPages: 0,
      last: true,
    };
  }

  // 2. BUILD URL
  const baseUrl = `${process.env.NEXT_PUBLIC_API_URL}/your-resource`;
  const url = query ? `${baseUrl}?${query.toString()}` : baseUrl;

  try {
    // 3. FETCH WITH HMAC (10s timeout)
    const response = await fetchWithHmac(url, {
      method: "GET",
      next: {
        revalidate: 600, // ISR: 10 minutes
        tags: ["your-resource"],
      },
    });

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    const data = await response.json();

    // 4. ZOD PARSING (runtime validation)
    const parsed = PagedResponseSchema.parse(data);

    return parsed;
  } catch (error) {
    console.error("[YourResource] Fetch failed:", error);

    // 5. SAFE FALLBACK (resilience)
    return {
      content: [],
      currentPage: 0,
      pageSize: 20,
      totalElements: 0,
      totalPages: 0,
      last: true,
    };
  }
}
```

### Guarded Pattern Checklist

- [x] **Env guard**: Check `NEXT_PUBLIC_API_URL`, return safe fallback if missing
- [x] **Query builder**: Use `buildEventsQuery` / `buildNewsQuery` from caller
- [x] **HMAC fetch**: Use `fetchWithHmac` (NOT raw `fetch()`)
- [x] **Timeout**: `fetchWithHmac` has built-in 10s timeout
- [x] **Zod parsing**: Validate response shape at runtime
- [x] **Safe fallback**: Return empty DTO on error (never throw)
- [x] **Cache tags**: Use `next: { revalidate, tags }` for ISR
- [x] **Error logging**: Log errors for debugging

---

## Common Patterns

### Pagination

```typescript
export async function fetchEventsExternal(
  query?: URLSearchParams
): Promise<PagedResponseDTO<Event>> {
  // ... fetch logic

  const parsed = PagedResponseSchema.parse(data);

  // Use 'last' property to stop infinite scroll
  return parsed; // { content[], last: boolean }
}
```

**Client-side infinite scroll**:

```typescript
const { data, size, setSize } = useSWRInfinite((pageIndex) => {
  const params = buildEventsQuery({ place, page: pageIndex });
  return getInternalApiUrl("/api/events", params);
}, fetcher);

const isReachedEnd = data?.[data.length - 1]?.last;
```

### Search Term Mapping

**IMPORTANT**: Internal filter key `searchTerm` maps to API param `term`.

```typescript
// In buildEventsQuery()
if (filters.searchTerm) {
  params.set("term", filters.searchTerm); // NOT 'searchTerm'
}
```

### Distance & Geolocation

**UI filter** uses `distance` + `lat` + `lon`.  
**API** expects `radius` + `lat` + `lon`.

```typescript
import { distanceToRadius } from "types/event";

if (filters.distance && filters.lat && filters.lon) {
  params.set("radius", distanceToRadius(filters.distance).toString());
  params.set("lat", filters.lat.toString());
  params.set("lon", filters.lon.toString());
}
```

**Never send default distance (50)** - omit to reduce URL bloat.

### Date Filtering

```typescript
if (filters.byDate) {
  params.set("byDate", filters.byDate); // Shortcuts: avui, dema, setmana
} else if (filters.from || filters.to) {
  if (filters.from) params.set("from", filters.from);
  if (filters.to) params.set("to", filters.to);
}
```

**Don't send both `byDate` and `from/to`** unless intentional.

---

## Security Best Practices

### HMAC Signing

**DO**:

```typescript
// In external wrapper
import { fetchWithHmac } from "@lib/api/fetch-wrapper";

const response = await fetchWithHmac(url, {
  method: "GET",
  next: { revalidate: 600 },
});
```

**DON'T**:

```typescript
// ❌ WRONG: Raw fetch without HMAC
const response = await fetch(url);

// ❌ WRONG: Manual HMAC signing
import crypto from "crypto";
const signature = crypto.createHmac("sha256", secret).update(url).digest("hex");
// Use fetchWithHmac() which handles this automatically
```

### Middleware HMAC Enforcement

**Public endpoints** (GET, no auth needed):

- `/api/events`
- `/api/news`
- `/api/categories`
- `/api/places`
- `/api/regions`
- `/api/cities`

**Protected endpoints** (POST/PUT/DELETE, HMAC required):

- `/api/visits` (POST)
- `/api/events/*` (POST/PUT/DELETE)

**Implementation**: `proxy.ts` allowlists public GET routes; all others require HMAC.

---

## Fetch Best Practices

### ✅ ALWAYS Use Safe Fetch

**DO**:

```typescript
// For internal API calls (Layer 3)
import { fetchWithHmac } from "@lib/api/fetch-wrapper";
const response = await fetchWithHmac(url, {
  /* options */
});
// Built-in 10s timeout, HMAC signing

// For external webhooks/services (fire-and-forget)
import { safeFetch, fireAndForgetFetch } from "@utils/safe-fetch";
const response = await safeFetch(url, {
  /* options */
});
// Built-in 5s timeout, response validation, Sentry logging

await fireAndForgetFetch(url, { method: "POST", body: data });
// Fire-and-forget pattern for webhooks
```

**DON'T**:

```typescript
// ❌ WRONG: Raw fetch (can hang indefinitely in serverless)
const response = await fetch(url);

// ❌ WRONG: Manual AbortSignal (duplicates safeFetch logic)
const controller = new AbortController();
setTimeout(() => controller.abort(), 5000);
const response = await fetch(url, { signal: controller.signal });
```

**ESLint warns on raw `fetch()`** - always use wrappers.

---

## Error Handling & Sentry

### Sentry Tagging Conventions

Always include consistent tags for searchability:

```typescript
import { captureException } from "@sentry/nextjs";

captureException(error, {
  tags: {
    section: "events-fetch", // Feature area
    type: "validation-failed", // Error type
    layer: "external-wrapper", // Architecture layer
  },
  extra: {
    params, // Request context
    responseStatus: response.status, // API response info
  },
});
```

**Standard tags**:

| Tag       | Values                                                       |
| --------- | ------------------------------------------------------------ |
| `section` | `events-fetch`, `news-fetch`, `categories`, `webhooks`       |
| `type`    | `validation-failed`, `fetch-failed`, `timeout`, `hmac-error` |
| `layer`   | `external-wrapper`, `internal-route`, `client-lib`           |

### ⚠️ Preserve Stack Traces

**DO**:

```typescript
// Pass original error - preserves stack trace
captureException(error, {
  tags: { section: "events-fetch" },
  extra: { params },
});
```

**DON'T**:

```typescript
// ❌ WRONG: Loses original stack trace
captureException(new Error(error.message), {
  tags: { section: "events-fetch" },
});

// ❌ WRONG: Swallows error details
captureException(new Error("Fetch failed"));
```

### Validation Failure Pattern

When Zod validation fails, capture with context:

```typescript
const result = PagedResponseSchema.safeParse(data);

if (!result.success) {
  console.error("Validation failed:", result.error.format());

  captureException(new Error("API response validation failed"), {
    tags: {
      section: "events-fetch",
      type: "validation-failed",
    },
    extra: {
      zodErrors: result.error.format(),
      rawData: JSON.stringify(data).slice(0, 1000), // Truncate for safety
    },
  });

  return safeFallback;
}
```

### Error Message Sanitization

Use the helper to prevent leaking sensitive data:

```typescript
import { getSanitizedErrorMessage } from "@utils/api-error-handler";

catch (error) {
  const errorMessage = getSanitizedErrorMessage(error);
  console.error("Fetch failed:", errorMessage);
  // Safe to log - sensitive info removed
}
```

---

## Testing

### Unit Test (External Wrapper)

```typescript
import { fetchYourResourceExternal } from "@lib/api/your-resource-external";

describe("fetchYourResourceExternal", () => {
  it("returns empty data when NEXT_PUBLIC_API_URL missing", async () => {
    delete process.env.NEXT_PUBLIC_API_URL;

    const result = await fetchYourResourceExternal();

    expect(result.content).toEqual([]);
    expect(result.last).toBe(true);
  });

  it("handles API errors gracefully", async () => {
    // Mock fetch to throw
    global.fetch = vi.fn().mockRejectedValue(new Error("Network error"));

    const result = await fetchYourResourceExternal();

    expect(result.content).toEqual([]); // Safe fallback
  });
});
```

### Integration Test (Internal Route)

```typescript
import { GET } from "@app/api/your-resource/route";
import { NextRequest } from "next/server";

describe("GET /api/your-resource", () => {
  it("returns cached response with correct headers", async () => {
    const request = new NextRequest("http://localhost:3000/api/your-resource");

    const response = await GET(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(response.headers.get("Cache-Control")).toContain("s-maxage=600");
    expect(data).toHaveProperty("content");
  });
});
```

---

## Common Mistakes

### ❌ Calling External API from Pages

```typescript
// WRONG: Direct call in page component
export default async function EventsPage() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/events`);
  const events = await res.json();
  return <EventList events={events} />;
}

// CORRECT: Use internal API client
import { fetchEvents } from "@lib/api/events";

export default async function EventsPage() {
  const events = await fetchEvents({ place: "barcelona" });
  return <EventList events={events} />;
}
```

### ❌ Duplicating Query Logic

```typescript
// WRONG: Manual URLSearchParams in multiple places
const params = new URLSearchParams();
params.set("place", "barcelona");
params.set("term", searchTerm);

// CORRECT: Use query builder
const params = buildEventsQuery({ place: "barcelona", searchTerm });
```

### ❌ Missing Env Guard

```typescript
// WRONG: Direct API call without guard
export async function fetchData() {
  const url = `${process.env.NEXT_PUBLIC_API_URL}/data`;
  const res = await fetch(url); // Crashes if env var missing
  return res.json();
}

// CORRECT: Guard first
export async function fetchData() {
  if (!process.env.NEXT_PUBLIC_API_URL) {
    console.warn("[Data] API URL not set");
    return { content: [] }; // Safe fallback
  }
  // ... fetch logic
}
```

### ❌ Forgetting Cache Headers

```typescript
// WRONG: No cache headers
return NextResponse.json(data);

// CORRECT: Set appropriate cache headers
return NextResponse.json(data, {
  headers: {
    "Cache-Control": "s-maxage=600, stale-while-revalidate=3600",
  },
});
```

---

## ⚠️ CRITICAL: Build-Time vs Runtime Behavior

### The Problem: Internal Routes Don't Exist During Build

During `next build` (static generation), internal API routes (`/api/*`) are **not available** because the Next.js server isn't running yet. This causes a **chicken-and-egg problem**:

1. Build tries to generate static pages
2. Pages call client libraries (`lib/api/events.ts`, `lib/api/places.ts`, etc.)
3. Client libraries call internal routes via `getInternalApiUrl("/api/...")`
4. Internal routes don't exist yet → returns HTML error page
5. JSON parse fails: `"<!DOCTYPE "... is not valid JSON`

### Environment-Specific Behavior

| Environment | `isBuildPhase` | Behavior |
|-------------|----------------|----------|
| **SST/AWS** | `true` (no `VERCEL_URL`) | Bypasses internal routes ✅ |
| **Vercel** | Depends on `NEXT_PHASE` | May try internal routes → fail ❌ |
| **Local dev** | `false` | Uses internal routes (server running) ✅ |

### The Solution: `isBuildPhase` Bypass Pattern

Every client library in `lib/api/*.ts` MUST check `isBuildPhase` and call external wrappers directly during build:

```typescript
import { isBuildPhase } from "@utils/constants";
import { fetchYourResourceExternal } from "./your-resource-external";

export async function fetchYourResource(): Promise<YourDTO[]> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  if (!apiUrl) return [];

  // ⚠️ CRITICAL: During build, bypass internal API (server not running)
  if (isBuildPhase) {
    try {
      return await fetchYourResourceExternal();
    } catch (error) {
      console.error("fetchYourResource: external fetch failed during build", error);
      return []; // Safe fallback
    }
  }

  // Runtime: use internal API route (with caching benefits)
  try {
    return await resourceCache(fetchFromInternalApi);
  } catch (e) {
    console.error("Error fetching resource:", e);
    return [];
  }
}
```

### Files That MUST Have This Pattern

| File | Functions | Status |
|------|-----------|--------|
| `lib/api/events.ts` | `fetchEvents`, `getCategorizedEvents` | ✅ Has pattern |
| `lib/api/regions.ts` | `fetchRegionsWithCities`, `fetchRegionsOptions` | ✅ Has pattern |
| `lib/api/cities.ts` | `fetchCities` | ✅ Has pattern |
| `lib/api/places.ts` | `fetchPlaceBySlug`, `fetchPlaces` | ✅ Has pattern |
| `lib/api/categories.ts` | `fetchCategories`, `fetchCategoryById` | ✅ Has pattern |
| `lib/api/news.ts` | Check if needed | Verify |

### How to Verify

```bash
# Check all client libraries have the pattern
grep -l "isBuildPhase" lib/api/*.ts | grep -v external

# Expected: events.ts, regions.ts, cities.ts, places.ts, categories.ts
```

### Symptoms of Missing Pattern

- Build error: `SyntaxError: Unexpected token '<', "<!DOCTYPE "... is not valid JSON`
- Build error: `Error fetching X by slug: HTTP 401` (if HMAC secret missing)
- Error only appears when Next.js cache is cleared or on fresh deploy

---

## Resources

### Templates

- [external-wrapper-template.ts](./templates/external-wrapper-template.ts)
- [internal-route-template.ts](./templates/internal-route-template.ts)
- [client-library-template.ts](./templates/client-library-template.ts)

### Examples

- [correct-api-call-flow.md](./examples/correct-api-call-flow.md)
- [query-builder-usage.md](./examples/query-builder-usage.md)

### Reference Files

- `lib/api/*-external.ts` - External wrappers
- `app/api/*` - Internal routes
- `utils/api-helpers.ts` - Query builders
- `utils/fetch-with-hmac.ts` - HMAC fetch utility
- `utils/safe-fetch.ts` - Safe fetch wrappers

---

## FAQ

**Q: When do I need a new API route?**  
A: When adding a new backend resource or endpoint variant. Example: `/api/events/trending`.

**Q: Can I skip the internal route and call external wrapper directly?**  
A: No. Pages/components should never import `*-external.ts`. Always go through `/api/*`.

**Q: What if I need to call a third-party API (not our backend)?**  
A: Create an internal route (`/api/third-party`) that proxies the call. Use `safeFetch` if no HMAC needed.

**Q: How do I debug HMAC signature mismatches?**  
A: Check middleware logs (`proxy.ts`). Ensure `HMAC_SECRET` matches between client and server.

**Q: Should I use `fetch` or `axios`?**  
A: Use `fetchWithHmac` (for internal API with HMAC) or `safeFetch` (for external APIs). Never raw `fetch`.

---

**Last Updated**: January 15, 2026  
**Maintainer**: Development Team  
**Related Skills**: `filter-system-dev`, `type-system-governance`
