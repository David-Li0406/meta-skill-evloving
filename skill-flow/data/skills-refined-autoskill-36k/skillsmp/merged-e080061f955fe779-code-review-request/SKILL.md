---
name: code-review-request
description: Use this skill when completing tasks, implementing major features, or validating work before merging to ensure quality and compliance with requirements.
---

# Request Code Review

Assign a code-reviewer sub-agent to capture issues before they cascade.

**Core Principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task driven by the sub-agent
- After completing major features
- Before merging into the main branch

**Optional but Valuable:**
- When stuck (for a fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bugs

## How to Request

**1. Get Git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Assign the Code Reviewer Sub-Agent:**

Use the Task tool to call the code-reviewer type, filling out the template in `code-reviewer.md`.

**Placeholders:**
- `{WHAT_WAS_IMPLEMENTED}` - What you just built
- `{PLAN_OR_REQUIREMENTS}` - What it should accomplish
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

[Assigning code-reviewer sub-agent]
  WHAT_WAS_IMPLEMENTED: Validation and repair functions for session indexing
  PLAN_OR_REQUIREMENTS: Task 2 in docs/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added theoretical basis for verifyIndex() and repairIndex(), including 4 types of issues

[Sub-agent returns]:
  Strengths: Clear architecture, valid arguments
  Issues:
    Important: Missing discussion on progress indicators
    Minor: Justification for reporting interval (100) unclear
  Assessment: Ready to proceed

You: [Add discussion on progress indicators]
[Continue to Task 3]
```

## Integration with Workflow

**Sub-Agent Driven Development:**
- Review after each task
- Capture issues before they compound
- Fix before moving to the next task

**Execution Plan:**
- Review after each batch (3 tasks)
- Gather feedback, apply, continue

**Ad-hoc Development:**
- Review before merging
- Review when stuck

## Warning Signals

**Never:**
- Skip reviews because "it's simple"
- Ignore **Critical** issues
- Proceed with unresolved **Important** issues
- Argue against valid technical feedback

**If the Reviewer is Wrong:**
- Rebut with technical reasoning
- Provide evidence/code/tests that support your position
- Request clarification

Refer to the template: `code-reviewer.md`