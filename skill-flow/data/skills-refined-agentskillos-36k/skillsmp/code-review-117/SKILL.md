---
name: code-review
description: "Use when reviewing code changes or conducting PR reviews."
---

# Code Review

**Goal:** Find bugs, ensure quality, share knowledge.

## Process

```
UNDERSTAND -> What changed and why?
EXAMINE    -> Check code systematically
TEST       -> Run it yourself
FEEDBACK   -> Provide actionable comments
FOLLOW-UP  -> Verify fixes
```

## Examine Code

```bash
git diff main...feature-branch --stat
git checkout feature-branch && npm test
```

**Check:**
- Correctness: Logic? Edge cases? Error paths?
- Security: Input validation? Auth checked?
- Testing: Tests exist? Cover regressions?

## Feedback Severity

| Level | Meaning | Action |
|-------|---------|--------|
| Critical | Bug, security | Must fix |
| Important | Logic error | Should fix |
| Minor | Style, naming | Can fix later |

**Good Format:**
```markdown
**[Important]** Missing null check

`user` could be null if API fails. Throws at line 45.
```

## Review Checklist

1. Logic errors - Will it work?
2. Security holes - Can it be exploited?
3. Error handling - Will it crash?
4. Test coverage - Will regressions be caught?

## Block PR If

- Hardcoded credentials
- Disabled security checks
- Tests that always pass
- Catch-all error swallowing

## Decision Criteria

| Finding | Action |
|---------|--------|
| Critical issue | Block merge |
| Important issue | Request changes |
| Only minor/nitpicks | Approve with comments |

**Pairs with:** pr-workflow, verification, tdd
