# エラーハンドリング実装パターン

## 概要

アプリケーション全体で一貫したエラーハンドリングを実現する。
Application 層は throw せずカスタムエラーを return し、Interface 層で HTTPException に変換。

## 設計原則

### Application 層 (Service)
- **throw しない**
- カスタムエラーを return する
- 戻り値は `Promise<Result | NotFoundError | ConflictError | ...>`

### Interface 層 (Route Handler)
- `result instanceof カスタムエラー` でチェック
- HTTPException に変換
- ユーザーフレンドリーなメッセージを設定 (API レイヤーの責務)

## カスタムエラーの定義

### lib/errors.ts

```ts
import { HTTPException } from "hono/http-exception"

/**
 * 認証エラー (ログイン必須の操作)
 */
export class UnauthorizedException extends HTTPException {
  constructor() {
    super(401, { message: "ログインしてください" })
    this.name = "UnauthorizedException"
  }
}

/**
 * リソースが見つからない
 */
export class NotFoundError extends Error {
  readonly statusCode = 404

  constructor(message = "リソースが見つかりません") {
    super(message)
    this.name = "NotFoundError"
    Object.freeze(this)
  }
}

/**
 * バリデーションエラー
 */
export class ValidationError extends Error {
  readonly statusCode = 400

  constructor(message = "入力値が不正です") {
    super(message)
    this.name = "ValidationError"
    Object.freeze(this)
  }
}

/**
 * 認証エラー
 */
export class AuthenticationError extends Error {
  readonly statusCode = 401

  constructor(message = "認証が必要です") {
    super(message)
    this.name = "AuthenticationError"
    Object.freeze(this)
  }
}

/**
 * 権限エラー
 */
export class ForbiddenError extends Error {
  readonly statusCode = 403

  constructor(message = "アクセス権限がありません") {
    super(message)
    this.name = "ForbiddenError"
    Object.freeze(this)
  }
}

/**
 * 重複エラー
 */
export class ConflictError extends Error {
  readonly statusCode = 409

  constructor(message = "リソースが既に存在します") {
    super(message)
    this.name = "ConflictError"
    Object.freeze(this)
  }
}

/**
 * 内部エラー
 */
export class InternalError extends Error {
  readonly statusCode = 500

  constructor(message = "内部エラーが発生しました") {
    super(message)
    this.name = "InternalError"
    Object.freeze(this)
  }
}

/**
 * 外部サービスエラー
 */
export class ExternalServiceError extends Error {
  readonly statusCode = 502

  constructor(message = "外部サービスでエラーが発生しました") {
    super(message)
    this.name = "ExternalServiceError"
    Object.freeze(this)
  }
}
```

## 使用例

### Application 層 (Service)

```ts
// application/update-customer.ts
import { NotFoundError, ConflictError } from "@/lib/errors"

type Result = {
  customer: CustomerEntity
}

export class UpdateCustomer {
  constructor(
    readonly c: Context,
    readonly deps = {
      customerRepository: new CustomerRepository(c),
    },
  ) {}

  async execute(props: Props): Promise<Result | NotFoundError | ConflictError> {
    const { customerRepository } = this.deps

    // 見つからない場合はカスタムエラーを return
    const customer = await customerRepository.findById(props.id)
    if (!customer) {
      return new NotFoundError("顧客が見つかりません")
    }

    // 重複チェック
    if (props.email) {
      const existing = await customerRepository.findByEmail(props.email)
      if (existing && existing.id !== props.id) {
        return new ConflictError("このメールアドレスは既に使用されています")
      }
    }

    // 更新処理
    let updated = customer
    if (props.name) {
      updated = updated.withName(props.name)
    }
    if (props.email) {
      updated = updated.withEmail(props.email)
    }

    await customerRepository.save(updated)

    return { customer: updated }
  }
}
```

### Interface 層 (Route Handler)

```ts
// interface/routes/customers.$customer.ts
import { NotFoundError, ConflictError } from "@/lib/errors"

export const PUT = factory.createHandlers(
  authorizedAdmin(),
  zValidator("json", zUpdateCustomerBody),
  async (c: Context) => {
    const id = c.req.param("customer")
    const body = c.req.valid("json")

    const service = new UpdateCustomer(c)
    const result = await service.execute({
      id,
      name: body.name,
      email: body.email,
    })

    // カスタムエラーの場合は HTTPException に変換
    // ユーザーフレンドリーなメッセージに変換するのは API レイヤーの責務
    if (result instanceof NotFoundError) {
      throw new HTTPException(404, { message: "顧客が見つかりません" })
    }

    if (result instanceof ConflictError) {
      throw new HTTPException(409, { message: "このメールアドレスは既に使用されています" })
    }

    return c.json({
      id: result.customer.id,
      name: result.customer.name,
      email: result.customer.email,
    })
  },
)
```

## HTTP ステータスコードガイドライン

| カスタムエラー | ステータス | 例 |
|--------------|----------|-----|
| `NotFoundError` | 404 | 顧客が見つかりません |
| `ValidationError` | 400 | 名前は必須です |
| `AuthenticationError` | 401 | ログインしてください |
| `ForbiddenError` | 403 | 管理者権限が必要です |
| `ConflictError` | 409 | このメールアドレスは既に使用されています |
| `InternalError` | 500 | 予期しないエラーが発生しました |
| `ExternalServiceError` | 502 | 外部サービスとの連携に失敗しました |

## グローバルエラーハンドラー

```ts
// index.ts
export default factory
  .createApp()
  // ...ルート定義
  .onError((error, c) => {
    console.error(error)

    if (error instanceof HTTPException) {
      return c.json({ message: error.message }, error.status)
    }

    return c.json({ message: "Internal Server Error" }, 500)
  })
```
