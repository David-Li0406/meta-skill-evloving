---
name: development-workflow-skill
description: Use this skill when you need to create pull requests or follow a test-driven development cycle.
---

## Pull Request Creation

### 事前確認
- ユーザからマージ先のブランチを受け取ります。
- 現在開いているブランチ名に含まれる {大文字の英字列-数字}を Jira に紐つく {PROJECT-KEY} と認識します。

### 実行内容
- `git diff` で、現在のブランチとリモートのマージ先ブランチを比較し、変更の詳細を確認します（例: `this_branch` と `origin/main` を比較）。
- `gh pr create` でプルリクエストを作成します。
  - プルリクエストの内容は、すべて説明的にし、想定ターゲットの存在しない内容にしてください。

## Test-Driven Development Cycle

1. Red - Green - Refactor のサイクルで実装します。ただし、「TDD が適さないタスクである」と判断した場合は、DIRECT に実装して OK です。
   - Red: 仕様に則り、落ちるテストを書いてください。
   - Green: テストを通すことだけを考えた最小限の実装をおこなってください。
   - Refactor: テストを通すことだけではなく、コード品質向上をおこなってください。
     - 将来の変更や機能変更が容易にするための保守性の確保
     - コードの重複を排除したり、複雑さを取り除いてシンプルさの確保

2. 実装を終えたら、test と lint, 型チェック, semgrep を実施します。問題があれば修正します。
   - `docker compose exec {コンテナサービス名} bunx tsc --noEmit`
   - `docker compose exec {コンテナサービス名} bun run fix`
   - `docker compose exec {コンテナサービス名} test`
   - `docker compose run --rm semgrep semgrep <args...>`

## 参考情報
必要な内容を取捨選択し Read して参考にしてください。
- [Pull Request テンプレート](./references/PULL_REQUEST_TEMPLATE.md)
- [ドキュメント作成ガイドライン](../common/references/documents.md)
- [バックエンド開発ガイドライン](../common/references/backend.md)
- [フロントエンド開発ガイドライン](../common/references/frontend.md)
- [スキーマ駆動開発ガイドライン](../common/references/schema-db.md)
- [E2Eテストガイドライン](../common/references/e2e.md)