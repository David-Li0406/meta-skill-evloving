---
name: workflow
description: Executes predefined multi-skill workflows with automatic chaining, iteration limits, and quality gates
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Skill
  - TodoWrite
  - AskUserQuestion
---

# Workflow

**Purpose:** Execute predefined multi-skill workflows with automatic chaining, iteration limits, and quality gates.

## When to Use

- Complex tasks requiring multiple skills in sequence
- Need automatic review-fix-review loops
- Want consistent quality gates across all work
- Tasks that need orchestration beyond single skills

## Available Workflows

### `implement-review-fix`

**Full workflow: implementation → review → fix → validate**

```
1. /nestjs (implementation)
2. /review (comprehensive)
3. /nestjs (fix issues) ← repeats up to 3x
4. /lint-fix
5. Quality gates (lint, typecheck, tests)
```

**Usage:**

```
/workflow implement-review-fix "Create user management with RBAC"
```

### `review-only`

**Review cycle without implementation**

```
1. /review (comprehensive)
2. /api-nestjs-reviewer
3. Report findings
```

**Usage:**

```
/workflow review-only "Review the auth module for security issues"
```

### `fix-and-validate`

**Fix specific issues and validate**

```
1. Understand the issue
2. Fix using appropriate skill
3. /review to verify
4. Run quality gates
```

**Usage:**

```
/workflow fix-and-validate "Fix the N+1 query in user list"
```

## Iteration Rules

### Maximum Iterations

All workflows have iteration limits to prevent infinite loops:

- **Review-Fix Loop:** Max 3 iterations
- **Quality Gate Failures:** Max 2 retry attempts
- **Total Runtime:** 10 minute timeout

### Escalation Triggers

Escalate to user when:

1. **3 review iterations** completed with issues remaining
2. **Quality gate fails** 2 times
3. **Timeout** reached
4. **Critical blocker** encountered

### Escalation Format

```
❌ Workflow cannot complete automatically

**Remaining Issues:**
- Issue 1: description
- Issue 2: description

**Why Auto-Fix Failed:**
- Explanation

**Options:**
1. Manual fix - I'll wait for you to fix manually
2. Accept as-is - Proceed with known issues
3. Different approach - Try a different implementation
```

## Workflow Configuration

Workflows can be configured with parameters:

```typescript
interface WorkflowConfig {
  maxReviewIterations?: number; // Default: 3
  maxQualityGateRetries?: number; // Default: 2
  timeoutMinutes?: number; // Default: 10
  requireUserApproval?: boolean; // Default: false
  skipTests?: boolean; // Default: false
}
```

## Custom Workflows

Create custom workflows by defining:

```yaml
name: my-custom-workflow
description: What it does
steps:
  - skill: nestjs
    params: 'implement user feature'
  - skill: review
    params: 'comprehensive review'
  - skill: lint-fix
    params: ''
  - skill: test-runner
    params: 'unit'
maxIterations: 3
qualityGates:
  - lint
  - typecheck
  - test
```

## Related Skills

- `nestjs` - Master NestJS coordinator
- `orchestrator` - General-purpose task coordination
- `review` - Comprehensive code review
