---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, or before committing/creating PRs; requires fresh verification evidence before any success claim.
allowed-tools: ["shell", "read_file", "update_plan"]
metadata:
  short-description: Evidence gate before completion claims
---

# Verification Before Completion

**Read these references:**
- `~/.config/agent/core/behavior.md` - Evidence-based reasoning
- `~/.config/agent/core/methodology.md` - Verify phase discipline
- `~/.config/agent/core/communication.md` - Accurate status reporting

## Overview

Claiming work is complete without verification is unacceptable. Evidence comes first.

**Core principle:** Evidence before claims, always.

## Mode-Aware Verification

Verification requirements apply to ALL modes, but execution differs:

**Normal mode:**
- Confirm before running verification commands
- Show user the commands that will be run
- Execute after confirmation

**Autopilot mode:**
- Auto-run verification commands (Tier 3 operations)
- Report progress: "Running tests..."
- Show results automatically

**Full-auto mode:**
- Auto-run verification commands
- Log to audit trail
- Only pause if verification fails repeatedly

**Verification failure handling:**
- Normal: Report failure, ask for guidance
- Autopilot: Attempt one auto-fix, then ask for guidance
- Full-auto: Attempt up to 3 auto-fixes, then stop and report (see `~/.config/agent/domain/coding/guardrails.md` recovery procedures)

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

BEFORE claiming any status or expressing satisfaction:

1. **Identify** the command that proves the claim
2. **Run** the full command (fresh, complete)
3. **Read** the full output and exit code
4. **Verify** the output supports the claim
   - If NO: state actual status with evidence
   - If YES: state the claim with evidence
5. **Only then** make the claim

Skipping any step is a failure to verify.

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test output shows 0 failures | Previous run, "should pass" |
| Linter clean | Linter output shows 0 errors | Partial check |
| Build succeeds | Build command exit 0 | Linter passing |
| Bug fixed | Test of original symptom passes | Code changed |
| Requirements met | Checklist verified | "Looks done" |

## Red Flags — STOP

- Using "should", "probably", "seems"
- Expressing satisfaction before verification
- About to commit/PR without verification
- Trusting agent success reports without evidence
- Relying on partial checks

## Examples

**Tests:**
```
✅ Run tests → see 0 failures → "All tests pass"
❌ "Should pass now"
```

**Build:**
```
✅ Run build → exit 0 → "Build passes"
❌ "Linter passed"
```

**Requirements:**
```
✅ Re-read plan → verify checklist → "Requirements met"
❌ "Seems complete"
```

If verification fails or behavior is unclear, switch to `systematic-debugging`.

## Common Verification Commands (Quick Reference)

| Language/Tooling | Command |
|------------------|---------|
| Go | `go test ./...` |
| Python | `pytest` |
| Node | `npm test` |
| Rust | `cargo test` |

## When to Apply

**Always before:**
- Any completion claim
- Any positive status statement
- Committing, PR creation, or moving to next task

## Arguments

Target: ${ARGUMENTS}
