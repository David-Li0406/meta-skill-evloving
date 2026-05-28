---
title: Phase 5 - Progress Update
description: PROGRESS.yaml update patterns, GitHub issue commenting, and task state transitions for progress tracking
keywords: progress, yaml, github, issues, tracking, transitions
file-type: reference
skill: executing-tasks
---

# Phase 5: Progress Update

## YAML Update Patterns

**Task state transitions:**
```yaml
# Before execution
tasks:
  - id: "T-001"
    title: "Implement feature X"
    status: pending

# After successful execution
tasks:
  - id: "T-001"
    title: "Implement feature X"
    status: completed
    completed_at: "2024-01-14T10:30:00Z"
```

**Valid status values:**
| Status | Meaning | Transition From |
|--------|---------|-----------------|
| pending | Not started | initial |
| in_progress | Currently executing | pending |
| completed | Successfully finished | in_progress |
| blocked | Waiting on dependency | pending, in_progress |
| deferred | Postponed intentionally | pending, in_progress |

**PROGRESS.yaml location:**
- Story-level: `specs/<epic-id>/<story-id>/PROGRESS.yaml`
- Task tracked within story's tasks array

## GitHub Issue Commenting

**When to comment:**
- Task started (brief note)
- Task completed (summary of changes)
- Task blocked (blocker description)
- Significant progress milestone

**Comment format:**
```markdown
## Task T-001: [Status]

**Changes:**
- [List of commits/changes]

**Quality:**
- Tests: [pass/fail]
- Build: [pass/fail]

**Next:** [Next task or blocker]
```

**gh CLI pattern:**
```bash
gh issue comment <issue-number> --body "$(cat <<'EOF'
## Task Update
[content]
EOF
)"
```

## Task Transitions

**Transition rules:**
| Current | Valid Next | Trigger |
|---------|------------|---------|
| pending | in_progress | Execution starts |
| in_progress | completed | Quality gates pass |
| in_progress | blocked | Dependency discovered |
| blocked | in_progress | Blocker resolved |
| any | deferred | Intentional postponement |

**Never:**
- Skip pending -> completed (must go through in_progress)
- Move completed -> pending (create new task instead)

## Progress Checklist

- [ ] Update PROGRESS.yaml task status
- [ ] Add completed_at timestamp if completed
- [ ] Comment on GitHub issue if linked
- [ ] Update story-level progress if all tasks done
- [ ] Note any blockers for subsequent tasks
