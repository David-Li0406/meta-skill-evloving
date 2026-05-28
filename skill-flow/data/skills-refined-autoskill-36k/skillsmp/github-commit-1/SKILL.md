---
name: github-commit
description: Replaces the work of recording changes to the repository following specific conventions. Typical use cases: (1) Batch staging and committing product code and tests after implementation, (2) Reliably recording design artifacts such as architectural diagrams or ADR drafts, (3) Managing automatic fix and retry processes when pre-commit hooks fail.
---

# GitHub Commit

作業の区切りで変更内容をリポジトリに記録する際に使用する。
このスキルでは、**すべての変更**をステージングし、規約に沿ったメッセージでコミットする手順を規定する。

> **Note:** 作業開始前またはコミット前に、必ず `github-checkout-feature-branch` を使用して適切な作業ブランチにいることを確認済みであること。
> （必要に応じて `activate_skill{name: "github-checkout-feature-branch"}` を実行する）

## 手順

1. **コミットの実行:**
   以下のコマンドを実行し、変更をステージングしてコミットする。
   `run_shell_command{command: "git add . && git commit -m \"<type>: <subject>\""}`

2. **エラー対応:**
   コミット時に pre-commit フックなどが実行され、エラーが発生した場合は、エラー内容を確認して修正を行う。
   修正後、再度手順1を実行する。

## コミットメッセージの規約

`<type>: <subject>` 形式で記述する。

### Type の例

- `feat`: 新機能の追加
- `fix`: バグ修正
- `docs`: ドキュメントの変更
- `style`: コードの意味に影響しない変更（空白、フォーマット、セミコロン欠落など）
- `refactor`: バグ修正も機能追加も行わないコード変更
- `perf`: パフォーマンスを向上させるコード変更
- `test`: テストの追加や修正
- `chore`: ビルドプロセスや補助ツールの変更（上記以外の変更）

### Subject の例

- `ユーザー登録機能を追加`
- `ログイン時の認証バグを修正`
- `READMEにセットアップ手順を追記`
