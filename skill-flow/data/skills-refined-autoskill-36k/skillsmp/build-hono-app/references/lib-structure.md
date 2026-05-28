# Lib 層の構造

## 概要

Lib 層は全レイヤーから参照可能な横断的ライブラリ。
認証、セッション管理、定数、ユーティリティ関数など。

**注意**: 外部サービス連携 (メール送信、外部 API など) は Adapter の責務。Lib には含めない。

## ディレクトリ構造

```
lib/
├── auth/                    # 認証関連ユーティリティ
│   ├── hash-password.ts     # パスワードハッシュ化
│   └── verify-password.ts   # パスワード検証
├── constants/               # 定数定義
│   └── status.ts
├── crypto/                  # 暗号化ユーティリティ
│   └── generate-token.ts
├── session/                 # セッション管理
│   ├── session-payload.ts   # セッション型定義 (Valibot)
│   ├── authorized.ts        # 認可ミドルウェア
│   └── authorized-admin.ts  # 管理者認可
├── types/                   # 型定義
│   └── common.types.ts
├── utils/                   # ユーティリティ関数
│   ├── format.ts
│   └── detect-changes.ts
├── errors.ts                # アプリケーションエラー
└── schema.ts                # Drizzle スキーマ再エクスポート
```

## Lib に含めないもの

以下は Infrastructure 層の Adapter として実装する:

- メール送信 → `infrastructure/adapters/email.adapter.ts`
- 外部 API 連携 → `infrastructure/adapters/xxx.adapter.ts`

## 主要ファイル

### セッション管理

```ts
// lib/session/session-payload.ts
import { object, string, picklist, type InferOutput } from "valibot"

export const vSessionPayload = object({
  userId: string(),
  email: string(),
  role: picklist(["ADMIN", "STAFF"]),
})

export type SessionPayload = InferOutput<typeof vSessionPayload>
```

```ts
// lib/session/authorized.ts
import { factory } from "@/interface/factory"
import { HTTPException } from "hono/http-exception"

export const authorized = () =>
  factory.createMiddleware(async (c, next) => {
    const session = await getSession(c)
    if (!session) {
      throw new HTTPException(401, { message: "認証が必要です" })
    }
    c.set("session", session)
    return next()
  })
```

```ts
// lib/session/authorized-admin.ts
export const authorizedAdmin = () =>
  factory.createMiddleware(async (c, next) => {
    const session = c.get("session")
    if (session?.role !== "ADMIN") {
      throw new HTTPException(403, { message: "管理者権限が必要です" })
    }
    return next()
  })
```

### アプリケーションエラー

```ts
// lib/errors.ts
export class NotFoundError extends Error {
  readonly statusCode = 404

  constructor(message = "リソースが見つかりません") {
    super(message)
    this.name = "NotFoundError"
    Object.freeze(this)
  }
}

export class ValidationError extends Error {
  readonly statusCode = 400

  constructor(message = "入力値が不正です") {
    super(message)
    this.name = "ValidationError"
    Object.freeze(this)
  }
}

export class ConflictError extends Error {
  readonly statusCode = 409

  constructor(message = "リソースが競合しています") {
    super(message)
    this.name = "ConflictError"
    Object.freeze(this)
  }
}

export class ForbiddenError extends Error {
  readonly statusCode = 403

  constructor(message = "この操作を行う権限がありません") {
    super(message)
    this.name = "ForbiddenError"
    Object.freeze(this)
  }
}
```

### ユーティリティ

```ts
// lib/utils/format.ts
export function normalizePhone(phone: string | null | undefined): string | null {
  if (!phone) return null
  return phone.replace(/[^\d+]/g, "")
}

export function formatDate(date: Date): string {
  return date.toISOString().split("T")[0]
}
```

```ts
// lib/utils/detect-changes.ts
export function detectChanges<T extends Record<string, unknown>>(
  before: T,
  after: Partial<T>,
  fields: (keyof T)[]
): Record<string, { before: unknown; after: unknown }> {
  const changes: Record<string, { before: unknown; after: unknown }> = {}

  for (const field of fields) {
    if (field in after && before[field] !== after[field]) {
      changes[field as string] = {
        before: before[field],
        after: after[field],
      }
    }
  }

  return changes
}
```

### 型定義

```ts
// lib/types/common.types.ts
export type Pagination = {
  page: number
  limit: number
  total: number
}

export type SortOrder = "asc" | "desc"

export type ListParams = {
  page?: number
  limit?: number
  sortBy?: string
  sortOrder?: SortOrder
}
```
