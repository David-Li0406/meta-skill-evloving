---
name: jira-markdown-conversion
description: Converts Jira issues and backlog data to structured Markdown format using Atlassian MCP. Use when working with Jira data visualization, documentation, or reporting.
allowed-tools: mcp__atlassian__getJiraIssue, mcp__atlassian__searchJiraIssuesUsingJql, mcp__atlassian__getVisibleJiraProjects, Write, Read
---

# Jira to Markdown Conversion Skill

Atlassian MCPを使用してJiraデータを取得し、AI可読性の高いMarkdown形式に変換します。

## 対応タスク

- Jira issueの詳細情報をMarkdownドキュメントに変換
- Jiraバックログ（未解決issue一覧）をMarkdownテーブルに変換
- Sprintの内容をMarkdown形式でドキュメント化
- 複数のissueを構造化されたMarkdownレポートに変換

## 環境情報

### Cloud ID
- **hadron.atlassian.net**: `f6e0f50a-4acf-4011-90fa-8fcc9b50cd86`

### 利用可能なMCPツール
- `mcp__atlassian__getJiraIssue` - 個別Issue詳細取得
- `mcp__atlassian__searchJiraIssuesUsingJql` - JQL検索
- `mcp__atlassian__getVisibleJiraProjects` - プロジェクト一覧取得

## Markdown変換パターン

### 1. Issue詳細のMarkdown化

```markdown
# [ISSUE-KEY] タイトル

## メタデータ
- **ステータス**: {status}
- **タイプ**: {issueType}
- **担当者**: {assignee or [未割り当て]}
- **優先度**: {priority or [未設定]}
- **作成日**: {created}
- **更新日**: {updated}

## 説明
{description or [未記入]}

## コメント
{comments}

## 添付ファイル
{attachments}
```

### 2. バックログのテーブル化

```markdown
## バックログ一覧

| キー | タイプ | サマリー | ステータス | 担当者 | 優先度 | 作成日 |
|------|--------|----------|------------|--------|--------|---------|
| SCRUM-1 | Feature | タスク 1 | Idea | [未割り当て] | [未設定] | 2026-01-06 |
| SCRUM-2 | タスク | タスク 2 | To Do | [未割り当て] | [未設定] | 2026-01-06 |
```

### 3. Sprint情報のMarkdown化

```markdown
## Sprint情報

- **名前**: SCRUM Sprint 0
- **状態**: active
- **開始日**: 2026-01-06
- **終了日**: 2026-01-20

### Sprint内のIssue

| キー | サマリー | ステータス | 担当者 |
|------|----------|------------|--------|
| ... | ... | ... | ... |
```

## データ取得ワークフロー

### バックログ取得
1. `mcp__atlassian__searchJiraIssuesUsingJql`を使用
2. JQL: `project = {PROJECT_KEY} AND resolution = Unresolved ORDER BY created DESC`
3. 取得フィールド: summary, status, issuetype, priority, created, assignee

### 個別Issue取得
1. `mcp__atlassian__getJiraIssue`を使用
2. issueIdOrKey: `{ISSUE_KEY}`
3. すべてのフィールドを取得

## 構造化ルール

1. **メタデータを先頭に配置** - 重要な情報を最初に表示
2. **未記入項目の明示** - `[未記入]`、`[未割り当て]`、`[未設定]`と明記
3. **日付の整形** - ISO形式から読みやすい形式に変換（YYYY-MM-DD）
4. **プレースホルダーと実データの区別** - 実データと説明文を明確に分離
5. **階層構造の維持** - 見出しレベルで情報の重要度を表現
6. **テーブルの活用** - 一覧データは必ずテーブル形式で表現

## 変換時の注意事項

- null値は`[未設定]`または`[未記入]`と表示
- 日本語と英語のフィールド名が混在する場合は、日本語を優先
- SprintフィールドはcustomField_10020として取得される
- Issue keyは必ずリンクまたは強調表示

## 使用例

### 例1: プロジェクトのバックログ取得
```
「SCRUMプロジェクトのバックログをMarkdownで出力して」
→ JQL検索 + Markdown変換
```

### 例2: 個別Issue詳細
```
「SCRUM-5の詳細をMarkdownで」
→ Issue取得 + Markdown変換
```

### 例3: Sprint内容の可視化
```
「Sprint 0の内容をまとめて」
→ Sprint検索 + Issue一覧取得 + Markdown変換
```

## 参考資料

- Atlassian MCP Server Documentation
- Jira REST API Reference
- JQL (Jira Query Language) Syntax
