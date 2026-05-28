# next - 次ステップ提案

## 実行内容

タスクの現在状態を分析して次に実行すべきコマンドを提案する。

## 手順

1. タスク名が省略された場合、会話コンテキストから推測
2. `specs/{taskname}/` を確認
3. 各ファイルの存在と内容から状態を判定

## 状態判定ロジック

| 状態 | 判定条件 | 提案コマンド |
|------|---------|-------------|
| タスク未作成 | overview.md なし | `/sdd:init-task` |
| 調査未完了 | 調査項目に🔴がある | `/sdd:conduct-research {taskname}` |
| 要件未定義 | specification.md なし | `/sdd:define-requirements {taskname}` |
| 技術未定義 | technical-details.md なし | `/sdd:define-technical {taskname}` |
| Phase未計画 | Phase構成セクションなし | `/sdd:plan-phases {taskname}` |
| Phase詳細未作成 | tasks/phase*.md なし | `/sdd:breakdown-phase {taskname} N` |
| 実装中 | タスクに未完了あり | `/sdd:implement-phase {taskname} N.M` |
| Phase検証待ち | 全タスク完了 | `/sdd:verify-phase {taskname} N` |

## 出力例

```
## 次のステップ: auth-feature

現在の状態: Phase 2 実装中（タスク 2.3 完了）

**推奨コマンド:**
/sdd:implement-phase auth-feature 2.4

**理由:**
Phase 2のタスク2.4「認証トークン検証」が未完了です。
```

## 関連コマンド

- `/sdd:utils status` - 全タスクのステータス確認
