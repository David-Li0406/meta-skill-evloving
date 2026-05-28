# Hono hc Client

Hono の型安全な API クライアント。

## Client Setup

```ts
// src/lib/client.ts
import { hc } from "hono/client"
import type { AppType } from "@/api/app"

const endpoint =
  typeof window !== "undefined" ? location.origin : "http://localhost"

export const client = hc<AppType>(endpoint, {
  init: { credentials: "include", mode: "cors" },
  async fetch(input: URL | RequestInfo, init?: RequestInit) {
    const resp = await fetch(input, init)

    if (resp.ok === false) {
      const json = await resp.json<{ message: string }>()
      throw new Error(json.message)
    }

    return resp
  },
})
```

## Why hc Instead of fetch

- API ルートから型が自動推論される
- エンドポイントのタイポを防止
- レスポンス型が自動的に付与される
- 一箇所でエラーハンドリングを統一

## Usage Examples

### GET Request

```ts
const response = await client.api.posts.$get({
  query: { type: "playlog", limit: 20 },
})
const data = await response.json()
// data.posts は自動的に型付け
```

### POST Request

```ts
const response = await client.api.posts.$post({
  json: {
    type: "hitokoto",
    content: "今日のひとこと",
  },
})
const data = await response.json()
// data.id が返る
```

### Path Parameters

```ts
const response = await client.api.posts[":id"].reactions.$post({
  param: { id: postId },
})
```

### PATCH Request

```ts
await client.api.posts[":id"].flag.$patch({
  param: { id: postId },
  json: { flag: "good" },
})
```

### DELETE Request

```ts
await client.api.invites[":id"].$delete({
  param: { id: inviteId },
})
```

## Type Inference

```ts
import type { InferResponseType } from "hono/client"

// レスポンス型を取得
type PostsResponse = InferResponseType<typeof client.api.posts.$get>
type Post = PostsResponse["posts"][number]

// ネストした型を取得
type SessionResponse = InferResponseType<typeof client.api.auth.session.$get>
type User = NonNullable<SessionResponse["user"]>
```

## Error Handling

client.ts でエラーを throw するので、呼び出し側で catch：

```ts
async function createPost(content: string) {
  try {
    await client.api.posts.$post({ json: { type: "hitokoto", content } })
  } catch (error) {
    if (error instanceof Error) {
      toast.error(error.message)
    }
  }
}
```

## Do NOT Use

```ts
// Bad: 型安全性がない
const response = await fetch("/api/posts", {
  method: "POST",
  body: JSON.stringify({ content: "test" }),
})

// Good: 型安全
const response = await client.api.posts.$post({
  json: { type: "hitokoto", content: "test" },
})
```
