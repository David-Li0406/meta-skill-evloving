---
name: realtime-feature
description: Supabase Realtimeを使ったリアルタイム機能の実装。ライブ更新、購読設定、リアルタイムコンポーネント作成時に使用。
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Supabase Realtime機能実装スキル

Katorin2でのリアルタイム機能実装ガイドです。

## リアルタイム対応テーブル

現在Realtimeが有効なテーブル：
- `matches` - 対戦結果のリアルタイム更新
- `participants` - 参加者変更の通知
- `notifications` - 通知のリアルタイム配信
- `team_entries` - チームエントリー状態
- `individual_matches` - チーム戦内の個人戦

## カスタムフックの実装パターン

### 基本的な購読フック

```typescript
// src/hooks/useRealtimeMatches.ts
'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import type { Match } from '@/types/tournament'
import type { RealtimePostgresChangesPayload } from '@supabase/supabase-js'

export function useRealtimeMatches(tournamentId: string) {
  const [matches, setMatches] = useState<Match[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const supabase = createClient()

  useEffect(() => {
    // 初期データ取得
    const fetchMatches = async () => {
      const { data, error } = await supabase
        .from('matches')
        .select('*')
        .eq('tournament_id', tournamentId)
        .order('round')
        .order('match_number')

      if (!error && data) {
        setMatches(data)
      }
      setIsLoading(false)
    }

    fetchMatches()

    // Realtime購読
    const channel = supabase
      .channel(`matches:${tournamentId}`)
      .on(
        'postgres_changes',
        {
          event: '*',  // INSERT, UPDATE, DELETE全て
          schema: 'public',
          table: 'matches',
          filter: `tournament_id=eq.${tournamentId}`
        },
        (payload: RealtimePostgresChangesPayload<Match>) => {
          handleRealtimeUpdate(payload)
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [tournamentId])

  const handleRealtimeUpdate = (
    payload: RealtimePostgresChangesPayload<Match>
  ) => {
    const { eventType, new: newRecord, old: oldRecord } = payload

    setMatches(current => {
      switch (eventType) {
        case 'INSERT':
          return [...current, newRecord as Match]

        case 'UPDATE':
          return current.map(match =>
            match.id === (newRecord as Match).id
              ? (newRecord as Match)
              : match
          )

        case 'DELETE':
          return current.filter(match =>
            match.id !== (oldRecord as Match).id
          )

        default:
          return current
      }
    })
  }

  return { matches, isLoading }
}
```

### 通知用フック

```typescript
// src/hooks/useRealtimeNotifications.ts
'use client'

import { useEffect, useState, useCallback } from 'react'
import { createClient } from '@/lib/supabase/client'
import type { Notification } from '@/types/database'

export function useRealtimeNotifications(userId: string | null) {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [unreadCount, setUnreadCount] = useState(0)
  const supabase = createClient()

  useEffect(() => {
    if (!userId) return

    // 初期データ取得（未読のみ）
    const fetchNotifications = async () => {
      const { data } = await supabase
        .from('notifications')
        .select('*')
        .eq('user_id', userId)
        .is('read_at', null)
        .order('created_at', { ascending: false })
        .limit(20)

      if (data) {
        setNotifications(data)
        setUnreadCount(data.length)
      }
    }

    fetchNotifications()

    // 新しい通知を購読
    const channel = supabase
      .channel(`notifications:${userId}`)
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'notifications',
          filter: `user_id=eq.${userId}`
        },
        (payload) => {
          const newNotification = payload.new as Notification
          setNotifications(current => [newNotification, ...current])
          setUnreadCount(count => count + 1)
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [userId])

  const markAsRead = useCallback(async (notificationId: string) => {
    await supabase
      .from('notifications')
      .update({ read_at: new Date().toISOString() })
      .eq('id', notificationId)

    setNotifications(current =>
      current.filter(n => n.id !== notificationId)
    )
    setUnreadCount(count => Math.max(0, count - 1))
  }, [])

  return { notifications, unreadCount, markAsRead }
}
```

## コンポーネントでの使用

```typescript
// src/components/tournament/RealtimeBracket.tsx
'use client'

import { useRealtimeMatches } from '@/hooks/useRealtimeMatches'

interface Props {
  tournamentId: string
  initialMatches: Match[]  // SSRで取得した初期データ
}

export function RealtimeBracket({ tournamentId, initialMatches }: Props) {
  const { matches, isLoading } = useRealtimeMatches(tournamentId)

  // 初期表示はSSRデータ、その後はリアルタイムデータ
  const displayMatches = isLoading ? initialMatches : matches

  return (
    <div className="bracket">
      {displayMatches.map(match => (
        <MatchCard key={match.id} match={match} />
      ))}
    </div>
  )
}
```

## Presenceの使用（オンラインユーザー表示）

```typescript
// src/hooks/usePresence.ts
'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

interface PresenceState {
  onlineUsers: { id: string; name: string }[]
}

export function usePresence(roomId: string, user: { id: string; name: string }) {
  const [onlineUsers, setOnlineUsers] = useState<PresenceState['onlineUsers']>([])
  const supabase = createClient()

  useEffect(() => {
    const channel = supabase.channel(`room:${roomId}`)

    channel
      .on('presence', { event: 'sync' }, () => {
        const state = channel.presenceState()
        const users = Object.values(state).flat() as PresenceState['onlineUsers']
        setOnlineUsers(users)
      })
      .subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
          await channel.track(user)
        }
      })

    return () => {
      supabase.removeChannel(channel)
    }
  }, [roomId, user.id])

  return { onlineUsers }
}
```

## DBでのRealtime設定

```sql
-- マイグレーションでRealtimeを有効化
ALTER PUBLICATION supabase_realtime ADD TABLE new_table;

-- 特定のカラムのみ購読（パフォーマンス最適化）
ALTER PUBLICATION supabase_realtime
  SET TABLE matches (id, status, winner_id, player1_score, player2_score);
```

## ベストプラクティス

1. **初期データはSSR**: Server Componentで初期データを取得し、propsで渡す
2. **フィルター活用**: `filter`パラメータで必要なデータのみ購読
3. **クリーンアップ**: useEffect内で必ずチャンネルを削除
4. **楽観的更新**: UIは即座に更新し、エラー時にロールバック
5. **接続状態の監視**: 切断時の再接続ロジックを実装
