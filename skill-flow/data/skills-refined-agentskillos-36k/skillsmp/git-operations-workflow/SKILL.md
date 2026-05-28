---
name: Git Operations & Workflow
description: Standard git workflow for committing, branching, and pushing changes
version: 1.0.0
triggers:
  - Committing code changes
  - Creating feature branches
  - Pushing to remote repository
  - Checking git status
  - Reviewing uncommitted changes
---

## Context

This repository uses Git for version control with a main branch deployment strategy. Changes are committed locally, pushed to GitHub, and automatically deployed via GitHub Actions.

**Repository**: oviney/blog  
**Main Branch**: `main`  
**Remote**: https://github.com/oviney/blog

**Commit Convention**: Use conventional commit format:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - CSS/design changes
- `refactor:` - Code restructuring
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks

## Step-by-Step Instructions

### 1. Check Status Before Committing

```bash
cd /Users/ouray.viney/code/economist-blog-v5
git status
```

**Review**:
- Red files = unstaged (not added)
- Green files = staged (ready to commit)
- Untracked files = new files not in git

### 2. Review Changes

```bash
# View all changes
git diff

# View staged changes only
git diff --cached

# View specific file changes
git diff path/to/file
```

### 3. Stage Files

```bash
# Stage specific files
git add path/to/file1 path/to/file2

# Stage all changes in directory
git add docs/skills/

# Stage all changes
git add .
```

### 4. Commit Changes

```bash
# Standard commit
git commit -m "feat: add Claude Skills persistence architecture"

# Multi-line commit with description
git commit -m "feat: implement defect tracking dashboard" -m "- Created GitHub Projects board
- Added bug issue template
- Set up labels for priority and components"
```

**Commit Message Best Practices**:
- Start with conventional commit prefix
- Use imperative mood ("add" not "added")
- Keep first line under 72 characters
- Add detailed description in second message if needed

### 5. Push to Remote

```bash
# Push to main branch
git push origin main

# Push new branch
git push -u origin feature-branch-name
```

### 6. Verify Push

- Check GitHub Actions: https://github.com/oviney/blog/actions
- Wait for deployment (~1-2 minutes)
- Verify on production: https://www.viney.ca/

## Common Pitfalls

### Pitfall 1: Committing Without Reviewing Changes
**Problem**: Accidentally commit unwanted files or sensitive data  
**Solution**: Always run `git status` and `git diff` before committing  
**Prevention**: Use `git add` for specific files, not `git add .` blindly

### Pitfall 2: Vague Commit Messages
**Problem**: Messages like "fix stuff" or "updates" that don't explain what changed  
**Solution**: Write clear, descriptive messages following conventional commit format  
**Example**: "feat: add priority labels to bug tracker" instead of "updates"

### Pitfall 3: Forgetting to Pull Before Push
**Problem**: Push rejected because remote has changes you don't have  
**Solution**: Pull first if working with others: `git pull origin main`  
**Note**: For solo projects, this is less common

### Pitfall 4: Pushing Directly to Main Without Testing
**Problem**: Broken code deployed to production  
**Solution**: Pre-commit hook validates builds locally before commit  
**Reminder**: Never use `--no-verify` to bypass checks

### Pitfall 5: Large Binary Files
**Problem**: Accidentally committing large images, videos, or generated files  
**Solution**: Check file sizes before committing. Use [`.gitignore`](../../.gitignore) for build artifacts  
**Example**: Don't commit `_site/`, `node_modules/`, `.DS_Store`

## Code Snippets/Patterns

### Standard Commit Workflow

```bash
cd /Users/ouray.viney/code/economist-blog-v5

# Check what changed
git status
git diff

# Stage specific changes
git add docs/skills/ docs/AI_CODING_GUIDELINES.md

# Commit with descriptive message
git commit -m "feat: implement Claude Skills persistence architecture"

# Push to remote
git push origin main
```

**When to use**: Every code change

### Feature Branch Workflow

```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: implement new feature"

# Push branch to remote
git push -u origin feature/new-feature

# Create PR on GitHub, then merge
```

**When to use**: Large features that need review before merging

### Undo Last Commit (Before Push)

```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes and commit
git reset --hard HEAD~1
```

**When to use**: Made a mistake in last commit, haven't pushed yet

### Check Commit History

```bash
# View recent commits
git log --oneline -10

# View commits with file changes
git log --stat

# View specific file history
git log --follow path/to/file
```

**When to use**: Review what was changed and when

### Stash Changes Temporarily

```bash
# Save uncommitted changes
git stash

# Apply stashed changes
git stash pop

# List all stashes
git stash list
```

**When to use**: Need to switch context without committing

## Related Files

- [`.gitignore`](../../.gitignore) - Files excluded from git
- [`.git/hooks/pre-commit`](../../.git/hooks/pre-commit) - Pre-commit validation script
- [`docs/DEVELOPMENT_WORKFLOW.md`](../DEVELOPMENT_WORKFLOW.md) - Full development workflow
- [`.github/workflows/jekyll.yml`](../../.github/workflows/jekyll.yml) - CI/CD pipeline

## Success Criteria

- [ ] Changes reviewed with `git status` and `git diff`
- [ ] Only relevant files staged
- [ ] Commit message follows conventional format
- [ ] Pre-commit hook passed (if applicable)
- [ ] Push successful
- [ ] GitHub Actions build passed
- [ ] Changes visible on production (if applicable)

## Version History

- **1.0.0** (2026-01-05): Initial git operations skill creation
