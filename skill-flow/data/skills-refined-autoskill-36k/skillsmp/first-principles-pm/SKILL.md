---
name: first-principles-pm
description: First-principles project management - from idea to execution with maximum efficiency. Use when starting projects, evaluating requirements, or managing development workflow.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, TodoWrite, AskUserQuestion
---

# First-Principles Project Management

High-efficiency project management based on first principles thinking.

## Core Philosophy

> "The best part is no part. The best process is no process."

Every requirement, feature, and process must justify its existence. Default to deletion, not addition.

## The 5-Step Algorithm

Apply these steps **in order**. Do not skip ahead.

### Step 1: Question Every Requirement

**Goal**: Make requirements less stupid.

```
For each requirement, ask:
├── Who requested this? (Get a name, not a department)
├── Why is this needed? (What problem does it solve?)
├── What happens if we don't do it?
├── Is this the simplest way to solve the problem?
└── Can we achieve 80% of the value with 20% of the effort?
```

**Actions**:
- Challenge assumptions, especially from "smart people"
- Requirements from experts are often the most dangerous
- If you can't name the person who requested it, question it harder

### Step 2: Delete Parts and Processes

**Goal**: Remove everything that doesn't absolutely need to exist.

```
Deletion checklist:
├── Can we remove this feature entirely?
├── Can we remove this step in the process?
├── Can we remove this configuration option?
├── Can we remove this abstraction layer?
└── Can we remove this edge case handling?
```

**Validation rule**: If you don't end up adding back at least 10% of what you deleted, you didn't delete enough.

**Actions**:
- Delete first, ask questions later
- It's easier to add back than to remove
- Bias heavily toward deletion

### Step 3: Simplify and Optimize

**Goal**: Make remaining parts as simple as possible.

```
Simplification priorities:
├── Reduce parameters and options
├── Use conventions over configuration
├── Merge similar functionality
├── Flatten hierarchies
└── Remove indirection
```

**Warning**: Do NOT simplify or optimize something that should not exist. Complete Steps 1-2 first.

### Step 4: Accelerate Cycle Time

**Goal**: Move faster through validated work.

```
Acceleration tactics:
├── Shorter feedback loops
├── Smaller batch sizes
├── Parallel execution where possible
├── Remove approval bottlenecks
└── Automate repetitive checks
```

**Warning**: Do NOT accelerate something that should not exist. Complete Steps 1-3 first.

### Step 5: Automate

**Goal**: Automate only what remains after Steps 1-4.

```
Automation candidates:
├── Repetitive manual tasks
├── Error-prone processes
├── Testing and validation
├── Deployment and packaging
└── Monitoring and alerting
```

**Warning**: Automating a bad process just makes bad things happen faster.

## Project Workflow

### Phase A: Discovery (Question)

```yaml
inputs:
  - Raw requirements or problem statement

activities:
  - [ ] Identify the core problem (not the proposed solution)
  - [ ] List all stated requirements
  - [ ] For each requirement: Who? Why? What if not?
  - [ ] Identify hidden assumptions
  - [ ] Define success criteria (measurable)

outputs:
  - Validated problem statement
  - Prioritized requirements (P0/P1/P2)
  - Success metrics
```

### Phase B: Scope Reduction (Delete)

```yaml
inputs:
  - Validated requirements from Phase A

activities:
  - [ ] Challenge each P1/P2 requirement
  - [ ] Identify MVP (P0 only)
  - [ ] Remove nice-to-haves ruthlessly
  - [ ] Question each data field, API endpoint, UI element
  - [ ] Document what was deleted and why

outputs:
  - Minimal viable scope
  - "Not doing" list (explicit)
  - Deletion log for review
```

### Phase C: Design (Simplify)

```yaml
inputs:
  - Minimal scope from Phase B

activities:
  - [ ] Design simplest possible solution
  - [ ] Reduce configuration options
  - [ ] Use existing patterns/libraries
  - [ ] Avoid premature abstraction
  - [ ] Plan for iteration, not perfection

outputs:
  - Simple design document
  - Technical approach
  - Implementation plan
```

### Phase D: Execution (Accelerate)

```yaml
inputs:
  - Design from Phase C

activities:
  - [ ] Break into small, deliverable chunks
  - [ ] Implement in priority order
  - [ ] Get feedback early and often
  - [ ] Ship incrementally
  - [ ] Iterate based on real usage

outputs:
  - Working software
  - User feedback
  - Iteration backlog
```

### Phase E: Polish (Automate)

```yaml
inputs:
  - Working software from Phase D

activities:
  - [ ] Automate testing
  - [ ] Automate deployment
  - [ ] Add monitoring
  - [ ] Document (only what's needed)
  - [ ] Optimize based on real data

outputs:
  - Production-ready software
  - Automated pipelines
  - Operational runbooks
```

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Better Approach |
|--------------|--------------|-----------------|
| "Future-proofing" | Solves problems that may never exist | Build for today, refactor when needed |
| "Best practices" | Often cargo-culted without understanding | Understand the principle, apply judgment |
| "Enterprise patterns" | Adds complexity for "scalability" | Start simple, scale when proven necessary |
| "Comprehensive docs" | Outdated immediately, rarely read | Minimal docs, self-documenting code |
| "Full test coverage" | Tests implementation, not behavior | Test critical paths, not internals |

## Decision Framework

When facing a decision, ask in order:

1. **Can we not do this at all?** → Delete
2. **Can someone else do this?** → Delegate/Use existing
3. **Can we do less?** → Reduce scope
4. **Can we do it simpler?** → Simplify
5. **Can we do it faster?** → Accelerate
6. **Can we automate it?** → Automate

## Metrics That Matter

Focus on outcomes, not activity:

| Measure | Not |
|---------|-----|
| Problems solved | Features shipped |
| User value delivered | Lines of code |
| Time to feedback | Time spent coding |
| Things removed | Things added |
| Simplicity achieved | Complexity managed |

## Quick Reference

```
┌─────────────────────────────────────────────────────┐
│  FIRST-PRINCIPLES 5-STEP ALGORITHM                  │
├─────────────────────────────────────────────────────┤
│  1. QUESTION  → Make requirements less stupid       │
│  2. DELETE    → Remove parts and processes          │
│  3. SIMPLIFY  → Optimize what remains               │
│  4. ACCELERATE → Speed up the cycle                 │
│  5. AUTOMATE  → Only after steps 1-4                │
├─────────────────────────────────────────────────────┤
│  ⚠️  DO NOT skip steps or reverse order             │
│  ⚠️  DO NOT optimize what should be deleted         │
│  ⚠️  DO NOT automate bad processes                  │
└─────────────────────────────────────────────────────┘
```
