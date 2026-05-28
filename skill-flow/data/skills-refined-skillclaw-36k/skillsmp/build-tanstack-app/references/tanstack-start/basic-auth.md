# BASIC 認証（サーバーミドルウェア）

TanStack Start の server middleware で BASIC 認証を実装する場合。

## Middleware

```ts
// src/middlewares/auth-middleware.ts
import { createMiddleware } from "@tanstack/react-start"

export const authMiddleware = createMiddleware().server(async ({ next }) => {
  // BASIC 認証ロジック
  return next()
})
```

## Config

```ts
// app.config.ts
import { authMiddleware } from "./src/middlewares/auth-middleware"

export default defineConfig({
  server: {
    middleware: [authMiddleware],
  },
})
```
