---
name: git-workflow
description: Use this skill when you need to implement effective Git workflows, including branching strategies, commit conventions, and collaboration best practices.
---

# Git Workflow Best Practices

You are an expert in Git version control, following industry best practices for commits, branching, and collaboration workflows.

## Core Principles

- Write clear, atomic commits that address single logical changes.
- Follow the Conventional Commits specification for all commit messages.
- Use feature branches to isolate changes and enable easier code review.
- Keep branches short-lived and regularly sync with the main branch.
- Never commit directly to the main/master branch.

## Commit Guidelines

### Conventional Commits Format

Use the following format for all commit messages:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

- `feat`: A new feature (correlates with MINOR in SemVer)
- `fix`: A bug fix (correlates with PATCH in SemVer)
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `build`: Changes that affect the build system or external dependencies
- `ci`: Changes to CI configuration files and scripts
- `chore`: Other changes that don't modify src or test files
- `revert`: Reverts a previous commit

### Commit Message Guidelines

- Use lowercase letters in the entire body of the commit message.
- Keep the commit message title under 60 characters.
- Use imperative mood: "Add feature" not "Added feature."
- Explain the *why* behind the change, not just *what* was changed.
- Reference related issues or tickets in the footer.

### Examples

```
feat(auth): add OAuth2 authentication support

Implement OAuth2 flow for Google and GitHub providers.
This allows users to sign in with their existing accounts.

Closes #123
```

```
fix(api): handle null response from external service

The external API sometimes returns null instead of an empty array.
Added null check to prevent TypeError in downstream processing.

Fixes #456
```

## Branching Strategy

### Branch Naming Conventions

Use descriptive, kebab-case branch names with prefixes:

- `feature/` - New features (e.g., `feature/user-authentication`)
- `bugfix/` - Bug fixes (e.g., `bugfix/login-redirect-loop`)
- `hotfix/` - Urgent production fixes (e.g., `hotfix/critical-bug`)

### Example Workflow

1. **Create a Feature Branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/user-auth
   ```

2. **Make Changes and Commit**
   ```bash
   git add .
   git commit -m "feat(auth): add login endpoint"
   ```

3. **Push and Create a Pull Request**
   ```bash
   git push origin feature/user-auth
   ```

4. **After PR Review, Rebase if Needed**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

5. **Squash Commits Before Merging (Optional)**
   ```bash
   git rebase -i HEAD~3
   ```

6. **Force Push After Rebase**
   ```bash
   git push origin feature/user-auth --force-with-lease
   ```

## Branch Lifecycle Closure

### Merging and Cleanup

- **Merge via Pull Request (Recommended)**
- **Delete Local Branch After Merging**
   ```bash
   git branch -d feature/{name}
   ```

- **Force Delete Local Branch if Abandoned**
   ```bash
   git branch -D feature/{name}
   ```

- **Cleanup Worktrees**
   ```bash
   git worktree remove ../.worktrees/{name}
   ```

## Instrumentation
```bash
./scripts/log-skill.sh "git-workflow" "workflow" "{calling_workflow_name}"
```