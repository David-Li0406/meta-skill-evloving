---
name: generating-performance-theories
description: "[PHASE 2] Analyzes code to identify optimization opportunities. Entry: BENCHMARK_BASELINE.md exists AND (no PERFORMANCE_THEORIES.md OR all theories fixed). Outputs: PERFORMANCE_THEORIES.md. Next: PHASE 3 (verifying-performance-theories)."
---

# Generating Performance Theories

Systematically analyzes language implementation code to generate testable performance hypotheses. Produces a prioritized list of theories ready for verification with profiling tools.

## What This Skill Does

1. **Loads benchmark data** - Reads BENCHMARK_BASELINE.md and timing results
2. **Analyzes performance gaps** - Compares actual vs expected performance
3. **Performs systematic code analysis** - Examines implementation for anti-patterns
4. **Generates prioritized theories** - Each with verification plan and expected evidence
5. **Outputs theory list** - Ready for `verifying-performance-theories` skill

## Prerequisites

- **REQUIRED**: `BENCHMARK_BASELINE.md` exists (from `establishing-benchmark-baseline` skill)
- **REQUIRED**: Benchmark timing data available
- **RECOMMENDED**: Familiarity with Truffle/Graal performance patterns

## Quick Start

**Step 0**: Check if a theories file (e.g., `PERFORMANCE_THEORIES.md`) already exists in the workspace:
- If it exists with **unverified theories**, skip this workflow and continue with `verifying-performance-theories`
- If it exists but **all theories are validated and fixed**, delete it and run this skill again to generate new theories for the next optimization iteration

**Step 1**: Ask user for analysis focus using AskUserQuestion:
- All issues (comprehensive)
- Critical & high-impact only
- Implementation issues only
- Configuration issues only
- Architectural issues only

**Step 2**: Load benchmark baseline and timing results

**Step 3**: Execute systematic analysis following [WORKFLOW.md](WORKFLOW.md)

**Step 4**: Output theory list for verification

## Theory Structure

Each generated theory includes:

```
Theory: [Description of the performance issue]
Source: [Where discovered - code location, performance gap, pattern]
Category: [Implementation / Configuration / Architectural]
Severity: [Critical / High / Medium / Low]
Verification Tools:
  - Tool 1: [skill name] → Purpose: [what to check]
  - Tool 2: [skill name] → Purpose: [what to check]
Expected Evidence: [What tool output would confirm theory]
Rationale: [Why this is expected to be an issue]
```

## Analysis Categories

### Implementation Issues
- Missing specializations in operations/nodes
- Uncached method calls or library usage
- Improper boundary annotations
- Frame access patterns causing materialization

**Tool Skills for Verification**:
- `detecting-performance-warnings` - Find optimization barriers
- `profiling-with-cpu-sampler` - Identify hot functions
- `tracing-execution-counts` - Verify frequencies

### Configuration Issues
- Bytecode DSL settings
- Compilation thresholds
- Boxing elimination configuration
- Missing optimization flags

**Tool Skills for Verification**:
- `tracing-compilation-events` - Check compilation behavior
- `analyzing-compiler-graphs` - Examine IR optimizations

### Architectural Issues
- Data structure choices causing allocation
- Object shape instability
- Recursive patterns without proper caching
- Control flow preventing optimization

**Tool Skills for Verification**:
- `profiling-memory-allocations` - Track allocation patterns
- `detecting-deoptimizations` - Find instabilities
- `analyzing-compiler-graphs` - Deep IR analysis

## Systematic Code Analysis

### Step 1: Language Definition & Bytecode Configuration
```
Check @GenerateBytecode annotation settings:
- [ ] Boxing elimination enabled for primitives?
- [ ] Uncached interpreter enabled?
- [ ] Appropriate tier thresholds?
```

### Step 2: ALL Operations/Nodes
```
For EACH @Operation or Node class:
- [ ] Has primitive specializations (int, long, double)?
- [ ] Uses @Cached for method lookups?
- [ ] Proper @TruffleBoundary on slow paths?
- [ ] No virtual calls in hot paths?
```

### Step 3: Runtime Data Structures
```
For each runtime type (Object, Array, Class, Function):
- [ ] Shape stability maintained?
- [ ] Inline caching for property access?
- [ ] Efficient storage (primitives not boxed)?
```

### Step 4: Frame and Variable Access
```
- [ ] Slot access uses FrameSlotKind properly?
- [ ] No unnecessary materialization?
- [ ] Stable frame sizes?
```

### Step 5: Library and Interop Usage
```
- [ ] All @CachedLibrary has limit parameter?
- [ ] @ExportLibrary on appropriate classes?
- [ ] Interop calls cached?
```

## Priority Levels

- **Priority 1 (Critical)**: Blocks optimization entirely (missing @Cached, virtual calls in hot paths)
- **Priority 2 (High)**: Significant degradation (missing specializations, boxing overhead)
- **Priority 3 (Medium)**: Noticeable impact (suboptimal caching limits, allocation patterns)
- **Priority 4 (Low)**: Minor optimizations (code style, minor inefficiencies)

## Output Format

```markdown
# Performance Theories

Generated: [Date]
Focus: [User-selected focus]
Benchmark: [Benchmark name]

## Theory 1: [Title]

**Source**: [code location or performance gap]
**Category**: Implementation
**Severity**: Critical

**Verification Plan**:
1. `detecting-performance-warnings` → Check for virtual call warnings at [location]
2. `profiling-with-cpu-sampler` → Measure time in [function], expect >X% if theory true

**Expected Evidence**: Virtual call warning at line X, or >30% time in interpreter tier

**Rationale**: [Why this is expected to cause issues]

---

## Theory 2: [Title]
...
```

## Integration with Other Skills

**Prerequisite Skills**:
- `establishing-benchmark-baseline` → Provides BENCHMARK_BASELINE.md

**Successor Skills**:
- `verifying-performance-theories` → Verifies theories with profiling tools
- `implementing-performance-fixes` → Implements and validates fixes for verified theories

**Tool Skills Referenced**:
- `profiling-with-cpu-sampler` - Time-based profiling
- `tracing-execution-counts` - Frequency analysis
- `detecting-performance-warnings` - Optimization barriers
- `tracing-compilation-events` - Compilation analysis
- `tracing-inlining-decisions` - Inlining analysis
- `detecting-deoptimizations` - Deoptimization detection
- `profiling-memory-allocations` - Memory profiling
- `analyzing-compiler-graphs` - Deep IR analysis

## Workflow

```text
1. [establishing-benchmark-baseline] → Create baseline (PHASE 1)
2. [generating-performance-theories] → THIS SKILL (PHASE 2)
3. [verifying-performance-theories]  → Verify with tools (PHASE 3)
4. [implementing-performance-fixes]  → Implement and validate fix (PHASE 4)
5. Loop to step 2 if performance gaps remain
```

See [WORKFLOW.md](WORKFLOW.md) for detailed analysis procedures.
