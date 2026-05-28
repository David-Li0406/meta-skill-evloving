---
name: pr-and-cleanup
description: PR作成とworktreeの自動クリーンアップを行います。
allowed-tools: Bash(git:*), Bash(gh:*), Bash(cd:*), Bash(pwd:*)
---

# PR And Cleanup

worktreeでの開発完了後、PR作成と同時にworktreeを自動的にクリーンアップします。

## 概要

このスキルは以下を自動で実行します:

1. 現在のworktreeディレクトリとブランチを検出
2. 未コミットの変更がないか確認
3. PRを作成
4. PR作成成功後、worktreeを削除
5. mainブランチ（リポジトリルート）に移動

**重要**: ローカルブランチとリモートブランチは残ります

## 使用方法

### 基本的な使い方

```bash
# worktreeディレクトリ内で実行
cd .worktrees/<feature-name>
bash ../../.claude/skills/pr-and-cleanup/scripts/pr_and_cleanup.sh
```

### オプション

```bash
# PR作成のみ（worktreeを削除しない）
bash pr_and_cleanup.sh --pr-only

# worktreeクリーンアップのみ（PR作成済みの場合）
bash pr_and_cleanup.sh --cleanup-only

# タイトルと本文を事前指定
bash pr_and_cleanup.sh --title "feat: Add new feature" --body "詳細な説明..."

# ドラフトPRとして作成
bash pr_and_cleanup.sh --draft
```

## 前提条件

- worktreeディレクトリ内で実行すること
- すべての変更がコミット済みであること
- `gh` CLI がインストール・認証済みであること

## 関連スキル

- `create-worktree`: worktree作成
