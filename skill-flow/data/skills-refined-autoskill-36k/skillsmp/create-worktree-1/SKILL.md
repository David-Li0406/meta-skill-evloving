---
name: create-worktree
description: |
  Git worktreeを使って並行開発環境を構築。feature/<name>ブランチと
  .worktrees/<name>/ディレクトリを作成し、複数機能の同時開発を可能にする。
  「worktreeを作成」「並行開発環境を準備」などの指示で起動。
---

# Create Worktree Skill

## Purpose

このスキルは、Git worktreeを活用した並行開発環境の構築を自動化します:

- 複数の機能を同時に異なるディレクトリで開発
- mainブランチを切り替えずに新しいブランチで作業
- 独立した作業ディレクトリによるコンテキスト分離
- CI/CDの並行実行による効率的な開発フロー

## When to Use

以下の場合にこのスキルを使用:

- 新機能の開発開始時
- 複数のfeatureブランチを並行で作業したい場合
- mainブランチの状態を保ちながら実験的な変更を試したい場合
- レビュー待ちの間に別のタスクに着手したい場合
- 緊急のhotfixと通常開発を並行して進めたい場合

## Instructions

### 1. Validate Environment

**必須条件の確認:**

```bash
# Gitリポジトリ内で実行されているか確認
git rev-parse --git-dir 2>/dev/null || echo "Not a git repository"

# 既存のworktreeを確認
git worktree list
```

### 2. Determine Feature Name

ユーザーから機能名を取得するか、作業内容から適切な名前を提案:

**Good feature names:**
- `user-authentication`
- `api-rate-limiting`
- `dashboard-redesign`

**Avoid:**
- スペースを含む名前
- 特殊文字（`/` は除く）
- 曖昧な名前（`fix`, `test` など）

### 3. Create Worktree

**基本的なworktree作成:**

```bash
# 機能名を受け取る
FEATURE_NAME="<feature-name>"

# ブランチ名を決定（カスタマイズ可能）
BRANCH_NAME="feature/${FEATURE_NAME}"

# worktreeディレクトリパス
WORKTREE_DIR=".worktrees/${FEATURE_NAME}"

# 既存ブランチがあるか確認
if git show-ref --verify --quiet "refs/heads/${BRANCH_NAME}"; then
  # 既存ブランチからworktreeを作成
  git worktree add "${WORKTREE_DIR}" "${BRANCH_NAME}"
else
  # 新しいブランチでworktreeを作成
  git worktree add -b "${BRANCH_NAME}" "${WORKTREE_DIR}"
fi
```

### 4. Report Status

作成後、以下の情報をユーザーに提供:

```markdown
✅ Worktreeを作成しました

**Location:** .worktrees/<feature-name>/
**Branch:** feature/<feature-name>
**Base:** <base-branch> (例: main)

**次のステップ:**
1. `cd .worktrees/<feature-name>/` でディレクトリに移動
2. 通常通り開発を進める
3. 完了したら `pr-and-cleanup` スキルでPR作成とクリーンアップ

**便利なコマンド:**
- `git worktree list` - すべてのworktreeを表示
- `git worktree remove <path>` - worktreeを手動削除
```

### 5. Handle Edge Cases

**既存のworktreeが同じパスに存在する場合:**

```bash
if [ -d "${WORKTREE_DIR}" ]; then
  echo "⚠️ Worktree already exists at ${WORKTREE_DIR}"
  echo "既存のworktreeを使用しますか、それとも別の名前で作成しますか？"
  # ユーザーに確認
fi
```

**ディスク容量の確認（オプション）:**

```bash
# 現在のリポジトリサイズを確認
du -sh .git

# worktree作成には同程度のディスク容量が必要
```

## Key Principles

1. **シンプルさ優先**: プロジェクト固有の設定は行わない
2. **安全性**: 既存のworktreeを上書きしない
3. **標準的な命名規則**: `feature/` プレフィックスをデフォルトとする
4. **柔軟性**: ブランチ名とディレクトリ名をカスタマイズ可能

## Customization Options

ユーザーが以下をカスタマイズしたい場合は質問して確認:

- **ブランチプレフィックス**: `feature/`, `bugfix/`, `hotfix/` など
- **worktreeベースディレクトリ**: `.worktrees/` 以外の場所
- **ベースブランチ**: `main` 以外（`develop`, `staging` など）

## Dependencies

- Git 2.5+ (worktree機能のサポート)
- 書き込み権限のあるディレクトリ

## Integration with Other Skills

- **pr-and-cleanup**: worktree環境でのPR作成とクリーンアップ
- **code-review**: worktree内でのコードレビュー実施

## Best Practices

1. **命名の一貫性**: チーム内で統一された命名規則を使用
2. **定期的なクリーンアップ**: 不要になったworktreeは削除
3. **worktreeリストの確認**: `git worktree list` で定期的に確認
4. **ドキュメント化**: プロジェクトのREADMEにworktreeの使用方法を記載

## Common Issues and Solutions

### Issue 1: "already checked out" エラー

```
fatal: 'feature/xxx' is already checked out at '.worktrees/xxx'
```

**Solution**: 既存のworktreeを削除するか、別のブランチ名を使用

```bash
git worktree remove .worktrees/xxx
# または
git worktree add -b feature/xxx-v2 .worktrees/xxx-v2
```

### Issue 2: worktree削除後もブランチが残る

**Solution**: worktreeとブランチは独立して管理される

```bash
# worktreeの削除
git worktree remove .worktrees/xxx

# ブランチも削除する場合（オプション）
git branch -d feature/xxx
```

### Issue 3: .worktreesディレクトリが大きくなりすぎる

**Solution**: 定期的に不要なworktreeをクリーンアップ

```bash
# 使用していないworktreeを確認
git worktree list

# 不要なものを削除
git worktree prune
```

## Notes

- worktreeは完全な作業コピーを作成するため、大きなリポジトリでは時間がかかる場合があります
- `.git/worktrees/` にメタデータが保存されます
- worktree内でもgitコマンドは通常通り動作します
- 各worktreeは独立した作業ディレクトリですが、同じリポジトリ（.git）を共有します
