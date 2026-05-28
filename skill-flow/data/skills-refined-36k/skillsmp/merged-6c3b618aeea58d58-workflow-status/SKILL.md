---
name: workflow-status
description: Use this skill to display the current workflow phase status and progress for a project.
---

# Workflow Status Skill

Display current workflow status and progress for a project.

## Overview

This skill provides a formatted status report showing:
- Current phase
- Phase completion status
- Task progress
- Recent feedback
- Any errors or blockers

## Usage

```
/workflow-status --project <project-name>
```

## Prerequisites

- SurrealDB connection configured for the project namespace.

## State Sources

- `workflow_state` in SurrealDB - Overall workflow state
- `phase_outputs` in SurrealDB - Task breakdown and validation/verification
- `logs` in SurrealDB - Error and blocker information

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

## Last Updated

{timestamp}
```

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

## Phase Names

| Number | Name | Description |
|--------|------|-------------|
| 0 | Discussion | Gather requirements |
| 1 | Planning | Create plan.json |
| 2 | Validation | Cursor + Gemini validate plan |
| 3 | Implementation | Execute tasks with TDD |
| 4 | Verification | Cursor + Gemini review code |
| 5 | Completion | Generate summary |

## Status Values

| Status | Meaning |
|--------|---------|
| pending | Not started |
| in_progress | Currently executing |
| completed | Successfully finished |
| needs_revision | Requires changes |
| blocked | Cannot proceed |
| failed | Failed after max retries |

## Task Statistics

Calculate and display:
- Total tasks
- Completed tasks
- In-progress tasks
- Pending tasks
- Failed tasks
- Completion percentage

## Feedback Summary

For validation/verification feedback, show:
- Agent name
- Score (1-10)
- Approved status
- Number of concerns
- Number of blocking issues

## Error Display

Show recent errors with:
- Timestamp
- Phase where error occurred
- Error message
- Suggested action

## Integration

This skill is called by:
- `/orchestrate` - To show progress
- User directly - To check status
- Resume operations - To determine where to continue

## Outputs

- Human-readable status report for the current project.

## Error Handling

- If SurrealDB is unreachable, show a degraded report and warn about missing phase data.

## Related Skills

- `/status` - Summary status view
- `/orchestrate` - Full workflow execution