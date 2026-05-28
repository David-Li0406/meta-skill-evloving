---
name: worktree-create
description: gwqを使って新しいworktreeを作成・追加。「worktreeを作成」「worktreeを追加」「新しいブランチで作業」「feature branchを切りたい」「PRを作成するためにブランチを作る」「gwq add」時に使用
argument-hint: <branch-name>
---

# Worktree作成

gwqを使って新しいworktreeを作成します。

## 引数
- `$ARGUMENTS`: ブランチ名（例: `feature/new-feature`）

## 手順

1. 既存ブランチからworktreeを作成する場合:
   ```bash
   # リモートブランチの場合は先にfetch
   git fetch origin $ARGUMENTS
   gwq add $ARGUMENTS
   ```

2. 新規ブランチを作成してworktreeを作成する場合:
   ```bash
   gwq add -b $ARGUMENTS
   ```

3. 作成後、worktreeのパスを取得して移動可能:
   ```bash
   cd $(gwq get $ARGUMENTS)
   ```

4. 作成されたworktreeの確認:
   ```bash
   gwq list
   ```

## オプション
- インタラクティブ選択: `gwq add -i`
- 作成後そのまま移動: `gwq add -s <branch>`
