# SKILL.md生成用テンプレート

SKILL.mdを生成する際に、このテンプレートを参照する。

## テンプレート

```yaml
---
name: {library}
description: |
  Provides documentation for {Library}.
  Use when working with code that imports "{package-name}", "{related-exports}", or any "{package-prefix}-*" packages.
  Use when the user asks about {Library} or shows code with {Library} imports.
  Can also be invoked directly with "{Library}", "{日本語キーワード}".
context: fork
agent: Explore
allowed-tools: WebFetch, WebSearch, Read
---

# {Library} Documentation

## Your Task

ユーザーの質問に対して、ドキュメントを調査して回答してください。

**質問:** $ARGUMENTS

## Instructions

1. **references/llms.md を読む**
   - 質問に関連するセクションとURLを特定

2. **WebFetchで詳細取得**
   - 関連するURLをWebFetchで取得
   - 必要な情報を抽出

3. **回答を生成**
   - 具体的なコード例を含める
   - 参照したURLを明記

## Reference

ドキュメント構造は [references/llms.md](references/llms.md) を参照。
```

## プレースホルダー

| プレースホルダー | 説明 | 例 |
|------------------|------|-----|
| `{library}` | スキル名（小文字、ハイフン区切り） | `tanstack-query` |
| `{Library}` | ライブラリの表示名 | `TanStack Query` |
| `{package-name}` | メインパッケージ名 | `@tanstack/react-query` |
| `{related-exports}` | 関連するエクスポート名 | `useQuery`, `useMutation` |
| `{package-prefix}-*` | パッケージプレフィックス | `@tanstack/query-*` |
| `{日本語キーワード}` | 日本語での呼び出しキーワード | `データフェッチ` |

## 記載ルール

### descriptionの書き方

**ルール:**
- 1024文字以内
- 英語（最終行の日本語キーワード部分を除く）
- 三人称・動詞で始める

**トリガー条件を含める:**
1. import文のパターン: `imports "package-name"`
2. ワイルドカード: `any "@tanstack/*" packages`
3. ユーザーの質問パターン: `asks about {Library}`
4. 関連キーワード: 主要なAPI名、関数名、コンポーネント名

### 良いdescription例

```yaml
description: |
  Provides documentation for TanStack Query (React Query).
  Use when working with code that imports "useQuery", "useMutation", "@tanstack/react-query", or any "@tanstack/query-*" packages.
  Use when the user asks about data fetching, caching, or shows code with React Query hooks.
  Can also be invoked directly with "React Query", "TanStack Query", "データフェッチ".
```
