---
name: parallelize
description: Use when planning parallel execution of independent tasks via subagents or concurrent tool calls; for workflow planning or throughput optimization.
allowed-tools: ["read_file", "update_plan"]
metadata:
  short-description: Analyze parallelization opportunities
---

# Parallelization Analysis

**Read this reference:**
- `references/parallelization.md` - Concurrent execution patterns and strategies

## Instructions

**Important**: This is about parallelizing **implementation work** (spawning subagents, concurrent tool calls), NOT writing parallel code.

### Analysis Steps

1. **Identify independent work units**
   - Which tasks have no dependencies?
   - What can be done simultaneously?
   - Where are the blocking dependencies?

2. **Map dependency graph**
   - Draw (mentally or explicitly) dependencies
   - Identify critical path (longest sequential chain)
   - Find parallelizable branches

3. **Calculate potential speedup**
   - How much work can run concurrently?
   - What's the theoretical maximum speedup?
   - What are the practical constraints?

4. **Design execution strategy**
   - Spawn multiple subagents for independent work
   - Use parallel tool calls where possible
   - Batch independent operations
   - Minimize sequential bottlenecks

### Parallelization Patterns

**Pattern 1: Independent Reads**
```
Read file A, Read file B, Read file C in parallel
→ Process results sequentially if needed
```

**Pattern 2: Independent Analysis**
```
Analyze module A, Analyze module B in parallel
→ Combine results
```

**Pattern 3: Pipeline Parallelism**
```
Stage 1 (Task A) → Stage 2 (Tasks B, C in parallel) → Stage 3 (Task D)
```

### Dispatching Parallel Work (Codex-compatible)

When tasks are independent, batch tool calls in a single message or use `multi_tool_use.parallel` for concurrent reads/analysis. Keep scopes narrow and independent to avoid conflicts.

### Per AGENT.md

"Always use subagents wherever possible to speed up work" - apply this principle throughout.

## Arguments

Work to analyze for parallelization: ${ARGUMENTS}
