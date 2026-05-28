---
title: Workflow Selection Guide
description: Guide for choosing the appropriate workflow for your sprint based on complexity, verification needs, and execution requirements.
keywords: workflow, selection, decision, complexity, verification, sprint-default, gherkin
skill: creating-sprints
---

# Workflow Selection Guide

How to choose the right workflow for your sprint.

## Available Workflows

| Workflow | Purpose | Verification | Complexity |
|----------|---------|--------------|------------|
| `sprint-default` | Full sprint lifecycle | Basic | Medium |
| `gherkin-verified-execution` | Verified development | Full gherkin | High |
| `execute-with-qa` | Execution with QA phase | QA checks | Medium |
| `flat-foreach` | Simple step iteration | None | Low |
| `flat-foreach-qa` | Iteration with QA | QA checks | Low-Medium |
| `execute-step` | Single task execution | None | Minimal |
| `feature-standard` | Feature implementation | Basic | Medium |
| `bugfix-workflow` | Quick bug fixes | Minimal | Low |

## Decision Tree

```text
How complex is your sprint?
├── Simple (1-2 steps, minimal verification)
│   └── Do you need any verification?
│       ├── YES → flat-foreach-qa
│       └── NO → flat-foreach or execute-step
│
├── Medium (3-6 steps, standard verification)
│   └── What type of work?
│       ├── Feature development → sprint-default
│       ├── Bug fixes → bugfix-workflow
│       └── Mixed tasks → execute-with-qa
│
└── Complex (5-10 steps, full verification)
    └── Is autonomous execution critical?
        ├── YES → gherkin-verified-execution
        └── NO → sprint-default
```

## Workflow Comparison

### By Verification Level

| Level | Workflow | What's Verified |
|-------|----------|-----------------|
| None | `flat-foreach`, `execute-step` | Nothing |
| Minimal | `bugfix-workflow` | Task completion |
| Basic | `sprint-default`, `feature-standard` | Build/test pass |
| Full QA | `execute-with-qa`, `flat-foreach-qa` | QA phase |
| Gherkin | `gherkin-verified-execution` | Scenarios + QA |

### By Use Case

| Use Case | Recommended Workflow |
|----------|---------------------|
| Multi-step feature | `sprint-default` |
| Complex autonomous work | `gherkin-verified-execution` |
| Quick bug fixes | `bugfix-workflow` |
| Simple iterations | `flat-foreach` |
| Learning/prototyping | `execute-step` |
| Production-critical | `gherkin-verified-execution` |

### By Step Count

| Steps | Recommended Workflows |
|-------|----------------------|
| 1-2 | `execute-step`, `flat-foreach` |
| 3-5 | `sprint-default`, `execute-with-qa` |
| 5-8 | `sprint-default`, `gherkin-verified-execution` |
| 8-10 | `gherkin-verified-execution` only |
| >10 | Break into multiple sprints |

## Workflow Details

### sprint-default

**Best for**: Standard multi-step feature development

```yaml
phases:
  - prepare: Initialize environment
  - development: For-each step execution
  - qa: Quality checks
  - deploy: Finalization
```

**Use when**:
- Building features with 3-8 steps
- Standard verification is sufficient
- Need prepare/deploy phases

### gherkin-verified-execution

**Best for**: Complex autonomous work requiring verification

```yaml
phases:
  - prepare: Initialize
  - development: For-each step with:
    - plan: Create gherkin scenarios
    - context: Gather implementation context
    - execute: Implement with verification
    - verify: Run scenario tests
    - qa: Quality checks
```

**Use when**:
- Autonomous execution is critical
- Steps are complex and need planning
- Full verification trail required
- Production-critical changes

### execute-with-qa

**Best for**: Steps that need verification without full gherkin

```yaml
phases:
  - development: For-each step
  - qa: Quality checks per step
```

**Use when**:
- Need QA but not full gherkin
- Medium complexity tasks
- Quick feedback on each step

### flat-foreach

**Best for**: Simple step iteration without extras

```yaml
phases:
  - execute: For-each step (just run it)
```

**Use when**:
- Simple, well-defined tasks
- No verification needed
- Fast iteration required

### flat-foreach-qa

**Best for**: Simple iteration with basic QA

```yaml
phases:
  - execute: For-each step
  - qa: Basic quality check
```

**Use when**:
- Simple tasks
- Want basic sanity check
- Don't need full verification

### execute-step

**Best for**: Single task execution

```yaml
phases:
  - execute: Run the step prompt
```

**Use when**:
- Step-level workflow reference
- One-off tasks
- Testing/prototyping

### bugfix-workflow

**Best for**: Quick, focused bug fixes

```yaml
phases:
  - investigate: Find root cause
  - fix: Implement fix
  - verify: Confirm fix works
```

**Use when**:
- Fixing specific bugs
- Fast turnaround needed
- Scope is well-defined

## Selection Checklist

| Question | If Yes | If No |
|----------|--------|-------|
| Is this production-critical? | gherkin-verified-execution | Consider simpler |
| Do I need full verification? | gherkin-verified-execution | execute-with-qa or less |
| Am I fixing bugs? | bugfix-workflow | Other workflows |
| Is this a prototype? | flat-foreach or execute-step | More structured |
| Are there 5+ complex steps? | gherkin-verified-execution | sprint-default |
| Do I need QA but not gherkin? | execute-with-qa | flat-foreach-qa |

## Common Patterns

### Feature Development

```yaml
workflow: sprint-default  # Standard features
# OR
workflow: gherkin-verified-execution  # Critical features
```

### Bug Fix Sprint

```yaml
workflow: bugfix-workflow  # Single bug
# OR
workflow: execute-with-qa  # Multiple related bugs
```

### Refactoring Sprint

```yaml
workflow: gherkin-verified-execution  # High-risk refactoring
# OR
workflow: sprint-default  # Standard refactoring
```

### Documentation Sprint

```yaml
workflow: flat-foreach  # Simple doc updates
# OR
workflow: execute-with-qa  # Important docs needing review
```

## Mixing Workflows

You can override workflow per step:

```yaml
workflow: sprint-default  # Default for sprint

steps:
  - prompt: Simple task
    # Uses sprint-default

  - prompt: Critical implementation
    workflow: gherkin-verified-execution  # Override for this step

  - prompt: Quick fix
    workflow: bugfix-workflow  # Override for this step
```

## When to Break Sprints

Consider breaking into multiple sprints when:

| Situation | Action |
|-----------|--------|
| >8 steps | Split into focused sprints |
| Mixed complexity | Group by complexity level |
| Different verification needs | Separate by workflow type |
| Long estimated duration | Split into sessions |
| Multiple unrelated goals | One sprint per goal |
