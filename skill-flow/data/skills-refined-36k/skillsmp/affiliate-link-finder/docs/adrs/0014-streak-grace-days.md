# ADR 0014: Streak Tracking with Grace Day System

## Status
Accepted

## Context
Users with ADHD struggle with consistency due to executive function challenges. Traditional streak systems (miss one day = lose everything) are demotivating and unsustainable for this population.

Research shows:
- ADHD users benefit from forgiveness mechanisms
- All-or-nothing systems increase anxiety and abandonment
- Sustainable habit building requires flexibility

## Decision
We implemented a grace day system that forgives missed days while maintaining accountability:

**Core Rules:**
- Users get 2 grace days per month
- Grace days auto-apply when user misses a day
- Streak continues if grace days are available
- Streak resets only when grace days are exhausted
- Grace days reset at start of each month

**Implementation:**
- `Streak` entity tracks: `currentStreak`, `longestStreak`, `graceDaysRemaining`, `graceDaysUsed`
- `StreakService` calculates streak from daily logs
- Grace days apply automatically via business logic
- UI displays grace day status prominently

## Consequences

### Positive
- More sustainable for ADHD users
- Reduces anxiety and pressure
- Maintains accountability (finite grace days)
- Encourages long-term consistency over perfection
- Users can see grace day usage, promoting awareness

### Negative
- More complex than simple streak counting
- Could enable procrastination if misused
- Requires clear UI communication of how system works

### Neutral
- Grace days are a monthly budget (not per-streak)
- System favors consistency over rigid daily adherence
- Balances motivation with realistic ADHD challenges
