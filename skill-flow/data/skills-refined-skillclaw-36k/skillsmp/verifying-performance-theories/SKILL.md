---
name: verifying-performance-theories
description: "[PHASE 3] Proves theories with profiling tools. Entry: PERFORMANCE_THEORIES.md has unverified theories. Outputs: Theory marked verified/falsified. Next: PHASE 4 (implementing-performance-fixes) when one theory is verified."
---

# Verifying Performance Theories

Systematically verifies performance theories using profiling tools. Enforces rigorous methodology to ensure only proven issues make it into the final report.

## Core Principle

**Code analysis finds POTENTIAL issues. Tools PROVE which issues actually matter.**

## Quick Start

**Input**: List of theories from `generating-performance-theories` skill

**Approach**: Verify one theory at a time, highest-severity first. If the most critical theory is already verified and fixed, or has been falsified, skip it and continue with the next critical theory. Fix verified issues, re-profile, continue.

**Output**: Verified findings for `generating-performance-reports`

## Workflow Overview

1. **Select** highest-priority unverified theory
2. **Prepare** - load tool docs, form expectations (Fermi estimation)
3. **Execute** verification - use profiling tools OR direct implementation (if fix is <10 lines)
4. **Handle emergent issues** - pivot if more critical, note as future work if not
5. **Synthesize** evidence → VERIFIED / FALSIFIED / INCONCLUSIVE
6. **Next steps** - if verified, recommend fix and stop; otherwise continue

See [WORKFLOW.md](WORKFLOW.md) for detailed procedures.

## Tool Skills

| Purpose | Tool Skill |
|---------|-----------|
| Hot function identification | `profiling-with-cpu-sampler` |
| Execution frequency | `tracing-execution-counts` |
| Optimization barriers | `detecting-performance-warnings` |
| Compilation behavior | `tracing-compilation-events` |
| Inlining analysis | `tracing-inlining-decisions` |
| Type stability | `detecting-deoptimizations` |
| Allocation patterns | `profiling-memory-allocations` |
| Deep IR analysis | `analyzing-compiler-graphs` |

**Note on Compiler Graphs**: When theories come from code analysis (e.g., "this allocation should be eliminated"), compiler graphs provide **direct evidence** of what the compiler actually did. Use them early for allocation/boxing theories, not as a last resort.

## Common Pitfalls

- ❌ **Substituting code analysis for tool verification** - Code shows potential, tools prove actuality
- ❌ **Running only one tool** - Multiple tools required for confidence
- ❌ **Skipping Fermi verification** - Silent tool failures produce garbage data
- ❌ **Over-profiling simple fixes** - If the fix is small (<10 lines), implement and benchmark instead of extensive profiling
- ❌ **Ignoring emergent issues** - If tools reveal a critical issue (like deopt loops), evaluate whether to pivot
- ❌ **Always pivoting** - Only pivot if the new issue is MORE critical than the current theory

## Related Skills

**Predecessor**: `generating-performance-theories` → Provides theories to verify

**Successor**: `implementing-performance-fixes` → Implements and validates fixes for verified theories

**Tool Skills Used**:
- `profiling-with-cpu-sampler`
- `tracing-execution-counts`
- `detecting-performance-warnings`
- `tracing-compilation-events`
- `tracing-inlining-decisions`
- `detecting-deoptimizations`
- `profiling-memory-allocations`
- `analyzing-compiler-graphs`

## Workflow Position

```text
1. [establishing-benchmark-baseline] → Create baseline (PHASE 1)
2. [generating-performance-theories] → Generate theories (PHASE 2)
3. [verifying-performance-theories]  → THIS SKILL (PHASE 3)
4. [implementing-performance-fixes]  → Implement and validate fix (PHASE 4)
5. Loop to step 2 if performance gaps remain
```
