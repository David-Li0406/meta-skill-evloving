---
name: worktree-cleanup
description: 作業完了後のworktreeとtmuxセッションのクリーンアップ。「worktreeを削除」「作業を終了」時に使用
argument-hint: <worktree-pattern>
---

# Worktreeクリーンアップ

作業完了後のworktreeとtmuxセッションを削除します。

## 引数
- `$ARGUMENTS`: worktreeパターン（例: `feature/old-feature`）

## 手順

1. tmuxセッション終了:
   ```bash
   gwq tmux kill <pattern>
   ```

2. worktree削除（ブランチは残す）:
   ```bash
   gwq remove <pattern>
   ```

3. worktreeとブランチを一緒に削除:
   ```bash
   gwq remove -b <pattern>
   ```

4. 不要なworktree情報をクリーンアップ:
   ```bash
   gwq prune
   ```

## オプション
- 強制削除（未コミット変更があっても）: `gwq remove -f <pattern>`

## 注意
- 削除前に `gwq status` で変更がないか確認
- 重要な変更がある場合はコミットしてから削除
- **重要**: `gwq remove`は削除対象のworktreeディレクトリ内からは実行できない。メインリポジトリディレクトリに移動してから実行すること
  ```bash
  cd $(gwq get master)  # または cd ~/ghq/github.com/<owner>/<repo>
  gwq remove -b <pattern>
  ```

## 完全クリーンアップ例
```bash
# 1. セッション終了
gwq tmux kill feature/done

# 2. メインリポジトリに移動
cd $(gwq get master)

# 3. worktreeとブランチ削除
gwq remove -b feature/done

# 4. 孤立したworktree参照をクリーン
gwq prune
```
