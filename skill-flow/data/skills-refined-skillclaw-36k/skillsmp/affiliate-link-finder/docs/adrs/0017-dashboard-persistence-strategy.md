# ADR 0017: Dashboard Persistence Strategy

**Date:** 2026-01-19  
**Status:** Accepted  
**Deciders:** Development Team

## Context

The redesigned dashboard requires real-time tracking of medication intake and historical data for streak calculations. We needed to decide whether to create a new persistence model or leverage existing infrastructure.

## Decision

Reuse the existing `DailyLog` entity and `LogRepository` to track dashboard interactions.

### Rationale
- **Consistency**: Analytics and Trends already use `DailyLog`.
- **Performance**: Avoids creating redundant database queries and synchronization logic.
- **Simplicity**: `LogEntry` already supports `supplementId`, `taken`, and `takenAt` timestamps, which are sufficient for current and upcoming features like completion tracking.

## Consequences

**Positive:**
- Zero migration cost for existing users' data.
- Built-in support for streak calculation via `LogRepository.getStreakCount`.
- Simplified state updates in `DailyStackViewModel`.

**Negative:**
- `DailyLog` remains a large JSON blob in Firestore; future growth may require flattening if performance degrades.

## Alternatives Considered

| Option | Rejected Because |
|--------|------------------|
| New `MedicationLog` entity | Redundant; would require syncing data between two logs for accurate analytics. |
| Local-only state | Doesn't support cross-device sync or long-term trend analysis. |
