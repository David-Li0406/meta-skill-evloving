---
name: ics
description: This skill should be used when the user asks to "create calendar event", "add to calendar", "generate ics", "export to ical", or shares a flight/hotel/event booking screenshot or text to convert to calendar format.
---

# /ics

Extract event details from text or screenshots and generate `.ics` files for import into Apple Calendar, Google Calendar, or Outlook.

## Instructions

1. **Identify the input type:**
   - If user provides a file path to a screenshot/image, use the Read tool to view it
   - If user provides text, parse it directly

2. **Extract event details:**
   - **SUMMARY**: Event title (e.g., "Flight AA123 SFO→JFK", "Marriott Hotel Stay")
   - **DTSTART**: Start date/time in UTC (format: `YYYYMMDDTHHMMSSZ`)
   - **DTEND**: End date/time in UTC
   - **LOCATION**: Venue, airport, hotel address
   - **DESCRIPTION**: Additional details (confirmation number, booking reference, etc.)

3. **Handle time zones:**
   - Ask user for their local timezone if times appear ambiguous
   - Convert all times to UTC for the .ics file
   - Include `TZID` if needed for display purposes

4. **Generate the .ics file:**

```ics
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Claude Code//ICS Generator//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:{unique-id}@claude-code
DTSTAMP:{current-utc-timestamp}
DTSTART:{start-datetime}
DTEND:{end-datetime}
SUMMARY:{event-title}
LOCATION:{location}
DESCRIPTION:{details}
END:VEVENT
END:VCALENDAR
```

5. **Save the file:**
   - Default filename: `{event-type}-{date}.ics` (e.g., `flight-2025-01-15.ics`)
   - Save to current directory or user-specified path

## Event Type Templates

### Flight

- SUMMARY: `Flight {airline}{number} {origin}→{destination}`
- DTSTART: Departure time (local converted to UTC)
- DTEND: Arrival time (local converted to UTC)
- LOCATION: Departure airport
- DESCRIPTION: Confirmation #, seat, terminal/gate if available

### Hotel

- SUMMARY: `{hotel-name} - Check-in`
- DTSTART: Check-in date at 15:00 local (default)
- DTEND: Check-out date at 11:00 local (default)
- LOCATION: Hotel address
- DESCRIPTION: Confirmation #, room type, contact info

### Generic Event

- SUMMARY: Event name
- DTSTART/DTEND: As specified
- LOCATION: Venue
- DESCRIPTION: Any additional details

## Example Usage

**Input:** Screenshot of flight confirmation showing:

```
United Airlines UA456
Jan 20, 2025
Depart: SFO 8:30 AM → Arrive: ORD 2:45 PM
Confirmation: ABC123
```

**Output file:** `flight-2025-01-20.ics`

```ics
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Claude Code//ICS Generator//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:ua456-20250120@claude-code
DTSTAMP:20250120T000000Z
DTSTART:20250120T163000Z
DTEND:20250120T204500Z
SUMMARY:Flight UA456 SFO→ORD
LOCATION:San Francisco International Airport (SFO)
DESCRIPTION:Confirmation: ABC123\nUnited Airlines
END:VEVENT
END:VCALENDAR
```

## Notes

- For multi-leg flights, create separate events for each leg
- For hotel stays spanning multiple nights, create a single all-day event
- Always include confirmation/booking numbers in DESCRIPTION
- Use `\n` for line breaks within DESCRIPTION field
