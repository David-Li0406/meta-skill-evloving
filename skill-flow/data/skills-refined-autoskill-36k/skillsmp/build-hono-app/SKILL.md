---
name: build-hono-app
description: TypeScript バックエンド開発スキル。Clean Architecture、レイヤー構成、Repository パターン、Use Case 実装、エラーハンドリングなど。API 開発時に使用。
---

# TypeScript Backend Development

TypeScript バックエンドの設計・実装パターンを定義する。
Clean Architecture に基づくレイヤー構成で、保守性・テスト容易性を重視。

## レイヤー構成

```
api/
├── domain/              # ドメイン層 (ビジネスロジック)
│   ├── entities/        # エンティティ
│   ├── values/          # 値オブジェクト
│   └── errors/          # ドメインエラー
├── application/         # アプリケーション層 (ユースケース)
├── infrastructure/      # インフラ層
│   ├── repositories/    # リポジトリ実装
│   ├── adapters/        # 外部サービスアダプター
│   └── converters/      # データ変換
├── interface/           # インターフェース層
│   ├── routes/          # HTTPハンドラー
│   ├── middlewares/     # ミドルウェア
│   ├── serializers/     # レスポンス変換
│   └── factory.ts       # Hono Factory
├── lib/                 # 共有ライブラリ (横断的関心事のみ)
│   ├── auth/            # 認証ユーティリティ
│   ├── constants/       # 定数
│   ├── crypto/          # 暗号化ユーティリティ
│   ├── session/         # セッション管理
│   ├── types/           # 型定義
│   ├── utils/           # ユーティリティ
│   └── errors.ts        # アプリケーションエラー
├── migrations/          # D1 マイグレーション
├── drizzle.schema.ts    # DB スキーマ定義
├── env.d.ts             # 型定義
└── index.ts             # エントリーポイント
```

## 依存関係のルール

```
Interface → Application → Infrastructure → Domain
                ↓              ↓            ↓
              Lib            Lib          Lib
```

- 上位レイヤーは下位レイヤーに依存する
- 下位レイヤーは上位レイヤーを知らない
- Domain は最も内側で、外部依存がない
- Lib は全レイヤーから参照可能 (横断的関心事のみ)

## 設計原則

### Domain 層
- Entity は DB の存在を知らない (`fromRecord()` のようなメソッドは定義しない)
- DB レコードから Entity への変換は Repository (インフラ層) の責務
- ファクトリメソッドは具体的な名前を使う (`create()` より `createWithEmail()`)

### Application 層 (Service)
- throw しない。カスタムエラーを return する
- 戻り値は `Promise<Result | NotFoundError | ConflictError | ...>`

### Infrastructure 層
- 外部サービス連携は全て Adapter として実装 (Lib には含めない)
- メール送信、外部 API は Adapter の責務

### Interface 層
- `result instanceof カスタムエラー` でエラー判定
- HTTPException に変換してユーザーフレンドリーなメッセージを設定

### Lib 層
- 横断的関心事のみ (認証、セッション、定数、ユーティリティ)
- 外部サービス連携は含めない

## 命名規則

### ファイル命名

| レイヤー | パターン | 例 |
|---------|---------|-----|
| Entity | `xxx.entity.ts` | `customer.entity.ts` |
| Value | `xxx.value.ts` | `email.value.ts` |
| Repository | `xxx.repository.ts` | `customer.repository.ts` |
| Adapter | `xxx.adapter.ts` | `email.adapter.ts`, `payment.adapter.ts` |
| Use Case | `動詞-名詞.ts` | `create-customer.ts`, `update-customer.ts` |
| Route | `resource.$param.ts` | `customers.$customer.ts` |

### Service (Use Case) 命名

| 操作 | プレフィックス | 例 |
|------|--------------|-----|
| 作成 | `create-` | `create-customer.ts` |
| 更新 | `update-` | `update-customer.ts` |
| 削除 | `delete-` | `delete-customer.ts` |
| 取得 | `fetch-` / `get-` | `fetch-customer.ts` |
| 一括 | `bulk-` | `bulk-update-orders.ts` |
| 同期 | `sync-` | `sync-users.ts` |
| Upsert | `upsert-` | `upsert-profile.ts` |

### Route ファイル命名

| URL | ファイル名 |
|-----|-----------|
| `/customers` | `customers.ts` |
| `/customers/:customer` | `customers.$customer.ts` |
| `/customers/:customer/orders` | `customers.$customer.orders.ts` |
| `/customers/:customer/orders/:id` | `customers.$customer.orders.$id.ts` |
| `/customers/search` | `customers.search.ts` |

## 参照ファイル

各パターンの詳細は以下を参照:

### ドメイン層
- [references/domain-entity.md](references/domain-entity.md) - Entity の実装パターン
- [references/domain-value.md](references/domain-value.md) - Value Object の実装パターン
- [references/domain-error.md](references/domain-error.md) - ドメインエラー

### アプリケーション層
- [references/application-service.md](references/application-service.md) - Service (Use Case) の実装パターン

### インフラ層
- [references/infrastructure-repository.md](references/infrastructure-repository.md) - Repository パターン
- [references/infrastructure-adapter.md](references/infrastructure-adapter.md) - Adapter パターン

### インターフェース層
- [references/interface-route-handler.md](references/interface-route-handler.md) - HTTP ハンドラー
- [references/interface-entry-point.md](references/interface-entry-point.md) - エントリーポイント
- [references/interface-error-handling.md](references/interface-error-handling.md) - エラーハンドリング

### 共通
- [references/drizzle-schema.md](references/drizzle-schema.md) - DB スキーマ定義
- [references/lib-structure.md](references/lib-structure.md) - Lib 層の構造
