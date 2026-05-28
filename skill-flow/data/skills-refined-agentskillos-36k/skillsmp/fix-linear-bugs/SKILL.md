---
name: fix-linear-bugs
description: "Fix Linear issues tagged with \"bug\". Either produces a PR with the fix or explains why it won't be fixed. Triggers - fix bugs, linear bugs, bug triage, resolve bugs."
---

# Fix Linear Bugs

**Iron Law:** Bugs produce either a FIX (PR) or an EXPLANATION (won't fix). No middle ground.

> ⚠️ **ONE ISSUE AT A TIME**
>
> Work on ONE bug, submit PR, then move to the next.
> Do NOT start a second bug until the first has a PR submitted.
> This ensures focused work, clean commits, and proper review cycles.

## Overview

This skill handles Linear issues tagged with "bug". Every bug must be resolved with either:
1. A Pull Request that fixes it
2. A documented explanation of why it won't be fixed

```
Bug → Understand → EXPLORE CODEBASE → Reproduce → Decision
                         ↓                            ↓
              Find affected code          ┌──────────┴──────────┐
                                          ↓                     ↓
                                    FIX (PR)            WON'T FIX (Explanation)
```

## Valid Outcomes

| Outcome | When to Use | Action |
|---------|-------------|--------|
| **Fix with PR** | Bug is valid and fixable | TDD fix → `/submit-pr` |
| **Won't Fix** | Out of scope, by design, or not worth fixing | Comment explanation, close |
| **Duplicate** | Already reported/fixed | Link to original, close |
| **Cannot Reproduce** | Bug not reproducible | Request more info or close |
| **Needs More Info** | Insufficient details | Comment questions, keep open |

---

## The Workflow

### Step 1: List Pending Bugs (Priority Order)

**Filter by "Todo" status and work highest priority first:**

```typescript
mcp__linear-server__list_issues({
  label: "bug",
  state: "Todo",  // Only unstarted bugs
  limit: 20
});
// Note: Linear API doesn't filter by priority - sort results client-side
```

**Sort results by priority (work in this sequence):**
1. **Urgent** (priority: 1) - Drop everything
2. **High** (priority: 2) - Address soon
3. **Normal** (priority: 3) - Standard queue
4. **Low** (priority: 4) - When time permits
5. **No Priority** (priority: 0) - Needs triage first

### Step 2: Select a Bug (Highest Priority First)

Present bugs sorted by priority:

```markdown
## Pending Bugs (Priority Order)

| Priority | ID | Title | Age |
|----------|-----|-------|-----|
| 🔴 Urgent | PEA-301 | Login fails with special characters | 1 day |
| 🟠 High | PEA-315 | Pagination shows wrong count | 3 days |
| 🟡 Normal | PEA-320 | Tooltip misaligned | 5 days |

**Recommendation:** Start with PEA-301 (highest priority)

Which bug would you like to address?
```

**Default behavior:** If user says "next bug" without specifying, always pick the highest priority unaddressed bug.

### Step 3: Understand the Bug

Read the full issue:

```typescript
mcp__linear-server__get_issue({ id: "issue-uuid" });
```

Gather:
- What is the expected behavior?
- What is the actual behavior?
- Steps to reproduce
- Environment/context
- Impact/severity

### Step 4: Explore Codebase (MANDATORY)

**Before attempting to reproduce, explore the codebase to find affected code:**

```typescript
// Dispatch Explore agent for comprehensive analysis
Task({
  subagent_type: "Explore",
  prompt: `
    Research context for bug: "[bug title]"

    Bug details: [paste bug description]

    Find:
    1. Code files related to this functionality
    2. Existing tests for this area (may reveal expected behavior)
    3. Recent changes that might have introduced the bug
    4. Related error handling or validation logic
    5. Similar patterns elsewhere that work correctly

    Return findings to inform debugging and reproduction.
  `,
  description: "Explore codebase for bug context"
});
```

Or use direct search:

```bash
# Find related files
Glob: "**/*[feature-name]*"

# Search for error messages or related code
Grep: "error message from bug report"

# Check git history for recent changes
git log --oneline -20 -- src/affected/path/
```

**Present findings to user:**

```markdown
## Codebase Analysis

### Affected Code Found
- `src/auth/login.ts` - Login handler (lines 45-89)
- `src/auth/validate.ts` - Input validation (lines 12-34)
- `src/utils/sanitize.ts` - Sanitization helper

### Existing Tests
- `tests/auth/login.test.ts` - Has 5 tests, none for special chars
- Gap identified: No test coverage for edge case

### Recent Changes (potential cause)
- `abc123` (3 days ago): "refactor: improve input sanitization"
  - Changed `sanitize.ts` - LIKELY CULPRIT

### Related Patterns
- `src/auth/register.ts:67` - Similar validation, works correctly
- Difference: Register doesn't use sanitization on password

### Key Findings
1. **Likely root cause:** sanitize.ts:23 strips special chars
2. **Test gap:** No tests for special character passwords
3. **Working example:** Register flow handles this correctly
```

### Step 5: Reproduce the Bug

**Before writing any fix, REPRODUCE the bug:**

1. Set up the environment described
2. Follow reproduction steps
3. Observe the actual behavior
4. Document your findings

```markdown
## Reproduction Attempt

**Steps taken:**
1. [What you did]
2. [What you did]

**Result:** [Reproduced / Could not reproduce]
**Environment:** [Your test environment]
```

### Step 6: Decision Point

```
Can you reproduce it?
├── NO → Request more info OR close as "Cannot Reproduce"
└── YES → Is it worth fixing?
          ├── NO → Close as "Won't Fix" with explanation
          └── YES → Proceed to fix
```

### Step 7A: Fix the Bug (TDD)

**Use TDD process - test first:**

1. **Write failing test** that demonstrates the bug
2. **Run test** - verify it fails (proves bug exists)
3. **Write minimal fix** to pass the test
4. **Run test** - verify it passes
5. **Refactor** if needed

```markdown
## Bug Fix Plan

**Root Cause:** [What's causing the bug]
**Fix Approach:** [How you'll fix it]

**Test:** Will write test that [describes expected behavior]
**Files:** [Files to modify]
```

### Step 7B: Submit PR

After fix is verified locally:

```
Use /submit-pr skill for full PR pipeline
```

**PR Description must include:**
- Link to Linear issue
- Root cause explanation
- How fix addresses it
- Test coverage added

### Step 7C: Won't Fix / Close

If not fixing, document clearly:

```typescript
mcp__linear-server__create_comment({
  issueId: "bug-issue-uuid",
  body: `## Resolution: Won't Fix

**Reason:** [Why this won't be fixed]

**Options:**
${reasonType === 'by_design' ? '- This is intended behavior because [reason]' : ''}
${reasonType === 'out_of_scope' ? '- This is outside our current scope because [reason]' : ''}
${reasonType === 'not_worth_it' ? '- The fix cost outweighs the impact because [reason]' : ''}

**Alternatives:**
- [Any workarounds for the user]`
});

mcp__linear-server__update_issue({
  id: "bug-issue-uuid",
  state: "Canceled"  // Or your "Won't Fix" state
});
```

### Step 8: Confirm Resolution

```markdown
## Bug Resolved

**Bug:** PEA-301 - Login fails with special characters
**Resolution:** Fixed in PR #123
**Root Cause:** Input not properly escaped
**Test Added:** Yes - `tests/auth/login.test.ts`

Linear issue will auto-close when PR merges.

Next bug?
```

---

## Won't Fix Reasons

Use these templates:

### By Design
```
This behavior is intentional:
- [Explain the design decision]
- [Why it works this way]

If this causes issues for your use case, please create a feature request instead.
```

### Out of Scope
```
This is outside our current scope:
- [What scope it falls under]
- [Why it's not prioritized]

We may revisit this in the future. Creating a tracking issue for [timeframe/milestone].
```

### Cannot Reproduce
```
We could not reproduce this issue:
- Environment tested: [details]
- Steps followed: [steps]
- Result: [what happened]

Please provide:
- [ ] Browser/OS version
- [ ] Console errors
- [ ] Network requests
- [ ] Screen recording if possible
```

### Duplicate
```
This is a duplicate of [ISSUE-ID].

Tracking in the original issue. Closing this one.
```

---

## Example Session

**User says:** `/fix-linear-bugs`

**Step 1-2 - List & Select (Priority Order):**
```
## Pending Bugs (Todo Status, Priority Order)

| Priority | ID | Title | Age |
|----------|-----|-------|-----|
| 🔴 Urgent | PEA-299 | Payment fails silently | 2 hours |
| 🟠 High | PEA-301 | Login fails with special characters | 1 day |
| 🟡 Normal | PEA-315 | Pagination shows wrong count | 3 days |

**Recommendation:** Start with PEA-299 (Urgent priority)

Which bug would you like to address?
```

**User:** "PEA-301"

**Step 3 - Understand:**
```
## Bug Analysis: PEA-301

**Title:** Login fails with special characters
**Reporter:** User via support
**Priority:** High

**Expected:** User can login with password containing special chars
**Actual:** Login returns "Invalid credentials" error
**Steps to Reproduce:**
1. Create account with password "Test@123!"
2. Log out
3. Try to log in with same password
4. Error appears

**Impact:** Users with special character passwords cannot login
```

**Step 4 - Explore Codebase (MANDATORY):**
```
Dispatching Explore agent to research bug context...

## Codebase Analysis

### Affected Code Found
- `src/auth/login.ts` - Login handler (lines 45-89)
- `src/auth/validate.ts` - Input validation
- `src/utils/sanitize.ts` - Sanitization helper

### Existing Tests
- `tests/auth/login.test.ts` - 5 tests, none for special chars
- Gap: No test coverage for special character passwords

### Recent Changes (potential cause)
- `abc123` (3 days ago): "refactor: improve input sanitization"
  - Changed `sanitize.ts` - LIKELY CULPRIT

### Related Patterns
- `src/auth/register.ts:67` - Similar validation, works correctly
- Difference: Register doesn't sanitize password

### Key Findings
1. **Likely root cause:** sanitize.ts:23 strips special chars
2. **Test gap:** No tests for special character passwords
3. **Working example:** Register flow handles this correctly

### Recommended Investigation
Focus on `sanitize.ts` - compare with register flow.
```

**Step 5 - Reproduce:**
```
## Reproduction Attempt

**Steps:**
1. Created test account with password "Test@123!"
2. Logged out
3. Attempted login

**Result:** REPRODUCED - Got "Invalid credentials" error
**Environment:** Local dev server

**Confirmed:** sanitize.ts:23 strips "@" and "!" before comparison
```

**Step 6-7 - Fix (informed by exploration):**
```
## Bug Fix Plan

**Root Cause:** sanitize.ts:23 strips special characters before password comparison
**Fix:** Skip sanitization for password field (sanitize only display fields)

**TDD Plan:**
1. Write test: login with special char password should succeed
2. Verify test fails (confirms bug at sanitize.ts:23)
3. Add password exclusion to sanitize function
4. Verify test passes

Proceeding with fix...
```

[TDD implementation happens here]

```
## Fix Complete

**Test added:** `tests/auth/login.test.ts` - "handles special characters in password"
**Files modified:** `src/utils/sanitize.ts` (line 23)
**All tests passing:** Yes

Ready to submit PR?
```

**User:** "Yes"

[/submit-pr flow happens]

**Step 8 - Confirm:**
```
## Bug Resolved

**Bug:** PEA-301 - Login fails with special characters
**Resolution:** PR #45 - Fix password sanitization
**Root Cause:** Overly aggressive input sanitization (sanitize.ts:23)
**Test Added:** Yes

PR created, CI running. Linear issue will auto-close on merge.

Next bug?
```

---

## Quick Reference

```
FILTER:  state: "Todo" only (unstarted bugs)
ORDER:   Urgent → High → Normal → Low → No Priority
PROCESS: List → Select (by priority) → Understand → EXPLORE CODEBASE → Reproduce → Decide → Fix/Close → Confirm
OUTPUT:  PR (fix) OR Explanation (won't fix)
ALWAYS:  ONE BUG AT A TIME → PR → next bug. Work highest priority first, TDD for fixes

MANDATORY EXPLORATION:
- Use Explore agent for comprehensive analysis
- Find affected code, existing tests, recent changes
- Identify likely root cause BEFORE reproducing
- Check git history for potential culprit commits

VALID OUTCOMES:
- PR with fix (TDD process)
- Won't fix (documented reason)
- Duplicate (linked to original)
- Cannot reproduce (request more info)
- Needs more info (ask questions)

TOOLS:
- Task(subagent_type: "Explore") - Codebase exploration
- Glob, Grep, Read - Direct search
- git log - Check recent changes
- mcp__linear-server__list_issues (find bugs)
- mcp__linear-server__get_issue (read details)
- mcp__linear-server__create_comment (add explanation)
- mcp__linear-server__update_issue (close/update)
- /submit-pr (for fixes)
```

## Red Flags - STOP

- **Starting second bug before first has PR** → STOP, finish first bug
- About to fix without reproducing → STOP, reproduce first
- About to fix without test → STOP, write failing test first
- Closing without explanation → STOP, document why
- Can't decide fix vs won't fix → STOP, ask user

---

## Integration

**Uses:**
- **Linear MCP** - Issue operations
- **TDD skill** - Test-first bug fixes
- **submit-pr** - PR submission pipeline
- **debug** - For complex bugs

**Workflow with Linear:**
```
Bug found → Linear issue created
    ↓
/fix-linear-bugs
    ↓
├── Fix → PR → Merge → Issue auto-closes
└── Won't Fix → Comment → Close issue
```

## Trigger Keywords

- "fix bugs"
- "fix linear bugs"
- "linear bugs"
- "bug triage"
- "resolve bugs"
- "pending bugs"
