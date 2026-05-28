---
name: timezone-strategy
description: Use this skill when handling dates and times in the application. Ensures consistent UTC storage and JST display patterns across backend and frontend code.
---

# Timezone Strategy Skill

Use this skill when handling dates and times in API routes, database operations, or frontend display.

## When to Use

- Saving timestamps to the database
- Displaying dates/times in the UI
- Getting the current date/time for business logic
- Reviewing code for timezone-related bugs

## Core Strategy

**UTC Storage + Frontend JST Conversion**

| Layer | Format | Example |
|-------|--------|---------|
| Database | UTC | `2025-01-14T22:43:00Z` |
| Frontend Display | JST | `07:43` |

## Patterns & Examples

### 1. Database Storage (UTC)

Always save timestamps in UTC using `toISOString()`.

```typescript
// GOOD
const record = {
  checked_in_at: new Date().toISOString()  // "2025-01-14T22:43:00Z"
}

// DB column type: TIMESTAMP WITH TIME ZONE
```

### 2. Frontend Display (JST)

Always specify `timeZone: 'Asia/Tokyo'` when displaying.

```typescript
// GOOD
new Date(utcString).toLocaleTimeString('ja-JP', {
  hour: '2-digit',
  minute: '2-digit',
  timeZone: 'Asia/Tokyo'
})
```

### 3. Current Date/Time (JST)

Use utility functions from `lib/utils/timezone.ts`.

```typescript
import { getCurrentDateJST, getCurrentTimeJST } from '@/lib/utils/timezone'

const today = getCurrentDateJST()  // "2025-01-15"
const now = getCurrentTimeJST()    // "07:43"
```

## Best Practices

### Do

- Use `new Date().toISOString()` for database storage
- Use `timeZone: 'Asia/Tokyo'` for display
- Use `getCurrentDateJST()` / `getCurrentTimeJST()` for current date/time
- Use `TIMESTAMP WITH TIME ZONE` column type

### Don't

- Use `new Date().toISOString().split('T')[0]` for "today's date"
  - Returns **UTC date**, which is yesterday before 9:00 AM JST
- Omit timezone specification when displaying
- Store JST time directly in database

## Utility Functions

Available in `lib/utils/timezone.ts`:

| Function | Description | Return Example |
|----------|-------------|----------------|
| `formatTimeJST(isoString)` | Convert UTC string to JST time | `"07:43"` |
| `getCurrentDateJST()` | Get current JST date | `"2025-01-15"` |
| `getCurrentTimeJST()` | Get current JST time | `"07:43"` |

## Notes

- Supabase Dashboard shows UTC (this is normal)
- JST 7:43 = UTC 22:43 (previous day) is correct conversion
- Japan does not use daylight saving time (fixed UTC+9)

## References

- `lib/utils/timezone.ts` - Utility function implementations
- `docs/03_database.md` - Database schema definitions
