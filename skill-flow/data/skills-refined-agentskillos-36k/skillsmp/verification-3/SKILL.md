---
name: verification
description: Use before claiming work complete, fixed, or passing - requires running verification commands and confirming output; evidence before assertions always
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Announce at start:** "I'm using gambit:verification to confirm this with evidence."

## Rigidity Level

LOW FREEDOM - NO exceptions. Run verification command, read output, THEN make claim.

No shortcuts. No "should work". No partial verification. Run it, prove it.

## Quick Reference

| Claim | Verification Required | Not Sufficient |
|-------|----------------------|----------------|
| **Tests pass** | Run full test command, see 0 failures | Previous run, "should pass" |
| **Build succeeds** | Run build, see exit 0 | Linter passing |
| **Bug fixed** | Test original symptom, passes | Code changed |
| **Task complete** | Check all success criteria, run verifications | "Implemented the feature" |
| **All tasks done** | `TaskList` shows all completed | "All tasks done" |

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## When to Use

**ALWAYS before:**
- Any success/completion claim
- Any expression of satisfaction ("Great!", "Perfect!", "Done!")
- Committing, PR creation, task completion
- Moving to next task
- ANY communication suggesting completion/correctness

**Red flags you need this:**
- Using "should", "probably", "seems to"
- Expressing satisfaction before verification
- About to commit/push without verification
- Trusting agent success reports
- Relying on partial verification

## The Process

### 1. Identify Verification Command

What command proves this claim?

| Claim | Command |
|-------|---------|
| Tests pass | `go test ./...` or `npm test` |
| Build succeeds | `go build ./...` or `npm run build` |
| Linter clean | `golangci-lint run` or `npm run lint` |
| No TODOs | `rg "TODO" src/` |
| Task complete | Verify each success criterion |

### 2. Run the Command

Execute the full command (fresh, complete).

**For verbose commands (tests, hooks, commits):** Use test-runner agent
```
Task
  subagent_type: "test-runner"
  prompt: "Run: go test ./..."
```

**For other commands:** Run directly and capture output.

### 3. Read the Output

Full output, check exit code, count failures.

**Don't:**
- Skim for "PASS"
- Assume success from partial output
- Trust cached results

**Do:**
- Read complete output
- Count actual pass/fail numbers
- Check exit code

### 4. Verify Against Claim

Does output confirm the claim?

**If NO:** State actual status with evidence
```
Tests: 33 passed, 1 failed.
Failure: test_login_with_expired_token still fails.
The fix didn't handle expired tokens.
Investigating...
```

**If YES:** State claim WITH evidence
```
Tests pass. [Ran: go test ./..., Output: 34/34 passed, exit 0]
Ready to commit.
```

### 5. Only Then Make the Claim

After evidence gathered, make the claim with reference to evidence.

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Common Excuses

All of these mean: **STOP. Run verification.**

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

### Tests

```
GOOD: [Run test command] [See: 34/34 pass] "All tests pass"
BAD:  "Should pass now" / "Looks correct"
```

### Regression Tests (TDD Red-Green)

```
GOOD: Write → Run (fail) → Fix → Run (pass) → Verify regression caught
BAD:  "I've written a regression test" (without red-green verification)
```

### Build

```
GOOD: [Run build] [See: exit 0] "Build passes"
BAD:  "Linter passed" (linter doesn't check compilation)
```

### Task Completion

```
GOOD: Re-read task → Create checklist → Verify each → Report gaps or completion
BAD:  "Tests pass, task complete"
```

### Agent Delegation

```
GOOD: Agent reports success → Check VCS diff → Verify changes → Report actual state
BAD:  Trust agent report
```

## Task Tool Integration

### Before Marking Task Complete

```
TaskGet
  taskId: "current-task-id"
```

Read success criteria. Verify EACH criterion:

```markdown
## Task Verification

### Success Criteria Check

1. [ ] "POST /auth/login returns valid JWT"
   - Ran: `curl -X POST localhost:8080/auth/login -d '...'`
   - Output: `{"token": "eyJ..."}`
   - Status: VERIFIED

2. [ ] "Invalid password returns 401"
   - Ran: `curl -X POST localhost:8080/auth/login -d '{"password":"wrong"}'`
   - Output: `{"error": "Invalid credentials"}`, status 401
   - Status: VERIFIED

3. [ ] "All tests pass"
   - Ran: `go test ./...`
   - Output: `ok  ... 34/34 tests passed`
   - Status: VERIFIED

All criteria verified. Task complete.
```

THEN mark complete:
```
TaskUpdate
  taskId: "current-task-id"
  status: "completed"
```

### Before Marking Epic Complete

```
TaskList
```

Verify ALL subtasks show status="completed".

```
TaskGet
  taskId: "epic-task-id"
```

Review each success criterion. Run full verification.

## Pre-Commit Hook Assumption

**If your project uses pre-commit hooks enforcing tests:**
- All test failures are from your current changes
- Never check if errors were "pre-existing"
- Don't run `git checkout <sha> && pytest` to verify
- Pre-commit hooks guarantee previous commit passed
- Just fix the error directly

## Examples

### Bad: Claiming Success Without Verification

```
Developer modifies authentication logic.

Developer thinks: "This fix is straightforward, tests should pass now"

Developer writes: "Great! All tests passing. The bug is fixed."

[No test command run, no output shown]
```

**Why it fails:**
- "Should pass" ≠ evidence
- Confidence ≠ verification
- Might have broken other tests
- Might not have fixed the bug

### Good: Verification Before Claim

```
Developer modifies authentication logic.

Runs: go test ./...
Output: 33 passed, 1 failed
Failure: TestLoginWithExpiredToken

Developer writes:
"Tests: 33 passed, 1 failed.
Failure: TestLoginWithExpiredToken still fails.
The fix didn't handle expired tokens.
Investigating..."
```

**Why it works:**
- Ran actual command
- Read actual output
- Reported actual status
- No false claims

### Bad: Closing Task Without Criterion Verification

```
Task success criteria:
- [ ] All functions fully implemented (no stubs, no TODOs)
- [ ] Tests written and passing
- [ ] Pre-commit hooks pass

Developer implements functions.

Developer thinks: "I implemented everything, task complete"

TaskUpdate
  taskId: "task-id"
  status: "completed"

[No verification commands run]
```

**Why it fails:**
- Might have TODO comments left
- Specific tests not run
- Pre-commit hooks not checked

### Good: Verifying Each Criterion

```
TaskGet taskId: "task-id"

Success criteria:
- [ ] All functions fully implemented (no stubs, no TODOs)
- [ ] Tests written and passing
- [ ] Pre-commit hooks pass

Verification:

1. Check for TODOs:
   $ rg "TODO|FIXME" src/
   [no output]
   Status: VERIFIED

2. Run tests:
   $ go test ./...
   ok ... 12/12 tests passed
   Status: VERIFIED

3. Run pre-commit:
   $ pre-commit run --all-files
   [all checks passed]
   Status: VERIFIED

All criteria verified.

TaskUpdate
  taskId: "task-id"
  status: "completed"
```

## Verification Checklist

Before claiming tests pass:
- [ ] Ran full test command (not partial)
- [ ] Saw output showing 0 failures
- [ ] Used test-runner agent if output verbose

Before claiming build succeeds:
- [ ] Ran build command (not just linter)
- [ ] Saw exit code 0
- [ ] Checked for compilation errors

Before marking task complete:
- [ ] Re-read success criteria from task
- [ ] Ran verification for each criterion
- [ ] Saw evidence all pass
- [ ] THEN marked complete

Before marking epic complete:
- [ ] Ran `TaskList`
- [ ] Saw all subtasks completed
- [ ] Ran verification for epic success criteria
- [ ] THEN marked epic complete

## Integration

**This skill is called by:**
- `gambit:test-driven-development` (verify tests pass/fail)
- `gambit:executing-plans` (verify task success criteria)
- ALL skills before completion claims

**This skill calls:**
- test-runner agent (run tests, hooks, commits without output pollution)

**Agents used:**
- test-runner (run verbose commands, return summary only)

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
