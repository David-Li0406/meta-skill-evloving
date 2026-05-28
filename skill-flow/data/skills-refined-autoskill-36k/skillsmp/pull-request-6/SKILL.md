---
name: pull-request
description: "Pull Request作成スキル。.github/PULL_REQUEST_TEMPLATE.mdに準拠した高品質なPRを作成。Use when: PR作成、Pull Request作成、変更内容のPR化を依頼された時。"
---

# Pull Request作成

`.github/PULL_REQUEST_TEMPLATE.md`のテンプレート形式に準拠した高品質なPull Requestを作成します。

## PR作成原則

1. **コミット履歴の分析**: ブランチのコミット履歴から変更内容を把握
2. **What/Why/Howの明確化**: 何を、なぜ、どのように変更したかを明示
3. **レビュアー視点**: レビュアーが理解しやすい構成と説明
4. **テンプレート準拠**: 既存のPRテンプレート形式に従う
5. **Issue連携**: 関連Issueを正確に参照

## PR概要の構成要素

| 要素             | 必須/任意 | 説明                         |
| ---------------- | --------- | ---------------------------- |
| Summary          | 必須      | PRの目的と背景を2-3文で説明  |
| Type of Change   | 必須      | 変更種別を選択               |
| Related Issues   | 必須      | 関連Issue番号を記載          |
| Changes          | 必須      | 変更内容を詳細に列挙         |
| Test Plan        | 必須      | テスト方法と確認事項         |
| Screenshots      | 任意      | UI変更時のスクリーンショット |
| Additional Notes | 任意      | その他の注意事項             |

## What/Why/How の明確化

| 要素                  | 記述場所         | 説明                                   |
| --------------------- | ---------------- | -------------------------------------- |
| **What（何を）**      | Summary, Changes | 何を変更したか                         |
| **Why（なぜ）**       | Summary          | なぜ変更したか（目的、背景、効果）     |
| **How（どのように）** | Changes          | どのように変更したか（実装方法、詳細） |

## PR作成手順

### 1. ブランチとコミット履歴を確認

```bash
# 現在のブランチを確認
git branch --show-current

# ベースブランチとの差分コミットを確認
git log main...HEAD --oneline

# 変更ファイルを確認
git diff main...HEAD --name-only

# 変更内容の詳細を確認
git diff main...HEAD
```

### 2. セルフレビュー（ブランチ差分チェック）

**PR作成前の必須プロセス**として、自分の変更内容を客観的に確認します。

```bash
# self-review スキルを使用
"実装が完了しました。セルフレビューをお願いします"
```

詳細な手順とチェックリストは [self-review/SKILL.md](../self-review/SKILL.md) を参照してください。

### 3. Summary を生成

**目的**: PRの「何を」「なぜ」「効果」を2-3文で説明

**生成方法**:

1. コミットメッセージのtype（feat, fix, docsなど）を確認
2. 複数のコミットから共通の目的を抽出
3. Issueの説明文を参考に背景を記述
4. 2-3文で簡潔にまとめる

**例**:

```markdown
## Summary

シェルスクリプトの品質を保証するため、shellcheck と shfmt を使用したリンティング環境を構築します。これにより、バグの早期発見とコードスタイルの統一が可能になります。
```

### 4. Type of Change を選択

変更の性質に応じて適切な種別を選択:

- Bug fix (non-breaking change which fixes an issue)
- New feature (non-breaking change which adds functionality)
- Breaking change (fix or feature that would cause existing functionality to not work as expected)
- Documentation update
- Refactoring (no functional changes)
- Performance improvement
- Test update

### 5. Related Issues を記載

Issue番号を正確に記載:

- `Closes #XXX`: このPRで解決するIssue（マージ時に自動クローズ）
- `Fixes #XXX`: バグ修正の場合
- `Related to #YYY`: 関連するが自動クローズしないIssue

**例**:

```markdown
## Related Issues

Closes #20
Related to #15
```

### 6. Changes を構成

**目的**: 「何を」「どのように」変更したかを詳細に説明

**生成方法**:

1. `git diff --name-only` でファイル一覧を取得
2. 関連ファイルをグループ化（例: GitHub Actions, Docker, Docs）
3. 各グループで変更内容を階層的に記述

**例**:

```markdown
## Changes

- GitHub Actions ワークフロー (.github/workflows/shell-linting.yml) を追加

  - PR と main ブランチへのプッシュで自動実行
  - shellcheck による静的解析
  - shfmt によるフォーマットチェック

- Docker 環境を追加

  - Dockerfile.shell-linting: shellcheck と shfmt をインストール
  - docker-compose.shell-linting.yml: 簡単に実行可能な設定

- ドキュメントを追加
  - .claude/skills/shell-linting/SKILL.md: 詳細なルールとベストプラクティス
  - docs/shell-linting.md: ユーザー向けガイド
```

### 7. Test Plan を生成

**目的**: テスト方法と確認事項を明確にする

**生成方法**:

1. Issueの受け入れ基準をTest Planに変換
2. テストコミットからテスト項目を抽出
3. チェックリスト形式で記述（実施済みは`[x]`、未実施は`[ ]`）

**例**:

```markdown
## Test Plan

- [x] shellcheck が全スクリプトでエラーなく実行される
- [x] shfmt のフォーマットチェックが通る
- [ ] GitHub Actions ワークフローが正常に動作する
- [ ] Docker 環境でリンティングが実行できる
```

### 8. Checklist を確認

PR提出前に以下を確認:

- コードはプロジェクトのスタイルガイドに従っている
- 自己レビューを実施した
- コメントを適切に追加した（特に複雑な部分）
- 関連するドキュメントを更新した
- 変更によって新しい警告は発生していない
- テストを追加/更新した
- すべてのテストが通過する

### 9. PR作成コマンドを実行

```bash
# PRを作成（タイトルと本文を指定）
gh pr create --title "feat: add shell linting environment" --body "$(cat <<'EOF'
## Summary

シェルスクリプトの品質を保証するため、shellcheck と shfmt を使用したリンティング環境を構築します。これにより、バグの早期発見とコードスタイルの統一が可能になります。

## Type of Change

- [x] New feature (non-breaking change which adds functionality)

## Related Issues

Closes #20

## Changes

- GitHub Actions ワークフロー (.github/workflows/shell-linting.yml) を追加
  - PR と main ブランチへのプッシュで自動実行
  - shellcheck による静的解析
  - shfmt によるフォーマットチェック

- Docker 環境を追加
  - Dockerfile.shell-linting: shellcheck と shfmt をインストール
  - docker-compose.shell-linting.yml: 簡単に実行可能な設定

## Test Plan

- [x] shellcheck が全スクリプトでエラーなく実行される
- [x] shfmt のフォーマットチェックが通る
- [ ] GitHub Actions ワークフローが正常に動作する
- [ ] Docker 環境でリンティングが実行できる

## Checklist

- [x] コードはプロジェクトのスタイルガイドに従っています
- [x] 自己レビューを実施しました
- [x] 関連するドキュメントを更新しました
- [x] テストを追加/更新しました

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

## PR品質チェックポイント

| 項目                | チェック内容                                  |
| ------------------- | --------------------------------------------- |
| **タイトル**        | Conventional Commits形式（type: description） |
| **Summary**         | 目的と背景が2-3文で明確                       |
| **Type of Change**  | 適切な変更種別を選択                          |
| **Related Issues**  | Issue番号が正確（Closes/Fixes/Related to）    |
| **Changes**         | 変更内容が階層的で詳細                        |
| **Test Plan**       | テスト方法が具体的でチェックリスト形式        |
| **Checklist**       | 全項目を確認済み                              |
| **Breaking Change** | 破壊的変更がある場合は明記                    |

## 良い例・悪い例

### 良い例

```markdown
## Summary

シェルスクリプトの品質を保証するため、shellcheck と shfmt を使用したリンティング環境を構築します。これにより、バグの早期発見とコードスタイルの統一が可能になります。

## Type of Change

- [x] New feature (non-breaking change which adds functionality)

## Related Issues

Closes #20

## Changes

- GitHub Actions ワークフロー (.github/workflows/shell-linting.yml) を追加

  - PR と main ブランチへのプッシュで自動実行
  - shellcheck による静的解析
  - shfmt によるフォーマットチェック

- Docker 環境を追加

  - Dockerfile.shell-linting: shellcheck と shfmt をインストール
  - docker-compose.shell-linting.yml: 簡単に実行可能な設定

- ドキュメントを追加
  - .claude/skills/shell-linting/SKILL.md: 詳細なルールとベストプラクティス
  - docs/shell-linting.md: ユーザー向けガイド

## Test Plan

- [x] shellcheck が全スクリプトでエラーなく実行される
- [x] shfmt のフォーマットチェックが通る
- [ ] GitHub Actions ワークフローが正常に動作する
- [ ] Docker 環境でリンティングが実行できる

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**なぜ良いか**:

- Summary で目的と効果が明確
- Type of Change が適切に選択されている
- Related Issues で正確にIssueを参照
- Changes が階層的で詳細
- Test Plan が具体的でチェックリスト形式

### 悪い例

```markdown
Add shell linting

Added some files for shell linting.
```

**なぜ悪いか**:

- Summary が不明確（なぜ必要か、効果は何か）
- Type of Change が選択されていない
- Related Issues が記載されていない
- Changes が具体的でない（どのファイル？何を追加？）
- Test Plan が存在しない

## 他のスキルとの連携

### commit-message スキルとの連携

- PRタイトルはConventional Commits形式に準拠
- コミットメッセージからSummaryを生成
- 各コミットのbodyからChangesを構成

### github-issue スキルとの連携

- Issueの受け入れ基準をTest Planに変換
- Issueの説明文をSummaryの背景に活用
- Related Issuesで正確にIssueを参照

### code-review スキルとの連携

- レビュアーが確認すべき点をChangesに明記
- 破壊的変更やリスクをAdditional Notesに記載

## 実際の使用シナリオ

### シナリオ1: 新機能追加のPR

```bash
# ブランチ: feature/add-user-auth
# コミット履歴:
# - feat: JWT認証ミドルウェアを追加
# - feat: ユーザーログインエンドポイントを追加
# - test: 認証テストを追加
# - docs: APIドキュメントを更新
```

**生成されるPR**:

```markdown
## Summary

ユーザー認証機能を追加し、JWTベースの認証を実装します。これにより、セキュアなAPIアクセスが可能になります。

## Type of Change

- [x] New feature (non-breaking change which adds functionality)

## Related Issues

Closes #30

## Changes

- 認証ミドルウェアを追加 (middleware/auth.js)

  - JWTトークンの検証
  - 認証エラーハンドリング

- ログインエンドポイントを追加 (routes/auth.js)

  - POST /api/login: ユーザー認証とトークン発行

- テストを追加 (tests/auth.test.js)

  - 認証成功・失敗のテストケース
  - トークン検証のテストケース

- APIドキュメントを更新 (docs/api.md)
  - 認証エンドポイントの説明
  - 認証ヘッダーの使用方法

## Test Plan

- [x] 認証ミドルウェアのテストが通る
- [x] ログインエンドポイントのテストが通る
- [ ] CI/CDパイプラインが成功する

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### シナリオ2: バグ修正のPR

```bash
# ブランチ: fix/memory-leak
# コミット履歴:
# - fix: データ処理のメモリリークを修正
# - test: メモリリーク回帰テストを追加
```

**生成されるPR**:

```markdown
## Summary

データ処理におけるメモリリークを修正します。リソースが適切に解放されずメモリ使用量が増加していた問題を解決します。

## Type of Change

- [x] Bug fix (non-breaking change which fixes an issue)

## Related Issues

Fixes #45

## Changes

- データ処理のメモリリークを修正 (services/data-processor.js)

  - リソース解放処理を追加
  - try-finallyブロックで確実にクリーンアップ

- 回帰テストを追加 (tests/data-processor.test.js)
  - メモリリーク検出テスト

## Test Plan

- [x] メモリリーク回帰テストが通る
- [x] 既存のテストが全て通る
- [ ] 本番環境でメモリ使用量が安定する

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### シナリオ3: ドキュメント更新のPR

```bash
# ブランチ: docs/pr-guidelines
# コミット履歴:
# - docs: PR作成スキルドキュメントを追加
# - docs: AGENTS.mdにPRガイドラインを追加
# - docs: PRテンプレートを更新
```

**生成されるPR**:

```markdown
## Summary

Pull Request作成時の適切な概要作成ガイドラインを整備します。AIエージェントが高品質なPR概要を自動生成できるようになります。

## Type of Change

- [x] Documentation update

## Related Issues

Closes #24

## Changes

- PR作成スキルを追加 (.claude/skills/pull-request/SKILL.md)

  - フォーマット定義
  - 良い例・悪い例
  - AIエージェント向けガイド

- AGENTS.mdを更新

  - PR作成ガイドラインへの参照を追加

- PRテンプレートを更新 (.github/PULL_REQUEST_TEMPLATE.md)
  - Summary, Changes, Test Planセクションを明確化

## Test Plan

- [x] ドキュメントが読みやすい
- [x] AIエージェントがガイドラインを理解できる
- [ ] 実際にこのガイドラインでPRを作成できる

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## 重要な注意事項

1. **コミット履歴の分析**: PRを作成する前に必ずコミット履歴を確認
2. **What/Why/Howの明確化**: レビュアーが理解しやすい構成
3. **テンプレート準拠**: 既存のPRテンプレート形式に従う
4. **Issue連携**: Related Issuesで正確にIssueを参照
5. **Claude Code署名**: PR本文の末尾に署名を追加
6. **チェックリスト確認**: 提出前に全項目をチェック
