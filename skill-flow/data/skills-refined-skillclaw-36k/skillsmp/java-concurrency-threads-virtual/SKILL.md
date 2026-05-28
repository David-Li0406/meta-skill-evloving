---
name: java-concurrency-threads-virtual
description: Choose and implement the right concurrency model in Java (thread pools vs virtual threads), including throughput/latency trade-offs, blocking I/O, backpressure, cancellation, and measurement. Use when tuning throughput or working with blocking I/O.
license: CC-BY-4.0
compatibility: "JDK 21+ recommended (Virtual Threads final). Works with any server/framework; integration details vary."
metadata:
  owner: "backend"
  version: "1.0"
  tags: [java, concurrency, virtual-threads, loom, performance, scalability]
---

# Concurrency Patterns & Virtual Threads (Project Loom)

## Intent

This skill helps you:

- Decide **when virtual threads are the best default**
- Avoid common production pitfalls (pinned threads, pool exhaustion, unbounded concurrency)
- Implement a **measured** migration from platform threads / pools to virtual threads
- Add **backpressure, timeouts, cancellation**, and observability
- Produce a clear recommendation + measurement plan

Virtual threads shine for **I/O-bound** workloads where you would otherwise block platform threads.

---

## Scope

### In scope

- Concurrency model selection:
  - platform threads + bounded pools
  - virtual threads for per-task concurrency
  - structured concurrency (if available)
- Safe usage patterns:
  - timeouts, cancellation, resource bounds
  - backpressure and concurrency limiting
- Integration considerations:
  - HTTP servers, DB pools, external calls
- Measurement workflow (load tests + metrics + thread dumps/JFR)

### Out of scope

- Full reactive programming rewrites (separate skill)
- Kernel-level tuning (separate ops skill)
- Deep JVM ergonomics (covered by GC/perf skills)

---

## When to use

Triggers / keywords:

- “blocking I/O”, “thread pool saturated”, “queue backlog”
- “increase throughput”, “reduce latency spikes”
- “too many threads”, “context switching”
- “migrate to Java 21”, “virtual threads”
- “deadlocks / contention”, “synchronized hotspot”

---

## Required inputs (context to attach in Cursor)

- Entry points that schedule work (request handler, job runner)
- Thread pool/executor configuration
- External I/O boundaries:
  - HTTP clients
  - DB calls (JDBC)
  - queue consumers/producers
- Timeouts configuration (or lack thereof)
- Observability: metrics, logs, traces around those boundaries

---

## Core mental model (in one paragraph)

Virtual threads provide a cheap “thread-per-task” style without paying the same OS-thread cost, so you can write straightforward blocking code while scaling concurrency—**but only if you also bound external resources** (DB connections, sockets, rate limits) and avoid patterns that pin virtual threads for long periods.

---

## Decision checklist (choose the right model)

### Step 1 — Classify the workload

- If most time is waiting on network/DB/file I/O: **I/O-bound** → virtual threads likely help
- If most time is CPU computation: **CPU-bound** → keep bounded CPU pool; virtual threads won’t create extra CPU

Deliverable: workload classification with evidence (metrics/traces/JFR).

### Step 2 — Identify your true bottleneck

Common bottlenecks:

- DB connection pool limit
- upstream rate limit
- thread pool saturation
- lock contention / synchronized hotspots
- GC pressure / allocation

Virtual threads help mainly with “blocked threads waiting for I/O”.
They do NOT increase DB connections or fix slow queries.

Deliverable: bottleneck list + top 1–2 hypotheses.

---

## Implementation playbook

### Step 3 — Make timeouts and cancellation explicit (non-optional)

Before scaling concurrency, ensure:

- HTTP client has connect/read timeouts
- DB calls have query timeouts
- queue operations have sane timeouts
- request-level deadlines exist (even if coarse)

Why: virtual threads can create huge concurrency; without timeouts you get stuck tasks and resource leaks.

Deliverable: timeout policy.

---

### Step 4 — Add concurrency limits (backpressure)

Even with virtual threads, you must bound:

- concurrent DB queries (e.g., semaphore around DB operations)
- concurrent calls per upstream (bulkhead)
- queue consumption concurrency
- in-flight requests

Pattern: `Semaphore` or “bulkhead” around scarce resources.

Deliverable: “Resource Bound Map” (what is bounded and how).

---

### Step 5 — Introduce virtual threads in the safest surface area first

Start with:

- background tasks that do blocking I/O
- fan-out/fan-in helper calls

Use an executor:

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
  Future<Result> f = executor.submit(() -> blockingCall());
}
```

Or create a virtual thread directly:

```java
Thread.startVirtualThread(() -> blockingCall());

```

Prefer **structured** lifetime management:

- scope tasks to a request or a well-defined operation boundary
- ensure cancellation on failure/timeouts

Deliverable: minimal patch introducing virtual thread execution for one path.

---

### Step 6 — (Optional) Use Structured Concurrency if available

If your JDK exposes StructuredTaskScope (preview/incubator depending on version),

it can model “fork/join as a unit”:

- on first failure, cancel the rest
- on timeout, cancel all
- keep lifetimes well-structured

Deliverable: structured concurrency usage (if allowed by your build policy).

---

### Step 7 — Avoid common pitfalls (virtual-thread-specific)

1. **Pinned threads**

- Using `synchronized` around blocking operations can pin a virtual thread to a carrier thread.
- Long-running blocking inside synchronized blocks is risky.

Mitigation:

- minimize synchronized scope
- use `ReentrantLock` carefully (still can block)
- keep blocking I/O outside synchronized

1. **ThreadLocal abuse**

- Virtual threads make ThreadLocal usage more expensive and harder to reason about at scale.
- Prefer explicit context passing or “scoped values” (if available).

1. **Unbounded concurrency causing resource exhaustion**

- You can easily create 100k waiting tasks.
- Without limits: DB pool exhaustion, too many open sockets, file descriptor exhaustion.

Mitigation:

- concurrency limiting
- rate limiting
- timeouts

Deliverable: pitfalls checklist included in PR description.

---

## Measurement plan (must include)

### Step 8 — Define success metrics

Choose 3–5 metrics:

- p95/p99 latency per endpoint
- throughput (RPS)
- error rate / timeouts
- DB pool utilization, queue lag
- CPU utilization / runnable threads

### Step 9 — Run controlled load tests

Compare:

- baseline (platform threads / old pools)
- new (virtual threads + backpressure + timeouts)

Keep test conditions identical.

### Step 10 — Verify with thread dumps / JFR

- Confirm fewer blocked platform threads
- Confirm carrier thread utilization is reasonable
- Look for pinned thread indicators (if tooling supports it)
- Validate no new contention hotspots

Deliverable: “Before vs After” report.

---

## Outputs / Artifacts

- Recommendation: chosen concurrency model and why
- Code changes: executor usage, timeouts, backpressure controls
- Resource Bound Map
- Measurement plan + results summary
- Runbook: how to debug saturation under load

---

## Definition of Done (DoD)

- [ ]  Timeouts are explicit at all I/O boundaries
- [ ]  Concurrency is bounded for scarce resources (DB/upstream)
- [ ]  Load test shows measurable improvement (or documented no-change)
- [ ]  No evidence of new pinned-thread pathologies
- [ ]  Observability updated (metrics/logs/traces around boundaries)
- [ ]  Rollback plan exists (feature flag or config switch)

---

## Common failure modes & fixes

- Symptom: throughput improved but error rate spikes
  - Cause: DB pool exhausted (more concurrency hit DB)
  - Fix: add DB bulkhead + tune pool + fix slow queries
- Symptom: latency spikes remain
  - Cause: lock contention / synchronized bottleneck
  - Fix: reduce contention, redesign critical section
- Symptom: CPU goes high, no throughput gain
  - Cause: CPU-bound workload; too much parallelism
  - Fix: bounded CPU executor; optimize code paths
- Symptom: “too many open files”
  - Cause: unbounded concurrency / missing timeouts
  - Fix: timeouts + concurrency limits + connection reuse

---

## Guardrails (What NOT to do)

- Do NOT “switch everything to virtual threads” without measurement.
- Do NOT remove backpressure because “threads are cheap now”.
- Do NOT run with infinite timeouts.
- Do NOT rely on ThreadLocal-heavy context propagation at massive scale without a plan.

---

## References (primary)

- Oracle Java 21 Virtual Threads Guide: <https://docs.oracle.com/en/java/javase/21/core/virtual-threads.html>
- JDK 21 overview (JEP list): <https://openjdk.org/projects/jdk/21/>
- Structured Concurrency (Oracle docs): <https://docs.oracle.com/en/java/javase/21/core/structured-concurrency.html>
- Scoped Values (OpenJDK JEP 446): <https://openjdk.org/jeps/446>
