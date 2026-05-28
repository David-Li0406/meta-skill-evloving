---
name: create-worktree
description: planモード終了後、feature開発用のworktreeを自動作成します。
allowed-tools: Bash(git:*), Bash(mkdir:*), Bash(cp:*), Bash(chmod:*), Bash(bash:*), Bash(python3:*)
---

# Git Worktree Creator

planモード終了後、feature開発用の独立したworktree環境を自動作成します。

## 概要

このSkillは以下を自動で実行します：

1. `.worktrees/<feature-name>/` ディレクトリにworktreeを作成
2. `feature/<feature-name>` ブランチを新規作成
3. Python venv環境をセットアップ

## 使用方法

### 基本的な使い方

```bash
# スクリプトを実行
bash .claude/skills/create-worktree/scripts/create_worktree.sh <feature-name>

# 例: svg-export 機能を開発する場合
bash .claude/skills/create-worktree/scripts/create_worktree.sh svg-export
```

### 実行結果

```
.worktrees/svg-export/     # worktreeディレクトリ
├── venv/                  # 新規作成されたvenv
├── app/                   # Next.jsフロントエンド
├── api/                   # FastAPIバックエンド
└── ...
```

## worktree内での開発

```bash
cd .worktrees/<feature-name>
source venv/bin/activate
npm run dev
```

## 作業完了後

### PR作成とworktree削除を同時に行う（推奨）

**pr-and-cleanup** スキルを使用：

```bash
cd .worktrees/<feature-name>
/pr-and-cleanup
```

### 手動でworktreeを削除する場合

```bash
git worktree remove .worktrees/<feature-name>
```
