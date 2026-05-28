---
name: executing-tasks
description: Provides reusable 6-phase task execution workflow for any task type including context gathering, planning, execution, quality check, progress update, and learning documentation. This skill should be used when implementing tasks from story breakdowns, executing development work, or running structured task workflows. Triggers on "execute task", "task workflow", "implement task", "task phases", "quality check", "run task", "complete task".
---

# Task Execution

Standardized 6-phase workflow for executing any task type with consistent quality gates and progress tracking. Integrates with sprint-orchestration for task assignment and progress updates.

## 6-Phase Workflow

```text
[1. CONTEXT] --> [2. PLANNING] --> [3. EXECUTION] --> [4. QUALITY] --> [5. PROGRESS] --> [6. LEARNING]
     |               |                  |                 |                |                 |
  Load skill    TodoWrite tasks    Execute work      Verify results   Update YAML      Document
  Gather info   15-30 min chunks   Atomic commits    Run checks       Comment issue    learnings
```

## Phase Summary

| Phase | Purpose | Key Actions |
|-------|---------|-------------|
| 1. Context | Gather task-specific information | Load relevant skills, read specs/designs, identify dependencies |
| 2. Planning | Break work into trackable units | TodoWrite with 15-30 min granularity, identify parallelizable work |
| 3. Execution | Implement the actual work | Follow task-type patterns, atomic commits, delegate to subagents |
| 4. Quality | Verify correctness | Run verification commands, record results, handle errors |
| 5. Progress | Update tracking systems | PROGRESS.yaml transitions, GitHub issue comments, metrics |
| 6. Learning | Capture improvements | Document blockers, patterns discovered, process improvements |

## Completion Criteria by Task Type

| Task Type | Verification | Success Criteria |
|-----------|--------------|------------------|
| Code implementation | `npm run typecheck && npm run test` | All tests pass, no type errors |
| Test writing | `npm run test -- <test-file>` | Tests pass, coverage meets target |
| Documentation | Frontmatter validation, link checks | AI-readable, accurate content |
| Refactoring | Tests pass, no behavior change | All existing tests green |
| Bug fix | Regression test added and passes | Issue resolved, test prevents recurrence |
| Configuration | Manual verification or smoke test | System functions correctly |

## Quality Gates

Before transitioning from Execution (Phase 3) to Quality (Phase 4):
- All planned TodoWrite items completed or explicitly deferred
- Atomic commits made for logical units of work
- No uncommitted changes unless intentionally staged

Before transitioning from Quality (Phase 4) to Progress (Phase 5):
- All verification commands executed
- Any failures documented with root cause
- Re-execution loop if quality checks fail

## References

| Reference | Purpose |
|-----------|---------|
| `references/phase-1-context.md` | Context gathering strategies by task type |
| `references/phase-2-planning.md` | TodoWrite patterns and task granularity |
| `references/phase-3-execution.md` | Execution patterns and subagent delegation |
| `references/phase-4-quality.md` | Quality gates and error handling |
| `references/phase-5-progress.md` | PROGRESS.yaml updates and issue commenting |
| `references/phase-6-learning.md` | Learning documentation format |
| `assets/task-prompt-template.md` | Ralph-loop prompt template for task execution |
