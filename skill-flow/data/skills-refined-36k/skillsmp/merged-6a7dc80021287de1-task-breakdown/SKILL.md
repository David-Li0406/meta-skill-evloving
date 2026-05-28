---
name: task-breakdown
description: Use this skill to break down PM stories into organized tasks for both frontend and backend development, ensuring tasks are ordered by their respective architecture layers.
---

# Task Breakdown

## ⚠️ CRITICAL RULES - READ FIRST

**BEFORE doing anything, you MUST:**

1. **CHECK EXISTING TASK FILE FIRST**:
   - ALWAYS check if `story-{story-name}.md` already exists in the appropriate tasks directory (`docs/reference/frontend/tasks/` or `docs/reference/backend/tasks/`).
   - If exists: READ it and continue from current progress (add new tasks or update existing ones).
   - If not exists: Create new task breakdown file.
   - **NEVER re-break down existing tasks**.

2. **FILE NAMING**:
   - Pattern: `story-{story-name}.md` (single file per story).
   - All tasks for this story go into this ONE file.
   - Tasks are separated by `---` dividers.

3. **MULTIPLE TASKS IN ONE FILE**:
   - One file contains ALL tasks for the story.
   - Each task = independently testable section.
   - Clear scope and acceptance criteria per task.
   - Tasks numbered sequentially (Task 1, Task 2, etc.).

4. **ALWAYS SAVE TO CORRECT PATH**:
   - Path: `docs/reference/{frontend/backend}/tasks/story-{story-name}.md`.
   - NO exceptions, NO other locations.

5. **READ CONTEXT FIRST**:
   - Read story from `docs/reference/pm/stories/`.
   - Read design from `docs/reference/{frontend/backend}/designs/` if exists.
   - Read design system from `docs/reference/{frontend/backend}/design-system.md`.
   - Read constraints from `docs/reference/{frontend/backend}/constraints.md`.

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Read story/PRD**: Load from `docs/reference/pm/stories/` or `docs/reference/pm/versions/`.
2. **Read design** (if exists): Load from `docs/reference/{frontend/backend}/designs/`.
3. **Read constraints**: Load design system and technical constraints.
4. **Identify components**: What UI elements or backend layers are needed.
5. **Identify interactions**: What APIs, data flows, and logic are needed.
6. **Break into tasks**: Independently testable, single responsibility, by architecture layer.
7. **Order by dependencies**:
   - For frontend: Setup → Static UI → Dynamic Logic → Interactions → Testing.
   - For backend: Types → Database → Repository → Service → API → Tests.
8. **Generate single file**: Create `story-{story-name}.md` with all tasks in sections.
9. **Update Story file**: Add "Related Tasks" section to story file with link to task file.
10. **Summary**: Show created file and next steps.

## Task File Format

**Key points:**

- Single file contains all tasks for the story.
- Tasks numbered sequentially (Task 1, Task 2, etc.).
- Each task has: Description, Context, Acceptance Criteria, Scope, Implementation Steps.
- Progress section at the end tracks completion.
- Both story-based and standalone use the same format (only filename differs).

## Updating Story File

After generating the task file, **ALWAYS** update the story file to add the "Related Tasks" section:

```markdown
## Related Tasks

### Frontend/Backend Tasks

Task breakdown: [docs/reference/{frontend/backend}/tasks/story-user-profile.md](../{frontend/backend}/tasks/story-user-profile.md)

**Progress**: 0/X tasks completed

- [ ] Task 1: Description
- [ ] Task 2: Description
- [ ] Task 3: Description
```

**Key points:**

- Add this section at the end of the story file (before any existing notes).
- Include link to the task file.
- Use `- [ ]` checkboxes for each task (will be checked when task completes).
- List tasks in execution order.
- Keep the section organized by frontend/backend if both exist.
- Include progress counter (X/Y tasks completed).

## Key Rules

- ALWAYS create a single file containing all tasks for the story.
- MUST use `story-{story-name}.md` naming (NOT multiple files).
- ALWAYS include test tasks at the end.
- MUST note dependencies between tasks (in each task's metadata).
- Keep tasks focused - not too big, not too small.
- Each task section is self-contained with clear acceptance criteria.
- Separate tasks with `---` dividers.
- Include Story Progress section at the end of file.

## Common Mistakes

- ❌ Tasks too large (full feature) → ✅ Break into layers/sections.
- ❌ Tasks too small (add one field/button) → ✅ Group related work.
- ❌ Skip dependencies → ✅ Note which tasks depend on others.
- ❌ Forget testing → ✅ Always include test tasks.
- ❌ Create multiple files → ✅ Use single file with multiple task sections.