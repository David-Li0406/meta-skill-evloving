---
name: implementing-performance-fixes
description: "[PHASE 4] Implements and validates fixes for verified theories. Entry: PERFORMANCE_THEORIES.md has a verified theory. Outputs: Code fix, BENCHMARK_BASELINE.md new column, theory marked fixed/fix-failed. Next: Loop to PHASE 2 if performance gaps remain, otherwise done."
---

# Implementing Performance Fixes

Transforms verified performance theories into working fixes with measured validation.

## Core Principle

**Verified theories identify the problem. This skill implements and validates the solution.**

## Prerequisites

- **REQUIRED**: `PERFORMANCE_THEORIES.md` with at least one theory status `verified`
- **REQUIRED**: `BENCHMARK_BASELINE.md` with benchmark descriptions and execution commands
- **REQUIRED**: Theory verification evidence from `verifying-performance-theories`

## Quick Start

**Step 1**: Load the most critical verified theory from `PERFORMANCE_THEORIES.md`

**Step 2**: Design fix approach (see [WORKFLOW.md](WORKFLOW.md) Phase 2)

**Step 3**: Implement the fix

**Step 4**: Run 3 relevant benchmarks to validate (select based on benchmark focus in BENCHMARK_BASELINE.md)

**Step 5**: Based on results:

- **Improved** → Keep fix, run all benchmarks, update files
- **Degraded** → Revert fix, update theory status

## Workflow Overview

```text
1. Load verified theory with evidence
2. Design fix (architectural changes allowed if cost-benefit fits)
3. Implement fix
4. Run 3 relevant benchmarks
5a. If improved → run all benchmarks → update BENCHMARK_BASELINE → mark theory "fixed"
5b. If degraded → revert → mark theory "fix-failed"
```

## Benchmark Selection

Select 3 benchmarks from BENCHMARK_BASELINE.md based on their documented focus:

1. Read each benchmark's **Rationale** field
2. Match rationale to the code path affected by your fix
3. Prioritize benchmarks that exercise the fixed code

## File Updates

### BENCHMARK_BASELINE.md

Add new column to results table:

```markdown
| Benchmark | Baseline | After Fix #N |
|-----------|----------|--------------|
| queens    | 32ms     | 24ms         |
```

### PERFORMANCE_THEORIES.md

Update theory status:

```markdown
**Status**: fixed  <!-- was: verified -->
**Fix Applied**: [Date] - [Brief description of fix]
**Performance Impact**: [X% improvement on benchmark Y]
```

Or if fix failed:

```markdown
**Status**: fix-failed  <!-- was: verified -->
**Fix Attempted**: [Date] - [What was tried]
**Reason**: [Why it didn't improve performance]
```

## Status Values

| Status | Meaning |
|--------|---------|
| `verified` | Theory proven, awaiting fix |
| `fixed` | Fix applied and validated |
| `fix-failed` | Fix attempted but reverted |
| `falsified` | Theory disproven during verification |

## Integration

**Predecessor**: `verifying-performance-theories` → Provides verified theories

**Successor**: Loop back to `generating-performance-theories` if more issues exist

## Workflow Position

```text
1. [establishing-benchmark-baseline] → Create baseline (PHASE 1)
2. [generating-performance-theories] → Generate theories (PHASE 2)
3. [verifying-performance-theories]  → Verify with tools (PHASE 3)
4. [implementing-performance-fixes]  → THIS SKILL (PHASE 4)
5. Loop to step 2 if performance gaps remain
```

See [WORKFLOW.md](WORKFLOW.md) for detailed phase instructions.
