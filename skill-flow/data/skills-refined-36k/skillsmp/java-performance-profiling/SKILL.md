---
name: java-performance-profiling
description: A reproducible Java performance profiling workflow using JFR and async-profiler concepts: capture evidence (CPU/alloc/locks), analyze flamegraphs, form hypotheses, ship fixes, and verify regressions. Use when CPU is high or latency spikes.
license: CC-BY-4.0
compatibility: "JDK 17+ (recommended JDK 21). Production-safe approach uses JFR. async-profiler usage depends on deployment permissions."
metadata:
  owner: "backend"
  version: "1.0"
  tags: [java, performance, profiling, jfr, async-profiler, flamegraph, latency]
---

# Java Performance Profiling (JFR + async-profiler workflow)

## Intent

This skill gives you a **repeatable** profiling loop:

1) Confirm the symptom and isolate a reproducible scenario
2) Capture evidence with the **lowest-risk tool first** (JFR)
3) Analyze: CPU hot paths, allocation hotspots, lock contention, thread states
4) Make a small fix
5) Re-measure and produce a concise report

Goal: ship performance fixes with confidence, not guesswork.

---

## Scope

### In scope

- CPU profiling (sampling)
- Allocation profiling (where memory is allocated)
- Lock contention analysis
- Thread state analysis (runnable/blocked/waiting)
- JFR capture and analysis
- async-profiler-style flamegraph workflow (conceptual + practical guidance)
- Verification via A/B load tests

### Out of scope

- Microbenchmark-only optimization (use JMH skill if needed)
- OS kernel perf tuning
- Full distributed tracing diagnosis (covered by observability skill)

---

## When to use

Triggers:

- CPU high in production
- p95/p99 latency spikes
- throughput regression after release
- frequent GC due to allocation storms
- lock contention symptoms (threads blocked, long waits)

---

## Required inputs (context to attach in Cursor)

- The hot endpoints / services
- Recent changes (PR diff)
- Baseline metrics dashboards (latency, CPU, GC, error rate)
- Deployment constraints:
  - can you run JFR in prod?
  - can you attach profilers?
  - can you reproduce in staging?

---

## Safety-first tool selection

Use tools in this order:

1) Metrics + logs + traces to locate where to profile
2) **JFR** for production-safe profiling
3) async-profiler for deeper CPU/alloc/lock signals when allowed
4) Heap dump / GC deep dive if memory-leak suspected

---

## Procedure (step-by-step)

### Step 1 — Write a profiling question (avoid fishing)

Examples:

- “Which methods consume the most CPU during /search at p99?”
- “Where are we allocating the most objects per request?”
- “Which lock is contended during peak traffic?”

Deliverable: a single profiling question + success metric.

---

### Step 2 — Reproduce and minimize noise

- Use a stable load scenario (same input size, same dataset, same concurrency)
- Pin down:
  - request path
  - concurrency level
  - duration
- Confirm the symptom exists under the scenario.

Deliverable: “Repro recipe” (commands, parameters, expected symptom).

---

### Step 3 — Capture JFR (preferred baseline)

Start a bounded recording:

- short duration (30–300s)
- include CPU, allocation, locks, thread events

Capture methods vary:

- `jcmd <pid> JFR.start ...`
- `jfr` tool (depending on environment)
- JVM startup flags in a controlled environment (not first choice)

Always store:

- recording file name
- time window
- workload parameters
- build/version hash

Deliverable: a JFR recording + metadata.

---

### Step 4 — Analyze JFR: a structured checklist

When opening JFR (JMC or other tooling), check:

**CPU / Execution**

- hottest methods and call stacks
- suspicious loops
- high cost serialization/deserialization
- regex backtracking hotspots
- logging overhead (string concat, JSON encode)

**Allocation**

- top allocation sites (per request)
- big object arrays, large maps/lists
- repeated parsing of the same data
- missing caching for derived results

**Locks**

- monitors and contended locks
- synchronized blocks with I/O inside
- thread parking patterns

**Thread states**

- many threads blocked on DB pool?
- many runnable threads competing for CPU?
- many waiting threads due to missing timeouts?

Deliverable: “Top 3 findings” with evidence pointers (screen captures or notes).

---

### Step 5 — Use async-profiler-style flamegraphs when permitted

If you can attach a profiler in staging or a safe prod window:

- Generate a CPU flamegraph for the same scenario
- Optionally allocation or lock flamegraphs (depending on tool support)

Rules:

- keep capture windows short
- run during controlled load
- avoid collecting sensitive data
- get explicit approval for production attaches

Deliverable: flamegraph(s) + short interpretation.

---

### Step 6 — Convert findings into hypotheses and fixes

For each finding, produce:

- Hypothesis: “X is expensive because Y”
- Fix idea: “Change A to B”
- Expected impact: “Reduce allocations by ~N per request” or “Reduce CPU in method M”
- Risk: correctness risk and rollback plan

Prefer small fixes:

- avoid “rewrite everything”
- isolate changes
- add micro-level regression tests when appropriate

Deliverable: a small PR with focused perf fix.

---

### Step 7 — Verify with the same workload and report

Re-run the same test:

- baseline vs new
- compare p95/p99, throughput, CPU, allocation rate, GC time, errors

Report template:

- Context (service/version)
- Workload
- Baseline metrics
- Changes
- After metrics
- Evidence (JFR/flamegraph deltas)
- Risk / rollback plan

Deliverable: perf report + artifacts in `references/` folder (or attachment store).

---

## Outputs / Artifacts

- Repro recipe
- JFR recording + metadata
- Optional flamegraphs
- “Top 3 findings” summary
- PR with measured improvements
- Report template filled

---

## Definition of Done (DoD)

- [ ] Profiling question defined and answered with evidence
- [ ] Recording captured and stored with metadata
- [ ] Fix is small and has rollback plan
- [ ] Re-measurement confirms improvement or documents no-change
- [ ] No new correctness regressions (tests passed)
- [ ] Report written (baseline vs after)

---

## Common failure modes & fixes

- Symptom: flamegraph shows “native” or “unknown”
  - Cause: missing symbols, container restrictions
  - Fix: use JFR; ensure correct permissions; profile in staging

- Symptom: results not reproducible
  - Cause: workload not controlled, noisy environment
  - Fix: stabilize inputs, duration, concurrency; repeat runs

- Symptom: you optimize the wrong thing
  - Cause: not tying profiling to p95/p99 paths
  - Fix: start from metrics/traces; profile where pain exists

---

## Guardrails (What NOT to do)

- Do NOT profile production with high-overhead tooling without explicit approval.
- Do NOT “optimize” without measurements.
- Do NOT micro-optimize before fixing algorithmic or I/O bottlenecks.
- Do NOT commit profiler configs that leak secrets or sensitive paths.

---

## References (primary)

- Java Flight Recorder (JDK tooling): <https://docs.oracle.com/en/java/javase/21/jfapi/using-java-flight-recorder.html>
- `jcmd` and diagnostics overview: <https://docs.oracle.com/en/java/javase/21/troubleshoot/diagnostic-tools.html>
- `jfr` command (Oracle tool reference): <https://docs.oracle.com/en/java/javase/21/docs/specs/man/jfr.html>
- Flight Recorder (OpenJDK JEP 328): <https://openjdk.org/jeps/328>
- async-profiler (project): <https://github.com/jvm-profiling-tools/async-profiler>
