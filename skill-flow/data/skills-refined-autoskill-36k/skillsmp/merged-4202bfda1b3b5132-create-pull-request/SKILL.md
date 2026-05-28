---
name: create-pull-request
description: Use this skill when creating pull requests, writing PR descriptions, or preparing code for review.
---

# Create Pull Request

This skill guides you through creating pull requests with proper format and templates.

## PR Title

Use the [Conventional Commit Format](https://www.conventionalcommits.org/), same as commit messages:

```text
<type>(<scope>): <description>
```

### Types

- `feat`: User-facing features or behavior changes (must change production code)
- `fix`: Bug fixes (must change production code)
- `docs`: Documentation only
- `style`: Code style/formatting (no logic changes)
- `refactor`: Code restructuring without behavior change
- `test`: Adding or updating tests
- `chore`: CI/CD, tooling, dependency bumps, configs (no production code)

## PR Description Template

```markdown
## Summary

One sentence describing the overall change.

- Optional supporting details
- If needed

## Test plan

- [ ] How to verify it works
```

### Linked Issues

- `Closes #<issue_number>` - Automatically closes issue when PR is merged
- `Fixes #<issue_number>` - Automatically closes bug issue when PR is merged
- `Resolves #<issue_number>` - Automatically closes issue when PR is merged

### Screenshots

- Required for UI changes (Before/After comparison)
- Include relevant terminal output for CLI changes

## Command

```bash
gh pr create \
  --title "<type>(<scope>): <description>" \
  --body "PR body" \
  --assignee "@me"
```

## Branch Naming

Use `type/short-description`:

```text
feat/infinite-scroll
fix/album-path-validation
chore/pre-commit-hooks
```

## Instructions

1. Run `git log main..HEAD` to see commits for this branch
2. Run `git diff main...HEAD` to see all changes
3. Summarize the changes in 1-2 sentences
4. Create a test plan with verification steps
5. Apply appropriate labels using `gh pr create --label <label>` or `gh pr edit --add-label <label>`.

### Labels

Apply all labels that fit. Use the following labels:

- `enhancement` - User-facing features or improvements (must change production code behavior)
- `refactor` - Production code changes that don't alter behavior
- `bug` - Fixes broken production code functionality
- `test` - Changes to tests
- `documentation` - Documentation changes

**No label needed** for dependency bumps, CI/CD, tooling, or infrastructure changes.

## After PR Creation

1. Wait for CI checks to complete
2. Review any automated feedback
3. Address review comments (with user approval)
4. Request merge approval from user
5. **NEVER merge without explicit user approval**