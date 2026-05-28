<overview>
nostr-tools is the canonical JavaScript/TypeScript library for Nostr. It provides low-level utilities for key generation, event signing, relay communication, and NIP implementations. Available on npm as `nostr-tools`.
</overview>

<installation>
```bash
npm install nostr-tools
# or
bun add nostr-tools
# or
yarn add nostr-tools
```

Types are included. Works in Node.js, browsers, and edge runtimes.
</installation>

<imports>
## Module Structure

nostr-tools uses subpath exports for tree-shaking:

```typescript
// Core functions (no side effects)
import { generateSecretKey, getPublicKey, finalizeEvent, verifyEvent } from 'nostr-tools/pure'

// Relay pool
import { SimplePool } from 'nostr-tools/pool'

// Individual relay connection
import { Relay } from 'nostr-tools/relay'

// NIP implementations
import * as nip04 from 'nostr-tools/nip04'  // Deprecated encryption
import * as nip19 from 'nostr-tools/nip19'  // Bech32 encoding
import * as nip44 from 'nostr-tools/nip44'  // Modern encryption
import * as nip05 from 'nostr-tools/nip05'  // DNS verification
```
</imports>

<key_management>
## Key Generation

```typescript
import { generateSecretKey, getPublicKey } from 'nostr-tools/pure'

// Generate random secret key (Uint8Array, 32 bytes)
const sk = generateSecretKey()

// Derive public key (hex string, 64 chars)
const pk = getPublicKey(sk)
```

## NIP-19 Encoding

```typescript
import * as nip19 from 'nostr-tools/nip19'

// Encode
const nsec = nip19.nsecEncode(sk)  // nsec1...
const npub = nip19.npubEncode(pk)  // npub1...
const note = nip19.noteEncode(eventId)  // note1...

// Encode with metadata
const nprofile = nip19.nprofileEncode({
  pubkey: pk,
  relays: ['wss://relay.example.com']
})

const nevent = nip19.neventEncode({
  id: eventId,
  relays: ['wss://relay.example.com'],
  author: pk
})

// Decode any NIP-19 string
const { type, data } = nip19.decode('npub1...')
// type: 'npub' | 'nsec' | 'note' | 'nprofile' | 'nevent' | 'naddr'
```
</key_management>

<event_operations>
## Creating Events

```typescript
import { finalizeEvent } from 'nostr-tools/pure'

const eventTemplate = {
  kind: 1,
  created_at: Math.floor(Date.now() / 1000),
  tags: [],
  content: 'Hello Nostr!'
}

// finalizeEvent adds: id, pubkey, sig
const signedEvent = finalizeEvent(eventTemplate, sk)
```

## Verifying Events

```typescript
import { verifyEvent } from 'nostr-tools/pure'

const isValid = verifyEvent(event)  // boolean
```

## Event Hash

```typescript
import { getEventHash } from 'nostr-tools/pure'

const hash = getEventHash(event)  // hex string
```
</event_operations>

<simple_pool>
## SimplePool

Manages connections to multiple relays:

```typescript
import { SimplePool } from 'nostr-tools/pool'

const pool = new SimplePool()
const relays = ['wss://relay.damus.io', 'wss://nos.lol']
```

## Query Methods

```typescript
// Get single event
const event = await pool.get(relays, { ids: ['...'] })

// Query multiple events (waits for all relays)
const events = await pool.querySync(relays, {
  kinds: [1],
  authors: ['pk'],
  limit: 20
})

// Multiple filters (OR logic)
const events = await pool.querySync(relays, [
  { kinds: [0], authors: ['pk1'] },
  { kinds: [1], authors: ['pk2'] }
])
```

## Subscriptions

```typescript
const sub = pool.subscribeMany(
  relays,
  [{ kinds: [1], since: Math.floor(Date.now() / 1000) }],
  {
    onevent(event) {
      console.log('Received:', event)
    },
    oneose() {
      console.log('End of stored events')
    },
    onclose(reasons) {
      console.log('Closed:', reasons)
    }
  }
)

// Close subscription
sub.close()
```

## Publishing

```typescript
// Returns array of promises (one per relay)
const promises = pool.publish(relays, signedEvent)

// Wait for at least one success
await Promise.any(promises)

// Or check all results
const results = await Promise.allSettled(promises)
```

## Closing Connections

```typescript
pool.close(relays)
```
</simple_pool>

<single_relay>
## Single Relay Connection

For fine-grained control:

```typescript
import { Relay } from 'nostr-tools/relay'

const relay = await Relay.connect('wss://relay.example.com')

// Subscribe
relay.subscribe([{ kinds: [1], limit: 10 }], {
  onevent(event) { console.log(event) },
  oneose() { console.log('EOSE') }
})

// Publish
await relay.publish(signedEvent)

// Close
relay.close()
```
</single_relay>

<nip44_encryption>
## NIP-44 Encryption

```typescript
import * as nip44 from 'nostr-tools/nip44'

// Create conversation key (cache this!)
const conversationKey = nip44.getConversationKey(senderSk, recipientPk)

// Encrypt
const ciphertext = nip44.encrypt(plaintext, conversationKey)

// Decrypt (same key works both directions)
const decrypted = nip44.decrypt(ciphertext, conversationKey)
```
</nip44_encryption>

<nip05_verification>
## NIP-05 DNS Verification

```typescript
import * as nip05 from 'nostr-tools/nip05'

// Verify user@domain.com
const profile = await nip05.queryProfile('user@domain.com')
// { pubkey: '...', relays: [...] } or null
```
</nip05_verification>

<utilities>
## Hex/Bytes Conversion

```typescript
import { bytesToHex, hexToBytes } from '@noble/hashes/utils'

const hex = bytesToHex(uint8Array)
const bytes = hexToBytes(hexString)
```

## Filter Matching

```typescript
import { matchFilter, matchFilters } from 'nostr-tools'

const matches = matchFilter(filter, event)  // boolean
const matchesAny = matchFilters(filters, event)  // boolean
```
</utilities>

<type_definitions>
## Key Types

```typescript
import type { Event, UnsignedEvent, Filter } from 'nostr-tools'

interface Event {
  id: string
  pubkey: string
  created_at: number
  kind: number
  tags: string[][]
  content: string
  sig: string
}

interface UnsignedEvent {
  kind: number
  created_at: number
  tags: string[][]
  content: string
}

interface Filter {
  ids?: string[]
  authors?: string[]
  kinds?: number[]
  since?: number
  until?: number
  limit?: number
  [key: `#${string}`]: string[]
}
```
</type_definitions>

<common_patterns>
## Deduplication

SimplePool deduplicates automatically, but for custom logic:

```typescript
const seen = new Set<string>()

function handleEvent(event: Event) {
  if (seen.has(event.id)) return
  seen.add(event.id)
  // Process event
}
```

## Retry Publishing

```typescript
async function publishWithRetry(event: Event, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await Promise.any(pool.publish(relays, event))
      return true
    } catch {
      await new Promise(r => setTimeout(r, 1000 * (i + 1)))
    }
  }
  return false
}
```

## Subscription Timeout

```typescript
function subscribeWithTimeout(filter: Filter, timeoutMs: number) {
  return new Promise<Event[]>((resolve) => {
    const events: Event[] = []
    const timeout = setTimeout(() => {
      sub.close()
      resolve(events)
    }, timeoutMs)

    const sub = pool.subscribeMany(relays, [filter], {
      onevent(event) { events.push(event) },
      oneose() {
        clearTimeout(timeout)
        sub.close()
        resolve(events)
      }
    })
  })
}
```
</common_patterns>
