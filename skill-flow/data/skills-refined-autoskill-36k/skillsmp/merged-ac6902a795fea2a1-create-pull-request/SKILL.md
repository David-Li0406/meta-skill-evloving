---
name: create-pull-request
description: Use this skill to create well-structured and documented pull requests that are ready for review and merging.
---

# Create Pull Request Skill

Create well-structured and documented pull requests with comprehensive descriptions, proper linking, and review-ready formatting.

## When to Use

- Ready to submit code for review
- Need to create a pull request from the current branch
- Want consistent pull request formatting across the team

## How to Use

### 1. Verify Branch State

```bash
# Check current branch
git branch --show-current

# Ensure all changes are committed
git status

# View commits that will be included in the PR
git log main..HEAD --oneline
```

### 2. Review Changes

Before creating the pull request, understand what you're submitting:

```bash
# See all changes vs main branch
git diff main...HEAD

# List changed files
git diff main...HEAD --name-only
```

### 3. Push to Remote

```bash
# Push and set upstream
git push -u origin <feature-branch>
```

### 4. Generate Pull Request

```bash
gh pr create --title "<type>: <description>" --body "$(cat <<'EOF'
## Summary

Brief description of what this PR does and why.

## Changes

- List key files/components changed
- Explain non-obvious implementation decisions

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots

(If applicable)

## Related Issues

Closes #[issue-number]
EOF
)"
```

## PR Description Template

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

## Best Practices

1. **Small PRs** - easier to review, faster to merge
2. **One concern per PR** - don't mix features with refactoring
3. **Descriptive title** - summarize the change in <72 chars
4. **Link issues** - use "Closes #123" for auto-linking
5. **Screenshots** - include for UI changes
6. **Test evidence** - show tests pass or describe manual testing

## Useful gh Commands

```bash
# Create PR with specific base branch
gh pr create --base <target-branch>

# Create draft PR
gh pr create --draft

# View PR status
gh pr view

# List open PRs
gh pr list

# Check PR checks status
gh pr checks
```