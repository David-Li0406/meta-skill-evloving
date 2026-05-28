---
name: nextjs-page
description: Next.js App Routerでページとコンポーネントを作成。新規ページ、Server Component、Client Component作成時に使用。
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Next.js App Router ページ作成スキル

Katorin2プロジェクトでのNext.js 16 App Routerページ作成ガイドです。

## ディレクトリ構造

```
src/app/
├── (auth)/                    # 認証レイアウト
│   ├── layout.tsx
│   ├── login/page.tsx
│   └── register/page.tsx
├── (main)/                    # メインアプリレイアウト
│   ├── layout.tsx
│   ├── tournaments/
│   │   ├── [id]/
│   │   │   ├── page.tsx       # 大会詳細
│   │   │   ├── edit/page.tsx  # 編集
│   │   │   └── bracket/page.tsx
│   │   ├── new/page.tsx       # 新規作成
│   │   └── page.tsx           # 一覧
│   ├── teams/
│   ├── series/
│   └── my/
├── auth/callback/route.ts     # OAuth コールバック
├── layout.tsx                 # ルートレイアウト
└── page.tsx                   # ホーム
```

## Server Component（デフォルト）

データ取得を行うページはServer Componentとして実装：

```typescript
// src/app/(main)/tournaments/[id]/page.tsx
import { createClient } from '@/lib/supabase/server'
import { notFound } from 'next/navigation'
import { TournamentDetail } from '@/components/tournament/TournamentDetail'

interface Props {
  params: Promise<{ id: string }>
}

export async function generateMetadata({ params }: Props) {
  const { id } = await params
  const supabase = await createClient()

  const { data: tournament } = await supabase
    .from('tournaments')
    .select('title, description')
    .eq('id', id)
    .single()

  return {
    title: tournament?.title ?? '大会詳細',
    description: tournament?.description ?? ''
  }
}

export default async function TournamentPage({ params }: Props) {
  const { id } = await params
  const supabase = await createClient()

  // 大会データ取得
  const { data: tournament, error } = await supabase
    .from('tournaments')
    .select(`
      *,
      organizer:profiles(*),
      participants(*, user:profiles(*)),
      matches(*)
    `)
    .eq('id', id)
    .single()

  if (error || !tournament) {
    notFound()
  }

  // 認証ユーザー取得
  const { data: { user } } = await supabase.auth.getUser()

  const isOrganizer = user?.id === tournament.organizer_id

  return (
    <TournamentDetail
      tournament={tournament}
      isOrganizer={isOrganizer}
      currentUserId={user?.id}
    />
  )
}
```

## Client Component

インタラクションが必要な部分はClient Componentに分離：

```typescript
// src/components/tournament/TournamentActions.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import { Button } from '@/components/ui/button'

interface Props {
  tournamentId: string
  isOrganizer: boolean
}

export function TournamentActions({ tournamentId, isOrganizer }: Props) {
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()
  const supabase = createClient()

  const handleStart = async () => {
    setIsLoading(true)
    try {
      const { error } = await supabase
        .from('tournaments')
        .update({ status: 'in_progress' })
        .eq('id', tournamentId)

      if (error) throw error
      router.refresh()
    } catch (error) {
      console.error('Failed to start tournament:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (!isOrganizer) return null

  return (
    <Button onClick={handleStart} disabled={isLoading}>
      {isLoading ? '処理中...' : '大会を開始'}
    </Button>
  )
}
```

## フォームページ

```typescript
// src/app/(main)/tournaments/new/page.tsx
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import { TournamentForm } from '@/components/tournament/TournamentForm'

export const metadata = {
  title: '大会作成'
}

export default async function NewTournamentPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return (
    <div className="container max-w-2xl py-8">
      <h1 className="text-2xl font-bold mb-6">新しい大会を作成</h1>
      <TournamentForm />
    </div>
  )
}
```

## Server Actions

フォーム送信にはServer Actionsを使用：

```typescript
// src/app/(main)/tournaments/new/actions.ts
'use server'

import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import { revalidatePath } from 'next/cache'

export async function createTournament(formData: FormData) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    throw new Error('Unauthorized')
  }

  const title = formData.get('title') as string
  const description = formData.get('description') as string
  const format = formData.get('format') as string

  const { data, error } = await supabase
    .from('tournaments')
    .insert({
      title,
      description,
      tournament_format: format,
      organizer_id: user.id,
      status: 'draft'
    })
    .select()
    .single()

  if (error) {
    throw new Error(error.message)
  }

  revalidatePath('/tournaments')
  redirect(`/tournaments/${data.id}`)
}
```

## Loading UI

```typescript
// src/app/(main)/tournaments/[id]/loading.tsx
import { Skeleton } from '@/components/ui/skeleton'

export default function TournamentLoading() {
  return (
    <div className="container py-8">
      <Skeleton className="h-10 w-64 mb-4" />
      <Skeleton className="h-4 w-full mb-2" />
      <Skeleton className="h-4 w-3/4 mb-6" />
      <div className="grid grid-cols-2 gap-4">
        <Skeleton className="h-32" />
        <Skeleton className="h-32" />
      </div>
    </div>
  )
}
```

## Error Handling

```typescript
// src/app/(main)/tournaments/[id]/error.tsx
'use client'

import { useEffect } from 'react'
import { Button } from '@/components/ui/button'

export default function TournamentError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div className="container py-8 text-center">
      <h2 className="text-xl font-bold mb-4">
        エラーが発生しました
      </h2>
      <p className="text-muted-foreground mb-4">
        {error.message}
      </p>
      <Button onClick={reset}>
        もう一度試す
      </Button>
    </div>
  )
}
```

## パターン: 一覧 + 詳細

```typescript
// 一覧ページ: src/app/(main)/tournaments/page.tsx
export default async function TournamentsPage() {
  const supabase = await createClient()

  const { data: tournaments } = await supabase
    .from('tournaments')
    .select('*, organizer:profiles(display_name, avatar_url)')
    .eq('visibility', 'public')
    .order('created_at', { ascending: false })

  return (
    <div className="container py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">大会一覧</h1>
        <Link href="/tournaments/new">
          <Button>大会を作成</Button>
        </Link>
      </div>
      <div className="grid gap-4">
        {tournaments?.map(tournament => (
          <TournamentCard key={tournament.id} tournament={tournament} />
        ))}
      </div>
    </div>
  )
}
```
