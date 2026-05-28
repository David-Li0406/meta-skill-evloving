---
name: managing-git
description: Knowledge and patterns for Git workflows with emphasis on trunk-based development for rapid iteration.
---

# Managing Git Skill

This skill provides patterns and best practices for Git workflows, with trunk-based development as the primary approach.

## Primary Workflow: Trunk-Based Development

This plugin emphasizes **trunk-based development** (TBD) where:
- All work commits directly to main
- Changes are small, atomic, and well-tested
- Feature flags manage incomplete features
- Continuous integration catches issues early

```
main ────●────●────●────●────●────▶
         │    │    │    │    │
         Small, tested commits
```

### Why Trunk-Based?

1. **Faster iteration** - No PR review bottleneck for solo/small teams
2. **Simpler workflow** - One branch, fewer merge conflicts
3. **Continuous integration** - Issues caught immediately
4. **Ship faster** - Deploy any commit, use feature flags

### Safeguards for Main-Branch Development

- Run tests before every push
- Use `/ai-dev:commit-push` for quality gates
- Keep commits small and reversible
- Use feature flags for incomplete work
- Always have a revert plan

## Alternative: GitHub Flow (For Teams)

When PRs are required (team policy, compliance):

```
main
  │
  ├── feature/add-auth ──────┐
  │                          │ PR
  ├──────────────────────────┘
```

### Git Flow (Legacy)

For projects requiring release branches (enterprise):

```
main ────────────────────────────────────────▶
  │                                     ▲
  ├── release/1.0 ──────────────────────┤
develop ──┴─────────────────────────────┴───▶
```

## Conventional Commits

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Neither fix nor feature |
| `perf` | Performance improvement |
| `test` | Adding tests |
| `chore` | Maintenance tasks |
| `ci` | CI/CD changes |

### Examples
```bash
feat(auth): add password reset flow

Implement password reset via email with secure tokens.
Tokens expire after 24 hours.

Closes #123
```

```bash
fix(api): handle null response from payment service

The payment service can return null for cancelled transactions.
Added null check and appropriate error handling.
```

## Common Commands

### Daily Workflow
```bash
# Start work
git checkout main
git pull origin main
git checkout -b feature/my-feature

# During work
git add .
git commit -m "feat: implement feature"

# Sync with main
git fetch origin
git rebase origin/main

# Push
git push -u origin feature/my-feature
```

### Fixing Mistakes
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Amend last commit
git commit --amend -m "new message"

# Undo staged changes
git restore --staged <file>

# Undo working directory changes
git restore <file>
```

### Investigating
```bash
# View history
git log --oneline -20

# View changes
git diff HEAD~1
git diff --cached  # staged changes

# Find who changed a line
git blame <file>

# Search commits
git log --grep="keyword"
git log -S "code"  # search for code
```

### Branch Management
```bash
# List branches
git branch -a

# Delete branch
git branch -d feature/done
git push origin --delete feature/done

# Rename branch
git branch -m old-name new-name
```

## Merge vs Rebase

### Merge
```bash
git checkout main
git merge feature/branch
```
- Preserves complete history
- Creates merge commits
- Better for shared branches

### Rebase
```bash
git checkout feature/branch
git rebase main
```
- Creates linear history
- Rewrites commits
- Better for local work

## Interactive Rebase

```bash
git rebase -i HEAD~3
```

Commands:
- `pick` - Keep commit
- `reword` - Change message
- `edit` - Pause for amendments
- `squash` - Combine with previous
- `fixup` - Combine, discard message
- `drop` - Remove commit

## Cherry-Pick

```bash
# Apply specific commit
git cherry-pick abc1234

# Apply without committing
git cherry-pick --no-commit abc1234
```

## Stashing

```bash
# Stash changes
git stash
git stash push -m "work in progress"

# List stashes
git stash list

# Apply stash
git stash pop        # apply and remove
git stash apply      # apply and keep

# Drop stash
git stash drop stash@{0}
```

## Tags

```bash
# Create tag
git tag v1.0.0
git tag -a v1.0.0 -m "Release 1.0.0"

# Push tags
git push origin v1.0.0
git push origin --tags

# List tags
git tag -l "v1.*"
```

## .gitignore Patterns

```gitignore
# Dependencies
node_modules/
.venv/
__pycache__/

# Build output
dist/
build/
*.egg-info/

# IDE
.idea/
.vscode/
*.swp

# Environment
.env
.env.local
*.local

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Coverage
coverage/
.coverage
htmlcov/
```

## Best Practices

1. **Commit often** - Small, focused commits
2. **Write good messages** - Clear and descriptive
3. **Pull before push** - Stay in sync
4. **Use branches** - One feature per branch
5. **Review before merge** - Use pull requests
6. **Don't commit secrets** - Use .gitignore
7. **Tag releases** - Semantic versioning
8. **Keep main clean** - Always deployable
