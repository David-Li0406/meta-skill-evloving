# ADR 0013: Notification Scheduling with Timezone Support

## Status
Accepted

## Context
The app requires recurring daily notifications to remind users to take their supplement stacks. Requirements:
- Daily reminders at user-specified times (e.g., 8:00 AM, 12:00 PM, 8:00 PM)
- Reliable scheduling across app restarts
- Respects device timezone
- Works on both Android and iOS

Flutter's `flutter_local_notifications` package provides basic notification support but doesn't handle timezone-aware scheduling out of the box.

## Decision
We adopted the `timezone` package (v0.9.0) alongside `flutter_local_notifications` (v17.0.0) to enable reliable, timezone-aware notification scheduling.

Key implementation details:
- Initialize timezone data on app startup: `tz.initializeTimeZones()`
- Use `zonedSchedule()` with `matchDateTimeComponents.time` for daily recurrence
- Set `AndroidScheduleMode.exactAllowWhileIdle` for reliability even in battery saver mode
- Schedule at local timezone: `tz.TZDateTime.from(scheduledDate, tz.local)`

## Consequences

### Positive
- Accurate daily notifications at user's local time
- Handles timezone changes (travel, DST)
- Platform-consistent behavior (Android & iOS)
- Future-proof for additional scheduling needs

### Negative
- Additional dependency (`timezone` package ~400KB)
- Requires timezone initialization on startup
- More complex than simple time-based scheduling

### Neutral
- Must request notification permissions on iOS
- Android requires battery optimization exemptions for reliability
- Scheduled notifications persist across app restarts
