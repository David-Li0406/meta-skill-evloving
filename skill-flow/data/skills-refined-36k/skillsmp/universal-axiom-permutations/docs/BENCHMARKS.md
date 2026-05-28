# Performance Benchmarks

## Overview

This document describes the performance benchmark suite for The Universal Axiom implementations across Python, JavaScript, Rust, and Julia.

## Benchmark Scenarios

### 1. Basic Computation
Tests the core intelligence computation at various n values:
- **n=1**: Baseline computation with minimal Fibonacci overhead
- **n=10**: Medium complexity with moderate Fibonacci values
- **n=20**: Higher complexity with larger Fibonacci numbers

**Metrics**: Execution time per operation

### 2. Evolution Simulation
Tests the evolution process over multiple steps:
- **10 steps**: Short evolution sequence (n=1 → n=11)
- **100 steps**: Medium evolution sequence (n=1 → n=101)
- **1000 steps**: Long evolution sequence (stress test)

**Metrics**: Total time, time per evolution step

### 3. Contradiction Resolution
Tests the simulator's contradiction resolution mechanism:
- Multiple contradiction resolution cycles
- Subjectivity reduction tracking
- Coherence measurement overhead

**Metrics**: Time per resolution cycle, coherence calculation time

### 4. State Inspection
Tests serialization and state access:
- State retrieval operations
- History tracking overhead
- JSON serialization performance

**Metrics**: Time per state access, serialization overhead

### 5. Large N Values
Tests behavior with extreme values:
- **n=50**: Large Fibonacci numbers
- **n=100**: Very large Fibonacci numbers
- **n=150**: Stress test (may overflow in some languages)

**Metrics**: Execution time, numerical stability

### 6. Fibonacci Sequence Generation
Tests the Fibonacci sequence generation in isolation:
- Generate sequence up to n=12
- Generate sequence up to n=50
- Generate sequence up to n=100

**Metrics**: Time per sequence generation

## Metrics Measured

For each benchmark:
- **Execution time**: Mean, median, p95, p99 (where applicable)
- **Throughput**: Operations per second
- **Iterations**: Number of iterations for reliable measurements

## Running Benchmarks

### Python
```bash
python benchmarks/benchmark_python.py
```

### JavaScript
```bash
npm run build
node benchmarks/benchmark-javascript.js
```

### Rust
```bash
cd src/rust
cargo bench
```

### Julia
```bash
julia benchmarks/benchmark_julia.jl
```

### All Languages (Comparison)
```bash
python benchmarks/compare_all.py
```

## Interpreting Results

### Expected Performance Characteristics

**Rust**: Fastest overall
- Compiled, native code
- Zero-cost abstractions
- Minimal runtime overhead

**Julia**: Fast for numerical computation
- JIT compiled
- Optimized for scientific computing
- Good balance of speed and ease of use

**JavaScript**: Moderate performance
- V8 JIT optimization
- Single-threaded
- Good for moderate workloads

**Python**: Slowest but acceptable
- Interpreted
- Dynamic typing overhead
- Simple, readable implementation

### Performance Comparisons

Typical relative performance (Rust = 1x baseline):
- Rust: 1x (fastest)
- Julia: 2-5x
- JavaScript: 10-20x
- Python: 50-100x

Note: These are approximate ratios. Actual performance depends on:
- JIT warmup (Julia, JavaScript)
- Optimization flags (Rust: release vs debug)
- System resources
- Input sizes

## Benchmark Results

See `benchmarks/RESULTS.md` for the latest cross-language comparison results.
