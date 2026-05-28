---
name: workflow-status
description: Use this skill to display the current status and progress of a project's workflow, including phases, tasks, and any blockers.
---

# Skill body

## Overview

This skill provides a comprehensive status report of the current workflow, showing:
- Current phase
- Phase completion status
- Task progress
- Any blockers or errors
- Next recommended action

## Usage

```
/workflow-status --project <project-name>
```

## Prerequisites

- SurrealDB connection configured for the project namespace.

## State Sources

Check these sources:
- `workflow_state` in SurrealDB - Overall workflow state
- `phase_outputs` in SurrealDB - Task breakdown and validation/verification
- `logs` in SurrealDB - Error and blocker logs

## Status Report Format

```markdown
# Workflow Status: {project_name}

## Current Phase: {current_phase} - {phase_name}

## Phase Progress

| Phase | Status | Details |
|-------|--------|---------|
| 0. Discussion | {status} | {notes} |
| 1. Planning | {status} | {notes} |
| 2. Validation | {status} | Cursor: {score}, Gemini: {score} |
| 3. Implementation | {status} | {completed}/{total} tasks |
| 4. Verification | {status} | Cursor: {score}, Gemini: {score} |
| 5. Completion | {status} | {notes} |

## Task Progress

| Task | Title | Status | Attempts |
|------|-------|--------|----------|
| T1 | {title} | completed | 1 |
| T2 | {title} | in_progress | 2 |
| T3 | {title} | pending | 0 |

Completed: {N}/{total} ({percentage}%)

## Recent Feedback

### Validation (Phase 2)
- Cursor: Score {X}/10 - {approved/rejected}
- Gemini: Score {X}/10 - {approved/rejected}

### Verification (Phase 4)
- Cursor: Score {X}/10 - {approved/rejected}
- Gemini: Score {X}/10 - {approved/rejected}

## Errors/Blockers

{List any errors or blockers}

## Next Action

Continue with: /task {next_task} or /workflow-status -v for detailed view.

## Reading State

```python
# Pseudocode for reading state
state = workflow_state_repo.get(project)

current_phase = state.get("current_phase", 0)
phase_status = state.get("phase_status", {})
tasks = state.get("tasks", [])
validation = phase_outputs_repo.get_by_type(phase=2, output_type="validation_consolidated")
verification = phase_outputs_repo.get_by_type(phase=4, output_type="verification_consolidated")
errors = logs_repo.get_by_type("blocker")
```