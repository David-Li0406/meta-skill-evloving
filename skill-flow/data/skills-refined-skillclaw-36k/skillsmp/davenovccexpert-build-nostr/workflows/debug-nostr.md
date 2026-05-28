# Workflow: Debug Nostr Issues

<required_reading>
**Read these reference files NOW:**
1. references/protocol-fundamentals.md
2. references/nostr-tools-api.md
3. references/relay-management.md
</required_reading>

<process>
## Step 1: Identify the Problem Category

| Symptom | Likely Cause | Jump To |
|---------|--------------|---------|
| Events not appearing | Relay, filter, or subscription issue | Step 2 |
| Signature invalid | Key handling or event construction | Step 3 |
| Connection failures | Relay down or WebSocket issue | Step 4 |
| Encryption fails | NIP-44 key derivation or format | Step 5 |
| Events duplicated | Missing deduplication | Step 6 |
| Slow performance | Too many relays or subscriptions | Step 7 |

## Step 2: Debug Missing Events

```typescript
import { verifyEvent } from 'nostr-tools/pure'

// 1. Verify the event was created correctly
console.log('Event ID:', event.id)
console.log('Event valid:', verifyEvent(event))

// 2. Check if event was published successfully
const publishResults = await Promise.allSettled(pool.publish(relays, event))
publishResults.forEach((r, i) => {
  console.log(`${relays[i]}: ${r.status}`)
  if (r.status === 'rejected') {
    console.log('  Error:', r.reason)
  }
})

// 3. Verify subscription filter matches event
const filter = { kinds: [1], authors: [pk] }
console.log('Filter:', JSON.stringify(filter))
console.log('Event matches filter:', eventMatchesFilter(event, filter))

function eventMatchesFilter(event: Event, filter: Filter): boolean {
  if (filter.kinds && !filter.kinds.includes(event.kind)) return false
  if (filter.authors && !filter.authors.includes(event.pubkey)) return false
  if (filter.since && event.created_at < filter.since) return false
  if (filter.until && event.created_at > filter.until) return false
  return true
}

// 4. Check if relay received it
const retrieved = await pool.get(relays, { ids: [event.id] })
console.log('Event retrievable:', !!retrieved)
```

## Step 3: Debug Signature Issues

```typescript
import { finalizeEvent, verifyEvent, getEventHash } from 'nostr-tools/pure'
import { bytesToHex, hexToBytes } from '@noble/hashes/utils'

// Verify event structure
function debugEvent(event: Event) {
  console.log('=== Event Debug ===')
  console.log('ID length:', event.id.length, '(should be 64)')
  console.log('Pubkey length:', event.pubkey.length, '(should be 64)')
  console.log('Sig length:', event.sig.length, '(should be 128)')
  console.log('Kind:', event.kind, '(number?', typeof event.kind === 'number', ')')
  console.log('Created_at:', event.created_at, '(number?', typeof event.created_at === 'number', ')')
  console.log('Tags:', JSON.stringify(event.tags))
  console.log('Content type:', typeof event.content)

  // Verify hash
  const expectedId = getEventHash(event)
  console.log('ID matches hash:', event.id === expectedId)

  // Verify signature
  console.log('Signature valid:', verifyEvent(event))
}

// Common issues:
// - created_at as string instead of number
// - Tags not as array of arrays
// - Content not a string
// - Using wrong key format
```

## Step 4: Debug Connection Issues

```typescript
async function debugRelay(relayUrl: string) {
  console.log(`=== Testing ${relayUrl} ===`)

  // Test WebSocket connection
  const ws = new WebSocket(relayUrl)

  return new Promise((resolve) => {
    const timeout = setTimeout(() => {
      console.log('Connection timeout')
      ws.close()
      resolve(false)
    }, 5000)

    ws.onopen = () => {
      console.log('WebSocket connected')
      clearTimeout(timeout)

      // Send REQ to test
      const subId = 'test-' + Date.now()
      ws.send(JSON.stringify(['REQ', subId, { kinds: [0], limit: 1 }]))
    }

    ws.onmessage = (msg) => {
      const data = JSON.parse(msg.data)
      console.log('Received:', data[0])

      if (data[0] === 'EOSE') {
        console.log('Relay responding correctly')
        ws.close()
        resolve(true)
      } else if (data[0] === 'NOTICE') {
        console.log('Relay notice:', data[1])
      } else if (data[0] === 'AUTH') {
        console.log('Relay requires authentication (NIP-42)')
      }
    }

    ws.onerror = (err) => {
      console.log('WebSocket error:', err)
      clearTimeout(timeout)
      resolve(false)
    }

    ws.onclose = (event) => {
      console.log('Connection closed:', event.code, event.reason)
    }
  })
}

// Test all relays
async function testAllRelays(relays: string[]) {
  for (const relay of relays) {
    await debugRelay(relay)
  }
}
```

## Step 5: Debug Encryption Issues

```typescript
import * as nip44 from 'nostr-tools/nip44'
import { getPublicKey } from 'nostr-tools/pure'

function debugEncryption(senderSk: Uint8Array, recipientSk: Uint8Array) {
  const senderPk = getPublicKey(senderSk)
  const recipientPk = getPublicKey(recipientSk)

  console.log('=== Encryption Debug ===')
  console.log('Sender pubkey:', senderPk)
  console.log('Recipient pubkey:', recipientPk)

  // Generate conversation keys from both sides
  const senderKey = nip44.getConversationKey(senderSk, recipientPk)
  const recipientKey = nip44.getConversationKey(recipientSk, senderPk)

  console.log('Keys match:', Buffer.from(senderKey).equals(Buffer.from(recipientKey)))

  // Test encryption round-trip
  const testMessage = 'Test encryption'
  try {
    const encrypted = nip44.encrypt(testMessage, senderKey)
    console.log('Encrypted length:', encrypted.length)

    const decrypted = nip44.decrypt(encrypted, recipientKey)
    console.log('Decryption successful:', decrypted === testMessage)
  } catch (err) {
    console.error('Encryption error:', err)
  }
}
```

## Step 6: Debug Duplicate Events

```typescript
class DeduplicatedSubscription {
  private seenIds = new Set<string>()

  wrap(callback: (event: Event) => void) {
    return (event: Event) => {
      if (this.seenIds.has(event.id)) {
        console.log('Duplicate filtered:', event.id.slice(0, 8))
        return
      }
      this.seenIds.add(event.id)
      callback(event)
    }
  }

  stats() {
    return {
      uniqueEvents: this.seenIds.size
    }
  }
}

// Usage
const dedup = new DeduplicatedSubscription()
pool.subscribeMany(relays, [filter], {
  onevent: dedup.wrap((event) => {
    console.log('Unique event:', event.id)
  })
})
```

## Step 7: Debug Performance Issues

```typescript
async function profileNostrOperation(name: string, fn: () => Promise<void>) {
  const start = performance.now()
  await fn()
  const duration = performance.now() - start
  console.log(`${name}: ${duration.toFixed(2)}ms`)
}

// Profile relay queries
await profileNostrOperation('Query 100 events', async () => {
  await pool.querySync(relays, { kinds: [1], limit: 100 })
})

// Count open subscriptions
let openSubs = 0
function trackSubscription(sub: Sub) {
  openSubs++
  console.log(`Open subscriptions: ${openSubs}`)

  const originalClose = sub.close.bind(sub)
  sub.close = () => {
    openSubs--
    console.log(`Open subscriptions: ${openSubs}`)
    originalClose()
  }
  return sub
}
```

## Step 8: Use Browser DevTools / Network Tab

For browser-based debugging:

1. Open DevTools → Network → WS filter
2. Find relay connections
3. Click to see messages
4. Look for:
   - AUTH challenges (NIP-42)
   - OK messages with errors
   - CLOSED messages with reasons
   - NOTICE messages from relay

Common OK error prefixes:
- `duplicate:` - Event already exists
- `blocked:` - Relay policy blocks event
- `rate-limited:` - Too many requests
- `invalid:` - Malformed event
- `pow:` - Proof of work required

## Step 9: Log Raw Protocol Messages

```typescript
// Wrap WebSocket to log all messages
const OriginalWebSocket = WebSocket

class LoggingWebSocket extends OriginalWebSocket {
  constructor(url: string) {
    super(url)

    this.addEventListener('message', (e) => {
      console.log(`← ${url}:`, JSON.parse(e.data))
    })

    const originalSend = this.send.bind(this)
    this.send = (data: string) => {
      console.log(`→ ${url}:`, JSON.parse(data))
      originalSend(data)
    }
  }
}

// Replace globally for debugging
(globalThis as any).WebSocket = LoggingWebSocket
```
</process>

<anti_patterns>
Avoid:
- Debugging without logging raw messages
- Assuming the event is valid without verifying
- Ignoring relay responses (OK, NOTICE, CLOSED)
- Not testing individual relays in isolation
- Forgetting that filters use AND logic within, OR between
- Not checking event timestamps (since/until filters)
</anti_patterns>

<success_criteria>
Debugging session complete when:
- Root cause identified
- Fix verified with logging
- Events flow correctly end-to-end
- No duplicate or missing events
- Performance acceptable
- Connection stable
</success_criteria>
