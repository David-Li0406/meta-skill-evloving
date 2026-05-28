# faion-feature-executor

SDD feature executor with quality gates: sequential task execution, test/coverage validation after each task, code review cycles until all issues resolved.

## Overview

This skill orchestrates complete feature implementation in the SDD workflow:

1. **Context Loading** - Load project constitution, feature spec, design, and implementation plan
2. **Task Discovery** - Find tasks in `in-progress/` (resume) and `todo/` (new)
3. **Task Execution Loop** - Execute each task via `faion-task-executor-agent` with post-task validation (tests, coverage, build)
4. **Code Review Cycle** - Iterate with `faion-code-agent` until no issues remain
5. **Finalize** - Move feature to `done/`, generate summary report

## Usage

```
/faion-feature-executor {project} {feature}
```

**Examples:**
```
/faion-feature-executor cashflow-planner 01-auth
/faion-feature-executor faion-net 02-landing-page
```

## Agents Used

| Agent | Purpose |
|-------|---------|
| `faion-task-executor-agent` | Execute individual tasks |
| `faion-code-agent` | Code review (review mode) |
| `faion-test-agent` | Test execution and coverage analysis |
| `faion-hallucination-checker-agent` | Verify task completion claims |

## Quality Gates

After each task:
- All tests pass
- Coverage meets threshold (default 80%)
- Project builds and runs

After all tasks:
- Code review passes (max 5 iterations)
- No critical/security issues
- No style violations

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Full skill specification with workflow details |
| `CLAUDE.md` | This navigation file |

## Integration

Part of SDD workflow:
```
SPEC -> DESIGN -> IMPL-PLAN -> TASKS -> [FEATURE-EXECUTOR] -> DONE
```

Related skills: `faion-sdd`, `faion-task-executor-agent`

---

*v1.0.0 | 2026-01-18*
