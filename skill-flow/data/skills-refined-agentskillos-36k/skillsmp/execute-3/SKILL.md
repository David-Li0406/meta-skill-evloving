---
name: execute
description: "Use when following a written plan or task list. Checkpoint verification at each step. Triggers - execute plan, follow plan, implement plan, next step, continue, proceed."
---

# Executing Plans

**Iron Law:** VERIFY each checkpoint before proceeding to the next step.

## Overview

Plans fail in execution, not conception. This skill ensures disciplined execution with checkpoint verification at every step. Deviation from plan without explicit acknowledgment is the primary failure mode.

## When to Use

- Following a written plan (from plan skill)
- Working through a task list or checklist
- Multi-phase implementations
- Any sequential work with dependencies
- After brainstorming when moving to implementation

## The Execution Loop

```
0. SYNC    -> Ensure workspace is current with origin/main
1. LOCATE  -> Find current step in plan
2. VERIFY  -> Check prerequisites are met
3. EXECUTE -> Complete the step (and only this step)
4. CONFIRM -> Verify step output matches expectation
5. UPDATE  -> Mark complete, document deviations
6. REPEAT  -> Move to next step
```

## Step 0: Sync - Create Worktree from Latest Origin

Before starting ANY execution, create an isolated worktree from the latest remote state.

**Use the git-worktrees skill** for the full workflow. Key points:

```bash
# ALWAYS fetch first
git fetch origin

# Create worktree from origin/main (NOT local main)
git worktree add .worktrees/feature-name origin/main -b feature/feature-name
cd .worktrees/feature-name

# Install dependencies and verify baseline
```

```markdown
## Workspace Setup Check

- [ ] Ran `git fetch origin`
- [ ] Created worktree from `origin/main` (not local main)
- [ ] Dependencies installed
- [ ] Baseline tests pass
```

**Why `origin/main`?** Local `main` may be behind remote. Always base new work on the latest remote state to avoid merge conflicts and building on stale code.

**NEVER skip this step.** Starting execution on stale code leads to painful rebases and wasted effort.

**See:** git-worktrees skill for full worktree workflow.

## Step 1: Locate - Find Current Step

Before executing anything, establish WHERE you are:

```markdown
## Current Execution State

**Plan Reference**: [file/location of plan]
**Current Phase**: Phase 2 of 4
**Current Step**: Step 3 of 5 in Phase 2
**Previous Step**: Completed [step name]
**Blockers**: None / [describe blocker]
```

**If no plan exists:** STOP. Invoke plan skill first.

## Step 2: Verify - Check Prerequisites

Each step has prerequisites. Verify ALL before starting:

```markdown
## Step Prerequisites Check

**Step**: "Create user authentication endpoint"

Prerequisites:
- [x] Database schema exists (verified: users table present)
- [x] Auth library installed (verified: package.json)
- [x] Prior step complete (verified: session middleware working)
- [ ] Test environment ready (BLOCKED: need env vars)

**Status**: BLOCKED - cannot proceed until env vars configured
```

**NEVER proceed with unmet prerequisites.** Document the blocker and either:
1. Resolve the blocker first
2. Escalate to user
3. Adjust plan with explicit acknowledgment

## Step 3: Execute - Complete This Step Only

Focus on the CURRENT step. Do not anticipate future steps.

```markdown
## Execution Focus

**Executing**: Step 3 - Create user authentication endpoint
**Scope**: ONLY this endpoint, nothing else
**NOT doing**: Frontend integration (Step 5), testing (Step 4)
```

**Scope Discipline:**
- Complete what the step says
- No more, no less
- Future optimizations wait for their step
- Resist "while I'm here" additions

### TDD Within Steps (MANDATORY for Code)

> **Iron Law:** Code step = TDD step. No exceptions.

When a step involves writing code, TDD is NOT optional:

```
┌─────────────────────────────────────────────────────────────┐
│  1. Write test FIRST (watch it fail)                        │
│  2. Write minimal code to pass                              │
│  3. Refactor while green                                    │
│  4. Then proceed to step verification                       │
└─────────────────────────────────────────────────────────────┘
```

**The sub-cycle within each code step:**

```
STEP START
    ↓
Is this a code step?
├── NO → Execute normally
└── YES → TDD cycle:
          ├── Write failing test
          ├── Verify test fails (RED)
          ├── Write minimal code
          ├── Verify test passes (GREEN)
          ├── Refactor if needed
          └── Continue to Step 4 (Confirm)
```

**Example - Step: "Add password validation"**

```markdown
## TDD Execution

**Test first:**
```typescript
test('rejects passwords under 8 characters', () => {
  expect(validatePassword('short')).toBe(false);
});
```

**Run test:** FAILS (validatePassword doesn't exist) ✓ RED

**Minimal code:**
```typescript
function validatePassword(password: string): boolean {
  return password.length >= 8;
}
```

**Run test:** PASSES ✓ GREEN

**Proceed to Step 4 (Confirm) with full verification**
```

**Common TDD Violations During Execution:**

| Violation | Reality |
|-----------|---------|
| "I'll add tests after" | Tests prove nothing after the fact |
| "This is too simple for TDD" | Simple code breaks. Test it. |
| "The plan didn't mention tests" | TDD is implicit for all code |
| "I'll test at the end of the phase" | Test each step. Not at the end. |

## Step 4: Confirm - Verify Step Output

Each step has expected outputs. Verify them:

```markdown
## Step Verification

**Step**: Create user authentication endpoint

**Expected Outputs**:
- [ ] POST /api/auth/login endpoint exists
- [ ] Returns JWT on success
- [ ] Returns 401 on failure
- [ ] Unit test for endpoint passes

**Verification Commands**:
```bash
npm test -- --testPathPattern="auth"
curl -X POST localhost:3000/api/auth/login -d '{"email":"test@test.com","password":"test"}'
```

**Actual Result**: [paste output]
**Step Status**: PASS / FAIL
```

**If verification fails:** Do NOT proceed. Debug, fix, re-verify.

## Step 5: Update - Mark Complete, Document Deviations

Update the plan with execution reality:

```markdown
## Step Completion

**Step 3**: Create user authentication endpoint
**Status**: COMPLETE
**Completed At**: [timestamp]

**Deviations from Plan**:
- Plan said "use bcrypt", used argon2 instead (more secure)
- Added rate limiting (not in plan, approved by user)

**Notes for Future Steps**:
- Rate limiting middleware now available for other endpoints
- Password reset will need similar pattern
```

**Deviation Protocol:**
1. Document WHAT changed
2. Document WHY it changed
3. Assess impact on future steps
4. Get user approval if significant

## Step 6: Repeat - Move to Next Step

Only after current step is VERIFIED COMPLETE:

```markdown
## Transition to Next Step

**Completed**: Step 3 - Authentication endpoint
**Next**: Step 4 - Write integration tests
**Prerequisites for Next**: [list and pre-check]
**Handoff Context**: [what next step needs to know]
```

## Progress Tracking

Maintain a running progress summary:

```markdown
## Plan Execution Progress

**Plan**: User Authentication Feature
**Started**: [date]
**Status**: In Progress

| Phase | Step | Status | Notes |
|-------|------|--------|-------|
| 1 | Schema design | COMPLETE | Used Prisma |
| 1 | Migration | COMPLETE | 3 tables created |
| 2 | Auth middleware | COMPLETE | JWT-based |
| 2 | Login endpoint | COMPLETE | With rate limiting |
| 2 | Logout endpoint | IN PROGRESS | Current step |
| 3 | Tests | PENDING | - |
| 4 | Integration | PENDING | - |

**Overall Progress**: 4/7 steps (57%)
**Blockers**: None
**ETA**: [estimate if known]
```

## Deviation Detection and Handling

### Minor Deviations (Continue with Documentation)

- Different library than specified (equivalent functionality)
- Additional error handling (improves quality)
- Refactored existing code (required for integration)

**Action:** Document and continue.

### Major Deviations (Pause and Reassess)

- Scope change required by discovery
- Blocker requires plan restructuring
- Dependencies unavailable
- Architecture assumption invalid

**Action:** Stop execution. Document finding. Revise plan. Get user approval.

```markdown
## Major Deviation Detected

**Step Affected**: Step 4 - Integrate with payment provider
**Deviation**: Payment provider API changed, documented approach won't work

**Impact Assessment**:
- Steps 4-6 need revision
- New API requires different auth flow
- Estimated additional effort: 2 days

**Recommended Actions**:
1. Revise steps 4-6 with new API requirements
2. Add API migration step
3. Update timeline

**Awaiting**: User approval to proceed with revised plan
```

## Completion Criteria

A plan is complete when:

```markdown
## Plan Completion Checklist

- [ ] All phases marked complete
- [ ] All steps verified with evidence
- [ ] All deviations documented
- [ ] All tests passing (if applicable)
- [ ] User acceptance obtained
- [ ] Handoff documentation created
- [ ] Plan archived with final status
```

## Examples

### Good Execution

```
Plan Step: "Add validation to user registration"

1. LOCATE: Phase 2, Step 3 of registration feature
2. VERIFY: Registration endpoint exists (confirmed),
           schema has required fields (confirmed)
3. EXECUTE: Added zod validation for email, password, name
4. CONFIRM:
   - npm test passes (23/23)
   - Invalid input returns 400 (tested with curl)
   - Valid input still works (tested)
5. UPDATE: Step 3 complete, no deviations
6. REPEAT: Moving to Step 4 - Email verification
```

### Bad Execution (DO NOT DO THIS)

```
Plan Step: "Add validation to user registration"

"Adding validation... also noticed the login could use
some cleanup, so I'll refactor that too... and while
I'm here, let me add password reset since it's related..."

[Multiple unplanned changes, no verification, no documentation]
```

**Why wrong:** Scope creep, no checkpoint verification, no deviation tracking.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll document later" | You won't. Document now. |
| "This small addition won't hurt" | Scope creep kills plans. Stick to the step. |
| "Verification is obvious" | Run the verification command anyway. |
| "Prerequisites are probably fine" | Check them explicitly. |
| "I know what comes next" | Follow the plan. Your memory deceives you. |
| "The plan is just a guide" | The plan is the contract. Deviate with documentation. |
| "Checkpoints slow me down" | Checkpoints prevent costly rework. |
| "I can see it works" | Seeing is not verifying. Run the test. |

## Red Flags - STOP and Start Over

- **Starting execution without a worktree from `origin/main`**
- Executing steps out of order
- Skipping prerequisite verification
- Making changes not in current step
- Not documenting deviations
- "While I'm here" additions
- Proceeding without step verification
- No progress tracking visible
- Multiple steps "in progress" simultaneously
- Ignoring blockers to continue
- **Writing code without a failing test first**
- **Skipping TDD "because the plan didn't mention tests"**

**If you catch yourself doing any of these: STOP. Return to Step 1.**

## Verification Checklist

Before starting execution:

- [ ] Ran `git fetch origin`
- [ ] Created worktree from `origin/main` (see git-worktrees skill)
- [ ] Dependencies installed and baseline tests pass

Before marking a step complete:

- [ ] Located current step in plan
- [ ] Verified all prerequisites met
- [ ] **If code step: followed TDD (test first, watch fail, then implement)**
- [ ] Executed only the current step scope
- [ ] Ran verification commands with evidence
- [ ] Documented any deviations
- [ ] Updated progress tracking
- [ ] Identified prerequisites for next step
- [ ] Created handoff context if needed

## Quick Reference

```
FIRST:       Sync with origin/main
BEFORE step: Check prerequisites
DURING step: Only current scope
AFTER step:  Verify output
ALWAYS:      Document deviations
NEVER:       Skip checkpoints
NEVER:       Multiple steps at once
NEVER:       Execute on stale code
```

## Integration

**Pairs with:**
- **git-worktrees** - Create isolated workspace from origin/main (Step 0)
- **plan** - Create plans before execution
- **brainstorm** - Inform execution decisions
- **verification** - Verify each checkpoint
- **tdd** - TDD within each step (MANDATORY for code)
- **session** - Track progress across sessions
