---
name: git-worktree-management
description: Use this skill to manage Git worktrees for parallel development, ensuring proper branch handling and environment setup.
---

# Git Worktree Management

このスキルは、Git worktreeを使用して並行開発環境を構築し、ブランチの管理を支援します。

## 重要なルール

- 作業を開始する前に、必ずこのスキルを使ってworktreeとブランチを作成してください。
- worktree作成後は、必ず `.claude/settings.local.json` のシンボリックリンクを作成すること。この手順は必須です。

## Git Workflow Rules

### 1. Pre-work Check (作業前のブランチ確認)

作業を開始する前に、まず `git branch --show-current` で現在のブランチを確認してください。

- **現在が `main` (または `master`) ブランチの場合**:
  - 直接作業は禁止。新しい機能開発や修正を行う場合は、必ず `git worktree` を使用して新しい作業ディレクトリを作成してください。
  
- **現在が `main` 以外のブランチの場合**:
  - そのまま作業を開始してください。

### 2. Create Worktree

#### Purpose

このスキルは、Git worktreeを活用した並行開発環境の構築を自動化します。

#### Instructions

1. **Validate Environment**:
   ```bash
   git rev-parse --git-dir 2>/dev/null || echo "Not a git repository"
   git worktree list
   ```

2. **Determine Feature Name**:
   ユーザーから機能名を取得するか、作業内容から適切な名前を提案します。

3. **Create Worktree**:
   ```bash
   FEATURE_NAME="<feature-name>"
   BRANCH_NAME="feature/${FEATURE_NAME}"
   WORKTREE_DIR=".worktrees/${FEATURE_NAME}"

   if git show-ref --verify --quiet "refs/heads/${BRANCH_NAME}"; then
     git worktree add "${WORKTREE_DIR}" "${BRANCH_NAME}"
   else
     git worktree add -b "${BRANCH_NAME}" "${WORKTREE_DIR}"
   fi
   ```

4. **Create Symbolic Link**:
   ```bash
   MAIN_REPO=$(git worktree list --porcelain | grep -m 1 "worktree" | cut -d' ' -f2)
   rm -f "${WORKTREE_DIR}/.claude/settings.local.json"
   ln -s "${MAIN_REPO}/.claude/settings.local.json" "${WORKTREE_DIR}/.claude/settings.local.json"
   ```

5. **Report Status**:
   ```markdown
   ✅ Worktreeを作成しました
   **Location:** .worktrees/<feature-name>/
   **Branch:** feature/<feature-name>
   ```

### 3. Pull Request (PR作成)

作業完了後のPull Request（PR）作成支援においては、以下のルールを適用してください。
- **言語:** タイトルおよび説明文は必ず「日本語」で記述すること。
- 内容: 変更の概要、目的、関連するIssue番号を含めること。

## Best Practices

1. **命名の一貫性**: チーム内で統一された命名規則を使用。
2. **定期的なクリーンアップ**: 不要になったworktreeは削除。
3. **worktreeリストの確認**: `git worktree list` で定期的に確認。

## Common Issues and Solutions

### Issue 1: "already checked out" エラー
- **Solution**: 既存のworktreeを削除するか、別のブランチ名を使用。

### Issue 2: worktree削除後もブランチが残る
- **Solution**: worktreeとブランチは独立して管理される。

### Issue 3: .worktreesディレクトリが大きくなりすぎる
- **Solution**: 定期的に不要なworktreeをクリーンアップ。

## Notes

- worktreeは完全な作業コピーを作成するため、大きなリポジトリでは時間がかかる場合があります。
- 各worktreeは独立した作業ディレクトリですが、同じリポジトリ（.git）を共有します。