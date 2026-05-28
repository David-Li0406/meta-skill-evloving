---
title: Phase Types Reference
description: Detailed explanation of simple phases vs for-each phases with decision criteria and examples.
keywords: phase, simple, for-each, iteration, workflow, decision
skill: creating-workflows
---

# Phase Types Reference

Workflows consist of phases. Each phase is either a **simple phase** (direct execution) or a **for-each phase** (iteration over steps).

## Phase Type Comparison

| Aspect | Simple Phase | For-Each Phase |
|--------|--------------|----------------|
| Execution | Once per workflow | Once per step in SPRINT.yaml |
| Prompt Source | Inline `prompt` field | Referenced workflow |
| Step Variables | Not available | Available (`{{step.*}}`) |
| Use Case | Setup, QA, deploy | Development, step iteration |
| Nesting | No | Yes (references another workflow) |

## Simple Phase

### Structure

```yaml
- id: <unique-identifier>
  prompt: |
    Instructions for this phase.
    Can use {{phase.*}} and {{sprint.*}} variables.
```

### Characteristics

- Executes exactly once
- Prompt defined inline
- No access to step context
- Ideal for sprint-level operations

### Examples

**Preparation Phase**
```yaml
- id: prepare
  prompt: |
    Initialize the sprint environment.
    Create branch: sprint/{{sprint.id}}
    Set up development environment.
```

**QA Phase**
```yaml
- id: qa
  prompt: |
    Run quality assurance checks:
    1. Execute test suite: npm test
    2. Run linter: npm run lint
    3. Type check: npm run typecheck
```

**Deploy Phase**
```yaml
- id: deploy
  prompt: |
    Finalize sprint:
    1. Push all changes
    2. Create pull request
    3. Add reviewers
```

## For-Each Phase

### Structure

```yaml
- id: <unique-identifier>
  for-each: step
  workflow: <workflow-reference>
```

### Characteristics

- Executes once per step in SPRINT.yaml
- References external workflow for each iteration
- Provides step context to nested workflow
- Creates hierarchical execution tree

### Examples

**Development Phase**
```yaml
- id: development
  for-each: step
  workflow: feature-standard
```

**Execute All Steps**
```yaml
- id: execute-all
  for-each: step
  workflow: execute-step
```

## Decision Tree

```text
What does this phase need to do?
│
├─ Process each step from SPRINT.yaml individually?
│  │
│  └─ YES → FOR-EACH PHASE
│           └─ Create or reference a step-level workflow
│              that uses {{step.prompt}}, {{step.id}}
│
└─ Perform sprint-level operation (setup, QA, deploy)?
   │
   └─ YES → SIMPLE PHASE
            └─ Write inline prompt with instructions
```

## When to Use Each Type

### Use Simple Phase When:

| Scenario | Example |
|----------|---------|
| Sprint initialization | Create branch, setup environment |
| Quality assurance | Run tests, lint, type check |
| Deployment | Create PR, push changes |
| Single operation | Generate report, cleanup |
| No step iteration needed | Global configuration |

### Use For-Each Phase When:

| Scenario | Example |
|----------|---------|
| Implementing features | Each step is a separate feature |
| Processing items | Each step needs same workflow |
| Step-specific artifacts | Create plan/output per step |
| Isolated execution | Each step runs in fresh context |

## Mixing Phase Types

Most sprint workflows combine both types:

```yaml
name: Standard Sprint
phases:
  # Simple: Setup (once)
  - id: prepare
    prompt: "Initialize sprint environment"

  # For-each: Development (per step)
  - id: development
    for-each: step
    workflow: feature-standard

  # Simple: QA (once)
  - id: qa
    prompt: "Run all quality checks"

  # Simple: Deploy (once)
  - id: deploy
    prompt: "Create PR and finalize"
```

## Nested Workflow Design

For-each phases reference step-level workflows that receive step context:

### Top-Level Workflow

```yaml
# sprint-workflow.yaml
phases:
  - id: development
    for-each: step
    workflow: step-implementation
```

### Step-Level Workflow

```yaml
# step-implementation.yaml
name: Step Implementation
phases:
  - id: plan
    prompt: |
      Plan implementation for: {{step.prompt}}
      Output: context/{{step.id}}-plan.md

  - id: implement
    prompt: |
      Implement based on plan.
      Reference: context/{{step.id}}-plan.md

  - id: verify
    prompt: |
      Verify implementation of {{step.id}}
```

## Compiled Output Structure

### Simple Phase → Single Task

```yaml
# PROGRESS.yaml
phases:
  - id: prepare
    status: pending
    prompt: "Initialize sprint environment"
```

### For-Each Phase → Steps Array

```yaml
# PROGRESS.yaml
phases:
  - id: development
    status: pending
    steps:
      - id: step-1
        prompt: "Implement auth"
        status: pending
        phases:
          - id: plan
            status: pending
            prompt: "Plan implementation for: Implement auth"
          - id: implement
            status: pending
            prompt: "Implement based on plan."
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Using `{{step.*}}` in simple phase | Variables won't resolve | Use for-each or remove step vars |
| For-each without workflow | Compilation error | Add `workflow` reference |
| Simple phase with `workflow` | Invalid combination | Remove workflow or add for-each |
| For-each with inline `prompt` | Invalid combination | Remove prompt, use workflow |
