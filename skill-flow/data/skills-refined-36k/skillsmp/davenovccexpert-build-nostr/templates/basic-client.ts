/**
 * Basic Nostr Client Template
 *
 * A minimal setup for a Nostr client with key management,
 * relay connection, publishing, and subscriptions.
 */

import { generateSecretKey, getPublicKey, finalizeEvent, verifyEvent } from 'nostr-tools/pure'
import { SimplePool } from 'nostr-tools/pool'
import * as nip19 from 'nostr-tools/nip19'
import type { Event, Filter } from 'nostr-tools'

// ============================================================================
// Configuration
// ============================================================================

const DEFAULT_RELAYS = [
  'wss://relay.damus.io',
  'wss://relay.nostr.band',
  'wss://nos.lol'
]

// ============================================================================
// Key Management
// ============================================================================

interface KeyPair {
  sk: Uint8Array
  pk: string
  nsec: string
  npub: string
}

function generateKeyPair(): KeyPair {
  const sk = generateSecretKey()
  const pk = getPublicKey(sk)

  return {
    sk,
    pk,
    nsec: nip19.nsecEncode(sk),
    npub: nip19.npubEncode(pk)
  }
}

function importKeyPair(nsec: string): KeyPair {
  const { type, data } = nip19.decode(nsec)
  if (type !== 'nsec') throw new Error('Invalid nsec')

  const sk = data as Uint8Array
  const pk = getPublicKey(sk)

  return {
    sk,
    pk,
    nsec,
    npub: nip19.npubEncode(pk)
  }
}

// ============================================================================
// Nostr Client
// ============================================================================

interface NostrClientOptions {
  relays?: string[]
  keyPair?: KeyPair
}

class NostrClient {
  private pool: SimplePool
  private relays: string[]
  private keyPair: KeyPair

  constructor(options: NostrClientOptions = {}) {
    this.pool = new SimplePool()
    this.relays = options.relays ?? DEFAULT_RELAYS
    this.keyPair = options.keyPair ?? generateKeyPair()
  }

  // Getters
  get publicKey(): string {
    return this.keyPair.pk
  }

  get npub(): string {
    return this.keyPair.npub
  }

  // Publishing
  async publish(kind: number, content: string, tags: string[][] = []): Promise<Event> {
    const event = finalizeEvent({
      kind,
      created_at: Math.floor(Date.now() / 1000),
      tags,
      content
    }, this.keyPair.sk)

    await Promise.any(this.pool.publish(this.relays, event))
    return event
  }

  async publishNote(content: string): Promise<Event> {
    return this.publish(1, content)
  }

  // Querying
  async getEvent(id: string): Promise<Event | null> {
    return this.pool.get(this.relays, { ids: [id] })
  }

  async query(filter: Filter): Promise<Event[]> {
    return this.pool.querySync(this.relays, filter)
  }

  async getMyEvents(kind: number, limit = 20): Promise<Event[]> {
    return this.query({
      kinds: [kind],
      authors: [this.keyPair.pk],
      limit
    })
  }

  // Subscriptions
  subscribe(
    filter: Filter,
    onEvent: (event: Event) => void,
    onEose?: () => void
  ) {
    return this.pool.subscribeMany(
      this.relays,
      [filter],
      {
        onevent: onEvent,
        oneose: onEose
      }
    )
  }

  subscribeToNotes(authors: string[], onEvent: (event: Event) => void) {
    return this.subscribe(
      {
        kinds: [1],
        authors,
        since: Math.floor(Date.now() / 1000)
      },
      onEvent
    )
  }

  // Cleanup
  close() {
    this.pool.close(this.relays)
  }
}

// ============================================================================
// Usage Example
// ============================================================================

async function main() {
  // Create client
  const client = new NostrClient()

  console.log('Public key:', client.npub)

  // Publish a note
  const event = await client.publishNote('Hello from my Nostr client!')
  console.log('Published:', event.id)

  // Subscribe to your own notes
  const sub = client.subscribeToNotes([client.publicKey], (event) => {
    console.log('Received:', event.content)
  })

  // Query recent notes
  const notes = await client.getMyEvents(1, 10)
  console.log('My notes:', notes.length)

  // Cleanup
  // sub.close()
  // client.close()
}

// Export for use as module
export { NostrClient, generateKeyPair, importKeyPair }
export type { KeyPair, NostrClientOptions }
