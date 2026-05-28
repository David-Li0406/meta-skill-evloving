---
name: git-workflow
description: Use this skill when managing Git repositories, creating branches, handling merges, and following best practices for version control.
---

# Git Workflow Skill

This skill provides comprehensive guidance on Git workflows, branching strategies, commit conventions, and conflict resolution.

## Core Principles

1. **Atomic Commits**: One logical change per commit.
2. **Clear History**: Use meaningful commit messages that explain the "why" behind changes.
3. **Branch Hygiene**: Keep branches focused and short-lived.
4. **Safe Operations**: Understand destructive commands before using them.
5. **Collaboration-Friendly**: Follow team conventions consistently.

## When to Use This Skill

- Setting up branching strategies.
- Writing commit messages.
- Handling merges and conflicts.
- Managing releases.
- Code review workflows.
- Maintaining a clean history.

## Branching Strategies

### Git Flow

```
main (production)
  │
  └── develop (development)
        │
        ├── feature/xxx (feature branch)
        ├── release/x.x (release branch)
        └── hotfix/xxx (hotfix branch)
```

### GitHub Flow

```
main (always deployable)
  │
  └── feature/xxx (feature branch)
        │
        └── PR → Code Review → Merge
```

### Trunk-Based Development

```
main ─────●──●──●──●──●──●──●──●──●──●────▶
           │  │  │  │  │  │  │  │  │  │
          ●   ●  ●  ●  ●  ●  ●  ●  ●  ●
          Small, frequent commits (often direct to main)
```

## Commit Message Conventions

### Conventional Commits Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type     | Description      | Example                          |
|----------|------------------|----------------------------------|
| feat     | New feature      | feat(auth): add OAuth2 login     |
| fix      | Bug fix          | fix(api): handle null response    |
| docs     | Documentation    | docs(readme): update installation instructions |
| style    | Formatting       | style: format code                |
| refactor | Refactoring      | refactor(api): restructure user service |
| perf     | Performance      | perf(query): optimize search query |
| test     | Testing          | test(user): add user registration test |
| chore    | Maintenance      | chore(deps): update dependencies   |
| ci       | CI configuration | ci: add GitHub Actions            |

## Workflow Checklist

**Before Starting Work:**

- [ ] Pull latest from main.
- [ ] Create appropriately named branch.
- [ ] Understand the task scope.

**During Work:**

- [ ] Commit frequently with clear messages.
- [ ] Keep changes focused on one concern.
- [ ] Rebase on main periodically for long branches.

**Before PR:**

- [ ] Rebase on latest main.
- [ ] Squash fixup commits.
- [ ] Run tests and linting.
- [ ] Write clear PR description.

## Conflict Resolution

### During Merge Conflict

```bash
git status  # See conflicted files
# Edit conflicted files, then:
git add <resolved-file>
git commit
# Abort merge if necessary
git merge --abort
```

## Useful Git Commands

### Branch Management

```bash
# Create and switch to a new branch
git checkout -b feature/new-feature

# Delete a branch
git branch -d feature-branch  # Safe delete
git branch -D feature-branch  # Force delete
```

### Commit Management

```bash
# Amend last commit
git commit --amend -m "New message"
```

### History and Search

```bash
# View commit history
git log --oneline --graph --all
```

## Safety Guidelines

1. **Never force push to main/master**.
2. Check if others are using the branch before force pushing.
3. Use `--force-with-lease` instead of `--force` when possible.
4. Communicate with the team first.