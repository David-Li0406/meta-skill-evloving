# ADR 0011: Persistent Notification System for ADHD-Friendly Reminders

**Date:** 2026-01-19  
**Status:** Proposed  
**Deciders:** Development Team

## Context

ADHD users often struggle with:
- Forgetting to take supplements despite good intentions
- Dismissing single notifications and losing track
- Time blindness making it hard to remember when they last took supplements
- Need for gentle but persistent reminders that don't feel punishing

The lock screen mockup demonstrates a multi-tier notification strategy with escalating persistence.

## Decision

Implement a **3-tier persistent notification system** using `flutter_local_notifications` with platform-specific customization.

### Notification Tiers

| Tier | Trigger | Style | Actions |
|------|---------|-------|---------|
| **Primary Nudge** | Scheduled time | Rich notification with image | "Take Now", "Snooze 5m" |
| **Persistent Nudge** | After 3 dismissals | Border accent + counter | "Open App" |
| **Wellness Check** | 30min after stack | Mood rating buttons | Emoji selection |

### Technical Implementation

```dart
// Package: flutter_local_notifications ^17.0.0

class NotificationService {
  static const String channelId = 'supplement_nudges';
  static const String urgentChannelId = 'persistent_nudges';
  
  // Schedule primary nudge
  Future<void> scheduleStackReminder(SupplementStack stack) async {
    await flutterLocalNotificationsPlugin.zonedSchedule(
      stack.id.hashCode,
      'Morning Focus',
      'Omega-3, B12, and Vitamin D',
      _nextInstanceOfTime(stack.scheduledTime),
      NotificationDetails(
        android: AndroidNotificationDetails(
          channelId,
          'Supplement Nudges',
          importance: Importance.high,
          priority: Priority.high,
          styleInformation: BigPictureStyleInformation(...),
          actions: [
            AndroidNotificationAction('take', 'Take Now'),
            AndroidNotificationAction('snooze', 'Snooze 5m'),
          ],
        ),
        iOS: DarwinNotificationDetails(
          presentAlert: true,
          presentBadge: true,
          presentSound: true,
          categoryIdentifier: 'STACK_REMINDER',
          attachments: [DarwinNotificationAttachment(...)],
        ),
      ),
      androidScheduleMode: AndroidScheduleMode.exactAllowWhileIdle,
      uiLocalNotificationDateInterpretation: ...,
    );
  }
  
  // Escalate to persistent nudge after dismissals
  Future<void> escalateToPersistent(int dismissalCount) async {
    await flutterLocalNotificationsPlugin.show(
      999, // High-priority ID
      'PERSISTENT NUDGE',
      'Your Focus Stack is waiting! This is your ${_ordinal(dismissalCount)} reminder.',
      NotificationDetails(
        android: AndroidNotificationDetails(
          urgentChannelId,
          'Persistent Nudges',
          importance: Importance.max,
          priority: Priority.max,
          color: Color(0xFF13EC5B), // Primary green
          ledColor: Color(0xFF13EC5B),
          ledOnMs: 1000,
          ledOffMs: 500,
          ongoing: true, // Sticky notification
        ),
      ),
    );
  }
}
```

### iOS Notification Categories

```swift
// AppDelegate.swift
let takeAction = UNNotificationAction(
    identifier: "TAKE_ACTION",
    title: "Take Now",
    options: [.foreground]
)

let snoozeAction = UNNotificationAction(
    identifier: "SNOOZE_ACTION", 
    title: "Snooze 5m",
    options: []
)

let stackCategory = UNNotificationCategory(
    identifier: "STACK_REMINDER",
    actions: [takeAction, snoozeAction],
    intentIdentifiers: [],
    options: [.customDismissAction]
)

UNUserNotificationCenter.current().setNotificationCategories([stackCategory])
```

### Android Notification Channels

```kotlin
// MainActivity.kt
val channel = NotificationChannel(
    "supplement_nudges",
    "Supplement Nudges",
    NotificationManager.IMPORTANCE_HIGH
).apply {
    description = "Reminders for your supplement stacks"
    enableLights(true)
    lightColor = Color.parseColor("#13EC5B")
    enableVibration(true)
    vibrationPattern = longArrayOf(0, 500, 200, 500)
}
```

## Notification Flow

```
User schedules stack for 9:00 AM
    ↓
9:00 AM: Primary Nudge sent
    ↓
User dismisses → Snooze 5m
    ↓
9:05 AM: Primary Nudge #2
    ↓
User dismisses → Snooze 5m
    ↓
9:10 AM: Primary Nudge #3
    ↓
User dismisses → ESCALATE
    ↓
9:10 AM: Persistent Nudge (sticky)
    ↓
User taps "Open App" → Navigate to DailyStackScreen
    ↓
9:30 AM: Wellness Check notification
```

## Dismissal Tracking

Store dismissal count in local storage:

```dart
class NotificationDismissalTracker {
  static const String _keyPrefix = 'nudge_dismissals_';
  
  Future<int> getDismissalCount(String stackId) async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getInt('$_keyPrefix$stackId') ?? 0;
  }
  
  Future<void> incrementDismissals(String stackId) async {
    final prefs = await SharedPreferences.getInstance();
    final count = await getDismissalCount(stackId);
    await prefs.setInt('$_keyPrefix$stackId', count + 1);
    
    // Escalate after 3 dismissals
    if (count + 1 >= 3) {
      await NotificationService().escalateToPersistent(count + 1);
    }
  }
  
  Future<void> resetDismissals(String stackId) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('$_keyPrefix$stackId');
  }
}
```

## User Settings

Allow users to configure in `PersistentRemindersScreen`:

- **Snooze Duration:** 5m, 10m, 15m, 30m
- **Max Reminders:** 1-5 before escalation
- **Quiet Hours:** 10 PM - 7 AM (no nudges)
- **Notification Style:** Gentle, Standard, Persistent
- **Wellness Checks:** Enabled/Disabled

## Consequences

**Positive:**
- ADHD-friendly persistent reminders without punishment
- Escalation prevents users from ignoring indefinitely
- Rich notifications with images increase engagement
- Action buttons reduce friction (no need to open app)

**Negative:**
- Requires platform-specific code (iOS/Android)
- Battery impact from frequent notifications
- Risk of notification fatigue if overused
- Complexity in managing notification state

**Mitigations:**
- Respect system "Do Not Disturb" settings
- Provide easy opt-out in settings
- Limit escalation to 3 reminders max per stack
- Clear all notifications when stack is completed

## Dependencies

- `flutter_local_notifications: ^17.0.0`
- `timezone: ^0.9.0` (for scheduling)
- `shared_preferences: ^2.0.0` (dismissal tracking)
- Platform permissions: `POST_NOTIFICATIONS` (Android 13+), `UNUserNotificationCenter` (iOS)

## Future Enhancements

- Smart scheduling based on user patterns (ML)
- Adaptive snooze times (learns user behavior)
- Integration with Apple Health / Google Fit for context
- Voice-based "I took it" confirmation via Siri/Assistant
