---
name: date-time-implementation
description: Guide for implementing date/time operations using dayjs with unix timestamps and Polish locale. Use when adding date handling to components or API endpoints.
---

# Date and Time Implementation Skill

Guide for implementing date/time operations using dayjs utility with unix timestamps.

## Purpose

USE this skill when:
- Adding date/time functionality to components
- Implementing API endpoints with date fields
- Working with scheduled dates or timestamps
- Formatting dates for display

## Critical Rules

⚠️ **ALWAYS import from `~/app/utils/date.ts`** - NEVER import dayjs directly
⚠️ **USE unix timestamps (seconds)** - For API communication and database storage
⚠️ **STORE as integer** - Database columns use integer type for unix timestamps
⚠️ **USE Polish locale** - Pre-configured in app/utils/date.ts

## Import Pattern

```typescript
// ✅ CORRECT: Import pre-configured dayjs
import { dayjs, formatDatePL, dateToUnixTimestamp, unixTimestampToDate } from "~/app/utils/date"

// ❌ WRONG: Direct import bypasses configuration
import dayjs from "dayjs"
```

## Unix Timestamp Strategy

### Converting to Unix Timestamp

```typescript
import { dateToUnixTimestamp, dayjs } from "~/app/utils/date"

// From Date object
const timestamp = dateToUnixTimestamp(new Date()) // Returns seconds

// From dayjs object
const timestamp = dayjs().unix()

// From ISO string
const timestamp = dayjs("2025-01-15").unix()
```

### Converting from Unix Timestamp

```typescript
import { unixTimestampToDate, dayjs } from "~/app/utils/date"

// To Date object
const date = unixTimestampToDate(1736942400)

// To dayjs for manipulation
const dayjsDate = dayjs.unix(1736942400)
const formatted = dayjsDate.format("YYYY-MM-DD")
```

## API Data Exchange

### Sending to API

```typescript
import { dateToUnixTimestamp } from "~/app/utils/date"

const formData = {
  title: "Meeting",
  scheduledDate: dateToUnixTimestamp(selectedDate), // seconds
}

await $fetch("/api/meetings", {
  method: "POST",
  body: formData,
})
```

### Receiving from API

```typescript
import { formatDatePL } from "~/app/utils/date"

const { data: meetings } = await useFetch<Meeting[]>("/api/meetings")

const displayDate = computed(() => {
  if (!meetings.value?.[0]) return ""
  return formatDatePL(meetings.value[0].scheduledDate)
})
```

## Database Schema Pattern

```typescript
// server/database/schema.ts
export const meetings = sqliteTable("meetings", {
  id: text("id").primaryKey(),
  scheduledDate: integer("scheduled_date").notNull(), // Unix timestamp (seconds)
  createdAt: integer("created_at", { mode: "timestamp" }).notNull(),
  updatedAt: integer("updated_at", { mode: "timestamp" }).notNull(),
})
```

## Formatting Dates

```typescript
import { formatDatePL, dayjs } from "~/app/utils/date"

// Polish locale formatting
const formatted = formatDatePL(timestamp) // "15 stycznia 2025"

// Custom formatting
const custom = dayjs.unix(timestamp).format("DD.MM.YYYY") // "15.01.2025"
```

## Component Integration with CalendarDate

```typescript
import { CalendarDate } from "@internationalized/date"
import { dateToUnixTimestamp, unixTimestampToDate, dayjs } from "~/app/utils/date"

// Convert CalendarDate to unix timestamp
function calendarDateToUnixTimestamp(calDate: CalendarDate): number {
  const jsDate = new Date(calDate.year, calDate.month - 1, calDate.day)
  return dateToUnixTimestamp(jsDate)
}

// Convert unix timestamp to CalendarDate
function unixTimestampToCalendarDate(timestamp: number): CalendarDate {
  const dayjsDate = dayjs.unix(timestamp)
  return new CalendarDate(
    dayjsDate.year(),
    dayjsDate.month() + 1,
    dayjsDate.date()
  )
}
```

## Anti-Patterns

❌ Direct dayjs import
❌ Using milliseconds instead of seconds
❌ Storing ISO strings in database
❌ Using Date.now() / 1000 (use dateToUnixTimestamp)

## References

- Full patterns: `.agents/date-time-patterns.md`
- dayjs documentation: Official docs (Context7)
