---
name: datetime
description: This skill should be used when the user asks about "time", "date", "timezone", "convert time", "what time is it in", "how many days until", "duration between", or needs date/time calculations.
---

# /datetime

Handle date, time, timezone conversions, and duration calculations.

## Instructions

### 1. Current Time

Show current time in requested timezone(s):

```
Current time:
  UTC:        2024-01-15 14:30:00 UTC
  Local:      2024-01-15 09:30:00 EST (UTC-5)
  Requested:  2024-01-15 23:30:00 JST (UTC+9)
```

### 2. Timezone Conversions

Convert a specific time between zones:

```
Input:  2024-01-15 09:00 EST
Output: 2024-01-15 14:00 UTC
        2024-01-15 23:00 JST
        2024-01-15 15:00 CET
```

### 3. Common Timezone Abbreviations

| Abbrev    | Name                       | Offset  |
| --------- | -------------------------- | ------- |
| UTC       | Coordinated Universal Time | +0      |
| EST/EDT   | US Eastern                 | -5/-4   |
| CST/CDT   | US Central                 | -6/-5   |
| PST/PDT   | US Pacific                 | -8/-7   |
| GMT       | Greenwich Mean Time        | +0      |
| CET/CEST  | Central European           | +1/+2   |
| JST       | Japan Standard             | +9      |
| IST       | India Standard             | +5:30   |
| AEST/AEDT | Australian Eastern         | +10/+11 |
| SGT       | Singapore                  | +8      |
| ICT       | Indochina (Vietnam)        | +7      |

### 4. Duration Calculations

Calculate time between two dates:

```
From: 2024-01-15
To:   2024-03-20

Duration:
  65 days
  9 weeks, 2 days
  2 months, 5 days
```

### 5. Date Arithmetic

Add or subtract from a date:

```
Start: 2024-01-15
Add:   30 days

Result: 2024-02-14
```

### 6. Format Conversions

Convert between formats:

```
Input:  1705330200 (Unix timestamp)
Output: 2024-01-15T14:30:00Z (ISO 8601)
        Mon, 15 Jan 2024 14:30:00 +0000 (RFC 2822)
        January 15, 2024 2:30 PM UTC (Human)
```

### 7. Business Days

Calculate working days (Mon-Fri):

```
From: 2024-01-15 (Mon)
To:   2024-01-26 (Fri)

Calendar days: 11
Business days: 10
```

## Python Utility

For complex operations, use the datetime utility:

```bash
uv run tools/datetime_util.py --help
```

## Edge Cases to Handle

- **DST transitions**: Warn about ambiguous times (e.g., 1:30 AM during fall-back)
- **Leap years**: February 29 exists only in leap years
- **Timezone offset changes**: Some zones have changed historically
