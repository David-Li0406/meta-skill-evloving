---
name: optimizing-truffle-performance
description: "[ORCHESTRATOR] Runs full performance optimization loop for Truffle languages. Entry: User wants to optimize performance. Process: Determines current state, executes appropriate phase (1→2→3→4), loops until performance meets expectations. IMPORTANT: Single entry point for all optimization work."
---

# Optimizing Truffle Performance

Orchestrates the complete performance optimization workflow. Single entry point that manages state, transitions, and termination.

## Quick Start

**Step 1**: Determine current state (see State Detection below)

**Step 2**: Execute the appropriate phase skill

**Step 3**: After phase completes, re-evaluate state and continue or terminate

## State Detection

Check files in this order to determine current phase:

```text
1. BENCHMARK_BASELINE.md exists?
   NO  → Execute PHASE 1 (establishing-benchmark-baseline)
   YES → Continue to check 2

2. PERFORMANCE_THEORIES.md exists?
   NO  → Execute PHASE 2 (generating-performance-theories)
   YES → Continue to check 3

3. Any theory with status "verified"?
   YES → Execute PHASE 4 (implementing-performance-fixes)
   NO  → Continue to check 4

4. Any theory with status "pending" or unverified?
   YES → Execute PHASE 3 (verifying-performance-theories)
   NO  → Continue to check 5

5. All theories "fixed" or "fix-failed" or "falsified"?
   YES → Evaluate termination (see below)
   NO  → Error state, ask user
```

## Phase Skills

| Phase | Skill | Purpose |
|-------|-------|---------|
| 1 | `establishing-benchmark-baseline` | Create benchmarks and baseline |
| 2 | `generating-performance-theories` | Analyze code, generate theories |
| 3 | `verifying-performance-theories` | Prove/disprove theories with tools |
| 4 | `implementing-performance-fixes` | Implement fix, validate improvement |

## Termination Criteria

After all theories are processed (fixed/fix-failed/falsified), evaluate:

**Continue optimization (loop to PHASE 2)** if:

- Performance still below baseline expectations (check BENCHMARK_BASELINE.md)
- User requests more optimization
- Significant performance gaps remain (>20% slower than expected)

**Stop optimization** if:

- Performance meets or exceeds baseline expectations
- User indicates satisfaction
- No more theories can be generated (diminishing returns)
- All recent fixes failed (indicates deeper issues)

## Edge Cases

| Situation | Action |
|-----------|--------|
| All theories falsified | Loop to PHASE 2 with different focus |
| No performance gap found | Optimization complete, congratulate user |

## Workflow Visualization

```text
                    ┌─────────────────────────────────────┐
                    │                                     │
                    ▼                                     │
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐ │
│ PHASE 1 │───▶│ PHASE 2 │───▶│ PHASE 3 │───▶│ PHASE 4 │─┘
│Baseline │    │Theories │    │ Verify  │    │  Fix    │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
                    ▲                             │
                    │         (if gaps remain)    │
                    └─────────────────────────────┘
                              │
                              ▼ (if done)
                         ┌─────────┐
                         │  DONE   │
                         └─────────┘
```

## Orchestrator Checklist

Copy this to track progress:

```text
Optimization Progress:
- [ ] State determined
- [ ] PHASE 1: Baseline established (BENCHMARK_BASELINE.md exists)
- [ ] PHASE 2: Theories generated (PERFORMANCE_THEORIES.md exists)
- [ ] PHASE 3: Theory verified (at least one verified)
- [ ] PHASE 4: Fix implemented and validated
- [ ] Termination evaluated
- [ ] Loop or complete
```

## Integration

This skill CALLS the phase skills:

- `establishing-benchmark-baseline` (PHASE 1)
- `generating-performance-theories` (PHASE 2)
- `verifying-performance-theories` (PHASE 3)
- `implementing-performance-fixes` (PHASE 4)

This skill does NOT call tool skills directly. Tool skills are called by PHASE 3.

