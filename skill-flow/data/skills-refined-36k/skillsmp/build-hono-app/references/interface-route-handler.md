# Route Handler 実装パターン

## 概要

Route Handler は HTTP リクエストを受け取り、Service (Use Case) を呼び出す。
Hono の Factory パターンでミドルウェアと組み合わせる。

## 設計原則

### 1. 薄いハンドラー
- バリデーション、Service 呼び出し、レスポンス変換のみ
- ビジネスロジックは Service (Application 層) に委譲

### 2. ファイルベースルーティング
- `routes/customers.ts` → `/customers`
- `routes/customers.$id.ts` → `/customers/:id`
- `routes/customers.$id.orders.ts` → `/customers/:id/orders`

### 3. HTTP メソッドのエクスポート
- `export const GET = ...`
- `export const POST = ...`
- `export const PUT = ...`
- `export const DELETE = ...`

### 4. エラーハンドリング
- Application 層は throw しない (カスタムエラーを return する)
- Route Handler で `result instanceof カスタムエラー` をチェック
- HTTPException に変換し、ユーザーフレンドリーなメッセージを設定

## 命名規則

| URL パターン | ファイル名 |
|-------------|-----------|
| `/customers` | `customers.ts` |
| `/customers/:customer` | `customers.$customer.ts` |
| `/customers/:customer/orders` | `customers.$customer.orders.ts` |
| `/customers/:customer/orders/:orderId` | `customers.$customer.orders.$orderId.ts` |

## 実装例

```ts
import { z } from "zod"
import type { Context } from "hono"
import { HTTPException } from "hono/http-exception"
import { factory } from "@/interface/factory"
import { authorized, authorizedAdmin } from "@/lib/session/authorized"
import { zValidator } from "@hono/zod-validator"
import { CreateCustomer } from "@/application/create-customer"
import { UpdateCustomer } from "@/application/update-customer"
import { FetchCustomer } from "@/application/fetch-customer"
import { DeleteCustomer } from "@/application/delete-customer"
import { NotFoundError, ConflictError } from "@/lib/errors"

// --- バリデーションスキーマ ---

const zCreateCustomerBody = z.object({
  name: z.string().min(1, "名前は必須です"),
  email: z.string().email("有効なメールアドレスを入力してください"),
})

const zUpdateCustomerBody = z.object({
  name: z.string().min(1).optional(),
  email: z.string().email().optional(),
})

// --- GET /customers/:id ---

export const GET = factory.createHandlers(
  authorized(),
  async (c: Context) => {
    const id = c.req.param("id")

    const service = new FetchCustomer(c)
    const result = await service.execute({ id })

    if (result instanceof NotFoundError) {
      throw new HTTPException(404, { message: "顧客が見つかりません" })
    }

    return c.json({
      id: result.customer.id,
      name: result.customer.name,
      email: result.customer.email,
      status: result.customer.status,
      createdAt: result.customer.createdAt.toISOString(),
      updatedAt: result.customer.updatedAt.toISOString(),
    })
  },
)

// --- POST /customers ---

export const POST = factory.createHandlers(
  authorized(),
  zValidator("json", zCreateCustomerBody),
  async (c: Context) => {
    const body = c.req.valid("json")

    const service = new CreateCustomer(c)
    const result = await service.execute({
      name: body.name,
      email: body.email,
    })

    if (result instanceof ConflictError) {
      throw new HTTPException(409, { message: "このメールアドレスは既に登録されています" })
    }

    return c.json(
      {
        id: result.customer.id,
        name: result.customer.name,
        email: result.customer.email,
      },
      201,
    )
  },
)

// --- PUT /customers/:id ---

export const PUT = factory.createHandlers(
  authorizedAdmin(),
  zValidator("json", zUpdateCustomerBody),
  async (c: Context) => {
    const id = c.req.param("id")
    const body = c.req.valid("json")

    const service = new UpdateCustomer(c)
    const result = await service.execute({
      id,
      name: body.name,
      email: body.email,
    })

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

// --- DELETE /customers/:id ---

export const DELETE = factory.createHandlers(
  authorizedAdmin(),
  async (c: Context) => {
    const id = c.req.param("id")

    const service = new DeleteCustomer(c)
    const result = await service.execute({ id })

    if (result instanceof NotFoundError) {
      throw new HTTPException(404, { message: "顧客が見つかりません" })
    }

    return c.json({ success: true })
  },
)
```

## エラーハンドリングの原則

### Application 層 (Service)
- throw しない
- カスタムエラーを return する

```ts
// application/update-customer.ts
import { NotFoundError, ConflictError } from "@/lib/errors"

async execute(props: Props): Promise<Result | NotFoundError | ConflictError> {
  const customer = await this.deps.customerRepository.findById(props.id)
  if (!customer) {
    return new NotFoundError("顧客が見つかりません")
  }

  const existing = await this.deps.customerRepository.findByEmail(props.email)
  if (existing && existing.id !== props.id) {
    return new ConflictError("このメールアドレスは既に使用されています")
  }

  // ...
  return { customer: updated }
}
```

### Interface 層 (Route Handler)
- `result instanceof カスタムエラー` でチェック
- HTTPException に変換
- ユーザーフレンドリーなメッセージを設定

```ts
import { NotFoundError, ConflictError } from "@/lib/errors"

const result = await service.execute(props)

if (result instanceof NotFoundError) {
  throw new HTTPException(404, { message: "顧客が見つかりません" })
}

if (result instanceof ConflictError) {
  throw new HTTPException(409, { message: "このメールアドレスは既に使用されています" })
}

return c.json(result.customer)
```
