---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements
---

# Requesting Code Review

Perform structured self-review to catch issues before they cascade.

**Core principle:** Review early, review often.

## When to Request Review

**Mandatory:**
- After completing major feature
- Before merge to main
- After significant refactoring

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to Perform Review

**1. Get git diff for review:**
```bash
# Compare against main/master
git diff main --stat
git diff main

# Or compare specific commits
git diff HEAD~3..HEAD --stat
git diff HEAD~3..HEAD
```

**2. Follow the review checklist below systematically**

**3. Document findings using the output format**

**4. Act on findings:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later

## Review Checklist

### Code Quality
- [ ] Clean separation of concerns?
- [ ] Proper error handling?
- [ ] Type safety (if applicable)?
- [ ] DRY principle followed?
- [ ] Edge cases handled?

### Architecture
- [ ] Sound design decisions?
- [ ] Scalability considerations?
- [ ] Performance implications?
- [ ] Security concerns addressed?

### Testing
- [ ] Tests actually test logic (not mocks)?
- [ ] Edge cases covered?
- [ ] Integration tests where needed?
- [ ] All tests passing?

### Requirements
- [ ] All plan requirements met?
- [ ] Implementation matches spec?
- [ ] No scope creep?
- [ ] Breaking changes documented?

### Production Readiness
- [ ] Migration strategy (if schema changes)?
- [ ] Backward compatibility considered?
- [ ] Documentation complete?
- [ ] No obvious bugs?

## Output Format

Document your review findings:

```markdown
## Code Review: [Feature/Task Name]

**Reviewed:** [date]
**Commits:** [base]...[head]

### Strengths
[What's well done? Be specific with file:line references]

### Issues

#### Critical (Must Fix)
[Bugs, security issues, data loss risks, broken functionality]

#### Important (Should Fix)
[Architecture problems, missing features, poor error handling, test gaps]

#### Minor (Nice to Have)
[Code style, optimization opportunities, documentation improvements]

### Assessment
**Ready to merge:** [Yes/No/With fixes]
**Reasoning:** [Technical assessment in 1-2 sentences]
```

**For each issue include:**
- File:line reference
- What's wrong
- Why it matters
- How to fix (if not obvious)

## Example

```
[Just completed: Add verification function]

You: Let me review my changes before proceeding.

$ git diff main --stat
 src/indexer.ts     | 45 +++++++++++++++
 src/verifier.ts    | 82 +++++++++++++++++++++++++
 tests/verifier.test.ts | 67 ++++++++++++++++++++
 3 files changed, 194 insertions(+)

[Review against checklist...]

## Code Review: Verification Functions

### Strengths
- Clean architecture with proper separation (verifier.ts)
- Good test coverage (67 lines, all edge cases)
- Proper error handling with fallbacks (verifier.ts:45-52)

### Issues

#### Important
1. **Missing progress indicators**
   - File: indexer.ts:130
   - Issue: No feedback during long operations
   - Fix: Add progress callback or logging

#### Minor
1. **Magic number**
   - File: verifier.ts:23
   - Issue: Hardcoded 100 for reporting interval
   - Fix: Extract to named constant

### Assessment
**Ready to merge:** With fixes
**Reasoning:** Core implementation solid. Progress indicator is important for UX.

[Fix progress indicators]
[Continue to next task]
```

## Integration with Workflows

**Executing Plans:**
- Review after each batch (3 tasks)
- Document findings, apply fixes, continue

**Ad-Hoc Development:**
- Review before merge
- Review when stuck

**Feature Development:**
- Review after each logical milestone
- Catch issues before they compound

## Red Flags

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Rush through checklist

**Quality indicators:**
- Every checklist item considered
- Specific file:line references
- Clear severity categorization
- Honest assessment
