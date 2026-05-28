# Session Context Pattern

React Context + React Query でセッション管理。

## Context Definition

Proxy で Provider 未設定時のエラーを検出。

```ts
// src/contexts/session-context.ts
import { createContext } from "react"

type User = {
  id: string
  email: string
  name: string
  role: string
  avatarUrl: string | null
}

type Value = {
  user: User | null
  isLoading: boolean
  signOut(): Promise<void>
  refresh(): Promise<void>
}

const proxy = new Proxy({} as Value, {
  get() {
    throw new Error("SessionContext must be provided")
  },
})

export const SessionContext = createContext<Value>(proxy)
```

## Provider Implementation

```tsx
// src/components/session-provider.tsx
import { useQuery } from "@tanstack/react-query"
import { SessionContext } from "@/contexts/session-context"
import { client } from "@/lib/client"

type Props = {
  children: React.ReactNode
}

const endpoint = client.api.auth.session

export function SessionProvider(props: Props) {
  const query = useQuery({
    queryKey: [endpoint.$url().href],
    async queryFn() {
      const resp = await endpoint.$get()
      const data = await resp.json()
      return data.user ?? null
    },
    staleTime: 1000 * 60 * 5,
    retry: false,
  })

  async function signOut() {
    await client.api.auth.sign.out.$post()
    await query.refetch()
  }

  async function refresh() {
    await query.refetch()
  }

  const value = {
    user: query.data ?? null,
    isLoading: query.isLoading,
    signOut,
    refresh,
  }

  return (
    <SessionContext.Provider value={value}>
      {props.children}
    </SessionContext.Provider>
  )
}
```

## Custom Hook

```ts
// src/hooks/use-session.ts
import { useContext } from "react"
import { SessionContext } from "@/contexts/session-context"

export function useSession() {
  return useContext(SessionContext)
}
```

## Usage in Components

```tsx
import { useSession } from "@/hooks/use-session"

export function UserMenu() {
  const session = useSession()

  if (session.isLoading) {
    return <Skeleton />
  }

  if (!session.user) {
    return <LoginButton />
  }

  return (
    <div>
      <span>{session.user.name}</span>
      <Button onClick={session.signOut}>ログアウト</Button>
    </div>
  )
}
```

## Role-Based UI

```tsx
export function PostCard(props: Props) {
  const session = useSession()
  const isAdmin = session.user?.role === "admin"

  return (
    <Card>
      {/* 共通コンテンツ */}

      {isAdmin && (
        <>
          <Separator />
          <AdminActions post={props.post} />
        </>
      )}
    </Card>
  )
}
```

## Key Points

- useQuery でセッション状態を管理
- refetch でログアウト後の状態更新
- Proxy で Provider 未設定を検出
