---
name: frontend-task-breakdown
description: Use this skill to break down a project management story into organized frontend tasks, ensuring proper dependency order and following UI development layers.
---

# Task Breakdown

## ⚠️ CRITICAL RULES - READ FIRST

**BEFORE doing anything, you MUST:**

1. **CHECK EXISTING TASK FILE FIRST**:
   - ALWAYS check if `story-{story-name}.md` already exists in `docs/reference/frontend/tasks/`
   - If it exists: READ it and continue from current progress (add new tasks or update existing ones)
   - If it does not exist: Create a new task breakdown file
   - **NEVER re-break down existing tasks**

2. **FILE NAMING**:
   - Pattern: `story-{story-name}.md` (single file per story)
   - Example: `story-user-profile.md`
   - All tasks for this story go into this ONE file
   - Tasks are separated by `---` dividers

3. **MULTIPLE TASKS IN ONE FILE**:
   - One file contains ALL tasks for the story
   - Each task = independently testable section
   - Clear scope and acceptance criteria per task
   - Tasks numbered sequentially (Task 1, Task 2, etc.)

4. **ALWAYS SAVE TO CORRECT PATH**:
   - Path: `docs/reference/frontend/tasks/story-{story-name}.md`
   - NO exceptions, NO other locations

5. **READ CONTEXT FIRST**:
   - Read story from `docs/reference/pm/stories/`
   - Read design from `docs/reference/frontend/designs/` if it exists
   - Read design system from `docs/reference/frontend/design-system.md`
   - Read constraints from `docs/reference/frontend/constraints.md`

## Language Configuration

Before generating any content, check `aico.json` in the project root for the `language` field to determine the output language. If not set, default to English.

## Process

1. **Read story/PRD**: Load from `docs/reference/pm/stories/` or `docs/reference/pm/versions/`
2. **Read design** (if exists): Load from `docs/reference/frontend/designs/`
3. **Identify components**: What UI elements are needed
4. **Identify interactions**: What logic and events are needed
5. **Break into tasks**: Independently testable, single responsibility
6. **Order by dependencies**: Setup → Static UI → Dynamic → Tests
7. **Generate single file**: Create `story-{story-name}.md` with all tasks in sections
8. **Update Story file**: Add "Related Tasks" section to the story file with a link to the task file
9. **Summary**: Show created file and next steps

## Task File Format

```markdown
# [Story Name] - Frontend Tasks

> Project: [project-name]
> Created: YYYY-MM-DD
> Last Updated: YYYY-MM-DD
> Source: docs/reference/pm/stories/[story].md
> Design: docs/reference/frontend/designs/[name].md
> Status: in_progress

## Progress

| Task                         | Status         | Notes |
| ---------------------------- | -------------- | ----- |
| 1. Setup component structure | ✅ completed   |       |
| 2. Implement header section  | 🔄 in_progress |       |
| 3. Implement content section | ⏳ pending     |       |

## Tasks

### Task 1: [Task Name]

**Status**: ⏳ pending  
**Goal**: What this task achieves  
**Scope**: Files to create/modify  
**Acceptance Criteria**:

- [ ] Criterion 1
- [ ] Criterion 2  
**Dependencies**: Task X (if any)
```

## Key Rules

- ALWAYS create a single file containing all tasks for the story
- MUST use `story-{story-name}.md` naming (NOT multiple files)
- ALWAYS include test tasks at the end
- MUST note dependencies between tasks (in each task's metadata)
- Keep tasks focused - not too big, not too small
- Each task section is self-contained with clear acceptance criteria
- Separate tasks with `---` dividers
- Include Story Progress section at the end of the file

## Common Mistakes

- ❌ Tasks too large (full page) → ✅ Break into sections
- ❌ Tasks too small (add one button) → ✅ Group related work
- ❌ Skip dependencies → ✅ Note which tasks depend on others
- ❌ Forget testing → ✅ Always include test tasks