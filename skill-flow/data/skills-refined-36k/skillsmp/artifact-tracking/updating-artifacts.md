# UPDATE Function: Updating Task Status & Progress

Use artifact-tracker agent for surgical field-level updates.

## Routing Decision: CLI vs Agent

**Use CLI scripts first** - they cost ~50-100 tokens vs ~4,000+ for agent operations.

| Scenario | Method | Command |
|----------|--------|---------|
| Mark task complete | **CLI** | `python scripts/update-status.py -f FILE -t TASK-X -s completed` |
| Mark task blocked | **CLI** | `python scripts/update-status.py -f FILE -t TASK-X -s blocked -n "reason"` |
| Batch update (2+ tasks) | **CLI** | `python scripts/update-batch.py -f FILE --updates "T1:completed,T2:completed"` |
| Update with detailed notes | Agent | `Task("artifact-tracker", "Update... with context: ...")` |
| Record architectural decision | Agent | `Task("artifact-tracker", "Record decision: ...")` |
| Add blocker with resolution plan | Agent | `Task("artifact-tracker", "Add blocker...")` |

**Rule of thumb**: If it's just a status change, use CLI. If you need to record context/reasoning, use agent.

---

## Update Task Status

**Command**:
```markdown
Task("artifact-tracker", "Update [PRD] phase [N]: Mark TASK-X.Y as [status]")
```

**Status Values**: `pending`, `in_progress`, `complete`, `blocked`, `at_risk`

## Update With Notes

**Command**:
```markdown
Task("artifact-tracker", "Update [PRD] phase [N]: Mark TASK-X.Y as complete.
Note: 'Implementation complete, tests passing'")
```

## Update Progress Percentage

**Command**:
```markdown
Task("artifact-tracker", "Update [PRD] phase [N]: Set overall progress to 60%")
```

## Add Blocker

**Command**:
```markdown
Task("artifact-tracker", "Update [PRD] phase [N]: Add blocker BLOCKER-001.
Title: 'Missing API endpoint'. Severity: high. Blocking: TASK-2.3, TASK-2.4")
```

## Resolve Blocker

**Command**:
```markdown
Task("artifact-tracker", "Update [PRD] phase [N]: Resolve BLOCKER-001.
Resolution: 'Backend endpoint deployed'")
```

## Add Context Note

**Command**:
```markdown
Task("artifact-tracker", "Add note to [PRD] context:
Decision: Using SVG paths for connectors instead of CSS
Rationale: Better button positioning on paths
Location: components/flow-banner.tsx:45")
```

## Batch Update (Multiple Tasks)

**Command**:
```markdown
Task("artifact-tracker", "Update [PRD] phase [N]:
- TASK-1.1: complete
- TASK-1.2: complete
- TASK-2.1: in_progress
- Overall progress: 45%")
```

## What Gets Updated

When status changes, artifact-tracker automatically updates:
- YAML `tasks[].status` field
- YAML `completed_tasks`, `in_progress_tasks`, `blocked_tasks` counts
- YAML `progress` percentage (recalculated)
- YAML `updated` timestamp
- Markdown task table row

## Token Efficiency

Updates are surgical (~500 bytes) vs full-file rewrites (~25KB):
- Edit only YAML fields that changed
- Update only affected markdown table row
- Don't touch other sections

## Best Practices

1. **Update immediately** after task completion (don't batch)
2. **Include notes** for context on decisions or gotchas
3. **Use artifact-tracker** (not manual Edit) for consistency
4. **Mark blockers** when tasks can't proceed
