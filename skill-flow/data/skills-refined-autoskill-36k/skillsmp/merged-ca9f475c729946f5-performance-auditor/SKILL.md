---
name: performance-auditor
description: Use this skill when monitoring and optimizing performance across database, frontend, and AI systems, including analyzing query performance, optimizing indexes, and identifying N+1 queries.
---

# Performance Auditor

Expert performance optimization for applications across database, frontend, and AI systems.

## Quick Start

Choose your performance concern:

- **Database performance**: Slow queries, missing indexes, sequential scans
- **React Query optimization**: Caching strategy, stale times, unnecessary refetches
- **AI performance**: Latency, costs, cache effectiveness
- **N+1 query detection**: Finding and fixing N+1 patterns
- **Optimization checklist**: Complete performance audit
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
2. Review the relevant performance targets and strategies.
3. Run SQL scripts or code patterns as needed.
4. Check for unexpected results and common pitfalls.

## Key Tools

- **Database analysis**: Analyze query performance and suggest index improvements.
- **N+1 detection**: Identify and resolve N+1 query issues.
- **Cache optimization**: Review React Query usage for optimal caching.
- **AI monitoring**: Track latency and costs of AI calls.

## Usage Examples

### Analyze Query Performance
```sql
-- Test single verse lookup performance
EXPLAIN ANALYZE
SELECT * FROM public.get_verse_by_ref('John', 3, 16, 'finstlk201', 'fi');

-- Check execution time statistics
SELECT
  query,
  calls,
  total_exec_time,
  mean_exec_time,
  max_exec_time
FROM pg_stat_statements
WHERE query LIKE '%get_verse_by_ref%'
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Identify Missing Indexes
```sql
-- Check for sequential scans (potential missing indexes)
SELECT
  schemaname,
  tablename,
  seq_scan,
  idx_scan,
  CASE
    WHEN seq_scan > idx_scan THEN 'Consider index'
    ELSE 'OK'
  END as recommendation
FROM pg_stat_user_tables
WHERE schemaname IN ('public', 'bible_schema')
ORDER BY seq_scan DESC
LIMIT 20;
```

### Monitor AI Call Performance
```sql
-- AI performance metrics (last 7 days)
SELECT
  feature,
  ai_vendor,
  COUNT(*) as call_count,
  ROUND(AVG(latency_ms), 2) as avg_latency_ms,
  ROUND(SUM(cost_usd), 4) as total_cost_usd
FROM bible_schema.ai_usage_logs
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY feature, ai_vendor
ORDER BY call_count DESC;
```

### Optimize React Query Usage
```typescript
// Recommended React Query configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes
      retry: 1,
      refetchOnWindowFocus: false,
      refetchOnMount: false,
    },
  },
});
```

### Identify N+1 Query Problems
```typescript
// Common N+1 patterns to avoid
const { data: topics } = useQuery(['topics'], fetchTopics);
topics?.forEach(topic => {
  const { data: verses } = useQuery(['verses', topic.id], () => fetchTopicVerses(topic.id)); // N queries!
});
```

## Performance Optimization Checklist

### Database
- [ ] Indexes on foreign keys
- [ ] Regular VACUUM and ANALYZE

### React Query
- [ ] Appropriate staleTime for each query type
- [ ] No unnecessary refetches

### AI Calls
- [ ] Caching enabled for translations
- [ ] Appropriate model selection

### Frontend
- [ ] Code splitting for routes
- [ ] Image optimization

## Monitoring Tools

### Supabase Dashboard
- Database → Performance
- Edge Functions → Logs

### Browser DevTools
```javascript
// Measure page load performance
window.addEventListener('load', () => {
  const perfData = performance.getEntriesByType('navigation')[0];
  console.log('Page Performance:', {
    domContentLoaded: perfData.domContentLoadedEventEnd - perfData.fetchStart,
    loadComplete: perfData.loadEventEnd - perfData.fetchStart,
  });
});
```

## Related Documentation
- See `Docs/02-DESIGN.md` for architecture
- See `Docs/05-DEV.md` for query patterns
- See `Docs/06-AI-ARCHITECTURE.md` for AI optimization