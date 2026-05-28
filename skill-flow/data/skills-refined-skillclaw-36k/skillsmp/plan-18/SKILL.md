---
name: plan
description: "Use when you have a spec or requirements for a multi-step task, before touching code. Triggers - plan, design, architect, implementation plan, spec, requirements."
---

# Writing Plans

**Iron Law:** NEVER write code before the plan is complete and approved.

## No Code Policy

> **Plans must be plain prose.** No code blocks, no implementation snippets. Describe tasks in clear written English. Code belongs in the implementation phase, not the plan.

Why:
- Plans should be readable by anyone (technical or not)
- Code in plans creates false precision - it will change during implementation
- Prose forces you to think through the approach, not just copy-paste patterns

## Overview

Plans bridge the gap between requirements and implementation. A good plan enables any skilled developer to execute correctly, even with zero context about the codebase. Plans fail when they're vague, miss edge cases, or skip verification steps.

## When to Use

- Before implementing any multi-step feature
- When requirements are defined but approach is unclear
- After brainstorming, when moving to structured execution
- When delegating work to subagents or other developers
- Before any change touching more than 3 files

## The Process

```
1. CLARIFY   -> Understand what we're building
2. RESEARCH  -> Understand the existing codebase
3. DESIGN    -> Structure the approach
4. DOCUMENT  -> Write the plan
5. VALIDATE  -> Review and approve
```

## Step 1: Clarify - Understand What We're Building

Before writing anything, ensure you understand:

```markdown
## Goal Clarification

**What**: [One sentence - what we're building]
**Why**: [Business/user value]
**Success Criteria**:
- [ ] Criterion 1 (measurable)
- [ ] Criterion 2 (testable)
- [ ] Criterion 3 (observable)

**Scope**:
- IN: [What's included]
- OUT: [What's explicitly excluded]

**Constraints**:
- Technical: [Stack, performance, etc.]
- Timeline: [Deadlines if any]
- Dependencies: [What must exist first]
```

**Ask clarifying questions if anything is unclear.** Do not proceed with assumptions.

## Step 2: Research - Understand the Codebase

Investigate before designing:

```markdown
## Codebase Research

**Relevant Files**:
- `src/path/to/related.ts` - Does X, we'll extend it
- `tests/path/to/tests.ts` - Existing test patterns
- `docs/architecture.md` - Relevant architecture

**Existing Patterns**:
- Authentication: Uses JWT middleware
- Error handling: Custom ApiError class
- Database: Prisma with transactions

**Similar Features**:
- User registration follows same flow
- Payment module has similar validation

**Gotchas Found**:
- Must use specific error format
- Tests require mock database
```

## Step 3: Design - Structure the Approach

Break down into phases and tasks:

```markdown
## Design Overview

**Architecture**: [2-3 sentences on approach]
**Tech Stack**: [Key technologies]

**Phases**:
1. Foundation - Setup and scaffolding
2. Core - Main implementation
3. Integration - Connect components
4. Testing - Verification
5. Polish - Edge cases, docs

**Risk Areas**:
- [Area 1] - Mitigation: [strategy]
- [Area 2] - Mitigation: [strategy]
```

## Step 4: Document - Write the Plan

### Plan Document Format

Plans should be written in plain prose. Here's the structure:

**Header Section:**
- Feature name and goal (one sentence)
- Status (Draft, In Review, Approved, In Progress, Complete)
- Estimated scope (Small, Medium, Large)
- Architecture summary (2-3 sentences on approach)

**Success Criteria:**
List 3-5 measurable criteria. Each should be verifiable - describe what success looks like, not how to verify it.

**Phases:**
Break work into logical phases (typically 3-5). Each phase should have:
- Clear objective (what this phase accomplishes)
- List of tasks with descriptive names
- Checkpoint criteria to verify phase completion

**Tasks:**
Each task should include:
- Which files will be created or modified (exact paths)
- What the task accomplishes in plain English
- How to verify it worked
- TDD order: write test first, then implementation

**Dependencies:**
List any packages, API keys, or external services needed.

**Risks:**
Identify potential problems and how to mitigate them.

**Alternatives:**
Document other approaches considered and why they weren't chosen.

### Task Granularity Rules

**Each step is ONE action (2-5 minutes max):**

Good:
- "Write the failing test for X" - one action
- "Run test to verify it fails" - one action
- "Implement minimal code to pass" - one action
- "Run test to verify it passes" - one action
- "Commit changes" - one action

Bad:
- "Implement the feature" - too vague
- "Add tests and implementation" - multiple actions
- "Write the authentication system" - way too big

### Plan Requirements Checklist

- [ ] Exact file paths (not "in the utils folder")
- [ ] Complete code snippets (not "add validation")
- [ ] Exact commands with expected output
- [ ] Each step is 2-5 minutes of work
- [ ] TDD order: test first, then implementation
- [ ] Commit after each logical unit
- [ ] Verification at each phase checkpoint
- [ ] No ambiguous instructions

## Step 5: Validate - Review and Approve

Before execution, verify the plan:

```markdown
## Plan Review Checklist

- [ ] Goal is clear and measurable
- [ ] All files have exact paths
- [ ] All code is complete (not pseudocode)
- [ ] All commands have expected outputs
- [ ] Steps are granular (2-5 min each)
- [ ] TDD pattern followed throughout
- [ ] Phase checkpoints are verifiable
- [ ] Dependencies are identified
- [ ] Risks have mitigations
- [ ] Someone with no context could execute this
```

**Get user approval before proceeding to execution.**

## Output Location

Save plans to the appropriate location:

1. If `docs/plans/` exists: `docs/plans/YYYY-MM-DD-feature-name.md`
2. Otherwise: `.claude/tasks/plan-feature-name.md`

## Execution Handoff

After saving the plan:

```markdown
## Plan Complete

**Saved to**: `docs/plans/2024-01-15-user-auth.md`
**Phases**: 4
**Tasks**: 12
**Estimated Scope**: Medium

**Ready to execute?** Two options:

1. **Sequential** - Execute tasks one by one with verification
2. **Subagent-Driven** - Dispatch parallel subagents per task

Which approach would you prefer?
```

## Examples

### Good Plan Excerpt

**Task 2.1: Add Password Hashing**

Files to create:
- src/utils/password.ts (password hashing utility)
- tests/utils/password.test.ts (unit tests)

Step 1: Write failing test that verifies passwords can be hashed and the hash differs from the original. Also test that the original password can be verified against its hash.

Step 2: Run the test and confirm it fails because the module doesn't exist yet.

Step 3: Implement the password utility with hashPassword and verifyPassword functions using bcrypt. The hash should be at least 50 characters.

Step 4: Run the test again and verify it passes.

Step 5: Commit with message describing the new password utility.

### Bad Plan (DO NOT DO THIS)

**Task: Implement Password System**
- Add password hashing
- Add verification
- Make sure it's secure
- Add tests

Files: utils folder

**Why wrong:** Vague tasks, no exact paths, no specific steps, no verification criteria.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The task is simple enough" | Simple tasks compound. Plan anyway. |
| "I'll figure it out as I go" | That's how bugs happen. Plan first. |
| "Plans take too long" | Plans save 10x the time in rework. |
| "I know this codebase" | Future you doesn't. Document it. |
| "Just one small change" | Small changes cascade. Plan the cascade. |
| "The user wants it now" | Rushing creates more delays. |

## Red Flags - STOP and Revise

- Tasks that take more than 10 minutes
- "Implement X" without specific steps
- Missing file paths
- Missing test commands
- Pseudocode instead of real code
- No verification checkpoints
- "Figure out the best approach" in a step
- Skipped phases or tasks

## Verification Checklist

Before calling the plan complete:

- [ ] Every task has exact file paths
- [ ] Every task has complete code
- [ ] Every task has run command with expected output
- [ ] Every phase has verification checkpoint
- [ ] Plan is executable by someone with no context
- [ ] Success criteria are measurable
- [ ] User has approved the plan

## Quick Reference

```
ALWAYS: Exact file paths
ALWAYS: Complete code (not pseudocode)
ALWAYS: Test first, then implement
ALWAYS: Expected output for commands
NEVER: "Implement X" without breakdown
NEVER: Skip verification steps
MINIMUM: 3 success criteria
```

## Integration

**Pairs with:**
- **brainstorm** - Generate options before planning
- **execute** - Execute the plan step by step
- **tdd** - TDD pattern within each task
- **verification** - Verify checkpoints
- **subagent-driven-development** - Parallel execution
