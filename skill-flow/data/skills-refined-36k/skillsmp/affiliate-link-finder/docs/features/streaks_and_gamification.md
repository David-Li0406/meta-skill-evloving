# Streaks & Gamification Mechanics

This document details the retention and motivation systems built into the app.

## Overview
The app uses "White Hat" gamification to encourage consistency without creating anxiety. See [ADR-005](file:///Users/lycanbeats/Desktop/adhd_supplement_app/docs/adrs/005-gamification-strategy.md) for design philosophy.

## Screens

### 1. `TrophyRoomScreen`
**Location**: `lib/presentation/views/trophy_room_screen.dart`

A visual display of all earned achievements.

**Badge Categories:**
- **Consistency**: 7-day, 30-day, 100-day streaks.
- **Exploration**: Try 10 different supplements.
- **Community**: Refer 3 friends.
- **Learning**: Read 5 science articles.

**UI:**
- Locked badges shown in grayscale with unlock criteria.
- Unlocked badges shown in full color with unlock date.
- Confetti animation on unlock.

### 2. `MilestoneSuccessScreen`
**Location**: `lib/presentation/views/milestone_success_screen.dart`

A full-screen celebration shown when hitting major streaks (7, 30, 90 days).

**Features:**
- Particle background animation.
- Trophy icon with streak count.
- Share button (social proof).
- Motivational message.

**Trigger Logic:**
Called by `DailyStackViewModel` when `streakCount` hits a milestone threshold.

### 3. `LevelUpScreen`
**Location**: `lib/presentation/views/level_up_screen.dart`

Shown when the user's "Brain Health Score" increases a level.

**Levels:**
- Lv 1-5: Beginner
- Lv 6-10: Intermediate
- Lv 11+: Advanced

**Level Calculation:**
Based on cumulative action points:
- Log supplements: +10 pts
- Complete symptom check-in: +5 pts
- Maintain 7-day streak: +50 pts

### 4. `StreakRecoveryScreen` & `StreakSavedScreen`
**Location**: 
- `lib/presentation/views/streak_recovery_screen.dart`
- `lib/presentation/views/streak_saved_screen.dart`

**Streak Recovery:**
Shown when a user misses a day. Offers:
- "Use a Grace Day" (if available).
- "Start a new streak" (resets counter).

**Streak Saved:**
Confirmation screen after using a Grace Day.
- Shows remaining grace days.
- Encourages user to get back on track.

### 5. `SuccessStatsScreen`
**Location**: `lib/presentation/views/success_stats_screen.dart`

A comprehensive view of the user's stats dashboard.

**Metrics:**
- Total days logged.
- Current streak.
- Longest streak ever.
- Completion percentage.
- Total supplements tried.

**Visualizations:**
- Calendar heatmap (GitHub-style).
- Progress bars for various achievements.

## Grace Period Mechanics
Users start with 3 grace days per month. These:
- Auto-renew monthly.
- Cannot stack (max 3 at a time).
- Are used automatically when a day is missed.

**Purpose:**
Prevents the "broken streak = quit app" cycle common in ADHD users with RSD (Rejection Sensitive Dysphoria).

## Related Features
See also: [Gamification and Notifications](gamification_and_notifications.md).
