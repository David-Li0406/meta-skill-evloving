---
name: api-design
description: API設計 - REST/GraphQL設計原則、バージョニング、エラーハンドリング、ドキュメント
requires-guidelines:
  - common
---

# API設計

## 使用タイミング

- API設計時（新規エンドポイント追加）/ APIレビュー時 / ドキュメント作成時

---

## レビュー観点

### 🔴 Critical（修正必須）

| 観点 | 検出パターン | 対策 |
|------|-------------|------|
| リソース設計違反 | 動詞ベースURL (`/createUser`) | リソース名詞 + HTTPメソッド |
| ステータスコード誤用 | エラーでも200返却 | 適切なステータスコード |
| エラー形式未統一 | バラバラなJSON構造 | RFC 7807 Problem Details |

### 🟡 Warning（要改善）

| 観点 | 検出パターン | 対策 |
|------|-------------|------|
| バージョニング未実装 | `/api/users` 固定 | `/api/v1/users` or ヘッダー |
| ページネーション不足 | 全件取得 | カーソルベースページネーション |
| レート制限なし | 認証APIに制限なし | express-rate-limit等 |

**コード例が必要な場合**: Context7で「REST API design」「GraphQL best practices」を検索

---

## REST API パターン

### リソース設計

| パターン | URL | メソッド | 用途 |
|---------|-----|---------|------|
| コレクション | `/users` | GET/POST | 一覧/作成 |
| 単一リソース | `/users/123` | GET/PUT/PATCH/DELETE | CRUD |
| サブリソース | `/users/123/posts` | GET | 関連取得 |

### ステータスコード

| コード | 用途 |
|-------|------|
| 200/201/204 | 成功系 |
| 400/401/403/404 | クライアントエラー |
| 409/422/429 | 競合/処理不可/レート超過 |
| 500 | サーバーエラー |

---

## GraphQL パターン

| 観点 | ベストプラクティス |
|------|-------------------|
| スキーマ | 明確な命名・型定義 |
| ページネーション | Connection pattern |
| N+1問題 | DataLoader使用 |

---

## チェックリスト

**REST**: リソースベースURL / 適切なステータス / エラー統一 / バージョニング / ページネーション / レート制限

**GraphQL**: 明確なスキーマ / Null許容設定 / DataLoader / Connection pattern

**共通**: 認証・認可 / CORS / OpenAPI/GraphQLドキュメント / セキュリティヘッダー

---

## 出力形式

```
🔴 Critical: エンドポイント - 問題 - 修正案
🟡 Warning: エンドポイント - 問題 - 改善案
📊 Summary: Critical X件 / Warning Y件
```

---

## 外部リソース

- **Context7**: OpenAPI 3.x、GraphQL公式、Google/Microsoft API Design Guide、RFC 7807
- **Serena memory**: プロジェクト固有のAPI規約・バージョニング戦略
