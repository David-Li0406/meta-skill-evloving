---
name: verification-before-completion
description: This skill should be used when claiming a task is "done", "complete", "finished", "fixed", "passing", or before committing. Requires running verification commands before making success claims.
allowed-tools: Bash, mcp__plugin_serena_serena, mcp__plugin_serena_serena_*
---

# Verification Before Completion

**Announce at start:** "I'm using the verification-before-completion skill to verify this work."

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```text
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```text
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

## When to Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction ("Great!", "Perfect!", "Done!")
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases ("tests pass", "done", "fixed")
- Paraphrases and synonyms ("looks good", "ready", "complete")
- Implications of success ("moving on to...")
- ANY communication suggesting completion/correctness

## Agent Report Verification

**CRITICAL: Do not trust agent success reports.**

```text
Agent reports "success" → Verify independently

1. Check VCS diff: git diff HEAD~1
2. Verify changes exist and match expectations
3. Run verification commands yourself
4. THEN report actual state
```

Agents may:
- Report partial completion as full
- Claim tests pass without running them
- Miss requirements they don't understand
- Be optimistic about their work

**Always verify, never trust.**

## Verification Patterns

| Claim | Requires | NOT Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

### Regression Test Verification (TDD Red-Green)

```text
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Done!")
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ tests ≠ build |
| "Agent said success" | Verify independently |
| "Partial check is enough" | Partial proves nothing |

## Examples

```text
✅ [Run npm test] [See: 34/34 pass] "All tests pass"
❌ "Should pass now"

✅ [Run build] [See: exit 0] "Build succeeds"
❌ "Linter passed" (linter doesn't verify build)

✅ Re-read plan → Checklist each item → "Requirements met"
❌ "Tests pass, phase complete" (tests ≠ requirements)
```

## Why This Matters

From real failure patterns:
- "I don't believe you" - trust broken with human partner
- Undefined functions shipped - would crash in production
- Missing requirements shipped - incomplete features delivered
- Time wasted: false completion → redirect → rework

**Violates:** "Honesty is a core value. If you lie, you'll be replaced."

## Real-World Impact

| Approach | Outcome |
|----------|---------|
| Claim without verification | 60% rework rate, broken trust |
| Verify then claim | 5% rework rate, high confidence |
| Time to verify | 30 seconds |
| Time to fix false claims | Hours of debugging + trust repair |

**The math is clear:** 30 seconds verification beats hours of rework.

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.

## Integration

This principle applies at every claim point:

- **TDD** - Verify RED, verify GREEN
- **finishing-a-development-branch** - Verify tests before merge options
- **execute-plan** - Each task verified before marking complete
- **code review** - Verify issues fixed before claiming addressed

Triggers independently when making claims outside formal workflows.
