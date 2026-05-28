---
name: git-workflow
description: Git and GitHub workflow automation skills for OpenCode agents
---

# Git Workflow Skill

Use this skill for Git and GitHub operations in OpenCode projects.

## When to Use

- Initializing new Git repositories
- Creating GitHub repositories via `gh` CLI
- Managing feature branches and PRs
- Resolving merge conflicts
- Setting up Git submodules
- Configuring Git hooks and automation

## Git Repository Initialization

### Initialize New Repository
```bash
# Initialize git repo
git init

# Configure user
git config user.name "layeddie"
git config user.email "layeddie@users.noreply.github.com"

# Configure repository
git config core.autocrlf input
git config init.defaultBranch main

# Make initial commit
git add .
git commit -m "feat: initial commit"

# Rename to main branch
git branch -M main
```

### Create GitHub Repository
```bash
# Create public repo
gh repo create <repo-name> --public --source=. --remote=origin --push

# Create private repo
gh repo create <repo-name> --private --source=. --remote=origin --push

# Verify setup
git remote -v
gh repo view
```

### Initialize Existing Project with GitHub
```bash
# Navigate to project directory
cd ~/path/to/your-project-name

# Initialize git
git init
git add .
git commit -m "feat: initial commit"

# Create GitHub repo and push
gh repo create <repo-name> --public --source=. --remote=origin --push
```

## Feature Branch Workflow

### Create Feature Branch
```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/descriptive-name
```

### Commit Changes with Conventional Commits
```bash
# Stage all changes
git add .

# Commit with conventional format
git commit -m "feat: add git specialist role"
git commit -m "fix: resolve merge conflict in git_rules.md"
git commit -m "docs: update README with git workflow"
git commit -m "refactor: move tensioner to separate repository"
git commit -m "test: add integration tests for git workflow"
git commit -m "chore: update dependencies"
```

### Push Feature Branch
```bash
# Push to GitHub
git push -u origin feature/descriptive-name
```

### Create Pull Request
```bash
# Create PR with description
gh pr create --title "Add git workflow integration" \
  --body "Implements git_rules.md and git specialist role" \
  --reviewer layeddie

# Create PR linked to issue
gh pr create --title "Fix issue #123" --body "Closes #123"

# Create PR with specific base branch
gh pr create --base develop --title "Feature: add new functionality"
```

### Merge Pull Request
```bash
# Merge with squash (recommended for feature branches)
gh pr merge --squash

# Merge with regular merge
gh pr merge --merge

# Rebase and merge
gh pr merge --rebase
```

### Cleanup After Merge
```bash
# Switch back to main
git checkout main

# Pull latest changes
git pull origin main

# Delete local branch
git branch -d feature/descriptive-name

# Delete remote branch
git push origin --delete feature/descriptive-name
```

## Git Submodules

### Add Submodule
```bash
# Add ai-rules as submodule
git submodule add https://github.com/layeddie/ai-rules.git ai-rules
git commit -m "chore: add ai-rules as submodule"

# Update submodule to latest
git submodule update --remote ai-rules
git add ai-rules
git commit -m "chore: update ai-rules submodule"

# Remove submodule
git submodule deinit ai-rules
git rm ai-rules
rm -rf .git/modules/ai-rules
git commit -m "chore: remove ai-rules submodule"
```

## Merge Conflict Resolution

### Check for Conflicts
```bash
# Attempt merge
git checkout main
git pull origin main
git merge feature/my-feature

# Check if conflicts exist
git status
# Will show "both modified" for conflicted files
```

### Resolve Conflicts Manually
```bash
# Open conflicted files
# Look for conflict markers:
# <<<<<<< HEAD
# Your changes
# =======
# Incoming changes
# >>>>>>> feature/my-feature

# Edit file to resolve conflicts
vim <conflicted-file>

# Mark as resolved
git add <conflicted-file>

# Complete merge
git commit -m "fix: resolve merge conflict in <file>"
```

### Resolve with Merge Tool
```bash
# Use configured merge tool
git mergetool

# Configure merge tool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# Run merge tool
git mergetool
git commit -m "fix: resolve merge conflicts"
```

### Abort Merge
```bash
# Abort merge and return to previous state
git merge --abort
```

## Git Hooks Automation

### Pre-commit Hook (Format and Test)
```bash
# Create .git/hooks/pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
mix format
mix test --max-failures=1
EOF
chmod +x .git/hooks/pre-commit
```

### Pre-push Hook (Run Tests)
```bash
# Create .git/hooks/pre-push
cat > .git/hooks/pre-push << 'EOF'
#!/bin/sh
mix test
EOF
chmod +x .git/hooks/pre-push
```

### Commit-msg Hook (Conventional Commits)
```bash
# Create .git/hooks/commit-msg
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/sh
commit_regex='^(feat|fix|docs|style|refactor|test|chore|ci|perf)(\(.+\))?: .{1,50}'
error_msg="Aborting commit. Your commit message is not formatted correctly."

if ! grep -qE "$commit_regex" "$1"; then
    echo "$error_msg" >&2
    exit 1
fi
EOF
chmod +x .git/hooks/commit-msg
```

## GitHub CLI Automation

### Repository Management
```bash
# List repositories
gh repo list layeddie

# View repository details
gh repo view layeddie/ai-rules

# View repository settings
gh repo view layeddie/ai-rules --json name,visibility,defaultBranchRef

# Update repository visibility
gh repo edit layeddie/ai-rules --visibility public
```

### Issue Management
```bash
# Create issue
gh issue create --title "Bug: git workflow fails" \
  --body "Description of the bug" \
  --label bug

# List issues
gh issue list --label bug --limit 10

# View issue details
gh issue view 123

# Close issue
gh issue close 123
```

### Pull Request Management
```bash
# List open PRs
gh pr list --state open

# View PR details
gh pr view 456

# View PR checks
gh pr checks 456

# Close PR
gh pr close 456
```

### Workflow Management
```bash
# List workflows
gh workflow list

# View workflow runs
gh run list --workflow=ci.yml

# Trigger workflow
gh workflow run ci.yml

# View workflow run details
gh run view 789 --log
```

## Git Maintenance

### Cleanup
```bash
# Prune remote branches
git remote prune origin

# Remove stale branches
git branch -vv | grep ': gone]' | awk '{print $1}' | xargs git branch -D

# Clean untracked files
git clean -fd

# Reset to main (use carefully)
git reset --hard origin/main
```

### Large File Management
```bash
# Find large files
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {print substr($0,6)}' | \
  sort -nk2 | \
  tail -10

# Remove file from history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch large-file.zip" \
  --prune-empty --tag-name-filter cat -- --all
```

### Git Optimization
```bash
# Repack repository
git gc --aggressive --prune=now

# Verify repository integrity
git fsck --full

# Check repository size
du -sh .git
```

## Branch Protection Configuration

### Configure Branch Protection via CLI
```bash
# Enable branch protection for main
gh api repos/layeddie/<repo>/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["ci"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}' \
  --field restrictions=null \
  --field allow_deletions=false \
  --field allow_force_pushes=false
```

### View Branch Protection Rules
```bash
gh api repos/layeddie/<repo>/branches/main/protection
```

## Best Practices

### Commit Frequently
- ✅ Commit often, commit early
- ✅ Keep commits atomic (one logical change)
- ✅ Write descriptive commit messages
- ❌ Don't commit broken code
- ❌ Don't commit sensitive data

### Feature Branches
- ✅ Create branches for features
- ✅ Use descriptive branch names
- ✅ Keep branches short-lived
- ❌ Don't work directly on main
- ❌ Don't leave stale branches

### Pull Requests
- ✅ Request review before merging
- ✅ Link to related issues
- ✅ Update PR description if scope changes
- ❌ Don't merge unreviewed code
- ❌ Don't merge failing tests

### Merge Strategy
- ✅ Use squash merge for feature branches
- ✅ Use rebase for linear history
- ❌ Don't use merge commits on main (except hotfixes)
- ❌ Don't force push to shared branches

## Troubleshooting

### Repository Not Found
```bash
# Check remote configuration
git remote -v

# Update remote URL
git remote set-url origin https://github.com/layeddie/ai-rules.git
```

### Authentication Issues
```bash
# Check authentication
gh auth status

# Login to GitHub
gh auth login

# Re-authenticate
gh auth logout
gh auth login
```

### Submodule Issues
```bash
# Reinitialize submodules
git submodule deinit --all
git submodule update --init --recursive

# Sync submodule URLs
git submodule sync --recursive
```

### Merge Conflicts
```bash
# See conflict markers
git diff --check

# Use merge tool
git mergetool

# Abort merge if needed
git merge --abort
```

## Integration with OpenCode

### Build Mode Git Workflow
```bash
# 1. Create feature branch before implementing
git checkout -b feature/impl-<feature-name>

# 2. Implement feature and commit
git add .
git commit -m "feat: implement <feature description>"

# 3. Push and create PR
git push -u origin feature/impl-<feature-name>
gh pr create --title "Implement <feature>" --body "Closes #<issue>"

# 4. After review and merge
gh pr merge --squash
git checkout main
git pull origin main
git branch -d feature/impl-<feature-name>
```

### Plan Mode Git Workflow
Plan mode is read-only, no git operations needed.

### Review Mode Git Workflow
```bash
# Review PR
gh pr view <pr-number>

# Add review comment
gh pr review <pr-number> --comment -b "Suggestion: use conventional commits"

# Approve PR
gh pr review <pr-number> --approve

# Request changes
gh pr review <pr-number> --request-changes -b "Please add tests"
```

## Summary

This skill provides:
- Repository initialization and setup
- Feature branch workflow automation
- GitHub CLI integration
- Merge conflict resolution
- Submodule management
- Git hooks automation
- Best practices and troubleshooting
- Integration with OpenCode modes
