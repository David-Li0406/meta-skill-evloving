---
title: Workflow Patterns Reference
description: Common workflow patterns with examples and use cases.
keywords: patterns, templates, best practices, examples, workflow
skill: creating-workflows
---

# Workflow Patterns Reference

Reusable workflow patterns for common development scenarios.

## Pattern Overview

| Pattern | Phases | Use Case |
|---------|--------|----------|
| Minimal Execute | 1 | Simple task execution |
| Plan-Execute | 2 | Deliberate implementation |
| Plan-Execute-Verify | 3 | Implementation with testing |
| Full Feature | 4 | Complete feature lifecycle |
| Full Sprint | 4 | Sprint with iteration |
| Bug Fix | 3 | Diagnosis and repair |
| Flat For-Each | 1 | Simple step iteration |

## Pattern 1: Minimal Execute

Single-phase workflow for straightforward tasks.

```yaml
name: Minimal Execute
description: Direct task execution without phases
phases:
  - id: execute
    prompt: |
      Execute the following task:
      {{step.prompt}}
```

**Use when:**
- Tasks are self-contained
- No planning or verification needed
- Quick one-off operations

## Pattern 2: Plan-Execute

Two-phase workflow with deliberate planning.

```yaml
name: Plan Execute
description: Plan then implement
phases:
  - id: plan
    prompt: |
      Analyze and plan:
      {{step.prompt}}

      Create implementation plan in context/{{step.id}}-plan.md

  - id: execute
    prompt: |
      Execute based on plan:
      1. Read context/{{step.id}}-plan.md
      2. Implement the solution
      3. Commit changes
```

**Use when:**
- Tasks benefit from upfront analysis
- Implementation spans multiple files
- Decisions need documentation

## Pattern 3: Plan-Execute-Verify

Three-phase workflow with verification.

```yaml
name: Plan Execute Verify
description: Implementation with testing
phases:
  - id: plan
    prompt: |
      Plan implementation for:
      {{step.prompt}}
      Output: context/{{step.id}}-plan.md

  - id: execute
    prompt: |
      Implement following context/{{step.id}}-plan.md
      Commit logical units separately.

  - id: verify
    prompt: |
      Verify implementation:
      1. Run related tests
      2. Check for regressions
      3. Validate against requirements
```

**Use when:**
- Quality assurance is important
- Changes may affect existing functionality
- Automated tests exist

## Pattern 4: Full Feature Lifecycle

Four-phase workflow for complete feature implementation.

```yaml
name: Full Feature
description: Complete feature lifecycle
phases:
  - id: plan
    prompt: |
      ## Task
      {{step.prompt}}

      ## Instructions
      1. Analyze requirements
      2. Identify affected files
      3. Document approach
      Output: context/{{step.id}}-plan.md

  - id: implement
    prompt: |
      Implement based on context/{{step.id}}-plan.md
      - Follow code conventions
      - Make atomic commits
      - Handle edge cases

  - id: test
    prompt: |
      Write and run tests:
      1. Unit tests for new functions
      2. Integration tests if needed
      3. Run existing test suite

  - id: document
    prompt: |
      Update documentation:
      1. API docs if interfaces changed
      2. README if user-facing
      3. Code comments for complex logic
```

**Use when:**
- Implementing substantial features
- Documentation is expected
- Full test coverage required

## Pattern 5: Full Sprint Workflow

Top-level sprint workflow with for-each development.

```yaml
name: Full Sprint
description: Complete sprint with step iteration
phases:
  - id: prepare
    prompt: |
      Initialize sprint:
      1. Create branch: sprint/{{sprint.id}}
      2. Gather initial context
      3. Document setup in context/_shared.md

  - id: development
    for-each: step
    workflow: feature-standard

  - id: qa
    prompt: |
      Sprint quality assurance:
      1. Run full test suite
      2. Execute linter and type checks
      3. Security audit
      4. Review all changes

  - id: deploy
    prompt: |
      Finalize sprint:
      1. Push all changes
      2. Create PR: gh pr create
      3. Add reviewers and labels
```

**Use when:**
- Running full development sprints
- Multiple steps need processing
- Standard CI/CD pipeline

## Pattern 6: Bug Fix Workflow

Focused workflow for diagnosing and fixing bugs.

```yaml
name: Bug Fix
description: Diagnose, fix, verify
phases:
  - id: diagnose
    prompt: |
      ## Bug
      {{step.prompt}}

      ## Instructions
      1. Reproduce the bug
      2. Analyze logs and errors
      3. Identify root cause
      Output: context/{{step.id}}-diagnosis.md

  - id: fix
    prompt: |
      Fix based on context/{{step.id}}-diagnosis.md
      - Minimal change required
      - No scope creep
      - Atomic commit

  - id: verify
    prompt: |
      Verify fix:
      1. Confirm bug is resolved
      2. Run regression tests
      3. Add test case if appropriate
```

**Use when:**
- Fixing reported bugs
- Minimal change needed
- Root cause analysis required

## Pattern 7: Flat For-Each

Minimal workflow for step iteration without nesting.

```yaml
name: Flat For-Each
description: Execute all steps directly
phases:
  - id: execute-all
    for-each: step
    workflow: execute-step
```

With simple step workflow:

```yaml
# execute-step.yaml
name: Execute Step
phases:
  - id: execute
    prompt: |
      Execute: {{step.prompt}}
```

**Use when:**
- Steps are independent
- No shared setup/teardown
- Simple sequential execution

## Pattern Selection Guide

```text
How complex is the task?
│
├─ Very simple (single action)
│  └─ Pattern 1: Minimal Execute
│
├─ Needs planning
│  │
│  ├─ No verification needed
│  │  └─ Pattern 2: Plan-Execute
│  │
│  └─ Needs verification
│     │
│     ├─ No documentation needed
│     │  └─ Pattern 3: Plan-Execute-Verify
│     │
│     └─ Documentation needed
│        └─ Pattern 4: Full Feature
│
├─ Multiple steps (sprint)
│  └─ Pattern 5: Full Sprint
│
├─ Bug fix
│  └─ Pattern 6: Bug Fix
│
└─ Simple iteration
   └─ Pattern 7: Flat For-Each
```

## Combining Patterns

Patterns can be nested. A sprint workflow (Pattern 5) typically uses a feature workflow (Pattern 3 or 4) for its development phase:

```yaml
# Sprint level uses Pattern 5
phases:
  - id: prepare
    prompt: "..."
  - id: development
    for-each: step
    workflow: full-feature  # References Pattern 4
  - id: qa
    prompt: "..."
```

## Customization Tips

1. **Add phases** - Insert phases between existing ones
2. **Remove phases** - Delete phases that don't apply
3. **Merge phases** - Combine simple related phases
4. **Change iteration** - Switch between simple and for-each
5. **Reference different workflows** - Swap nested workflow references
