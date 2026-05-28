---
name: establishing-benchmark-baseline
description: "[PHASE 1] Creates benchmark suite and performance expectations. Entry: No BENCHMARK_BASELINE.md exists. Outputs: BENCHMARK_BASELINE.md, benchmark files. Next: PHASE 2 (generating-performance-theories)."
---

# Establishing Benchmark Baseline

Establishes performance baselines for your language implementation through automated discovery and implementation of industry-standard benchmarks.

**Use this skill FIRST** before any performance analysis or optimization work.

## Quick Start

**Step 0**: Check if `BENCHMARK_BASELINE.md` already exists in the workspace. If it does, skip this workflow and continue with `generating-performance-theories`.

**Step 1**: Ask user which benchmarks to generate using AskUserQuestion tool:
- Benchmarks Game only
- AreWeFastYet only
- Both (recommended)

**Step 2**: Copy this checklist to track progress:

```
Baseline Progress:
- [ ] Phase 1: Analyze language characteristics
- [ ] Phase 2: Identify comparable languages
- [ ] Phase 3: Discover and fetch Benchmarks Game data (if selected)
- [ ] Phase 4: Implement and measure Benchmarks Game benchmarks (if selected)
- [ ] Phase 5: Discover and fetch AreWeFastYet data (if selected)
- [ ] Phase 6: Implement and measure AreWeFastYet benchmarks (if selected)
- [ ] Phase 7: Generate and save baseline report with performance data
```

**Step 3**: Execute workflow following phase instructions in [WORKFLOW.md](WORKFLOW.md).

## What This Skill Does

1. **Analyzes language** - Determines type system, execution model, platform, paradigm
2. **Identifies comparable languages** - Finds 1-2 similar languages for comparison
3. **Discovers benchmarks** - Queries Benchmarks Game and/or AreWeFastYet
4. **Implements locally** - Creates benchmark files, runs them, collects timing
5. **Generates baseline** - Creates `BENCHMARK_BASELINE.md` with expectations

## Key URLs

**Benchmarks Game**:
- Measurements: `https://benchmarksgame-team.pages.debian.net/benchmarksgame/measurements/{language}.html`
- Descriptions: `https://benchmarksgame-team.pages.debian.net/benchmarksgame/description/{benchmark}.html`

**AreWeFastYet**:
- README: `https://raw.githubusercontent.com/smarr/are-we-fast-yet/refs/heads/master/README.md`
- Benchmarks: `https://raw.githubusercontent.com/smarr/are-we-fast-yet/refs/heads/master/benchmarks/{language}/{benchmark}.{ext}`

## Output Files

- **Local benchmark files** - Executable implementations
- **BENCHMARK_BASELINE.md** - Comprehensive report with performance expectations

## Integration with Other Skills

**Use this skill BEFORE**:
- `detecting-performance-warnings` - Identifies optimization barriers
- `profiling-with-cpu-sampler` - Profiles execution time
- `tracing-compilation-events` - Analyzes compilation behavior
- `analyzing-compiler-graphs` - Deep-dive compiler optimization

**Workflow**:

```text
1. [establishing-benchmark-baseline] → THIS SKILL (PHASE 1)
2. [generating-performance-theories] → Generate theories (PHASE 2)
3. [verifying-performance-theories]  → Verify with tools (PHASE 3)
4. [implementing-performance-fixes]  → Implement and validate fix (PHASE 4)
5. Loop to step 2 if performance gaps remain
```

## Common Mistakes to Avoid

- **Skipping this skill** - Always establish baselines before optimization
- **Choosing inappropriate benchmarks** - Select benchmarks relevant to your language's strengths
- **Not verifying correctness** - Ensure benchmark outputs are correct to avoid misleading results
- **Small sample size** - Use sufficient iterations for reliable timing data (e.g., N=500 or more)

## Detailed Documentation

See [WORKFLOW.md](WORKFLOW.md) for detailed phase instructions.
See [EXAMPLES.md](EXAMPLES.md) for complete walkthrough examples.
