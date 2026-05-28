---
name: pr-create
description: Create well-structured pull requests with proper descriptions
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: git
---

# PR Create

Create well-structured pull requests with comprehensive descriptions, proper linking, and review-ready formatting.

## When to Use

- Ready to submit code for review
- Need to create PR from current branch
- Want consistent PR formatting across team

## How to Use

```
Create a PR for this branch
```

```
Create PR targeting develop branch
```

```
Create draft PR with WIP changes
```

## Process

### 1. Gather Context

```bash
# Current branch and status
git status
git branch --show-current

# Commits to include
git log main..HEAD --oneline

# Full diff
git diff main...HEAD --stat
```

### 2. Analyze Changes

- Identify primary change type (feature, fix, refactor)
- List affected components/modules
- Note breaking changes
- Check for related issues

### 3. Generate PR

```bash
gh pr create --title "feat: add user authentication" --body "$(cat <<'EOF'
## Summary

Brief description of what this PR does and why.

## Changes

- Added JWT authentication middleware
- Created login/logout endpoints
- Updated user model with password hashing

## Testing

- [ ] Unit tests added
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots

(if applicable)

## Related Issues

Closes #123
EOF
)"
```

## PR Template

```markdown
## Summary

<!-- What does this PR do? Why is it needed? -->

## Type of Change

- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## Changes Made

<!-- List the main changes -->

- 
- 
- 

## Testing

<!-- How was this tested? -->

- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if needed)
- [ ] No new warnings introduced

## Screenshots

<!-- If applicable, add screenshots -->

## Related Issues

<!-- Link related issues: Closes #123, Fixes #456 -->

## Notes for Reviewers

<!-- Any specific areas to focus on? Context needed? -->
```

## Title Conventions

Format: `<type>: <description>`

| Type | Use For |
|------|---------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation only |
| style | Formatting, no code change |
| refactor | Code change, no feature/fix |
| perf | Performance improvement |
| test | Adding tests |
| chore | Maintenance, dependencies |

Examples:
- `feat: add dark mode toggle`
- `fix: resolve login timeout issue`
- `refactor: simplify auth middleware`

## Options

```bash
# Draft PR
gh pr create --draft

# Assign reviewers
gh pr create --reviewer @teammate

# Add labels
gh pr create --label "enhancement"

# Target specific branch
gh pr create --base develop

# Auto-merge when checks pass
gh pr merge --auto --squash
```

## Best Practices

1. **Small PRs** - easier to review, faster to merge
2. **One concern per PR** - don't mix features with refactoring
3. **Descriptive title** - summarize the change in <72 chars
4. **Link issues** - use "Closes #123" for auto-linking
5. **Screenshots** - include for UI changes
6. **Test evidence** - show tests pass or describe manual testing
