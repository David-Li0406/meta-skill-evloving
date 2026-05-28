/**
 * Custom Event Schema Template
 *
 * A typed, versioned event schema for application-specific
 * data storage on Nostr with addressable events.
 */

import { generateSecretKey, getPublicKey, finalizeEvent } from 'nostr-tools/pure'
import { SimplePool } from 'nostr-tools/pool'
import type { Event, Filter } from 'nostr-tools'

// ============================================================================
// Schema Definition
// ============================================================================

/**
 * Define your application's data types here.
 * Always include a version for schema evolution.
 */

// Version 1 of our schema
interface AppDataV1 {
  version: 1
  type: 'settings' | 'document' | 'list'
  data: unknown
  metadata: {
    createdAt: number
    updatedAt: number
    tags?: string[]
  }
}

// When you need to migrate, define V2
interface AppDataV2 {
  version: 2
  type: 'settings' | 'document' | 'list' | 'template'  // Added new type
  data: unknown
  metadata: {
    createdAt: number
    updatedAt: number
    tags?: string[]
    author?: string  // Added new field
  }
}

// Union type for all versions
type AppData = AppDataV1 | AppDataV2

// Current version helper
type CurrentAppData = AppDataV2
const CURRENT_VERSION = 2

// ============================================================================
// Configuration
// ============================================================================

// Addressable kind - stores latest per pubkey+kind+d-tag
const APP_DATA_KIND = 30078

const DEFAULT_RELAYS = [
  'wss://relay.damus.io',
  'wss://nos.lol'
]

// ============================================================================
// Type Guards & Validators
// ============================================================================

function isAppDataV1(data: unknown): data is AppDataV1 {
  if (typeof data !== 'object' || data === null) return false
  const obj = data as Record<string, unknown>
  return (
    obj.version === 1 &&
    typeof obj.type === 'string' &&
    ['settings', 'document', 'list'].includes(obj.type) &&
    typeof obj.metadata === 'object'
  )
}

function isAppDataV2(data: unknown): data is AppDataV2 {
  if (typeof data !== 'object' || data === null) return false
  const obj = data as Record<string, unknown>
  return (
    obj.version === 2 &&
    typeof obj.type === 'string' &&
    ['settings', 'document', 'list', 'template'].includes(obj.type) &&
    typeof obj.metadata === 'object'
  )
}

function isAppData(data: unknown): data is AppData {
  return isAppDataV1(data) || isAppDataV2(data)
}

// ============================================================================
// Schema Migration
// ============================================================================

function migrateToLatest(data: AppData): CurrentAppData {
  if (data.version === 2) {
    return data
  }

  // Migrate V1 -> V2
  if (data.version === 1) {
    return {
      version: 2,
      type: data.type,
      data: data.data,
      metadata: {
        ...data.metadata,
        author: undefined  // New field, no value from V1
      }
    }
  }

  throw new Error(`Unknown version: ${(data as AppData).version}`)
}

// ============================================================================
// Event Builder
// ============================================================================

interface CreateEventOptions {
  type: CurrentAppData['type']
  id: string  // Unique identifier for this data item
  data: unknown
  tags?: string[]
}

class AppEventBuilder {
  private sk: Uint8Array
  private pk: string
  private namespace: string

  constructor(sk: Uint8Array, namespace = 'myapp') {
    this.sk = sk
    this.pk = getPublicKey(sk)
    this.namespace = namespace
  }

  private getDTag(type: string, id: string): string {
    return `${this.namespace}:${type}:${id}`
  }

  create(options: CreateEventOptions): Event {
    const now = Date.now()

    const appData: CurrentAppData = {
      version: CURRENT_VERSION,
      type: options.type,
      data: options.data,
      metadata: {
        createdAt: now,
        updatedAt: now,
        tags: options.tags,
        author: this.pk
      }
    }

    const nostrTags: string[][] = [
      ['d', this.getDTag(options.type, options.id)],
      ['t', this.namespace],
      ['t', `${this.namespace}:${options.type}`]
    ]

    // Add custom tags for filtering
    if (options.tags) {
      options.tags.forEach(tag => {
        nostrTags.push(['t', tag])
      })
    }

    return finalizeEvent({
      kind: APP_DATA_KIND,
      created_at: Math.floor(now / 1000),
      tags: nostrTags,
      content: JSON.stringify(appData)
    }, this.sk)
  }

  update(options: CreateEventOptions, existingCreatedAt: number): Event {
    const now = Date.now()

    const appData: CurrentAppData = {
      version: CURRENT_VERSION,
      type: options.type,
      data: options.data,
      metadata: {
        createdAt: existingCreatedAt,
        updatedAt: now,
        tags: options.tags,
        author: this.pk
      }
    }

    const nostrTags: string[][] = [
      ['d', this.getDTag(options.type, options.id)],
      ['t', this.namespace],
      ['t', `${this.namespace}:${options.type}`]
    ]

    if (options.tags) {
      options.tags.forEach(tag => {
        nostrTags.push(['t', tag])
      })
    }

    return finalizeEvent({
      kind: APP_DATA_KIND,
      created_at: Math.floor(now / 1000),
      tags: nostrTags,
      content: JSON.stringify(appData)
    }, this.sk)
  }

  markDeleted(type: string, id: string): Event {
    const appData: CurrentAppData = {
      version: CURRENT_VERSION,
      type: type as CurrentAppData['type'],
      data: { deleted: true },
      metadata: {
        createdAt: Date.now(),
        updatedAt: Date.now(),
        author: this.pk
      }
    }

    return finalizeEvent({
      kind: APP_DATA_KIND,
      created_at: Math.floor(Date.now() / 1000),
      tags: [
        ['d', this.getDTag(type, id)],
        ['deleted', 'true']
      ],
      content: JSON.stringify(appData)
    }, this.sk)
  }
}

// ============================================================================
// Event Repository
// ============================================================================

interface ParsedEvent<T> {
  event: Event
  appData: CurrentAppData
  data: T
}

class AppDataRepository {
  private pool: SimplePool
  private relays: string[]
  private builder: AppEventBuilder
  private pk: string
  private namespace: string

  constructor(
    sk: Uint8Array,
    options: { relays?: string[]; namespace?: string } = {}
  ) {
    this.pool = new SimplePool()
    this.relays = options.relays ?? DEFAULT_RELAYS
    this.namespace = options.namespace ?? 'myapp'
    this.builder = new AppEventBuilder(sk, this.namespace)
    this.pk = getPublicKey(sk)
  }

  private getDTag(type: string, id: string): string {
    return `${this.namespace}:${type}:${id}`
  }

  private parseEvent<T>(event: Event): ParsedEvent<T> | null {
    try {
      const raw = JSON.parse(event.content)

      if (!isAppData(raw)) {
        console.warn('Invalid app data format')
        return null
      }

      const appData = migrateToLatest(raw)

      // Check for deleted marker
      const deletedTag = event.tags.find(t => t[0] === 'deleted')
      if (deletedTag) {
        return null
      }

      return {
        event,
        appData,
        data: appData.data as T
      }
    } catch (err) {
      console.error('Failed to parse event:', err)
      return null
    }
  }

  // -------------------------------------------------------------------------
  // CRUD Operations
  // -------------------------------------------------------------------------

  async save<T>(type: CurrentAppData['type'], id: string, data: T, tags?: string[]): Promise<Event> {
    // Check if exists (for createdAt preservation)
    const existing = await this.get<T>(type, id)

    const event = existing
      ? this.builder.update({ type, id, data, tags }, existing.appData.metadata.createdAt)
      : this.builder.create({ type, id, data, tags })

    await Promise.any(this.pool.publish(this.relays, event))
    return event
  }

  async get<T>(type: string, id: string): Promise<ParsedEvent<T> | null> {
    const event = await this.pool.get(this.relays, {
      kinds: [APP_DATA_KIND],
      authors: [this.pk],
      '#d': [this.getDTag(type, id)]
    })

    if (!event) return null
    return this.parseEvent<T>(event)
  }

  async list<T>(type: string, limit = 100): Promise<ParsedEvent<T>[]> {
    const events = await this.pool.querySync(this.relays, {
      kinds: [APP_DATA_KIND],
      authors: [this.pk],
      '#t': [`${this.namespace}:${type}`],
      limit
    })

    return events
      .map(e => this.parseEvent<T>(e))
      .filter((p): p is ParsedEvent<T> => p !== null)
  }

  async listByTag<T>(tag: string, limit = 100): Promise<ParsedEvent<T>[]> {
    const events = await this.pool.querySync(this.relays, {
      kinds: [APP_DATA_KIND],
      authors: [this.pk],
      '#t': [tag],
      limit
    })

    return events
      .map(e => this.parseEvent<T>(e))
      .filter((p): p is ParsedEvent<T> => p !== null)
  }

  async delete(type: string, id: string): Promise<void> {
    const event = this.builder.markDeleted(type, id)
    await Promise.any(this.pool.publish(this.relays, event))
  }

  // -------------------------------------------------------------------------
  // Subscriptions
  // -------------------------------------------------------------------------

  subscribe<T>(
    type: string,
    onChange: (item: ParsedEvent<T>, eventType: 'create' | 'update' | 'delete') => void
  ) {
    return this.pool.subscribeMany(
      this.relays,
      [{
        kinds: [APP_DATA_KIND],
        authors: [this.pk],
        '#t': [`${this.namespace}:${type}`],
        since: Math.floor(Date.now() / 1000)
      }],
      {
        onevent: (event) => {
          const deletedTag = event.tags.find(t => t[0] === 'deleted')
          if (deletedTag) {
            onChange({ event, appData: {} as CurrentAppData, data: {} as T }, 'delete')
            return
          }

          const parsed = this.parseEvent<T>(event)
          if (parsed) {
            const isNew = parsed.appData.metadata.createdAt === parsed.appData.metadata.updatedAt
            onChange(parsed, isNew ? 'create' : 'update')
          }
        }
      }
    )
  }

  // -------------------------------------------------------------------------
  // Cleanup
  // -------------------------------------------------------------------------

  close(): void {
    this.pool.close(this.relays)
  }
}

// ============================================================================
// Usage Example
// ============================================================================

// Define your data types
interface UserSettings {
  theme: 'light' | 'dark'
  notifications: boolean
  language: string
}

interface Document {
  title: string
  content: string
  status: 'draft' | 'published'
}

async function main() {
  const sk = generateSecretKey()
  const repo = new AppDataRepository(sk, { namespace: 'myapp' })

  // Save settings
  await repo.save<UserSettings>('settings', 'user-prefs', {
    theme: 'dark',
    notifications: true,
    language: 'en'
  })

  // Save a document
  await repo.save<Document>('document', 'doc-1', {
    title: 'My First Document',
    content: 'Hello, world!',
    status: 'draft'
  }, ['important', 'draft'])

  // Read settings
  const settings = await repo.get<UserSettings>('settings', 'user-prefs')
  console.log('Settings:', settings?.data)

  // List all documents
  const docs = await repo.list<Document>('document')
  console.log('Documents:', docs.map(d => d.data.title))

  // Subscribe to document changes
  const sub = repo.subscribe<Document>('document', (item, type) => {
    console.log(`Document ${type}:`, item.data.title)
  })

  // Update document
  await repo.save<Document>('document', 'doc-1', {
    title: 'My First Document',
    content: 'Updated content!',
    status: 'published'
  }, ['important', 'published'])

  // Delete document
  await repo.delete('document', 'doc-1')

  // Cleanup
  // sub.close()
  // repo.close()
}

// Export
export {
  AppEventBuilder,
  AppDataRepository,
  migrateToLatest,
  isAppData,
  APP_DATA_KIND,
  CURRENT_VERSION
}
export type { AppData, AppDataV1, AppDataV2, CurrentAppData, ParsedEvent }
