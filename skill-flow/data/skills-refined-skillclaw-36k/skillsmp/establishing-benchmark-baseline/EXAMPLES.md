# Baseline Report Example

This file shows the expected structure of BENCHMARK_BASELINE.md.

## Example Report Structure

```markdown
# Benchmark Baseline Report for [Language Name]

Generated: [Date]

## Language Analysis

- **Type System**: [static/dynamic] typing
- **Execution Model**: [interpreter/bytecode VM/JIT/AOT/hybrid]
- **Platform**: [native/JVM/LLVM/custom]
- **Paradigm**: [imperative/OO/functional/multi-paradigm]
- **Complexity**: [minimal/moderate/full-featured]
- **GC**: [type and approach]
- **Optimization**: [specific optimizations detected]

## Comparable Languages

### 1. [Language Name]
**Rationale**: [Why this language was selected]
**URL**: [Benchmarks Game measurement page]

### 2. [Language Name]
**Rationale**: [Why this language was selected]
**URL**: [Benchmarks Game measurement page]

## Benchmarks from Benchmarks Game

### 1. [benchmark-name]
**Rationale**: [Why selected - what it tests]
**URL**: [Benchmarks Game description page]

## Benchmarks from AreWeFastYet

### 1. [benchmark-name]
**Rationale**: [What it tests]
**Status**: [Newly implemented / Existing implementation]

## How to Execute Benchmarks

### [benchmark-name]
**File**: `[filename].[ext]`
**Command**: `[execution command]`
**Test Parameter**: [N value or iterations]
**Verification**: [How to verify correctness]

## Actual Performance Results

### Benchmarks Game Results

| Benchmark | Date | Iterations | Total Time | Average Time | Notes |
|-----------|------|------------|------------|--------------|-------|
| fannkuch-redux | 2025-12-21 10:30 | 100 | 12.54s | 125.4ms | N=12 |

### AreWeFastYet Results

| Benchmark | Date | Iterations | Inner Iterations | Total Time | Average Time |
|-----------|------|------------|------------------|------------|--------------|
| queens | 2025-12-21 10:50 | 100 | 5000 | 3.2s | 32ms |

## Reference Language Performance

### [benchmark-name] (N=[value])

| Language | Elapsed Time | CPU Time | Memory |
|----------|--------------|----------|--------|
| [Lang A] | X.XX s | Y.YY-Z.ZZ s | M KB |

**Expected Performance**:
- Best case: [Min]s
- Expected: [Avg]s
- Worst case: [Max]s

## Next Steps

1. Compare results against expected ranges
2. If performance below expectations, use profiling skills
3. After optimizations, re-run benchmarks and append new results
```
