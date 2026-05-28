---
name: coderabbit-review-flow
description: CodeRabbitAIのPRレビューコメントを取得し、指摘事項を修正するワークフロー。ユーザーが「CodeRabbitのコメントを修正して」と言った場合にこのスキルを使用する。
---

# CodeRabbit Review Flow Skill

CodeRabbitAIのPRレビューコメントを取得し、指摘事項を修正するためのワークフロー。

## When to Use

- CodeRabbitのレビューコメントを確認したい場合
- CodeRabbitの指摘事項を修正したい場合
- PRのレビューステータスを確認したい場合
- ユーザーが「CodeRabbitのコメントを修正して」と依頼した場合

## Workflow

### Step 1: PRのレビューコメントを取得

GitHub CLIを使用してCodeRabbitのレビューコメントを取得する。

```bash
# PR番号を取得
PR_NUMBER=$(gh pr view --json number -q '.number')

# レビューコメント（コード行に対するコメント）を取得
gh api repos/:owner/:repo/pulls/$PR_NUMBER/comments \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]") | {id, path, line, created_at, body}]'

# PRコメント（全体に対するコメント）を取得
gh pr view $PR_NUMBER --comments --json comments \
  --jq '.comments[] | select(.author.login == "coderabbitai[bot]")'
```

**注意**: PRコメントとレビューコメントは別のAPIエンドポイント。

| 種類 | 説明 | API |
|------|------|-----|
| PRコメント | PR全体に対するコメント（サマリーなど） | `gh pr view --comments` |
| レビューコメント | 特定のコード行に対するコメント | `gh api .../pulls/.../comments` |

### Step 2: コメントの分類

取得したコメントを以下の3カテゴリに分類：

| カテゴリ | 判断基準 | 対応 |
|----------|----------|------|
| **自動修正可能** | 明確な修正指示、`Prompt for AI Agents`セクションあり | 自動で修正開始 |
| **ユーザー判断必要** | 設計判断、複数の選択肢、breaking change | ユーザーに確認 |
| **スキップ** | `✅ Addressed`マークあり、情報提供のみ | 対応不要 |

#### 自動修正可能の判断基準

以下の条件を満たす場合は自動修正可能：

1. **「Prompt for AI Agents」セクション**がある
2. **具体的なコード修正案**（diff形式）が提示されている
3. **タイポ・フォーマット**の指摘
4. **未使用import/変数**の削除
5. **型の追加・修正**

#### ユーザー判断が必要なケース

以下の場合はユーザーに確認を求める：

1. **設計変更**（アーキテクチャ、API設計）
2. **複数の解決策**が提示されている
3. **Breaking change**の可能性
4. **ビジネスロジック**に関わる変更
5. **パフォーマンス vs 可読性**のトレードオフ

### Step 3: ユーザーへの一覧提示

修正が必要なコメントを整理して提示：

```markdown
## CodeRabbit レビュー結果

### 自動修正予定（承認後に実行）
1. **src/app/api/route.ts:42** - 未使用importの削除
2. **src/components/Button.tsx:15** - 型の追加

### ユーザー判断が必要
1. **src/services/auth.ts:28** - 認証フローの変更提案
   - 選択肢A: セッションベース認証に変更
   - 選択肢B: 現状のJWT認証を維持
   → どちらを選択しますか？

### 対応済み/スキップ
- **src/utils/helper.ts:10** - ✅ Addressed
```

**ユーザー判断が不要な場合**：自動で修正を開始
**ユーザー判断が必要な場合**：ユーザーの回答を待つ

### Step 4: 修正の実装

CodeRabbitのコメントには通常、修正のヒントが含まれている：

#### 「Prompt for AI Agents」セクション

```markdown
**🤖 Prompt for AI Agents**
In file `src/example.ts` at line 42, replace the synchronous call with...
```

このセクションの指示に従って修正する。

#### 「Suggested fix」または「Committable suggestion」

```diff
- const result = await fetchData();
+ const result = await fetchData().catch(handleError);
```

diff形式で提示されている場合は、そのまま適用する。

### Step 5: コミットとプッシュ

修正をコミットしてプッシュすると、CodeRabbitが自動的に再レビューを実行する。

```bash
git add .
git commit -m "fix: CodeRabbitレビュー指摘事項の修正

- [修正内容1]
- [修正内容2]

🤖 Generated with [Claude Code](https://claude.com/claude-code)"

git push
```

CodeRabbitは対応されたコメントに「Addressed」マークを自動的に付与する。

## Quick Commands

### 現在のPRのCodeRabbitコメントを一覧表示

```bash
PR_NUMBER=$(gh pr view --json number -q '.number')
gh api repos/:owner/:repo/pulls/$PR_NUMBER/comments \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]") | {path, line, body}]'
```

### 未対応のコメントのみを抽出

```bash
gh api repos/:owner/:repo/pulls/$PR_NUMBER/comments \
  --jq '[.[] | select(.user.login == "coderabbitai[bot]") | select(.body | contains("✅ Addressed") | not) | {path, line, body}]'
```

### CodeRabbitサマリーを取得

```bash
gh pr view $PR_NUMBER --comments --json comments \
  --jq '.comments[] | select(.author.login == "coderabbitai[bot]") | .body' | head -100
```

## Comment Structure

### 重要度マーク

| マーク | 重要度 | 対応方針 |
|--------|--------|----------|
| 🔴 Critical | 必ず修正 | セキュリティ、データ損失リスク |
| 🟠 Major | 修正推奨 | バグ、パフォーマンス問題 |
| 🟡 Minor | 可能なら修正 | コードスタイル、リファクタリング |
| ✅ Addressed | 対応済み | スキップ |

## Troubleshooting

### コメントが取得できない場合

```bash
# 認証状態を確認
gh auth status

# リポジトリへのアクセス権を確認
gh repo view
```

### PR番号が不明な場合

```bash
# 現在のブランチに関連するPRを検索
gh pr list --head $(git branch --show-current)

# または現在のブランチのPRを表示
gh pr view
```

### CodeRabbitのレビューがない

- PRを作成/更新してから5-10分待つ
- CodeRabbitがリポジトリに設定されているか確認
- ドラフトPRの場合、レビューがスキップされる設定の可能性
