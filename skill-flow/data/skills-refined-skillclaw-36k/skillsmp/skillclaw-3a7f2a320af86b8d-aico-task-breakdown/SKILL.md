---
name: aico-task-breakdown
description: Use this skill when you need to break down a PM story into organized tasks for either frontend or backend development, ensuring tasks are ordered by their respective architectural or development layers.
---

# Task Breakdown

## ⚠️ CRITICAL RULES - READ FIRST

**BEFORE doing anything, you MUST:**

1. **CHECK EXISTING TASK FILE FIRST**:
   - ALWAYS check if `story-{story-name}.md` already exists in the appropriate tasks directory (`docs/reference/frontend/tasks/` or `docs/reference/backend/tasks/`).
   - If it exists: READ it and continue from current progress (add new tasks or update existing ones).
   - If not exists: Create new task breakdown file.
   - **NEVER re-break down existing tasks**.

2. **FILE NAMING**:
   - Pattern: `story-{story-name}.md` (single file per story).
   - Example: `story-user-profile.md`.
   - All tasks for this story go into this ONE file.
   - Tasks are separated by `---` dividers.

3. **MULTIPLE TASKS IN ONE FILE**:
   - One file contains ALL tasks for the story.
   - Each task = independently testable section.
   - Clear scope and acceptance criteria per task.
   - Tasks numbered sequentially (Task 1, Task 2, etc.).

4. **ALWAYS SAVE TO CORRECT PATH**:
   - For frontend: `docs/reference/frontend/tasks/story-{story-name}.md`.
   - For backend: `docs/reference/backend/tasks/story-{story-name}.md`.
   - NO exceptions, NO other locations.

5. **READ CONTEXT FIRST**:
   - Read story from `docs/reference/pm/stories/`.
   - Read design from `docs/reference/frontend/designs/` or `docs/reference/backend/designs/` if exists.
   - Read design system from `docs/reference/frontend/design-system.md` or constraints from `docs/reference/backend/constraints.md`.

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Read story/PRD**: Load from `docs/reference/pm/stories/` or `docs/reference/pm/versions/`.
2. **Identify components** (for frontend) or **data entities** (for backend): What UI elements or domain objects are needed.
3. **Identify interactions** (for frontend) or **API endpoints** (for backend): What logic and routes are needed.
4. **Break into tasks**: Independently testable, single responsibility.
5. **Order by dependencies**: 
   - For frontend: Setup → Static UI → Dynamic Logic → Interactions → Testing.
   - For backend: Data Models → Database → Repository → Service → API → Validation → Tests.
6. **Save output**: ALWAYS write to the correct path.

## Task File Template

```markdown
# [Story Name] - [Frontend/Backend] Tasks

> Project: [project-name]
> Created: YYYY-MM-DD
> Last Updated: YYYY-MM-DD
> Source: docs/reference/pm/stories/[story].md
> Design: docs/reference/[frontend/backend]/designs/[name].md
> Status: in_progress

## Progress

| Task                         | Status         | Notes |
| ---------------------------- | -------------- | ----- |
| 1. Setup component structure (Frontend) / Define data models (Backend) | ⏳ pending |       |
| 2. Implement header section (Frontend) / Create database migrations (Backend) | ⏳ pending |       |
| 3. Implement content section (Frontend) / Implement repository layer (Backend) | ⏳ pending |       |

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