# Tooling: schema snapshots, EXPLAIN, index checks

## Schema snapshot (Supabase local)
- Generate schema docs:
  - `make schema-docs`
  - `make schema-docs-check`

## EXPLAIN workflow
Use parameterized queries and verify indexes:
```sql
explain (analyze, buffers)
select *
from core.shows
where imdb_series_id = 'tt11363282';
```

## Index usage checks
```sql
select
  relname as table,
  indexrelname as index,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
from pg_stat_user_indexes
order by idx_scan desc;
```

## pg_stat_statements (if enabled)
```sql
select
  query,
  calls,
  total_exec_time,
  mean_exec_time
from pg_stat_statements
order by total_exec_time desc
limit 20;
```

## Verify Supabase API exposure
Ensure `core` is exposed in `supabase/config.toml`:
```toml
[api]
schemas = ["public", "graphql_public", "core"]
```
