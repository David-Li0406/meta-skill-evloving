# Workflow: Create Custom Event Kinds for App Data

<required_reading>
**Read these reference files NOW:**
1. references/event-kinds.md
2. references/data-exchange-patterns.md
3. references/custom-protocols.md
</required_reading>

<process>
## Step 1: Understand Kind Ranges

Choose your kind number based on storage behavior:

| Range | Type | Use When |
|-------|------|----------|
| 1000-9999 | Regular | All events should be stored permanently |
| 10000-19999 | Replaceable | Only latest version matters (per pubkey+kind) |
| 20000-29999 | Ephemeral | Real-time only, no storage needed |
| 30000-39999 | Addressable | Latest per pubkey+kind+d-tag (like database rows) |

**For app data exchange:**
- User settings → Addressable (30000+) with d-tag as setting key
- Real-time sync → Ephemeral (20000+)
- Audit log → Regular (1000+)

## Step 2: Define Your Event Schema

```typescript
// Define the kind number
const APP_DATA_KIND = 30078  // Addressable, parameterized

// Define the content structure
interface AppDataEvent {
  version: number
  type: string
  data: unknown
  checksum?: string
}

// Define required tags
// 'd' tag is required for addressable events
// Use additional tags for filtering
```

## Step 3: Create Type-Safe Event Builder

```typescript
import { finalizeEvent, type UnsignedEvent } from 'nostr-tools/pure'

interface CreateAppEventOptions {
  dataType: string
  dataId: string
  data: unknown
  references?: Array<{ type: 'event' | 'pubkey', id: string }>
}

function createAppEvent(
  options: CreateAppEventOptions,
  sk: Uint8Array
): Event {
  const tags: string[][] = [
    ['d', `${options.dataType}:${options.dataId}`],  // Unique identifier
    ['t', options.dataType]  // Type tag for filtering
  ]

  // Add references
  options.references?.forEach(ref => {
    if (ref.type === 'event') {
      tags.push(['e', ref.id])
    } else {
      tags.push(['p', ref.id])
    }
  })

  const content: AppDataEvent = {
    version: 1,
    type: options.dataType,
    data: options.data
  }

  return finalizeEvent({
    kind: APP_DATA_KIND,
    created_at: Math.floor(Date.now() / 1000),
    tags,
    content: JSON.stringify(content)
  }, sk)
}
```

## Step 4: Create Query Helpers

```typescript
import { type Filter } from 'nostr-tools'

function queryByType(dataType: string, author?: string): Filter {
  const filter: Filter = {
    kinds: [APP_DATA_KIND],
    '#t': [dataType]
  }

  if (author) {
    filter.authors = [author]
  }

  return filter
}

function queryById(dataType: string, dataId: string, author?: string): Filter {
  return {
    kinds: [APP_DATA_KIND],
    '#d': [`${dataType}:${dataId}`],
    ...(author && { authors: [author] })
  }
}

function queryByTimeRange(
  dataType: string,
  since: Date,
  until?: Date
): Filter {
  return {
    kinds: [APP_DATA_KIND],
    '#t': [dataType],
    since: Math.floor(since.getTime() / 1000),
    ...(until && { until: Math.floor(until.getTime() / 1000) })
  }
}
```

## Step 5: Implement CRUD Operations

```typescript
class NostrDataStore {
  constructor(
    private pool: SimplePool,
    private relays: string[],
    private sk: Uint8Array
  ) {}

  private pk = getPublicKey(this.sk)

  // CREATE / UPDATE (same operation for addressable events)
  async save(type: string, id: string, data: unknown): Promise<string> {
    const event = createAppEvent({ dataType: type, dataId: id, data }, this.sk)
    await Promise.any(this.pool.publish(this.relays, event))
    return event.id
  }

  // READ one
  async get<T>(type: string, id: string): Promise<T | null> {
    const event = await this.pool.get(
      this.relays,
      queryById(type, id, this.pk)
    )

    if (!event) return null

    const parsed = JSON.parse(event.content) as AppDataEvent
    return parsed.data as T
  }

  // READ many
  async list<T>(type: string, limit = 100): Promise<T[]> {
    const events = await this.pool.querySync(
      this.relays,
      { ...queryByType(type, this.pk), limit }
    )

    return events.map(e => {
      const parsed = JSON.parse(e.content) as AppDataEvent
      return parsed.data as T
    })
  }

  // DELETE (publish empty/deleted marker)
  async delete(type: string, id: string): Promise<void> {
    const event = createAppEvent(
      { dataType: type, dataId: id, data: { deleted: true } },
      this.sk
    )
    await Promise.any(this.pool.publish(this.relays, event))
  }
}
```

## Step 6: Handle Schema Migrations

```typescript
interface AppDataEvent {
  version: number  // Always include version!
  type: string
  data: unknown
}

function migrateData(event: AppDataEvent): AppDataEvent {
  switch (event.version) {
    case 1:
      // Migrate v1 → v2
      return {
        ...event,
        version: 2,
        data: migrateV1ToV2(event.data)
      }
    case 2:
      // Current version
      return event
    default:
      throw new Error(`Unknown version: ${event.version}`)
  }
}
```

## Step 7: Document Your Event Kind

Create documentation for your custom kind:

```markdown
## Kind 30078: Application Data

### Purpose
Store application-specific structured data with addressable semantics.

### Tags
- `d` (required): Unique identifier in format `{type}:{id}`
- `t`: Data type for filtering
- `e`: Referenced events
- `p`: Referenced pubkeys

### Content
JSON object:
```json
{
  "version": 1,
  "type": "user_preference",
  "data": { ... }
}
```

### Behavior
- Addressable: Latest event per pubkey+kind+d-tag is kept
- Clients should verify version compatibility
```
</process>

<anti_patterns>
Avoid:
- Using existing standardized kinds for custom purposes
- Not versioning your content schema
- Large content payloads (>64KB) - use references instead
- Not including d-tag for addressable events
- Storing sensitive data unencrypted
- Deeply nested JSON (hard to query with tags)
- Not documenting your event kind schema
</anti_patterns>

<success_criteria>
A well-designed custom event kind:
- Uses appropriate kind range for storage behavior
- Has versioned content schema
- Uses tags for efficient filtering
- Has type-safe builders and parsers
- Handles schema migrations
- Is documented for other developers
- Follows NIP conventions (lowercase hex, proper tag format)
</success_criteria>
