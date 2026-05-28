---
name: requesting-code-review
description: "Use after completing tasks, implementing major features, or before merging to verify work meets requirements."
---

# Requesting Code Review

Request code review to catch issues before they cascade.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in implementation plan
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## Two-Stage Review

### Stage 1: Spec Compliance
- Does the code match the plan/spec?
- Are all requirements addressed?
- Missing functionality?

### Stage 2: Code Quality
- Clean code principles
- Security concerns
- Performance issues
- Test coverage

## How to Request

**1. Gather context:**
```bash
# Get commit range
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Provide review context:**
- What was implemented
- What it should do (plan/requirements)
- Commit range (BASE to HEAD)
- Brief summary

**3. Act on feedback:**

| Severity | Action |
|----------|--------|
| 🔴 Critical | Fix immediately, blocks progress |
| 🟠 Important | Fix before proceeding |
| 🟢 Minor | Note for later |

## Review Request Template

```markdown
## Code Review Request

**What was implemented:** [Brief description]

**Requirements:** [Link to plan/spec or bullet points]

**Commits:** BASE_SHA..HEAD_SHA

**Summary:** [What changed, key decisions made]

**Specific concerns:** [Optional - areas you want extra scrutiny]
```

## Integration with Workflows

**With executing-plans:**
- Review after each batch (3 tasks)
- Get feedback, apply, continue

**With TDD:**
- Review includes test coverage check
- Verify RED-GREEN-REFACTOR was followed

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue without technical reasoning

**If reviewer wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification
