# Notification Service

This document describes the local notification infrastructure.

## Overview
The app uses `flutter_local_notifications` for scheduling and displaying local push notifications.

## Component

### `NotificationService` (Infrastructure Service)
**Location**: `lib/infrastructure/services/notification_service.dart`

**Key Methods:**
- `init()`: Initializes the native notification plugin (Android/iOS settings).
- `showNotification({id, title, body})`: Immediately displays a notification.

**Android Configuration:**
- Channel ID: `adhd_channel`
- Channel Name: `ADHD Notifications`
- Importance: `max`
- Priority: `high`

## Current State (MVP)
The service is a **basic wrapper**. It can show immediate notifications but **lacks**:
- Scheduled notifications (daily reminders).
- Repeating notifications (hourly nudges).
- Background task integration.

## Future Enhancements (See Task.md Phase 10 & 15)
- [ ] **Scheduled Reminders**: `flutterLocalNotificationsPlugin.zonedSchedule(...)`.
- [ ] **"Nag Mode"**: Repeat until acknowledged (for critical meds).
- [ ] **Black Box Logging**: Every notification sent should also be logged to `NotificationHistoryScreen`.
- [ ] **Smart Nudges**: Time-aware nudges based on user behavior patterns.

## ADR Reference
See [ADR-004: Notification Architecture](file:///Users/lycanbeats/Desktop/adhd_supplement_app/docs/adrs/004-notification-system-architecture.md).
