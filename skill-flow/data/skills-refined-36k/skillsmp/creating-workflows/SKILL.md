---
name: creating-workflows
description: Guide for creating sprint workflow definitions. This skill should be used when users want to create a new workflow, modify existing workflows, understand workflow schema, or define phase sequences. Triggers on "create workflow", "new workflow", "workflow definition", "define phases".
---

# Creating Workflows

Guide for authoring sprint workflow definitions in `.claude/workflows/`.

## What is a Workflow?

| Concept | Description |
|---------|-------------|
| Workflow | YAML file defining execution phases |
| Phase | Individual step with prompt or iteration |
| For-Each | Phase that iterates over sprint steps |
| Template Variables | Dynamic values substituted at runtime |
| Ralph Mode | Autonomous goal-driven workflow (no predefined phases) |

## Workflow Location

```text
.claude/workflows/
├── sprint-default.yaml     # Top-level sprint workflow
├── feature-standard.yaml   # Step-level implementation workflow
├── bugfix-workflow.yaml    # Quick bug fix workflow
└── custom-workflow.yaml    # Your custom workflows
```

## Quick Start

### 1. Create Workflow File

```yaml
# .claude/workflows/my-workflow.yaml
name: My Custom Workflow
description: Brief description of workflow purpose

phases:
  - id: first-phase
    prompt: |
      Instructions for first phase.
      {{step.prompt}}

  - id: second-phase
    prompt: |
      Instructions for second phase.
```

### 2. Reference in SPRINT.yaml

```yaml
workflow: my-workflow
steps:
  - Implement feature X
  - Add tests for feature X
```

## Phase Types Decision Tree

```text
Do you need to process multiple sprint steps?
├── YES → Use for-each phase
│         └── for-each: step
│             workflow: step-workflow
│
└── NO → Use simple phase
         └── prompt: "Instructions here"
```

## Workflow Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| Simple Sequential | Linear task flow | `prepare → execute → verify` |
| For-Each Development | Step iteration | `development` phase with `for-each: step` |
| Nested Workflow | Complex step execution | For-each phase referencing step workflow |
| Hybrid | Mixed phases | Simple + for-each combined |
| Ralph Mode | Autonomous goal-driven | `mode: ralph` with dynamic steps |

## Template Variables

| Variable | Available In | Value |
|----------|--------------|-------|
| `{{step.prompt}}` | For-each phases | Step description from SPRINT.yaml |
| `{{step.id}}` | For-each phases | Step identifier (e.g., step-1) |
| `{{step.index}}` | For-each phases | 0-based step index |
| `{{phase.id}}` | All phases | Current phase identifier |
| `{{sprint.id}}` | All phases | Sprint identifier |
| `{{sprint.name}}` | All phases | Sprint name (if set) |

## Example Workflows

### Minimal Workflow

```yaml
name: Minimal Execute
phases:
  - id: execute
    prompt: "Execute the task: {{step.prompt}}"
```

### Sprint Workflow with For-Each

```yaml
name: Standard Sprint
phases:
  - id: prepare
    prompt: "Prepare sprint environment"

  - id: development
    for-each: step
    workflow: feature-standard

  - id: qa
    prompt: "Run tests and quality checks"

  - id: deploy
    prompt: "Create PR and finalize"
```

## Ralph Mode Workflows

Ralph Mode enables autonomous goal-driven execution where Claude creates steps dynamically instead of following predefined phases.

### Ralph Mode Structure

```yaml
name: My Ralph Workflow
mode: ralph

goal-prompt: |
  Analyze goal and create steps...

reflection-prompt: |
  Evaluate if goal is complete...

per-iteration-hooks:
  - id: learning
    workflow: "m42-signs:learning-extraction"
    parallel: true
    enabled: false
```

### Per-Iteration Hooks

Hooks are deterministic tasks that run every iteration:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique hook identifier |
| `workflow` | string | External workflow/plugin reference |
| `prompt` | string | Inline prompt (alternative to workflow) |
| `parallel` | boolean | Run non-blocking in background |
| `enabled` | boolean | Default enabled state |

See `references/workflow-schema.md` for full Ralph Mode schema.

## References

- `references/workflow-schema.md` - Complete YAML schema (includes Ralph Mode)
- `references/template-variables.md` - All available variables
- `references/phase-types.md` - Simple vs for-each phases
- `references/workflow-patterns.md` - Common patterns

## Assets

- `assets/feature-workflow.yaml` - Feature implementation template
- `assets/bugfix-workflow.yaml` - Bug fix template
- `assets/validation-checklist.md` - Pre-deployment checklist

## Validation

Before using a workflow:

1. Check YAML syntax is valid
2. Verify all phase IDs are unique
3. Ensure for-each phases have `workflow` reference
4. Confirm referenced workflows exist in `.claude/workflows/`
5. Test template variables resolve correctly

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|------------|
| Workflow not found | Missing file | Create in `.claude/workflows/` |
| Phase skipped | Missing `prompt` or `for-each` | Add required field |
| Variable not resolved | Wrong context | Check variable availability (step.* only in for-each) |
| Compilation error | Invalid YAML | Validate YAML syntax |

## Related

- **orchestrating-sprints** - Running and managing sprints
- **creating-sprints** - Creating SPRINT.yaml definitions
