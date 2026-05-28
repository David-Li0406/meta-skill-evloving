# Offline Mode & Error Handling

This document covers how the app handles network issues and errors gracefully.

## Overview
The app is designed to work offline-first, storing data locally and syncing when connectivity returns.

## Screens

### 1. `OfflineErrorScreen`
**Location**: `lib/presentation/views/offline_error_screen.dart`

Shown when the app detects no internet connection on critical operations (login, sync).

**Features:**
- Friendly error message: "Looks like you're offline. Don't worry, your logs are saved locally."
- "Retry" button.
- "Continue Offline" option (dismisses and allows local-only use).

**Auto-Retry:**
Checks connectivity every 30 seconds and auto-dismisses when connection is restored.

### 2. `CloudSyncScreen`
**Location**: `lib/presentation/views/cloud_sync_screen.dart`

A loading screen shown during initial sync or when uploading large batches of data.

**UI:**
- Animated cloud icon.
- Progress indicator.
- "Syncing your data..." message.

**Trigger Points:**
- First login (download user's existing data).
- After extended offline period (upload queued logs).

### 3. `DeveloperHandoffLogicTriggersScreen`
**Location**: `lib/presentation/views/developer_handoff_logic_triggers_screen.dart`

A debug screen for developers to manually trigger events and test error states.

**Actions:**
- Simulate offline mode.
- Clear local cache.
- Force crash notification.
- Test push notification delivery.
- Trigger specific error states.

**Access:**
Hidden from normal users. Accessed via secret gesture (7 taps on version number).

## Offline Data Strategy
The app uses a **local-first** architecture:

1. **Writes**: All user actions (log supplements, rate symptoms) are written to local storage first.
2. **Queue**: If offline, actions are queued for later sync.
3. **Sync**: On reconnection, queued actions are uploaded to Firebase.
4. **Reads**: Cached data is displayed immediately; fresh data is fetched in background.

**Technologies:**
- `sqflite` or `hive` for local database.
- `connectivity_plus` for network status monitoring.
- (Future) `Riverpod 3.0` for offline persistence API.

## Error Types Handled
- **Network Errors**: Offline screen, retry logic.
- **Authentication Errors**: Redirect to login, clear stale tokens.
- **Validation Errors**: Inline form errors with specific guidance.
- **Server Errors**: "Something went wrong. Try again later."

## User Experience Principles
- **Never block**: User can always interact with cached data.
- **Transparent syncing**: Clear indicators when syncing is happening.
- **Fail gracefully**: Errors are shown but never crash the app.
