---
name: worktree-management
description: 並行タスク用にgit worktreeを作成・管理する（worktreeが無い場合のみ使う）。
allowed-tools: Bash, Read, Grep, Glob
---

# Worktree管理（共通）

このスキルは、対象タスクのworktreeが存在しない場合にのみ使用する。

## 手順

1) 事前確認（preflight）
- Run: `git status --porcelain`
- If uncommitted changes exist, ask user to commit/stash.
- Run: `git fetch --all --prune`

2) ブランチとbaseを決める
- Branch: `feature/issue-<NUMBER>` or `fix/issue-<NUMBER>`
- Base: `origin/main`

3) ignore設定を確認
- Ensure `.worktrees/` is in `.gitignore`

4) worktreeを作成
```
mkdir -p .worktrees
git worktree add .worktrees/<safe-branch-name> -b <branch> <base>
```

## 安全制約
- Never delete with `rm -rf`
- Remove via `git worktree remove` only when explicitly asked
