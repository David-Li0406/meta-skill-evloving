# Value Object 実装パターン

## 概要

Value Object は値で識別されるイミュータブルなオブジェクト。
ドメインの概念を型安全に表現し、バリデーションを内包する。

## 種類

### 1. 単純値オブジェクト

単一の値をラップする。

```ts
import { z } from "zod"

const zValue = z.string().email()

/**
 * メールアドレス
 */
export class EmailValue {
  readonly value: string

  constructor(value: string) {
    this.value = zValue.parse(value)
    Object.freeze(this)
  }
}
```

### 2. 複合値オブジェクト

複数のフィールドを持つ。

```ts
import { z } from "zod"

const zProps = z.object({
  amount: z.number(),
  currency: z.enum(["JPY", "USD", "EUR"]),
})

type Props = z.infer<typeof zProps>

/**
 * 金額
 */
export class MoneyValue implements Props {
  readonly amount!: Props["amount"]
  readonly currency!: Props["currency"]

  constructor(props: Props) {
    Object.assign(this, zProps.parse(props))
    Object.freeze(this)
  }
}
```

### 3. 大規模複合値オブジェクト

多数のフィールドを持つ。

```ts
const zProps = z.object({
  street: z.string(),
  city: z.string(),
  state: z.string(),
  postalCode: z.string(),
  country: z.string(),
  // ... 必要に応じて追加
})

type Props = z.infer<typeof zProps>

/**
 * 住所
 */
export class AddressValue implements Props {
  readonly street!: Props["street"]
  readonly city!: Props["city"]
  readonly state!: Props["state"]
  readonly postalCode!: Props["postalCode"]
  readonly country!: Props["country"]

  constructor(props: Props) {
    Object.assign(this, zProps.parse(props))
    Object.freeze(this)
  }

  /**
   * フルアドレスを取得する
   */
  get fullAddress(): string {
    return `${this.postalCode} ${this.state}${this.city}${this.street}`
  }
}
```

## 命名規則

| 種類 | クラス名 | ファイル名 |
|------|---------|-----------|
| ID | `IdValue` | `id.value.ts` |
| メール | `EmailValue` | `email.value.ts` |
| 名前 | `NameValue` | `name.value.ts` |
| パスワード | `PasswordValue` | `password.value.ts` |
| 金額 | `MoneyValue` | `money.value.ts` |
| 住所 | `AddressValue` | `address.value.ts` |

## 設計原則

### 1. イミュータブル

```ts
constructor(props: Props) {
  Object.assign(this, zProps.parse(props))
  Object.freeze(this)  // 変更不可
}
```

### 2. バリデーション内包

```ts
// Zod で constructor 内でバリデーション
constructor(value: string) {
  this.value = zValue.parse(value)  // 不正な値は例外
}
```

### 3. Entity との違い

| 特性 | Entity | Value Object |
|------|--------|--------------|
| 識別 | ID で識別 | 値で識別 |
| 可変性 | イミュータブル (with* で新規作成) | イミュータブル |
| ライフサイクル | あり (createdAt, updatedAt) | なし |
| 等価性 | ID が同じなら同一 | 全フィールドが同じなら同一 |

## 実装例: パスワード

```ts
import { z } from "zod"
import { hashSync, compareSync } from "bcrypt-ts"

const zValue = z.string().min(8)

/**
 * パスワード
 */
export class PasswordValue {
  readonly value: string

  constructor(value: string) {
    this.value = zValue.parse(value)
    Object.freeze(this)
  }

  /**
   * ハッシュ化する
   */
  hash(): HashedPasswordValue {
    return new HashedPasswordValue(hashSync(this.value, 10))
  }
}

/**
 * ハッシュ化済みパスワード
 */
export class HashedPasswordValue {
  constructor(readonly value: string) {
    Object.freeze(this)
  }

  /**
   * パスワードを検証する
   */
  verify(password: string): boolean {
    return compareSync(password, this.value)
  }
}
```

## 実装例: 住所 (複合)

```ts
const zProps = z.object({
  postalCode: z.string().regex(/^\d{3}-\d{4}$/, "郵便番号の形式が不正です"),
  prefecture: z.string().min(1, "都道府県は必須です"),
  city: z.string().min(1, "市区町村は必須です"),
  street: z.string().min(1, "番地は必須です"),
  building: z.string().optional(),
})

type Props = z.infer<typeof zProps>

/**
 * 住所
 */
export class AddressValue implements Props {
  readonly postalCode!: Props["postalCode"]
  readonly prefecture!: Props["prefecture"]
  readonly city!: Props["city"]
  readonly street!: Props["street"]
  readonly building!: Props["building"]

  constructor(props: Props) {
    Object.assign(this, zProps.parse(props))
    Object.freeze(this)
  }

  /**
   * フルアドレスを取得する
   */
  get fullAddress(): string {
    const base = `〒${this.postalCode} ${this.prefecture}${this.city}${this.street}`
    return this.building ? `${base} ${this.building}` : base
  }
}
```
