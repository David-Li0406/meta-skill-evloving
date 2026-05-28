# Cloudflare Workers Integration

Cloudflare Workers + D1 を使う場合の固有設定。

## HonoEnv

```ts
// src/api/types.ts
import type { DrizzleD1Database } from "drizzle-orm/d1"
import type * as schema from "@/schema"

export type HonoEnv = {
  Bindings: Cloudflare.Env  // Cloudflare 固有
  Variables: {
    database: DrizzleD1Database<typeof schema>
    userId: string | null
  }
}
```

## Database Middleware

```ts
// src/api/middlewares/database-middleware.ts
import { drizzle } from "drizzle-orm/d1"
import { HTTPException } from "hono/http-exception"
import { factory } from "@/api/factory"
import * as schema from "@/schema"

export const databaseMiddleware = factory.createMiddleware((c, next) => {
  if (!c.env.DB) {  // Cloudflare D1 binding
    throw new HTTPException(500, { message: "Database not configured" })
  }

  const client = drizzle(c.env.DB, { schema })
  c.set("database", client)

  return next()
})
```

## drizzle.config.ts

ローカル D1（Wrangler が生成する sqlite ファイル）に drizzle-kit で接続するための設定。

```ts
import { existsSync, readdirSync } from "node:fs"
import { defineConfig } from "drizzle-kit"

export default defineConfig({
  out: "drizzle",
  schema: "src/schema.ts",
  dialect: "sqlite",
  get dbCredentials() {
    const hasDatabase = existsSync(
      ".wrangler/state/v3/d1/miniflare-D1DatabaseObject",
    )

    if (hasDatabase === false) {
      return { url: ":memory:" }
    }

    const fileNames = readdirSync(
      ".wrangler/state/v3/d1/miniflare-D1DatabaseObject",
    )

    const fileName = fileNames.find((fileName) => {
      return fileName.endsWith(".sqlite")
    })

    if (fileName === undefined) {
      return { url: ":memory:" }
    }

    return {
      url: `.wrangler/state/v3/d1/miniflare-D1DatabaseObject/${fileName}`,
    }
  },
})
```

D1 はローカル開発時 `.wrangler/state/v3/d1/` に sqlite ファイルを生成する。この設定でそのファイルを自動検出して `bun drizzle-kit studio` で接続できる。
