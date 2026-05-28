---
name: HSM Benchmark Runner
description: Run benchmarks and analyze performance against targets
version: 1.0.0
tags: [hsm, benchmarking, performance]
---

# HSM Benchmark Runner

Run benchmarks for HSM modules and compare against performance targets.

## Usage

```
/hsm-bench [module-number]
```

## What You Do

1. **Run benchmarks:**
   - If module specified: `cd crates/<module> && cargo bench`
   - If no module: `cargo bench --all`

2. **Parse results:**
   Extract criterion output for:
   - Operations per second
   - Latency (p50, p95, p99)
   - Throughput

3. **Compare against targets:**
   Read success metrics from `docs/phases/phase-2-plans/module-*-ENHANCE.md`

   Example targets:
   - Crypto Engine: Ed25519 >1,000 ops/sec, ECDSA >500 ops/sec
   - Key Manager: Lookup p99 <1ms, >1,000 concurrent ops/sec
   - Auth: Cert validation p99 <5ms, Permission check <100μs
   - gRPC API: >10k connections, >5,000 req/sec, p99 <100ms
   - Audit: Write p99 <5ms, >10k events/sec
   - Storage: Cached read <100μs, Cold read p99 <5ms

4. **Generate report:**
   Show pass/fail for each metric with actual vs target values.

## Example Output

```
Module 1: Crypto Engine
========================
Ed25519 Sign:     1,245 ops/sec  ✅ (target: >1,000)
ECDSA P-256 Sign:   678 ops/sec  ✅ (target: >500)
AES-256-GCM:      6,123 ops/sec  ✅ (target: >5,000)

Overall: 3/3 targets met ✅
```
