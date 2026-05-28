# Workflow: Set Up New Nostr Client

<required_reading>
**Read these reference files NOW:**
1. references/nostr-tools-api.md
2. references/relay-management.md
3. references/key-management.md
</required_reading>

<process>
## Step 1: Install Dependencies

```bash
npm install nostr-tools
# or
bun add nostr-tools
```

For TypeScript projects, types are included.

## Step 2: Create Key Pair

```typescript
import { generateSecretKey, getPublicKey } from 'nostr-tools/pure'
import * as nip19 from 'nostr-tools/nip19'

// Generate new key pair
const sk = generateSecretKey() // Uint8Array
const pk = getPublicKey(sk)    // hex string

// Human-readable formats
const nsec = nip19.nsecEncode(sk) // nsec1...
const npub = nip19.npubEncode(pk) // npub1...

console.log('Secret key (KEEP SAFE):', nsec)
console.log('Public key:', npub)
```

**CRITICAL:** Store the secret key securely. Never commit to git or expose in client code.

## Step 3: Initialize Relay Pool

```typescript
import { SimplePool } from 'nostr-tools/pool'

const pool = new SimplePool()

// Recommended starting relays
const relays = [
  'wss://relay.damus.io',
  'wss://relay.nostr.band',
  'wss://nos.lol',
  'wss://relay.snort.social'
]
```

## Step 4: Create Your First Event

```typescript
import { finalizeEvent } from 'nostr-tools/pure'

const eventTemplate = {
  kind: 1,  // Text note
  created_at: Math.floor(Date.now() / 1000),
  tags: [],
  content: 'Hello Nostr!'
}

const signedEvent = finalizeEvent(eventTemplate, sk)
// signedEvent now has: id, pubkey, sig populated
```

## Step 5: Publish Event

```typescript
// Publish to all relays, wait for at least one success
const publishPromises = pool.publish(relays, signedEvent)

try {
  await Promise.any(publishPromises)
  console.log('Published successfully!')
} catch (err) {
  console.error('Failed to publish to any relay')
}
```

## Step 6: Subscribe to Events

```typescript
const sub = pool.subscribeMany(
  relays,
  [
    {
      kinds: [1],
      authors: [pk],
      limit: 10
    }
  ],
  {
    onevent(event) {
      console.log('Received event:', event)
    },
    oneose() {
      console.log('End of stored events')
    }
  }
)

// Later: close subscription
// sub.close()
```

## Step 7: Verify Setup

```bash
# Run your app and check:
# 1. Key pair generated
# 2. Connected to relays (no WebSocket errors)
# 3. Event published (check on https://njump.me/npub...)
# 4. Subscription receiving events
```
</process>

<anti_patterns>
Avoid:
- Storing secret keys in environment variables for client apps (use secure storage)
- Connecting to too many relays (3-5 is typically sufficient)
- Not handling WebSocket disconnections (relays drop connections)
- Ignoring event verification (always verify signatures from untrusted sources)
- Using synchronous patterns (Nostr is inherently async)
</anti_patterns>

<success_criteria>
A properly set up Nostr client:
- Generates and securely stores key pairs
- Connects to multiple relays for redundancy
- Can publish signed events
- Can subscribe and receive events
- Handles connection failures gracefully
- Verifies event signatures
</success_criteria>
