# Task Planner Templates

Reference templates for task-planner skill. Load on demand, not part of core workflow.

## Agent Context Template

When spawning impl agents, use this format:

```markdown
## Task Assignment

**Task ID:** T2
**Wave:** 1
**Agent:** code-implementer-agent
**Dependencies:** None

## Your Task

{task description}

## Context from Plan

> **Architecture Decision:**
> {relevant section from plan}

> **Files to Create/Modify:**
> {file list}

## Full Plan

Available at: {plan_file path from state}

## Constraints

- Follow patterns in plan
- Do not modify scope
- MUST write tests for your implementation
- MUST run tests and ensure they pass before completing
- Task is NOT complete until tests pass
```

## GitHub Issue Format

Issue body structure with checkbox tasks:

```markdown
## Plan: {title}

### Context & Analysis
{codebase exploration findings}

### Architecture Decisions
{design choices with rationale}

### Task Breakdown

#### Wave 1: {description} (parallel)
- [ ] T1: {task description}
- [ ] T2: {task description}

#### Wave 2: {description} (depends on Wave 1)
- [ ] T3: {task description}

### Execution Order

| ID | Task | Agent | Wave | Depends |
|----|------|-------|------|---------|
| T1 | ... | code-implementer-agent | 1 | - |

### Verification Checklist
- [ ] All tests pass
- [ ] No security vulnerabilities
- [ ] Code reviewed

### Related PRs
<!-- Auto-updated by hooks -->
```

## State File Schema

```json
{
  "plan_file": ".claude/plans/YYYY-MM-DD-slug.md",
  "issue": 42,
  "current_wave": 1,
  "executing_tasks": [],
  "tasks": [{
    "id": "T1",
    "description": "...",
    "agent": "code-implementer-agent",
    "wave": 1,
    "depends_on": [],
    "status": "pending|in_progress|implemented|completed",
    "review_status": "pending|passed|blocked",
    "critical_findings": [],
    "advisory_findings": []
  }],
  "wave_gates": {
    "1": {
      "impl_complete": false,
      "tests_passed": null,
      "reviews_complete": false,
      "blocked": false
    }
  }
}
```
