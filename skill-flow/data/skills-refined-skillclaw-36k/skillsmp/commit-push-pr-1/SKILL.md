---
name: commit-push-pr
description: コミット、プッシュ、PR作成を一括実行
allowed-tools: Bash(npm run fmt), Bash(npm run ts), Bash(git checkout --branch:*), Bash(git add:*), Bash(git status:*), Bash(git push:*), Bash(git commit:*), Bash(gh pr create:*)
---

## コンテキスト

- 現在のgit status: !`git status`
- 現在のgit diff（ステージ済み・未ステージの変更）: !`git diff HEAD`
- 現在のブランチ: !`git branch --show-current`

## タスク

上記の変更内容に基づいて以下を実行：
1. `npm run fmt` でコードをフォーマット
2. `npm run ts` で型チェック
3. mainブランチにいる場合は新しいブランチを作成
4. 適切なメッセージでコミットを作成
5. originにプッシュ
6. `gh pr create` でプルリクエストを作成
7. 複数のツールを1つのレスポンスで呼び出すこと。上記すべてを1つのメッセージで実行すること。他のツールを使ったり、他のことをしないこと。
