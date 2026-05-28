---
name: github-resource-access
description: Use when accessing GitHub resources such as issues, PRs, repositories, or secrets
---

# GitHub Resource Access

## Overview

GitHub上のリソースへのアクセスルール。**gh CLIを使用し、読み取りは自由、変更は指示必須**。

## When to Use

- Issue/PR/リポジトリ情報を取得・変更する場面
- GitHub上のリソースにアクセスしたいと思った時
- 「ついでに」GitHub上の何かを変更したくなった時

## Core Rules

```
1. GitHub リソースへのアクセスには gh CLI を使用せよ
2. 読み取り = 自由
3. 変更 = 明示的指示が必要
```

## Quick Reference

| 操作種別 | 許可 | gh CLI コマンド例 |
|---------|------|------------------|
| 読み取り | 常に可 | `gh issue view`, `gh pr list`, `gh repo view`, `gh secret list` |
| 変更 | 指示必須 | `gh issue create`, `gh pr create`, `gh issue comment`, `gh secret set` |

**変更操作の定義:**
- Issue/PR の作成・更新・クローズ
- コメントの投稿
- ラベル・アサインの変更
- Secretsの設定

## Decision Flow

```
GitHubリソースにアクセスしたい
  ↓
gh CLI を使用せよ
  ↓
読み取り操作か？ → Yes → 実行可
  ↓ No
ユーザーから明示的な指示があるか？ → Yes → 実行可
  ↓ No
実行禁止。ユーザーに提案せよ
```

## Red Flags

以下の思考が浮かんだら**実行禁止**:

- 「ついでにラベルを付けておこう」
- 「参照リンクをコメントしておくと便利そう」
- 「Issueをクローズしておこう」
- 「関連PRにメンションしておこう」

**代わりに:** ユーザーに「〜しましょうか？」と提案せよ。

## Exceptions

以下のコマンドは**変更操作がタスクの目的**なので許可:
- `/create-pr`, `/issue:create-pr` - PR作成
- `/issue:define-requirement` - コメント投稿
- `/setup-release` - Secrets設定

## Common Mistakes

| 誤り | 正しい対応 |
|------|-----------|
| 調査中に見つけた情報をコメント追加 | ユーザーに提案して許可を待つ |
| 作業完了後に自動でIssueクローズ | ユーザーに報告し指示を待つ |
| 整理のためラベルを追加 | ユーザーに提案して許可を待つ |
