# Adapter 実装パターン

## 概要

Adapter は外部サービスとの通信をカプセル化する。
REST API や GraphQL の呼び出しを抽象化し、ドメイン層から外部依存を隠蔽。

外部サービス連携は全て Adapter として実装する (Lib には含めない)。

## 命名規則

| 外部サービス | ファイル名 |
|-------------|-----------|
| 外部 API | `xxx-api.adapter.ts` |
| メール送信 | `email.adapter.ts` |
| 決済サービス | `payment.adapter.ts` |
| ストレージ | `storage.adapter.ts` |

## 実装パターン (REST API)

```ts
// infrastructure/adapters/payment.adapter.ts
import type { Context } from "@/env"

type ChargeResult =
  | { success: true; chargeId: string }
  | { success: false; error: string }

type RefundResult =
  | { success: true }
  | { success: false; error: string }

/**
 * 決済サービスアダプター
 */
export class PaymentAdapter {
  constructor(readonly c: Context) {}

  /**
   * 決済を実行する
   */
  async charge(params: {
    amount: number
    currency: string
    customerId: string
  }): Promise<ChargeResult> {
    const response = await fetch("https://api.payment.example.com/charges", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${this.c.env.PAYMENT_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(params),
    })

    if (!response.ok) {
      return { success: false, error: "決済に失敗しました" }
    }

    const data = await response.json()
    return { success: true, chargeId: data.id }
  }

  /**
   * 返金を実行する
   */
  async refund(chargeId: string): Promise<RefundResult> {
    const response = await fetch(
      `https://api.payment.example.com/charges/${chargeId}/refund`,
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${this.c.env.PAYMENT_API_KEY}`,
        },
      }
    )

    if (!response.ok) {
      return { success: false, error: "返金に失敗しました" }
    }

    return { success: true }
  }
}
```

## 実装パターン (GraphQL API)

```ts
// infrastructure/adapters/external-api.adapter.ts
import type { Context } from "@/env"

// GraphQL クエリ定義
const GET_USER_QUERY = `
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
    }
  }
`

type GetUserResult =
  | { success: true; user: User }
  | { success: false; error: string }

/**
 * 外部 API アダプター (GraphQL)
 */
export class ExternalApiAdapter {
  constructor(readonly c: Context) {}

  async getUser(userId: string): Promise<GetUserResult> {
    const response = await fetch("https://api.example.com/graphql", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${this.c.env.EXTERNAL_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: GET_USER_QUERY,
        variables: { id: userId },
      }),
    })

    if (!response.ok) {
      return { success: false, error: "API呼び出しに失敗しました" }
    }

    const { data, errors } = await response.json()

    if (errors?.length > 0) {
      return { success: false, error: errors[0].message }
    }

    if (!data.user) {
      return { success: false, error: "ユーザーが見つかりません" }
    }

    return { success: true, user: data.user }
  }
}
```

## 設計原則

### 1. 戻り値パターン

成功/失敗を明示的に表現:

```ts
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string }
```

### 2. Context 注入

```ts
constructor(readonly c: Context) {}
```

### 3. エラーハンドリング

```ts
async getData(id: string): Promise<GetDataResult> {
  try {
    const response = await fetch(...)

    if (!response.ok) {
      return { success: false, error: "API呼び出しに失敗しました" }
    }

    const data = await response.json()
    return { success: true, data }
  } catch (error) {
    return { success: false, error: "ネットワークエラーが発生しました" }
  }
}
```

## Service からの使用

```ts
export class ProcessOrder {
  constructor(
    readonly c: Context,
    readonly deps = {
      orderRepository: new OrderRepository(c),
      paymentAdapter: new PaymentAdapter(c),
    },
  ) {}

  async execute(props: Props): Promise<Result | ExternalServiceError> {
    const { orderRepository, paymentAdapter } = this.deps

    // 決済実行
    const chargeResult = await paymentAdapter.charge({
      amount: props.amount,
      currency: "JPY",
      customerId: props.customerId,
    })

    if (!chargeResult.success) {
      return new ExternalServiceError("決済に失敗しました")
    }

    // 注文作成
    const order = OrderEntity.create({
      customerId: props.customerId,
      chargeId: chargeResult.chargeId,
      amount: props.amount,
    })

    await orderRepository.save(order)

    return { order }
  }
}
```

## メール送信 Adapter

メール送信も外部サービス連携なので Adapter として実装する。

```ts
// infrastructure/adapters/email.adapter.ts
import type { Context } from "@/env"

type SendEmailParams = {
  to: string
  subject: string
  html: string
}

type SendEmailResult =
  | { success: true }
  | { success: false; error: string }

/**
 * メール送信アダプター
 */
export class EmailAdapter {
  constructor(readonly c: Context) {}

  async send(params: SendEmailParams): Promise<SendEmailResult> {
    const response = await fetch("https://api.email.example.com/send", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${this.c.env.EMAIL_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: "noreply@example.com",
        to: params.to,
        subject: params.subject,
        html: params.html,
      }),
    })

    if (!response.ok) {
      return { success: false, error: "メール送信に失敗しました" }
    }

    return { success: true }
  }

  /**
   * パスワードリセットメールを送信
   */
  async sendPasswordReset(params: {
    to: string
    userName: string
    resetUrl: string
  }): Promise<SendEmailResult> {
    return this.send({
      to: params.to,
      subject: "パスワードリセット",
      html: `
        <h1>パスワードリセット</h1>
        <p>${params.userName} 様</p>
        <p>以下のリンクからパスワードをリセットしてください:</p>
        <a href="${params.resetUrl}">${params.resetUrl}</a>
      `,
    })
  }
}
```
