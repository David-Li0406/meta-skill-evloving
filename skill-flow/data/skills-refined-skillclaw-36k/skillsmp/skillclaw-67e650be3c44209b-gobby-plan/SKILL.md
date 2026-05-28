---
name: gobby-plan
description: Use this skill when the user asks to "/gobby-plan", "create plan", "plan feature", or "write specification". It guides users through structured specification planning and task creation.
---

# /gobby-plan - Implementation Planning Skill

Guide users through structured requirements gathering, specification writing, and task creation.

## Workflow Overview

1. **Requirements Gathering** - Ask questions to understand the feature.
2. **Draft Plan** - Write a structured plan document.
3. **Plan Verification** - Check for TDD anti-patterns and dependency issues.
4. **User Approval** - Present the plan for review.
5. **Task Creation** - Create tasks from the approved plan.
6. **Task Verification** - Update the plan with task references.

## Step 0: **REQUIRED** ENTER PLAN MODE

Before creating any plan, you must enter Claude Code's plan mode to explore the codebase and design the implementation approach.

**How to enter**: Use the `EnterPlanMode` tool or respond with a planning-focused message that triggers plan mode. This mode allows you to read files and design without making edits.

**Why required**: Plan creation requires understanding existing code patterns, architecture constraints, and dependencies before proposing new work.

## Step 1: Requirements Gathering

Ask the user:
1. "What is the name/title for this feature or project?"
2. "What is the high-level goal? (1-2 sentences)"
3. "Are there any constraints or requirements I should know about?"
4. "What are the unknowns or risks?"

## Step 2: Draft Plan Structure

Create a plan with:
- **Epic title**: The overall feature name.
- **Phases**: Logical groupings of work (e.g., "Foundation", "Core Implementation", "Polish").
- **Tasks**: Atomic units of work under each phase.
- **Dependencies**: Which tasks block which (use notation: `depends: #N` or `depends: Phase N`).

## Step 3: Write Plan Document

Write to `.gobby/plans/{kebab-name}.md`:

```markdown
# {Epic Title}

## Overview
{Goal and context from Step 1}

## Constraints
{Constraints from Step 1}

## Phase 1: {Phase Name}

**Goal**: {One sentence outcome}

**Tasks:**
- [ ] Task 1 title
- [ ] Task 2 title (depends: Task 1)
- [ ] Task 3 title (parallel)

## Phase 2: {Phase Name}

**Goal**: {One sentence outcome}

**Tasks:**
- [ ] Task 4 (depends: Phase 1)
- [ ] Task 5 (parallel with Task 4)

## Task Mapping

<!-- Updated after task creation -->
| Plan Item | Task Ref | Status |
|-----------|----------|--------|
```