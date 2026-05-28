# Calendar Reference

## Commands

### calendar-list
List all available calendars.
```bash
calendar-list        # Human-readable
calendar-list -j     # JSON output
```

### calendar-events
Query calendar events.
```bash
calendar-events                           # Today (default)
calendar-events -d 2025-11-15             # Specific date
calendar-events -w                        # This week
calendar-events -r 2025-11-15 2025-11-20  # Date range
calendar-events -c "Work"                 # Filter by calendar
calendar-events -j                        # JSON output
```

### calendar-add
Create new event. **REQUIRES USER CONFIRMATION**.
```bash
calendar-add -t "Meeting" -s 2025-11-15T14:00:00 -e 2025-11-15T15:00:00
calendar-add -t "Lunch" -s 2025-11-15T12:00:00 -e 2025-11-15T13:00:00 -l "Cafe" -c "Personal"
```

**Date format**: ISO-8601 `YYYY-MM-DDTHH:MM:SS` (24-hour time)

## Examples

**"What's on my calendar today?"**
```bash
calendar-events
```

**"Show my work meetings this week"**
```bash
calendar-events -w -c "Work"
```

**"Create lunch event tomorrow at noon"**
1. Calculate tomorrow's date
2. **ASK USER** with `AskUserQuestion`
3. If confirmed: `calendar-add -t "Lunch" -s 2025-11-16T12:00:00 -e 2025-11-16T13:00:00`

## Limitations

- Large date ranges (years) may timeout - use weeks/months
- Exit code 3 = timeout, suggest smaller range
