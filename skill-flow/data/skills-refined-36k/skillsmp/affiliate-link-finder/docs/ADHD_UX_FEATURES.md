# ADHD-Friendly UX Features

This document outlines the specific features implemented to support users with ADHD, focusing on reducing cognitive load, managing time blindness, and encouraging consistency.

## 1. "Quick Take" Swipe Gesture
**Problem**: Logging supplement intake required multiple taps (navigate to daily stack -> find item -> tap checkmark), which creates friction for users with ADHD.
**Solution**: Implemented a swipe-right gesture on any supplement card in the Daily Stack.
- **Visual Feedback**: A green background with a checkmark icon appears behind the card as it is swiped.
- **Effect**: Instantly logs the supplement as taken and removes it from the "due" list.
- **Benefit**: Reduces the motor and cognitive effort required to keep logs accurate.

## 2. Time Urgency & Countdown
**Problem**: "Time blindness" makes it difficult for users with ADHD to gauge how much time they have left before a dose is due or how long it has been since a dose was missed.
**Solution**: Dynamic time status labels on supplement cards.
- **Format**: 
  - `in 30m` / `in 2h 15m`: Countdown to scheduled dose.
  - `Overdue by 15m`: Clear indicator of missed time.
  - `Overdue`: If missed by more than 4 hours.
- **Implementation**: Normalizes broad time slots (Morning, Afternoon, Evening, Night) to specific anchor hours (08:00, 13:00, 18:00, 21:00) to provide relative urgency.

## 3. Persistent Nudge Notifications
**Problem**: A single notification is easily ignored or forgotten immediately after being dismissed.
**Solution**: A sequence of reminders.
- **Morning Sequence**:
  - `08:00`: Main reminder.
  - `08:15`: Warning nudge if not logged.
  - `08:30`: Final follow-up.
- **Evening Summary**:
  - `20:00`: A prompt to review the day's progress and "close the loop" on any unlogged items.
- **Benefit**: Creates multiple "re-entry points" for the user to remember their routine.

## 4. Simplified Onboarding
**Problem**: Long onboarding flows with too many decisions lead to "choice paralysis" and app abandonment.
**Solution**: Reduced the flow from 6+ steps to 3 core value-driven decisions.
1.  **Goal Selection**: Focuses on *why* the user is here (e.g., "Mental Clarity").
2.  **Safety Check**: High-impact decision about existing medications (Ensures safety early).
3.  **Direct-to-Dashboard**: Skips manual stack building initially, allowing users to explore pre-configured suggestions or add items contextually.

## 5. 4:00 AM Rollover Logic
**Problem**: Users with ADHD often have erratic sleep schedules. A hard midnight reset can be discouraging if a user takes an "evening" supplement at 1 AM.
**Solution**: The "logical day" resets at 4:00 AM.
- **Benefit**: Supplements taken after midnight but before 4 AM are still counted towards the previous calendar day's goals and streak.
