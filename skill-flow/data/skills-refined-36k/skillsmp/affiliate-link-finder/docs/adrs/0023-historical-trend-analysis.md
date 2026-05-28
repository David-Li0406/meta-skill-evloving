# ADR 0023: Historical Trend Analysis Logic

**Date:** 2026-01-20  
**Status:** Accepted  
**Deciders:** Development Team

## Context

The "Insights" and "Weekly Review" screens previously relied on dummy data or simplistic "current week" averages. To provide real value, the app needed to show relative improvement or decline compared to historical baselines.

## Decision

Implement a **14-day Rolling Baseline** for trend analysis.

Calculation Logic:
1. **Current Stats**: Mean of data from the last 7 days.
2. **Baseline Stats**: Mean of data from the preceding 7 days (days 8-14).
3. **Trend**: Percentage delta between (1) and (2).
4. **Focus Correlation**: Comparison of consistency percentages against focus score trends within the same window.

## Rationale
- **Clinical Relevance**: Weekly comparison is a standard rhythm for monitoring medication changes.
- **Actionable Insights**: Telling a user "Your focus is up 5% compared to last week" is more motivating than "Your focus is 7.2 today".
- **Data Integrity**: Using 14 days of data ensures that a single "bad day" doesn't skew the trend disproportionately.

## Consequences

**Positive:**
- Users can see the actual impact of their supplement stack over time.
- Standardizes the math across `WeeklyReviewViewModel` and `SuccessStatsViewModel`.

**Negative:**
- Requires the user to have at least 8-14 days of data before trends become meaningful.
- Performance impact when calculating across 100+ logs (mitigated by Repository-level aggregation).

## Alternatives Considered

| Option | Rejected Because |
|--------|------------------|
| Month-over-Month | Too long a feedback loop for ADHD users; trends would be stale by the time they show up. |
| Lifetime Average | Doesn't account for recent stack changes or life stress; irrelevant for short-term adjustments. |
| Raw Data Only | High cognitive load for the user to interpret their own charts. |
