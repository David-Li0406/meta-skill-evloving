---
name: creating-ics-files
description: >
  Creates RFC 5545-compliant .ics calendar files from documents or metadata.
  Use when the user asks to create calendar events, meeting invites, or .ics files.
---

# ICS File Creator

Creates `.ics` (iCalendar) files from documents or metadata provided by the user.

## Default Assumptions

- **Timezone**: US Central (America/Chicago - Minneapolis) unless specified otherwise

## Required Information

Before creating an ICS file, ensure you have:

1. **Event title/summary** - from the document or user input
2. **Date and time** - start and end times
3. **Location** - if not provided, ask the user
4. **Invitees** - if not provided, ask the user for attendee email addresses
5. **Notes/description** - if not provided, ask the user

## Workflow

1. Parse the provided document or metadata to extract event details
2. Identify any missing required information (location, invitees, notes)
3. Ask the user for any missing information before proceeding
4. Generate the ICS file
5. Display a detailed summary for verification (see below)

## ICS File Format

Use this template for generating events:

```text
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//ICS Generator//EN
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
UID:{unique-id}@generated
DTSTAMP:{current-utc-timestamp}
DTSTART;TZID=America/Chicago:{start-datetime}
DTEND;TZID=America/Chicago:{end-datetime}
SUMMARY:{event-title}
LOCATION:{location}
DESCRIPTION:{notes}
ORGANIZER;CN={organizer-name}:mailto:{organizer-email}
ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;CN={attendee-name}:mailto:{attendee-email}
END:VEVENT
END:VCALENDAR
```

### Date/Time Formats

- With timezone: `DTSTART;TZID=America/Chicago:20250115T140000`
- All-day events: `DTSTART;VALUE=DATE:20250115`
- UTC: `DTSTART:20250115T200000Z`

### Multiple Attendees

Add one `ATTENDEE` line per invitee:

```text
ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;CN=Alice:mailto:alice@example.com
ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;CN=Bob:mailto:bob@example.com
```

## Verification Summary

After creating the ICS file, ALWAYS display a detailed summary like this:

```
## Event Summary

**Title**: Weekly Team Standup
**Date**: Wednesday, January 15, 2025
**Time**: 2:00 PM - 2:30 PM (US Central - America/Chicago)
**Duration**: 30 minutes
**Location**: Conference Room A / https://zoom.us/j/123456789

**Invitees**:
- Alice Smith <alice@example.com>
- Bob Jones <bob@example.com>

**Notes**:
Weekly sync to discuss project progress and blockers.

**File**: meeting.ics
```

This allows the user to manually verify all event details are correct before using the file.

## Recurring Events

For recurring events, add an RRULE:

- Weekly: `RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR`
- Daily: `RRULE:FREQ=DAILY`
- Monthly: `RRULE:FREQ=MONTHLY;BYMONTHDAY=15`
- With end date: `RRULE:FREQ=WEEKLY;UNTIL=20251231T235959Z`
- With count: `RRULE:FREQ=WEEKLY;COUNT=10`

## Validation Checklist

Before returning the ICS file, verify:

- [ ] All `BEGIN:` / `END:` blocks are correctly paired
- [ ] Required properties present: `UID`, `DTSTAMP`, `DTSTART`, `DTEND`, `SUMMARY`
- [ ] Timezone is correctly specified (default: America/Chicago)
- [ ] All attendee email addresses are valid format
- [ ] Location is included
- [ ] Description/notes are included
- [ ] For recurring events, RRULE syntax is valid
