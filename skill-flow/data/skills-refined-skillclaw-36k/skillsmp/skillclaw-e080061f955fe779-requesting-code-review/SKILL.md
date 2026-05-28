---
name: requesting-code-review
description: Use this skill when you have completed a task, implemented a major feature, or need to verify that your work meets requirements before merging.
---

# Requesting Code Review

Assign a code-reviewer agent to catch issues before they cascade.

**Core Principle:** Review early, review often.

## When to Request a Review

**Mandatory:**
- After each task driven by the agent
- After completing a major feature
- Before merging into the main branch

**Optional but Valuable:**
- When stuck (to gain a fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bugs

## How to Request

**1. Get Git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Assign the Code Reviewer Agent:**

Use the Task tool to call the code-reviewer type, filling out the template in `code-reviewer.md`.

**Placeholders:**
- `{WHAT_WAS_IMPLEMENTED}` - What you just built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit
- `{DESCRIPTION}` - Brief summary

**3. Act on Feedback:**
- Immediately fix **Critical** issues
- Fix **Important** issues before proceeding
- Note **Minor** issues for later
- If the reviewer is wrong, provide a rebuttal (with reasoning)

## Example

```
[Just completed Task 2: Added validation function]

You: Let me request a code review before continuing.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Assigning code-reviewer agent]
  WHAT_WAS_IMPLEMENTED: Validation and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: Task 2 in docs/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added theoretical basis for verifyIndex() and repairIndex(), including 4 types of issues

[Agent returns]:
  Strengths: Clear architecture, valid tests
  Issues:
    Important: Missing discussion on progress indicators
    Minor: Unclear justification for reporting interval (100)
  Assessment: Ready to proceed

You: [Add discussion on progress indicators]
[Continue to Task 3]
```

## Integration with Workflow

**Agent-Driven Development:**
- Review after each task
- Catch issues before they compound
- Fix before moving to the next task

**Execution Plan:**
- Review after each batch (3 tasks)
- Get feedback, apply, continue

**Ad-hoc Development:**
- Review before merging
- Review when stuck

## Warning Signals

**Never:**
- Skip reviews because "it's simple"
- Ignore **Critical** issues
- Proceed without fixing **Important** issues
- Argue against valid technical feedback

**If the Reviewer is Wrong:**
- Rebut with technical reasoning
- Show evidence/code/tests that support your case
- Request clarification

Refer to the template: requesting-code-review/code-reviewer.md