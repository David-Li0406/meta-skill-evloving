---
name: git-workflow
description: Use this skill when managing Git branches, creating commits, resolving conflicts, or following team conventions.
---

# Git Workflow

This skill provides best practices for Git version control, including branching strategies, commit conventions, and conflict resolution.

## Core Principles

1. **Atomic commits** - One logical change per commit.
2. **Clear history** - Meaningful commit messages that explain why.
3. **Branch hygiene** - Keep branches focused and short-lived.
4. **Safe operations** - Understand destructive commands before using.
5. **Collaboration-friendly** - Follow team conventions consistently.

## Branch Naming Convention

- `feature/xxx` - New features
- `bugfix/xxx` - Bug fixes
- `hotfix/xxx` - Urgent production fixes
- `release/xxx` - Release preparation

## Commit Message Format

```
<type>(<scope>): <subject>

<body>
```

### Types

| Type     | Description  | Example                         |
|----------|--------------|---------------------------------|
| feat     | New feature  | feat(auth): Add OAuth login     |
| fix      | Bug fix      | fix(cart): Fix price calculation |
| docs     | Documentation | docs(readme): Update installation instructions |
| style    | Formatting   | style: Format code              |
| refactor | Refactoring  | refactor(api): Refactor user service |
| perf     | Performance  | perf(query): Optimize search query |
| test     | Testing      | test(user): Add user registration test |
| chore    | Build/tooling| chore(deps): Update dependencies |
| ci       | CI configuration | ci: Add GitHub Actions      |

## Workflow Steps

1. Create a branch from `main`.
2. Make changes and commit.
3. Push and create a Pull Request (PR).
4. Conduct code review.
5. Merge to `main`.

## Quick Summary

### Before Starting Work

- Pull the latest from `main`.
- Create an appropriately named branch.
- Understand the task scope.

### During Work

- Commit frequently with clear messages.
- Keep changes focused on one concern.
- Rebase on `main` periodically for long branches.

### Before PR

- Rebase on the latest `main`.
- Squash fixup commits.
- Run tests and linting.
- Write a clear PR description.

## Useful Git Commands

### Branch Operations

```bash
# Create and switch to a new branch
git checkout -b feature/new-feature

# Delete a local branch
git branch -d feature/xxx

# Push a branch to remote
git push origin feature/xxx
```

### Commit Operations

```bash
# Stage specific files
git add src/user.ts src/auth.ts

# Amend the last commit
git commit --amend
```

### Sync Operations

```bash
# Pull and rebase
git pull --rebase origin main

# Push changes
git push origin feature/xxx
```

### Conflict Resolution Steps

1. Pull the latest code.
2. Merge or rebase.
3. Resolve conflicts in the affected files.
4. Mark files as resolved and continue.

## Pull Request Process

### Creating a PR

```bash
# Push the branch
git push -u origin feature/xxx

# Create PR using GitHub CLI
gh pr create --title "feat: Add user feature" --body "## Changes\n- Added user registration\n- Added user login"
```

### PR Template

```markdown
## Change Type

- [ ] New feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Documentation update

## Description

[Describe the changes made]

## Related Issue

Closes #xxx

## Testing

- [ ] Added new tests
- [ ] All tests passed
- [ ] Local validation passed
```

## Best Practices

1. **Small, frequent commits** - Each commit should do one thing.
2. **Meaningful commit messages** - Explain why changes were made.
3. **Keep branches updated** - Regularly sync with the main branch.
4. **Pre-PR self-check** - Lint, test, and review your code.
5. **Avoid committing sensitive information** - Use environment variables.
6. **Use `.gitignore`** - Ignore unnecessary files.
7. **Regularly clean up branches** - Delete merged branches.
8. **Backup important operations** - Create backup branches before rebasing.
9. **Follow team conventions** - Maintain consistent branch and commit standards.
10. **Utilize Git Hooks** - Automate checks before commits.