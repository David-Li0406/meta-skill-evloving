---
name: zellij-worktree
description: Zellij git worktree workflow guide including keybindings (Ctrl+o g/G), pane/session modes, worktree switcher, and parallel development with Claude Code
---

# Zellij + gwq + fzf で Git Worktree を切り替える

git worktree を使って複数ブランチを並列で開発するためのワークフロー。
worktree を新しいペインまたはセッションで開いて、サクサク切り替えられる。

## 使い方

### キーバインド

zellij 内で以下のキーを押す：

1. **`Ctrl+o`** - Session モードに入る
2. **`g`** - Worktree Switcher を起動（**新しいペイン**で開く）
3. **`G`** - Worktree Switcher を起動（**新しいセッション**で開く）

フローティングウィンドウが開き、fzf でブランチを選択できる。

### ペインモード vs セッションモード

| モード | キー | 説明 |
|--------|------|------|
| ペイン（デフォルト） | `g` | 現在のセッション内に新しいペインを作成 |
| セッション | `G` | ブランチ専用の新しいセッションを作成 |

**ペインモード** は手軽に複数ブランチを1つのセッション内で管理したい場合に便利。
**セッションモード** はブランチごとに完全に独立した作業環境が欲しい場合に使う。

### ブランチリストの表示

fzf には以下の順番でブランチが表示される：

| マーク | 説明 |
|--------|------|
| ✨ | 新規ブランチを作成（一番上に表示） |
| 🌳 | 既存の worktree（すでに作成済み） |
| （なし） | ローカルブランチ |
| 🌐 | リモートブランチ（ローカルに未取得） |

### 新規ブランチの作成

1. `Ctrl+o g` で Worktree Switcher を起動
2. 一番上の `✨ [新規ブランチを作成]` を選択
3. 新しいブランチ名を入力
4. worktree が作成され、新しいペインで開く

### 動作の流れ

1. ブランチを選択
2. worktree が存在しなければ `gwq add` で自動作成
3. 新しいペインまたはセッションで worktree のディレクトリを開く

セッションモードの場合、セッション名は `リポジトリ名__ブランチ名` の形式になる。
例: `dotfiles__feature-new-feature`

### 関連キーバインド

| キー | 説明 |
|------|------|
| `Ctrl+o g` | Worktree Switcher（新しいペインで開く） |
| `Ctrl+o G` | Worktree Switcher（新しいセッションで開く） |
| `Ctrl+o x` | Worktree削除（worktree + ブランチ） |
| `Ctrl+o X` | Worktree削除（worktreeのみ） |
| `Ctrl+o f` | Session Switcher（fzfでセッション切り替え） |
| `Ctrl+o w` | Session Manager（組み込みプラグイン） |
| `Ctrl+o d` | 現在のセッションから Detach |

## Worktree の削除

`Ctrl+o x` または `Ctrl+o X` で worktree を削除できる。

### 削除モード

| キー | 説明 |
|------|------|
| `x` | worktree とブランチを両方削除（デフォルト） |
| `X` | worktree のみ削除（ブランチは残る） |

### 削除の流れ

1. `Ctrl+o x` で Worktree Remove を起動
2. fzf で削除する worktree を選択（複数選択可能）
3. 選択した worktree が削除される

※ 現在チェックアウト中のブランチの worktree は削除できない

## Session Switcher

`Ctrl+o f` でセッション一覧を fzf で表示し、素早く切り替えられる。

### 表示内容

| マーク | 説明 |
|--------|------|
| ✨ | 新規セッションを作成 |
| 📍 | 現在のセッション |
| 🔌 | 他のセッション |

## ユースケース

### Claude Code で並列開発

複数の機能を同時に Claude Code で開発したいとき：

1. `Ctrl+o g` で feature-A のブランチを選択 → Claude Code 起動
2. `Ctrl+o g` で feature-B のブランチを選択 → 別の Claude Code 起動
3. `Ctrl+o g` で行き来しながら両方の進捗を確認

### コードレビューしながら開発

1. main ブランチで開発中
2. `Ctrl+o g` でレビュー対象のブランチに切り替え
3. レビュー完了後、`Ctrl+o g` で main に戻る

## 関連ツール

- [gwq](https://github.com/d-kuro/gwq) - Git worktree をシンプルに管理
- [fzf](https://github.com/junegunn/fzf) - ファジーファインダー
- [zellij](https://zellij.dev/) - ターミナルマルチプレクサ

## 参考

- [tmux, gwq, fzfでworktreeをサクサク切り替えてAIコーディングを並列する](https://zenn.dev/ymat19/articles/9107170744368f)
