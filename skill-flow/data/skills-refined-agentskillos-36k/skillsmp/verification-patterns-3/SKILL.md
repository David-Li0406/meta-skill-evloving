---
name: verification-patterns
description: Evidence-based verification of completed work. Use when verifying task completion, confirming work is done, validating changes, or checking if a task is finished.
---

# Verification Patterns

> "The most impactful tip is: **always ask Claude Code to verify it has completed the task.**"
> — Boris

## Core Principle

**Never trust "I've completed X" without evidence.**

Verification means proving work is done, not just saying it is.

## The Verification Protocol

### Step 1: Identify Claims

What work was supposedly completed?
- Code changes made
- Bugs fixed
- Features added
- Tests written

### Step 2: Define Evidence

For each claim, what would prove it?

| Claim | Evidence |
|-------|----------|
| Bug fixed | Reproduction steps no longer fail |
| Feature added | Feature works as specified |
| Tests written | Tests exist and pass |
| Code changed | Diff shows expected changes |

### Step 3: Gather Evidence

```bash
# Check code changes
git diff --stat

# Run tests
npm test

# Verify build
npm run build

# Check behavior
curl http://localhost:3000/api/endpoint
```

### Step 4: Report Results

For each claim:
- ✅ Verified with evidence
- ⚠️ Partially verified
- ❌ Not verified

## Evidence Types

### Code Evidence
- File diffs showing changes
- New files created
- Tests added

### Runtime Evidence
- Tests passing
- Build succeeding
- Application running

### Behavioral Evidence
- Feature works as expected
- Bug no longer reproducible

## Verification Checklist

```markdown
### Code Changes
- [ ] Files modified as intended
- [ ] No unintended changes

### Tests
- [ ] All existing tests pass
- [ ] New tests added (if applicable)

### Build
- [ ] Build completes without errors

### Behavior
- [ ] Primary functionality works
- [ ] No regressions introduced
```

## Anti-Patterns

### "I've done it"
Bad: "I've added the login feature."
Good: "Login feature added. Tests pass: 12/12. Login flow verified working."

### "Should work"
Bad: "This should fix the bug."
Good: "Bug fixed. Reproduced issue, applied fix, confirmed issue no longer occurs."

## Remember

**"Show me, don't tell me."**
