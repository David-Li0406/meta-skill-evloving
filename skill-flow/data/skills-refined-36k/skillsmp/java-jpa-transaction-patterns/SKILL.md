---
name: java-jpa-transaction-patterns
description: Transaction boundary and JPA/Hibernate usage patterns to prevent data bugs and performance issues (lazy loading pitfalls, N+1, locking). Includes checklists, code patterns, and regression tests.
license: CC-BY-4.0
compatibility:
  jdk: "17+"
  persistence: ["Jakarta Persistence (JPA)", "Hibernate ORM"]
  runtime: ["Spring", "Jakarta EE", "Quarkus", "Micronaut", "Plain Java"]
metadata:
  owner: "backend-platform"
  version: "1.0"
  tags: ["java", "jpa", "hibernate", "transactions", "locking", "n+1", "lazy-loading"]
---

# java-jpa-transaction-patterns

## Intent

Standardize how transactions and persistence contexts are used so that:

- correctness is preserved under concurrency,
- performance is predictable (no hidden N+1 / lazy traps),
- locking is explicit and safe.

This skill is framework-agnostic: it applies whether you use Spring @Transactional, JTA, or programmatic EntityTransaction.

## Scope

### In scope

- Transaction demarcation: where and how to start/commit/rollback
- Persistence context boundaries and flush behavior
- Lazy loading pitfalls and safe fetch patterns
- Locking strategies: optimistic vs pessimistic
- N+1 detection and elimination
- Regression tests for typical data bugs (lost updates, stale reads, deadlocks)

### Out of scope

- Database-specific query tuning beyond JPA (see java-jdbc-performance for that)
- Complex CQRS/event-sourcing modeling decisions

## When to use

- You see LazyInitializationException / “session is closed”
- Random data inconsistencies under concurrent updates
- Slow endpoints due to N+1 queries
- Deadlocks or lock timeouts
- “It works locally but fails under load” data-access issues

## Key mental models

### 1) Transaction boundary defines correctness

A transaction is the unit of atomicity and isolation. If your business operation spans multiple SQL statements, the *boundary* must match the operation.

Rule of thumb:

- If multiple writes must succeed/fail together -> same transaction.
- If read-your-writes consistency matters -> same transaction.
- If you call external services -> avoid holding DB transaction open while waiting.

### 2) Persistence context is not “a cache you can ignore”

The EntityManager persistence context:

- tracks entity state (managed/detached),
- delays SQL until flush/commit,
- can hide extra queries via lazy loads.

If you don’t control the boundary, you don’t control SQL or locks.

### 3) Lazy loading is a feature, not a surprise

Lazy loading is safe only when:

- the persistence context is still open, AND
- you understand how many lazy associations will be accessed.

Default stance:

- avoid relying on lazy loads across layers
- decide fetch shape explicitly per use case

## Standard architecture boundary

- Controller/Resource: request mapping + input validation only
- Service (application layer): transaction boundary and orchestration
- Repository/DAO: data access primitives (queries) only

Transaction boundary belongs in the Service layer by default.

## Transaction patterns (with examples)

### Pattern A — Single service-level transaction

Use when: typical CRUD or business operations requiring atomicity.

Spring-style:

- @Transactional on service method

Jakarta EE / plain JPA style:

- begin/commit around the service method

Guidelines:

- Keep transactions short
- Don’t do network calls inside transaction
- Prefer explicit exception mapping and rollback rules

### Pattern B — Read-only transaction (still useful)

Use when: you need consistent reads and controlled fetch behavior.

Guidelines:

- Mark read-only where supported
- Avoid accidental flush (no entity mutation)
- Use projections/DTO queries for large graphs

### Pattern C — Two-phase workflow: DB transaction + external call

Use when: you must call external services.
Approach:

1) Transaction 1: write “intent” and commit (e.g., outbox/event record)
2) External call out of band
3) Transaction 2: finalize state based on response

This reduces lock hold time and improves resilience.

## Lazy loading pitfalls & solutions

### Pitfall 1 — Open Session In View (OSIV) hides bugs

If the session remains open into the web layer, lazy loads happen “wherever,” producing unpredictable query counts.

Default recommendation:

- disable OSIV (or equivalent) for APIs
- shape data explicitly in repository layer

### Pitfall 2 — Serialization triggers lazy loads

JSON serialization of entities can trigger lazy loads, causing N+1 and leaking internal relationships.

Solutions:

- never expose entities directly in API responses
- map to DTOs
- use explicit fetch joins or projections

## N+1 query elimination toolkit (choose the smallest hammer)

### Option 1 — DTO projection query (preferred for read APIs)

- Query only fields you need into a DTO
- Avoid loading entire entity graphs
Benefits: minimal SQL, stable performance.

### Option 2 — Fetch join for a known bounded relationship

- Use join fetch for specific association(s)
Guardrail: join fetching multiple collections can explode result sets.

### Option 3 — Batch fetching (ORM-level)

Use when: you need to traverse lazily, but want fewer round-trips.

- Hibernate batch fetching / @BatchSize reduces N+1 by grouping loads.

### Option 4 — EntityGraph (JPA)

Use when: you need flexible per-use-case fetch plans without rewriting queries.

## Locking: explicit decision-making

### Default: optimistic locking with @Version

Use when: conflicts are rare.

- Adds version column
- Detects lost updates
- On conflict: retry or return 409 (Conflict) depending on API semantics

### Pessimistic locking (SELECT ... FOR UPDATE semantics)

Use when: you must prevent concurrent modifications and conflicts are common.
Risks:

- deadlocks under different lock ordering
- throughput reduction

Guidelines:

- keep locked section minimal
- lock in a consistent order (by primary key)
- set lock timeouts where supported
- prefer “skip locked” patterns only if business semantics allow

## Flush/clear strategy (performance and correctness)

- Avoid calling flush too often; it increases lock time and IO
- In batch writes:
  - flush and clear periodically to avoid memory bloat
  - use JDBC batching if supported (see java-jdbc-performance)

## Checklist: Transaction boundary

- [ ] Does the service method represent a single business operation?
- [ ] Are you holding a transaction while waiting on network IO? (avoid)
- [ ] Are exceptions mapped to rollback correctly?
- [ ] Do you rely on OSIV/lazy loads in controller/serialization? (avoid)
- [ ] Are write operations idempotent where required?

## Checklist: N+1

- [ ] Enable SQL logging in test or use datasource proxy
- [ ] Write a regression test that asserts query count for hot endpoints
- [ ] Prefer DTO projections for list endpoints
- [ ] Use batch fetching or entity graphs for bounded traversals

## Regression tests (minimum set)

1) Lost update test:
   - two concurrent transactions update same row -> version conflict expected (optimistic)
2) Deadlock/lock timeout test (if you use pessimistic locks)
3) Query count test (prevent N+1 regressions)
4) Lazy initialization test:
   - ensure service returns DTO and does not leak entity graph

## Definition of Done (DoD)

- [ ] Transaction boundary resides at service layer (or justified otherwise)
- [ ] API responses are DTOs (no entity serialization)
- [ ] Locking strategy documented per write-critical workflow
- [ ] N+1 risk assessed and mitigated (projection/fetch/batch/entity graph)
- [ ] Regression tests added for bug class being fixed

## Guardrails (What NOT to do)

- Do not expose JPA entities directly in API responses
- Do not rely on OSIV to “make lazy loading work”
- Do not add pessimistic locks by default without measuring deadlock risk
- Do not keep transactions open across network calls

## Cursor usage (recommended)

Minimal context:

- Entities + repositories for the feature
- Service methods that orchestrate writes
- SQL logs / query plan hints (if available)
Prompt snippet:
“Use java-jpa-transaction-patterns. Identify transaction boundaries and N+1 risks. Propose DTO/projection or fetch plan. Recommend locking mode and add regression tests.”
