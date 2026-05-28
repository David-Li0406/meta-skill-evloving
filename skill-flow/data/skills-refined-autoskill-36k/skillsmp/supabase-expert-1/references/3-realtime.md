# 3. Real-time & Sync Strategy

**Impact: HIGH**

Supabase Realtime (2026) is optimized for high-concurrency event broadcasting and presence tracking.

## 3.1 Realtime Channels

Channels allow you to group related real-time functionality.

```typescript
const channel = supabase.channel('room-1')

channel
  .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'messages' }, (payload) => {
    console.log('New message:', payload)
  })
  .subscribe()
```

## 3.2 Broadcast vs. Presence

- **Broadcast**: Send a message to all users in a channel (e.g., "User started typing"). Fast, ephemeral.
- **Presence**: Track the state of online users (e.g., "Who is currently in this room?"). Handles syncing state when users join/leave.

### Presence Pattern
```typescript
const channel = supabase.channel('game-lobby', {
  config: {
    presence: {
      key: user.id,
    },
  },
})

channel
  .on('presence', { event: 'sync' }, () => {
    const state = channel.presenceState()
    console.log('Online users:', state)
  })
  .on('presence', { event: 'join' }, ({ key, newPresences }) => {
    console.log('User joined:', key)
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await channel.track({ online_at: new Date().toISOString() })
    }
  })
```

## 3.3 Throttling and Optimization (2026)

In 2026, you can configure throttling directly in the Supabase Dashboard:
- **Presence Events/sec**: Limit how often `sync` events are fired.
- **Payload Size**: Restrict broadcast messages to < 10KB to ensure low latency.

**Best Practice**: Never broadcast large data objects. Broadcast the `id` of the changed item and let clients fetch the full data via the standard API (which is cached by the edge).

## 3.4 Real-time RLS

Real-time events now respect RLS policies by default. If a user doesn't have `SELECT` access to a row via RLS, they will not receive a `postgres_changes` event for that row.
