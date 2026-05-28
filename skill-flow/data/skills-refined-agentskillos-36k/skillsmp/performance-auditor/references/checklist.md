# Performance Optimization Checklist

Complete audit checklist for comprehensive performance review.

## Database Performance

- [ ] Indexes on all foreign keys (`user_id`, `verse_id`, etc.)
- [ ] Indexes on frequently filtered columns (`status`, `created_at`, `osis`)
- [ ] GIN indexes for full-text search columns
- [ ] Composite indexes for common multi-column WHERE clauses
- [ ] `VACUUM` and `ANALYZE` run regularly (at least weekly)
- [ ] Connection pooling configured (pgBouncer or Supabase default)
- [ ] Query plan reviewed with `EXPLAIN ANALYZE` for slow queries
- [ ] No sequential scans on large tables
- [ ] Index cardinality appropriate (not too many, not too few)
- [ ] Partitioning strategy for large tables (if >100M rows)

## React Query Configuration

- [ ] Appropriate `staleTime` set for each query type
  - Bible content (static): 30 min
  - User data (mutable): 1-5 min
  - AI results (expensive): Infinity
- [ ] `gcTime` (cache time) > `staleTime` to maintain in memory
- [ ] `refetchOnWindowFocus: false` unless data is highly volatile
- [ ] `refetchOnMount: false` unless data is critical
- [ ] Mutations invalidate appropriate queries with `onSuccess`
- [ ] No N+1 query patterns
- [ ] Cache size monitored (< 5MB in most cases)
- [ ] Prefetching implemented for predictable navigation
- [ ] No redundant query keys (same data with different keys)

## React Component Performance

- [ ] Code splitting for routes (lazy loading)
- [ ] Heavy components memoized with `React.memo()`
- [ ] Expensive computations wrapped in `useMemo()`
- [ ] Event handlers wrapped in `useCallback()` when passed to memo'd children
- [ ] No unnecessary re-renders detected in React DevTools Profiler
- [ ] Virtual scrolling for lists > 100 items
- [ ] Image optimization (lazy loading, appropriate formats)
- [ ] Debouncing on search/filter inputs
- [ ] Service worker for offline support and caching

## AI Performance

- [ ] Caching enabled for translation results
- [ ] Cache hit rate monitored (target: >50% for translations)
- [ ] Appropriate model selection per use case
  - Simple queries: Claude Haiku
  - Complex reasoning: Claude Opus
- [ ] Token limits set to prevent runaway requests
- [ ] Timeout handling with exponential backoff
- [ ] Retry logic implemented for failed calls
- [ ] Batch processing used where possible
- [ ] Cost monitored per feature

## API and Network

- [ ] API responses < 200ms baseline
- [ ] Gzip compression enabled
- [ ] CDN used for static assets
- [ ] HTTP caching headers set appropriately
- [ ] Database query time < 50% of total response time
- [ ] No unnecessary data in API responses (GraphQL query optimization)
- [ ] Pagination implemented for large result sets
- [ ] Rate limiting configured

## Monitoring and Observability

- [ ] `pg_stat_statements` enabled for slow query tracking
- [ ] Performance budget defined and monitored
- [ ] Core Web Vitals monitored (LCP, FID, CLS)
- [ ] Error rates tracked (target: < 1%)
- [ ] Request latency tracked by endpoint
- [ ] Database CPU and connection count monitored
- [ ] AI call costs tracked daily

## Database Schema

- [ ] Primary keys on all tables
- [ ] Foreign keys with appropriate constraints
- [ ] Column types optimized (not oversized)
- [ ] Enum types used instead of string columns where appropriate
- [ ] Nullable columns minimized
- [ ] Comments documenting unusual design decisions

## Testing

- [ ] Performance regression tests written
- [ ] Load testing for critical paths (chapter load, search)
- [ ] Database performance tests with realistic data volumes
- [ ] React Query cache behavior tested

## Quick Win Opportunities

Priority items if you have limited time:

1. **Most impact**: Fix N+1 queries (often 10x improvement)
2. **High impact**: Add missing indexes (2-5x improvement)
3. **High impact**: Optimize React Query staleTime (30-50% fewer requests)
4. **Medium impact**: Implement code splitting (10-20% faster page load)
5. **Medium impact**: Cache AI results (eliminate expensive re-calls)

## Monitoring Commands

Keep these queries handy for quick diagnostics:

```sql
-- Quick overview (run these first)
SELECT schemaname, tablename, seq_scan, idx_scan
  FROM pg_stat_user_tables WHERE seq_scan > idx_scan
  ORDER BY seq_scan DESC LIMIT 10;

-- Slowest queries
SELECT query, calls, ROUND(mean_exec_time::numeric, 2) as mean_time_ms
  FROM pg_stat_statements WHERE query NOT LIKE '%pg_stat%'
  ORDER BY mean_exec_time DESC LIMIT 10;

-- Unused indexes
SELECT schemaname, tablename, indexname, idx_scan
  FROM pg_stat_user_indexes WHERE idx_scan = 0
  AND indexname NOT LIKE '%_pkey' ORDER BY created DESC;
```
