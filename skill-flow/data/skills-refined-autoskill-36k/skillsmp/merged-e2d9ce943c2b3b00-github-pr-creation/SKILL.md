---
name: github-pr-creation
description: Use this skill to automate the creation of GitHub Pull Requests after changes have been committed and pushed.
---

# GitHub Pull Request Creation Workflow

このスキルは、GitHubのプルリクエスト作成に必要な一連のワークフローを自動化します。

## When to Use

以下の状況でこのスキルを使用します。

- ユーザーが変更を push した後、PR を作成したい時
- ユーザーが機能実装やタスクを完了し、PR を出したい時
- ユーザーが「PR作って」「プルリクエスト出して」などと言及した時

## Prerequisites

- ブランチが作成済み
- 変更がコミット済み
- 変更がリモートに push 済み

上記が満たされていない場合、Git 操作を完了させるための手順を確認してください。

## Procedure

### 1. 変更内容の確認

現在の状態を確認します：

```bash
git status  # 変更されたファイルを確認
git diff    # 変更内容の差分を確認
```

### 2. 事前準備とチェック

コミット前に必要なチェックを実行します：

1. リポジトリルートの`CLAUDE.md`を確認し、プロジェクト固有の要件を確認
2. テスト、リンター、ビルドステップが記載されている場合は実行
3. エラーや失敗がある場合は、先に解決してから進める

### 3. 変更のステージングとコミット

**重要**：ファイルのステージングは必ず明示的なパスで行います：

```bash
# ❌ 絶対に使用しない
git add .
git add -A

# ✅ 正しい方法
git add path/to/file1.txt path/to/file2.txt path/to/file3.txt
```

コミットメッセージは以下の形式で作成します：

```bash
git commit -m "$(cat <<'EOF'
<変更の簡潔な説明>

<詳細な説明（必要に応じて）>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### 4. リモートへのプッシュ

現在のブランチをoriginにプッシュします：

```bash
git push -u origin <branch-name>
```

リモートにブランチが存在しない場合は自動的に作成されます。

### 5. PR 作成

PRテンプレートを検出し、存在する場合はそれを基にPRを作成します。テンプレートが存在しない場合は以下の構造で作成します：

```markdown
## 概要
<変更の簡潔な説明を1-3個の箇条書きで>

## 変更内容
<主な変更点のリスト>

## テスト
<変更がどのようにテストされたか（該当する場合）>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

PRを作成：

```bash
gh pr create --title "<PRのタイトル>" --body "$(cat <<'EOF'
<PR本文の内容>
EOF
)"
```

作成後、PR URLをユーザーに返します。

## Title and Description Guidelines

- タイトルはタスクと実装内容を要約した自然言語の文にします。
- Body (description) は以下のフォーマットで日本語の内容を記述します。

```markdown
## What

- 変更内容の詳細
- 技術的な解説(など)

## Why

- 変更の背景
- 実装の意図 (など)
```

## Important Notes

1. **準備ステップをスキップしない**：CLAUDE.mdに記載された要件は必ず実行
2. **テストやチェックが失敗したら進まない**：失敗を解決してから次に進む
3. **明示的なファイルパスでステージング**：`git add .`や`git add -A`は絶対に使用しない
4. **日本語でコミュニケーション**：特に指定が無い限り、ユーザーとのやり取りは日本語で行う
5. **不明な点があれば確認**：どのステップでも不明な点があれば、ユーザーに確認を取る

## Error Handling

- コマンドが失敗した場合は、特に指定が無い限り日本語でエラーメッセージをユーザーに説明
- 次のステップに進む前に、問題を解決するための提案を提示
- 必要に応じて、ユーザーに追加の情報や確認を求める