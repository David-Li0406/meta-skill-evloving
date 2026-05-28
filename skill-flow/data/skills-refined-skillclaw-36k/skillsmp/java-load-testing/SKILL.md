---
name: java-load-testing
description: Create a load test plan and executable scripts (k6/Gatling style) with scenarios, success metrics, and regression gates. Use when investigating perf regressions, sizing capacity, or validating SLOs before release.
license: CC-BY-4.0
compatibility:
  jdk: "17+"
  runtime: "Any HTTP service (REST/gRPC gateway)"
metadata:
  owner: perf-platform
  version: "0.1.0"
  tags: [java, performance, load-testing, k6, gatling, slo]
---

# Java Load Testing (Plan + Scripts + Report)

## Goal

Turn “we think it’s fast enough” into:

- a measurable performance baseline
- reproducible load scripts
- clear success criteria (SLO/SLA-style)
- a regression signal in CI (when appropriate)

## Scope

### In scope

- Workload modeling: user journeys, read/write mix, data sets
- Scenario design: smoke, load, stress, spike, soak
- Metrics + success criteria: latency percentiles, throughput, error rate, saturation
- Tooling approach:
  - k6 (JS) OR Gatling (Scala/Java DSL) OR any equivalent
- Report template and trend tracking
- Safe operational practices (don’t melt prod)

### Out of scope

- Micro-optimizations without measurements
- “Benchmark theater” without environment control

## When to use

- Performance regression suspected after a change
- Capacity planning or sizing (CPU/mem/DB)
- New feature that adds heavy queries or external calls
- Pre-release performance validation

## Core concepts (the “physics” of load)

- Latency is shaped by queueing under saturation:
  - when utilization approaches 100%, tail latency explodes
- Percentiles matter:
  - average latency can hide p99 pain
- You need both:
  - “service metrics” (latency, errors, throughput)
  - “resource metrics” (CPU, memory, GC, DB connections, thread pools)

## Step-by-step workflow

### Step 1: Define the test objective

Pick one:

- Regression guard: compare current vs baseline
- Capacity: find max sustainable RPS under SLO
- Bottleneck discovery: identify saturation point and culprit
- Stability: long soak to detect leaks and slow degradation

### Step 2: Lock down the environment

Record:

- service version (commit/tag)
- JVM flags
- instance sizes and replicas
- DB/broker versions (if relevant)
- network path and load generator location
- any caches enabled

Without this, results won’t be comparable.

### Step 3: Build a workload model

- Identify critical endpoints/journeys (top traffic or highest business value)
- Define request mix (%):
  - e.g., 70% reads, 25% writes, 5% admin
- Define realistic data:
  - user ids, item ids, search queries
- Add think time / pacing:
  - avoid “firehose” that doesn’t resemble real users unless stress testing

### Step 4: Choose test types (recommended set)

- Smoke: 1–2 min, very low load, validate script correctness
- Load: 10–30 min, target expected peak load
- Stress: ramp beyond expected peak to find breaking point
- Spike: sudden jump, evaluate autoscaling and resilience
- Soak: 1–6 hours, detect leaks and slow resource creep

### Step 5: Implement scripts (k6-style)

You want:

- parameterized base URL
- environment-based auth tokens (never commit secrets)
- checks (functional correctness under load)
- thresholds (SLO-like gates)

k6 script skeleton:

```javascript
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  scenarios: {
    steady: { executor: "constant-vus", vus: 50, duration: "10m" }
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<300", "p(99)<800"]
  }
};

export default function () {
  const res = http.get(`${__ENV.BASE_URL}/api/v1/items`);
  check(res, { "status is 200": (r) => r.status === 200 });
  sleep(0.5);
}
```

### Step 6: Implement scripts (Gatling-style)

Gatling focuses on:

- scenarios, injection profiles
- assertions on percentiles and error rates
- rich reporting

Gatling skeleton (conceptual):

```groovy
setUp(
  scn.inject(
    rampUsersPerSec(1).to(100).during(10.minutes),
    constantUsersPerSec(100).during(20.minutes)
  )
).assertions(
  global.failedRequests.percent.lte(1),
  global.responseTime.percentile3.lte(800)
)
```

### Step 7: Measure and decide

Collect:

- request metrics (p50/p95/p99, RPS, errors)

- JVM metrics (GC pauses, heap, allocation rate)

- DB metrics (connections, slow queries)

- thread pool / queue metrics
Compare:

- baseline vs current

- pre-change vs post-change
Document:

- what changed

- why performance changed

- mitigation options

### Success criteria templates

Choose one set and write it down explicitly:

- Latency SLO:

  - p95 < 300ms

  - p99 < 800ms

- Error rate:

  - < 1% 5xx

- Saturation guardrails:
  - CPU < 75% sustained
  - DB connections < 80% of pool
  - GC pause p99 < 200ms

### CI integration guidance

- Do NOT run heavy load tests on every PR by default.
Recommended:

- PR: smoke test + micro checks (optional)
- Nightly: full load/stress suites
- Release candidate: full suite + comparison to baseline

Store artifacts:

- reports
- raw metrics snapshots
- environment manifest

### Definition of Done (DoD)

- [] Test objective defined

- [] Environment recorded

- [] Scenarios implemented (smoke + load at minimum)

- [] Thresholds/assertions defined

- [] Report produced with conclusions

- [] Regression signal defined (if needed)

### Guardrails (Safety)

- Never run heavy load tests against production without explicit approval

- Rate limit and coordinate with infra owners

- Never embed secrets in scripts

- Always provide a stop/abort procedure

### Outputs / Artifacts

- `loadtest/k6/*.js` or `loadtest/gatling/*`

- `loadtest/README.md` (how to run, environment variables)

- `reports/<date>-<version>.md` (summary + charts links)

- CI job definition (nightly or release pipeline)

### References (official docs)

- k6 docs: [https://grafana.com/docs/k6/](https://grafana.com/docs/k6/)

- Gatling docs: [https://docs.gatling.io/](https://docs.gatling.io/)
