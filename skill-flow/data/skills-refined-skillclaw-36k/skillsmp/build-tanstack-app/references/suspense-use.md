# Suspense + use() Pattern

React 19 の use() フックと Suspense を組み合わせたデータフェッチング。

## Basic Pattern

### Parent Component

```tsx
import { useQuery } from "@tanstack/react-query"
import { Suspense } from "react"
import { client } from "@/lib/client"

const endpoint = client.api.posts

export function TimelineContent() {
  const query = useQuery({
    queryKey: [endpoint.$url().href],
    async queryFn() {
      const resp = await endpoint.$get()
      const data = await resp.json()
      return data
    },
  })

  return (
    <Suspense fallback={<ContentFallback />}>
      <PostList query={query} />
    </Suspense>
  )
}
```

### Child Component

```tsx
import type { UseQueryResult } from "@tanstack/react-query"
import type { InferResponseType } from "hono/client"
import { use } from "react"
import { client } from "@/lib/client"

const endpoint = client.api.posts

type Props = {
  query: UseQueryResult<InferResponseType<typeof endpoint.$get>>
}

export function PostList(props: Props) {
  const result = use(props.query.promise)

  if (result.posts.length === 0) {
    return <Empty message="投稿がありません" />
  }

  return (
    <div className="flex flex-col gap-4">
      {result.posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  )
}
```

## Key Points

### endpoint パターン

```ts
const endpoint = client.api.posts

// queryKey に URL を使う
queryKey: [endpoint.$url().href]

// 型推論
type Response = InferResponseType<typeof endpoint.$get>
```

### Props の型

```ts
type Props = {
  query: UseQueryResult<InferResponseType<typeof endpoint.$get>>
}
```

### use() でデータ取得

```ts
const result = use(props.query.promise)
// result.posts を直接使う
```

## With Query Parameters

```tsx
const endpoint = client.api.posts

export function TimelineContent() {
  const [type, setType] = useState<"hitokoto" | "playlog">("playlog")

  const query = useQuery({
    queryKey: [endpoint.$url().href, type],
    async queryFn() {
      const resp = await endpoint.$get({ query: { type } })
      const data = await resp.json()
      return data
    },
  })

  return (
    <Suspense fallback={<ContentFallback />}>
      <PostList query={query} />
    </Suspense>
  )
}
```

## With Actions

```tsx
const endpoint = client.api.posts

export function TimelineContent() {
  const query = useQuery({
    queryKey: [endpoint.$url().href],
    async queryFn() {
      const resp = await endpoint.$get()
      return await resp.json()
    },
  })

  const mutation = useMutation({
    async mutationFn(postId: string) {
      await client.api.posts[":id"].reactions.$post({
        param: { id: postId },
      })
    },
    onSuccess() {
      query.refetch()
    },
  })

  return (
    <Suspense fallback={<ContentFallback />}>
      <PostList
        query={query}
        onReaction={(id) => mutation.mutate(id)}
      />
    </Suspense>
  )
}
```

## Skeleton Fallback

```tsx
export function ContentFallback() {
  return (
    <div className="flex flex-col gap-4">
      <PostCardSkeleton />
      <PostCardSkeleton />
      <PostCardSkeleton />
    </div>
  )
}

export function PostCardSkeleton() {
  return (
    <Card className="p-4">
      <div className="flex items-start gap-3">
        <Skeleton className="size-10 rounded-full" />
        <div className="flex flex-1 flex-col gap-2">
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-3/4" />
        </div>
      </div>
    </Card>
  )
}
```
