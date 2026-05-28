---
name: performance-optimization
description: Use this skill when you need to optimize the performance of your application by identifying bottlenecks and implementing effective strategies.
---

# Performance Optimization

> **Core Question**

**What's the bottleneck, and is optimization worth it?**

## Before Optimizing

- Have you measured? (Don't guess)
- What's the acceptable performance?
- Will optimization add complexity?

## Performance Decision → Implementation

| Goal                | Design Choice         | Implementation                     |
|---------------------|-----------------------|------------------------------------|
| Reduce allocations   | Pre-allocate, reuse   | `with_capacity`, object pools      |
| Improve cache        | Contiguous data       | `Vec`, `SmallVec`                 |
| Parallelize          | Data parallelism      | `rayon`, threads                   |
| Avoid copies         | Zero-copy             | References, `Cow<T>`              |
| Reduce indirection    | Inline data           | `smallvec`, arrays                 |

## Thinking Prompts

1. **Have you measured?**
   - Profile first → flamegraph, perf
   - Benchmark → criterion, cargo bench
   - Identify actual hotspots

2. **What's the priority?**
   - Algorithm (10x-1000x improvement)
   - Data structure (2x-10x)
   - Allocation (2x-5x)
   - Cache (1.5x-3x)

3. **What's the trade-off?**
   - Complexity vs speed
   - Memory vs CPU
   - Latency vs throughput

## Trace Up ↑

To domain constraints:

```
"How fast does this need to be?"
    ↑ Ask: What's the performance SLA?
    ↑ Check: domain-* (latency requirements)
    ↑ Check: Business requirements (acceptable response time)
```

| Question               | Trace To  | Ask                             |
|------------------------|-----------|---------------------------------|
| Latency requirements    | domain-*  | What's acceptable response time?|
| Throughput needs        | domain-*  | How many requests per second?   |
| Memory constraints       | domain-*  | What's the memory budget?       |

## Trace Down ↓

To implementation:

```
"Need to reduce allocations"
    ↓ m01-ownership: Use references, avoid clone
    ↓ m02-resource: Pre-allocate with_capacity

"Need to parallelize"
    ↓ m07-concurrency: Choose rayon or threads
    ↓ m07-concurrency: Consider async for I/O-bound

"Need cache efficiency"
    ↓ Data layout: Prefer Vec over HashMap when possible
    ↓ Access patterns: Sequential over random access
```

## Quick Reference

| Tool                | Purpose                     |
|---------------------|-----------------------------|
| `cargo bench`       | Micro-benchmarks            |
| `criterion`         | Statistical benchmarks       |
| `perf` / `flamegraph` | CPU profiling              |
| `heaptrack`         | Allocation tracking          |