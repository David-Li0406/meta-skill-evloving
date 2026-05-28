---
name: specify
description: Define what you want to build (requirements and user stories) - focus on WHAT and WHY, not the tech stack
---

# Specify - Functional Specifications

## Overview

Create detailed functional specifications focusing on **what** you're building and **why**, not the technical implementation details.

**Announce at start:** "I'm using the specify skill to create functional specifications."

## When to Use

- After establishing project constitution
- Before creating technical implementation plans
- When defining new features or requirements
- When clarifying user needs and business requirements

## The Process

### Step 1: Understand Requirements

1. Review project constitution (`.specify/memory/constitution.md`)
2. Understand the user's intent and requirements
3. Focus on **WHAT** and **WHY**, not **HOW**

### Step 2: Create Specification

Create specification in `specs/<feature-id>/spec.md` following the template:

**Required Sections:**

1. **Feature Overview**
   - Feature name and ID
   - High-level description
   - Business value and motivation

2. **User Stories**
   - As a [user type]
   - I want to [action]
   - So that [benefit]
   - Acceptance criteria

3. **Functional Requirements**
   - Core functionality
   - Edge cases
   - Error handling
   - Data validation rules

4. **Non-Functional Requirements**
   - Performance requirements
   - Security requirements
   - Accessibility requirements
   - Compatibility requirements

5. **Constraints and Assumptions**
   - Technical constraints
   - Business constraints
   - Assumptions about users/environment

6. **Review & Acceptance Checklist**
   - Requirements completeness
   - Clarity and specificity
   - Testability
   - Consistency with constitution

### Step 3: Create Feature Branch

- Create git branch: `001-<feature-name>` (or next sequential number)
- Commit specification to branch
- Use `Superpowers/using-git-worktrees` if needed for isolated workspace

### Step 4: Validate Specification

Ask user to review:
- Are all requirements captured?
- Are user stories clear and testable?
- Are edge cases covered?
- Does it align with project constitution?

## Example Prompt

```
/speckit.specify Build an application that can help me organize my photos in separate 
photo albums. Albums are grouped by date and can be re-organized by dragging and dropping 
on the main page. Albums are never in other nested albums. Within each album, photos are 
previewed in a tile-like interface.
```

## Output Structure

```
specs/
└── 001-<feature-name>/
    └── spec.md
```

## Key Principles

- **Be explicit**: Describe WHAT and WHY clearly
- **Don't specify tech stack**: Leave implementation details for planning phase
- **User-centric**: Focus on user needs and benefits
- **Testable**: Requirements should be verifiable
- **Complete**: Cover all aspects (happy path, edge cases, errors)

## Integration with Other Skills

After creating specification:
- Use `SpecKit/clarify` to clarify any underspecified areas
- Use `SpecKit/plan` to create technical implementation plan
- Use `Superpowers/brainstorming` if design exploration is needed

## Common Mistakes to Avoid

- ❌ Specifying implementation details (tech stack, algorithms)
- ❌ Vague requirements ("should be fast", "user-friendly")
- ❌ Missing edge cases or error scenarios
- ❌ Mixing requirements with design decisions
- ❌ Skipping user stories or acceptance criteria
