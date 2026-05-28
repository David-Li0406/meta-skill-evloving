# Swift / iOS Realtime Patterns (supabase-swift)

## Core setup

- Create a single `SupabaseClient` and reuse it app-wide.
- Confirm current API shape with Context7: some versions use `supabase.channel(...)`, newer APIs introduce `supabase.realtimeV2.channel(...)`.

## Subscribe & observe status

```swift
let channel = await supabase.realtimeV2.channel("public:messages")

Task {
    for status in await channel.statusChange {
        // unsubscribed, subscribing, subscribed, unsubscribing
    }
}

await channel.subscribe()
```

If your version uses the legacy API, create the channel with:
`let channel = supabase.channel("room")`

## Postgres Changes

```swift
for await change in channel.postgresChange(AnyAction.self, table: "messages") {
    // handle insert/update/delete
}
```

## Broadcast

```swift
try await channel.broadcast(event: "PING", message: ["ts": .double(Date.now.timeIntervalSince1970)])
```

## Presence

```swift
await channel.track(state: ["user_id": "abc_123"])
await channel.untrack()
```

## Recommended patterns

- Use AsyncStream or callbacks for listening to changes.
- Start subscriptions on view appear or foreground; clean up on disappear/background.
- Prefer `await channel.unsubscribe()` or `await supabase.removeChannel(channel)` to prevent unused subscriptions.
- Keep one channel instance per topic; avoid duplicate subscriptions.
- Use typed models (`Codable`) for payload decoding when possible.
- Prefer Broadcast for ephemeral UI state; use Postgres Changes only for persisted data.
