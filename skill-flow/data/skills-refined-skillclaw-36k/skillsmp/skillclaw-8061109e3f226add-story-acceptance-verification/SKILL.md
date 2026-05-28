---
name: story-acceptance-verification
description: Use this skill when you need to verify and close stories after ensuring all related frontend and backend tasks are completed.
---

# Skill body

## Language Configuration

Before generating any content, check `aico.json` in project root for the `language` field to determine the output language. If not set, default to English.

## Process

1. **Identify the story**: Get the story ID (e.g., S-001) from notification or user.
2. **Read the story**: Load `docs/reference/pm/stories/{story-id}.md`.
3. **Find related tasks**:
   - Check `docs/reference/frontend/tasks/` for frontend tasks.
   - Check `docs/reference/backend/tasks/` for backend tasks.
4. **Verify all tasks completed**:
   - Read each task file's `> **Status**:` field.
   - Ensure all task statuses are `✅ completed`.
   - Confirm there are no `⏳ pending` or `🔄 in_progress` tasks remaining.
5. **Update story**:
   - If ALL tasks are completed → Update acceptance criteria from `- [ ]` to `- [x]`.
   - If some tasks are incomplete → Report progress and list the incomplete tasks.

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