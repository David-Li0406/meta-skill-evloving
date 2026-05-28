---
name: verification-before-completion
description: "Use when about to claim work is complete, fixed, or passing. Invoke BEFORE committing, creating PRs, or making any success claims. The Iron Law - evidence before assertions, always."
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**The Iron Law:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

**Violating the letter of this rule IS violating the spirit of this rule.**

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

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction ("Great!", "Perfect!", "Done!")
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## Verification Requirements

| Claim | Requires | NOT Sufficient |
|-------|----------|----------------|
| "Tests pass" | Test command output: 0 failures | Previous run, "should pass" |
| "Linter clean" | Linter output: 0 errors | Partial check, extrapolation |
| "Build succeeds" | Build command: exit 0 | Linter passing, logs look good |
| "Bug fixed" | Test original symptom: passes | "Code changed, assumed fixed" |
| "Regression test works" | Red-green cycle verified | Test passes once |
| "Agent completed" | VCS diff shows changes | Agent reports "success" |
| "Requirements met" | Line-by-line checklist | Tests passing |

## Key Verification Patterns

### Tests

```
CORRECT:
[Run test command] -> [See: 34/34 pass] -> "All tests pass"

WRONG:
"Should pass now" / "Looks correct"
```

### Regression Tests (TDD Red-Green)

```
CORRECT:
Write -> Run (pass) -> Revert fix -> Run (MUST FAIL) -> Restore -> Run (pass)

WRONG:
"I've written a regression test" (without red-green verification)
```

### Build

```
CORRECT:
[Run build] -> [See: exit 0] -> "Build passes"

WRONG:
"Linter passed" (linter doesn't check compilation)
```

### Requirements

```
CORRECT:
Re-read plan -> Create checklist -> Verify each item -> Report gaps or completion

WRONG:
"Tests pass, phase complete"
```

### Agent Delegation

```
CORRECT:
Agent reports success -> Check VCS diff -> Verify changes -> Report actual state

WRONG:
Trust agent report without verification
```

## Red Flags - STOP Immediately

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without verification
- Trusting agent success reports blindly
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work to be over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification command |
| "I'm confident" | Confidence is NOT evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter is NOT compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion is NOT an excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |
| "The code looks correct" | Looking is NOT running |
| "I made minimal changes" | All changes need verification |

## Verification Commands by Project Type

### Node.js / TypeScript
```bash
# Tests
npm test
npm run test:coverage

# Build
npm run build
npm run typecheck

# Lint
npm run lint
```

### Python
```bash
# Tests
pytest
pytest --cov

# Type check
mypy .

# Lint
ruff check .
```

### Go
```bash
# Tests
go test ./...

# Build
go build ./...

# Lint
golangci-lint run
```

### Rust
```bash
# Tests
cargo test

# Build
cargo build

# Lint
cargo clippy
```

## Verification Checklist

Before claiming completion:

- [ ] Identified the verification command(s)
- [ ] Ran command(s) in current session (not stale output)
- [ ] Read full output (not just "passed")
- [ ] Checked exit code is 0
- [ ] Counted failures/errors (must be 0)
- [ ] No warnings that indicate problems
- [ ] Evidence quoted in completion message

## Example: Correct Verification

```
I've implemented the retry logic. Let me verify:

$ npm test

PASS  src/__tests__/retry.test.ts
  retryOperation
    ✓ retries failed operations 3 times (15 ms)
    ✓ returns immediately on success (2 ms)
    ✓ throws after max retries exceeded (8 ms)

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total

All 3 tests pass. Build verification:

$ npm run build
Build succeeded (exit 0)

Implementation complete. Ready to commit.
```

## Example: Incorrect (Do NOT Do This)

```
I've implemented the retry logic. The tests should pass now.
Ready to commit!
```

**Why wrong:** No actual test run. No evidence. "Should pass" is not verification.

## Why This Matters

From real failures:
- User said "I don't believe you" - trust broken
- Undefined functions shipped - would crash in production
- Missing requirements shipped - incomplete features
- Time wasted on false completion -> redirect -> rework

**Honesty is a core value. If you lie, you'll be replaced.**

## Multi-Stage Verification

For complex completions, verify each stage:

```bash
# Stage 1: Unit tests
npm test

# Stage 2: Integration tests
npm run test:integration

# Stage 3: Build
npm run build

# Stage 4: Type check
npm run typecheck

# Stage 5: Lint
npm run lint
```

All must pass before claiming complete.

## Agent Verification Protocol

When delegating to sub-agents:

1. Agent reports success
2. **YOU verify** with `git diff` or `git status`
3. **YOU run** verification commands
4. **YOU confirm** changes match requirements
5. Only then report completion

**Never trust agent reports without independent verification.**

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.

## Integration

**Always loaded:** This is a Process skill, loaded at session start.

**Pairs with:**
- **tdd** - Verification is built into TDD cycle
- **git-expert** - Verify before commits and PRs
- **execute** - Verify each phase before proceeding
