---
title: Progress Schema
description: Compiled PROGRESS.yaml schema including phase hierarchy, current pointer, status values, and statistics.
keywords: progress, schema, compiled, hierarchy, pointer, status, statistics
skill: orchestrating-sprints
---

# Progress Schema

## Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `sprint-id` | string | Sprint identifier |
| `status` | enum | Sprint execution status |
| `phases` | list | Compiled phase hierarchy |
| `current` | object | Execution pointer |
| `stats` | object | Execution statistics |

## Status Enums

### Sprint Status

| Value | Description |
|-------|-------------|
| `not-started` | Sprint initialized but not begun |
| `in-progress` | Actively executing phases |
| `completed` | All phases finished |
| `blocked` | Cannot proceed, needs resolution |
| `paused` | Manually paused by user |
| `needs-human` | Requires human intervention |

### Phase Status

| Value | Description |
|-------|-------------|
| `pending` | Not yet started |
| `in-progress` | Currently executing |
| `completed` | Successfully finished |
| `blocked` | Cannot proceed |
| `skipped` | Intentionally skipped |

## Phase Hierarchy

Three-level structure supporting simple and for-each phases.

### CompiledTopPhase

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Phase identifier |
| `status` | enum | Phase status |
| `prompt` | string | Execution prompt (simple phase only) |
| `steps` | list | CompiledStep entries (for-each phase only) |

### CompiledStep

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Step identifier |
| `prompt` | string | Original prompt template |
| `status` | enum | Step status |
| `phases` | list | CompiledPhase entries |

### CompiledPhase

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Phase identifier |
| `status` | enum | Phase status |
| `prompt` | string | Interpolated execution prompt |

## Current Pointer

| Field | Type | Description |
|-------|------|-------------|
| `phase` | number | Index into phases array (0-based) |
| `step` | number\|null | Index into steps array (null if simple phase) |
| `sub-phase` | number\|null | Index into sub-phases array |

## Stats Object

| Field | Type | Description |
|-------|------|-------------|
| `started-at` | ISO 8601 | Sprint start timestamp |
| `completed-at` | ISO 8601 | Sprint end timestamp |
| `total-phases` | number | Total phase count |
| `completed-phases` | number | Completed count |
| `total-steps` | number | Total steps (for-each only) |
| `completed-steps` | number | Completed steps |

---

## Ralph Mode Fields

When `mode: ralph` is set in PROGRESS.yaml, additional fields are available for autonomous goal-driven execution.

### Top-Level Ralph Fields

| Field | Type | Description |
|-------|------|-------------|
| `mode` | `'standard' \| 'ralph'` | Workflow mode (default: `standard`) |
| `goal` | string | Goal text for Ralph mode execution |

### ralph (Configuration Object)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `idle-threshold` | number | `3` | Iterations without progress before reflection mode triggers |

### dynamic-steps

Steps created dynamically by Claude during Ralph mode execution.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique step identifier (e.g., `step-0`, `step-1`) |
| `prompt` | string | Step task description |
| `status` | PhaseStatus | Current execution status (`pending`, `in-progress`, `completed`, `blocked`) |
| `added-at` | ISO 8601 | Timestamp when step was created |
| `added-in-iteration` | number | Which iteration created this step |

### hook-tasks

Tracking for per-iteration hook executions.

| Field | Type | Description |
|-------|------|-------------|
| `iteration` | number | Which iteration this task belongs to |
| `hook-id` | string | Reference to per-iteration hook ID |
| `status` | `'spawned' \| 'running' \| 'completed' \| 'failed'` | Hook task execution status |
| `pid` | number \| null | Process ID if running in background |
| `transcript` | string | Path to transcript file (relative to sprint directory) |

### ralph-exit

Tracks goal completion detection.

| Field | Type | Description |
|-------|------|-------------|
| `detected-at` | ISO 8601 \| null | When `RALPH_COMPLETE` was detected |
| `iteration` | number \| null | Which iteration completed the goal |
| `final-summary` | string \| null | Summary extracted from Claude's completion message |

### Ralph Mode PROGRESS.yaml Example

```yaml
mode: ralph
goal: |
  Build authentication system with JWT tokens

ralph:
  idle-threshold: 3

per-iteration-hooks:
  - id: learning
    workflow: "m42-signs:learning-extraction"
    parallel: true
    enabled: true

dynamic-steps:
  - id: step-0
    prompt: "Initialize auth module structure"
    status: completed
    added-at: "2026-01-18T10:00:00Z"
    added-in-iteration: 1
  - id: step-1
    prompt: "Implement JWT token generation"
    status: in-progress
    added-at: "2026-01-18T10:05:00Z"
    added-in-iteration: 1

hook-tasks:
  - iteration: 1
    hook-id: learning
    status: completed
    pid: null
    transcript: transcripts/iter-1-learning.jsonl

ralph-exit:
  detected-at: null
  iteration: null
  final-summary: null
```

---

## Example PROGRESS.yaml (Standard Mode)

```yaml
sprint-id: feature-auth-2026-01
status: in-progress

phases:
  # Simple phase
  - id: setup-branch
    status: completed
    prompt: "Create feature branch and set up project structure"

  # For-each phase with expanded steps
  - id: implement-endpoints
    status: in-progress
    steps:
      - id: implement-endpoints-login
        prompt: "Implement {{endpoint}} endpoint"
        status: completed
        phases:
          - id: implement-endpoints-login-gather
            status: completed
            prompt: "Gather context for login endpoint"
          - id: implement-endpoints-login-execute
            status: completed
            prompt: "Implement login endpoint"
          - id: implement-endpoints-login-verify
            status: completed
            prompt: "Verify login endpoint implementation"

      - id: implement-endpoints-logout
        prompt: "Implement {{endpoint}} endpoint"
        status: in-progress
        phases:
          - id: implement-endpoints-logout-gather
            status: completed
            prompt: "Gather context for logout endpoint"
          - id: implement-endpoints-logout-execute
            status: in-progress
            prompt: "Implement logout endpoint"
          - id: implement-endpoints-logout-verify
            status: pending
            prompt: "Verify logout endpoint implementation"

      - id: implement-endpoints-refresh
        prompt: "Implement {{endpoint}} endpoint"
        status: pending
        phases:
          - id: implement-endpoints-refresh-gather
            status: pending
            prompt: "Gather context for refresh endpoint"
          - id: implement-endpoints-refresh-execute
            status: pending
            prompt: "Implement refresh endpoint"
          - id: implement-endpoints-refresh-verify
            status: pending
            prompt: "Verify refresh endpoint implementation"

  # Simple phase
  - id: final-review
    status: pending
    prompt: "Run full test suite and create PR"

current:
  phase: 1
  step: 1
  sub-phase: 1

stats:
  started-at: 2026-01-15T09:00:00Z
  completed-at: null
  total-phases: 3
  completed-phases: 1
  total-steps: 3
  completed-steps: 1
```
