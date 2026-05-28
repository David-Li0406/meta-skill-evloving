---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# Code Review

Perform systematic code review to catch issues before they cascade.

**Core principle:** Review early, review often.

## When to Review

**Mandatory:**
- After completing major feature
- Before merge to main
- Before creating pull request

**Optional but valuable:**
- After each significant task in multi-task development
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Perform Review

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Review the changes:**

```bash
# See what files changed
git diff --stat $BASE_SHA..$HEAD_SHA

# Review the actual changes
git diff $BASE_SHA..$HEAD_SHA
```

**3. Check against requirements:**
- Read the plan/requirements that guided this work
- Compare implementation against spec
- Verify all requirements are met

**4. Evaluate code quality:**

**Code Quality:**
- Clean separation of concerns?
- Proper error handling?
- Type safety (if applicable)?
- DRY principle followed?
- Edge cases handled?

**Architecture:**
- Sound design decisions?
- Scalability considerations?
- Performance implications?
- Security concerns?

**Testing:**
- Tests actually test logic (not mocks)?
- Edge cases covered?
- Integration tests where needed?
- All tests passing?

**Production Readiness:**
- Migration strategy (if schema changes)?
- Backward compatibility considered?
- Documentation complete?
- No obvious bugs?

**5. Categorize issues found:**

**Critical (Must Fix):**
- Bugs, security issues, data loss risks, broken functionality

**Important (Should Fix):**
- Architecture problems, missing features, poor error handling, test gaps

**Minor (Nice to Have):**
- Code style, optimization opportunities, documentation improvements

**6. Fix issues:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later

## Review Output Format

Document your review findings:

### Strengths
[What's well done? Be specific with file:line references.]

### Issues

#### Critical (Must Fix)
[List with file:line, what's wrong, why it matters, how to fix]

#### Important (Should Fix)
[List with file:line, what's wrong, why it matters, how to fix]

#### Minor (Nice to Have)
[List with file:line, what's wrong, why it matters]

### Assessment
- Ready to merge? [Yes/No/With fixes]
- Reasoning: [1-2 sentence technical assessment]

## Integration with Workflows

**Executing Plans:**
- Review after each batch (3 tasks)
- Fix issues before continuing

**Ad-Hoc Development:**
- Review before merge
- Review before PR creation

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Say "looks good" without actually checking

**Always:**
- Be specific (file:line references)
- Explain WHY issues matter
- Give clear verdict (ready/not ready)
- Categorize by actual severity
