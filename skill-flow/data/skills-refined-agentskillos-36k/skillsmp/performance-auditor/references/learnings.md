# Performance Auditor Learnings

Common gotchas, anti-patterns, and corrections discovered through performance work.

## Gotchas

### seq_scan > idx_scan Doesn't Always Mean Missing Index
- **Pattern**: Query shows seq_scan=1000, idx_scan=10. Conclusion: Add index!
- **Wrong**: Immediately create index on scanned columns
- **Right**: Check table size first. Tables < 10k rows are faster with sequential scans
- **Why**: Small sequential scans (cache-friendly) beat index lookups (random I/O). PostgreSQL query planner usually makes the right choice.
- **Solution**: Validate with `EXPLAIN ANALYZE` before indexing. Look for "Seq Scan" in EXPLAIN output with high actual row counts.

### GIN Indexes Create False Positives
- **Pattern**: Full-text search suddenly uses 90% CPU after adding GIN index
- **Wrong**: Index is working, queries are just expensive
- **Right**: Check if query is using the index correctly with `EXPLAIN`
- **Why**: GIN indexes are large and slow on updates. Great for reads, terrible for write-heavy tables.
- **Solution**: Use GIN only on read-mostly tables. Don't use on rapidly-changing search content.

### React Query staleTime=0 Defeats Caching
- **Pattern**: Queries always refetch. Why is caching not working?
- **Wrong**: Increase gcTime
- **Right**: Understand that staleTime=0 means "always stale." Increase staleTime.
- **Why**: staleTime determines when data goes "stale"; stale queries refetch. gcTime just controls how long data stays in memory.
- **Solution**: Set staleTime based on how often data changes, not how long to keep in memory.

### N+1 Queries Hidden in Component Renders
- **Pattern**: Add 10 topics to page, 10 requests fire. Remove all topics, still 10 requests.
- **Wrong**: N+1 is coming from a loop
- **Right**: Check for multiple useQuery hooks in mapped components
- **Why**: `topics.map(t => <TopicCard key={t.id} />)` where TopicCard calls `useQuery(fetchTopicData)` creates N queries automatically.
- **Solution**: Load all data at parent level, pass down as props. Use query keys that include all IDs: `['topics', topicIds.sort().join(',')]`

### AI Cache Hit Rates Lie Without Warmup
- **Pattern**: Cache hit rate shows 20%. That's terrible!
- **Wrong**: Cache is broken or undersized
- **Right**: Data hasn't been populated yet. Need warmup queries first.
- **Why**: Cache hit rate only counts translations already in database. New features start at 0%.
- **Solution**: Run warmup queries on first deploy. Monitor cache hit rate after 1 week of traffic.

### Missing Indexes on Foreign Keys
- **Pattern**: Topics load slow, but no slow query detected
- **Wrong**: No bottleneck exists
- **Right**: Foreign key joins need indexes on the FK column
- **Why**: Filtering by `topic_id` in topic_verses join scans entire table without index
- **Solution**: Always add index on foreign key columns: `CREATE INDEX idx_topic_verses_topic_id ON topic_verses(topic_id);`

## Anti-Patterns

| Don't | Do Instead | Reason |
|-------|------------|--------|
| `refetchOnWindowFocus: true` globally | Set only for user-data queries | Refetches all queries when tab regains focus, causes jank |
| `staleTime: 0` for expensive queries | `staleTime: 5 * 60 * 1000` | Forces refetch every time component mounts, defeats caching |
| Load all data upfront in useEffect | Paginate or virtualize | Large data transfers kill initial load performance |
| Individual useQuery per item in array | Batch-load at parent level | Creates N+1 queries |
| `Promise.all()` with 50+ requests | Batch into groups of 5-10 | Overwhelms browser connection pool |
| Invalidate entire cache on mutation | `invalidateQueries({ queryKey: ['specific', 'key'] })` | Causes unnecessary refetches of unrelated queries |
| Monitor query performance with `console.time()` | Use React Query DevTools | Manual timing is unreliable and adds overhead |
| Add indexes to frequently queried strings | Check cardinality first | Low-cardinality string indexes (status='active') are ineffective |
| Cache AI results forever (staleTime: Infinity) | Cache only truly immutable data | AI models change; translations become outdated |

## Sticky Fixes

### EXPLAIN Output is Confusing
**Solution**: Focus on these columns only:
- Node Type: Seq Scan vs Index Scan (what access method)
- Rows: Estimated vs Actual (how far off is planner?)
- Planning Time: > 5ms suggests complex query
- Execution Time: Total time to run query

Ignore everything else until you understand these first.

### pgBouncer Connection Pool Exhaustion
**Solution**: Monitor connections:
```sql
SELECT count(*) FROM pg_stat_activity;  -- Should be < 20
```
If consistently high, increase `max_connections` or reduce query parallelism. Tune by reducing `staleTime` to reduce concurrent queries.

### React Query DevTools Hides Cache Issues
**Solution**: Monitor cache size manually:
```typescript
const cache = queryClient.getQueryCache();
const size = JSON.stringify(cache.getAll()).length / 1024;
console.log('Cache size:', size + 'MB');
```
If > 5MB, implement cache cleanup for older queries.

### AI Translation Costs Exploding
**Solution**: Check cache first:
```sql
SELECT source, COUNT(*) FROM term_translations
  WHERE source = 'ai' AND created_at > NOW() - INTERVAL '1 day'
  GROUP BY source;
```
If `source='ai'` is high, check for repeated requests. Add request deduplication layer.

### Slow Search Despite Index
**Solution**: Check if full-text search index is being used:
```sql
EXPLAIN ANALYZE SELECT * FROM verses WHERE to_tsvector('finnish', content) @@ to_tsquery('finnish', 'rakkaus');
```
If shows "Seq Scan" instead of "Index Scan using gin_index", index is configured wrong or query doesn't match index type.

### Premature Optimization False Positives
**Solution**: Measure first, then optimize:
1. Run EXPLAIN ANALYZE (shows if query is actually slow)
2. Check pg_stat_statements (shows if query runs frequently)
3. Only optimize if SLOW AND FREQUENT

Don't optimize queries that run once per week, even if theoretically slow.

## Performance Regression Prevention

Monitor these metrics continuously:

1. **API response time (p95)**: Should stay < 200ms
2. **Cache hit rate**: Should stay > 50% for cacheable queries
3. **Database connections**: Should stay < 20
4. **Largest queries**: Top 5 by execution time should be < 100ms each
5. **Error rate**: Should stay < 1%

Set alerts if any metric degrades by > 20% week-over-week.
