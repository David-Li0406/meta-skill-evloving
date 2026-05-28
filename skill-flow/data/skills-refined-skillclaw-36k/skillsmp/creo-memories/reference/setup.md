# Creo Memories セットアップガイド

## 概要

Creo MemoriesはHTTP MCP経由でClaude Codeと接続します。OAuth認証により安全にアクセスできます。

## プラグインインストール（推奨）

```bash
/install chronista-club/claude-plugin-creo-memories
```

インストール後、`.mcp.json` が自動設定されます。

## 手動セットアップ

### 1. MCPサーバーを追加

Claude Codeで以下のコマンドを実行：

```bash
claude mcp add --transport http creo-memories https://mcp.creo-memories.in
```

または、`.mcp.json` に直接追加：

```json
{
  "mcpServers": {
    "creo-memories": {
      "type": "http",
      "url": "https://mcp.creo-memories.in"
    }
  }
}
```

### 2. OAuth認証

初回接続時に認証が必要です：

1. `/mcp` でcreo-memoriesを選択
2. `Authenticate` を選択
3. ブラウザでAuth0ログイン画面が開く
4. Google/GitHubアカウントでログイン
5. 認証完了後、Claude Codeに戻る

### 3. 接続確認

```typescript
// ユーザー情報を取得
mcp__creo-memories__get_user()

// 最近のメモリを表示
mcp__creo-memories__list({ limit: 5 })
```

## 認証方式

### OAuth（推奨）

ブラウザ経由でAuth0認証。Claude Codeのデフォルト方式。

### APIキー

プログラマティックアクセス用：

```typescript
// APIキーを生成（一度だけ表示）
mcp__creo-memories__generate_api_key()
```

生成されたキーは安全に保管し、`Authorization: Bearer <key>` ヘッダーで使用。

## SpaceとDomain

### 概念

- **Space**: 作業コンテキスト（プロジェクト単位）
- **Domain**: 知識の分類領域（技術分野、目的別）

### 初期設定

```typescript
// Space一覧を確認
mcp__creo-memories__list_spaces()

// ドメイン一覧を確認
mcp__creo-memories__list_domains()
```

## トラブルシューティング

### 認証エラー

```
Error: Authentication required
```

**対処**:
1. `/mcp` でcreo-memoriesを選択
2. `Authenticate` で再認証

### 接続エラー

```
Error: Connection refused
```

**対処**:
1. インターネット接続を確認
2. `https://mcp.creo-memories.in/health` にアクセスできるか確認
3. MCPサーバー設定を確認

## 本番環境情報

| 項目 | 値 |
|------|-----|
| MCPエンドポイント | `https://mcp.creo-memories.in` |
| Webビューアー | `https://creo-memories.in` |
| Auth0ドメイン | `creo-memories.jp.auth0.com` |
