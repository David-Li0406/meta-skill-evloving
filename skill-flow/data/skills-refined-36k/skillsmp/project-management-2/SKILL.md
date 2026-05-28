---
name: Project Management
description: Manage the workspace roadmap by adding tasks, updating status, and maintaining the project backlog.
---

# Project Management Skill

Use this skill when asked to "add a task", "update the roadmap", "what are we working on?", or "prioritize X".

The Single Source of Truth is **`.agent/ROADMAP.md`**.

## Core Operations

### 1. Add Task
**Trigger**: "Add [task] to the backlog"
**Procedure**:
1.  Read `.agent/ROADMAP.md`.
2.  Generate a new unique ID (e.g., `[TASK-003]`) by incrementing the highest existing ID.
3.  Append the task to the `## Backlog` section (under `### Unsorted` if no priority is given).
4.  **Format**: `- [TASK-ID] Title (Status: Planned)`

### 2. Update Status
**Trigger**: "Mark [task] as In Progress" or "Move [task] to Active"
**Procedure**:
1.  Find the task by ID or fuzzy title match.
2.  Move the line to the appropriate section:
    -   `## Active Tasks` -> `(Status: In Progress)`
    -   `## Completed` -> `(Status: Done)` (Add completion date if possible)
    -   `## Backlog` -> `(Status: Planned)`

### 3. Review / Summarize
**Trigger**: "What is the status?" or "Review the roadmap"
**Procedure**:
1.  Read `.agent/ROADMAP.md`.
2.  Summarize items in `## Active Tasks` and high-priority items in `## Backlog`.

## Roadmap Schema

```markdown
# Workspace Roadmap

## Active Tasks
- [TASK-001] Example Task (Status: In Progress)

## Backlog
### High Priority
- [TASK-002] Important Feature (Status: Planned)

### Unsorted
- [TASK-003] New Idea (Status: Planned)

## Completed
- [TASK-000] Old Task (Status: Done)
```
