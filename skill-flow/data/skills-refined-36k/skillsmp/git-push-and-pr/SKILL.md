---
name: git-push-and-pr
description: Git push to remote and create GitHub Pull Request. Use when the user wants to push changes and create a PR after completing code changes. Handles worktree environments, automatic upstream setup, and PR creation with Japanese title/body using HEREDOC format.
---

# Git Push and PR Creation

Pushes the current branch to remote and creates a GitHub Pull Request with structured Japanese descriptions.

## Overview

This skill provides a workflow for:
1. Checking if the branch is pushed to remote
2. Pushing with proper upstream tracking
3. Creating a PR using `gh pr create` command
4. Handling git worktree environments

## Prerequisites

- `git` command available
- `gh` CLI installed and authenticated (`gh auth login`)
- Current directory is a git repository (or worktree)
- Changes committed to the branch

## Workflow

### Step 1: Check Current State

```bash
# Get current branch name
git branch --show-current

# Check for uncommitted changes
git status --porcelain

# Check if remote tracking exists
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null
```

### Step 2: Push to Remote

**If upstream is not set (first push):**

```bash
git push -u origin $(git branch --show-current)
```

**If upstream already exists:**

```bash
git push
```

### Step 3: Create Pull Request

Use HEREDOC format to preserve multi-line body formatting:

```bash
gh pr create --title "feat: [機能名]" --base main --body "$(cat <<'EOF'
## 概要
[変更の目的と背景]

## 変更内容

### 主な変更
- [変更点1]
- [変更点2]

### API変更
- [エンドポイント変更]

### UI/UX変更
- [画面変更]

## テスト

- [ ] 手動テスト実施
- [ ] エラーハンドリング確認

## レビュー観点

### 重点的に確認してほしい箇所
1. **[ファイル名]**: [理由]

## チェックリスト

- [ ] TypeScriptの型安全性を確保
- [ ] エラーハンドリングを実装
EOF
)"
```

## Commands Reference

### Branch Operations

```bash
# Get current branch
git branch --show-current

# Check if branch exists on remote
git ls-remote --heads origin $(git branch --show-current)

# Check tracking branch
git rev-parse --abbrev-ref --symbolic-full-name @{u}
```

### Push Operations

```bash
# Push with upstream tracking (first push)
git push -u origin <branch-name>

# Normal push (after upstream is set)
git push

# Force push (use with caution)
git push --force-with-lease
```

### PR Operations

```bash
# Create PR with HEREDOC body
gh pr create --title "<title>" --base main --body "$(cat <<'EOF'
<multi-line body>
EOF
)"

# Create PR interactively
gh pr create

# Create PR with specific reviewers
gh pr create --title "<title>" --body "<body>" --reviewer <username>

# Create draft PR
gh pr create --title "<title>" --body "<body>" --draft

# List PRs
gh pr list

# View PR URL after creation
gh pr view --web
```

## Worktree Environment Handling

Git worktrees share the same `.git` directory. Commands work the same way in worktrees:

```bash
# Check if in worktree
git rev-parse --git-common-dir

# Push from worktree (same as regular repo)
git push -u origin $(git branch --show-current)
```

**Important**: Each worktree has its own branch, so push operations are isolated per worktree.

## Error Handling

### Uncommitted Changes

```bash
# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
  echo "Error: Uncommitted changes exist. Please commit first."
  exit 1
fi
```

### Branch is main

```bash
# Prevent PR from main to main
current_branch=$(git branch --show-current)
if [ "$current_branch" = "main" ]; then
  echo "Error: Cannot create PR from main branch. Create a feature branch first."
  exit 1
fi
```

### gh CLI Not Authenticated

```bash
# Check gh auth status
gh auth status
# If not authenticated: gh auth login
```

### PR Already Exists

```bash
# Check if PR already exists for branch
gh pr list --head $(git branch --show-current) --state open
```

## PR Title Conventions

Follow Conventional Commits format in Japanese:

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feat: [機能名]の実装` | `feat: 出席管理機能の実装` |
| Bug Fix | `fix: [問題]の修正` | `fix: ログインエラーの修正` |
| Refactor | `refactor: [対象]のリファクタリング` | `refactor: API構造のリファクタリング` |
| Docs | `docs: [内容]のドキュメント更新` | `docs: READMEの更新` |
| Performance | `perf: [対象]のパフォーマンス改善` | `perf: クエリの最適化` |
| Style | `style: [対象]のスタイル修正` | `style: UIデザインの調整` |

## Complete Example Script

```bash
#!/bin/bash

# 1. Get current branch
BRANCH=$(git branch --show-current)

# 2. Check not on main
if [ "$BRANCH" = "main" ]; then
  echo "Error: Cannot create PR from main branch"
  exit 1
fi

# 3. Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
  echo "Error: Uncommitted changes exist"
  exit 1
fi

# 4. Push to remote (with -u if needed)
if ! git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null; then
  echo "Setting upstream and pushing..."
  git push -u origin "$BRANCH"
else
  echo "Pushing to existing upstream..."
  git push
fi

# 5. Create PR with HEREDOC
gh pr create --title "feat: 機能の実装" --base main --body "$(cat <<'EOF'
## 概要
この変更は...

## 変更内容
- 変更点1
- 変更点2

## テスト
- [ ] 手動テスト実施
EOF
)"

# 6. Show PR URL
echo "PR created successfully!"
gh pr view --web
```

## Integration with github-pr-creator Agent

This skill is designed to be used by the `github-pr-creator` agent:

1. Agent analyzes code changes and generates PR description
2. Agent uses this skill's commands to:
   - Check and push branch to remote
   - Create PR with structured Japanese body
3. Agent returns the PR URL to user

## Best Practices

1. **Always commit before creating PR**: Check `git status` first
2. **Use descriptive branch names**: `feat/attendance-management`, `fix/login-error`
3. **Use HEREDOC for body**: Preserves formatting and special characters
4. **Quote variables**: `"$BRANCH"` to handle special characters
5. **Check existing PRs**: Avoid duplicate PRs for same branch
6. **Use `--base main`**: Explicitly specify target branch

## Troubleshooting

### "Permission denied" on push

```bash
# Check remote URL
git remote -v

# If HTTPS, may need credentials
gh auth setup-git
```

### "No upstream branch" error

```bash
# Set upstream explicitly
git push -u origin $(git branch --show-current)
```

### HEREDOC not working in PowerShell

On Windows, use Git Bash or escape properly:

```powershell
# PowerShell alternative
$body = @"
## 概要
変更内容...
"@

gh pr create --title "feat: 機能" --base main --body $body
```
