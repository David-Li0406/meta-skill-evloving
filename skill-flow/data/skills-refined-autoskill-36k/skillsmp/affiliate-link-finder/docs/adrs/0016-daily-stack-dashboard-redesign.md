# ADR 0016: Daily Stack Dashboard Redesign & Time-slot Logic

**Date:** 2026-01-19  
**Status:** Accepted  
**Deciders:** Development Team

## Context

The previous dashboard implementation provided a flat list of medications, which was difficult for users with ADHD to prioritize. User feedback indicated a need for better organization based on when medications should be taken throughout the day.

## Decision

Redesign the dashboard to use a "Daily Stack" approach, grouping medications into specific time-slots:
- **Morning Focus**: Items scheduled before 12:00 PM or tagged as "morning".
- **Afternoon**: Items scheduled between 12:00 PM and 6:00 PM.
- **Evening Stack**: Items scheduled after 6:00 PM or tagged as "evening/bedtime".

### Implementation Detail
- Add `scheduledTime` to `StackItem` to allow precise organization.
- Implement filtering logic in `DailyStackViewModel` to provide separate lists for each time-slot.
- Use a dynamic greeting and progress tracking to improve engagement.

## Consequences

**Positive:**
- Reduced cognitive load for users by showing only what is relevant "now".
- Clearer visualization of daily progress.
- Foundation for time-based notification reliability checks (Late Dose Triage).

**Negative:**
- Requires reliable `scheduledTime` data fields.
- Additional complexity in the ViewModel for filtering and sorting.

## Alternatives Considered

| Option | Rejected Because |
|--------|------------------|
| Keep flat list | Failed to address user prioritization needs. |
| Automatic AI sorting | Overly complex for initial phase; manual scheduling is more predictable for medical adherence. |
