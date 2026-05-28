# Entity 実装パターン

## 概要

Entity はビジネスドメインの核となるオブジェクト。
ID で識別され、ライフサイクル (作成・更新・削除) を持つ。

## 設計原則

### 1. イミュータブル設計
- constructor で `Object.freeze(this)`
- 更新は新しいインスタンスを返す

### 2. Zod スキーマでバリデーション
- `zProps` でプロパティを定義
- constructor で `zProps.parse(props)` を実行

### 3. Fluent API
- `with*()` メソッドで更新
- メソッドチェーンが可能

### 4. ファクトリメソッド

Entity にファクトリメソッドを定義する。
本来はファクトリは別クラス (Factory パターン) にするべきだが、使いやすさを優先してEntity 内に定義する。

- `createXxx()` - 新規作成 (例: `createWithEmail()`, `createFromSignup()`)
- メソッド名は具体的に。単なる `create()` より意図が伝わる名前が望ましい

**注意**: `fromRecord()` のような DB レコードからの復元メソッドは Entity に定義しない。
ドメイン層が DB の存在を知っているのは設計上問題がある。
DB レコードから Entity への変換は Repository (インフラ層) の責務として実装する。

## 命名規則

| 種類 | 命名 | 例 |
|------|------|-----|
| クラス名 | `XxxEntity` | `CustomerEntity` |
| ファイル名 | `xxx.entity.ts` | `customer.entity.ts` |
| ファクトリ | `createXxx()` | `createWithEmail()`, `createFromSignup()` |
| 更新メソッド | `with*()` | `withName()`, `withEmail()` |
| 状態変更 | 動詞 | `activate()`, `delete()`, `cancel()` |
| 状態取得 | `is*`, `has*`, `can*` | `isDeleted`, `hasAddress` |

## 実装例

```ts
import { z } from "zod"

// Zod スキーマ定義
const zProps = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  status: z.enum(["active", "inactive", "deleted"]),
  createdAt: z.date(),
  updatedAt: z.date(),
  deletedAt: z.date().nullable(),
})

type Props = z.infer<typeof zProps>

/**
 * 顧客
 * サービスを利用する顧客を表す。
 */
export class CustomerEntity implements Props {
  readonly id!: Props["id"]

  /**
   * 名前
   */
  readonly name!: Props["name"]

  /**
   * メールアドレス
   */
  readonly email!: Props["email"]

  /**
   * ステータス
   */
  readonly status!: Props["status"]

  readonly createdAt!: Props["createdAt"]
  readonly updatedAt!: Props["updatedAt"]
  readonly deletedAt!: Props["deletedAt"]

  constructor(props: Props) {
    Object.assign(this, zProps.parse(props))
    Object.freeze(this)
  }

  // --- 更新メソッド (with* パターン) ---

  /**
   * 名前を更新する
   */
  withName(name: string) {
    return new CustomerEntity({
      ...this,
      name,
      updatedAt: new Date(),
    })
  }

  /**
   * メールアドレスを更新する
   */
  withEmail(email: string) {
    return new CustomerEntity({
      ...this,
      email,
      updatedAt: new Date(),
    })
  }

  // --- 状態変更メソッド ---

  /**
   * 有効化する
   */
  activate() {
    return new CustomerEntity({
      ...this,
      status: "active",
      updatedAt: new Date(),
    })
  }

  /**
   * 削除する (論理削除)
   */
  delete() {
    return new CustomerEntity({
      ...this,
      status: "deleted",
      deletedAt: new Date(),
      updatedAt: new Date(),
    })
  }

  // --- 状態取得ゲッター ---

  /**
   * 削除済みである
   */
  get isDeleted() {
    return this.deletedAt !== null
  }

  /**
   * 有効である
   */
  get isActive() {
    return this.status === "active"
  }

  // --- ファクトリメソッド ---

  /**
   * メールアドレスで新規作成
   * 通常のサインアップフローで使用
   */
  static createWithEmail(params: { name: string; email: string }) {
    const now = new Date()
    return new CustomerEntity({
      id: crypto.randomUUID(),
      name: params.name,
      email: params.email,
      status: "active",
      createdAt: now,
      updatedAt: now,
      deletedAt: null,
    })
  }

  /**
   * 招待から新規作成
   * 管理者が招待したユーザーを作成する場合
   */
  static createFromInvitation(params: {
    name: string
    email: string
    invitedBy: string
  }) {
    const now = new Date()
    return new CustomerEntity({
      id: crypto.randomUUID(),
      name: params.name,
      email: params.email,
      status: "inactive", // 招待は未有効化状態で作成
      createdAt: now,
      updatedAt: now,
      deletedAt: null,
    })
  }
}
```
