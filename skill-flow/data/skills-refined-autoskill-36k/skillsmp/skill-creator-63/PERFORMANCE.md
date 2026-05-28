# Performance

This file is an example placeholder referenced by the Skill Creator skill.

## Performance Goals

- **Latency**: p50/p95/p99 targets
- **Throughput**: expected RPS / job rate
- **Resource budgets**: CPU/memory, DB connections

## Profiling & Measurement

- How to measure locally (benchmarks, synthetic tests)
- What to check in CI (perf tests, regression guards)
- Production signals (dashboards, traces)

## Common Hotspots

- N+1 queries
- Excessive serialization / JSON handling
- Chatty service-to-service calls
- Large payloads / over-fetching
- Unbounded lists or expensive sorting

## Optimization Playbook

1. Reduce work: cache, memoize, precompute
2. Reduce I/O: batch, pagination, connection reuse
3. Reduce allocations: reuse buffers, avoid copies
4. Reduce contention: lock minimization, pooling

## Rollout

- Use feature flags for risky optimizations
- Compare before/after metrics
- Define rollback criteria
