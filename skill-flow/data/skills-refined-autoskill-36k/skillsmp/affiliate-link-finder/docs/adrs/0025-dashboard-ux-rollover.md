# ADR 0025: Dashboard UX and Logical Day Rollover

## Context
The Dashboard ("Today" view) needs to feel rewarding and respect the lifestyle of users who may stay up past midnight. Standard calendar day resets cause confusion for late-night usage. Additionally, users want a cleaner view of what remains to be taken.

## Decision
1. **Logical Rollover**: Set the "Daily Reset" time to **4:00 AM**. Any intake before 4 AM is attributed to the previous calendar day.
2. **Dynamic Filtering**: Items marked as "Taken" are filtered out from the Today Dashboard to reduce cognitive load.
3. **Feedback Loop**: Integrated system sounds (tick) and haptic feedback to reward completion.

## Implementation
- **ViewModel**: `DailyStackViewModel` implements `_getLogicalToday()` which subtracts a day if the current hour is < 4.
- **UI**: Added `HapticFeedback` and `SystemSound` to the `onTake` callback in `DashboardScreen`.
- **UI**: Moved the options menu (3-dots) to the top-left of `MedicationCard` for a cleaner interface.

## Consequences
- **Pros**: Matches ADHD user behavior (night owls); reduced "clutter" in the UI; enhanced gamification via tactile/audible feedback.
- **Cons**: Users cannot see "Completed" items on the dashboard (though they remain in the History).
- **Verification**: Covered by `daily_stack_view_model_test.dart`.
