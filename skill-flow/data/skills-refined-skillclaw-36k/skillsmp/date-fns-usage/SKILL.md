---
name: date-fns-usage
description: Comprehensive date-fns usage guidance for date manipulation, formatting, and time zone handling in JavaScript/TypeScript applications
---

# What I Cover

This skill provides guidance on using date-fns for:

- Date parsing and formatting
- Date arithmetic (adding/subtracting time)
- Date comparisons (before/after, same day, etc.)
- Week and month operations
- Time zone handling
- Localization and internationalization

# Common Patterns

## Date Formatting

```javascript
import { format } from 'date-fns';

// Format dates for API calls
const dateStr = format(new Date(), 'yyyy-MM-dd');

// Format for display
const displayDate = format(date, 'PPP'); // e.g., "January 1st, 2024"
```

## Week Navigation

```javascript
import { startOfWeek, endOfWeek, addDays } from 'date-fns';

const weekStart = startOfWeek(date, { weekStartsOn: 1 }); // Monday start
const weekEnd = endOfWeek(date, { weekStartsOn: 1 });
const weekDates = Array.from({ length: 5 }, (_, i) => addDays(weekStart, i));
```

## Date Comparisons

```javascript
import { isPast, isToday, isFuture } from 'date-fns';

if (isPast(date) && !isToday(date)) {
  // Cannot place orders in the past
}
```

# Best Practices

- Import only the functions you need for tree-shaking
- Use consistent week start days (Monday = 1)
- Format dates consistently across the application
- Handle time zones appropriately for your use case
- Use date-fns over native Date methods for reliability

# Related Skills

- frontend-development
- sveltekit-development
- backend-development