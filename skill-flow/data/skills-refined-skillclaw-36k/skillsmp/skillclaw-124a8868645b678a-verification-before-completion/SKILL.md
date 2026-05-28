---
name: verification-before-completion
description: Use this skill when about to claim work is complete, fixed, or passing, before committing or creating PRs; it requires running verification commands and confirming output before making any success claims.
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency. **Core principle:** Evidence before claims, always.

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete).
3. READ: Full output, check exit code, count failures.
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence.
   - If YES: State claim WITH evidence.
5. ONLY THEN: Make the claim.

Skip any step = lying, not verifying.
```

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

- Using "should", "probably", "seems to".
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.).
- About to commit/push/PR without verification.
- Trusting agent success reports.
- Relying on partial verification.
- Thinking "just this once".
- Tired and wanting work over.
- **ANY wording implying success without having run verification.**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification. |
| "I'm confident" | Confidence ≠ evidence. |
| "Just this once" | No exceptions. |
| "Linter passed" | Linter ≠ compiler. |
| "Agent said success" | Verify independently. |
| "I'm tired" | Exhaustion ≠ excuse. |
| "Partial check is enough" | Partial verification is not sufficient. |