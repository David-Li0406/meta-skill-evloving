# Authentication Pattern

JWT + Cookie ベースの認証実装。

## Auth Middleware

```ts
// src/api/middlewares/auth-middleware.ts
import type { Context } from "hono"
import { getCookie } from "hono/cookie"
import { HTTPException } from "hono/http-exception"
import { factory } from "@/api/factory"
import type { HonoEnv } from "@/api/types"
import { verifySessionToken } from "@/lib/session"

/**
 * authMiddleware 通過後の userId を取得
 */
export function getAuthUserId(c: Context<HonoEnv>): string {
  const userId = c.get("userId")
  if (!userId) {
    throw new HTTPException(401, { message: "認証エラー" })
  }
  return userId
}

/**
 * 認証ミドルウェア
 * セッション Cookie を検証し、userId を context にセット
 */
export const authMiddleware = factory.createMiddleware(async (c, next) => {
  const sessionCookie = getCookie(c, "session")

  if (!sessionCookie) {
    throw new HTTPException(401, { message: "認証が必要です" })
  }

  const jwtSecret = c.env.JWT_SECRET

  if (!jwtSecret) {
    throw new HTTPException(500, { message: "JWT_SECRET not configured" })
  }

  try {
    const payload = await verifySessionToken(sessionCookie, jwtSecret)
    c.set("userId", payload.userId)
    await next()
  } catch {
    throw new HTTPException(401, { message: "認証エラー" })
  }
})
```

## Session Token

```ts
// src/lib/session.ts
import { SignJWT, jwtVerify } from "jose"

type SessionPayload = {
  userId: string
}

export async function createSessionToken(
  userId: string,
  secret: string,
): Promise<string> {
  const key = new TextEncoder().encode(secret)
  return new SignJWT({ userId })
    .setProtectedHeader({ alg: "HS256" })
    .setExpirationTime("7d")
    .sign(key)
}

export async function verifySessionToken(
  token: string,
  secret: string,
): Promise<SessionPayload> {
  const key = new TextEncoder().encode(secret)
  const { payload } = await jwtVerify(token, key)
  return payload as SessionPayload
}
```

## Login Handler

```ts
// src/api/routes/auth.login.ts
import { zValidator } from "@hono/zod-validator"
import { compare } from "bcryptjs"
import { eq } from "drizzle-orm"
import { setCookie } from "hono/cookie"
import { HTTPException } from "hono/http-exception"
import { z } from "zod"
import { factory } from "@/api/factory"
import { createSessionToken } from "@/lib/session"
import { users } from "@/schema"

export const POST = factory.createHandlers(
  zValidator(
    "json",
    z.object({
      email: z.string().email(),
      password: z.string().min(1),
    }),
  ),
  async (c) => {
    const body = c.req.valid("json")
    const db = c.get("database")

    const user = await db.query.users.findFirst({
      where: eq(users.email, body.email),
    })

    if (!user) {
      throw new HTTPException(401, { message: "メールまたはパスワードが違います" })
    }

    const valid = await compare(body.password, user.passwordHash)

    if (!valid) {
      throw new HTTPException(401, { message: "メールまたはパスワードが違います" })
    }

    const token = await createSessionToken(user.id, c.env.JWT_SECRET)

    setCookie(c, "session", token, {
      httpOnly: true,
      secure: true,
      sameSite: "Lax",
      maxAge: 60 * 60 * 24 * 7, // 7 days
      path: "/",
    })

    return c.json({ user: { id: user.id, name: user.name, role: user.role } })
  },
)
```

## Session Check Handler

```ts
// src/api/routes/auth.session.ts
import { eq } from "drizzle-orm"
import { getCookie } from "hono/cookie"
import { factory } from "@/api/factory"
import { verifySessionToken } from "@/lib/session"
import { users } from "@/schema"

export const GET = factory.createHandlers(async (c) => {
  const sessionCookie = getCookie(c, "session")

  if (!sessionCookie) {
    return c.json({ user: null })
  }

  try {
    const payload = await verifySessionToken(sessionCookie, c.env.JWT_SECRET)
    const db = c.get("database")

    const user = await db.query.users.findFirst({
      where: eq(users.id, payload.userId),
      columns: {
        id: true,
        email: true,
        name: true,
        role: true,
        avatarUrl: true,
      },
    })

    return c.json({ user: user ?? null })
  } catch {
    return c.json({ user: null })
  }
})
```

## Logout Handler

```ts
// src/api/routes/auth.logout.ts
import { deleteCookie } from "hono/cookie"
import { factory } from "@/api/factory"

export const POST = factory.createHandlers(async (c) => {
  deleteCookie(c, "session", { path: "/" })
  return c.json({ success: true })
})
```

## Protected Route Usage

```ts
// authMiddleware を最初に配置
export const POST = factory.createHandlers(
  authMiddleware,
  zValidator("json", schema),
  async (c) => {
    const userId = getAuthUserId(c)
    // userId が保証される
  },
)
```

## Admin Check

```ts
export const GET = factory.createHandlers(
  authMiddleware,
  async (c) => {
    const userId = getAuthUserId(c)
    const db = c.get("database")

    const user = await db.query.users.findFirst({
      where: eq(users.id, userId),
    })

    if (user?.role !== "admin") {
      throw new HTTPException(403, { message: "管理者権限が必要です" })
    }

    // 管理者のみ実行可能な処理
  },
)
```

