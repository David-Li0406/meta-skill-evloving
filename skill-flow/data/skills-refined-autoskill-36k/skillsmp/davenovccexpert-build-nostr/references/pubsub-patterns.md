<overview>
Nostr's subscription model enables powerful pub/sub patterns for real-time data exchange between applications. This reference covers common patterns for building reactive, decentralized systems.
</overview>

<basic_pubsub>
## Core Pub/Sub Pattern

```typescript
import { SimplePool } from 'nostr-tools/pool'
import { finalizeEvent, generateSecretKey, getPublicKey } from 'nostr-tools/pure'

const pool = new SimplePool()
const relays = ['wss://relay.damus.io', 'wss://nos.lol']

// Publisher
async function publish(kind: number, content: string, tags: string[][] = []) {
  const event = finalizeEvent({
    kind,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content
  }, sk)

  await Promise.any(pool.publish(relays, event))
  return event.id
}

// Subscriber
function subscribe(filter: Filter, onEvent: (e: Event) => void) {
  return pool.subscribeMany(relays, [filter], {
    onevent: onEvent,
    oneose: () => console.log('Caught up to present')
  })
}
```
</basic_pubsub>

<topic_based>
## Topic-Based Pub/Sub

Use tags to create topic channels:

```typescript
const TOPIC_KIND = 25001  // Ephemeral

// Publish to topic
async function publishToTopic(topic: string, data: unknown) {
  return publish(TOPIC_KIND, JSON.stringify(data), [
    ['t', topic]
  ])
}

// Subscribe to topic
function subscribeToTopic(topic: string, onMessage: (data: unknown) => void) {
  return subscribe(
    {
      kinds: [TOPIC_KIND],
      '#t': [topic],
      since: Math.floor(Date.now() / 1000)
    },
    (event) => onMessage(JSON.parse(event.content))
  )
}

// Usage
subscribeToTopic('game-lobby', (data) => console.log('Lobby event:', data))
publishToTopic('game-lobby', { action: 'player_joined', id: 'abc' })
```
</topic_based>

<targeted_messaging>
## Targeted Messaging (P2P)

Send to specific recipients using p-tags:

```typescript
// Send to specific user
async function sendTo(recipientPk: string, data: unknown) {
  return publish(25002, JSON.stringify(data), [
    ['p', recipientPk]
  ])
}

// Receive messages addressed to me
function listenForMessages(myPk: string, onMessage: (data: unknown, from: string) => void) {
  return subscribe(
    {
      kinds: [25002],
      '#p': [myPk],
      since: Math.floor(Date.now() / 1000)
    },
    (event) => onMessage(JSON.parse(event.content), event.pubkey)
  )
}
```
</targeted_messaging>

<request_response>
## Request-Response Pattern

Use correlation IDs for request-response flows:

```typescript
interface PendingRequest {
  resolve: (response: unknown) => void
  reject: (error: Error) => void
  timeout: NodeJS.Timeout
}

class RequestResponseChannel {
  private pending = new Map<string, PendingRequest>()
  private myPk: string

  constructor(
    private pool: SimplePool,
    private relays: string[],
    private sk: Uint8Array,
    private kind = 25003
  ) {
    this.myPk = getPublicKey(sk)
    this.startListening()
  }

  private startListening() {
    this.pool.subscribeMany(this.relays, [{
      kinds: [this.kind],
      '#p': [this.myPk],
      since: Math.floor(Date.now() / 1000)
    }], {
      onevent: (event) => this.handleResponse(event)
    })
  }

  private handleResponse(event: Event) {
    const data = JSON.parse(event.content)
    if (data.correlationId && this.pending.has(data.correlationId)) {
      const req = this.pending.get(data.correlationId)!
      clearTimeout(req.timeout)
      this.pending.delete(data.correlationId)
      req.resolve(data.response)
    }
  }

  async request<T>(targetPk: string, payload: unknown, timeoutMs = 5000): Promise<T> {
    const correlationId = crypto.randomUUID()

    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.pending.delete(correlationId)
        reject(new Error('Request timeout'))
      }, timeoutMs)

      this.pending.set(correlationId, { resolve, reject, timeout })

      const event = finalizeEvent({
        kind: this.kind,
        created_at: Math.floor(Date.now() / 1000),
        tags: [['p', targetPk]],
        content: JSON.stringify({ correlationId, request: payload })
      }, this.sk)

      this.pool.publish(this.relays, event)
    })
  }

  // Call this to handle incoming requests
  onRequest(handler: (request: unknown, reply: (response: unknown) => void) => void) {
    this.pool.subscribeMany(this.relays, [{
      kinds: [this.kind],
      '#p': [this.myPk],
      since: Math.floor(Date.now() / 1000)
    }], {
      onevent: (event) => {
        const data = JSON.parse(event.content)
        if (data.request && data.correlationId) {
          handler(data.request, (response) => {
            const replyEvent = finalizeEvent({
              kind: this.kind,
              created_at: Math.floor(Date.now() / 1000),
              tags: [['p', event.pubkey]],
              content: JSON.stringify({ correlationId: data.correlationId, response })
            }, this.sk)
            this.pool.publish(this.relays, replyEvent)
          })
        }
      }
    })
  }
}
```
</request_response>

<broadcast_pattern>
## Broadcast Pattern

Publish to all followers/subscribers:

```typescript
// Broadcast to anyone listening to your pubkey
async function broadcast(data: unknown) {
  return publish(25004, JSON.stringify(data), [])
  // No p-tag = broadcast to anyone subscribed to this author
}

// Subscribe to a broadcaster
function subscribeToBroadcaster(broadcasterPk: string, onMessage: (data: unknown) => void) {
  return subscribe(
    {
      kinds: [25004],
      authors: [broadcasterPk],
      since: Math.floor(Date.now() / 1000)
    },
    (event) => onMessage(JSON.parse(event.content))
  )
}
```
</broadcast_pattern>

<channel_pattern>
## Channel/Room Pattern

Create named channels with multiple participants:

```typescript
const CHANNEL_KIND = 25005

interface Channel {
  id: string
  subscribe: (onMessage: (msg: unknown, from: string) => void) => Sub
  send: (data: unknown) => Promise<void>
}

function createChannel(channelId: string, pool: SimplePool, relays: string[], sk: Uint8Array): Channel {
  return {
    id: channelId,

    subscribe(onMessage) {
      return pool.subscribeMany(relays, [{
        kinds: [CHANNEL_KIND],
        '#d': [channelId],
        since: Math.floor(Date.now() / 1000)
      }], {
        onevent(event) {
          onMessage(JSON.parse(event.content), event.pubkey)
        }
      })
    },

    async send(data) {
      const event = finalizeEvent({
        kind: CHANNEL_KIND,
        created_at: Math.floor(Date.now() / 1000),
        tags: [['d', channelId]],
        content: JSON.stringify(data)
      }, sk)

      await Promise.any(pool.publish(relays, event))
    }
  }
}

// Usage
const lobby = createChannel('game-lobby-123', pool, relays, sk)
lobby.subscribe((msg, from) => console.log(`${from}: ${msg}`))
lobby.send({ action: 'ready' })
```
</channel_pattern>

<event_sourcing>
## Event Sourcing Pattern

Use regular events to build state from history:

```typescript
const STATE_KIND = 1001  // Regular - all stored

interface StateEvent {
  type: string
  payload: unknown
  seq: number
}

class EventSourcedState<T> {
  private state: T
  private seq = 0

  constructor(
    private pool: SimplePool,
    private relays: string[],
    private sk: Uint8Array,
    private stateId: string,
    private reducer: (state: T, event: StateEvent) => T,
    initialState: T
  ) {
    this.state = initialState
  }

  async replay(): Promise<void> {
    const events = await this.pool.querySync(this.relays, {
      kinds: [STATE_KIND],
      authors: [getPublicKey(this.sk)],
      '#d': [this.stateId]
    })

    // Sort by sequence
    events
      .map(e => JSON.parse(e.content) as StateEvent)
      .sort((a, b) => a.seq - b.seq)
      .forEach(se => {
        this.state = this.reducer(this.state, se)
        this.seq = Math.max(this.seq, se.seq)
      })
  }

  async dispatch(type: string, payload: unknown): Promise<void> {
    this.seq++
    const stateEvent: StateEvent = { type, payload, seq: this.seq }

    const event = finalizeEvent({
      kind: STATE_KIND,
      created_at: Math.floor(Date.now() / 1000),
      tags: [['d', this.stateId]],
      content: JSON.stringify(stateEvent)
    }, this.sk)

    await Promise.any(this.pool.publish(this.relays, event))
    this.state = this.reducer(this.state, stateEvent)
  }

  getState(): T {
    return this.state
  }
}
```
</event_sourcing>

<deduplication>
## Deduplication

Handle same event from multiple relays:

```typescript
class DeduplicatedHandler {
  private seen = new Set<string>()
  private maxSize = 10000

  handle(event: Event, callback: (event: Event) => void) {
    if (this.seen.has(event.id)) return

    // LRU-like cleanup
    if (this.seen.size >= this.maxSize) {
      const first = this.seen.values().next().value
      this.seen.delete(first)
    }

    this.seen.add(event.id)
    callback(event)
  }
}

// Usage
const dedup = new DeduplicatedHandler()
pool.subscribeMany(relays, [filter], {
  onevent: (event) => dedup.handle(event, processEvent)
})
```
</deduplication>

<anti_patterns>
## Anti-Patterns

**Polling instead of subscribing:**
```typescript
// BAD
setInterval(async () => {
  const events = await pool.querySync(relays, filter)
}, 5000)

// GOOD
pool.subscribeMany(relays, [filter], { onevent })
```

**Missing since filter:**
```typescript
// BAD - fetches entire history
{ kinds: [1] }

// GOOD - only new events
{ kinds: [1], since: Math.floor(Date.now() / 1000) }
```

**Not closing subscriptions:**
```typescript
// BAD - memory leak
pool.subscribeMany(relays, [filter], handlers)

// GOOD
const sub = pool.subscribeMany(relays, [filter], handlers)
// ... later
sub.close()
```
</anti_patterns>
