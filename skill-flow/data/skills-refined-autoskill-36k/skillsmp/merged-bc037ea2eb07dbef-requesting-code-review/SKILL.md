---
name: requesting-code-review
description: Use this skill when completing tasks, implementing major features, or before merging to verify work meets requirements by dispatching a code-review subagent to review implementation against plan or requirements.
---

# Requesting Code Review

Dispatch a code-review subagent to catch issues before they cascade.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing any feature or bug fix
- Before merging to main or creating a pull request
- For all code changes, including refactoring and configuration changes with logic
- For changes to critical paths (e.g., authentication, payment, data handling)

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bugs

## How to Request Review

### Step 1: Prepare for Review

Before requesting review, ensure:
- All tests are passing
- No errors or warnings
- Code follows Test-Driven Development (TDD)
- Requirements are met
- Evidence of verification is captured

### Step 2: Provide Context

When requesting review, include:

```markdown
I need code review for [feature/bugfix/refactor name].

**Context:**
- Completed tasks: [list]
- Requirements met: [reference to plan/spec]
- Tests added: [count] tests, all passing
- TDD followed: [Yes/No with attestation]

**Files for review:**
- src/[file].ts (modified - [what changed])
- src/[file].ts (new - [what it does])
- tests/[file].test.ts (modified - [tests added])

**Testing evidence:**
```
[paste test output showing all passing]
```

**Ready for review.**
```

### Step 3: Get Git SHAs

```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

### Step 4: Dispatch Code-Review Subagent

Use the Task tool with the `code-review` subagent type, providing:
- What was implemented (feature/task description)
- Plan or requirements it should meet (file path or description)
- Git range to review (BASE_SHA..HEAD_SHA)
- Any specific concerns to focus on

### Step 5: Act on Feedback

- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

## Review Outcomes

**Status: Approved**
- All issues resolved or no issues found. You may proceed to the next step.

**Status: Approved with minor items**
- No Critical or Important issues. Minor suggestions noted for future work. You may proceed, but address minor items when practical.

**Status: Needs revision**
- Critical or Important issues found. Action required:
  1. Stop - Do not proceed
  2. Fix all Critical issues (MUST be 0)
  3. Fix all Important issues OR convert to tracked issue with ID
  4. Re-run tests
  5. Provide evidence of fixes
  6. Request follow-up review if needed
  7. Only proceed after approval

**Status: Blocked**
- Fundamental issues requiring rework. Action required:
  1. Stop - Do not proceed
  2. Discuss issues with reviewer or human partner
  3. May require significant rework or redesign

## Common Mistakes

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue without technical justification

**Always:**
- Provide full context in review request
- Fix Critical issues immediately
- Document disagreements with technical justification
- Re-review after fixing Critical issues

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

## Red Flags - STOP IMMEDIATELY

If you catch yourself:
- Thinking "I'll skip review this time"
- Proceeding to the next batch without reviewing the current batch
- Marking work complete without code review

THEN:
- Stop immediately
- Request code review
- Wait for approval

**If reviewer is wrong:**
- Push back with technical reasoning
- Show code/tests that prove it works
- Request clarification

See the `code-review` skill for detailed review framework and output format.