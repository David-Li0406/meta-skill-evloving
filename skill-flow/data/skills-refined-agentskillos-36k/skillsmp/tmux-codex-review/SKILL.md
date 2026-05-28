---
name: tmux-codex-review
description: tmuxで右半分にCodexを開いてコードレビューを実行。「レビューして」「Codexでレビュー」「Codexに聞いて」「セカンドオピニオン」等の発言で起動。
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# tmux-codex-review

tmuxで右半分にCodexを開いて、インタラクティブにレビューやセカンドオピニオンを取得するSkill。

## 機能

- tmuxで右半分にCodexペインを作成・管理
- Codexにメッセージを送信し、返答をキャプチャ
- Claude Codeは左ペインで作業を継続しながらCodexと対話

## tmux-manager.sh コマンド

スクリプトパス: `~/.claude/skills/tmux-codex-review/scripts/tmux-manager.sh`

| コマンド | 説明 |
|----------|------|
| `ensure` | Codexペインを作成（既存なら再利用） |
| `send "msg"` | Codexにメッセージを送信（Enter自動送信） |
| `send -` | stdinからメッセージを読み取って送信 |
| `wait_response [s]` | 応答完了を待機（デフォルト120秒） |
| `capture [n]` | 出力をキャプチャ（デフォルト100行） |
| `close` | Codexペインを閉じる |
| `status` | ペインの状態を確認 |

## 前提条件

- tmuxセッション内で実行すること
- `codex`コマンドがインストールされていること（`npm install -g @openai/codex`）

## 実行手順

### ステップ1: Codexペインを作成

```bash
~/.claude/skills/tmux-codex-review/scripts/tmux-manager.sh ensure
```

出力例:
```
Created new Codex pane: %6 (bg=colour233)
Auto-started Codex in pane
```

### ステップ2: レビュー依頼を送信

git diffの内容をレビューしてもらう場合:

```bash
~/.claude/skills/tmux-codex-review/scripts/tmux-manager.sh send "git diffを確認して、セキュリティやパフォーマンスの問題があれば教えてください。"
```

または具体的な質問:

```bash
~/.claude/skills/tmux-codex-review/scripts/tmux-manager.sh send "このリポジトリのアーキテクチャについてセカンドオピニオンをください。"
```

### ステップ3: 返答を待機してキャプチャ

`wait_response`で応答完了を待機してからキャプチャ:

```bash
~/.claude/skills/tmux-codex-review/scripts/tmux-manager.sh wait_response && \
~/.claude/skills/tmux-codex-review/scripts/tmux-manager.sh capture 200
```

または従来のsleep方式:

```bash
sleep 30 && ~/.claude/skills/tmux-codex-review/scripts/tmux-manager.sh capture 100
```

### ステップ4: 結果の報告

キャプチャした内容からCodexの返答を抽出し、ユーザーに報告。

## 出力形式

```
Codexにメッセージを送信しました。右側のtmuxペインでCodexが応答しているのが見えるはずです。

少し待ってから、Codexの返答をキャプチャしましょう。

---
Codexの返答:
[キャプチャした内容]
---

Codexも元気そうですね！右側のtmuxペインでCodexが対話モードで待機しています。
```

## レビュー用プロンプト例

### コードレビュー
```
git diffを確認して、以下の観点でレビューしてください:
- P0: セキュリティ脆弱性、データ損失リスク
- P1: パフォーマンス問題、エラーハンドリング不足
- P2: 設計改善、保守性向上
- P3: 命名改善、軽微なリファクタリング
```

### アーキテクチャレビュー
```
このリポジトリの構造を確認して、設計上の懸念点があれば教えてください。
```

### セカンドオピニオン
```
[具体的な質問や相談内容]についてセカンドオピニオンをください。
```

## 注意事項

- tmuxセッション外では動作しません
- Codexの応答には数秒〜数十秒かかる場合があります
- `wait_response`は「esc to interrupt」の消失と「›」プロンプトの出現で完了を検知します
- Codexペインは明示的に`close`するまで開いたままです
