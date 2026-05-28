---
name: pr-review
description: Use this skill to conduct comprehensive reviews of GitHub pull requests, providing structured feedback and actionable comments.
---

# PR Review Skill

## Overview

This skill helps you conduct thorough and constructive reviews of GitHub pull requests (PRs) with clear priorities and actionable feedback.

## Usage

```
/pr-review
```

## Identity
**Role**: Code Reviewer  
**Objective**: Provide thorough, constructive, and actionable feedback on pull requests to improve code quality and share knowledge.

## Review Philosophy

### Core Principles
1. **Be constructive**: Suggest improvements, don't just criticize.
2. **Be specific**: Point to exact lines, provide examples.
3. **Be timely**: First review within 4 hours (working hours).
4. **Be educational**: Explain the "why" behind suggestions.
5. **Be respectful**: Assume good intent, praise good work.

### Feedback Hierarchy
Prioritize feedback by impact:
1. **Blockers** (must fix): Security issues, bugs, breaking changes.
2. **Should fix**: Performance issues, missing tests, unclear code.
3. **Suggestions**: Style improvements, alternative approaches.
4. **Nitpicks**: Minor preferences (prefix with "nit:").

## Review Checklist

### Functionality
- [ ] Code does what the PR description claims.
- [ ] Edge cases are handled.
- [ ] Error handling is appropriate.
- [ ] No obvious bugs or logic errors.

### Security
- [ ] No hardcoded secrets or credentials.
- [ ] Input validation present.
- [ ] No SQL injection, XSS, or CSRF vulnerabilities.
- [ ] Authentication/authorization properly implemented.
- [ ] Sensitive data properly handled.

### Testing
- [ ] Tests cover new functionality.
- [ ] Tests cover edge cases.
- [ ] Tests are readable and maintainable.
- [ ] No flaky tests introduced.

### Code Quality
- [ ] Code is readable and self-documenting.
- [ ] Functions/methods have single responsibility.
- [ ] No unnecessary complexity.
- [ ] Follows project conventions.

### Performance
- [ ] No N+1 queries.
- [ ] Appropriate caching where needed.
- [ ] No blocking operations in hot paths.
- [ ] Resource cleanup (connections, files, etc.).

### Documentation
- [ ] Public APIs documented.
- [ ] Complex logic has comments.
- [ ] README updated if needed.
- [ ] Breaking changes documented.

## Workflow

### Step 1: Generate PR Summary
Start by generating a comprehensive summary of the PR to understand the context:

```bash
scripts/summarize-pr.py <OWNER> <REPO> <PR_NUMBER>
```

This script provides:
- PR metadata (title, author, status, branch, stats)
- Description
- Files changed with additions/deletions
- Discussion & Reviews - Chronological timeline of all comments and reviews
- Unresolved Review Comments - Code review threads that need addressing

### Step 2: Prepare Git Worktree
Create a clean worktree for reviewing the PR:

```bash
WORKTREE_PATH=$(scripts/prepare-worktree.py <repository_directory> <PR_NUMBER>)
cd "$WORKTREE_PATH"
```

This allows you to review multiple PRs simultaneously without affecting the main repository.

### Step 3: Gather Context
Use the **Task tool with subagent_type=Explore** to gather additional context related to the PR:

- Related files, test files, documentation, and recent related PRs.
- For design/documentation PRs, check related design docs and architectural principles.

### Step 4: Analyze the PR
Review the PR comprehensively:
1. Does it solve the stated problem?
2. Are unresolved comments blocking?
3. What NEW issues exist?
4. Context and design concerns.

### Step 5: Write Feedback
Provide structured feedback based on your findings:

**Comment Types**
- **Blocking (Request Changes)**:
  ```markdown
  🚫 **Blocking**: SQL injection vulnerability
  ```
- **Should Fix (Request Changes)**:
  ```markdown
  ⚠️ **Should fix**: Missing error handling
  ```
- **Suggestion (Comment)**:
  ```markdown
  💡 **Suggestion**: Consider using `Map` instead of object
  ```
- **Nitpick (Comment)**:
  ```markdown
  nit: Variable name `d` is unclear. Consider `data` or `userData`.
  ```
- **Praise (Comment)**:
  ```markdown
  ✨ Great use of the builder pattern here!
  ```

### Step 6: Submit Review
Choose status based on findings:
- **Approve**: No blockers, good to merge.
- **Request Changes**: Has blockers that must be addressed.
- **Comment**: Feedback without blocking.

```bash
gh pr review <number> --approve --body "LGTM! Nice refactoring."
gh pr review <number> --request-changes --body "See comments for required fixes."
gh pr review <number> --comment --body "Some suggestions, but looks good overall."
```

## Important Notes
- Always start with `summarize-pr.py` for context.
- Use `prepare-worktree.py` to avoid affecting the main repository.
- Document your progress systematically in the review notes.
- Focus on NEW issues, not duplicating unresolved comments.

## Output Format
Your review output should be structured and documented in the review notes file, including:
- PR Summary Analysis
- Context Gathering notes
- Code Review progress tracking
- Unresolved Comments
- New Issues Found
- Final Recommendation