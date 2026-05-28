---
name: git-workflow
description: Use this skill for standardized Git practices, including branching strategies, commit guidelines, and collaboration techniques.
---

# Git Workflow

## Overview
This skill provides best practices for Git version control, ensuring consistent workflows, effective collaboration, and clean project history.

## Commit Guidelines
- Write clear, descriptive commit messages following the conventional commit format (feat, fix, docs, etc.).
- Keep commits atomic and focused, referencing issue numbers when applicable.

## Branching Strategy
- Use feature branches for new work and keep the main branch stable.
- Employ isolated worktrees for complex features or PR reviews to maintain a clean workspace.
- Delete branches after merging to keep the repository tidy.

### Branch Setup

#### Standard Branching
For quick, single-task fixes:
```bash
git checkout main && git pull origin main
git checkout -b feature/{feature-name}
```

#### Isolated Worktree (RECOMMENDED)
For complex features or PR reviews:
```bash
./scripts/worktree-feature.sh {feature-name}
cd ../.worktrees/feature-{feature-name}
```

## Branch Lifecycle Closure

### Merging Work
#### Work Merged via PR (Recommended)
If the PR was merged via GitHub:
```bash
git checkout main
git pull origin main
git branch -d feature/{name}      # Delete local
```

#### Local-Only Work (Direct Merge)
For small tasks that don't need a PR:
```bash
git checkout main
git merge feature/{name} --no-ff -m "merge: {feature}"
git branch -d feature/{name}      # Delete local
git push origin main
```

#### Abandon Work
To delete a feature branch:
```bash
git checkout main
git branch -D feature/{name}      # Force delete local
git push origin --delete feature/{name}  # Delete remote (if exists)
```

## Collaboration
- Pull frequently to stay updated and resolve conflicts carefully.
- Review diffs before committing and use pull requests for code review.

## Advanced Git Techniques

### Essential Commands
```bash
# Initialize repository
git init
git clone https://github.com/user/repo.git

# Check status and differences
git status
git diff                    # Unstaged changes
git diff --staged           # Staged changes

# Stage and commit
git add file.txt            # Stage specific file
git commit -m "message"
```

### Merging and Rebasing
```bash
# Merge
git merge feature-branch
git rebase main              # Rebase current branch onto main
```

### Conflict Resolution
Handle merge conflicts by resolving them manually or using a merge tool:
```bash
git mergetool
```

## Best Practices
1. **Commit Often**: Small, atomic commits are easier to manage.
2. **Write Clear Messages**: Follow conventional commit format.
3. **Keep History Clean**: Use rebase for feature branches.
4. **Never Rewrite Public History**: Avoid force pushing to shared branches.
5. **Review Before Pushing**: Check diff and status.

## Common Workflows

### Fixing Mistakes
To undo the last commit (not pushed):
```bash
git reset --soft HEAD~1  # Keep changes staged
```

### Cleaning Repository
Remove untracked files:
```bash
git clean -fd
```

## Conclusion
Always use Git workflows that match your team's conventions and maintain a clean, understandable project history.