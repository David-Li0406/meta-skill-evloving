# Hono API Pattern

Hono を使った型安全な API 実装パターン。

## Factory Setup

```ts
// src/api/factory.ts
import { createFactory } from "hono/factory"
import type { HonoEnv } from "@/api/types"

export const factory = createFactory<HonoEnv>()
```

## Environment Types

```ts
// src/api/types.ts
import type { DrizzleD1Database } from "drizzle-orm/d1"
import type * as schema from "@/schema"

export type HonoEnv = {
  Bindings: Cloudflare.Env
  Variables: {
    database: DrizzleD1Database<typeof schema>
    userId: string | null
  }
}
```

## Route Handler

1ファイル1ハンドラ。zValidator で入力検証。

```ts
// src/api/routes/posts.list.ts
import { zValidator } from "@hono/zod-validator"
import { desc, eq } from "drizzle-orm"
import { z } from "zod"
import { factory } from "@/api/factory"
import { posts } from "@/schema"

export const GET = factory.createHandlers(
  zValidator(
    "query",
    z.object({
      type: z.enum(["hitokoto", "playlog"]).optional(),
      limit: z.coerce.number().min(1).max(100).default(20),
      offset: z.coerce.number().min(0).default(0),
    }),
  ),
  async (c) => {
    const query = c.req.valid("query")
    const db = c.get("database")

    const result = await db.query.posts.findMany({
      where: query.type ? eq(posts.type, query.type) : undefined,
      orderBy: [desc(posts.createdAt)],
      limit: query.limit,
      offset: query.offset,
    })

    return c.json({ posts: result })
  },
)
```

## POST Handler with Auth

```ts
// src/api/routes/posts.create.ts
import { zValidator } from "@hono/zod-validator"
import { z } from "zod"
import { factory } from "@/api/factory"
import { authMiddleware, getAuthUserId } from "@/api/middlewares/auth-middleware"
import { posts } from "@/schema"

export const POST = factory.createHandlers(
  authMiddleware,
  zValidator(
    "json",
    z.object({
      type: z.enum(["hitokoto", "playlog"]),
      content: z.string().min(1).max(500),
    }),
  ),
  async (c) => {
    const body = c.req.valid("json")
    const db = c.get("database")
    const userId = getAuthUserId(c)

    const id = crypto.randomUUID()

    await db.insert(posts).values({
      id,
      userId,
      type: body.type,
      content: body.content,
    })

    return c.json({ id }, 201)
  },
)
```

## App Router

ルートを1箇所で集約し、型をエクスポート。

```ts
// src/api/app.ts
import { contextStorage } from "hono/context-storage"
import { cors } from "hono/cors"
import { factory } from "@/api/factory"
import { databaseMiddleware } from "@/api/middlewares/database-middleware"
import * as postsList from "@/api/routes/posts.list"
import * as postsCreate from "@/api/routes/posts.create"
import { onErrorJson } from "@/api/utils/on-error-json"

const app = factory.createApp()

app.use("*", cors())
app.use(contextStorage())
app.use(databaseMiddleware)
app.onError(onErrorJson)

export const routes = app
  .get("/api/posts", ...postsList.GET)
  .post("/api/posts", ...postsCreate.POST)

export type AppType = typeof routes
```

## Middleware

```ts
// src/api/middlewares/database-middleware.ts
import { drizzle } from "drizzle-orm/d1"
import { HTTPException } from "hono/http-exception"
import { factory } from "@/api/factory"
import * as schema from "@/schema"

export const databaseMiddleware = factory.createMiddleware((c, next) => {
  if (!c.env.DB) {
    throw new HTTPException(500, { message: "Database not configured" })
  }

  const client = drizzle(c.env.DB, { schema })
  c.set("database", client)

  return next()
})
```

## Error Handler

```ts
// src/api/utils/on-error-json.ts
import type { ErrorHandler } from "hono"
import { HTTPException } from "hono/http-exception"

export const onErrorJson: ErrorHandler = (err, c) => {
  if (err instanceof HTTPException) {
    return c.json({ message: err.message }, err.status)
  }
  console.error(err)
  return c.json({ message: "Internal Server Error" }, 500)
}
```

## Path Parameters

```ts
// src/api/routes/posts.flag.ts
export const PATCH = factory.createHandlers(
  authMiddleware,
  zValidator("param", z.object({ id: z.string() })),
  zValidator("json", z.object({ flag: z.string().nullable() })),
  async (c) => {
    const param = c.req.valid("param")
    const body = c.req.valid("json")
    const db = c.get("database")

    await db.update(posts).set({ flag: body.flag }).where(eq(posts.id, param.id))

    return c.json({ success: true })
  },
)
```
