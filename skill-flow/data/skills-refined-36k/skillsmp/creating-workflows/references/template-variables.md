---
title: Template Variables Reference
description: Complete reference for all available template variables in workflow prompts.
keywords: template, variables, substitution, step, phase, sprint, context
skill: creating-workflows
---

# Template Variables Reference

Template variables are placeholders in workflow prompts that get replaced with actual values at runtime.

## Syntax

Variables use double curly braces: `{{variable.property}}`

```yaml
prompt: |
  Implement: {{step.prompt}}
  Current phase: {{phase.id}}
```

## Variable Categories

### Step Variables

Available only in for-each phases and their nested workflows.

| Variable | Type | Description | Example Value |
|----------|------|-------------|---------------|
| `{{step.prompt}}` | string | Step description from SPRINT.yaml | "Implement user auth" |
| `{{step.id}}` | string | Step identifier | "step-1" |
| `{{step.index}}` | number | 0-based step index | 0, 1, 2... |

### Phase Variables

Available in all phases.

| Variable | Type | Description | Example Value |
|----------|------|-------------|---------------|
| `{{phase.id}}` | string | Current phase identifier | "development" |
| `{{phase.index}}` | number | 0-based phase index | 0, 1, 2... |

### Sprint Variables

Available in all phases.

| Variable | Type | Description | Example Value |
|----------|------|-------------|---------------|
| `{{sprint.id}}` | string | Sprint identifier | "2024-01-15_auth-feature" |
| `{{sprint.name}}` | string | Sprint name (optional) | "Authentication Feature" |

## Availability Matrix

| Variable | Simple Phase | For-Each Phase | Nested Workflow |
|----------|--------------|----------------|-----------------|
| `{{step.*}}` | No | Yes | Yes |
| `{{phase.*}}` | Yes | Yes | Yes |
| `{{sprint.*}}` | Yes | Yes | Yes |

## TypeScript Interface

```typescript
interface TemplateContext {
  step?: {
    prompt: string;
    id: string;
    index: number;
  };
  phase?: {
    id: string;
    index: number;
  };
  sprint?: {
    id: string;
    name?: string;
  };
}
```

## Usage Examples

### Step Context in For-Each

```yaml
# Top-level workflow with for-each
phases:
  - id: development
    for-each: step
    workflow: feature-workflow

# feature-workflow.yaml (nested)
phases:
  - id: implement
    prompt: |
      ## Task
      {{step.prompt}}

      ## Instructions
      Implement step {{step.id}} (index: {{step.index}})
```

### Sprint Context

```yaml
phases:
  - id: prepare
    prompt: |
      Initialize sprint: {{sprint.id}}
      Create branch: sprint/{{sprint.id}}
```

### Phase Context

```yaml
phases:
  - id: qa
    prompt: |
      Running phase: {{phase.id}}
      Phase index: {{phase.index}}
```

### Combined Variables

```yaml
phases:
  - id: verify
    prompt: |
      Verifying {{step.id}} in phase {{phase.id}}
      Sprint: {{sprint.id}}
      Task: {{step.prompt}}
```

## Output Artifacts Pattern

Use variables to create consistent artifact paths:

```yaml
phases:
  - id: plan
    prompt: |
      Write implementation plan to:
      context/{{step.id}}-plan.md

  - id: implement
    prompt: |
      Read plan from: context/{{step.id}}-plan.md
      Implement the requirements.
```

## Unresolved Variables

### Default Behavior

Unresolved variables remain as literal text in the output.

```yaml
# If step context is missing:
prompt: "Task: {{step.prompt}}"
# Outputs: "Task: {{step.prompt}}"
```

### Strict Mode

With compiler strict mode enabled, unresolved variables cause compilation errors.

## Common Patterns

### File Naming

```yaml
prompt: |
  Save to: artifacts/{{step.id}}-output.md
  Log to: logs/{{phase.id}}.log
```

### Git Operations

```yaml
prompt: |
  git checkout -b sprint/{{sprint.id}}
  git commit -m "{{phase.id}}: {{step.prompt}}"
```

### Progress Tracking

```yaml
prompt: |
  Processing step {{step.index}} of the sprint.
  Step ID: {{step.id}}
```

## Best Practices

1. **Use step.id for files** - Creates unique, traceable artifacts
2. **Include step.prompt in context** - Ensures task clarity
3. **Use sprint.id for branches** - Maintains sprint isolation
4. **Test variable resolution** - Verify substitution before deployment

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Variable not replaced | Wrong context (step.* in simple phase) | Check availability matrix |
| Empty value | Missing field in SPRINT.yaml | Verify source data |
| Literal `{{...}}` in output | Typo in variable name | Check spelling |
| Compilation error (strict) | Missing required context | Provide context or disable strict mode |
