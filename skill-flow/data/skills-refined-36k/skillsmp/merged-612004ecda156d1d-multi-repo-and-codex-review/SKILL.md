---
name: multi-repo-and-codex-review
description: Use this skill for parallel development across multiple repositories and to conduct code reviews interactively with Codex in a tmux session.
---

# 複数リポジトリ並行開発とCodexレビュー

このスキルは、ghq・gwq・tmuxを使用して複数リポジトリでの並行開発を行い、同時にCodexを利用してコードレビューを実施するためのワークフローを提供します。

## 複数リポジトリ並行開発

### ワークフロー

#### 1. リポジトリの取得
```bash
# リポジトリをclone（既にあればスキップ）
ghq get <repository-url-1>
ghq get <repository-url-2>
```

#### 2. 各リポジトリでworktree作成
```bash
# フロントエンド
cd $(ghq list -p | grep <frontend-repo>) && gwq add -b <feature-branch-1>

# バックエンド
cd $(ghq list -p | grep <backend-repo>) && gwq add -b <feature-branch-2>
```

#### 3. 各worktreeで開発サーバー起動
```bash
gwq tmux run -w <feature-branch-1> "<frontend-command>"
gwq tmux run -w <feature-branch-2> "<backend-command>"
```

#### 4. 状態確認
```bash
# 全リポジトリのworktree状態
gwq status -g --show-processes

# tmuxセッション一覧
gwq tmux list
```

#### 5. 特定worktreeでコマンド実行
```bash
gwq exec <feature-branch-1> -- <command-for-frontend>
gwq exec <feature-branch-2> -- <command-for-backend>
```

## Codexを使用したコードレビュー

### 機能

- tmuxでCodexペインを作成・管理
- Codexにメッセージを送信し、返答をキャプチャ
- 開発作業を続けながらCodexと対話

### 実行手順

#### ステップ1: Codexペインを作成
```bash
~/.claude/skills/tmux-codex-review/scripts/tmux-manager.sh ensure
```

#### ステップ2: レビュー依頼を送信
```bash
~/.claude/skills/tmux-codex-review/scripts/tmux-manager.sh send "<your-review-request>"
```

#### ステップ3: 返答を待機してキャプチャ
```bash
~/.claude/skills/tmux-codex-review/scripts/tmux-manager.sh wait_response && \
~/.claude/skills/tmux-codex-review/scripts/tmux-manager.sh capture <number-of-lines>
```

#### ステップ4: 結果の報告
```
Codexにメッセージを送信しました。右側のtmuxペインでCodexが応答しているのが見えるはずです。

少し待ってから、Codexの返答をキャプチャしましょう。

---
Codexの返答:
[キャプチャした内容]
---
```

## 注意事項

- tmuxセッション内で実行すること
- Codexの応答には数秒〜数十秒かかる場合があります
- Codexペインは明示的に`close`するまで開いたままです