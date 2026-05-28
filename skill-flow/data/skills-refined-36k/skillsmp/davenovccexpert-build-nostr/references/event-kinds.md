<overview>
Event kinds determine how relays store events and how clients interpret them. Choosing the right kind is critical for your application's data model.
</overview>

<kind_categories>
## Storage Behavior by Range

| Range | Category | Behavior |
|-------|----------|----------|
| 0 | Replaceable | Only latest per pubkey+kind |
| 1-2 | Regular | All stored permanently |
| 3 | Replaceable | Only latest per pubkey+kind |
| 4-44 | Regular | All stored permanently |
| 45-49 | Reserved | Future use |
| 1000-9999 | Regular | All stored permanently |
| 10000-19999 | Replaceable | Only latest per pubkey+kind |
| 20000-29999 | Ephemeral | NOT stored by relays |
| 30000-39999 | Addressable | Latest per pubkey+kind+d-tag |
| 40000-65535 | Reserved | Future use |
</kind_categories>

<decision_tree>
## Choosing a Kind

**Do you need to store all versions?**
→ Yes: Use Regular (1000-9999)
→ No: Continue...

**Is data tied to a unique identifier?**
→ Yes: Use Addressable (30000-39999) with d-tag as ID
→ No: Continue...

**Should only latest version exist?**
→ Yes: Use Replaceable (10000-19999)
→ No: Continue...

**Is this real-time only (no storage needed)?**
→ Yes: Use Ephemeral (20000-29999)
→ No: Use Regular (1000-9999)
</decision_tree>

<standard_kinds>
## Core Protocol Kinds

| Kind | Name | Content | Key Tags |
|------|------|---------|----------|
| 0 | Metadata | JSON: `{name, about, picture}` | - |
| 1 | Short Text Note | Plain text | e, p, t |
| 2 | Recommend Relay | Relay URL | - |
| 3 | Follows | JSON contact list | p |
| 5 | Event Deletion | Reason text | e, a |
| 6 | Repost | Empty or JSON | e, p |
| 7 | Reaction | Emoji or "+" | e, p |

## Messaging Kinds

| Kind | Name | Status | Notes |
|------|------|--------|-------|
| 4 | Encrypted DM | **Deprecated** | Use NIP-17 instead |
| 14 | Chat Message | Active | NIP-17 DM |
| 1059 | Gift Wrap | Active | NIP-59 wrapper |
| 1060 | Seal | Active | NIP-59 sealed |

## Application Kinds

| Kind | Name | Content |
|------|------|---------|
| 9735 | Zap | Lightning invoice |
| 10002 | Relay List | - (uses r tags) |
| 30023 | Long-form | Markdown article |
| 30078 | Application Data | Custom JSON |
| 31989 | Handler Info | App handler |
| 31990 | Handler Rec | Recommendations |
</standard_kinds>

<ephemeral_kinds>
## Ephemeral Events (20000-29999)

Use for real-time communication where storage is unnecessary:

```typescript
// Presence/typing indicator
const TYPING_KIND = 25050

// Real-time sync signal
const SYNC_SIGNAL_KIND = 25001

// Temporary notification
const NOTIFICATION_KIND = 25100
```

**Behavior:**
- Relays MAY refuse to store
- Delivered to active subscriptions only
- No historical queries
- Perfect for: typing indicators, live cursors, ephemeral chat

**Warning:** Some relays may still store ephemeral events briefly.
</ephemeral_kinds>

<replaceable_kinds>
## Replaceable Events (10000-19999)

Only the latest event per pubkey+kind is kept:

```typescript
// User settings
const SETTINGS_KIND = 10000

// Mute list
const MUTE_KIND = 10000

// Pin list
const PIN_KIND = 10001
```

**Use for:**
- User preferences
- Configuration
- Current state (not history)

**Query pattern:**
```typescript
const filter = {
  kinds: [10000],
  authors: [userPubkey]
}
// Returns only the latest event
```
</replaceable_kinds>

<addressable_kinds>
## Addressable Events (30000-39999)

Latest per pubkey+kind+d-tag. Perfect for app data with unique IDs:

```typescript
// Blog post
const LONG_FORM_KIND = 30023
// d-tag = slug, e.g., "my-first-post"

// User list
const LIST_KIND = 30000
// d-tag = list name, e.g., "favorites"

// Profile badge
const BADGE_KIND = 30009
// d-tag = badge identifier

// Application data
const APP_DATA_KIND = 30078
// d-tag = your data identifier
```

**d-tag requirement:**
```typescript
const event = {
  kind: 30078,
  tags: [
    ['d', 'user-settings-v1']  // Required!
  ],
  content: JSON.stringify(data)
}
```

**Query by d-tag:**
```typescript
const filter = {
  kinds: [30078],
  authors: [userPubkey],
  '#d': ['user-settings-v1']
}
```

**Reference with a-tag:**
```typescript
// Reference format: kind:pubkey:d-tag
const ref = `30078:${pubkey}:user-settings-v1`
const tags = [['a', ref]]
```
</addressable_kinds>

<custom_kinds>
## Defining Custom Kinds

**Choosing a number:**
- Check https://github.com/nostr-protocol/nips for reserved kinds
- Use ranges appropriate for your storage needs
- Document your kind in your app's docs

**Recommended structure:**

```typescript
const MY_APP_KIND = 30078  // Or another unused addressable

interface MyAppEvent {
  version: number  // For schema evolution
  type: string     // Discriminator
  data: unknown    // Payload
}

// Always version your schema!
const event = {
  kind: MY_APP_KIND,
  tags: [
    ['d', `myapp:${dataId}`],
    ['t', 'myapp'],  // For filtering
    ['client', 'myapp/1.0']  // Optional: identify client
  ],
  content: JSON.stringify({
    version: 1,
    type: 'settings',
    data: { theme: 'dark' }
  })
}
```
</custom_kinds>

<kind_selection_examples>
## Examples

**User's current location (real-time sharing):**
→ Ephemeral (25000+) - no storage needed

**User's home location (profile setting):**
→ Replaceable (10000+) - only latest matters

**List of bookmarked posts:**
→ Addressable (30000+) with d-tag "bookmarks"

**Chat message in a group:**
→ Regular (1000+) - all messages should persist

**Application sync state:**
→ Addressable (30000+) with d-tag per sync channel

**Typing indicator:**
→ Ephemeral (20000+) - real-time only
</kind_selection_examples>
