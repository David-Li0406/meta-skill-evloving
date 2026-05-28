# Workflow: Implement Pub/Sub Messaging Between Apps

<required_reading>
**Read these reference files NOW:**
1. references/pubsub-patterns.md
2. references/data-exchange-patterns.md
3. references/event-kinds.md
</required_reading>

<process>
## Step 1: Design Your Message Schema

Define what data flows between your apps:

```typescript
// Example: App state sync between clients
interface AppMessage {
  type: 'state_update' | 'action' | 'request' | 'response'
  payload: unknown
  correlationId?: string  // For request/response patterns
}
```

## Step 2: Choose Event Kind

| Use Case | Kind Range | Behavior |
|----------|------------|----------|
| Ephemeral messages (chat, signals) | 20000-29999 | NOT stored |
| Persistent app data | 30000-39999 | Addressable (latest per d-tag) |
| Regular events | 1000-9999 | All stored |

**For real-time data exchange:** Use ephemeral kinds (e.g., 25000).

```typescript
const APP_MESSAGE_KIND = 25000  // Ephemeral - not stored by relays
```

## Step 3: Create Publisher

```typescript
import { finalizeEvent, generateSecretKey, getPublicKey } from 'nostr-tools/pure'
import { SimplePool } from 'nostr-tools/pool'

const pool = new SimplePool()
const relays = ['wss://relay.damus.io', 'wss://nos.lol']

// App's identity
const sk = generateSecretKey()
const pk = getPublicKey(sk)

async function publish(message: AppMessage, targetPubkey?: string) {
  const tags: string[][] = []

  // If targeting specific recipient
  if (targetPubkey) {
    tags.push(['p', targetPubkey])
  }

  // Add correlation ID for request/response
  if (message.correlationId) {
    tags.push(['d', message.correlationId])
  }

  const event = finalizeEvent({
    kind: APP_MESSAGE_KIND,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content: JSON.stringify(message)
  }, sk)

  await Promise.any(pool.publish(relays, event))
  return event.id
}
```

## Step 4: Create Subscriber

```typescript
interface SubscriptionOptions {
  authors?: string[]      // Filter by sender pubkeys
  since?: number          // Only events after timestamp
  onMessage: (message: AppMessage, event: Event) => void
  onError?: (error: Error) => void
}

function subscribe(options: SubscriptionOptions) {
  const filter: Filter = {
    kinds: [APP_MESSAGE_KIND],
    since: options.since ?? Math.floor(Date.now() / 1000)
  }

  if (options.authors) {
    filter.authors = options.authors
  }

  // If listening for messages to me
  // filter['#p'] = [myPubkey]

  return pool.subscribeMany(
    relays,
    [filter],
    {
      onevent(event) {
        try {
          const message = JSON.parse(event.content) as AppMessage
          options.onMessage(message, event)
        } catch (err) {
          options.onError?.(err as Error)
        }
      },
      oneose() {
        console.log('Caught up with stored events, now real-time')
      }
    }
  )
}
```

## Step 5: Implement Request/Response Pattern

```typescript
async function request(
  message: Omit<AppMessage, 'type' | 'correlationId'>,
  targetPubkey: string,
  timeoutMs = 5000
): Promise<AppMessage> {
  const correlationId = crypto.randomUUID()

  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      sub.close()
      reject(new Error('Request timeout'))
    }, timeoutMs)

    // Listen for response
    const sub = pool.subscribeMany(
      relays,
      [{
        kinds: [APP_MESSAGE_KIND],
        authors: [targetPubkey],
        '#d': [correlationId],
        since: Math.floor(Date.now() / 1000)
      }],
      {
        onevent(event) {
          clearTimeout(timeout)
          sub.close()
          resolve(JSON.parse(event.content))
        }
      }
    )

    // Send request
    publish({
      type: 'request',
      payload: message.payload,
      correlationId
    }, targetPubkey)
  })
}
```

## Step 6: Handle Multiple Apps/Clients

```typescript
// Each app instance has unique identity
const APP_NAMESPACE = 'myapp'

function createAppFilter(appId: string): Filter {
  return {
    kinds: [APP_MESSAGE_KIND],
    '#t': [`${APP_NAMESPACE}:${appId}`]  // Tag-based routing
  }
}

// When publishing, add app tag
function publishToApp(appId: string, message: AppMessage) {
  const event = finalizeEvent({
    kind: APP_MESSAGE_KIND,
    created_at: Math.floor(Date.now() / 1000),
    tags: [['t', `${APP_NAMESPACE}:${appId}`]],
    content: JSON.stringify(message)
  }, sk)

  return pool.publish(relays, event)
}
```

## Step 7: Verify Communication

```typescript
// Test pub/sub flow
async function testPubSub() {
  let received = false

  const sub = subscribe({
    authors: [pk],
    onMessage: (msg) => {
      console.log('Received:', msg)
      received = true
    }
  })

  await publish({ type: 'action', payload: { test: true } })

  // Wait for propagation
  await new Promise(r => setTimeout(r, 2000))

  sub.close()
  console.log('Test passed:', received)
}
```
</process>

<anti_patterns>
Avoid:
- Using regular kinds (1-9999) for ephemeral real-time data (wastes relay storage)
- Not including timestamps in filters (fetches entire history)
- Polling instead of subscriptions (defeats real-time purpose)
- Assuming message delivery order (relays don't guarantee order)
- Large payloads in content (keep under 64KB, prefer references)
- Not handling duplicate events (same event from multiple relays)
</anti_patterns>

<success_criteria>
A working pub/sub implementation:
- Uses appropriate event kinds for use case
- Publishers can send to specific recipients or broadcast
- Subscribers receive real-time updates
- Request/response patterns work with correlation IDs
- Handles relay disconnections gracefully
- Deduplicates events received from multiple relays
- Parses and validates message payloads
</success_criteria>
