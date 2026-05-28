<overview>
Nostr (Notes and Other Stuff Transmitted by Relays) is a decentralized protocol for real-time data exchange. It uses WebSocket connections to relays (servers) that store and forward cryptographically signed events. The protocol is intentionally simple: one data type (Event), verified by signature, stored on multiple independent relays.
</overview>

<core_concepts>
## The Event

Every piece of data in Nostr is an Event:

```typescript
interface Event {
  id: string        // 32-byte hex SHA256 hash of serialized event
  pubkey: string    // 32-byte hex public key of creator
  created_at: number // Unix timestamp in seconds
  kind: number      // Event type (0-65535)
  tags: string[][]  // Array of tag arrays
  content: string   // Payload (arbitrary string)
  sig: string       // 64-byte hex Schnorr signature
}
```

The ID is computed as:
```
SHA256(JSON.stringify([0, pubkey, created_at, kind, tags, content]))
```

## Cryptography

- **Keys**: secp256k1 curve (same as Bitcoin)
- **Signatures**: Schnorr (BIP-340)
- **Secret key**: 32 bytes (256 bits)
- **Public key**: 32 bytes (x-coordinate only)
- **Signature**: 64 bytes

## Relays

Relays are WebSocket servers that:
- Accept EVENT messages from clients
- Store events (based on kind)
- Serve events via subscriptions
- Do NOT communicate with each other
- Do NOT guarantee delivery

Clients must connect to multiple relays for redundancy.

## Subscriptions

Clients request events using filters:

```typescript
interface Filter {
  ids?: string[]      // Match specific event IDs
  authors?: string[]  // Match pubkeys (exact 64-char hex)
  kinds?: number[]    // Match event kinds
  since?: number      // created_at >= value
  until?: number      // created_at <= value
  limit?: number      // Max events (applied per relay)
  "#<letter>"?: string[]  // Match tag values
}
```

Filter logic:
- Within a filter: AND (all conditions must match)
- Multiple filters: OR (any filter can match)
</core_concepts>

<messages>
## Client → Relay

| Message | Format | Purpose |
|---------|--------|---------|
| EVENT | `["EVENT", <event>]` | Publish an event |
| REQ | `["REQ", <sub_id>, <filter>...]` | Subscribe to events |
| CLOSE | `["CLOSE", <sub_id>]` | End subscription |

## Relay → Client

| Message | Format | Purpose |
|---------|--------|---------|
| EVENT | `["EVENT", <sub_id>, <event>]` | Deliver matching event |
| OK | `["OK", <event_id>, <bool>, <msg>]` | Accept/reject EVENT |
| EOSE | `["EOSE", <sub_id>]` | End of stored events |
| CLOSED | `["CLOSED", <sub_id>, <msg>]` | Subscription ended |
| NOTICE | `["NOTICE", <msg>]` | Human-readable message |
| AUTH | `["AUTH", <challenge>]` | Authentication required |
</messages>

<event_kinds>
## Kind Ranges

| Range | Type | Storage Behavior |
|-------|------|------------------|
| 0, 3 | Replaceable | Latest per pubkey+kind |
| 1, 2, 4-44, 1000-9999 | Regular | All stored |
| 10000-19999 | Replaceable | Latest per pubkey+kind |
| 20000-29999 | Ephemeral | NOT stored |
| 30000-39999 | Addressable | Latest per pubkey+kind+d-tag |

## Common Kinds

| Kind | Name | Use |
|------|------|-----|
| 0 | Metadata | User profile (name, about, picture) |
| 1 | Short Text Note | Social posts |
| 3 | Follows | Contact list |
| 4 | Encrypted DM | NIP-04 DM (deprecated) |
| 5 | Event Deletion | Request to delete events |
| 6 | Repost | Share another event |
| 7 | Reaction | Like/emoji reaction |
| 9735 | Zap | Lightning payment |
| 10002 | Relay List | User's preferred relays |
| 30023 | Long-form Content | Articles |
</event_kinds>

<tags>
## Standard Tags

| Tag | Format | Purpose |
|-----|--------|---------|
| e | `["e", <event_id>, <relay?>, <marker?>]` | Reference event |
| p | `["p", <pubkey>, <relay?>]` | Reference user |
| a | `["a", "<kind>:<pk>:<d>", <relay?>]` | Reference addressable event |
| d | `["d", <identifier>]` | Unique ID for addressable events |
| t | `["t", <hashtag>]` | Hashtag |
| r | `["r", <url>]` | Reference URL |

Tags with single lowercase letters (a-z) are indexable by relays.
</tags>

<nip19_encoding>
## Human-Readable Formats

| Prefix | Type | Example |
|--------|------|---------|
| npub | Public key | npub1... |
| nsec | Secret key | nsec1... |
| note | Event ID | note1... |
| nprofile | Profile + relays | nprofile1... |
| nevent | Event + relays | nevent1... |
| naddr | Addressable event | naddr1... |

All use Bech32 encoding for error detection.
</nip19_encoding>

<security_model>
## Trust Model

- Events are verified by signature, not by relay
- Relays are untrusted storage
- Clients MUST verify signatures
- Multiple relays provide redundancy, not consensus
- Metadata (pubkey, timestamp) is always visible
- Content can be encrypted (NIP-44)

## Key Security

- Secret keys must NEVER be exposed
- Use NIP-46 for web apps (remote signing)
- Consider hardware signing for high-value accounts
- Key rotation is possible but complex
</security_model>
