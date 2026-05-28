# ADR 004: Notification System Architecture (The "Black Box" Recorder)

## Status
Accepted

## Context
ADHD users frequently struggle with **Time Blindness** and **Working Memory Deficits**. 
Standard mobile push notifications are often:
1.  Missed entirely (phone in another room).
2.  Dismissed reflexively (to clear the screen) and immediately forgotten.
3.  Sources of anxiety ("What did I just miss?").

We need a system that ensures critical health reminders (medication, hydration) are persistent and reviewable, acting as an external memory aid.

## Decision
We will implement a **Dual-Layer Notification System**:

1.  **Ephemeral Layer (System Notifications)**:
    - Standard local notifications via `flutter_local_notifications`.
    - Used for immediate alerts (Time to take pills, Water check).
    - These can be dismissed by the OS or user.

2.  **Persistent Layer (The "Black Box" Log)**:
    - Internal app database (SQLite/Isar/Firebase) stores a permanent log of every notification sent.
    - **UI**: A dedicated `NotificationHistoryScreen` acting as a timeline.
    - **Logic**: Notifications are objects first, alerts second. When an alert is scheduled, a corresponding log entry is created.

## Consequences
### Positive
- **Safety**: Users can always check "Did I get a reminder to take my meds?" if they are unsure.
- **Auditable**: Provides a history of app interactivity and support.
- **Reduced Anxiety**: Users know they can "clear" their lock screen without losing information.

### Negative
- **Storage Overhead**: Requires storing text data for every notification.
- **Synchronization**: Need to ensure the local log syncs with cloud if multi-device support is added later.

## Implementation Details
- **Entity**: `NotificationLogItem` (id, title, body, timestamp, type).
- **Retention**: Logs older than 30 days may be archived or summarized to save space, but initially kept indefinitely for MVP.
