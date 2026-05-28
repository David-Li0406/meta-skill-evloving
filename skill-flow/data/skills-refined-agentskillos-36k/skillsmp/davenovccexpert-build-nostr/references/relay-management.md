<overview>
Relays are WebSocket servers that store and forward Nostr events. Proper relay management is critical for reliability, performance, and censorship resistance. This reference covers relay selection, connection management, and failure handling.
</overview>

<relay_basics>
## How Relays Work

Relays:
- Accept WebSocket connections from clients
- Store events (based on kind and relay policy)
- Forward events to subscribers
- Do NOT communicate with each other
- Do NOT guarantee delivery or persistence

Clients must:
- Connect to multiple relays for redundancy
- Handle relay failures gracefully
- Deduplicate events from multiple sources
</relay_basics>

<relay_selection>
## Choosing Relays

**Popular public relays (2024-2025):**
```typescript
const RELIABLE_RELAYS = [
  'wss://relay.damus.io',      // Large, popular
  'wss://relay.nostr.band',    // Search-focused
  'wss://nos.lol',             // Well-maintained
  'wss://relay.snort.social',  // Snort's relay
  'wss://purplepag.es',        // Profile-focused
  'wss://nostr.wine',          // Curated
]
```

**Considerations:**
| Factor | Recommendation |
|--------|----------------|
| Count | 3-5 relays for most apps |
| Mix | Large + small relays |
| Geography | Distribute geographically |
| Policies | Check NIP-11 info |
| Paid vs Free | Paid often more reliable |

**Finding user's preferred relays (NIP-65):**
```typescript
async function getUserRelays(pubkey: string): Promise<string[]> {
  const event = await pool.get(defaultRelays, {
    kinds: [10002],  // Relay list
    authors: [pubkey]
  })

  if (!event) return defaultRelays

  return event.tags
    .filter(t => t[0] === 'r')
    .map(t => t[1])
}
```
</relay_selection>

<simple_pool>
## Using SimplePool

```typescript
import { SimplePool } from 'nostr-tools/pool'

const pool = new SimplePool()

// Pool manages:
// - Connection lifecycle
// - Reconnection on failure
// - Event deduplication
// - Subscription management
```

**Query patterns:**
```typescript
// Single event
const event = await pool.get(relays, { ids: ['...'] })

// Multiple events
const events = await pool.querySync(relays, filter)

// Subscribe (real-time)
const sub = pool.subscribeMany(relays, [filter], handlers)
```

**Publishing:**
```typescript
// Returns promise per relay
const promises = pool.publish(relays, event)

// Best practice: wait for at least one
try {
  await Promise.any(promises)
} catch {
  // All relays failed
}
```
</simple_pool>

<connection_health>
## Monitoring Connection Health

```typescript
interface RelayHealth {
  url: string
  connected: boolean
  lastSuccess: number
  failures: number
  latencyMs: number
}

class HealthMonitor {
  private health = new Map<string, RelayHealth>()

  async checkRelay(relay: string): Promise<RelayHealth> {
    const start = Date.now()

    try {
      // Try to fetch a single event
      const event = await pool.get([relay], { kinds: [0], limit: 1 })
      const latency = Date.now() - start

      return this.updateHealth(relay, {
        connected: true,
        lastSuccess: Date.now(),
        latencyMs: latency,
        failures: 0
      })
    } catch {
      const current = this.health.get(relay) || this.defaultHealth(relay)
      return this.updateHealth(relay, {
        connected: false,
        failures: current.failures + 1
      })
    }
  }

  private defaultHealth(url: string): RelayHealth {
    return { url, connected: false, lastSuccess: 0, failures: 0, latencyMs: 0 }
  }

  private updateHealth(url: string, update: Partial<RelayHealth>): RelayHealth {
    const current = this.health.get(url) || this.defaultHealth(url)
    const updated = { ...current, ...update }
    this.health.set(url, updated)
    return updated
  }

  getHealthyRelays(): string[] {
    return [...this.health.entries()]
      .filter(([_, h]) => h.connected && h.failures < 3)
      .sort((a, b) => a[1].latencyMs - b[1].latencyMs)
      .map(([url]) => url)
  }
}
```
</connection_health>

<failover>
## Failover Strategies

```typescript
class ResilientPool {
  private primaryRelays: string[]
  private backupRelays: string[]
  private pool = new SimplePool()

  constructor(primary: string[], backup: string[]) {
    this.primaryRelays = primary
    this.backupRelays = backup
  }

  async publish(event: Event): Promise<void> {
    // Try primary first
    const primaryResults = await Promise.allSettled(
      this.pool.publish(this.primaryRelays, event)
    )

    const primarySuccesses = primaryResults.filter(
      r => r.status === 'fulfilled'
    ).length

    if (primarySuccesses > 0) return

    // Fall back to backup
    await Promise.any(this.pool.publish(this.backupRelays, event))
  }

  async query(filter: Filter): Promise<Event[]> {
    // Query both for redundancy
    const allRelays = [...this.primaryRelays, ...this.backupRelays]
    return this.pool.querySync(allRelays, filter)
  }

  subscribe(filter: Filter, handlers: SubscriptionHandlers) {
    // Subscribe to all for maximum coverage
    const allRelays = [...this.primaryRelays, ...this.backupRelays]
    return this.pool.subscribeMany(allRelays, [filter], handlers)
  }
}
```
</failover>

<nip11>
## NIP-11: Relay Information

Query relay capabilities:

```typescript
async function getRelayInfo(relayUrl: string): Promise<RelayInfo | null> {
  try {
    // Convert wss:// to https://
    const httpUrl = relayUrl.replace('wss://', 'https://').replace('ws://', 'http://')

    const response = await fetch(httpUrl, {
      headers: { 'Accept': 'application/nostr+json' }
    })

    return await response.json()
  } catch {
    return null
  }
}

interface RelayInfo {
  name?: string
  description?: string
  pubkey?: string
  contact?: string
  supported_nips?: number[]
  software?: string
  version?: string
  limitation?: {
    max_message_length?: number
    max_subscriptions?: number
    max_filters?: number
    max_limit?: number
    max_subid_length?: number
    min_pow_difficulty?: number
    auth_required?: boolean
    payment_required?: boolean
  }
}
```
</nip11>

<nip42>
## NIP-42: Authentication

Some relays require authentication:

```typescript
async function handleAuthChallenge(
  ws: WebSocket,
  challenge: string,
  relayUrl: string,
  sk: Uint8Array
) {
  // Create auth event
  const authEvent = finalizeEvent({
    kind: 22242,
    created_at: Math.floor(Date.now() / 1000),
    tags: [
      ['relay', relayUrl],
      ['challenge', challenge]
    ],
    content: ''
  }, sk)

  ws.send(JSON.stringify(['AUTH', authEvent]))
}

// In message handler:
function handleMessage(msg: string, ws: WebSocket, relay: string, sk: Uint8Array) {
  const data = JSON.parse(msg)

  if (data[0] === 'AUTH') {
    handleAuthChallenge(ws, data[1], relay, sk)
  }
}
```
</nip42>

<rate_limiting>
## Handling Rate Limits

```typescript
class RateLimitedPool {
  private lastPublish = new Map<string, number>()
  private minIntervalMs = 100  // 10 events/second max

  async publish(relays: string[], event: Event): Promise<void> {
    const promises = relays.map(async relay => {
      const last = this.lastPublish.get(relay) || 0
      const wait = Math.max(0, this.minIntervalMs - (Date.now() - last))

      if (wait > 0) {
        await new Promise(r => setTimeout(r, wait))
      }

      this.lastPublish.set(relay, Date.now())
      return this.pool.publish([relay], event)
    })

    await Promise.any(promises.flat())
  }
}
```
</rate_limiting>

<best_practices>
## Best Practices

1. **Use 3-5 relays** - More isn't better, causes overhead
2. **Mix relay types** - Large public + smaller/paid
3. **Handle failures gracefully** - Assume any relay can fail
4. **Cache relay info** - Don't query NIP-11 repeatedly
5. **Respect rate limits** - Check OK messages for rate-limit errors
6. **Close unused subscriptions** - Memory leak otherwise
7. **Use since in subscriptions** - Don't fetch entire history
8. **Implement health checks** - Remove unhealthy relays temporarily
9. **Follow user's relay list** - Query NIP-65 for their preferences
10. **Support NIP-42** - Some relays require authentication
</best_practices>

<common_errors>
## Common OK Message Errors

When publishing, relays respond with OK messages:

| Prefix | Meaning |
|--------|---------|
| `duplicate:` | Event already exists |
| `blocked:` | Relay policy blocks this event |
| `rate-limited:` | Too many requests |
| `invalid:` | Malformed event |
| `pow:` | Proof of work required |
| `restricted:` | Authentication required |

```typescript
pool.publish(relays, event).forEach((promise, i) => {
  promise.then(result => {
    console.log(`${relays[i]}: ${result}`)
  }).catch(err => {
    console.error(`${relays[i]} failed:`, err)
  })
})
```
</common_errors>
