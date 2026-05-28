---
name: pull-request-review
description: Reviews pull requests by comparing changes to previous versions, assessing code quality, effectiveness, and merge readiness. Use when reviewing pull requests, examining code changes before merge, or when the user asks for PR review or code review of pending changes.
---

# Pull Request Review

## Overview

This skill guides systematic review of pull requests by:
1. Comparing changes against the previous version (base branch)
2. Assessing the effectiveness and quality of changes
3. Evaluating merge readiness
4. Providing structured, actionable feedback

## Review Process

### Step 1: Understand the Context

Before reviewing, gather context:

1. **Identify the changes**:
   - Use `git diff` to see what files changed
   - Check `git log` to understand commit history
   - Review the PR description/commit messages for intent

2. **Understand the scope**:
   - What problem is this PR solving?
   - What files are affected?
   - Are there related changes in other PRs?

3. **Check the base branch**:
   - What branch is this merging into? (usually `main` or `master`)
   - What was the state before these changes?

### Step 2: Compare Changes

Use git tools to compare:

```bash
# See all changes in the PR
git diff main...feature-branch

# See changes in specific files
git diff main...feature-branch -- path/to/file

# See file list that changed
git diff --name-status main...feature-branch

# See commit history
git log main..feature-branch
```

**What to look for:**
- What was added, removed, or modified?
- Are the changes focused and cohesive?
- Do changes align with the stated purpose?

### Step 3: Assess Code Quality

Review each changed file for:

#### Correctness
- [ ] Logic is sound and handles edge cases
- [ ] No obvious bugs or errors
- [ ] Error handling is appropriate
- [ ] Edge cases are considered

#### Code Quality
- [ ] Code follows project conventions and style
- [ ] Functions/classes are appropriately sized
- [ ] Naming is clear and descriptive
- [ ] No code duplication (DRY principle)
- [ ] Comments explain "why" not "what"

#### Security
- [ ] No security vulnerabilities introduced
- [ ] Input validation where needed
- [ ] Sensitive data is handled properly
- [ ] Authentication/authorization checks are present

#### Performance
- [ ] No obvious performance regressions
- [ ] Efficient algorithms/data structures used
- [ ] Unnecessary operations avoided

### Step 4: Assess Effectiveness

Evaluate whether the changes achieve their goals:

1. **Does it solve the stated problem?**
   - Review the PR description/issue
   - Verify the solution addresses the root cause
   - Check if it introduces new problems

2. **Is the implementation appropriate?**
   - Is the approach reasonable for the problem size?
   - Could it be simpler?
   - Does it align with project architecture?

3. **Are there unintended side effects?**
   - Does it break existing functionality?
   - Are there breaking changes that need documentation?
   - Does it affect other parts of the system?

### Step 5: Check Testing

- [ ] Are there tests for new functionality?
- [ ] Do existing tests still pass?
- [ ] Are edge cases covered by tests?
- [ ] Is test coverage adequate?

### Step 6: Documentation & Communication

- [ ] PR description clearly explains the changes
- [ ] Code comments explain complex logic
- [ ] README/docs updated if needed
- [ ] Breaking changes are documented

## Review Feedback Format

Structure feedback using this format:

### Summary
Brief overview of the PR and overall assessment.

### What Works Well
- Positive aspects of the changes
- Good patterns or solutions used

### Critical Issues (Must Fix)
Issues that must be addressed before merging:
- 🔴 **Critical**: [Description] - [Why it matters] - [How to fix]

### Suggestions (Consider Improving)
Improvements that would enhance the code:
- 🟡 **Suggestion**: [Description] - [Why it helps] - [How to improve]

### Questions
Clarifications needed:
- ❓ **Question**: [What needs clarification]

### Effectiveness Assessment
- Does this solve the problem effectively?
- Are there better approaches?
- Any concerns about maintainability?

## Example Review Workflow

```bash
# 1. Checkout the PR branch (or fetch it)
git fetch origin feature-branch
git checkout feature-branch

# 2. Compare with main branch
git diff main...feature-branch

# 3. Review specific files
git diff main...feature-branch -- src/components/Game.tsx

# 4. Run tests
npm test

# 5. Check for linting issues
npm run lint
```

## Common Review Scenarios

### New Feature PR
- Verify feature works as described
- Check integration with existing code
- Ensure no regressions
- Verify tests and documentation

### Bug Fix PR
- Confirm the bug is actually fixed
- Check if fix addresses root cause
- Verify no similar bugs elsewhere
- Ensure fix doesn't introduce new issues

### Refactoring PR
- Verify behavior is unchanged
- Check that tests still pass
- Assess if refactoring improves code quality
- Ensure no performance regressions

### Performance PR
- Verify performance improvement
- Check for correctness maintained
- Review if optimization is appropriate
- Consider readability trade-offs

## Red Flags to Watch For

- Large PRs that should be split
- Changes unrelated to PR description
- Missing tests for critical functionality
- Security vulnerabilities
- Breaking changes without migration plan
- Code that's hard to understand
- Performance regressions
- Incomplete implementations

## Approval Criteria

A PR is ready to merge when:
- ✅ All critical issues are resolved
- ✅ Code quality meets project standards
- ✅ Tests pass and coverage is adequate
- ✅ Changes are effective and solve the problem
- ✅ Documentation is updated as needed
- ✅ No security or performance concerns
- ✅ Code is maintainable and readable

## Best Practices

1. **Be constructive**: Focus on improving code, not criticizing
2. **Be specific**: Point to exact lines/files and explain why
3. **Prioritize**: Distinguish must-fix from nice-to-have
4. **Ask questions**: If something is unclear, ask rather than assume
5. **Acknowledge good work**: Recognize well-written code
6. **Consider context**: Understand constraints and trade-offs made
