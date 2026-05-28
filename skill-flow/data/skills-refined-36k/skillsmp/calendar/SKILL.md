---
name: calendar
description: Read events from Calendar.app using icalBuddy
---

# Calendar

Read-only access to macOS Calendar.app via `icalBuddy`.

## Prerequisites

```bash
brew install ical-buddy
```

## Commands

### List Calendars

```bash
icalBuddy calendars
```

### Today's Events

```bash
# All calendars
icalBuddy eventsToday

# Specific calendar
icalBuddy -ic "mkane@cloudflare.com" eventsToday

# Compact format (no notes/attendees)
icalBuddy -eep notes,attendees -ic "mkane@cloudflare.com" eventsToday
```

### Upcoming Events

```bash
# Today + next 3 days
icalBuddy -ic "mkane@cloudflare.com" eventsToday+3

# From now only (exclude past events today)
icalBuddy -n -ic "mkane@cloudflare.com" eventsToday
```

### Events in Date Range

```bash
icalBuddy -ic "mkane@cloudflare.com" eventsFrom:"2026-01-07" to:"2026-01-14"
```

### Events Happening Now

```bash
icalBuddy -ic "mkane@cloudflare.com" eventsNow
```

### Show Event UIDs

```bash
icalBuddy -uid -ic "mkane@cloudflare.com" eventsToday
```

## Useful Options

| Option                 | Description                 |
| ---------------------- | --------------------------- |
| `-ic "Cal"`            | Include only this calendar  |
| `-ec "Cal"`            | Exclude this calendar       |
| `-n`                   | Only events from now on     |
| `-uid`                 | Show event UIDs             |
| `-nc`                  | No calendar names in output |
| `-eep notes`           | Exclude notes property      |
| `-eep attendees`       | Exclude attendees           |
| `-eep notes,attendees` | Exclude multiple properties |
| `-li 5`                | Limit to 5 items            |
| `-tf "%H:%M"`          | Time format (24h)           |
| `-df "%Y-%m-%d"`       | Date format                 |

## Example Output

```
• Team standup (Work)
    location: Zoom
    notes: Daily sync
    attendees: alice@co.com, bob@co.com
    09:00 - 09:30
• 1:1 with Alice (Work)
    location: Conference Room B
    14:00 - 14:30
```

## Filtering Noisy Calendars

Exclude holidays and birthdays:

```bash
icalBuddy -ec "Birthdays,UK Holidays,Siri Suggestions" eventsToday
```

Or include only work calendar:

```bash
icalBuddy -ic "mkane@cloudflare.com" eventsToday
```

## When to Use

- **Morning routine**: Check today's events to plan the day
- **Before meetings**: Get event details for meeting links and context
- **Scheduling**: Check availability before suggesting times
- **End of day**: Review what happened, what's tomorrow
