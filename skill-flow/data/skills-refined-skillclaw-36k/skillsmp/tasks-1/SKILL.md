---
name: tasks
description: Generate actionable task lists from implementation plan, organized by user story with dependencies
---

# Tasks - Task Breakdown

## Overview

Break down implementation plan into specific, actionable tasks organized by user story with proper dependency management.

**Announce at start:** "I'm using the tasks skill to generate actionable task breakdown."

## When to Use

- After creating technical implementation plan (`SpecKit/plan`)
- Before starting implementation
- When you need structured task list for execution

## Prerequisites

- ✅ Functional specification (`specs/<feature-id>/spec.md`)
- ✅ Technical implementation plan (`specs/<feature-id>/plan.md`)

## The Process

### Step 1: Review Plan

1. Read functional specification
2. Read implementation plan
3. Understand user stories and dependencies

### Step 2: Generate Task Breakdown

Create `specs/<feature-id>/tasks.md`:

**Task Organization:**

1. **By User Story**
   - Each user story becomes a separate implementation phase
   - Tasks grouped under each user story
   - Checkpoints after each user story phase

2. **Dependency Management**
   - Tasks ordered to respect dependencies
   - Models before services
   - Services before endpoints
   - Core functionality before edge cases

3. **Parallel Execution Markers**
   - Tasks that can run in parallel marked with `[P]`
   - Optimize development workflow

4. **File Path Specifications**
   - Each task includes exact file paths
   - Create vs Modify vs Test clearly indicated

5. **Test-Driven Development**
   - Test tasks included if TDD requested
   - Tests written before implementation
   - Test and implementation tasks paired

### Step 3: Task Structure

Each task should include:

```markdown
### Task N: [Component Name]

**User Story:** [Related user story]

**Dependencies:** [Previous tasks that must complete first]

**Files:**
- Create: `exact/path/to/file.swift`
- Modify: `exact/path/to/existing.swift:123-145`
- Test: `Tests/path/to/test.swift`

**Steps:**
1. [First step]
2. [Second step]
...

**Checkpoint:** [Validation criteria]
```

### Step 4: Validate Task Breakdown

Review for:
- Completeness: All plan items covered?
- Order: Dependencies respected?
- Clarity: Tasks actionable?
- Testability: Tests included?

## Example Usage

```
/speckit.tasks
```

The skill will:
1. Parse implementation plan
2. Break down into tasks by user story
3. Order tasks by dependencies
4. Mark parallelizable tasks
5. Include test tasks if TDD requested

## Output Format

```markdown
# Task Breakdown: [Feature Name]

## Phase 1: User Story 1 - [Description]

### Task 1: [Component]
**Dependencies:** None
**Files:** ...
**Steps:** ...

### Task 2: [Component]
**Dependencies:** Task 1
**Files:** ...
**Steps:** ...

**Checkpoint:** [Validation]

## Phase 2: User Story 2 - [Description]
...
```

## Key Principles

- **User story organization**: Group tasks by user story
- **Dependency respect**: Order tasks correctly
- **Parallelization**: Mark tasks that can run in parallel
- **File specificity**: Include exact file paths
- **Test inclusion**: Include test tasks if TDD requested

## Integration with Other Skills

- **Before**: Use `SpecKit/plan` to create implementation plan
- **After**: Use `SpecKit/implement` to execute tasks
- **Alternative**: Use `Superpowers/writing-plans` for more detailed, bite-sized steps

## Difference from Superpowers/writing-plans

- **SpecKit/tasks**: Task breakdown from plan (high-level tasks)
- **Superpowers/writing-plans**: Detailed implementation plan (bite-sized steps with exact code)

You can use both:
1. `SpecKit/tasks` for task organization
2. `Superpowers/writing-plans` for detailed step-by-step implementation
