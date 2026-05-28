# Repository 実装パターン

## 概要

Repository はデータアクセスを抽象化するレイヤー。
Domain 層の Entity と Infrastructure 層の DB を橋渡しする。

## 設計原則

### 1. Context 注入
- constructor で Context を受け取る
- DB インスタンスは `c.var.database` から取得

### 2. Entity 変換 (Repository の責務)

DB レコードから Entity への変換は Repository の責務。
Entity に `fromRecord()` のような DB 依存のメソッドを定義しない。

- DB レコード → Entity: Repository 内で `new Entity()` を呼び出す
- Entity → DB データ: 直接マッピング

### 3. null 安全
- 見つからない場合は `null` を返す
- 存在確認は呼び出し側で行う

## 命名規則

| メソッド | 用途 | 戻り値 |
|---------|------|--------|
| `findById()` | ID で取得 | `Entity \| null` |
| `findBy*()` | 条件で取得 | `Entity \| null` |
| `findAll()` | 全件取得 | `Entity[]` |
| `findAllBy*()` | 条件で複数取得 | `Entity[]` |
| `save()` | 保存 (insert/update) | `void` |
| `delete()` | 削除 | `void` |
| `upsert()` | 存在すれば更新、なければ作成 | `void` |
| `upsertBy*()` | 特定キーで upsert | `void` |

## 実装例

```ts
import type { Context } from "hono"
import { eq } from "drizzle-orm"
import { customers } from "@/drizzle.schema"
import { CustomerEntity } from "@/domain/entities/customer.entity"

/**
 * 顧客リポジトリ
 */
export class CustomerRepository {
  constructor(private readonly c: Context) {}

  /**
   * DB インスタンスを取得する
   */
  private get db() {
    return this.c.var.database
  }

  /**
   * ID で顧客を取得する
   */
  async findById(id: string): Promise<CustomerEntity | null> {
    const record = await this.db
      .select()
      .from(customers)
      .where(eq(customers.id, id))
      .get()

    if (!record) return null

    // DB レコードから Entity への変換は Repository の責務
    return new CustomerEntity({
      id: record.id,
      name: record.name,
      email: record.email,
      status: record.status,
      createdAt: record.createdAt,
      updatedAt: record.updatedAt,
      deletedAt: record.deletedAt,
    })
  }

  /**
   * メールアドレスで顧客を取得する
   */
  async findByEmail(email: string): Promise<CustomerEntity | null> {
    const record = await this.db
      .select()
      .from(customers)
      .where(eq(customers.email, email))
      .get()

    if (!record) return null

    return new CustomerEntity({
      id: record.id,
      name: record.name,
      email: record.email,
      status: record.status,
      createdAt: record.createdAt,
      updatedAt: record.updatedAt,
      deletedAt: record.deletedAt,
    })
  }

  /**
   * 全件取得する
   */
  async findAll(): Promise<CustomerEntity[]> {
    const records = await this.db.select().from(customers).all()

    return records.map((record) => new CustomerEntity({
      id: record.id,
      name: record.name,
      email: record.email,
      status: record.status,
      createdAt: record.createdAt,
      updatedAt: record.updatedAt,
      deletedAt: record.deletedAt,
    }))
  }

  /**
   * 顧客を保存する
   */
  async save(entity: CustomerEntity): Promise<void> {
    await this.db
      .insert(customers)
      .values({
        id: entity.id,
        name: entity.name,
        email: entity.email,
        status: entity.status,
        createdAt: entity.createdAt,
        updatedAt: entity.updatedAt,
        deletedAt: entity.deletedAt,
      })
      .onConflictDoUpdate({
        target: customers.id,
        set: {
          name: entity.name,
          email: entity.email,
          status: entity.status,
          updatedAt: entity.updatedAt,
          deletedAt: entity.deletedAt,
        },
      })
      .run()
  }

  /**
   * 顧客を削除する (物理削除)
   */
  async delete(id: string): Promise<void> {
    await this.db.delete(customers).where(eq(customers.id, id)).run()
  }

  /**
   * メールアドレスで upsert する
   */
  async upsertByEmail(entity: CustomerEntity): Promise<void> {
    await this.db
      .insert(customers)
      .values({
        id: entity.id,
        name: entity.name,
        email: entity.email,
        status: entity.status,
        createdAt: entity.createdAt,
        updatedAt: entity.updatedAt,
        deletedAt: entity.deletedAt,
      })
      .onConflictDoUpdate({
        target: customers.email,
        set: {
          name: entity.name,
          status: entity.status,
          updatedAt: entity.updatedAt,
          deletedAt: entity.deletedAt,
        },
      })
      .run()
  }
}
```
