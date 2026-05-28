---
status: stub | draft | current | needs-review | archived
module: {module-name}
category: performance
created: YYYY-MM-DD
updated: YYYY-MM-DD
last-synced: never | YYYY-MM-DD
completeness: 0
related:
  - path/to/related-doc.md
dependencies:
  - path/to/dependency-doc.md
---

# {System/Feature Name} - Performance

Brief one-sentence description of the performance characteristics being
documented.

## Table of Contents

1. [Overview](#overview)
2. [Current State](#current-state)
3. [Rationale](#rationale)
4. [Performance Characteristics](#performance-characteristics)
5. [Optimization Strategies](#optimization-strategies)
6. [Benchmarks](#benchmarks)
7. [Monitoring](#monitoring)
8. [Future Enhancements](#future-enhancements)
9. [Related Documentation](#related-documentation)

---

## Overview

Describe the performance goals and requirements (2-4 paragraphs).

- What performance characteristics matter for this system?
- What are the performance SLAs or targets?
- What trade-offs were made for performance?

### Performance Targets

- Metric 1: Target value (e.g., < 100ms p95 latency)
- Metric 2: Target value (e.g., > 1000 req/sec throughput)
- Metric 3: Target value (e.g., < 50MB memory usage)

### When to reference this document

- When investigating performance issues
- When adding features that may impact performance
- When setting performance budgets
- When optimizing hot paths

---

## Current State

### Performance Metrics

Current measured performance characteristics.

#### Latency

- **P50 (median):** Xms
- **P95:** Xms
- **P99:** Xms
- **Max observed:** Xms

#### Throughput

- **Requests per second:** X req/sec
- **Data processed:** X MB/sec
- **Concurrent operations:** X

#### Resource Usage

- **CPU:** X% average, Y% peak
- **Memory:** X MB average, Y MB peak
- **Disk I/O:** X MB/sec
- **Network:** X MB/sec

### Performance Bottlenecks

Known bottlenecks and their impact.

#### Bottleneck 1: {Name}

- **Location:** `src/path/to/code.ts:line`
- **Impact:** X% of total execution time
- **Why it exists:** Reasoning
- **Mitigation:** Current workaround or plan

#### Bottleneck 2: {Name}

...

---

## Rationale

### Performance Design Decisions

#### Decision 1: {Optimization Strategy}

**Context:** What performance problem needed solving

**Options considered:**

1. Option A (Chosen):
   - Performance impact: Description
   - Trade-offs: What was sacrificed
   - Why chosen: Reasoning

2. Option B:
   - Performance impact: Description
   - Trade-offs: What was sacrificed
   - Why rejected: Reasoning

#### Decision 2: {Caching Strategy}

...

### Trade-offs

Performance trade-offs made in the design.

#### Trade-off 1: {Name}

- **Performance gain:** What improved
- **Cost:** What was sacrificed (complexity, memory, etc.)
- **Justification:** Why it's worth it

#### Trade-off 2: {Name}

...

---

## Performance Characteristics

### Time Complexity

Algorithmic complexity analysis.

#### Operation 1: {Name}

- **Best case:** O(?)
- **Average case:** O(?)
- **Worst case:** O(?)
- **Practical performance:** Description

#### Operation 2: {Name}

...

### Space Complexity

Memory usage analysis.

#### Data Structure 1: {Name}

- **Space complexity:** O(?)
- **Practical memory usage:** X MB for Y items
- **Growth rate:** Description

#### Space Data Structure 2: {Name}

...

### I/O Characteristics

Input/output performance characteristics.

#### I/O Operation 1: {Name}

- **I/O type:** Sequential / Random / Network
- **Frequency:** X operations per request
- **Volume:** X bytes per operation
- **Optimization:** Caching / Batching / Async

#### I/O Operation 2: {Name}

...

---

## Optimization Strategies

### Implemented Optimizations

#### Optimization 1: {Name}

**What was optimized:** Description

**Technique used:** Caching / Memoization / Lazy Loading / Batching / etc.

**Implementation:**

```typescript
// Code example showing optimization
```

**Performance impact:**

- Before: X ms/req
- After: Y ms/req
- Improvement: Z% faster

**Trade-offs:**

- Increased memory usage by X MB
- Added complexity in Y area

#### Optimization 2: {Name}

...

### Caching Strategy

How caching is used to improve performance.

#### Cache 1: {Name}

**What is cached:** Description

**Cache type:** In-memory / Disk / Distributed

**TTL:** X seconds/minutes/hours

**Invalidation:** When and how cache is cleared

**Hit rate:** X% (target: Y%)

**Memory usage:** X MB

#### Cache 2: {Name}

...

### Batching and Parallelization

How operations are batched or parallelized.

#### Batch Operation 1: {Name}

**What is batched:** Description

**Batch size:** X items

**Batch interval:** X ms

**Performance gain:** Y% improvement

#### Parallel Operation 1: {Name}

**What is parallelized:** Description

**Concurrency level:** X concurrent operations

**Performance gain:** Y% improvement

---

## Benchmarks

### Benchmark Results

Detailed benchmark results and methodology.

#### Benchmark 1: {Scenario}

**Test scenario:** Description of what's being tested

**Test data:** Size and characteristics of test data

**Environment:**

- CPU: Specification
- Memory: Size
- Disk: Type (SSD/HDD)

**Results:**

| Metric | Value |
| :------ | :----- |
| Throughput | X req/sec |
| Latency (p50) | X ms |
| Latency (p95) | X ms |
| Latency (p99) | X ms |
| Memory usage | X MB |
| CPU usage | X% |

**Running the benchmark:**

```bash
pnpm bench -- benchmark-name
```

#### Benchmark 2: {Scenario}

...

### Performance Regression Tests

Tests that prevent performance regressions.

**Location:** `src/**/*.bench.ts`

**How to run:**

```bash
pnpm bench:ci
```

**Failure criteria:**

- Latency regression > X%
- Throughput regression > Y%
- Memory increase > Z%

---

## Monitoring

### Production Metrics

Metrics tracked in production.

#### Metric 1: {Name}

**What it measures:** Description

**How it's collected:** Method/Tool

**Alert threshold:** X value

**Dashboard:** Link to dashboard

#### Metric 2: {Name}

...

### Performance Alerts

Alerts configured for performance degradation.

#### Alert 1: {Name}

**Condition:** Metric > threshold for duration

**Severity:** Critical / Warning / Info

**Action:** What to do when alerted

#### Alert 2: {Name}

...

### Profiling

How to profile performance issues.

**Profiling tools:**

- Tool 1: When to use it
- Tool 2: When to use it

**How to profile:**

```bash
# Command to run profiler
node --prof src/index.js
node --prof-process isolate-*.log
```

**Interpreting results:**

- Look for: What to look for in profiles
- Red flags: Warning signs

---

## Future Enhancements

### Phase 1: Quick wins (next release)

#### Enhancement 1

- **What:** Description
- **Expected impact:** X% improvement
- **Effort:** Low / Medium / High

#### Enhancement 2

...

### Phase 2: Medium-term (2-3 releases)

#### Enhancement 3

- **What:** Description
- **Expected impact:** X% improvement
- **Effort:** Low / Medium / High
- **Trade-offs:** What might be sacrificed

#### Enhancement 4

...

### Phase 3: Long-term (future consideration)

#### Enhancement 5

- **What:** Description
- **Expected impact:** X% improvement
- **Effort:** Low / Medium / High
- **Risks:** Potential risks

#### Enhancement 6

...

---

## Related Documentation

**Internal Design Docs:**

- [Architecture](./architecture.md) - Overall system architecture
- [Observability](./observability.md) - Performance monitoring

**Package Documentation:**

- `pkgs/{module}/README.md` - Package overview
- `pkgs/{module}/CLAUDE.md` - Development guide

**External Resources:**

- [Performance Best Practices](url) - General guidance
- [Profiling Guide](url) - How to profile

---

**Document Status:** {Explain current status if stub/draft/needs-review}

**Next Steps:** {What performance work is planned next}
