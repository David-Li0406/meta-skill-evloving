---
name: create-github-pull-request
description: Use this skill to create comprehensive and review-ready GitHub pull requests with proper validation and structure.
---

# Create GitHub Pull Request Skill

## Overview

This skill facilitates the creation of consistent, review-ready pull requests (PRs) on GitHub, ensuring all necessary metadata, quality checks, and security validations are in place.

## Usage

```
/create-github-pull-request
```

## Identity
**Role**: Pull Request Author  
**Objective**: Create well-structured GitHub pull requests that facilitate efficient code review and merge.

## Prerequisites Check

Before creating a PR, verify:
1. All changes are committed (no uncommitted changes).
2. **Remote uses SSH** (never HTTPS).
3. Branch is pushed to remote.
4. Branch is up-to-date with the base branch.
5. CI checks pass locally (if applicable).

```bash
# Run these checks
git status
git fetch origin
git log origin/main..HEAD --oneline

# CRITICAL: Verify SSH remote (not HTTPS)
git remote -v
# Must show: git@github.com:owner/repo.git
# NOT: https://github.com/owner/repo.git

# If HTTPS detected, convert to SSH:
git remote set-url origin git@github.com:OWNER/REPO.git
```

## PR Structure

### Title Format
```
<type>(<scope>): <short description>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

### Description Template

```markdown
## Summary
<!-- 1-3 bullet points describing WHAT changed -->
- 

## Motivation
<!-- WHY this change is needed -->
- 

## Changes
<!-- Technical details of HOW -->
- 

## Testing
<!-- How this was tested -->
- [ ] 

## Security & Quality
- [ ] No sensitive data exposed
- [ ] Input validation implemented
- [ ] Linting and type checking passed
- [ ] Build successful

## Related Issues
Closes #123
```

## Workflow Steps

1. **Repository Validation** - Check authentication and branch status.
2. **Change Analysis** - Analyze commits and file changes.
3. **Quality Validation** - Run project-specific quality checks.
4. **Security Scanning** - Check for sensitive data exposure.
5. **Issue Discovery** - Find and link related issues.
6. **PR Creation** - Generate and create pull request with proper metadata.

### Quality Validation Process

- Run lint, test, build, and type-check commands.
- Validate package.json changes.
- Check for security vulnerabilities.

### Security Validation

- Scan for sensitive files (.env, .key, .pem).
- Check for hardcoded secrets, passwords, tokens.
- Validate input sanitization in changed files.

### Pre-Creation Requirements

- Repository state validated and clean.
- All quality checks passed (lint, test, build).
- Security scan completed without issues.
- Related issues identified and linked.

### Failure Resolution Process

When quality checks fail:
1. Create a specific task list for failures.
2. Collaborate with specialized agents for resolution.
3. Fix issues systematically with validation after each fix.
4. Re-run quality checks until all pass.

### Best Practices

- **Quality-first**: All checks must pass before PR creation.
- **Security validation**: Comprehensive scanning for vulnerabilities.
- **Issue linking**: Connect PRs to related issues with auto-closing keywords.
- **Small, focused changes**: Easier to review and merge.

## Outputs

- A created pull request with standardized title and description.

## Related Skills

- `/git-committer-atomic` - Prepare atomic commits.
- `/git-commit-conventional` - Standardize commit messages.