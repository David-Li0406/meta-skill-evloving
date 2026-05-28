---
name: data-validation-patterns
description: Guide for validating external data with Zod. Use when fetching from APIs, processing webhooks, or handling user input.
---

# Data Validation Patterns Skill

## Purpose

Ensure all external data is validated using Zod schemas before use. Prevents runtime type errors and provides safe fallbacks.

## ⚠️ CRITICAL: Always Validate External Data

**ALL data from external sources MUST be validated:**

- API responses (backend, third-party)
- Webhook payloads
- User input (forms, query params)
- URL parameters

## Zod Schema Location

All validation schemas live in `lib/validation/`:

```text
lib/validation/
├── event.ts      # Event DTOs, paged responses
├── city.ts       # City/region DTOs
├── place.ts      # Place DTOs
└── category.ts   # Category DTOs
```

**Rule**: Create schemas alongside the API client that uses them.

## Basic Validation Pattern

### 1. Define Schema

```typescript
// lib/validation/my-resource.ts
import { z } from "zod";

export const MyResourceSchema = z.object({
  id: z.string(),
  name: z.string(),
  count: z.number(),
  optional: z.string().optional(),
  nullable: z.string().nullable(),
});

export type MyResource = z.infer<typeof MyResourceSchema>;

// For arrays
export const MyResourceArraySchema = z.array(MyResourceSchema);

// For paged responses
export const PagedMyResourceSchema = z.object({
  content: z.array(MyResourceSchema),
  currentPage: z.number(),
  pageSize: z.number(),
  totalElements: z.number(),
  totalPages: z.number(),
  last: z.boolean(),
});
```

### 2. Create Parser Function

```typescript
// lib/validation/my-resource.ts

export function parseMyResource(data: unknown): MyResource | null {
  const result = MyResourceSchema.safeParse(data);
  if (!result.success) {
    console.error("MyResource validation failed:", result.error.format());
    return null;
  }
  return result.data;
}

export function parseMyResourceArray(data: unknown): MyResource[] {
  const result = MyResourceArraySchema.safeParse(data);
  if (!result.success) {
    console.error("MyResource array validation failed:", result.error.format());
    return []; // Safe fallback
  }
  return result.data;
}
```

### 3. Use in External Wrapper (Layer 3 - Calls External API)

```typescript
// lib/api/my-resource-external.ts
// NOTE: fetchWithHmac is ONLY used in external wrappers (Layer 3)
// See api-layer-patterns skill for the three-layer architecture
import { captureException } from "@sentry/nextjs";
import { fetchWithHmac } from "@lib/api/fetch-wrapper";
import { parseMyResource } from "@lib/validation/my-resource";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function fetchMyResourceExternal(id: string): Promise<MyResource | null> {
  if (!API_URL) return null; // Environment guard

  try {
    const response = await fetchWithHmac(`${API_URL}/api/my-resource/${id}`);
    const data = await response.json();

    const validated = parseMyResource(data);
    if (!validated) {
      captureException(new Error("MyResource validation failed"), {
        tags: { section: "my-resource", type: "validation-failed" },
        extra: { id, data },
      });
      return null;
    }

    return validated;
  } catch (error) {
    captureException(error, {
      tags: { section: "my-resource", type: "fetch-failed" },
      extra: { id },
    });
    return null;
  }
}
```

## Existing Parser Functions

Reference these existing patterns:

| Parser                     | Location                  | Returns                    |
| -------------------------- | ------------------------- | -------------------------- |
| `parsePagedEvents`         | `lib/validation/event.ts` | Paged events or null       |
| `parseEventDetail`         | `lib/validation/event.ts` | Event detail or null       |
| `parseCategorizedEvents`   | `lib/validation/event.ts` | Categorized events or null |
| `PlaceResponseArraySchema` | `lib/validation/place.ts` | Place array                |
| `CitySummaryArraySchema`   | `lib/validation/city.ts`  | City array                 |

## Validation with Sentry Integration

Always capture validation failures to Sentry:

```typescript
import { captureException } from "@sentry/nextjs";

export function parseWithSentry<T>(
  schema: z.ZodSchema<T>,
  data: unknown,
  context: { section: string; extra?: Record<string, unknown> }
): T | null {
  const result = schema.safeParse(data);

  if (!result.success) {
    console.error(
      `${context.section} validation failed:`,
      result.error.format()
    );

    // Create error with validation details for better Sentry context
    const validationError = new Error(
      `${context.section} validation failed: ${result.error.message}`
    );
    validationError.cause = result.error; // Preserve original Zod error

    captureException(validationError, {
      tags: {
        section: context.section,
        type: "validation-failed",
      },
      extra: {
        ...context.extra,
        zodErrors: result.error.format(),
      },
    });

    return null;
  }

  return result.data;
}
```

## Safe Fallback Patterns

### For Single Objects → Return `null`

```typescript
export function parseEvent(data: unknown): EventDetail | null {
  const result = EventDetailSchema.safeParse(data);
  return result.success ? result.data : null;
}

// Usage
const event = parseEvent(data);
if (!event) {
  return notFound(); // or handle gracefully
}
```

### For Arrays → Return `[]`

```typescript
export function parseEvents(data: unknown): Event[] {
  const result = EventArraySchema.safeParse(data);
  return result.success ? result.data : [];
}

// Usage - always safe to map
const events = parseEvents(data);
return events.map((e) => <EventCard key={e.id} event={e} />);
```

### For Paged Responses → Return Empty Page

```typescript
const emptyPage: PagedResponse<Event> = {
  content: [],
  currentPage: 0,
  pageSize: 10,
  totalElements: 0,
  totalPages: 0,
  last: true,
};

export function parsePagedEvents(data: unknown): PagedResponse<Event> {
  const result = PagedEventSchema.safeParse(data);
  return result.success ? result.data : emptyPage;
}
```

## Common Zod Patterns

### Optional vs Nullable

```typescript
z.string().optional(); // string | undefined
z.string().nullable(); // string | null
z.string().nullish(); // string | null | undefined
```

### Default Values

```typescript
z.number().default(0);
z.string().default("");
z.array(z.string()).default([]);
```

### Transformations

```typescript
// Coerce string to number
z.coerce.number();

// Transform after validation
z.string().transform((s) => s.toLowerCase());

// Date from string
z.string()
  .datetime()
  .transform((s) => new Date(s));
```

### Discriminated Unions

```typescript
const ResponseSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("success"), data: DataSchema }),
  z.object({ type: z.literal("error"), message: z.string() }),
]);
```

## Webhook Validation Example

From `lib/stripe/webhook.ts`:

```typescript
const StripeWebhookEventSchema = z.object({
  id: z.string().min(1),
  type: z.string().min(1),
  data: z.object({
    object: z.record(z.unknown()),
  }),
});

export type StripeWebhookEvent = z.infer<typeof StripeWebhookEventSchema>;

export function validateWebhookEvent(
  payload: unknown
): StripeWebhookEvent | null {
  const result = StripeWebhookEventSchema.safeParse(payload);
  if (!result.success) {
    console.error("Webhook validation failed:", result.error.format());
    return null;
  }
  return result.data;
}
```

## Checklist for New API Endpoint

- [ ] Created Zod schema in `lib/validation/`?
- [ ] Created parser function with safe fallback?
- [ ] Using `safeParse` (not `parse`) to avoid throws?
- [ ] Capturing validation failures to Sentry?
- [ ] Returning safe fallback (null, [], empty page)?
- [ ] Type exported via `z.infer<typeof Schema>`?

## Common Mistakes

1. **Using `parse` instead of `safeParse`** → Throws on invalid data
2. **Not logging validation errors** → Silent failures
3. **Returning `undefined` instead of `null`** → Inconsistent handling
4. **Forgetting Sentry capture** → No visibility into prod issues
5. **Defining types separately from schema** → Type drift

## Files to Reference

- [lib/validation/event.ts](../../../lib/validation/event.ts) - Complete example
- [lib/validation/city.ts](../../../lib/validation/city.ts) - Simple schema
- [lib/api/events.ts](../../../lib/api/events.ts) - Usage pattern
- [lib/stripe/webhook.ts](../../../lib/stripe/webhook.ts) - Webhook validation
