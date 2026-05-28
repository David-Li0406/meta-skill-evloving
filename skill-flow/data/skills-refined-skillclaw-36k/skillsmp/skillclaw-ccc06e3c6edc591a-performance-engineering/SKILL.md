---
name: performance-engineering
description: Use this skill when profiling code, optimizing bottlenecks, benchmarking, or when "performance", "profiling", "optimization", or "--perf" are mentioned.
---

# Performance Engineering

Evidence-based performance optimization → measure → profile → optimize → validate.

<when_to_use>

- Profiling slow code paths or bottlenecks
- Identifying memory leaks or excessive allocations
- Optimizing latency-critical operations (P95, P99)
- Benchmarking competing implementations
- Database query optimization
- Reducing CPU usage in hot paths
- Improving throughput (RPS, ops/sec)

NOT for: premature optimization, optimization without measurement, guessing at bottlenecks

</when_to_use>

<iron_law>

NO OPTIMIZATION WITHOUT MEASUREMENT

**Required workflow:**
1. Measure baseline performance with realistic workload
2. Profile to identify actual bottleneck
3. Optimize the bottleneck (not what you think is slow)
4. Measure again to verify improvement
5. Document gains and tradeoffs

Optimizing unmeasured code wastes time and introduces bugs.

</iron_law>

<phases>

Use a task management tool to track the optimization process:

**Phase 1: Establishing baseline**
- content: "Establish performance baseline with realistic workload"
- activeForm: "Establishing performance baseline"

**Phase 2: Profiling bottlenecks**
- content: "Profile code to identify actual bottlenecks"
- activeForm: "Profiling code to identify bottlenecks"

**Phase 3: Analyzing root cause**
- content: "Analyze profiling data to determine root cause"
- activeForm: "Analyzing profiling data"

**Phase 4: Implementing optimization**
- content: "Implement targeted optimization for identified bottleneck"
- activeForm: "Implementing optimization"

**Phase 5: Validating improvement**
- content: "Measure performance gains and verify no regressions"
- activeForm: "Validating performance improvement"

</phases>

<metrics>

## Key Performance Indicators

**Latency (response time):**
- P50 (median) — typical case
- P95 — most users
- P99 — tail latency
- P99.9 — outliers
- TTFB — time to first byte
- TTLB — time to last byte

**Throughput:**
- RPS — requests per second
- ops/sec — operations per second
- bytes/sec — data transfer rate
- queries/sec — database throughput

**Memory:**
- Heap usage — allocated memory
- GC frequency — garbage collection pauses
- GC duration — stop-the-world time
- Allocation rate — memory churn
- Resident set size (RSS) — total memory

</metrics>