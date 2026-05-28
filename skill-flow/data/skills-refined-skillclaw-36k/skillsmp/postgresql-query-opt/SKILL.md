---
name: postgresql-query-opt
description: Query optimization, EXPLAIN analysis, and indexing strategies for PostgreSQL.
---

# PostgreSQL Query & Optimization

## When to use this skill
- Debugging slow queries.
- Designing indexes for new schemas.
- Analyzing `EXPLAIN` output.
- Writing complex CTEs or recursive queries.

## 1. Indexing Strategy
- **B-Tree**: Default. Good for equality and range (`<`, `<=`, `=`, etc.).
- **GIN**: Essential for `jsonb`, `array`, and full-text search (`tsvector`).
- **Partial Indexes**: Use `WHERE` clause in index definition to save space (e.g., `WHERE is_active = true`).
- **Covering Indexes**: Use `INCLUDE` to store extra payload columns in the index leaf nodes (avoids heap lookup).

## 2. Query Patterns
- **CTEs**: Use Common Table Expressions (`WITH`) for readability. Note: Postgres >= 12 optimizes them well (materialization boundary is smarter).
- **EXPLAIN**: Always run `EXPLAIN (ANALYZE, BUFFERS)` to see actual execution times and I/O costs.
- **Nulls**: Be aware of `NOT IN (...)` with nulls (can yield unexpected results); prefer `NOT EXISTS`.

## 3. Performance Pitfalls
- **Seq Scans**: Acceptable for small tables; bad for large ones.
- **N+1**: Detecting N+1 queries in application layers.
- **Functions in WHERE**: Avoid `WHERE function(column) = val`; this kills index usage. Use expression indexes if needed.
