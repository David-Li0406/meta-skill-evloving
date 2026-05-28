---
name: requesting-code-review
description: Use this skill when completing tasks, implementing major features, or before merging to verify work meets requirements by dispatching a code-reviewer subagent to review implementation against the plan or requirements.
---

# Requesting Code Review

Dispatch a code-reviewer subagent to catch issues before they cascade.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing any feature (any size, any language/framework)
- After any bug fix (any severity, any language/framework)
- After any refactoring (any scope, any language/framework)
- Before merging to main
- Before creating a pull request
- Before claiming work complete
- For all code changes, especially those affecting critical paths (auth, payment, data handling)

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bugs

## How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code-reviewer subagent:**

Use the Task tool with code-reviewer type, filling the template at `code-reviewer.md`.

**Placeholders:**
- `{WHAT_WAS_IMPLEMENTED}` - What you just built
- `{PLAN_OR_REQUIREMENTS}` - What it should do
- `{BASE_SHA}` - Starting commit
- `{HEAD_SHA}` - Ending commit
- `{DESCRIPTION}` - Brief summary

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Review Process

The review process is iterative: review → fix → re-review until zero issues are found or issues are accepted per your workflow's policy.

## Integration with Workflows

**Subagent-Driven Development:**
- Review after EACH task
- Catch issues before they compound
- Fix before moving to the next task

**Executing Plans:**
- Review after each batch (3 tasks)
- Get feedback, apply, continue

**Ad-Hoc Development:**
- Review before merge
- Review when stuck

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore critical feedback

## Pushing Back on Reviews

If the reviewer is wrong:
- Push back with technical reasoning
- Show code/tests that prove it works
- Reference plan requirements
- Request clarification

## Exceptions to Mandatory Review

1. **Pure documentation**: Changes only to `.md` files in the docs directory.
2. **Configuration-only**: Dependency updates in configuration files with no logic changes.
3. **Emergency hotfix**: Must be reviewed within 24 hours after deployment.

When in doubt, request a code review. There are only three exceptions; no others.