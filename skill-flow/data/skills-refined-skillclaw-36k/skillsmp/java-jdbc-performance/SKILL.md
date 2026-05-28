---
name: java-jdbc-performance
description: JDBC performance playbook: connection pool sanity, batching, fetch size, statement tuning, and measurement. Produces measurable changes + benchmark guidance.
license: CC-BY-4.0
compatibility:
  jdk: "17+"
  drivers: ["PostgreSQL JDBC", "MySQL Connector/J", "SQL Server JDBC", "Oracle JDBC"]
  pools: ["HikariCP"]
metadata:
  owner: "backend-platform"
  version: "1.0"
  tags: ["java", "jdbc", "performance", "hikaricp", "batching", "fetch-size", "pooling"]
---

# java-jdbc-performance

## Intent

Improve database interaction performance by reducing:

- network round-trips,
- per-statement overhead,
- connection churn,
- inefficient result fetching,
while ensuring changes are measurable and regression-safe.

## When to use

- Slow queries at the application layer (even when DB looks okay)
- High DB CPU due to too many small queries
- Thread pool saturation caused by DB waits
- Connection pool exhaustion or timeouts
- Large result sets causing memory spikes or long tail latency

## Scope

### In scope

- Connection pool configuration sanity (HikariCP)
- PreparedStatement usage, batching, fetch size
- Transaction scope and autocommit implications
- Read streaming patterns for large result sets
- Basic measurement and before/after benchmarking guidance

### Out of scope

- Schema/index/query-plan design (belongs to DB optimization + migrations skill)
- ORM-level fetch shaping (see java-jpa-transaction-patterns)

## Step 0 — Baseline measurement (no tuning without data)

Collect:

- p50/p95/p99 latency per endpoint
- DB time vs CPU time (if you have tracing/metrics)
- Connection pool metrics: active, idle, pending threads
- Query counts and average statement duration
- Error counters: timeouts, transient failures, deadlocks

Minimal reproducible benchmark:

- A single representative operation loop (N requests) with stable input data
- Warm-up phase + measurement phase
- Record:
  - throughput (ops/s)
  - latency distribution
  - CPU usage
  - GC metrics

## Step 1 — Connection pool sanity (HikariCP baseline)

Goals:

- avoid too-small pools causing queueing,
- avoid too-large pools causing DB overload,
- ensure lifecycle settings prevent stale connections.

Baseline rules:

- maxPoolSize should align with DB capacity and app concurrency (not “CPU cores * 2” blindly)
- set maxLifetime < DB idle timeout to avoid broken connections
- prefer explicit connectionTimeout to fail fast under saturation
- keep idleTimeout reasonable to avoid churn
- use leakDetectionThreshold only for debugging (it adds overhead)

## Step 2 — Reduce per-query overhead

### Use PreparedStatement for repeated queries

- ensures server-side plan caching (varies by DB)
- avoids SQL string concatenation and injection risks

### Avoid SELECT *

- fetch only needed columns
- reduces IO and object mapping overhead

### Use server-side pagination for lists

- LIMIT/OFFSET (or keyset pagination for deep paging)
- never pull massive lists into memory

## Step 3 — Batching writes (massive throughput gains)

Use batching for:

- insert/update of many rows
- bulk status updates
- event/outbox inserts

Guidelines:

- choose batch size (e.g., 100–1000) based on row width and DB
- wrap batch in explicit transaction (autocommit off)
- use addBatch/executeBatch
- handle partial failures and retry carefully (idempotency keys where needed)

Example skeleton (JDBC):

- conn.setAutoCommit(false)
- PreparedStatement ps = conn.prepareStatement(...)
- loop:
    ps.addBatch()
    if (i % batchSize == 0) ps.executeBatch()
- ps.executeBatch()
- conn.commit()

## Step 4 — Fetch size and streaming reads

Large result sets:

- default behavior often fetches too much into memory
- configure fetch size and use forward-only ResultSet if supported

Guidelines:

- setFetchSize(N) on Statement/PreparedStatement
- for streaming:
  - use forward-only, read-only ResultSet
  - keep transaction open only as needed
  - avoid mapping entire result set into a list; process row-by-row

Important:

- some drivers require autocommit=false for cursor-based fetching
- verify driver-specific behavior before assuming streaming

## Step 5 — Transaction and autocommit semantics

- Autocommit=true means each statement is its own transaction
  - adds commit overhead
  - may defeat cursor streaming in some drivers
- For batch writes and streaming reads:
  - set autocommit=false
  - commit explicitly

## Step 6 — Network and timeouts

- set query timeout where appropriate
- ensure socket/read timeouts are configured at driver or datasource level
- treat timeouts as signals: don’t just increase them; reduce load and improve queries

## Verification and safety checks

- Validate correctness:
  - row counts
  - idempotency for retries
- Validate resource usage:
  - memory remains stable in streaming operations
  - connection pool does not get pinned by long transactions
- Validate observability:
  - metrics show reduced query counts or reduced DB time

## Output artifacts

- A short “Performance Change Log”:
  - baseline metrics
  - changes applied (pool/batch/fetch)
  - after metrics
- Code diffs: datasource config + JDBC call sites
- A benchmark snippet or reproducible load script

## Definition of Done (DoD)

- [ ] Baseline and after numbers recorded (latency + throughput + pool metrics)
- [ ] Connection pool settings reviewed against DB timeouts
- [ ] Batching enabled where appropriate and tested
- [ ] Fetch size/streaming approach validated with driver behavior
- [ ] Regression tests added for correctness (especially around batching)
- [ ] Rollback path defined (config toggles / feature flags)

## Guardrails (What NOT to do)

- Do not increase pool size blindly; you can DDoS your own DB
- Do not batch with autocommit=true and expect real gains
- Do not stream huge results while also doing slow per-row processing in the same transaction
- Do not “optimize” without recording baseline and after metrics

## Cursor usage (recommended)

Attach:

- DataSource config (Hikari)
- JDBC call sites (DAO/repository)
- Production symptoms: pool metrics, timeouts, p95/p99 graphs
Prompt snippet:
“Use java-jdbc-performance. Propose measurable improvements (pool + batching + fetch size). Provide a micro-benchmark plan and regression tests.”
