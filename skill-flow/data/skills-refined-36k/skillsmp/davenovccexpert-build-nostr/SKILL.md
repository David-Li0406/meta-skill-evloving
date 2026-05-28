---
name: davenov:cc:expert-build-nostr
description: Build Nostr applications for decentralized data exchange between clients. Full lifecycle - implement pub/sub messaging, relay connections, event handling, encryption, and custom protocols. Uses nostr-tools library.
---

<essential_principles>
## How Nostr Works

Nostr is a decentralized protocol for real-time data exchange. Understanding these fundamentals is critical for every implementation.

### 1. Events Are Everything

The entire protocol has ONE data type: the Event. Every piece of data - messages, profiles, reactions, custom app data - is an Event with this structure:

```typescript
interface Event {
  id: string        // SHA256 hash of serialized event
  pubkey: string    // 32-byte hex public key of creator
  created_at: number // Unix timestamp (seconds)
  kind: number      // Event type (0-65535)
  tags: string[][]  // Array of tag arrays
  content: string   // Payload (often JSON stringified)
  sig: string       // Schnorr signature
}
```

Every event is cryptographically signed. Authenticity is verified by signature, not by the relay.

### 2. Kind Numbers Define Behavior

Kind numbers determine how relays store events and how clients interpret them:

| Range | Type | Behavior |
|-------|------|----------|
| 0, 3, 10000-19999 | Replaceable | Only latest per pubkey+kind stored |
| 1, 2, 4-44, 1000-9999 | Regular | All stored permanently |
| 20000-29999 | Ephemeral | NOT stored - real-time only |
| 30000-39999 | Addressable | Latest per pubkey+kind+d-tag stored |

**For data exchange between apps:** Use ephemeral kinds (20000-29999) for transient messages, addressable kinds (30000+) for stateful data.

### 3. Relays Are Dumb Pipes

Relays are WebSocket servers that store and forward events. They:
- Accept events via `["EVENT", <event>]`
- Return events via subscriptions `["REQ", <sub_id>, <filter>...]`
- Do NOT communicate with each other
- Do NOT guarantee delivery or storage

**Your app must handle:** Multiple relay connections, deduplication, retry logic, and failure scenarios.

### 4. Subscriptions Are Filters

Clients subscribe to events using filter objects:

```typescript
interface Filter {
  ids?: string[]      // Specific event IDs
  authors?: string[]  // Pubkeys to match
  kinds?: number[]    // Event kinds
  since?: number      // Events after timestamp
  until?: number      // Events before timestamp
  limit?: number      // Max events to return
  "#e"?: string[]     // Events with these e-tags
  "#p"?: string[]     // Events mentioning these pubkeys
  "#<letter>"?: string[] // Any single-letter tag
}
```

### 5. Use nostr-tools for JavaScript/TypeScript

The canonical library is `nostr-tools`. Key imports:

```typescript
// Key generation and signing
import { generateSecretKey, getPublicKey, finalizeEvent, verifyEvent } from 'nostr-tools/pure'

// Relay pool management
import { SimplePool } from 'nostr-tools/pool'

// NIP-19 encoding (npub, nsec, etc.)
import * as nip19 from 'nostr-tools/nip19'

// NIP-44 encryption
import * as nip44 from 'nostr-tools/nip44'
```

### 6. Security Is Non-Negotiable

- NEVER expose secret keys in client-side code or logs
- ALWAYS verify event signatures before trusting data
- Use NIP-44 (not NIP-04) for encryption - NIP-04 is deprecated and insecure
- Store keys securely (use NIP-46 remote signing for web apps)
</essential_principles>

<intake>
**What would you like to do?**

1. Set up a new Nostr client/application
2. Implement pub/sub messaging between apps
3. Create custom event kinds for app data
4. Add encrypted communication (DMs, private data)
5. Connect to and manage relays
6. Debug relay/event issues
7. Something else

**Wait for response, then read the matching workflow.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "new", "setup", "start", "client", "app" | `workflows/setup-client.md` |
| 2, "pub/sub", "messaging", "real-time", "sync", "exchange" | `workflows/implement-pubsub.md` |
| 3, "custom", "kind", "data", "structured", "JSON" | `workflows/custom-event-kinds.md` |
| 4, "encrypt", "DM", "private", "NIP-44", "secret" | `workflows/add-encryption.md` |
| 5, "relay", "connect", "pool", "SimplePool" | `workflows/manage-relays.md` |
| 6, "debug", "broken", "not working", "error" | `workflows/debug-nostr.md` |
| 7, other | Clarify intent, then route or check references |
</routing>

<verification_loop>
## After Every Change

```bash
# 1. TypeScript compiles?
npx tsc --noEmit

# 2. Can connect to relays?
# Test with a known relay like wss://relay.damus.io

# 3. Events properly signed?
# Use verifyEvent() on created events

# 4. Subscriptions receiving data?
# Check EOSE message received
```

Report:
- "Build: OK" / "Build: X errors"
- "Relay connection: OK to X relays"
- "Event signing: Valid"
- "Subscription: Receiving events"
</verification_loop>

<reference_index>
## Domain Knowledge

All in `references/`:

**Protocol:** protocol-fundamentals.md, event-kinds.md, nips-overview.md
**Implementation:** nostr-tools-api.md, relay-management.md
**Patterns:** pubsub-patterns.md, data-exchange-patterns.md
**Security:** encryption-nip44.md, key-management.md
**Advanced:** custom-protocols.md, scaling-considerations.md
</reference_index>

<workflows_index>
## Workflows

All in `workflows/`:

| File | Purpose |
|------|---------|
| setup-client.md | Initialize a new Nostr client/app |
| implement-pubsub.md | Build pub/sub messaging between apps |
| custom-event-kinds.md | Design custom event kinds for app data |
| add-encryption.md | Implement NIP-44 encrypted communication |
| manage-relays.md | Connect to and manage relay pools |
| debug-nostr.md | Troubleshoot relay and event issues |
</workflows_index>

<templates_index>
## Templates

All in `templates/`:

| File | Purpose |
|------|---------|
| basic-client.ts | Minimal Nostr client setup |
| pubsub-handler.ts | Pub/sub event handler pattern |
| custom-event-schema.ts | Custom event kind definition |
</templates_index>
