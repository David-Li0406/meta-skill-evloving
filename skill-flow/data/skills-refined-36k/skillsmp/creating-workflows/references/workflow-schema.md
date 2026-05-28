---
title: Workflow Schema Reference
description: Complete YAML schema for workflow definitions including all fields, types, and validation rules.
keywords: workflow, schema, yaml, phases, validation, types
skill: creating-workflows
---

# Workflow Schema Reference

## File Structure

Workflow files are YAML documents stored in `.claude/workflows/`.

```yaml
# .claude/workflows/<workflow-name>.yaml
name: <string>           # Required
description: <string>    # Optional
phases: <list>           # Required
```

## Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Human-readable workflow name |
| `description` | string | No | Brief description of workflow purpose |
| `phases` | list[Phase] | Yes | Ordered list of phase definitions |

## Phase Schema

### Simple Phase

```yaml
- id: <string>           # Required - unique identifier
  prompt: <string>       # Required - execution instructions
```

### For-Each Phase

```yaml
- id: <string>           # Required - unique identifier
  for-each: step         # Required - iteration mode (only "step" supported)
  workflow: <string>     # Required - workflow reference for each iteration
```

## Phase Fields Reference

| Field | Type | Required | Context | Description |
|-------|------|----------|---------|-------------|
| `id` | string | Yes | All phases | Unique phase identifier (kebab-case recommended) |
| `prompt` | string | Conditional | Simple phases | Instructions for phase execution |
| `for-each` | `'step'` | Conditional | For-each phases | Iteration mode |
| `workflow` | string | Conditional | For-each phases | Workflow reference (no `.yaml` extension) |
| `parallel` | boolean | No | Step workflow phases | Run in background, don't block next step |
| `wait-for-parallel` | boolean | No | Top-level phases | Wait for all parallel tasks before continuing |

## Conditional Requirements

| Phase Type | Required Fields | Description |
|------------|-----------------|-------------|
| Simple | `id` + `prompt` | Direct prompt execution |
| For-Each | `id` + `for-each` + `workflow` | Iterates over steps, runs workflow per step |

## TypeScript Interface

```typescript
interface WorkflowDefinition {
  name: string;
  description?: string;
  phases: WorkflowPhase[];
}

interface WorkflowPhase {
  id: string;
  prompt?: string;
  'for-each'?: 'step';
  workflow?: string;
  parallel?: boolean;
  'wait-for-parallel'?: boolean;
}
```

## Validation Rules

### Workflow Level

1. `name` must be non-empty string
2. `phases` must be non-empty array
3. File must be valid YAML

### Phase Level

1. Each phase must have unique `id`
2. Phase `id` should be kebab-case (lowercase, hyphens)
3. Simple phase: `prompt` is required, `for-each` and `workflow` must be absent
4. For-each phase: `for-each` and `workflow` are required, `prompt` must be absent

### Reference Resolution

1. Workflow references resolve from `.claude/workflows/<name>.yaml`
2. References should not include `.yaml` extension
3. Circular workflow references are invalid

### Parallel Execution

1. `parallel` must be boolean if present
2. `wait-for-parallel` must be boolean if present
3. `parallel: true` only works in step workflows (not on for-each phases)
4. `wait-for-parallel: true` only makes sense on top-level simple phases

## Valid Examples

### Minimal Workflow

```yaml
name: Minimal
phases:
  - id: execute
    prompt: "Execute the task"
```

### Sprint Workflow

```yaml
name: Standard Sprint
description: Full sprint lifecycle
phases:
  - id: prepare
    prompt: "Initialize sprint environment"

  - id: development
    for-each: step
    workflow: feature-standard

  - id: qa
    prompt: "Run quality checks"
```

### Nested Workflows

```yaml
# sprint-workflow.yaml
name: Sprint with QA
phases:
  - id: develop
    for-each: step
    workflow: step-with-qa

# step-with-qa.yaml (referenced workflow)
name: Step with QA
phases:
  - id: implement
    prompt: "Implement: {{step.prompt}}"
  - id: test
    prompt: "Test implementation"
```

### Parallel Execution

Use `parallel: true` on step workflow phases to run them in background without blocking the next step. Use `wait-for-parallel: true` on top-level phases to create sync points.

```yaml
# sprint-workflow.yaml - Sprint with sync point
name: Sprint with Parallel Docs
description: Development with non-blocking documentation updates
phases:
  - id: development
    for-each: step
    workflow: feature-with-docs

  - id: sync
    prompt: "Verify all documentation updates completed..."
    wait-for-parallel: true

  - id: qa
    prompt: "Run final QA checks..."
```

```yaml
# feature-with-docs.yaml - Step workflow with parallel sub-phase
name: Feature with Docs
phases:
  - id: plan
    prompt: "Plan implementation for: {{step.prompt}}"

  - id: implement
    prompt: "Implement: {{step.prompt}}"

  - id: test
    prompt: "Test the implementation..."

  - id: update-docs
    prompt: "Update documentation for {{step.prompt}}..."
    parallel: true
```

## Invalid Examples

### Missing Required Fields

```yaml
# INVALID: Missing name
phases:
  - id: task
    prompt: "Do something"
```

```yaml
# INVALID: Empty phases
name: Empty Workflow
phases: []
```

### Invalid Phase Configuration

```yaml
# INVALID: Simple phase missing prompt
phases:
  - id: task
```

```yaml
# INVALID: For-each phase missing workflow
phases:
  - id: development
    for-each: step
```

```yaml
# INVALID: Mixed phase types (both prompt and for-each)
phases:
  - id: hybrid
    prompt: "Do something"
    for-each: step
    workflow: some-workflow
```

## File Naming Convention

| Pattern | Example | Description |
|---------|---------|-------------|
| `<purpose>-<type>.yaml` | `feature-standard.yaml` | Purpose-based naming |
| `<type>-<variant>.yaml` | `sprint-default.yaml` | Type with variant |
| `<action>-workflow.yaml` | `bugfix-workflow.yaml` | Action-focused |

---

## Ralph Mode Workflow

When creating a Ralph mode workflow, use `mode: ralph` instead of defining `phases`. Ralph mode enables autonomous goal-driven execution.

### Ralph Mode Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mode` | `'standard' \| 'ralph'` | No | Workflow mode (default: `standard`) |
| `goal-prompt` | string | Conditional | Prompt template for initial goal analysis (Ralph mode only) |
| `reflection-prompt` | string | Conditional | Prompt template for reflection when no pending steps (Ralph mode only) |
| `per-iteration-hooks` | list[PerIterationHook] | No | Hooks to run each iteration |

### Per-Iteration Hook Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique hook identifier |
| `workflow` | string | Conditional | Workflow reference (e.g., `"m42-signs:learning-extraction"`) |
| `prompt` | string | Conditional | Inline prompt (alternative to `workflow`) |
| `parallel` | boolean | Yes | If `true`, runs non-blocking in background |
| `enabled` | boolean | Yes | Default enabled state (can be overridden in SPRINT.yaml) |

**Note:** Either `workflow` or `prompt` is required, but not both.

### TypeScript Interface (Ralph Mode Extensions)

```typescript
interface WorkflowDefinition {
  name: string;
  description?: string;
  phases?: WorkflowPhase[];           // Optional for Ralph mode
  mode?: 'standard' | 'ralph';
  'goal-prompt'?: string;
  'reflection-prompt'?: string;
  'per-iteration-hooks'?: PerIterationHook[];
}

interface PerIterationHook {
  id: string;
  workflow?: string;
  prompt?: string;
  parallel: boolean;
  enabled: boolean;
}
```

### Ralph Mode Workflow Example

```yaml
name: Ralph Mode Workflow
description: Autonomous goal-driven execution with configurable per-iteration hooks
mode: ralph

goal-prompt: |
  Analyze the goal and create initial implementation steps.
  Break down complex goals into concrete, actionable tasks.

reflection-prompt: |
  No pending steps remain. Evaluate:
  1. Is the goal fully achieved?
  2. Are there edge cases or tests missing?
  3. Is documentation complete?

  If complete: RALPH_COMPLETE: [summary]
  If not: add more steps

per-iteration-hooks:
  - id: learning
    workflow: "m42-signs:learning-extraction"
    parallel: true
    enabled: false

  - id: documentation
    prompt: |
      Review changes from this iteration and update relevant documentation.
    parallel: true
    enabled: false

  - id: tests
    prompt: |
      Analyze code changes and suggest additional test cases.
    parallel: true
    enabled: false
```

### SPRINT.yaml for Ralph Mode

```yaml
workflow: ralph
goal: |
  Build authentication system with JWT tokens

# Override hook defaults
per-iteration-hooks:
  learning:
    enabled: true
  documentation:
    enabled: true
```

### Validation Rules (Ralph Mode)

1. If `mode: ralph`, `phases` should be absent or empty
2. If `mode: ralph`, `goal-prompt` and `reflection-prompt` are recommended
3. Per-iteration hooks must have unique `id` values
4. Each hook must have either `workflow` or `prompt`, not both
5. Hook `parallel` and `enabled` fields are required

---

## Schema Evolution

Current schema version supports:
- Simple phases with prompts
- For-each phases iterating over steps
- Template variable substitution
- Parallel execution with `parallel` and `wait-for-parallel`
- Ralph mode with autonomous goal-driven execution
- Per-iteration hooks for deterministic parallel tasks

Future versions may add:
- Conditional phases
- Phase dependencies
