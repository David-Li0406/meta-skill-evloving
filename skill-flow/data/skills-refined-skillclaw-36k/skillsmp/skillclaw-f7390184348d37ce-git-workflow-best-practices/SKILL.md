---
name: git-workflow-best-practices
description: Use this skill when managing Git workflows, including commits, branches, merges, and collaboration.
---

# Git Workflow Best Practices

This skill provides comprehensive guidelines for effective Git operations, ensuring clean commit history, effective collaboration, and maintainable version control in your projects.

## When to Use This Skill
- Creating meaningful commit messages
- Managing branches
- Merging code
- Resolving conflicts
- Collaborating with team members

## Branch Management

### Create Feature Branch
```bash
# Create and switch to new branch
git checkout -b feature/feature-name

# Or create from specific commit
git checkout -b feature/feature-name <commit-hash>
```

### Naming Conventions
- `feature/description`: New features
- `bugfix/description`: Bug fixes
- `hotfix/description`: Urgent fixes
- `refactor/description`: Code refactoring
- `docs/description`: Documentation updates

## Making Changes

### Stage Changes
```bash
# Stage specific files
git add file1.py file2.js

# Stage all changes
git add .

# Stage with patch mode (interactive)
git add -p
```

### Check Status
```bash
# See what's changed
git status

# See detailed diff
git diff

# See staged diff
git diff --staged
```

## Committing Changes

### Write Good Commit Messages
Follow the Conventional Commits format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Commit Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting, no code change
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

**Example:**
```bash
git commit -m "feat(auth): add JWT authentication

- Implement JWT token generation
- Add token validation middleware
- Update user model with refresh token

Closes #42"
```

## Pushing Changes
```bash
# Push to remote
git push origin feature/feature-name

# Force push (use with caution!)
git push origin feature/feature-name --force-with-lease

# Set upstream and push
git push -u origin feature/feature-name
```

## Pulling and Updating
```bash
# Pull latest changes
git pull origin main

# Pull with rebase (cleaner history)
git pull --rebase origin main

# Fetch without merging
git fetch origin
```

## Merging
### Merge Feature Branch
```bash
# Switch to main branch
git checkout main

# Merge feature
git merge feature/feature-name

# Merge with no fast-forward (create a merge commit)
git merge --no-ff feature/feature-name
```

## Conflict Resolution
**Always delegate to the appropriate agent for resolving merge or rebase conflicts.**

## Additional Best Practices
- **Use imperative mood** in subject line: "Add feature" not "Added feature"
- **Keep subject line under 50 characters**
- **Capitalize subject line**
- **No period at end of subject line**
- **Separate subject from body with a blank line**
- **Wrap body at 72 characters**
- **Explain what and why, not how**
- **Reference issues/tickets in footer**