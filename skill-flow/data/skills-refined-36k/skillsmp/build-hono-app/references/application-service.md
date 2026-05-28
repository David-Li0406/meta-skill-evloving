# Use Case (Service) 実装パターン

## 概要

Use Case (Service) はビジネスロジックを調整する。
Repository や Adapter を組み合わせて、1つのユースケースを実現。

## 設計原則

### 1. 依存性注入 (DI)
- constructor で Context と依存オブジェクトを受け取る
- デフォルト値でテスト容易性を確保

### 2. 単一責任
- 1クラス = 1ユースケース
- `execute()` メソッドで実行

### 3. エラーハンドリング
- **throw しない**
- カスタムエラーを return する
- 戻り値は `Promise<Result | NotFoundError | ConflictError | ...>`

## 命名規則

| 操作 | クラス名 | ファイル名 |
|------|---------|-----------|
| 作成 | `CreateCustomer` | `create-customer.ts` |
| 更新 | `UpdateCustomer` | `update-customer.ts` |
| 削除 | `DeleteCustomer` | `delete-customer.ts` |
| 取得 | `FetchCustomer` / `GetCustomer` | `fetch-customer.ts` |
| 一括 | `BulkUpdateCustomers` | `bulk-update-customers.ts` |
| 同期 | `SyncCustomers` | `sync-customers.ts` |

## 実装例

### 作成 Service

```ts
import type { Context } from "@/env"
import { CustomerRepository } from "@/infrastructure/repositories/customer.repository"
import { CustomerEntity } from "@/domain/entities/customer.entity"
import { ConflictError } from "@/lib/errors"

type Props = {
  name: string
  email: string
}

type Result = {
  customer: CustomerEntity
}

/**
 * 顧客を作成する
 */
export class CreateCustomer {
  constructor(
    readonly c: Context,
    readonly deps = {
      customerRepository: new CustomerRepository(c),
    },
  ) {}

  async execute(props: Props): Promise<Result | ConflictError> {
    const { customerRepository } = this.deps

    // 重複チェック
    const existing = await customerRepository.findByEmail(props.email)
    if (existing) {
      return new ConflictError("このメールアドレスは既に登録されています")
    }

    // Entity 作成
    const customer = CustomerEntity.create({
      name: props.name,
      email: props.email,
    })

    // 保存
    await customerRepository.save(customer)

    return { customer }
  }
}
```

### 更新 Service

```ts
import type { Context } from "@/env"
import { CustomerRepository } from "@/infrastructure/repositories/customer.repository"
import { NotFoundError, ConflictError } from "@/lib/errors"

type Props = {
  id: string
  name?: string
  email?: string
}

type Result = {
  customer: CustomerEntity
}

/**
 * 顧客を更新する
 */
export class UpdateCustomer {
  constructor(
    readonly c: Context,
    readonly deps = {
      customerRepository: new CustomerRepository(c),
    },
  ) {}

  async execute(props: Props): Promise<Result | NotFoundError | ConflictError> {
    const { customerRepository } = this.deps

    // 取得
    const customer = await customerRepository.findById(props.id)
    if (!customer) {
      return new NotFoundError("顧客が見つかりません")
    }

    // 更新
    let updated = customer
    if (props.name) {
      updated = updated.withName(props.name)
    }
    if (props.email) {
      // メールアドレス重複チェック
      const existing = await customerRepository.findByEmail(props.email)
      if (existing && existing.id !== props.id) {
        return new ConflictError("このメールアドレスは既に使用されています")
      }
      updated = updated.withEmail(props.email)
    }

    // 保存
    await customerRepository.save(updated)

    return { customer: updated }
  }
}
```

### 外部サービス連携 Service

```ts
import type { Context } from "@/env"
import { OrderRepository } from "@/infrastructure/repositories/order.repository"
import { PaymentAdapter } from "@/infrastructure/adapters/payment.adapter"
import { NotFoundError, ExternalServiceError } from "@/lib/errors"

type Props = {
  orderId: string
  amount: number
}

type Result = {
  order: OrderEntity
  chargeId: string
}

/**
 * 注文の決済を処理する
 */
export class ProcessOrderPayment {
  constructor(
    readonly c: Context,
    readonly deps = {
      orderRepository: new OrderRepository(c),
      paymentAdapter: new PaymentAdapter(c),
    },
  ) {}

  async execute(props: Props): Promise<Result | NotFoundError | ExternalServiceError> {
    const { orderRepository, paymentAdapter } = this.deps

    // 注文取得
    const order = await orderRepository.findById(props.orderId)
    if (!order) {
      return new NotFoundError("注文が見つかりません")
    }

    // 決済実行
    const chargeResult = await paymentAdapter.charge({
      amount: props.amount,
      currency: "JPY",
      customerId: order.customerId,
    })

    if (!chargeResult.success) {
      return new ExternalServiceError("決済に失敗しました")
    }

    // ローカル DB 更新
    const updated = order.withChargeId(chargeResult.chargeId)
    await orderRepository.save(updated)

    return {
      order: updated,
      chargeId: chargeResult.chargeId,
    }
  }
}
```

## Route Handler からの呼び出し

```ts
// interface/routes/customers.$customer.ts
import { NotFoundError, ConflictError } from "@/lib/errors"

export const PUT = factory.createHandlers(
  authorizedAdmin(),
  zValidator("json", zUpdateCustomerBody),
  async (c: Context) => {
    const id = c.req.param("customer")
    const body = c.req.valid("json")

    // Service をインスタンス化
    const service = new UpdateCustomer(c)

    // execute() を呼び出し、結果は result に格納
    const result = await service.execute({
      id,
      name: body.name,
      email: body.email,
    })

    // カスタムエラーの場合は HTTPException に変換
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
