---
name: debugging
description: Use when encountering bugs, test failures, or unexpected behavior - systematic root cause analysis before fixes, tools first, regression test required
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues. Symptom fixes are failure.

**Core principle:** Tools first, fixes second. Find root cause with evidence before proposing any fix.

**Announce at start:** "I'm using gambit:debugging to investigate this systematically."

## Rigidity Level

LOW FREEDOM - Follow the 6-phase process exactly. No fixes without root cause evidence. No closing without regression test and FIXED status classification. Use tools for investigation, not guessing.

## Quick Reference

| Phase | Action | STOP If | Tool |
|-------|--------|---------|------|
| 1 | Create bug Task | - | TaskCreate |
| 2 | Reproduce & gather evidence | Can't reproduce consistently | Bash, Read |
| 3 | Investigate root cause | Still guessing (no evidence) | WebSearch, Task (agents) |
| 4 | Write failing test (RED) | Test passes (doesn't catch bug) | Write, Bash |
| 5 | Fix and verify (GREEN) | Any test fails | Edit, Bash |
| 6 | Classify, close, and document | Status not FIXED | TaskUpdate |

**Fix Status Classification:**
| Status | Definition | Action |
|--------|------------|--------|
| FIXED | Root cause addressed, tests pass | Close Task |
| PARTIALLY_FIXED | Some aspects remain | Document, keep open |
| NOT_ADDRESSED | Fix missed the bug | Return to Phase 3 |
| CANNOT_DETERMINE | Need more info | Gather reproduction data |

**Critical sequence:** Task → Reproduce → Evidence → Root Cause → Failing Test → Fix → Verify → Classify → Close

## When to Use

**Use for ANY technical issue:**
- Test failures you need to fix
- Bugs reported by user
- Unexpected behavior in development
- Regression from recent change
- Build failures
- Performance problems

**Use ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't use for:**
- Implementing new features (use `gambit:execute-plan`)
- Refactoring (use `gambit:refactor`)
- Code that's working but ugly

## The Process

### Phase 1: Create Bug Task

**REQUIRED: Track from the start.**

```
TaskCreate
  subject: "Bug: [Clear description of symptom]"
  description: |
    ## Bug Description
    [What's wrong - be specific]

    ## Reproduction Steps
    1. [Step one]
    2. [Step two]
    3. [Expected vs actual behavior]

    ## Environment
    [Version, OS, relevant context]

    ## Status
    - [ ] Reproduced consistently
    - [ ] Root cause identified
    - [ ] Failing test written
    - [ ] Fix implemented
    - [ ] All tests pass
  activeForm: "Investigating bug"
```

**Then mark in progress:**
```
TaskUpdate
  taskId: "[bug-task-id]"
  status: "in_progress"
```

---

### Phase 2: Reproduce & Gather Evidence

**BEFORE attempting ANY fix:**

#### Step 2a: Read Error Messages Carefully

- Don't skip past errors or warnings
- Read stack traces completely
- Note line numbers, file paths, error codes
- Error messages often contain the exact solution

#### Step 2b: Reproduce Consistently

**Decision tree:**
- Can trigger reliably? → Go to Step 2c
- Intermittent? → Add logging/instrumentation, gather more data
- Can't reproduce? → **STOP. Cannot proceed without reproduction.**

```bash
# Run the failing test/scenario
go test ./path/to/failing_test.go -v
# or
npm test -- --grep "failing test name"
```

#### Step 2c: Check Recent Changes

```bash
# What changed recently?
git log --oneline -10
git diff HEAD~5..HEAD -- path/to/affected/code
```

**Ask:**
- What changed that could cause this?
- New dependencies, config changes?
- Environmental differences?

#### Step 2d: Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database):**

Add diagnostic instrumentation at each boundary:

```go
// Layer 1: Handler
log.Printf("=== Handler received: %+v", request)

// Layer 2: Service
log.Printf("=== Service processing: %+v", input)

// Layer 3: Database
log.Printf("=== Query result: %+v", result)
```

**Run once to gather evidence showing WHERE it breaks, THEN analyze.**

---

### Phase 3: Investigate Root Cause

**REQUIRED: Use tools for investigation, not guessing.**

#### Step 3a: Search for Error Message

**Dispatch internet-researcher agent:**

```
Task
  subagent_type: "hyperpowers:internet-researcher"
  description: "Search for error solution"
  prompt: |
    Search for error: [exact error message]

    Find:
    - Stack Overflow solutions
    - GitHub issues in [library] version [X]
    - Official documentation explaining this error
    - Known bugs and workarounds

    Return: Summary of solutions found and which applies to our case.
```

**Or use WebSearch directly for quick searches:**

```
WebSearch
  query: "[exact error message] [language/framework]"
```

Common findings:
- Known bug with workaround
- Configuration issue
- Version incompatibility

#### Step 3b: Investigate Codebase

**Dispatch codebase-investigator agent:**

```
Task
  subagent_type: "hyperpowers:codebase-investigator"
  description: "Investigate bug context"
  prompt: |
    Error occurs in function X at line Y.

    Find:
    - How is X called? What are the callers?
    - What does variable Z contain at this point?
    - Are there similar functions that work correctly?
    - What changed recently in this area?

    Return: Summary of code paths and likely root cause.
```

**Or use Explore agent for simpler investigations:**

```
Task
  subagent_type: "Explore"
  prompt: |
    Investigate this bug:

    Error: [exact error message]
    Location: [file:line]

    Questions to answer:
    - How does data flow to this point?
    - What conditions trigger this error?
    - Are there similar patterns elsewhere that work?
    - What assumptions is this code making?
```

#### Step 3c: Trace Data Flow Backward

**CRITICAL: Find where bad value ORIGINATES, not just where it causes symptoms.**

```
Start at error location (symptom)
    ↓
Where does this value come from?
    ↓
What called this with that value?
    ↓
Keep tracing backward until you find the SOURCE
    ↓
Fix at SOURCE, not at symptom location
```

**Example:**
```
NullPointerException at UserService.java:45
    ↑ email is null here
    ↑ User object passed from Controller
    ↑ User created in RegistrationHandler
    ↑ Email field not validated in DTO → THIS IS ROOT CAUSE
```

#### Step 3d: Form Hypothesis

**State clearly:** "I think X is the root cause because Y [evidence]"

**Evidence required:**
- Stack trace showing call path
- Log output showing state
- Code showing missing validation
- Test output showing failure mode

**STOP if no evidence.** Return to Step 3a-3c.

---

### Phase 4: Write Failing Test (RED)

**REQUIRED: Test must fail BEFORE fix, pass AFTER fix.**

#### Step 4a: Create Regression Test

Write the smallest test that reproduces the bug:

```go
func TestRejectsEmptyEmail(t *testing.T) {
    // Regression test for bug: [task-id]
    // Empty email was accepted, should fail validation

    _, err := CreateUser(User{Email: ""})

    if err == nil {
        t.Fatal("expected validation error for empty email")
    }
}
```

#### Step 4b: Verify Test FAILS (proves it catches the bug)

```bash
go test ./... -run TestRejectsEmptyEmail -v
# Expected: FAIL (bug exists, test catches it)
```

**Decision tree:**
- Test FAILS? → Good, go to Phase 5
- Test PASSES? → **STOP. Test doesn't catch the bug. Rewrite test.**

**If test passes immediately, it's not testing the bug.** The whole point is RED → GREEN.

---

### Phase 5: Fix and Verify (GREEN)

#### Step 5a: Implement Minimal Fix

Fix the ROOT CAUSE identified in Phase 3:

```go
func CreateUser(u User) (*User, error) {
    // FIX: Add validation that was missing
    if u.Email == "" {
        return nil, errors.New("email required")
    }
    // ... rest of implementation
}
```

**Rules:**
- ONE change addressing root cause
- No "while I'm here" improvements
- No bundled refactoring
- Minimal code to make test pass

#### Step 5b: Verify Test Now PASSES

```bash
go test ./... -run TestRejectsEmptyEmail -v
# Expected: PASS (fix works)
```

#### Step 5c: Run Full Test Suite

**REQUIRED: Use test-runner agent to avoid context pollution.**

```
Task
  subagent_type: "hyperpowers:test-runner"
  prompt: "Run: go test ./..."
```

**Decision tree:**
- All tests pass? → Go to Phase 6
- Other tests fail? → **STOP. Fix broke something. Investigate.**

#### Step 5d: If Fix Doesn't Work

**Count your fix attempts:**
- Attempt 1-2: Return to Phase 3, re-analyze with new information
- **Attempt 3+: STOP. Question the architecture.**

**Pattern indicating architectural problem:**
- Each fix reveals new problem in different place
- Fixes require "massive refactoring"
- Each fix creates new symptoms elsewhere

**If 3+ fixes failed:** Discuss with user before attempting more. This is NOT a failed hypothesis - this is a wrong architecture.

---

### Phase 6: Close and Document

#### Step 6a: Classify Fix Status

**REQUIRED: Classify before closing:**

| Status | Definition | Action |
|--------|------------|--------|
| **FIXED** | Root cause addressed, regression test passes, full suite passes | Close Task |
| **PARTIALLY_FIXED** | Some aspects addressed, others remain | Document what's left, keep open |
| **NOT_ADDRESSED** | Fix doesn't address actual bug | Return to Phase 3 |
| **CANNOT_DETERMINE** | Insufficient info to verify | Gather more reproduction data |

**Evidence required for FIXED status:**
- Root cause explanation (not just symptom description)
- Regression test output showing PASS
- Full test suite output
- Specific verification that bug is resolved

#### Step 6b: Update Task with Findings

```
TaskUpdate
  taskId: "[bug-task-id]"
  description: |
    ## Bug Description
    [Original description]

    ## Fix Status: FIXED
    **Evidence:**
    - Root cause: [explanation of what caused the bug]
    - Regression test: [test name] PASSES
    - Full suite: [N] tests pass
    - Fix verified: [specific verification that bug is resolved]

    ## Root Cause
    [What actually caused the bug - be specific]
    [File:line where fix was made]

    ## Fix
    [What was changed]

    ## Regression Test
    [Test name that prevents recurrence]
```

**If status is NOT FIXED:**
- **PARTIALLY_FIXED** → Document remaining work, create follow-up Task
- **NOT_ADDRESSED** → Return to Phase 3, do not close
- **CANNOT_DETERMINE** → Gather more info before closing

#### Step 6c: Mark Task Complete

```
TaskUpdate
  taskId: "[bug-task-id]"
  status: "completed"
```

#### Step 6d: Commit with Task Reference

```bash
git add -A
git commit -m "$(cat <<'EOF'
fix: [brief description]

Root cause: [explanation]
Regression test: [test name]

Task: [task-id]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

---

## Critical Rules

### Rules That Have No Exceptions

1. **Create Task before investigating** → Track from discovery to closure
2. **No fixes without root cause evidence** → Evidence = code path, logs, or test output showing WHY
3. **Test must fail before fix (RED)** → If test passes immediately, it doesn't catch the bug
4. **Run full test suite after fix** → Via test-runner agent
5. **If 3+ fixes fail, question architecture** → Stop and discuss with user

### Common Excuses

All of these mean: **STOP. Return to Phase 2-3.**

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too |
| "Emergency, no time for process" | Systematic is FASTER than thrashing |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem |
| "Obviously X is the cause" | "Obvious" fixes are often wrong. Get evidence. |

---

## Examples

### Bad: Fix Without Investigation

```
Developer sees: NullPointerException at UserService:45

"Obviously email is null. Add null check."

String email = user.getEmail() != null ? user.getEmail().toLowerCase() : "";

Bug "fixed"... but crashes continue with different data.
```

**Why it fails:**
- Fixed symptom (null at line 45), not root cause
- Didn't investigate WHY email is null
- Root cause: Registration endpoint doesn't validate email
- Null-check applied everywhere, root cause unfixed

### Good: Systematic Investigation

```
Developer sees: NullPointerException at UserService:45

Phase 1: Create Task
  "Bug: NullPointerException in UserService.getEmail()"

Phase 2: Reproduce
  $ curl -X POST /api/register -d '{"name":"test"}'
  # Consistently returns 500

Phase 3: Investigate
  WebSearch: "NullPointerException getEmail java"
  Explore agent: "Find where User objects are created"

  Trace backward:
    UserService:45 ← email null
    Controller:23 ← User from RegistrationHandler
    RegistrationHandler:15 ← User created without email validation

  ROOT CAUSE: Registration doesn't validate email field

Phase 4: Write failing test
  @Test void registrationRequiresEmail() {
      assertThrows(ValidationException.class, () ->
          register(new UserDTO(null, "password")));
  }
  // RUN: FAILS (bug exists) ✓

Phase 5: Fix root cause
  @PostMapping("/register")
  public User register(@RequestBody UserDTO dto) {
      if (dto.getEmail() == null || dto.getEmail().isEmpty()) {
          throw new ValidationException("Email required");
      }
      return userService.create(dto);
  }
  // RUN: Test PASSES ✓
  // Full suite: All pass ✓

Phase 6: Close Task
  Root cause: Registration endpoint missing email validation
  Fix: Added validation in RegistrationHandler
  Regression test: registrationRequiresEmail
```

### Bad: Test Written After Fix

```
Developer fixes validation bug, then writes test:

def validate_email(email):
    return "@" in email and len(email) > 0  # Fix

def test_validate_email():
    assert validate_email("user@example.com") == True  # Test after

# Test passes immediately - but only tests happy path
# Later, someone breaks validation:
def validate_email(email):
    return True  # Oops!

# Test STILL PASSES (only checked happy path)
```

**Why it fails:**
- Test written after fix → never saw it fail
- Only tests happy path remembered
- Doesn't test the actual bug (empty email)
- Regression goes undetected

### Good: Test Written Before Fix (RED-GREEN)

```
Phase 4: Write failing test FIRST
def test_empty_email_rejected():
    assert validate_email("") == False  # The bug case

def test_no_at_symbol_rejected():
    assert validate_email("invalid") == False

# RUN: FAILS (bug exists) ✓

Phase 5: Implement fix
def validate_email(email):
    if not email or "@" not in email:
        return False
    return True

# RUN: PASSES ✓

# Later regression attempt:
def validate_email(email):
    return True  # Oops!

# TEST CATCHES IT:
# FAIL: assert validate_email("") == False
```

---

## Verification Checklist

Before claiming bug fixed:

- [ ] Task created with reproduction steps
- [ ] Bug reproduced consistently
- [ ] Root cause identified with EVIDENCE (not guess)
- [ ] Wrote test that reproduces bug
- [ ] Verified test FAILS before fix (RED)
- [ ] Implemented fix addressing root cause (not symptom)
- [ ] Verified test PASSES after fix (GREEN)
- [ ] Ran full test suite (all pass)
- [ ] Classified fix status (FIXED with evidence)
- [ ] Updated Task with root cause, fix, and status classification
- [ ] Marked Task complete (only if status = FIXED)
- [ ] Committed with Task reference

**Can't check all boxes?** Return to the process.

**If status not FIXED:**
- PARTIALLY_FIXED → Document remaining work, keep Task open
- NOT_ADDRESSED → Return to Phase 3
- CANNOT_DETERMINE → Gather more reproduction data

---

## Integration

**This skill calls:**
- `gambit:tdd` (for RED-GREEN cycle)
- `gambit:verify` (for test suite verification)
- Explore agent (for codebase investigation)
- test-runner agent (for running tests without context pollution)
- WebSearch (for error message research)

**This skill is called by:**
- When bugs discovered during development
- When test failures need fixing
- When user reports bugs

**Workflow:**
```
Bug discovered
    ↓
gambit:debugging (this skill)
    ↓
Phase 1: Create Task
    ↓
Phase 2: Reproduce
    ↓
Phase 3: Investigate (tools first!)
    ↓
Phase 4: Write failing test (RED)
    ↓
Phase 5: Fix and verify (GREEN)
    ↓
Phase 6: Close Task
    ↓
Bug resolved with regression test
```

---

## Resources

**Investigation tools:**
- WebSearch for error messages
- Explore agent for codebase patterns
- Grep for finding similar code
- Read for understanding context

**When stuck:**
- Can't reproduce → Add logging, gather more data
- Don't understand error → WebSearch exact message
- Can't find root cause → Trace data flow backward
- Fix doesn't work → Question architecture (after 3 attempts)
- Test passes immediately → Test doesn't catch bug, rewrite

**Supporting techniques:**
- **Root cause tracing:** Trace backward through call stack to find origin
- **Defense in depth:** Add validation at multiple layers after finding root cause
- **Condition-based waiting:** Replace arbitrary timeouts with condition polling
