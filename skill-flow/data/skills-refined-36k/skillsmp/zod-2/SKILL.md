---
name: zod
description: This skill provides Zod 4 validation patterns and conventions for the fitness app. Use when writing validation schemas, working with ISO dates, or validating API inputs.
---

# Zod 4 Validation Skill

This skill documents Zod 4 validation patterns for the fitness app.

## Version

This project uses **Zod 4** (zod@^4.0.0). Zod 4 introduced several new APIs and syntax changes.

## Key Zod 4 Features

### ISO Date/Time Validation

Zod 4 introduces `z.iso` namespace for ISO 8601 format validation:

```typescript
// Datetime (ISO 8601)
z.iso.datetime()                           // "2020-01-01T06:15:00Z"
z.iso.datetime({ offset: true })           // "2020-01-01T06:15:00+02:00"
z.iso.datetime({ local: true })            // "2020-01-01T06:15:01" (no timezone)
z.iso.datetime({ precision: 3 })           // milliseconds required

// Date only
z.iso.date()                               // "2020-01-01"

// Time only
z.iso.time()                               // "06:15:00"
z.iso.time({ precision: 3 })               // "06:15:00.123"

// Duration
z.iso.duration()                           // "P3Y6M4DT12H30M5S"
```

### Custom Error Messages

```typescript
// With custom message
z.iso.datetime({ message: 'Invalid date format' })

// With multiple options
z.iso.datetime({
  offset: true,
  message: 'Date must include timezone offset'
})
```

### UUID Validation

```typescript
z.uuid()                                   // Any valid UUID
z.uuid({ version: 4 })                     // UUID v4 only
z.uuid({ message: 'Invalid ID' })          // Custom error
```

### Common Patterns

```typescript
// Optional datetime
z.iso.datetime().optional()

// Nullable datetime
z.iso.datetime().nullable()

// Both optional and nullable
z.iso.datetime().nullish()

// Transform to Date object
z.iso.datetime().transform(str => new Date(str))
```

## Schema Location Conventions

- **Shared schemas**: `/shared/schemas/*.ts` - Reusable across client/server
- **Shared validations**: `/shared/validations/*.ts` - API input validation
- **Local schemas**: Define in API route files for route-specific validation

## Example Schemas

### Query Parameters

```typescript
export const analyticsQuerySchema = z.object({
  period: z.enum(['7d', '30d', '90d', '1y', 'all']).optional(),
  startDate: z.iso.datetime({ message: 'Invalid start date' }).optional(),
  endDate: z.iso.datetime({ message: 'Invalid end date' }).optional(),
})
```

### Request Body

```typescript
export const createChallengeSchema = z.object({
  name: z.string().min(1).max(100),
  startDate: z.iso.datetime({ message: 'Invalid start date' }),
  endDate: z.iso.datetime({ message: 'Invalid end date' }),
}).refine(
  (data) => new Date(data.endDate) > new Date(data.startDate),
  { message: 'End date must be after start date', path: ['endDate'] }
)
```

### Route Parameters

```typescript
const paramsSchema = z.object({
  id: z.uuid({ message: 'Invalid ID format' }),
})
```

## Migration from Zod 3

| Zod 3 | Zod 4 |
|-------|-------|
| `z.string().datetime()` | `z.iso.datetime()` |
| `z.string().date()` | `z.iso.date()` |
| `z.string().time()` | `z.iso.time()` |
| `z.string().uuid()` | `z.uuid()` |

## Validation Helpers

Use the project's validation helpers in API routes:

```typescript
import { validateBody, validateParams, validateQuery } from '~~/server/utils/bodyValidation'

export default defineEventHandler(async (event) => {
  const { id } = await validateParams(event, paramsSchema)
  const body = await validateBody(event, bodySchema)
  const query = await validateQuery(event, querySchema)
})
```
