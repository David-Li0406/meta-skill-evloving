# エントリーポイント

## 概要

Hono アプリケーションのエントリーポイント構成。
ルーティング、ミドルウェア、エラーハンドリングの設定。

## index.ts

```ts
// api/index.ts
import { contextStorage } from "hono/context-storage"
import { cors } from "hono/cors"
import { HTTPException } from "hono/http-exception"
import { factory } from "@/interface/factory"
import { databaseMiddleware } from "@/interface/middlewares/database-middleware"

// ルートファイルをインポート
import * as customers from "@/interface/routes/customers"
import * as customers_$customer from "@/interface/routes/customers.$customer"
import * as customers_$customer_orders from "@/interface/routes/customers.$customer.orders"
// ... その他のルート

export default factory
  .createApp()
  // グローバルミドルウェア
  .use(contextStorage())
  .use(databaseMiddleware)
  .use("/*", cors({
    credentials: true,
    origin: (origin) => origin,
  }))

  // ルート定義
  .get("/customers", ...customers.GET)
  .post("/customers", ...customers.POST)
  .get("/customers/:customer", ...customers_$customer.GET)
  .put("/customers/:customer", ...customers_$customer.PUT)
  .delete("/customers/:customer", ...customers_$customer.DELETE)
  .get("/customers/:customer/orders", ...customers_$customer_orders.GET)
  .post("/customers/:customer/orders", ...customers_$customer_orders.POST)
  // ... その他のルート

  // エラーハンドラー
  .onError((error, c) => {
    console.error(error)

    if (error instanceof HTTPException) {
      return c.json({ message: error.message }, error.status)
    }

    return c.json({ message: "Internal Server Error" }, 500)
  })
```

## factory.ts

```ts
// interface/factory.ts
import { createFactory } from "hono/factory"
import type { HonoEnv } from "@/env"

export const factory = createFactory<HonoEnv>()
```

## env.d.ts

```ts
// api/env.d.ts
import type { InferOutput } from "valibot"
import type { DrizzleD1Database } from "drizzle-orm/d1"
import type { vSessionPayload } from "@/lib/session/session-payload"
import type { schema } from "@/lib/schema"

// Hono の Context 型
export type Context = {
  var: Variables
  env: Bindings
}

// Hono 環境型 (createFactory に渡す)
export type HonoEnv = {
  Bindings: Bindings
  Variables: Variables
}

// Cloudflare Workers 環境変数
export type Bindings = {
  DB: D1Database
  R2: R2Bucket
  // 外部サービス API キー (必要に応じて追加)
  EMAIL_API_KEY: string
  PAYMENT_API_KEY: string
  // ... その他の環境変数
}

// リクエストスコープの変数
export type Variables = {
  database: DrizzleD1Database<typeof schema> & { $client: D1Database }
  session: InferOutput<typeof vSessionPayload> | null
}
```

## database-middleware.ts

```ts
// interface/middlewares/database-middleware.ts
import { drizzle } from "drizzle-orm/d1"
import { factory } from "@/interface/factory"
import { schema } from "@/lib/schema"

export const databaseMiddleware = factory.createMiddleware(async (c, next) => {
  const db = drizzle(c.env.DB, { schema })
  c.set("database", db)
  return next()
})
```

## ルーティングパターン

### HTTP メソッドとファイルの対応

```ts
// interface/routes/customers.ts
export const GET = factory.createHandlers(...)   // GET /customers
export const POST = factory.createHandlers(...)  // POST /customers

// interface/routes/customers.$customer.ts
export const GET = factory.createHandlers(...)    // GET /customers/:customer
export const PUT = factory.createHandlers(...)    // PUT /customers/:customer
export const DELETE = factory.createHandlers(...) // DELETE /customers/:customer
```

### ルート登録パターン

```ts
// index.ts でのルート登録
.get("/customers", ...customers.GET)
.post("/customers", ...customers.POST)
.get("/customers/:customer", ...customers_$customer.GET)
.put("/customers/:customer", ...customers_$customer.PUT)
.delete("/customers/:customer", ...customers_$customer.DELETE)
```

### ネストしたルート

```ts
// customers.$customer.orders.ts → /customers/:customer/orders
.get("/customers/:customer/orders", ...customers_$customer_orders.GET)
.post("/customers/:customer/orders", ...customers_$customer_orders.POST)

// customers.$customer.orders.$id.ts → /customers/:customer/orders/:id
.get("/customers/:customer/orders/:id", ...customers_$customer_orders_$id.GET)
.put("/customers/:customer/orders/:id", ...customers_$customer_orders_$id.PUT)
```

## wrangler.toml

```toml
name = "api"
main = "index.ts"
compatibility_date = "2024-01-01"

[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

[[r2_buckets]]
binding = "R2"
bucket_name = "my-bucket"

[vars]
ENVIRONMENT = "production"
```

## package.json scripts

```json
{
  "scripts": {
    "dev": "drizzle-kit generate && wrangler d1 migrations apply <db> --local && wrangler dev --env local",
    "deploy": "wrangler deploy --minify",
    "check": "tsc --noEmit",
    "d1:build": "drizzle-kit generate",
    "d1:migrate": "wrangler d1 migrations apply <db> --local",
    "d1:migrate:remote": "wrangler d1 migrations apply <db> --remote"
  }
}
```
