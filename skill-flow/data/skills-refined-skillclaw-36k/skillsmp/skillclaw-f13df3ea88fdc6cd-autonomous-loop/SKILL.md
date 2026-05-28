---
name: autonomous-loop
description: Use this skill when you want to implement features autonomously, fix bugs in a loop, or run until completion, leveraging iterative self-improvement patterns.
---

# Autonomous Development Loop

Based on [Geoffrey Huntley's Ralph technique](https://github.com/frankbria/ralph-claude-code) for Claude Code.

> **For full autonomous mode, use `/ralph`.** This skill provides the underlying patterns.

## Core Principle: Dual-Condition Exit Gate

**Never exit prematurely.** Exit requires BOTH conditions:

1. **Completion Indicators ≥ 2** - Heuristic detection from your work
2. **Explicit EXIT_SIGNAL: true** - Your conscious declaration

**If only ONE is true → KEEP GOING**

This innovation (introduced in ralph-claude-code v0.9.9) prevents false exits when completion language appears during productive work.

## Completion Indicators

Count how many apply each loop:

| Indicator         | Pattern                                    |
| ----------------- | ------------------------------------------ |
| Tests passing     | 100% pass rate                             |
| Fix plan complete | All `- [ ]` → `- [x]`                      |
| "Done" language   | "done", "complete", "finished"             |
| "Nothing to do"   | "no changes needed", "already implemented" |
| "Ready" language  | "ready for review", "ready to merge"       |
| No errors         | Zero execution errors                      |

**Need ≥2 indicators + explicit EXIT_SIGNAL: true to exit**

## Circuit Breaker Pattern

Track your own progress and halt when stuck:

| State         | Condition                | Action             |
| ------------- | ------------------------ | ------------------ |
| **CLOSED**    | Normal operation         | Continue executing |
| **HALF_OPEN** | 2 loops without progress | Increase scrutiny  |
| **OPEN**      | Threshold exceeded       | HALT immediately   |

### Halt Thresholds

| Trigger           | Threshold     | Meaning             |
| ----------------- | ------------- | ------------------- |
| No progress loops | 3 consecutive | Spinning wheels     |
| Identical errors  | 5 consecutive | Stuck on same issue |
| Test-only loops   | 3 consecutive | Not implementing    |
| Output decline    | >70% drop     | Something's wrong   |

## Progress Detection

Track mentally each loop:

- **Files modified** (0 = no progress)
- **Tests changed** (pass/fail delta)
- **Tasks completed** (0 = no progress)