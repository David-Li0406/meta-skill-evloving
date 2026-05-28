---
name: manage-pr-comments
description: Use this skill when you need to read unresolved comments from GitHub PRs and resolve them automatically.
---

# Manage PR Comments

## Instructions

以下のステップに従って、GitHubプルリクエストから未対応のコメントを取得し、修正プランを作成し、未解決のレビューコメントを一括で解決します。

### 未解決のプルリクエストレビューコメントの取得

以下のコマンドを実行して、未解決のプルリクエストレビューコメントを取得します。

```
bash /プラグインルートパス/skills/manage-pr-comments/scripts/read-unresolved-pr-comments.sh 
```

### 修正プランの作成

取得した未解決コメントをもとに、修正プランを作成します。

- Exploreサブエージェントを使用して、未解決コメントの内容を分析します。
- Planサブエージェントを使用して、具体的な修正プランを策定します。

### 未解決レビューコメントの一括解決

以下のコマンドで未解決のレビューコメントを一括で解決します。

```
bash /プラグインルートパス/skills/manage-pr-comments/scripts/resolve-pr-comments.sh
```

各スレッドのResolve結果が表示されます。Issue comments（会話タブ）は元々Resolve機能がないため対象外です。