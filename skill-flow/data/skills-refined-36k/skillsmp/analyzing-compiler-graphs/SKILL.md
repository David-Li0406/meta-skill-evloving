---
name: analyzing-compiler-graphs
description: Dumps and analyzes Graal IR compiler graphs showing optimization decisions. Use BGV format with bgv2json/seafoam to inspect escape analysis, boxing removal, inlining decisions, and call node types. Reveals what compiler actually optimized vs intended. Use as last resort after basic profiling when root cause remains unclear.
---

# Analyzing Compiler Graphs

Deep-dive tool for understanding Graal compiler optimization decisions at the IR level. Dumps BGV files and analyzes them to reveal exactly what the compiler optimized.

## When to Use This Skill

**Use AFTER simpler profiling tools** when:
- Other tools show problems but don't reveal root cause
- Need to understand WHY optimization fails
- Investigating allocation elimination issues
- Debugging polymorphism and specialization

**Prerequisites**:
1. ✅ CPU profiling identified hot methods
2. ✅ Performance warnings revealed optimization barriers
3. ✅ Compilation/inlining traces showed issues
4. ✅ bgv2json or Seafoam installed

## Quick Start

### 1. Dump Compiler Graphs

```bash
# Basic dump for Truffle compilations
<launcher> --vm.Djdk.graal.Dump=Truffle:1 \
  --vm.Djdk.graal.PrintGraph=File \
  --vm.Djdk.graal.DumpPath=compiler_graphs \
  <program>

# Focused dump for specific method (recommended)
<launcher> --vm.Djdk.graal.Dump=Truffle:1 \
  --vm.Djdk.graal.MethodFilter='*hotFunction*' \
  --vm.Djdk.graal.DumpPath=compiler_graphs \
  --engine.CompileOnly='*hotFunction*' \
  <program>
```

### 2. Analyze with Seafoam

```bash
# Get help
seafoam help

# Describe graph characteristics
seafoam --json compiler_graphs/*.bgv.gz:2 describe

# Render to SVG
seafoam compiler_graphs/*.bgv.gz:2 render > graph.svg
```

### 3. Convert to JSON for Custom Analysis

```bash
bgv2json compiler_graphs/*.bgv > graphs.json
```

See [DUMPING.md](DUMPING.md) for detailed dump options.
See [QUERIES.md](QUERIES.md) for jq analysis queries.

## ⚠️ REQUIRED: Fermi Verification (Every Tool Invocation)

**Before dumping graphs**:
- [ ] Pre-calculate: Expected # of BGV files (1 per compiled function, typically 5-20)
- [ ] Smoke test: Dump trivial program first → Verify BGV files generated

**After dumping**:
- [ ] Validate: BGV file count within expectation? YES / NO
- [ ] If NO: **STOP** - Check MethodFilter, verify functions compiled
- [ ] List BGV files: `ls -lh compiler_graphs/*.bgv`

**After analyzing graphs**:
- [ ] Validate: Node counts reasonable? YES / NO
- [ ] If NO: **STOP** - May have wrong phase or too broad filter
- [ ] Save analysis: `tool-outputs/compiler-graph-analysis-[function].txt`

**Gate**: All boxes checked? → Proceed to interpretation

## Key Phases to Analyze

| Phase | Purpose | What to Check |
|-------|---------|---------------|
| After TruffleTier | **Most important** | Direct calls, constant nodes, no VirtualFrame refs |
| After PartialEscape | Allocation elimination | Zero allocation nodes if EA worked |
| Final | Generic Graal optimizations | Overall node reduction |

## Quick Problem Detection

### Check for Indirect Calls (Performance Problem!)

```bash
seafoam --json file.bgv.gz:2 describe | \
  jq '.node_counts | to_entries | .[] | select(.key | contains("Call"))'
```

**Good**: `OptimizedDirectCallNode`
**Bad**: `OptimizedIndirectCallNode`, `InvokeNode`

### Check for Failed Escape Analysis

```bash
cat graphs.json | jq 'select(.name | contains("After PartialEscape")) |
  .nodes[] | select(.props.label | test("Alloc|New"))'
```

**Good**: Empty output
**Bad**: `CommitAllocationNode`, `NewInstanceNode` present

### Check for Boxing

```bash
seafoam --json file.bgv.gz:2 describe | \
  jq '.node_counts | to_entries | .[] | select(.key | test("Box|Unbox"))'
```

**Good**: Empty output
**Bad**: `BoxNode`, `UnboxNode` present

## Node Types Reference

### Good Patterns (Optimized)
- `OptimizedDirectCallNode` - Specialized calls ✅
- `AddNode`, `MulNode`, `SubNode` - Primitive arithmetic ✅
- `ConstantNode` - Constants from partial evaluation ✅

### Bad Patterns (Need Fixes)
- `OptimizedIndirectCallNode` - Need caching ⚠️
- `InvokeNode` - Unspecialized method calls ⚠️
- `CommitAllocationNode`, `NewInstanceNode` - Escape analysis failed ⚠️
- `BoxNode`, `UnboxNode` - Missing primitive specializations ⚠️
- `DeoptimizeNode` in hot paths - Unstable assumptions ⚠️

## Common Problem Patterns

### Problem 1: Indirect Calls
**Fix**: Add `@Cached` for CallTarget lookup

### Problem 2: Failed Escape Analysis
**Fix**: Keep object lifetime strictly local

### Problem 3: Boxing/Unboxing
**Fix**: Add primitive specializations

See [PATTERNS.md](PATTERNS.md) for detailed fix examples.

## Best Practices

1. **Always use MethodFilter** - Avoid overwhelming output
2. **Start with Level 1** - Only use Level 2 when needed
3. **Focus on "After TruffleTier"** - Most relevant for language developers
4. **Compress BGV files** - `gzip compiler_graphs/*.bgv`
5. **Correlate with other tools** - Use with TraceCompilation, TracePerformanceWarnings

## Related Skills

- `profiling-with-cpu-sampler` - Identify hot functions FIRST
- `detecting-performance-warnings` - Find optimization barriers
- `tracing-compilation-events` - See compilation events
- `tracing-inlining-decisions` - Check inlining
- `detecting-deoptimizations` - Find instabilities
- `fetching-truffle-documentation` - API reference

## Detailed Documentation

- [DUMPING.md](DUMPING.md) - Dump options and commands
- [QUERIES.md](QUERIES.md) - jq analysis queries
- [PATTERNS.md](PATTERNS.md) - Problem patterns and fixes
