---
name: java-rest-clients-resilience
description: Resilient HTTP client playbook: timeouts, retries/backoff+jitter, circuit breakers, bulkheads, and idempotency keys. Produces resilience config + retry matrix and verification tests.
license: CC-BY-4.0
compatibility:
  jdk: "17+"
  clients: ["JDK HttpClient", "OkHttp", "Apache HttpClient"]
  resilience: ["Resilience4j (recommended)", "Custom minimal wrappers"]
metadata:
  owner: "backend-platform"
  version: "1.0"
  tags: ["java", "http", "resilience", "timeouts", "retries", "circuit-breaker", "bulkhead", "idempotency"]
---

# java-rest-clients-resilience

## Intent

Make outbound HTTP calls predictable under partial failure by standardizing:

- timeout budgeting,
- retry policy (only when safe),
- circuit breaker + bulkhead isolation,
- idempotency and deduplication,
- observability and safe fallbacks.

## When to use

- Upstream is flaky or slow; cascading failures appear
- Microservices latency debugging: “which dependency is causing p99?”
- You need safe retries and consistent client behavior across services
- Incident response: timeouts and retries are inconsistent across codebase

## Core principles

1. **Timeouts are not optional.**
2. **Retries are a controlled tool, not a default.**
3. **Prefer failing fast + graceful degradation over queueing forever.**
4. **Idempotency must be explicit** for any operation that might be retried.
5. **Isolation prevents blast radius** (bulkheads + circuit breakers).

## Step 0 — Dependency classification (required)

For each upstream endpoint, classify:

- Criticality: critical / important / best-effort
- Expected latency: p50/p95/p99
- Error modes: timeouts, 5xx, 429, connection resets
- Idempotency: safe to retry? (yes/no/only with idempotency key)
- Capacity constraints: rate limits, QPS caps
- Fallback option: cached data, default response, partial features

## Step 1 — Timeout budgeting (the backbone)

Set explicit budgets:

- connect timeout (TCP/TLS establishment)
- request timeout / overall deadline
- read timeout (if client supports separate)
- per-attempt timeout vs total timeout

Rule:

- Total timeout must be < caller’s own deadline / budget.
- In multi-hop calls, budgets must shrink each hop.

Recommended structure:

- totalDeadline = 800ms
- maxAttempts = 2
- perAttemptTimeout = 300ms
- remainingBudget reserved for local processing

## Step 2 — Retry policy (safe-by-default)

Retry only when:

- the operation is idempotent, OR
- you have an idempotency key + server dedup support.

Never retry blindly on:

- validation errors (4xx except 429/408 depending on semantics)
- non-idempotent operations without idempotency keys

Backoff:

- exponential backoff with jitter
- respect Retry-After when provided (429/503 patterns)

Bound retries:

- max attempts (2–3 typical)
- max elapsed time (stop when budget is exhausted)

## Step 3 — Circuit breaker (stop the bleeding)

Use when:

- repeated failures indicate upstream is unhealthy
- retries would amplify load and worsen outage

Circuit breaker parameters (conceptual):

- sliding window size
- failure rate threshold
- slow call threshold
- open state duration
- half-open permitted calls

Behavior:

- Open: fail fast (or fallback)
- Half-open: probe carefully

## Step 4 — Bulkhead isolation (contain blast radius)

Goal: one slow dependency must not exhaust all threads/CPU.

Choose bulkhead type:

- Semaphore bulkhead: limit concurrent calls (lightweight)
- Thread-pool bulkhead: isolate blocking calls in dedicated pool (heavier, strong isolation)

Guidelines:

- limit concurrency per upstream
- separate pools for “critical” vs “best-effort” dependencies
- set queue sizes carefully; prefer rejection over unbounded queues

## Step 5 — Idempotency keys (for safe retries on non-idempotent ops)

For POST/PUT operations that may create/charge/side-effect:

- generate Idempotency-Key (UUID) per logical request
- store/propagate it across retries
- server must deduplicate by (clientId, idempotencyKey) for a time window
- return the same result on duplicate requests

If you cannot implement server-side dedup:

- do NOT retry non-idempotent requests
- consider outbox pattern or explicit request tokens

## Step 6 — Fallbacks and degradation

Fallback types:

- cached response (stale-while-revalidate)
- partial response (omit optional sections)
- default value with warning flag
- queue for asynchronous processing (if business allows)

Guardrails:

- fallback must be observable (metrics/logs)
- do not hide persistent outages silently

## Step 7 — Observability (must-have)

Metrics:

- client_requests_total{upstream,method,status_class}
- client_latency_seconds (histogram/timer) per upstream
- retries_total and retry_exhausted_total
- circuit_state (open/half-open/closed)
- bulkhead_rejected_total
Tracing:
- add span per outbound call with:
  - upstream name
  - attempt count
  - timeout values
  - result (success/failure category)
Logs:
- structured, rate-limited logs on retry exhaustion and circuit opens

## Output artifacts

### A) Retry matrix (example template)

Fill this table per upstream endpoint:

- Endpoint: /v1/payments
  - Method: POST
  - Idempotent by HTTP semantics: NO
  - Idempotency-Key available: YES
  - Retry on: connect timeout, 502/503/504, 429 (respect Retry-After)
  - Max attempts: 2
  - Backoff: exponential + jitter
  - Total deadline: 800ms
  - Circuit breaker: enabled
  - Bulkhead: enabled (critical pool)

- Endpoint: /v1/profile/{id}
  - Method: GET
  - Idempotent by HTTP semantics: YES
  - Retry on: connect timeout, 502/503/504, 429
  - Max attempts: 2
  - Backoff: exponential + jitter
  - Total deadline: 300ms
  - Circuit breaker: enabled
  - Bulkhead: semaphore bulkhead

### B) Client configuration plan

- timeouts (connect + request deadline)
- retry rules and stop conditions
- circuit breaker thresholds
- bulkhead limits
- idempotency headers propagation

### C) Verification tests

- unit tests for retry classification (which errors are retried)
- integration tests with a stub server (WireMock) simulating:
  - timeouts
  - 5xx bursts
  - 429 + Retry-After
  - slow calls
- load test to ensure retries don’t multiply traffic dangerously

## Definition of Done (DoD)

- [ ] All outbound calls have explicit timeouts
- [ ] Retry policy is bounded, budget-aware, and safe-by-default
- [ ] Circuit breaker + bulkhead applied to critical upstreams
- [ ] Idempotency keys implemented for retried non-idempotent operations
- [ ] Metrics/traces/logs added for client behavior
- [ ] Tests cover failure modes and prevent regressions

## Guardrails (What NOT to do)

- Do not retry non-idempotent calls without idempotency keys
- Do not set large timeouts “to make errors go away”
- Do not use unbounded queues for bulkheads
- Do not enable retries + no circuit breaker (risk: cascading failure)
- Do not ignore rate limits; respect Retry-After or implement client-side rate limiting

## Cursor usage (recommended)

Attach:

- HTTP client wrapper (where requests are made)
- Resilience config (if exists)
- Production incident notes (timeouts, 5xx bursts, upstream SLO)
Prompt snippet:
“Use java-rest-clients-resilience. Produce a retry matrix and propose timeouts, retries, circuit breaker, and bulkhead settings. Ensure idempotency-key handling and add WireMock tests.”
