# status - タスクステータス表示

## 実行内容

sdd-webappのMCPツールを使用して全タスクのステータスを取得・表示する。

## 手順

1. `sdd_webapp_get_status` MCPツールを呼び出し
2. 結果を整形して表示

## 出力例

```
## SDDタスク一覧

| タスク | ステータス | Phase進捗 | 次のコマンド |
|--------|-----------|----------|-------------|
| auth-feature | 進行中 | Phase 2 (3/5) | /sdd:implement-phase auth-feature 2.4 |
| refactor-api | 未着手 | - | /sdd:init-task |

💡 詳細はsdd-webappダッシュボードで確認できます
```

## 関連コマンド

- `/sdd:utils next [taskname]` - 特定タスクの次ステップ
