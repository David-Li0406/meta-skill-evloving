---
name: calendar
description: Google Calendar management via CLI. Use when user mentions calendar, events, scheduling, appointments, meetings, free/busy time, or checking availability. Supports listing calendars, viewing/creating/updating/deleting events, and checking free/busy status.
---

# Calendar

Google Calendar access via `gccli` CLI.

## Account

Get the account email by running: `gccli accounts`

## Essential Commands

```bash
# List calendars
gccli <account> calendars

# List upcoming events (default: next week)
gccli <account> events primary

# Events with date range
gccli <account> events primary --from 2026-01-15T00:00:00 --to 2026-01-20T00:00:00

# Search events
gccli <account> events primary --query "meeting"

# Get event details
gccli <account> event primary <eventId>
```

## Creating Events

```bash
# Standard event
gccli <account> create primary \
  --summary "Meeting" \
  --start 2026-01-15T10:00:00 \
  --end 2026-01-15T11:00:00

# All-day event
gccli <account> create primary \
  --summary "Vacation" \
  --start 2026-01-20 \
  --end 2026-01-25 \
  --all-day

# With details
gccli <account> create primary \
  --summary "Team Sync" \
  --start 2026-01-15T14:00:00 \
  --end 2026-01-15T15:00:00 \
  --description "Weekly sync" \
  --location "Conference Room A" \
  --attendees "alice@example.com,bob@example.com"
```

## Modifying Events

```bash
# Update
gccli <account> update primary <eventId> --summary "New Title"

# Delete
gccli <account> delete primary <eventId>
```

## Free/Busy

```bash
gccli <account> freebusy primary --from 2026-01-15T00:00:00Z --to 2026-01-16T00:00:00Z
```

## Notes

- `primary` is the main calendar; use calendar ID from `calendars` command for others
- Datetimes: ISO 8601 format (local time or with Z for UTC)
- All-day events: use YYYY-MM-DD format with `--all-day` flag
