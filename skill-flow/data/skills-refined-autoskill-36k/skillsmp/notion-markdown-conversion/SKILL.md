---
name: notion-markdown-conversion
description: Converts Notion databases and pages to structured Markdown format using Notion MCP. Use when working with Notion data visualization, documentation, or exporting Notion content.
allowed-tools: mcp__Notion__notion-search, mcp__Notion__notion-fetch, Write, Read
---

# Notion to Markdown Conversion Skill

Notion MCPを使用してNotionのdatabaseやページを取得し、AI可読性の高いMarkdown形式に変換します。

## 対応タスク

- Notion databaseの全体構造をMarkdown化
- Database内のページ一覧をテーブル形式で出力
- 個別ページの詳細をMarkdown形式で出力
- Database schemaの可視化
- 検索結果をMarkdown形式で整形

## 利用可能なMCPツール

### データ取得
- `mcp__Notion__notion-search` - Notion全体を検索（semantic search）
- `mcp__Notion__notion-fetch` - 特定のページやdatabaseを取得

### データ書き込み（必要に応じて）
- `mcp__Notion__notion-create-pages` - 新規ページ作成
- `mcp__Notion__notion-update-page` - ページ更新

## Markdown変換パターン

### 1. Database構造のMarkdown化

```markdown
# Database: [Database Name]

## スキーマ

| プロパティ名 | タイプ | 説明 |
|------------|--------|------|
| Name | title | タイトルプロパティ |
| Status | select | ステータス選択 |
| Date | date | 日付 |

## ページ一覧

| Name | Status | Date | ... |
|------|--------|------|-----|
| ページ1 | 進行中 | 2026-01-06 | ... |
| ページ2 | 完了 | 2026-01-05 | ... |
```

### 2. 個別ページのMarkdown化

```markdown
# [Page Title]

## メタデータ
- **作成日**: 2026-01-06
- **最終更新**: 2026-01-06
- **作成者**: User Name
- **ステータス**: draft/current

## プロパティ
- **Status**: 進行中
- **Date**: 2026-01-06
- **Tags**: tag1, tag2

## コンテンツ

[ページの本文をNotion-flavored Markdownで表示]
```

### 3. 検索結果のMarkdown化

```markdown
## 検索結果: "{query}"

### ページ

| タイトル | タイプ | 最終更新 | URL |
|---------|--------|----------|-----|
| ... | ... | ... | ... |

### Databases

| タイトル | 説明 | URL |
|---------|------|-----|
| ... | ... | ... |
```

## データ取得ワークフロー

### Database全体の取得
1. `mcp__Notion__notion-fetch`でdatabase IDを指定して取得
2. Schemaとdata sourcesを解析
3. 各data sourceからページ一覧を取得
4. Markdown形式に変換

### ページ検索と取得
1. `mcp__Notion__notion-search`でキーワード検索
2. 検索結果からページURLまたはIDを抽出
3. `mcp__Notion__notion-fetch`で詳細取得
4. Markdown形式に変換

### 個別ページの詳細取得
1. ページURLまたはIDを指定
2. `mcp__Notion__notion-fetch`で取得
3. Notion-flavored Markdownをそのまま利用または整形

## 構造化ルール

1. **メタデータを先頭に配置** - 作成日、更新日、作成者など
2. **プロパティの明示** - Database propertiesを明確に表示
3. **null値の扱い** - 空のプロパティは`[未設定]`と表示
4. **日付の整形** - ISO形式から読みやすい形式に変換
5. **テーブルの活用** - 一覧データは必ずテーブル形式
6. **階層構造の維持** - 見出しレベルで情報の重要度を表現
7. **URLの保持** - 元のNotion URLを参照可能にする

## Notion特有の要素の扱い

### プロパティタイプ
- **title**: プレーンテキストとして表示
- **rich_text**: Markdownフォーマットを保持
- **number**: 数値として表示
- **select/multi_select**: タグまたはリストとして表示
- **date**: YYYY-MM-DD形式で表示
- **checkbox**: ✓/✗ または [x]/[ ] で表示
- **url**: Markdownリンク形式
- **email**: Markdownリンク形式
- **phone**: プレーンテキスト
- **files**: ファイル名とURLのリスト
- **people**: ユーザー名のリスト
- **relation**: 関連ページへのリンク
- **rollup**: 集計結果を表示
- **formula**: 計算結果を表示

### ブロック要素
- **paragraph**: 通常の段落
- **heading**: # ## ### で表現
- **bulleted_list**: - リスト
- **numbered_list**: 1. リスト
- **to_do**: - [ ] チェックリスト
- **toggle**: 折りたたみ可能セクション
- **quote**: > 引用
- **code**: ```言語 コードブロック
- **table**: Markdownテーブル
- **database**: Database参照

## 変換時の注意事項

1. **Notion-flavored Markdown**: Notionの拡張Markdown構文を保持
2. **カスタムタグの処理**: `<custom data-type="...">` タグの適切な変換
3. **プレースホルダーの扱い**: テンプレートのプレースホルダーを明示
4. **メンション**: @ユーザー、@ページ などを適切に表現
5. **URL抽出**: Notion URLから page ID を抽出可能
6. **Draft vs Published**: ページのステータスを明記

## URL形式

### ページURL
- 標準形式: `https://notion.so/workspace/Page-Title-{page-id}`
- ID抽出: 最後の32文字（ハイフン除く）がpage ID

### DatabaseURL
- 標準形式: `https://notion.so/workspace/{database-id}`
- View付き: `https://notion.so/workspace/{database-id}?v={view-id}`

## 使用例

### 例1: Database全体の取得
```
「Task ManagementデータベースをMarkdown形式で出力して」
→ Database fetch + Schema解析 + ページ一覧取得 + Markdown変換
```

### 例2: ページ検索と変換
```
「Notionで"ミーティング議事録"を検索してMarkdown化して」
→ Search + Fetch + Markdown変換
```

### 例3: 特定ページの詳細取得
```
「このNotionページをMarkdown形式で: https://notion.so/...」
→ Page fetch + Markdown変換
```

### 例4: Database内のページ一覧
```
「プロジェクトデータベースの全ページをテーブルで表示」
→ Database fetch + ページ一覧取得 + Markdownテーブル生成
```

## ベストプラクティス

1. **段階的取得**: まずDatabase schemaを取得してから詳細取得
2. **URLの活用**: Notion URLをそのまま渡せば自動でID抽出
3. **検索の活用**: タイトルが不明な場合はsearchから開始
4. **キャッシュ**: 取得したデータは適切にファイル保存
5. **バッチ処理**: 複数ページは並列取得で効率化

## 参考資料

- Notion MCP Server Documentation
- Notion-flavored Markdown Specification
- Notion API Reference
- Database Schema Types
