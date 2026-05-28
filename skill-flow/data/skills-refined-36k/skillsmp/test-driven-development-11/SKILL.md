---
name: test-driven-development
description: "TDD（テスト駆動開発）スキル。Red-Green-Refactorサイクルに基づく開発支援。Use when: 開発を依頼された時。"
---

# テスト駆動開発（TDD）

Red-Green-Refactorサイクルに基づくテスト駆動開発を支援します。

## TDDサイクル

| フェーズ | 説明                       | 実施内容                                             |
| -------- | -------------------------- | ---------------------------------------------------- |
| Red      | 失敗するテストを書く       | 要件を満たすテストケースを作成し、実行して失敗を確認 |
| Green    | テストを通す最小限のコード | テストが通る最小限の実装を追加                       |
| Refactor | コードを改善               | 重複排除、可読性向上、設計改善を実施                 |

## TDD原則

1. **テストファースト**: 実装前に必ずテストを書く
2. **最小実装**: テストを通す最小限のコードのみを書く
3. **リファクタリング**: グリーンになった後、コード品質を改善
4. **小さなステップ**: 一度に1つの機能に集中
5. **継続的な実行**: テストを頻繁に実行し、即座にフィードバック

## 開発手順

### 1. Red（失敗するテストを書く）

- 要件を理解し、期待する振る舞いを定義
- テストケースを作成（エッジケース、境界値も考慮）
- テストを実行して失敗を確認

  ```bash
  # プロジェクト固有のテストコマンドを実行

  # Shell Script Testing (bats)
  docker compose run shell-dev bats tests/

  # 特定のテストファイルのみ実行
  docker compose run shell-dev bats tests/example.bats
  ```

- 失敗理由が意図通りであることを確認

**テストファイルの扱い**:

- **コード開発**: 作成したテストファイルは最終成果物として残す（例: tests/\*.bats）
- **ドキュメント開発**: 検証用のテストチェックリスト（TEST.md など）は、Greenフェーズ完了後に以下のいずれかを実施
  - 不要な場合は削除する
  - 継続的な品質確認が必要な場合は残す
  - 実装ガイドとして有用な場合は本体ドキュメントに統合する

### 2. Green（テストを通す）

- テストを通す最小限のコードを実装
- ハードコードや単純な実装でも可
- テストが全て通ることを確認

  ```bash
  # Shell Script Testing (bats)
  docker compose run shell-dev bats tests/
  ```

- 新しいテストで既存テストが壊れていないか確認

### 3. Refactor（リファクタリング）

#### 3.1. コード改善

- コードの重複を排除
- 命名を改善
- 設計パターンの適用
- パフォーマンス最適化

#### 3.2. ローカルテスト実行

- テストが全て通り続けることを確認

  ```bash
  # Shell Script Testing (bats)
  docker compose run shell-dev bats tests/
  ```

#### 3.3. ローカルLint/Format実行

- Lintチェックを実行して警告がないことを確認

  ```bash
  # Shell Script Linting
  docker compose run shell-dev lint-shell
  ```

- Lintで問題がある場合には、コードフォーマットを適用する、個別に修正するなどして対応する

  ```bash
  # Shell Script Formatting (check)
  docker compose run shell-dev shfmt -d -i 2 .

  # Shell Script Formatting (apply)
  docker compose run shell-dev shfmt -i 2 -w .
  ```

- GitHub Actionsワークフローを修正した場合はActionLintを実行

  ```bash
  # GitHub Actions Linting
  docker compose run shell-dev actionlint
  ```

#### 3.4. Git Commit & Push

- すべてのローカルチェックが通ったら、変更をコミット・プッシュ

  ```bash
  git add .
  git commit -m "type: description"
  git push
  ```

#### 3.5. Pull Request 作成

- Pull Requestを作成（詳細は [.claude/skills/pull-request/SKILL.md](../pull-request/SKILL.md) を参照）

  ```bash
  gh pr create --title "type: description" --body "..."
  ```

#### 3.6. CI確認

- Pull Request作成後、GitHubでCI/CDパイプラインが自動実行される
- 以下のチェックが全て成功していることを確認:
  - **Actionlint**: GitHub Actions ワークフローファイルの構文チェック
  - **ShellCheck + shfmt**: シェルスクリプトの静的解析とフォーマットチェック
  - **Test**: プロジェクト固有のテスト実行
- CIが失敗した場合:
  1. PRページでログを確認してエラー原因を特定
  2. ローカルで同じコマンドを実行して再現
  3. 修正後、コミット・プッシュしてCIが再実行されるのを確認

## テスト品質チェックポイント

| 項目       | チェック内容                                 |
| ---------- | -------------------------------------------- |
| カバレッジ | 重要なパス、エッジケース、エラーケースを網羅 |
| 独立性     | テスト間の依存関係がない                     |
| 明確性     | テストの意図が明確で可読性が高い             |
| 速度       | テストが高速に実行できる                     |
| 信頼性     | テストが安定して同じ結果を返す               |

## 出力形式

### Red フェーズ

- 実装する機能の要件説明
- 作成したテストコード
- テスト実行結果（失敗の確認）

### Green フェーズ

- 実装したコード
- テスト実行結果（成功の確認）
- 実装の説明

### Refactor フェーズ

- リファクタリング内容の説明
- 改善後のコード
- ローカルテスト実行結果（引き続き成功の確認）
- ローカルLint/Formatチェック結果（全て通過）
- Git Commit & Push の実行
- Pull Request 作成
- CI結果の確認（PR作成後に自動実行、全てのチェックが成功）
- 改善のポイント

## GitHub Actions CI

プロジェクトでは以下のCI/CDチェックが自動実行されます:

- **Actionlint**: GitHub Actions ワークフローファイルの構文チェック ([actionlint.yml](.github/workflows/actionlint.yml))
- **ShellCheck + shfmt**: シェルスクリプトの静的解析とフォーマットチェック ([ci.yml](.github/workflows/ci.yml))
- **Test**: プロジェクト固有のテスト実行 ([ci.yml](.github/workflows/ci.yml))

CI/CDパイプラインのURL: `https://github.com/{owner}/{repo}/actions`
