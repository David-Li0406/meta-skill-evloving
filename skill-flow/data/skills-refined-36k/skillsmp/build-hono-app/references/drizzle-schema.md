# Drizzle Schema 定義

## 概要

Drizzle ORM を使用した SQLite (Cloudflare D1) スキーマ定義。
テーブル定義、リレーション、型推論のパターン。

## テーブル定義パターン

```ts
// drizzle.schema.ts
import { sqliteTable, text, integer, real } from "drizzle-orm/sqlite-core"
import { relations } from "drizzle-orm"

// 基本テーブル
export const customers = sqliteTable("customers", {
  // ID: UUID 文字列
  id: text("id", { length: 36 }).primaryKey(),

  // 外部キー
  shopId: text("shop_id", { length: 36 }).notNull(),

  // 文字列フィールド
  email: text("email", { length: 256 }).notNull().unique(),
  firstName: text("first_name", { length: 64 }),
  lastName: text("last_name", { length: 64 }),
  phone: text("phone", { length: 32 }),

  // Enum (text + enum オプション)
  status: text("status", { enum: ["active", "inactive", "deleted"] })
    .notNull()
    .default("active"),
  gender: text("gender", { enum: ["male", "female", "other"] }),

  // 数値
  height: real("height"),
  weight: real("weight"),

  // 外部サービス連携 ID (必要に応じて追加)
  externalUserId: text("external_user_id", { length: 64 }).unique(),

  // タイムスタンプ (integer + mode: "timestamp")
  createdAt: integer("created_at", { mode: "timestamp" }).notNull(),
  updatedAt: integer("updated_at", { mode: "timestamp" }).notNull(),
  deletedAt: integer("deleted_at", { mode: "timestamp" }),
})
```

## リレーション定義

```ts
// 1:N リレーション
export const customersRelations = relations(customers, ({ many }) => ({
  addresses: many(customerAddresses),
  orders: many(orders),
}))

// N:1 リレーション
export const ordersRelations = relations(orders, ({ one }) => ({
  customer: one(customers, {
    fields: [orders.customerId],
    references: [customers.id],
  }),
}))

// N:N リレーション (中間テーブル)
export const productCategories = sqliteTable("product_categories", {
  productId: text("product_id", { length: 36 }).notNull(),
  categoryId: text("category_id", { length: 36 }).notNull(),
})

export const productCategoriesRelations = relations(
  productCategories,
  ({ one }) => ({
    product: one(products, {
      fields: [productCategories.productId],
      references: [products.id],
    }),
    category: one(categories, {
      fields: [productCategories.categoryId],
      references: [categories.id],
    }),
  })
)
```

## 命名規則

### テーブル名

- snake_case
- 複数形
- 例: `customers`, `customer_addresses`, `product_categories`

### カラム名

- snake_case
- 例: `created_at`, `external_user_id`, `first_name`

### 型マッピング

| TypeScript | SQLite | Drizzle |
|-----------|--------|---------|
| `string` | TEXT | `text()` |
| `number` (整数) | INTEGER | `integer()` |
| `number` (小数) | REAL | `real()` |
| `boolean` | INTEGER (0/1) | `integer({ mode: "boolean" })` |
| `Date` | INTEGER (Unix) | `integer({ mode: "timestamp" })` |
| `enum` | TEXT | `text({ enum: [...] })` |
| `JSON` | TEXT | `text({ mode: "json" })` |

## スキーマエクスポート

```ts
// lib/schema.ts
import * as schema from "@/drizzle.schema"
export { schema }

// または個別エクスポート
export {
  customers,
  customersRelations,
  orders,
  ordersRelations,
  // ...
} from "@/drizzle.schema"
```

## マイグレーション

```bash
# マイグレーション生成
bun run d1:build
# または
drizzle-kit generate

# ローカル適用
bun run d1:migrate
# または
wrangler d1 migrations apply <db-name> --local

# リモート適用
bun run d1:migrate:remote
# または
wrangler d1 migrations apply <db-name> --remote
```

## Repository での使用

```ts
import { eq } from "drizzle-orm"
import { customers } from "@/drizzle.schema"

export class CustomerRepository {
  constructor(private readonly c: Context) {}

  private get db() {
    return this.c.var.database
  }

  // 型推論: typeof customers.$inferSelect
  async findById(id: string) {
    return await this.db.query.customers.findFirst({
      where: eq(customers.id, id),
    })
  }

  // 型推論: typeof customers.$inferInsert
  async create(data: typeof customers.$inferInsert) {
    return await this.db.insert(customers).values(data).returning()
  }

  // リレーション込みで取得
  async findByIdWithOrders(id: string) {
    return await this.db.query.customers.findFirst({
      where: eq(customers.id, id),
      with: {
        orders: true,
        addresses: true,
      },
    })
  }
}
```

## 型推論

```ts
// テーブルから型を推論
type Customer = typeof customers.$inferSelect
type NewCustomer = typeof customers.$inferInsert

// Repository の戻り値
async findById(id: string): Promise<Customer | null> {
  // ...
}
```
