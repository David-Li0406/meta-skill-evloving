# Architecture + Scalability Playbooks

## Normalization vs denormalization
- Normalize when:
  - Many write paths, strong consistency needed.
  - Multiple entities share the same attributes.
  - Updates must be atomic across related rows.
- Denormalize when:
  - Read paths dominate and joins are hot.
  - You can tolerate eventual consistency for derived fields.
  - You can rebuild derived data (batch or async).

## Consistency patterns
- Strong consistency: prefer transactions, FK constraints, and row locks for critical updates.
- Eventual consistency: use derived caches or materialized views with refresh strategy.
- Avoid anomalies by keeping a single source of truth and explicit backfill jobs.

## Transactionality and locking
- Default isolation: read committed; avoid long-running transactions.
- Use explicit transactions for multi-row invariants.
- Avoid `SELECT ... FOR UPDATE` unless necessary; keep locked sections short.
- Prefer idempotent migrations and resumable backfills.

## CAP considerations (TRR context)
- Postgres/Supabase is CP for most operations.
- Add Redis cache only when read latency dominates and staleness is acceptable.
- Add search (OpenSearch/Elasticsearch) only for complex text queries or relevance ranking.
- Time series: use native partitioning first; consider Timescale only for high-ingest metrics.

## Multi-tenant patterns
- Single schema + tenant_id + RLS (default): easiest and aligns with Supabase.
- Schema-per-tenant: only if tenant isolation is strict and counts are small.
- Shared tables + RLS: use for TRR if org/team features expand.

## Index strategy
- Btree: equality and ordering.
- Composite: (tenant_id, created_at) for tenant-scoped feeds.
- Partial: only active rows.
- GIN: JSONB and full-text.
- BRIN: large append-only tables.

## Common performance antipatterns
- N+1 queries in API handlers.
- Missing indexes on FK or frequently-filtered columns.
- Unbounded scans without pagination.
- JSONB filtering without GIN indexes.
- Large updates in a single transaction.

## Partitioning decision
- Time-based: if table grows unbounded and queries are time-sliced.
- Hash: if tenant_id is the main filter and hot tenants exist.
- Prefer native partitioning before Timescale unless metrics justify.

## Zero-downtime migrations
- Add columns first, default NULL.
- Backfill in batches.
- Dual-write if changing semantics.
- Flip reads to new columns.
- Make columns NOT NULL later.
- Use `CREATE INDEX CONCURRENTLY` for large tables.

## Read scaling + caching
- Read replicas for analytics-heavy workloads; keep writes on primary.
- Redis for hot reads or rate-limited endpoints; set TTL and invalidate on writes.
- Batch queries and avoid N+1 in API handlers.

## Connection pooling
- Use PgBouncer in transaction mode for high-concurrency APIs.
- Avoid long transactions to keep pool healthy.

## Monitoring + alerting
- Use `pg_stat_statements` to find slow queries and high total time.
- Track: p95 query latency, connection count, deadlocks, index bloat.
- Alert thresholds (starter):
  - p95 > 300ms for hot endpoints
  - lock waits > 1s
  - connections > 80% of pool

## Backup/DR
- Define RPO/RTO and test restores.
- Use PITR if data loss risk is high.
- Document rollback steps for each migration.

## Compliance + data lifecycle
- Support GDPR deletion/anonymization (soft delete + hard purge workflows).
- Log audit trails for sensitive writes.
- Track data lineage for derived tables and materialized views.
