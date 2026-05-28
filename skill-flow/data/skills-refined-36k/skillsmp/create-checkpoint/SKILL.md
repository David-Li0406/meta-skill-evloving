---
name: create-checkpoint
description: Create a checkpoint to track progress and share context
argument-hint: <workflow-id> <step> <status> <context>
---

# Create Checkpoint

## Overview

Record progress and provide context for future sessions or other agents. Use this skill when completing milestones, handing off work, encountering issues, or reaching natural pause points. Creates a checkpoint entry that captures the current workflow state for resumption or handoff.

## Arguments

### Definitions

- **`<workflow-id>`** (required): The workflow identifier for output organization.
- **`<step>`** (required): Current step name (e.g., analyze, plan, review).
- **`<status>`** (required): Checkpoint status. Values: `in_progress`, `completed`.
- **`<context>`** (required): Summary of current situation and progress.

### Values

\$ARGUMENTS

## Core Principles

- Checkpoints are append-only within a workflow
- Include enough context for seamless resumption
- Note any blockers or issues discovered
- Track progress with markdown checklists

## Instructions

1. Parse the workflow-id, step name, and status
2. Generate checkpoint ID (chk-NNN)
3. Create checkpoint entry with:
   - Context summary
   - Progress checklist
   - Notes for next session
   - Issues discovered
4. Save to `agentic/outputs/{workflow-id}/checkpoint.md`
5. Return confirmation with checkpoint ID

## Output Guidance

Return JSON confirmation:

```json
{
  "success": true,
  "checkpoint_id": "chk-001",
  "workflow_id": "abc123"
}
```

## Templates

### Checkpoint File Format

Checkpoints are stored in `agentic/outputs/{workflow-id}/checkpoint.md`:

```markdown
---
checkpoint_id: chk-001
step: build
created: 2024-01-15T14:30:00Z
workflow_id: abc-123
status: in_progress
---

## Context

Summary of the current situation...

## Progress

- [x] Completed task
- [ ] Pending task

## Notes for Next Session

Important details...

## Issues Discovered

Problems found...
```
