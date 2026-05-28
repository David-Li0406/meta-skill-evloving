# Gamification & Notification System

This document outlines the implementation and usage of the retention and engagement features in the ADHD Supplement App.

## 1. The Trophy Room (Gamification)
Located at `/trophy-room`, this screen visualizes the user's consistency.

### Key Components
- **Milestone Success Screen**: A popup celebration (`MilestoneSuccessScreen`) triggered when a user hits specific streak targets (7, 30, 90 days).
  - Uses `ParticlesBackground` for a safe, non-flashing confetti effect.
  - Allows sharing to social media via `share_plus`.
- **Badges**:
  - `LevelBadge`: Visual representation of current tier.
  - `WeeklyWinCard`: Highlights 7-day consistency.

### Developer Usage
To trigger a milestone manually (for testing):
```dart
Navigator.pushNamed(context, AppRouter.milestoneSuccess);
```

## 2. The Black Box (Notification History)
Located at `/notification-history`, this acts as the "Flight Recorder" for the user's day.

### Key Components
- **NotificationHistoryViewModel**: Manages the list of logs.
- **NotificationLogItem**: The data model.
  - `type`: `medication` (Pill Icon), `nudge` (Hand Icon), `achievement` (Trophy Icon).
- **Persistence**: 
  - *Current State*: Mocked in ViewModel.
  - *Future State*: Needs integration with `sqflite` or `hive` to persist logs across app restarts.

### Developer Usage
To add a notification to the history (Mock):
```dart
// Currently internal to ViewModel mock data.
// Future:
// locator<NotificationService>().logEvent(title: '...', body: '...');
```

## Design Philosophy
- **No Shame**: We celebrate wins and cushion losses.
- **Visual Clarity**: Different icons for different notification types help users scan their day quickly.
