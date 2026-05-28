---
name: technical-architecture
description: Use this skill when you need comprehensive guidance on building a market intelligence dashboard using a hybrid stack of Airtable, n8n, and React/Next.js.
---

# Technical Architecture Skill for React/Next.js + n8n Dashboard Stack

## Purpose

This skill provides comprehensive technical architecture guidance for building market intelligence dashboards on a hybrid "low-code" stack: Airtable (data layer) + n8n (workflow automation) + React/Next.js (frontend). It prioritizes rapid development, maintainability, and real-time responsiveness.

## Data Layer (Airtable)

### Schema Design Principles

1. **Normalize for clarity, denormalize for performance**
   - Core entities in separate tables.
   - Pre-computed rollups for dashboard views.

2. **Use formula fields for derived values**
   - Computed at read time, always fresh.
   - Example: `Days Since Last Contact = DATETIME_DIFF(NOW(), {Last Contact Date}, 'days')`.

3. **Use views as "API endpoints"**
   - Create views for specific use cases.
   - Views handle filtering and sorting server-side.

4. **Linked records for relationships**
   - Contact → Organisation (many-to-one).
   - Lead → Organisation + Contact (many-to-one).

### Materialized Views Pattern

For dashboard performance, pre-compute aggregations:

**Why:**
- Formula fields compute on read (slow for complex queries).
- Rollups across large tables are expensive.
- Dashboard needs fast responses (<500ms).

**Implementation:**
- n8n workflow runs on schedule (e.g., hourly).
- Aggregates data from source tables.
- Writes to "dashboard" tables with pre-computed values.
- Frontend reads from materialized tables only.

```
Raw Tables                    Materialized Views
──────────────                ──────────────────
Forces           ────┐
Contacts         ────┼──▶ n8n ──▶  DailyScores
Interactions     ────┤              WeeklyTrends
JobPostings      ────┘              AlertFeed
```

## Frontend Architecture (Next.js 14)

### Why Next.js + shadcn/ui

| Feature | Benefit |
|---------|---------|
| App Router | Server Components, streaming, layouts |
| TypeScript | Type safety, better developer experience |
| Optimized Performance | Automatic code splitting, image optimization |

## Related Skills

- UK Police Design System Skill — For frontend component specifications.
- Action-Oriented UX Skill — For interaction patterns the architecture must support.
- Notification System Skill — For alert delivery infrastructure.
- ADHD Interface Design Skill — For performance requirements (sub-100ms).