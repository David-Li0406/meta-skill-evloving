---
name: dynamic-tasks
description: Manages task complexity scoring and dynamic iteration limits. Decomposes problems into atomic items, scores complexity, and allocates appropriate loop counts. Use when tackling multi-step problems that need structured iteration management.
---

# Dynamic Task Management

Intelligent task decomposition and complexity-based iteration allocation.

## When to Use

- Multi-step implementation tasks
- Complex debugging sessions
- Iterative design refinement
- Any work requiring structured retry/revision cycles

## Core Concept

```
Problem → Decompose → Score → Allocate Loops → Execute → Re-evaluate
```

## Task Decomposition

Break problems into atomic items:

| Item Type | Characteristics | Example |
|-----------|-----------------|---------|
| **Atomic** | Single action, clear outcome | "Add email field to User model" |
| **Compound** | Multiple steps, dependencies | "Implement user auth" → decompose further |
| **Research** | Unknown scope, needs exploration | "Find why tests fail" |

### Decomposition Rules

1. **One verb per task**: "Create", "Update", "Fix", "Add", "Remove"
2. **Clear completion criteria**: Know when it's done
3. **No hidden dependencies**: If A needs B, list B first
4. **Testable outcome**: Can verify success

## Complexity Scoring

### Scoring Factors

| Factor | Low (1) | Medium (2) | High (3) |
|--------|---------|------------|----------|
| **Steps** | 1-2 | 3-5 | 6+ |
| **Tools** | 1 | 2-3 | 4+ |
| **Dependencies** | 0 | 1-2 | 3+ |
| **Uncertainty** | Known solution | Partial unknown | Mostly unknown |
| **Risk** | Reversible | Partially reversible | Hard to undo |

### Complexity Formula

```
Score = Steps + Tools + Dependencies + Uncertainty + Risk
Total: 5-7 = Low, 8-11 = Medium, 12-15 = High
```

### Quick Assessment

| Complexity | Description | Iterations |
|------------|-------------|------------|
| **Low** | Clear path, few steps, minimal risk | 3 |
| **Medium** | Some unknowns, multiple tools, moderate risk | 10 |
| **High** | Significant unknowns, many dependencies, high risk | 25 |

## Loop Allocation

### Base Iterations

```
Low complexity:    3 iterations
Medium complexity: 10 iterations
High complexity:   25 iterations
```

### Adjustment Factors

| Condition | Adjustment |
|-----------|------------|
| External API dependency | +2 |
| Concurrent/async code | +3 |
| Security-sensitive | +2 |
| Novel technology | +5 |
| Clear prior art | -2 |

## Execution Pattern

### Per-Task Loop

```
┌─────────────────────────────────────────┐
│           TASK EXECUTION LOOP           │
├─────────────────────────────────────────┤
│                                         │
│  Attempt ──→ Evaluate ──→ Success?      │
│     ▲              │         │          │
│     │         No   │    Yes  │          │
│     │              ▼         ▼          │
│     │      Iterations    Complete       │
│     │      Remaining?                   │
│     │         │                         │
│     │    Yes  │  No                     │
│     └─────────┘   │                     │
│                   ▼                     │
│              Escalate                   │
│                                         │
└─────────────────────────────────────────┘
```

### Iteration Tracking

```markdown
## Task: {Name}
**Complexity**: Medium (Score: 9)
**Iterations**: 4/10

| Attempt | Action | Result | Next |
|---------|--------|--------|------|
| 1 | Initial impl | Tests fail | Fix validation |
| 2 | Add validation | 2 tests pass | Fix edge case |
| 3 | Handle edge case | 4/5 pass | Fix timeout |
| 4 | Add timeout | All pass | ✅ Complete |
```

## Re-evaluation Triggers

Re-score complexity when:

- [ ] New dependencies discovered
- [ ] Scope changes mid-task
- [ ] Unexpected blockers appear
- [ ] 50% of iterations used without progress

### Re-evaluation Actions

| Situation | Action |
|-----------|--------|
| Easier than expected | Reduce remaining iterations |
| Harder than expected | Increase iterations, consider decomposition |
| Blocked | Pause, add blocker-resolution task |
| Scope creep | Split into multiple tasks |

## Escalation Protocol

When iterations exhausted:

```markdown
## Escalation: {Task Name}

**Iterations Used**: 10/10
**Progress**: 60%

**Blockers**:
1. {Blocker description}

**Options**:
(A) Accept partial completion
(B) Allocate 5 more iterations (justify)
(C) Decompose differently
(D) Abandon and document why
```

## Integration with Other Skills

### product-development

```markdown
Phase iteration limits use dynamic scoring:
- Simple requirement: Low (3 iterations)
- Complex feature: Medium (10 iterations)
- Architectural decision: High (25 iterations)
```

### software-engineering

```markdown
Implementation task scoring:
- Add field to model: Low
- Implement new endpoint: Medium
- Build distributed service: High
```

## Task Template

```markdown
## Task: {Name}

**Complexity Assessment**:
| Factor | Score | Reason |
|--------|-------|--------|
| Steps | {1-3} | {why} |
| Tools | {1-3} | {why} |
| Dependencies | {1-3} | {why} |
| Uncertainty | {1-3} | {why} |
| Risk | {1-3} | {why} |
| **Total** | {5-15} | {Low/Medium/High} |

**Iterations Allocated**: {N}
**Adjustments**: {+/- reasons}

**Completion Criteria**:
- [ ] {Criterion 1}
- [ ] {Criterion 2}
```

## Quick Reference

```
Low (3 loops):    Simple, known, reversible
Medium (10 loops): Some unknowns, moderate complexity
High (25 loops):   Complex, uncertain, high-stakes

Exhaust loops → Escalate → Don't infinite loop
New info → Re-score → Adjust allocation
```
