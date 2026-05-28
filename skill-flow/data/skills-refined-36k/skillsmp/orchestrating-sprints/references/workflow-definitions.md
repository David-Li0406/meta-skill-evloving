---
title: Workflow Definitions
description: Workflow YAML schema including phase types, template variables, and for-each expansion.
keywords: workflow, phases, for-each, template, variables, expansion
skill: orchestrating-sprints
---

# Workflow Definitions

## Workflow Structure

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Workflow identifier |
| `description` | string | No | Human-readable summary |
| `phases` | list | Yes | Ordered phase definitions |

## Phase Types

### Simple Phase

Direct prompt execution within current context.

```yaml
- id: review
  prompt: "Review changes and verify quality"
```

### For-Each Phase

Iterates over steps, spawning workflow per step.

```yaml
- id: implement
  for-each: step
  workflow: step-default
```

## Phase Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique phase identifier |
| `prompt` | string | Conditional | Prompt text (for simple phases) |
| `for-each` | 'step' | Conditional | Iteration mode (for for-each phases) |
| `workflow` | string | Conditional | Workflow reference (for for-each phases) |

**Conditional rules:**
- Simple phase: requires `prompt`
- For-each phase: requires `for-each` + `workflow`

## Template Variables

| Variable | Context | Value |
|----------|---------|-------|
| `{{step.prompt}}` | For-each phases | The prompt from SPRINT.yaml step |
| `{{step.id}}` | For-each phases | Step ID (e.g., step-1) |
| `{{step.index}}` | For-each phases | 0-based step index |
| `{{phase.id}}` | Any phase | Current phase ID |
| `{{sprint.id}}` | Any phase | Sprint identifier |

## Example Workflows

### sprint-default

Standard sprint workflow with planning, implementation, and review phases.

```yaml
name: sprint-default
description: Default sprint workflow with planning and review
phases:
  - id: planning
    prompt: "Analyze sprint goals and create implementation plan"

  - id: implement
    for-each: step
    workflow: step-default

  - id: review
    prompt: "Review all changes, run tests, verify sprint completion"
```

### feature-standard

Feature implementation workflow for step-level execution.

```yaml
name: feature-standard
description: Standard feature implementation workflow
phases:
  - id: context
    prompt: "Load context for {{step.id}}: {{step.prompt}}"

  - id: implement
    prompt: "Implement the feature following the step requirements"

  - id: verify
    prompt: "Run tests and verify implementation for {{step.id}}"

  - id: commit
    prompt: "Commit changes with descriptive message referencing {{step.id}}"
```
