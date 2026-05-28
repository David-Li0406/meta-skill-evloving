/**
 * Pub/Sub Event Handler Template
 *
 * A typed pub/sub system for exchanging data between
 * Nostr clients using custom event kinds.
 */

import { generateSecretKey, getPublicKey, finalizeEvent } from 'nostr-tools/pure'
import { SimplePool } from 'nostr-tools/pool'
import type { Event, Filter, Sub } from 'nostr-tools'

// ============================================================================
// Configuration
// ============================================================================

// Use ephemeral kind for real-time messages (not stored by relays)
const MESSAGE_KIND = 25000

const DEFAULT_RELAYS = [
  'wss://relay.damus.io',
  'wss://nos.lol'
]

// ============================================================================
// Message Types
// ============================================================================

interface BaseMessage {
  version: 1
  type: string
  timestamp: number
}

interface DataMessage extends BaseMessage {
  type: 'data'
  payload: unknown
}

interface RequestMessage extends BaseMessage {
  type: 'request'
  correlationId: string
  method: string
  params: unknown
}

interface ResponseMessage extends BaseMessage {
  type: 'response'
  correlationId: string
  result?: unknown
  error?: { code: number; message: string }
}

type Message = DataMessage | RequestMessage | ResponseMessage

// ============================================================================
// Pub/Sub Handler
// ============================================================================

interface PubSubOptions {
  relays?: string[]
  sk?: Uint8Array
  kind?: number
  namespace?: string
}

interface PendingRequest {
  resolve: (result: unknown) => void
  reject: (error: Error) => void
  timeout: NodeJS.Timeout
}

class PubSubHandler {
  private pool: SimplePool
  private relays: string[]
  private sk: Uint8Array
  private pk: string
  private kind: number
  private namespace: string
  private subscriptions: Sub[] = []
  private pendingRequests = new Map<string, PendingRequest>()
  private handlers = new Map<string, (event: Event, message: Message) => void>()
  private seenIds = new Set<string>()

  constructor(options: PubSubOptions = {}) {
    this.pool = new SimplePool()
    this.relays = options.relays ?? DEFAULT_RELAYS
    this.sk = options.sk ?? generateSecretKey()
    this.pk = getPublicKey(this.sk)
    this.kind = options.kind ?? MESSAGE_KIND
    this.namespace = options.namespace ?? 'default'
  }

  get publicKey(): string {
    return this.pk
  }

  // -------------------------------------------------------------------------
  // Publishing
  // -------------------------------------------------------------------------

  private async publishMessage(message: Message, targetPk?: string, channel?: string): Promise<string> {
    const tags: string[][] = [['t', this.namespace]]

    if (targetPk) {
      tags.push(['p', targetPk])
    }

    if (channel) {
      tags.push(['d', `${this.namespace}:${channel}`])
    }

    const event = finalizeEvent({
      kind: this.kind,
      created_at: Math.floor(Date.now() / 1000),
      tags,
      content: JSON.stringify(message)
    }, this.sk)

    await Promise.any(this.pool.publish(this.relays, event))
    return event.id
  }

  async publish(payload: unknown, channel?: string): Promise<string> {
    const message: DataMessage = {
      version: 1,
      type: 'data',
      timestamp: Date.now(),
      payload
    }

    return this.publishMessage(message, undefined, channel)
  }

  async sendTo(targetPk: string, payload: unknown): Promise<string> {
    const message: DataMessage = {
      version: 1,
      type: 'data',
      timestamp: Date.now(),
      payload
    }

    return this.publishMessage(message, targetPk)
  }

  // -------------------------------------------------------------------------
  // Request/Response
  // -------------------------------------------------------------------------

  async request<T>(targetPk: string, method: string, params: unknown, timeoutMs = 10000): Promise<T> {
    const correlationId = crypto.randomUUID()

    const message: RequestMessage = {
      version: 1,
      type: 'request',
      timestamp: Date.now(),
      correlationId,
      method,
      params
    }

    return new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.pendingRequests.delete(correlationId)
        reject(new Error(`Request timeout: ${method}`))
      }, timeoutMs)

      this.pendingRequests.set(correlationId, { resolve, reject, timeout })

      this.publishMessage(message, targetPk).catch(err => {
        clearTimeout(timeout)
        this.pendingRequests.delete(correlationId)
        reject(err)
      })
    })
  }

  async respond(requestEvent: Event, result: unknown): Promise<void> {
    const request = JSON.parse(requestEvent.content) as RequestMessage

    const message: ResponseMessage = {
      version: 1,
      type: 'response',
      timestamp: Date.now(),
      correlationId: request.correlationId,
      result
    }

    await this.publishMessage(message, requestEvent.pubkey)
  }

  async respondError(requestEvent: Event, code: number, errorMessage: string): Promise<void> {
    const request = JSON.parse(requestEvent.content) as RequestMessage

    const message: ResponseMessage = {
      version: 1,
      type: 'response',
      timestamp: Date.now(),
      correlationId: request.correlationId,
      error: { code, message: errorMessage }
    }

    await this.publishMessage(message, requestEvent.pubkey)
  }

  // -------------------------------------------------------------------------
  // Subscribing
  // -------------------------------------------------------------------------

  private handleEvent(event: Event): void {
    // Deduplicate
    if (this.seenIds.has(event.id)) return
    this.seenIds.add(event.id)

    // LRU cleanup
    if (this.seenIds.size > 10000) {
      const first = this.seenIds.values().next().value
      this.seenIds.delete(first)
    }

    try {
      const message = JSON.parse(event.content) as Message

      // Handle responses to pending requests
      if (message.type === 'response') {
        const pending = this.pendingRequests.get(message.correlationId)
        if (pending) {
          clearTimeout(pending.timeout)
          this.pendingRequests.delete(message.correlationId)

          if (message.error) {
            pending.reject(new Error(message.error.message))
          } else {
            pending.resolve(message.result)
          }
          return
        }
      }

      // Dispatch to registered handlers
      this.handlers.forEach(handler => handler(event, message))
    } catch (err) {
      console.error('Failed to parse message:', err)
    }
  }

  subscribe(channel: string, onMessage: (data: unknown, from: string) => void): () => void {
    const filter: Filter = {
      kinds: [this.kind],
      '#d': [`${this.namespace}:${channel}`],
      since: Math.floor(Date.now() / 1000)
    }

    const handlerId = crypto.randomUUID()

    this.handlers.set(handlerId, (event, message) => {
      if (message.type === 'data') {
        onMessage((message as DataMessage).payload, event.pubkey)
      }
    })

    const sub = this.pool.subscribeMany(this.relays, [filter], {
      onevent: (event) => this.handleEvent(event)
    })

    this.subscriptions.push(sub)

    return () => {
      this.handlers.delete(handlerId)
      sub.close()
    }
  }

  subscribeToMe(onMessage: (data: unknown, from: string) => void): () => void {
    const filter: Filter = {
      kinds: [this.kind],
      '#p': [this.pk],
      '#t': [this.namespace],
      since: Math.floor(Date.now() / 1000)
    }

    const handlerId = crypto.randomUUID()

    this.handlers.set(handlerId, (event, message) => {
      if (message.type === 'data') {
        onMessage((message as DataMessage).payload, event.pubkey)
      }
    })

    const sub = this.pool.subscribeMany(this.relays, [filter], {
      onevent: (event) => this.handleEvent(event)
    })

    this.subscriptions.push(sub)

    return () => {
      this.handlers.delete(handlerId)
      sub.close()
    }
  }

  onRequest(handler: (method: string, params: unknown, event: Event) => Promise<unknown>): () => void {
    const filter: Filter = {
      kinds: [this.kind],
      '#p': [this.pk],
      '#t': [this.namespace],
      since: Math.floor(Date.now() / 1000)
    }

    const handlerId = crypto.randomUUID()

    this.handlers.set(handlerId, async (event, message) => {
      if (message.type === 'request') {
        const req = message as RequestMessage
        try {
          const result = await handler(req.method, req.params, event)
          await this.respond(event, result)
        } catch (err) {
          await this.respondError(event, -1, String(err))
        }
      }
    })

    const sub = this.pool.subscribeMany(this.relays, [filter], {
      onevent: (event) => this.handleEvent(event)
    })

    this.subscriptions.push(sub)

    return () => {
      this.handlers.delete(handlerId)
      sub.close()
    }
  }

  // -------------------------------------------------------------------------
  // Cleanup
  // -------------------------------------------------------------------------

  close(): void {
    this.subscriptions.forEach(sub => sub.close())
    this.subscriptions = []
    this.handlers.clear()
    this.pendingRequests.forEach(req => {
      clearTimeout(req.timeout)
      req.reject(new Error('Handler closed'))
    })
    this.pendingRequests.clear()
    this.pool.close(this.relays)
  }
}

// ============================================================================
// Usage Example
// ============================================================================

async function main() {
  // Create two handlers (simulating two apps)
  const app1 = new PubSubHandler({ namespace: 'myapp' })
  const app2 = new PubSubHandler({ namespace: 'myapp' })

  console.log('App 1 pubkey:', app1.publicKey)
  console.log('App 2 pubkey:', app2.publicKey)

  // App 2 listens for direct messages
  app2.subscribeToMe((data, from) => {
    console.log('App 2 received from', from.slice(0, 8), ':', data)
  })

  // App 2 handles requests
  app2.onRequest(async (method, params) => {
    console.log('App 2 handling request:', method, params)
    if (method === 'ping') {
      return { pong: true, time: Date.now() }
    }
    throw new Error('Unknown method')
  })

  // Wait for subscriptions to establish
  await new Promise(r => setTimeout(r, 1000))

  // App 1 sends to App 2
  await app1.sendTo(app2.publicKey, { hello: 'world' })

  // App 1 makes a request to App 2
  const result = await app1.request(app2.publicKey, 'ping', {})
  console.log('Request result:', result)

  // Cleanup
  // app1.close()
  // app2.close()
}

// Export
export { PubSubHandler }
export type { Message, DataMessage, RequestMessage, ResponseMessage, PubSubOptions }
