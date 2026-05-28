# ADR 0010: Gamification System Architecture

**Date:** 2026-01-19  
**Status:** Accepted  
**Deciders:** Development Team

## Context

ADHD users benefit from dopamine-driven reward loops. We needed a gamification system that:
- Tracks daily supplement intake streaks
- Provides visual celebrations (confetti, badges)
- Supports "grace days" for ADHD-friendly forgiveness
- Unlocks achievements and trophies

## Decision

Implement a multi-layer gamification system with dedicated screens.

### Streak System

```dart
// Streak calculation in LogRepository
Future<int> getStreakCount(String userId) async {
  // Count consecutive days with entries
  // Grace periods don't break streaks
}
```

### Celebration Screens

| Screen | Trigger | Purpose |
|--------|---------|---------|
| `StreakSavedScreen` | Grace day applied | Reassurance |
| `StreakRecoveryScreen` | After missed day | Encouragement |
| `LevelUpScreen` | Milestone reached | Celebration |
| `TrophyRoomScreen` | On demand | View achievements |

### Grace Period Logic

Users get 2 "grace days" per week that protect streaks:

```dart
class GracePeriodCard extends StatelessWidget {
  // Shows: "1 GRACE DAY REMAINING"
  // Includes: weekly reset countdown
}
```

### XP and Levels

Dashboard shows XP progress:
- +10 XP per supplement taken
- +50 XP for completing full stack
- +100 XP for weekly consistency

## Screen Navigation Flow

```
Daily Stack → Check Streak Status
                    ↓
         ┌─────────────────────┐
         │ Streak Maintained?  │
         └─────────────────────┘
           │ Yes         │ No
           ↓             ↓
    Stay on screen   Grace Day Available?
                           │ Yes      │ No
                           ↓          ↓
                    StreakSaved   StreakRecovery
```

## Consequences

**Positive:**
- Motivating reward system for ADHD users
- Forgiveness mechanism reduces guilt
- Visual celebrations provide dopamine hits
- Trophy collection adds long-term engagement

**Negative:**
- Additional state to track
- Complex streak calculations
- Multiple celebration screens to maintain
