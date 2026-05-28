---
name: supabase-realtime-ios
description: Use when implementing or reviewing Supabase Realtime in iOS/Swift apps (supabase-swift). Covers Postgres Changes, Broadcast, Presence, channel lifecycle, and best practices.
---

# Supabase Realtime (iOS / Swift)

## When to use

- The request mentions Supabase Realtime, Postgres changes, broadcast, presence, or realtime channels on iOS/Swift.
- The task needs Swift SDK patterns, channel lifecycle, or realtime best practices.

## Workflow (concise)

1. Clarify which Realtime mode is needed: Postgres Changes vs Broadcast vs Presence.
2. Use Context7 `/supabase/supabase-swift` to confirm current Swift API shapes (Realtime V2 vs v1).
3. Use Supabase docs for product behavior, limits, replication, and security details.
4. Choose the right mode:
   - Postgres Changes for authoritative DB events.
   - Broadcast for low-latency, ephemeral client-to-client messages.
   - Presence for shared state and online user lists.
5. On iOS, wire lifecycle: subscribe on view appear/foreground, clean up on disappear/background.

## References

- `references/realtime-overview.md` for concepts, tradeoffs, and server-side setup.
- `references/swift-realtime-patterns.md` for Swift/iOS usage patterns.
