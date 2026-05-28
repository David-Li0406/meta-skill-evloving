# Workflow: Connect to and Manage Relays

<required_reading>
**Read these reference files NOW:**
1. references/relay-management.md
2. references/nostr-tools-api.md
3. references/scaling-considerations.md
</required_reading>

<process>
## Step 1: Understand SimplePool

SimplePool manages multiple relay connections automatically:

```typescript
import { SimplePool } from 'nostr-tools/pool'

const pool = new SimplePool()
```

Key behaviors:
- Creates WebSocket connections lazily (on first use)
- Reuses connections across operations
- Handles reconnection automatically
- Deduplicates events from multiple relays

## Step 2: Choose Relays

**Popular public relays:**
```typescript
const PUBLIC_RELAYS = [
  'wss://relay.damus.io',
  'wss://relay.nostr.band',
  'wss://nos.lol',
  'wss://relay.snort.social',
  'wss://purplepag.es',
  'wss://relay.nostr.info'
]
```

**Considerations:**
- Use 3-5 relays for redundancy
- Mix large and small relays
- Consider geographic distribution
- Check relay policies (some require payment or NIP-42 auth)

## Step 3: Query Events

```typescript
// Get single event by ID
const event = await pool.get(relays, {
  ids: ['event_id_here']
})

// Query multiple events
const events = await pool.querySync(relays, {
  kinds: [1],
  authors: ['pubkey_here'],
  limit: 20
})

// Query with multiple filters (OR logic)
const mixed = await pool.querySync(relays, [
  { kinds: [0], authors: ['pk1'] },  // Metadata from pk1
  { kinds: [1], authors: ['pk2'] }   // Notes from pk2
])
```

## Step 4: Subscribe to Real-Time Events

```typescript
const sub = pool.subscribeMany(
  relays,
  [{ kinds: [1], since: Math.floor(Date.now() / 1000) }],
  {
    onevent(event) {
      console.log('New event:', event.id)
    },
    oneose() {
      console.log('Caught up, now streaming real-time')
    },
    onclose(reasons) {
      // reasons is array of close reasons per relay
      console.log('Subscription closed:', reasons)
    }
  }
)

// Close when done
sub.close()
```

## Step 5: Publish Events

```typescript
import { finalizeEvent } from 'nostr-tools/pure'

const event = finalizeEvent({
  kind: 1,
  created_at: Math.floor(Date.now() / 1000),
  tags: [],
  content: 'Hello!'
}, sk)

// Publish returns array of promises (one per relay)
const promises = pool.publish(relays, event)

// Wait for at least one success
try {
  await Promise.any(promises)
  console.log('Published to at least one relay')
} catch {
  console.error('Failed to publish to any relay')
}

// Or wait for all
const results = await Promise.allSettled(promises)
const successes = results.filter(r => r.status === 'fulfilled').length
console.log(`Published to ${successes}/${relays.length} relays`)
```

## Step 6: Handle Connection States

```typescript
// SimplePool handles reconnection, but you can monitor health
async function checkRelayHealth(relay: string): Promise<boolean> {
  try {
    const testFilter = { kinds: [0], limit: 1 }
    const result = await pool.querySync([relay], testFilter)
    return true
  } catch {
    return false
  }
}

async function getHealthyRelays(candidates: string[]): Promise<string[]> {
  const checks = await Promise.all(
    candidates.map(async relay => ({
      relay,
      healthy: await checkRelayHealth(relay)
    }))
  )
  return checks.filter(c => c.healthy).map(c => c.relay)
}
```

## Step 7: Implement Relay Fallback

```typescript
class ResilientPool {
  private pool = new SimplePool()
  private primaryRelays: string[]
  private fallbackRelays: string[]

  constructor(primary: string[], fallback: string[]) {
    this.primaryRelays = primary
    this.fallbackRelays = fallback
  }

  async publish(event: Event): Promise<void> {
    // Try primary first
    try {
      await Promise.any(this.pool.publish(this.primaryRelays, event))
      return
    } catch {
      // Fall back to secondary
      await Promise.any(this.pool.publish(this.fallbackRelays, event))
    }
  }

  async query(filter: Filter): Promise<Event[]> {
    // Query both for better coverage
    const allRelays = [...this.primaryRelays, ...this.fallbackRelays]
    return this.pool.querySync(allRelays, filter)
  }
}
```

## Step 8: Close Connections

```typescript
// Close specific relay connections
pool.close(relays)

// Note: SimplePool doesn't have a closeAll method
// Track your relays and close them explicitly
const allRelays = new Set<string>()

function trackRelay(relay: string) {
  allRelays.add(relay)
}

function closeAll() {
  pool.close([...allRelays])
}
```

## Step 9: Implement NIP-42 Authentication (If Required)

Some relays require authentication:

```typescript
import { finalizeEvent } from 'nostr-tools/pure'

async function authenticateToRelay(
  ws: WebSocket,
  challenge: string,
  relayUrl: string,
  sk: Uint8Array
) {
  const authEvent = finalizeEvent({
    kind: 22242,  // NIP-42 auth event
    created_at: Math.floor(Date.now() / 1000),
    tags: [
      ['relay', relayUrl],
      ['challenge', challenge]
    ],
    content: ''
  }, sk)

  ws.send(JSON.stringify(['AUTH', authEvent]))
}

// Listen for AUTH challenge in relay messages
// ["AUTH", "<challenge>"]
```

## Step 10: Monitor Relay Metrics

```typescript
interface RelayStats {
  url: string
  lastConnected?: number
  eventsReceived: number
  eventsSent: number
  errors: number
}

class MonitoredPool {
  private pool = new SimplePool()
  private stats = new Map<string, RelayStats>()

  async publish(relays: string[], event: Event) {
    const results = await Promise.allSettled(this.pool.publish(relays, event))

    results.forEach((result, i) => {
      const stat = this.getStats(relays[i])
      if (result.status === 'fulfilled') {
        stat.eventsSent++
      } else {
        stat.errors++
      }
    })
  }

  private getStats(relay: string): RelayStats {
    if (!this.stats.has(relay)) {
      this.stats.set(relay, {
        url: relay,
        eventsReceived: 0,
        eventsSent: 0,
        errors: 0
      })
    }
    return this.stats.get(relay)!
  }

  getRelayStats(): RelayStats[] {
    return [...this.stats.values()]
  }
}
```
</process>

<anti_patterns>
Avoid:
- Connecting to too many relays (3-5 is usually enough)
- Not handling relay failures (always have fallbacks)
- Ignoring EOSE (end of stored events) signal
- Leaving subscriptions open indefinitely (memory leak)
- Assuming all relays are equally reliable
- Not deduplicating events (SimplePool does this, but verify)
- Blocking on Promise.all for publish (use Promise.any)
</anti_patterns>

<success_criteria>
Well-managed relay connections:
- Uses 3-5 relays for redundancy
- Has fallback relays configured
- Monitors relay health
- Handles connection failures gracefully
- Closes unused subscriptions
- Tracks metrics for debugging
- Authenticates when required (NIP-42)
</success_criteria>
