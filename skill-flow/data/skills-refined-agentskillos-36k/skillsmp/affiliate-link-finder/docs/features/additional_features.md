# Additional Features & Specialized Screens

This document covers miscellaneous features that don't fit into other categories.

## Home & Navigation

### 1. `DashboardScreen`
**Location**: `lib/presentation/views/dashboard_screen.dart`

The main landing screen after login.

**Widgets:**
- **Today's Progress**: Circular progress ring showing % of supplements taken.
- **Quick Actions**: Buttons for "Log Supplement", "Check-In", "Add to Stack".
- **Streak Display**: Current streak count with fire emoji.
- **Upcoming Reminders**: Next scheduled notification.
- **Weekly Summary**: Mini chart preview linking to `InsightsScreen`.

**Empty State:**
If no stacks configured, shows onboarding prompt.

### 2. `HomeWidgetsPreviewScreen`
**Location**: `lib/presentation/views/home_widgets_preview_screen.dart`

Demonstrates what the iOS/Android home screen widgets look like.

**Widget Types:**
- **Small**: Just the streak count.
- **Medium**: Today's progress + next dose time.
- **Large**: Full stack checklist.

**Setup Guide:**
Step-by-step instructions for adding widgets to home screen.

## Stack Building

### 3. `StackBuilderScreen`
**Location**: `lib/presentation/views/stack_builder_screen.dart`

The advanced stack editor (post-onboarding).

**Features:**
- Drag-and-drop reordering.
- Time-based stacks (Morning/Afternoon/Evening/Bedtime).
- Duplicate stack templates.
- Delete stacks.
- Safety warnings inline.

**Related:**
See [Onboarding & Setup](onboarding_and_setup.md) for initial stack creation.

### 4. `LibraryScreen`
**Location**: `lib/presentation/views/library_screen.dart`

**ViewModel**: `LibraryViewModel`

Browse and search the supplement catalog.

**Features:**
- Search bar (real-time filtering, user-aware).
- Category filters (Focus, Sleep, Energy, etc.).
- Supplement cards showing benefits and dosage.
- **Custom Supplements**: "Add Custom" Floating Action Button; private items marked with **CUSTOM** badge; delete support.
- "Add to Stack" quick action.

**Data:**
Fetches from `SupplementRepository` (Firebase or mock).

### 5. `SupplementDetailView`
**Location**: `lib/presentation/views/supplement_detail_view.dart`

Detailed view of a single supplement.

**Content:**
- Full description.
- Benefits list.
- Recommended dosage.
- Safety warnings.
- "Buy on Amazon" affiliate button.
- User reviews (future).

## Notifications & Reminders

### 6. `NotificationReliabilitySetupScreen`
**Location**: `lib/presentation/views/notification_reliability_setup_screen.dart`

Guides users through enabling critical notification permissions.

**Steps:**
1. Grant notification permission.
2. Disable battery optimization (Android).
3. Enable background app refresh (iOS).
4. Test notification delivery.

**Why This Matters:**
ADHD users depend on reminders. This ensures notifications aren't silently dropped.

### 7. `PersistentRemindersScreen`
**Location**: `lib/presentation/views/persistent_reminders_screen.dart`

Configure recurring nudges and medication reminders.

**Settings:**
- Reminder times (e.g., 8 AM, 2 PM, 8 PM).
- Repeat intervals (every 15 min until acknowledged).
- Quiet hours (don't nag at night).
- Notification sound/vibration patterns.

**Current State:**
UI only. Requires integration with `NotificationService` scheduled notifications.

## Miscellaneous

### 8. `MedicationSafetyScreen`
**Location**: `lib/presentation/views/medication_safety_screen.dart`

Educational screen about medication-supplement interactions.

**Content:**
- Why timing matters.
- Common interactions (Vitamin C + stimulants).
- Link to full SafetyGuard checker.

### 9. `CloudSyncScreen`
Already documented in [Offline & Error Handling](offline_and_error_handling.md).
