---
title: Phase 3 - Execution
description: Execution patterns by task type, subagent delegation rules, and commit conventions for task execution
keywords: execution, implementation, subagent, delegation, commits
file-type: reference
skill: executing-tasks
---

# Phase 3: Execution

## Execution Patterns by Task Type

| Task Type | Pattern | Commit Frequency |
|-----------|---------|------------------|
| Code implementation | Read -> Edit -> Verify -> Commit | Per logical unit |
| Test writing | Write test -> Run -> Fix -> Commit | Per test file |
| Documentation | Draft -> Validate -> Commit | Per document |
| Refactoring | Extract -> Transform -> Verify -> Commit | Per refactor step |
| Bug fix | Reproduce -> Fix -> Add test -> Commit | Single commit |
| Configuration | Change -> Verify -> Commit | Single commit |

## Subagent Delegation Rules

**Delegate when:**
- Task is independent and well-defined
- Work can proceed in parallel
- Specialized expertise benefits task

**Keep in main agent when:**
- Task requires cross-cutting context
- Sequential dependency on previous work
- Coordination complexity exceeds delegation benefit

**Delegation pattern:**
```javascript
Task(
  subagent_type="appropriate-type",
  prompt="Clear task description with success criteria"
)
```

| Subagent Type | Delegate For |
|---------------|--------------|
| coder | Independent implementation units |
| tester | Test suite creation |
| researcher | Background investigation |
| reviewer | Code review, quality assessment |

## Commit Conventions

**Commit message format:**
```
<type>(<scope>): <description>

<body - optional>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Types:** feat, fix, refactor, test, docs, chore

**Atomic commit rules:**
- One logical change per commit
- Tests pass after each commit
- No WIP commits to main branch
- Reference task ID in scope when applicable

## Execution Checklist

- [ ] Update TodoWrite item to "in_progress"
- [ ] Execute according to task-type pattern
- [ ] Make atomic commits at logical boundaries
- [ ] Update TodoWrite item to "completed"
- [ ] Proceed to next item or delegate parallel work
