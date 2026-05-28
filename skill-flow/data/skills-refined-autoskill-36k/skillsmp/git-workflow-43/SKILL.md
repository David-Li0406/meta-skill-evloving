---
name: git-workflow
description:
  Follow Git best practices for commits, branching, and collaboration. Use this skill when creating
  commits, managing branches, resolving merge conflicts, or establishing Git workflows for teams.
---

# Git Workflow Best Practices

This skill provides guidance for effective Git usage, commit conventions, and team collaboration
patterns.

## When This Skill Applies

- Writing commit messages
- Creating or managing branches
- Resolving merge conflicts
- Setting up team Git workflows
- Reviewing pull requests

## Commit Message Conventions

Follow the **Conventional Commits** specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type       | Description                                             |
| ---------- | ------------------------------------------------------- |
| `feat`     | New feature for users                                   |
| `fix`      | Bug fix for users                                       |
| `docs`     | Documentation only changes                              |
| `style`    | Formatting, missing semicolons, etc.                    |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf`     | Performance improvement                                 |
| `test`     | Adding or correcting tests                              |
| `build`    | Changes to build system or dependencies                 |
| `ci`       | Changes to CI configuration                             |
| `chore`    | Other changes that don't modify src or test files       |
| `revert`   | Reverts a previous commit                               |

### Examples

```
feat(auth): add OAuth2 login support

Implements Google and GitHub OAuth2 providers.
Users can now link social accounts to their profile.

Closes #123
```

```
fix(api): handle null response from payment gateway

The payment API occasionally returns null instead of
an error object. Added defensive check to prevent crash.
```

### Commit Message Rules

- Use imperative mood: "add feature" not "added feature"
- Keep subject line under 50 characters
- Capitalize the subject line
- Don't end subject with a period
- Separate subject from body with blank line
- Wrap body at 72 characters
- Explain what and why, not how

## Branching Strategies

### GitHub Flow (Recommended for most teams)

Simple and effective:

1. `main` is always deployable
2. Create feature branches from `main`
3. Open PR when ready for review
4. Merge to `main` after approval
5. Deploy from `main`

### Branch Naming

```
<type>/<ticket-id>-<short-description>
```

Examples:

- `feat/AUTH-123-oauth-login`
- `fix/BUG-456-null-pointer-crash`
- `refactor/TECH-789-extract-utils`

## Pull Request Best Practices

### Creating PRs

- Write a clear title summarizing the change
- Include context: what, why, and how to test
- Link related issues
- Keep PRs focused and reasonably sized (<400 lines ideal)
- Add screenshots for UI changes

### Reviewing PRs

- Review promptly (aim for <24 hours)
- Be constructive and specific
- Approve when "good enough"—don't block on style preferences
- Use suggestions for small changes

## Conflict Resolution

When resolving merge conflicts:

1. Understand both sides of the conflict
2. Communicate with the other author if unclear
3. Test the merged result
4. Don't blindly accept "ours" or "theirs"

## Git Hygiene

### Do

- Commit early and often (can squash later)
- Write meaningful commit messages
- Keep commits atomic (one logical change)
- Pull/rebase frequently to stay current
- Use `.gitignore` for generated files

### Don't

- Commit secrets, credentials, or API keys
- Force push to shared branches
- Commit large binary files
- Leave WIP commits in final PRs
- Commit broken code to main

## Useful Commands

```bash
# Interactive rebase to clean up commits
git rebase -i HEAD~5

# Amend the last commit
git commit --amend

# Stash changes temporarily
git stash push -m "description"

# Cherry-pick a specific commit
git cherry-pick <commit-hash>

# View commit history as graph
git log --oneline --graph --all
```
