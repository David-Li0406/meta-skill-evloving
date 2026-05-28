# ADR 0027: Tiered Gamification & Progress Visualization

## Status
Accepted

## Context
ADHD users benefit from immediate, clear, and tiered rewards that break down long-term goals into manageable chunks. The previous gamification system was binary (earned/locked) and lacked granularity, which could lead to loss of motivation for longer milestones.

## Decision
We decided to implement a tiered badge system and real-time progress visualization:

1.  **Tiered Badges**: Introduced `BadgeTier` (Bronze, Silver, Gold) to differentiate between entry-level wins and long-term achievements.
2.  **Progress Tracking**: Added `currentValue`, `targetValue`, and `progress` fields to `GamificationBadge`.
3.  **Real-Time Visualization**: Updated the `TrophyRoomScreen` to display `LinearProgressIndicator` for locked badges, providing immediate feedback on how close a user is to their next reward.
4.  **XP Reward Visibility**: Displayed potential XP rewards on locked badges to create a clearer "value prop" for completing the goal.

## Consequences
- **Positive**: Increased "dopamine hits" through visible progress; better long-term retention via Silver/Gold tiers.
- **Maintenance**: Requires repositories to calculate and provide current progress values for each badge.
