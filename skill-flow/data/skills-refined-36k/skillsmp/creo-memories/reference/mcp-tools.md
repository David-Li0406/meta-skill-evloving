# Creo Memories MCPツール リファレンス

## 概要

Creo MemoriesはMCP（Model Context Protocol）経由でClaude Codeと連携します。

**MCPサーバー名**: `creo-memories`
**エンドポイント**: `https://mcp.creo-memories.in`

---

## メモリ操作ツール

### remember

メモリを保存します。

```typescript
mcp__creo-memories__remember({
  content: "保存する内容",      // 必須
  category: "design",           // オプション
  tags: ["tag1", "tag2"],       // オプション
  labelIds: ["label:..."],      // オプション（ラベルID配列）
  metadata: { key: "value" },   // オプション
  contentType: "markdown",      // オプション（text/markdown）
  spaceId: "space:...",         // オプション
  domainId: "domain:..."        // オプション
})
```

---

### recall

セマンティック検索で関連メモリを取得します。

```typescript
mcp__creo-memories__recall({
  query: "検索クエリ",          // 必須
  limit: 10,                    // オプション（デフォルト: 10）
  threshold: 0.7,               // オプション（デフォルト: 0.7）
  labelIds: ["label:..."],      // オプション（ラベルフィルタ）
  includeLabels: true,          // オプション
  domainId: "domain:..."        // オプション
})
```

**閾値ガイド**:
- `0.9+`: 非常に関連性が高い
- `0.7-0.9`: 関連性が高い（推奨）
- `0.5-0.7`: ある程度関連

---

### search

高度な検索機能でメモリを検索します。

```typescript
mcp__creo-memories__search({
  query: "検索クエリ",          // オプション
  category: "design",           // オプション
  tags: ["tag1"],               // オプション
  fromDate: "2025-01-01T...",   // オプション（ISO 8601）
  toDate: "2025-12-31T...",     // オプション
  searchType: "hybrid",         // オプション（semantic/hybrid）
  limit: 10,                    // オプション
  threshold: 0.7                // オプション
})
```

---

### list

最近保存されたメモリを一覧表示します。

```typescript
mcp__creo-memories__list({
  limit: 20,                    // オプション（デフォルト: 20）
  category: "design",           // オプション
  verbose: false                // オプション
})
```

---

### forget

メモリを削除します。

```typescript
mcp__creo-memories__forget({
  id: "メモリID",               // 必須
  confirm: true                 // 必須（安全確認）
})
```

**注意**: 削除は取り消せません。`confirm: true` が必須です。

---

## ラベル管理ツール

### label_create

ラベルを作成します。

```typescript
mcp__creo-memories__label_create({
  name: "重要",                 // 必須
  color: "#FF0000"              // オプション（HEXカラー）
})
```

### label_list

ラベル一覧を取得します。

```typescript
mcp__creo-memories__label_list()
```

### label_attach

メモリにラベルを付与します。

```typescript
mcp__creo-memories__label_attach({
  memory_id: "memory:...",      // 必須
  label_id: "label:..."         // 必須
})
```

### label_detach

メモリからラベルを解除します。

```typescript
mcp__creo-memories__label_detach({
  memory_id: "memory:...",      // 必須
  label_id: "label:..."         // 必須
})
```

---

## Space管理ツール

Spaceはメモリを整理するための論理的な作業単位です。

### list_spaces

Space一覧を取得します。

```typescript
mcp__creo-memories__list_spaces()
```

### create_space

新しいSpaceを作成します。

```typescript
mcp__creo-memories__create_space({
  name: "プロジェクトA",        // 必須
  description: "説明",          // オプション
  metadata: {}                  // オプション
})
```

### get_space

Space詳細を取得します。

```typescript
mcp__creo-memories__get_space({
  space_id: "space:..."         // 必須
})
```

---

## Domain管理ツール

Domainは知識の分類領域です。

### list_domains

ドメイン一覧を取得します。

```typescript
mcp__creo-memories__list_domains({
  parent_id: "domain:..."       // オプション
})
```

### create_domain

新しいドメインを作成します。

```typescript
mcp__creo-memories__create_domain({
  name: "ドメイン名",           // 必須
  parent_id: "domain:...",      // オプション
  metadata: {}                  // オプション
})
```

### switch_domain

セッションのデフォルトドメインを切り替えます。

```typescript
mcp__creo-memories__switch_domain({
  sessionId: "session:...",     // 必須
  defaultDomainId: "domain:..." // 必須
})
```

---

## セッション管理ツール

### start_session

セッションを開始します。

```typescript
mcp__creo-memories__start_session({
  userId: "user:...",           // 必須
  defaultSpaceId: "space:...",  // オプション
  defaultDomainId: "domain:..." // オプション
})
```

### get_session

セッション情報を取得します。

```typescript
mcp__creo-memories__get_session({
  sessionId: "session:..."      // 必須
})
```

### end_session

セッションを終了します。

```typescript
mcp__creo-memories__end_session({
  sessionId: "session:..."      // 必須
})
```

---

## Todo管理ツール

### create_todo

Todoを作成します。

```typescript
mcp__creo-memories__create_todo({
  content: "タスク内容",        // 必須
  priority: "high",             // オプション（low/medium/high）
  dueDate: "2025-12-31T...",    // オプション
  tags: ["work"]                // オプション
})
```

### list_todos

Todo一覧を取得します。

```typescript
mcp__creo-memories__list_todos({
  status: "pending",            // オプション（pending/in_progress/completed）
  priority: "high",             // オプション
  tags: ["work"],               // オプション
  limit: 20                     // オプション
})
```

### complete_todo

Todoを完了としてマークします。

```typescript
mcp__creo-memories__complete_todo({
  id: "todo:..."                // 必須
})
```

---

## ユーザー管理ツール

### get_user

認証済みユーザーの情報を取得します。

```typescript
mcp__creo-memories__get_user()
```

### generate_api_key

APIキーを生成します（一度だけ表示）。

```typescript
mcp__creo-memories__generate_api_key()
```

---

## カテゴリ一覧

| カテゴリ | 用途 | 例 |
|---------|------|-----|
| `prd` | プロダクト要件 | ビジネス要件、ゴール |
| `spec` | 仕様・要件 | 機能要件、制約 |
| `design` | 設計・アーキテクチャ | システム設計、API設計 |
| `config` | 設定・構成 | 環境変数、サービス設定 |
| `infra` | インフラ | サーバー、デプロイ、DNS |
| `debug` | デバッグ | バグ原因、解決策 |
| `learning` | 学習・知見 | ベストプラクティス、TIL |
| `task` | タスク・計画 | 将来の実装、改善案 |
| `decision` | 意思決定 | 重要な決定と理由 |
