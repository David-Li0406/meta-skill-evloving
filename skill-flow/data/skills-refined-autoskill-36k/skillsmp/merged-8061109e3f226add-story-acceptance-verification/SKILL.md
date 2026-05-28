---
name: story-acceptance-verification
description: Use this skill to verify and close stories after ensuring all related frontend and backend tasks are completed.
---

# Story Acceptance

## Language Configuration

Before generating any content, check `aico.json` in the project root for the `language` field to determine the output language. If not set, default to English.

## Process

1. **Identify the story**: Get the story ID (e.g., S-001) from notification or user.
2. **Read the story**: Load `docs/reference/pm/stories/{story-id}.md`.
3. **Find related tasks**:
   - Check `docs/reference/frontend/tasks/` for frontend tasks.
   - Check `docs/reference/backend/tasks/` for backend tasks.
4. **Verify all tasks completed**:
   - Read each task file's `> **Status**:` field.
   - All task statuses should be `✅ completed`.
   - No `⏳ pending` or `🔄 in_progress` tasks remaining.
5. **Update story**:
   - If ALL tasks completed → Update acceptance criteria `- [ ]` to `- [x]`.
   - If partial → Report progress, list incomplete tasks.

## Verification Checklist

```markdown
## Story: S-XXX

### Frontend Tasks

- [x] docs/reference/frontend/tasks/s-xxx.md - All completed

### Backend Tasks

- [x] docs/reference/backend/tasks/s-xxx.md - All completed

### Result: ✅ Ready to close / ⏳ Waiting for tasks
```

## Task Status Mapping

| Task Status      | Meaning           |
| ---------------- | ----------------- |
| `✅ completed`   | Task done         |
| `🔄 in_progress` | Currently working  |
| `⏳ pending`     | Not started       |

## Story Update Format

When all tasks are complete, update the story file:

```markdown
## Acceptance Criteria

- [x] Criterion 1 (was `- [ ]`)
- [x] Criterion 2 (was `- [ ]`)
- [x] Criterion 3 (was `- [ ]`)
```

## Decision Logic

```
Has frontend tasks? ──Yes──> Check frontend/tasks/{story}.md
        │                            │
        No                     All completed?
        │                       │        │
        ▼                      Yes       No
Has backend tasks? ──Yes──> Check backend/tasks/{story}.md
        │                            │
        No                     All completed?
        │                       │        │
        ▼                      Yes       No
All checks passed? ─────────────┘        │
        │                                │
       Yes                              No
        │                                │
        ▼                                ▼
Update story checkboxes          Report incomplete tasks
```

## Key Rules

- MUST check BOTH frontend and backend tasks before closing.
- ONLY update story when ALL related tasks are completed.
- ALWAYS report which tasks are still pending if not ready to close.
- Use exact checkbox format: `- [x]` for completed, `- [ ]` for pending.

## Output Examples

### All Complete

```
## Story S-001 Acceptance Result

✅ **Ready to Close**

### Task Check
- Frontend: 3/3 completed
- Backend: 2/2 completed

Story acceptance criteria updated.
```

### Partial Complete

```
## Story S-001 Acceptance Result

⏳ **Waiting for Tasks**

### Task Check
- Frontend: 3/3 completed ✅
- Backend: 1/2 completed ⏳

### Incomplete Tasks
- [ ] Backend Task 2: Implement API endpoint
```

## Common Mistakes

- ❌ Close story with pending tasks → ✅ Check ALL related tasks first.
- ❌ Only check frontend OR backend → ✅ Check BOTH if story has both.
- ❌ Forget to update checkboxes → ✅ Always update `- [ ]` to `- [x]`.