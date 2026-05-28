---
name: java-gc-tuning
description: A disciplined GC analysis and tuning workflow for Java (G1/ZGC): symptoms triage, evidence capture (GC logs/JFR/heap), heap sizing, allocation hotspot reduction, and safe rollout. Use when GC pauses, OOMs, or suspected leaks occur.
license: CC-BY-4.0
compatibility: "JDK 17+ (recommended JDK 21). Assumes Unified JVM Logging (-Xlog) for GC logs."
metadata:
  owner: "backend"
  version: "1.0"
  tags: [java, gc, g1gc, zgc, memory, oom, troubleshooting, performance]
---

# GC Tuning & Memory Diagnostics (G1 / ZGC)

## Intent

GC tuning is not “try random flags”. This skill enforces a workflow:

1) Identify the symptom (pause vs throughput vs OOM vs leak)
2) Capture the right evidence (GC logs, JFR, heap dump when needed)
3) Choose the correct collector for your goals
4) Tune conservatively (heap sizing, pause targets) and reduce allocation hotspots
5) Validate via load tests and staged rollout

---

## Scope

### In scope

- Symptom triage: GC pauses, allocation rate spikes, OOM, suspected leak
- Evidence capture:
  - GC logs using Unified Logging (-Xlog)
  - JFR memory/GC events
  - `jcmd` histograms and heap dumps (when needed)
- Collector selection: G1 vs ZGC (and when not to change)
- Heap sizing strategy: Xms/Xmx, container memory, headroom
- Allocation hotspot reduction checklist
- Rollout and regression prevention

### Out of scope

- JVM internals deep theory (only what’s necessary)
- OS/cgroup tuning beyond basic container memory setup
- App-level memory architecture redesign (separate skill)

---

## When to use

Triggers:

- p95/p99 latency spikes correlated with GC
- long stop-the-world pauses
- frequent GC cycles (high GC overhead)
- OOMKilled / OutOfMemoryError
- suspected memory leak (heap grows without bound)
- sudden allocation rate increase after release

---

## Required inputs (context to attach in Cursor)

- JVM flags currently in use
- Runtime environment:
  - container limits, memory requests/limits
  - JDK vendor/version
- Metrics:
  - heap used/committed
  - GC time / pause quantiles
  - allocation rate (if available)
- Logs:
  - GC logs (sanitized)
  - error logs around OOM
- A reproduction load scenario if possible

---

## Core concepts (minimal)

- GC manages object lifetimes; pauses happen when GC needs to reclaim memory.
- Most performance problems come from:
  - too small heap or wrong sizing
  - extremely high allocation rate
  - promotion pressure / long-lived objects
  - memory leaks (unexpected retention)
- G1 is a balanced default for many services.
- ZGC targets low-latency and can reduce pause times, but you must validate throughput and memory overhead.

---

## Procedure (step-by-step)

### Step 1 — Classify the symptom (choose your path)

A) Latency spikes / pauses (but no OOM)
B) High GC overhead (too much time in GC)
C) OOM / OOMKilled
D) Suspected leak (heap grows steadily)

Deliverable: symptom classification + short timeline.

---

### Step 2 — Capture evidence (do not tune blind)

#### 2.1 Enable GC logging (Unified Logging)

In a controlled environment (or carefully in prod), enable GC logs with a bounded file policy.
Example patterns (adjust to your ops standards):

- `-Xlog:gc*:file=logs/gc.log:time,uptime,level,tags:filecount=10,filesize=50M`

Goal: capture pauses, frequencies, and causes.

#### 2.2 Capture a JFR snippet (optional but recommended)

Record 1–5 minutes during the incident window to correlate GC, allocation, and thread behavior.

#### 2.3 Use jcmd for quick snapshots

Useful commands depend on your policy:

- class histogram snapshot
- heap info
- thread dump correlation

Deliverable: evidence bundle (GC logs + optional JFR + jcmd snapshots).

---

### Step 3 — Build a baseline report

Extract:

- GC pause distribution (p50/p95/p99)
- GC frequency (how often)
- Heap occupancy after GC
- Allocation rate trend
- Old-gen growth trend

Deliverable: baseline metrics table (in the report, not necessarily in code).

---

### Step 4 — Heap sizing (often the highest leverage)

Principles:

- Give enough heap to avoid constant GC thrashing.
- Avoid huge heaps if you need tight latency (validate).
- In containers, ensure JVM sees correct memory limits and leaves headroom for native memory.

Actions:

- Ensure Xms/Xmx are set intentionally (not default guessing) where appropriate.
- Avoid extreme mismatches unless you know why.
- Keep OS/native headroom (thread stacks, metaspace, direct buffers).

Deliverable: recommended Xms/Xmx and memory headroom notes.

---

### Step 5 — Choose the collector deliberately

Default: G1 for general workloads.
Consider ZGC if:

- latency SLO is strict and pauses matter more than raw throughput
- you can validate under load
- your environment supports it cleanly

Avoid changing collector while also changing many other flags.
One major change at a time.

Deliverable: collector choice decision and a validation plan.

---

### Step 6 — Conservative tuning (collector-specific)

#### 6.1 G1 tuning guidelines (conservative)

- Set a realistic pause target:
  - `-XX:MaxGCPauseMillis=<value>`
- Observe if it increases GC frequency too much.
- Do not sprinkle old CMS-era flags.

If you see promotion pressure or humongous allocations:

- focus on reducing allocation spikes and large object churn first.

#### 6.2 ZGC tuning guidelines (conservative)

- Focus on:
  - enough heap headroom
  - stable allocation rate
- Validate pause improvements and ensure no throughput regression.

If available, understand whether you’re using a generational mode or not (depends on JDK line and features).
Always verify with your JDK vendor docs.

Deliverable: a minimal flag set, with justification.

---

### Step 7 — Fix allocation hotspots (often better than flags)

Common high-impact fixes:

- Avoid repeated JSON parse/serialize in hot paths
- Reuse buffers carefully (without unsafe pooling)
- Reduce temporary object creation in loops
- Replace regex-heavy parsing with faster logic
- Avoid building huge intermediate collections (stream carefully)
- Use primitives / arrays where appropriate (trade readability carefully)

Use profiling skill to locate allocation sites.

Deliverable: targeted code changes + tests.

---

### Step 8 — OOM / leak path

If OOM:

1) Determine whether it’s Java heap or native memory.
2) If heap:
   - capture heap dump (careful with size and privacy)
   - compare histograms over time
   - look for dominant retained sizes and suspicious retainers
3) If native:
   - check direct buffers, thread count, metaspace, JNI allocations

Deliverable: root cause hypothesis + mitigation + regression tests.

---

### Step 9 — Validate and roll out safely

- Re-run load test:
  - compare pause quantiles, throughput, error rate
- Canary rollout:
  - 1% traffic -> 10% -> 100%
- Ensure dashboards and alerts cover:
  - GC pause p99
  - allocation rate
  - old-gen occupancy
  - OOMKilled events

Deliverable: rollout notes and monitoring checklist.

---

## Outputs / Artifacts

- Evidence bundle (GC logs / JFR / snapshots)
- Baseline vs after report
- Minimal JVM flag recommendations with rationale
- Code changes reducing allocation pressure (if applicable)
- Runbook update (how to capture GC data in the future)

---

## Definition of Done (DoD)

- [ ] Symptom clearly classified with timeline
- [ ] Evidence captured (GC logs at minimum)
- [ ] One major change at a time (collector OR heap OR key flags)
- [ ] Improvement verified under load
- [ ] Canary rollout plan documented
- [ ] Alerts/dashboards updated

---

## Common failure modes & fixes

- Symptom: tuning increases GC frequency, hurts latency
  - Cause: pause target too aggressive or heap too small
  - Fix: adjust target, increase heap headroom, reduce allocations

- Symptom: OOM persists despite bigger heap
  - Cause: leak or native memory issue
  - Fix: heap dump analysis; check direct buffers/metaspace

- Symptom: switching to ZGC changes throughput
  - Cause: workload characteristics; headroom issues
  - Fix: validate; revert if necessary; reduce allocation pressure

---

## Guardrails (What NOT to do)

- Do NOT copy-paste “GC tuning flag lists” from random blogs.
- Do NOT tune without GC logs and a reproducible scenario.
- Do NOT keep legacy GC flags (CMS-era) on modern JDKs.
- Do NOT generate heap dumps in production without privacy + storage plan.

---

## References (primary)

- Oracle Java 21 Garbage Collection Tuning Guide: <https://docs.oracle.com/en/java/javase/21/gctuning/>
- OpenJDK ZGC wiki: <https://wiki.openjdk.org/display/zgc>
- JEP 439 (Generational ZGC): <https://openjdk.org/jeps/439>
- Unified JVM Logging (JEP 158): <https://openjdk.org/jeps/158>
- Oracle Diagnostic Tools (jcmd/JFR/etc.): <https://docs.oracle.com/en/java/javase/21/troubleshoot/diagnostic-tools.html>
