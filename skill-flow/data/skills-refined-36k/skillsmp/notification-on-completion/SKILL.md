---
name: notification-on-completion
description: Send desktop notification when Claude Code completes tasks or stops working
---

# Notification on Completion

タスクが完了したら、必ず `noti` コマンドで通知を送信してください。

## 実行タイミング

以下のタイミングで通知を送信:
- 複数ステップのタスクが完了した時
- エラーで停止した時
- ユーザーの入力待ちになる前

## 通知コマンド

```bash
noti "Claude Code: タスクが完了しました"
```

## 使用例

- ビルド完了時: `noti "ビルドが完了しました"`
- エラー発生時: `noti "エラーが発生しました"`
- 検索完了時: `noti "検索が完了しました"`
- 複数ファイルの編集完了時: `noti "ファイルの編集が完了しました"`

## 重要事項

- **必ず実行**: タスク完了時は必ず通知を送る
- **簡潔なメッセージ**: 何が完了したかを簡潔に伝える
- **日本語**: ユーザーは日本語を希望
