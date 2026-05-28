---
name: java-cache-redis
description: Redis caching playbook (cache-aside/read-through/write-through), TTL strategy, cache stampede protection, and invalidation/versioning. Produces cache key spec + invalidation strategy.
license: CC-BY-4.0
compatibility:
  jdk: "17+"
  cache: ["Redis"]
  serialization: ["JSON", "MsgPack", "Kryo (careful)", "Proto"]
metadata:
  owner: "backend-platform"
  version: "1.0"
  tags: ["java", "redis", "cache", "ttl", "stampede", "consistency", "invalidation"]
---

# java-cache-redis

## Intent

Introduce Redis caching safely with:

- predictable keys and TTLs,
- controlled consistency trade-offs,
- stampede (thundering herd) protection,
- observability and rollback switches.

This skill emphasizes “production correctness first, performance second”.

## When to use

- Latency optimization (read-heavy endpoints)
- DB offloading (high QPS reads)
- Expensive computations (aggregation, personalization, permissions snapshots)
- Stabilizing hot keys during spikes

## Scope

### In scope

- Cache-aside / read-through / write-through / write-behind patterns
- TTL strategy and jitter
- Cache stampede prevention: request coalescing, locks, probabilistic early refresh
- Key design: namespacing, versioning, multi-tenant safety
- Invalidation strategy: event-driven, time-based, version-based
- Metrics and failure handling (Redis down, partial failures)

### Out of scope

- Redis cluster topology design (ops topic)
- Persistent session storage and advanced Redis modules (separate skill)

## Golden rules

1. **Cache is an optimization layer**; correctness must not depend on it.
2. Every cached value must have:
   - a stable key spec,
   - an explicit TTL policy,
   - a fallback path (DB/source of truth),
   - a failure mode plan.
3. **Never cache “unbounded cardinality” keys** without quotas (risk: memory blow-up).
4. **Define consistency expectations** per use case (strong vs eventual).

## Pattern selection guide

### Pattern A — Cache-aside (recommended default)

Flow:

- Read: check cache -> miss -> load from DB -> populate cache -> return
- Write: write to DB -> invalidate cache (or update cache)

Pros:

- simple, explicit
- app controls data loading

Cons:

- stampede risk on misses
- invalidation complexity

### Pattern B — Read-through (cache loader)

Cache is responsible for loading on miss.
Pros: cleaner app code
Cons: harder to implement consistently in polyglot environments

### Pattern C — Write-through

Write to cache, cache writes synchronously to DB (or app writes both).
Pros: cache stays warm and consistent
Cons: higher write latency; write failures must be handled carefully

### Pattern D — Write-behind

Writes buffered and flushed asynchronously.
Pros: fast writes
Cons: risk of data loss; harder correctness model (use only when business allows)

## Key specification (mandatory)

Key format:

- {namespace}:{domain}:{version}:{tenant?}:{entityId}:{variant?}

Examples:

- cache:user:v3:12345
- cache:product:v2:tenantA:sku:ABC
- cache:search:v1:tenantA:qhash:9f2a...

Rules:

- Namespace must identify owning service/team
- Include a version segment to allow bulk invalidation by version bump
- Avoid raw PII in keys (hash if needed)
- Define max key length and allowed characters

## TTL strategy

### Choose TTL by data volatility

- Highly volatile: short TTL (seconds/minutes)
- Moderately volatile: medium TTL (minutes)
- Stable reference data: long TTL (hours/days) but still finite

### Add jitter to prevent synchronized expiry

- TTL = baseTTL +/- random(0..jitter)
This reduces coordinated cache misses (stampede).

### Consider negative caching

Cache “not found” for a short TTL to prevent repeated DB hits for missing keys.
Guardrail: keep TTL very small; ensure it won’t hide newly created data for long.

## Stampede (thundering herd) protection toolkit

### Option 1 — Request coalescing (singleflight)

- For the same key, only one in-flight loader hits DB
- Others wait (bounded) or serve stale value

### Option 2 — Distributed lock with bounded wait

- Acquire lock key with short TTL
- Loader populates cache, releases lock
- Others either wait briefly or fallback to stale/DB

Guardrails:

- lock TTL must be short
- avoid deadlocks by ensuring lock release is best-effort and TTL-based

### Option 3 — Serve stale while revalidate

- If cached value is near expiry, serve stale and refresh asynchronously
- Requires storing metadata (soft TTL vs hard TTL)

## Invalidation strategy (pick one primary)

### Strategy 1 — Time-based (TTL-only)

Use when: eventual consistency is acceptable and data changes are not critical.
Pros: simplest
Cons: stale reads until TTL expiry

### Strategy 2 — Explicit invalidation on writes (common)

On write to DB:

- delete cache key(s) affected
- optionally publish an event for cross-service invalidation

Pros: fresher reads
Cons: needs correct key mapping

### Strategy 3 — Version-based invalidation (bulk-safe)

- Keep a version token per domain/tenant
- Include version in derived keys
- On major changes, bump version token => old keys become unreachable

Pros: avoids scanning keys
Cons: requires strict key construction discipline

## Serialization choices (practical)

- JSON: debuggable, larger payload
- Proto/MsgPack: smaller, faster, requires schema discipline
Avoid:
- Java native serialization (security risk)
- Kryo without strict allowlist and versioning discipline

## Observability (must-have)

Metrics:

- cache_hit_total / cache_miss_total (by domain)
- cache_load_latency (timer/histogram)
- stampede_wait_count / lock_contention
- Redis error rate and fallback rate
Logs:
- on loader failure: key prefix + error category (no sensitive values)
Tracing:
- tag spans with cache.hit=true/false and loader path

## Failure handling (Redis is down / degraded)

- Fail open for read caches: fallback to DB (with rate limiting)
- Use circuit breaker/rate limiter around cache loader if Redis errors spike
- Protect DB: if cache collapses, throttle requests or degrade features

## Output artifacts

1) Cache key spec (namespaces, versions, examples)
2) TTL policy per domain
3) Stampede prevention plan (singleflight/lock/stale-while-revalidate)
4) Invalidation strategy (explicit/version-based)
5) Rollback switches (feature flag to disable cache writes/reads)

## Definition of Done (DoD)

- [ ] Key spec documented and code-enforced
- [ ] TTL + jitter defined per cache domain
- [ ] Stampede protection implemented for hot keys
- [ ] Invalidation strategy tested with write scenarios
- [ ] Metrics and dashboards added for hit ratio and fallback rate
- [ ] Safe fallback path exists and is load-tested (DB protection)

## Guardrails (What NOT to do)

- Do not cache unbounded keys (e.g., raw search queries) without hashing + quotas
- Do not cache sensitive data without encryption/strict access control policy
- Do not set “infinite TTL”
- Do not treat cache as the source of truth

## Cursor usage (recommended)

Attach:

- Redis client wrapper + cache abstraction
- The endpoints being optimized
- Current DB query profile (counts/latency)
Prompt snippet:
“Use java-cache-redis. Propose a cache-aside design with key spec, TTL+jitter, stampede protection, invalidation plan, and required metrics.”
