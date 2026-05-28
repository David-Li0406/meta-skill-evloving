<overview>
Nostr can serve as a decentralized data layer for applications that need to sync state across clients. This reference covers patterns for structured data exchange, state synchronization, and building data-driven applications on Nostr.
</overview>

<state_sync>
## State Synchronization

Use addressable events for state that needs to be updated:

```typescript
const STATE_KIND = 30078  // Addressable

interface AppState {
  version: number
  data: unknown
  updatedAt: number
}

class StateSyncer {
  constructor(
    private pool: SimplePool,
    private relays: string[],
    private sk: Uint8Array,
    private stateKey: string
  ) {}

  private pk = getPublicKey(this.sk)

  // Save state (overwrites previous)
  async save(data: unknown): Promise<void> {
    const state: AppState = {
      version: 1,
      data,
      updatedAt: Date.now()
    }

    const event = finalizeEvent({
      kind: STATE_KIND,
      created_at: Math.floor(Date.now() / 1000),
      tags: [['d', this.stateKey]],
      content: JSON.stringify(state)
    }, this.sk)

    await Promise.any(this.pool.publish(this.relays, event))
  }

  // Load latest state
  async load<T>(): Promise<T | null> {
    const event = await this.pool.get(this.relays, {
      kinds: [STATE_KIND],
      authors: [this.pk],
      '#d': [this.stateKey]
    })

    if (!event) return null

    const state = JSON.parse(event.content) as AppState
    return state.data as T
  }

  // Watch for changes
  watch<T>(onChange: (data: T) => void) {
    return this.pool.subscribeMany(this.relays, [{
      kinds: [STATE_KIND],
      authors: [this.pk],
      '#d': [this.stateKey]
    }], {
      onevent: (event) => {
        const state = JSON.parse(event.content) as AppState
        onChange(state.data as T)
      }
    })
  }
}
```
</state_sync>

<crdt_pattern>
## CRDT-Like Merge Pattern

For collaborative data, use timestamps for conflict resolution:

```typescript
interface CRDTValue<T> {
  value: T
  timestamp: number
  author: string
}

class LWWRegister<T> {
  private current: CRDTValue<T> | null = null

  merge(incoming: CRDTValue<T>): boolean {
    if (!this.current || incoming.timestamp > this.current.timestamp) {
      this.current = incoming
      return true  // State changed
    }
    return false
  }

  get(): T | undefined {
    return this.current?.value
  }
}

// Usage with Nostr
class NostrCRDT<T> {
  private register = new LWWRegister<T>()

  constructor(
    private pool: SimplePool,
    private relays: string[],
    private sk: Uint8Array,
    private dataId: string
  ) {}

  async sync() {
    const events = await this.pool.querySync(this.relays, {
      kinds: [30078],
      '#d': [this.dataId]
    })

    events.forEach(event => {
      const data = JSON.parse(event.content) as CRDTValue<T>
      this.register.merge(data)
    })

    return this.register.get()
  }

  async update(value: T) {
    const crdtValue: CRDTValue<T> = {
      value,
      timestamp: Date.now(),
      author: getPublicKey(this.sk)
    }

    this.register.merge(crdtValue)

    const event = finalizeEvent({
      kind: 30078,
      created_at: Math.floor(Date.now() / 1000),
      tags: [['d', this.dataId]],
      content: JSON.stringify(crdtValue)
    }, this.sk)

    await Promise.any(this.pool.publish(this.relays, event))
  }
}
```
</crdt_pattern>

<collection_pattern>
## Collection Pattern

Store multiple items with unique IDs:

```typescript
const COLLECTION_KIND = 30078

interface CollectionItem<T> {
  id: string
  data: T
  createdAt: number
  updatedAt: number
}

class NostrCollection<T> {
  constructor(
    private pool: SimplePool,
    private relays: string[],
    private sk: Uint8Array,
    private collectionName: string
  ) {}

  private pk = getPublicKey(this.sk)

  private getDTag(itemId: string): string {
    return `${this.collectionName}:${itemId}`
  }

  async add(id: string, data: T): Promise<void> {
    const item: CollectionItem<T> = {
      id,
      data,
      createdAt: Date.now(),
      updatedAt: Date.now()
    }

    const event = finalizeEvent({
      kind: COLLECTION_KIND,
      created_at: Math.floor(Date.now() / 1000),
      tags: [
        ['d', this.getDTag(id)],
        ['t', this.collectionName]
      ],
      content: JSON.stringify(item)
    }, this.sk)

    await Promise.any(this.pool.publish(this.relays, event))
  }

  async get(id: string): Promise<T | null> {
    const event = await this.pool.get(this.relays, {
      kinds: [COLLECTION_KIND],
      authors: [this.pk],
      '#d': [this.getDTag(id)]
    })

    if (!event) return null
    return (JSON.parse(event.content) as CollectionItem<T>).data
  }

  async list(): Promise<CollectionItem<T>[]> {
    const events = await this.pool.querySync(this.relays, {
      kinds: [COLLECTION_KIND],
      authors: [this.pk],
      '#t': [this.collectionName]
    })

    return events.map(e => JSON.parse(e.content) as CollectionItem<T>)
  }

  async delete(id: string): Promise<void> {
    // Publish with deleted flag (Nostr doesn't truly delete)
    const event = finalizeEvent({
      kind: COLLECTION_KIND,
      created_at: Math.floor(Date.now() / 1000),
      tags: [
        ['d', this.getDTag(id)],
        ['t', this.collectionName],
        ['deleted', 'true']
      ],
      content: JSON.stringify({ deleted: true })
    }, this.sk)

    await Promise.any(this.pool.publish(this.relays, event))
  }
}
```
</collection_pattern>

<linked_data>
## Linked Data Pattern

Reference events from other events:

```typescript
// Create an item that references another
async function createWithReference(
  data: unknown,
  referencedEventId: string,
  referencedPubkey: string
) {
  const event = finalizeEvent({
    kind: 30078,
    created_at: Math.floor(Date.now() / 1000),
    tags: [
      ['d', crypto.randomUUID()],
      ['e', referencedEventId],  // Event reference
      ['p', referencedPubkey]    // Author reference
    ],
    content: JSON.stringify(data)
  }, sk)

  return event
}

// Query all events referencing a specific event
async function getReferences(eventId: string): Promise<Event[]> {
  return pool.querySync(relays, {
    kinds: [30078],
    '#e': [eventId]
  })
}

// Reference addressable event
function createAddressableReference(kind: number, pubkey: string, dTag: string): string {
  return `${kind}:${pubkey}:${dTag}`
}

async function createWithAddressableRef(data: unknown, ref: string) {
  const event = finalizeEvent({
    kind: 30078,
    created_at: Math.floor(Date.now() / 1000),
    tags: [
      ['d', crypto.randomUUID()],
      ['a', ref]  // Addressable reference
    ],
    content: JSON.stringify(data)
  }, sk)

  return event
}
```
</linked_data>

<chunked_data>
## Large Data / Chunked Pattern

For data larger than typical event limits (~64KB):

```typescript
interface ChunkedData {
  id: string
  totalChunks: number
  chunkIndex: number
  data: string  // Base64 chunk
}

const CHUNK_SIZE = 32000  // Safe limit for content

async function uploadLargeData(data: Buffer, dataId: string): Promise<void> {
  const base64 = data.toString('base64')
  const totalChunks = Math.ceil(base64.length / CHUNK_SIZE)

  const chunkEvents: Event[] = []

  for (let i = 0; i < totalChunks; i++) {
    const chunkData: ChunkedData = {
      id: dataId,
      totalChunks,
      chunkIndex: i,
      data: base64.slice(i * CHUNK_SIZE, (i + 1) * CHUNK_SIZE)
    }

    const event = finalizeEvent({
      kind: 30078,
      created_at: Math.floor(Date.now() / 1000),
      tags: [
        ['d', `${dataId}:chunk:${i}`],
        ['t', 'chunked-data'],
        ['parent', dataId]
      ],
      content: JSON.stringify(chunkData)
    }, sk)

    chunkEvents.push(event)
  }

  // Publish all chunks
  await Promise.all(chunkEvents.map(e =>
    Promise.any(pool.publish(relays, e))
  ))
}

async function downloadLargeData(dataId: string): Promise<Buffer> {
  const events = await pool.querySync(relays, {
    kinds: [30078],
    '#parent': [dataId]
  })

  const chunks = events
    .map(e => JSON.parse(e.content) as ChunkedData)
    .sort((a, b) => a.chunkIndex - b.chunkIndex)

  if (chunks.length !== chunks[0]?.totalChunks) {
    throw new Error('Missing chunks')
  }

  const base64 = chunks.map(c => c.data).join('')
  return Buffer.from(base64, 'base64')
}
```
</chunked_data>

<versioning>
## Versioned Data Pattern

Track versions for optimistic updates:

```typescript
interface VersionedData<T> {
  version: number
  data: T
  previousEventId?: string
}

class VersionedStore<T> {
  private currentVersion = 0
  private currentEventId?: string

  async update(data: T): Promise<{ eventId: string; version: number }> {
    const versioned: VersionedData<T> = {
      version: this.currentVersion + 1,
      data,
      previousEventId: this.currentEventId
    }

    const event = finalizeEvent({
      kind: 30078,
      created_at: Math.floor(Date.now() / 1000),
      tags: [
        ['d', this.dataId],
        ['version', String(versioned.version)]
      ],
      content: JSON.stringify(versioned)
    }, this.sk)

    await Promise.any(pool.publish(relays, event))

    this.currentVersion = versioned.version
    this.currentEventId = event.id

    return { eventId: event.id, version: versioned.version }
  }

  async getHistory(): Promise<VersionedData<T>[]> {
    const events = await pool.querySync(relays, {
      kinds: [30078],
      '#d': [this.dataId]
    })

    return events
      .map(e => JSON.parse(e.content) as VersionedData<T>)
      .sort((a, b) => a.version - b.version)
  }
}
```
</versioning>

<multi_party>
## Multi-Party Data Exchange

Exchange data between known parties:

```typescript
interface SharedSpace {
  id: string
  members: string[]  // Pubkeys
}

class SharedDataSpace {
  constructor(
    private pool: SimplePool,
    private relays: string[],
    private sk: Uint8Array,
    private space: SharedSpace
  ) {}

  // Subscribe to updates from all members
  watch(onUpdate: (data: unknown, from: string) => void) {
    return this.pool.subscribeMany(this.relays, [{
      kinds: [30078],
      authors: this.space.members,
      '#space': [this.space.id]
    }], {
      onevent: (event) => {
        onUpdate(JSON.parse(event.content), event.pubkey)
      }
    })
  }

  // Publish to shared space
  async publish(data: unknown): Promise<void> {
    const event = finalizeEvent({
      kind: 30078,
      created_at: Math.floor(Date.now() / 1000),
      tags: [
        ['d', `${this.space.id}:${Date.now()}`],
        ['space', this.space.id],
        ...this.space.members.map(m => ['p', m])
      ],
      content: JSON.stringify(data)
    }, this.sk)

    await Promise.any(this.pool.publish(this.relays, event))
  }
}
```
</multi_party>

<best_practices>
## Best Practices

1. **Always version your data schema** - Include version field in content
2. **Use d-tags for addressable updates** - Enables "upsert" semantics
3. **Keep payloads small** - Under 64KB, use chunking for larger data
4. **Handle missing data** - Relays may not have everything
5. **Deduplicate on client** - Same event from multiple relays
6. **Use timestamps for ordering** - Don't rely on relay order
7. **Validate incoming data** - Don't trust content structure
8. **Consider encryption** - Use NIP-44 for sensitive data
</best_practices>
