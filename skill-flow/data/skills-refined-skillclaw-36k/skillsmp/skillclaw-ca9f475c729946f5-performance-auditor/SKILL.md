---
name: performance-auditor
description: Use this skill when you need to monitor and optimize performance across database, frontend, and AI systems, particularly for the KR92 Bible Voice project.
---

# Performance Auditor

Expert performance optimization for the KR92 Bible Voice project across database, frontend, and AI systems.

## Quick Start

Choose your performance concern:

- **Database performance**: Slow queries, missing indexes, sequential scans
- **React Query optimization**: Caching strategy, stale times, unnecessary refetches
- **AI performance**: Latency, costs, cache effectiveness
- **N+1 query detection**: Finding and fixing N+1 patterns
- **Complete performance audit**: Use the optimization checklist
- **Common gotchas**: Known issues and pitfalls

## Performance Targets

Reference targets for healthy performance:

| Operation | Target |
|-----------|--------|
| Single verse lookup | <20ms |
| Chapter load | <50ms |
| Text search | <100ms |
| AI translation | <500ms |
| Page load (FCP) | <1.5s |
| API response | <200ms |

## How to Use This Skill

1. Identify your performance issue (database, frontend, AI, or N+1).
2. Use the appropriate SQL scripts or code patterns provided below.
3. Check performance against the targets listed above.
4. Review common issues and solutions if results seem unexpected.

## Key Tools

- **Database analysis**: Use `EXPLAIN ANALYZE` to check query performance.
- **N+1 detection**: Identify N+1 patterns using provided detection scripts.
- **Cache optimization**: Review caching strategies for React Query.
- **AI monitoring**: Track latency and costs in AI usage logs.

## Usage Examples

### Example 1: Analyze Query Performance
```sql
-- Test single verse lookup performance
EXPLAIN ANALYZE
SELECT * FROM public.get_verse_by_ref(
  'John', 3, 16, 'finstlk201', 'fi'
);
```

### Example 2: Identify Missing Indexes
```sql
-- Check for sequential scans (potential missing indexes)
SELECT
  schemaname,
  tablename,
  seq_scan,
  CASE
    WHEN seq_scan > idx_scan THEN 'Consider index'
    ELSE 'OK'
  END as recommendation
FROM pg_stat_user_tables
WHERE schemaname IN ('public', 'bible_schema')
ORDER BY seq_scan DESC
LIMIT 20;
```