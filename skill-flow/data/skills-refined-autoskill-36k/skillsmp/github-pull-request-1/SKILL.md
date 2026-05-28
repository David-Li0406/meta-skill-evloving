---
name: github-pull-request
description: Replaces the entire process from creating and managing pull requests to final verification before merging. Typical use cases: (1) Synchronizing with the base branch, checking for conflicts, and automatic rebasing, (2) Creating titles based on conventions and detailed bodies including purpose, change summary, and verification methods, (3) Managing PRs through review feedback cycles and phase promotions based on dependencies.
---

# プルリクエストの管理 (PR Protocol)

1. **変更のコミット (Commit):**
   PR作成前に、未コミットの変更がある場合は `github-commit` スキルを呼び出して変更をコミットする。
   `activate_skill{name: "github-commit"}`

2. **既存PRの確認:**
   重複を防ぐため、`list_pull_requests` で関連する既存PRがないか確認する。

3. **Baseブランチとの同期と競合チェック (Sync & Conflict Check):**
   PRを作成する前に、マージ先となる `base` ブランチの最新状態を取り込み、コンフリクトがないか確認する。
   `run_shell_command{command: "git pull --rebase origin <base>"}`
   - **コンフリクトが発生した場合:**
     手動で解消し、コミット（またはrebase continue）を行ってから次の手順へ進む。

4. **新規作成 (Creation):**
   `create_pull_request` を実行する際は、以下のテンプレートを参照して `title` と `body` を指定する。
   **`head` (作業ブランチ) と `base` (マージ先) を必ず明示的に指定すること。**
   PR作成前に必ず思考プロセス内でテンプレートを埋め、**独自の要約や省略をせず**に `body` パラメータへ指定すること。

   `create_pull_request --title "<以下のテンプレートを参照>" --body "<以下のテンプレートを参照>" --head "<head>" --base "<base>"`

**PR Title テンプレート:**

```markdown
<type>(<scope>): <subject>
```

**PR Body テンプレート:**

```markdown
## 目的 (Goal)

<!-- なぜこの変更が必要か（背景とアウトカム） -->

## 変更の概要 (Summary)

<!-- 何をどのように変更したか -->

## 関連Issue (References)

Closes #<Issue番号>

## 検証方法 (Verification)

<!-- 実施したテストや動作確認の手順と結果（ログ等） -->

- [ ] Unit Test:
- [ ] Manual Check:
```
