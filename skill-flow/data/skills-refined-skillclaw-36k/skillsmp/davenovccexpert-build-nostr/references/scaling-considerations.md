<overview>
Nostr applications can encounter scaling challenges as usage grows. This reference covers performance optimization, relay load management, and architectural considerations for building scalable Nostr applications.
</overview>

<connection_scaling>
## Connection Management

**Problem:** Too many relay connections consume resources.

**Solution:** Limit connections intelligently:

```typescript
class ConnectionManager {
  private pool = new SimplePool()
  private maxRelays = 5
  private primaryRelays: string[]
  private userRelays = new Map<string, string[]>()

  constructor(primary: string[]) {
    this.primaryRelays = primary.slice(0, this.maxRelays)
  }

  // For general queries, use primary relays
  getPrimaryRelays(): string[] {
    return this.primaryRelays
  }

  // For specific user, use their announced relays (cached)
  async getUserRelays(pubkey: string): Promise<string[]> {
    if (!this.userRelays.has(pubkey)) {
      const event = await this.pool.get(this.primaryRelays, {
        kinds: [10002],
        authors: [pubkey]
      })

      const relays = event?.tags
        .filter(t => t[0] === 'r')
        .map(t => t[1])
        .slice(0, 3) || this.primaryRelays.slice(0, 2)

      this.userRelays.set(pubkey, relays)
    }
    return this.userRelays.get(pubkey)!
  }
}
```
</connection_scaling>

<subscription_management>
## Subscription Optimization

**Problem:** Too many open subscriptions cause memory leaks and slow performance.

**Solution:** Aggregate and deduplicate:

```typescript
class SubscriptionAggregator {
  private pool: SimplePool
  private relays: string[]
  private subscriptions = new Map<string, Set<(event: Event) => void>>()
  private activeFilters = new Map<string, Sub>()

  // Combine multiple listeners under one subscription
  subscribe(
    filterKey: string,
    filter: Filter,
    callback: (event: Event) => void
  ): () => void {
    if (!this.subscriptions.has(filterKey)) {
      this.subscriptions.set(filterKey, new Set())

      // Create single subscription for this filter
      const sub = this.pool.subscribeMany(this.relays, [filter], {
        onevent: (event) => {
          this.subscriptions.get(filterKey)?.forEach(cb => cb(event))
        }
      })

      this.activeFilters.set(filterKey, sub)
    }

    this.subscriptions.get(filterKey)!.add(callback)

    // Return unsubscribe function
    return () => {
      const listeners = this.subscriptions.get(filterKey)
      listeners?.delete(callback)

      if (listeners?.size === 0) {
        this.activeFilters.get(filterKey)?.close()
        this.activeFilters.delete(filterKey)
        this.subscriptions.delete(filterKey)
      }
    }
  }
}
```
</subscription_management>

<caching>
## Event Caching

**Problem:** Repeated queries for same data waste bandwidth.

**Solution:** Local cache with TTL:

```typescript
interface CachedEvent {
  event: Event
  cachedAt: number
}

class EventCache {
  private cache = new Map<string, CachedEvent>()
  private ttlMs: number

  constructor(ttlMs = 60000) {
    this.ttlMs = ttlMs
  }

  set(event: Event) {
    this.cache.set(event.id, {
      event,
      cachedAt: Date.now()
    })
  }

  get(id: string): Event | undefined {
    const cached = this.cache.get(id)
    if (!cached) return undefined

    if (Date.now() - cached.cachedAt > this.ttlMs) {
      this.cache.delete(id)
      return undefined
    }

    return cached.event
  }

  // For query caching, hash the filter
  static hashFilter(filter: Filter): string {
    return JSON.stringify(filter)
  }

  // Periodic cleanup
  cleanup() {
    const now = Date.now()
    for (const [id, cached] of this.cache) {
      if (now - cached.cachedAt > this.ttlMs) {
        this.cache.delete(id)
      }
    }
  }
}
```
</caching>

<pagination>
## Pagination

**Problem:** Loading all events at once is slow for large datasets.

**Solution:** Use `until` and `limit` for pagination:

```typescript
async function* paginatedQuery(
  pool: SimplePool,
  relays: string[],
  baseFilter: Filter,
  pageSize = 50
): AsyncGenerator<Event[]> {
  let until = Math.floor(Date.now() / 1000)
  let hasMore = true

  while (hasMore) {
    const events = await pool.querySync(relays, {
      ...baseFilter,
      until,
      limit: pageSize
    })

    if (events.length === 0) {
      hasMore = false
    } else {
      yield events

      // Next page starts before oldest event
      until = Math.min(...events.map(e => e.created_at)) - 1
      hasMore = events.length === pageSize
    }
  }
}

// Usage
for await (const page of paginatedQuery(pool, relays, { kinds: [1], authors: [pk] })) {
  console.log('Got page:', page.length)
}
```
</pagination>

<deduplication>
## Efficient Deduplication

**Problem:** Same event from multiple relays causes duplicates.

**Solution:** Bloom filter or LRU cache for seen IDs:

```typescript
class LRUDeduplicator {
  private seen: string[] = []
  private set = new Set<string>()
  private maxSize: number

  constructor(maxSize = 10000) {
    this.maxSize = maxSize
  }

  isDuplicate(id: string): boolean {
    if (this.set.has(id)) return true

    // Add to cache
    this.set.add(id)
    this.seen.push(id)

    // Evict oldest if over limit
    if (this.seen.length > this.maxSize) {
      const oldest = this.seen.shift()!
      this.set.delete(oldest)
    }

    return false
  }
}

// Usage
const dedup = new LRUDeduplicator()

pool.subscribeMany(relays, [filter], {
  onevent(event) {
    if (dedup.isDuplicate(event.id)) return
    processEvent(event)
  }
})
```
</deduplication>

<lazy_loading>
## Lazy Loading

**Problem:** Loading all related data upfront is slow.

**Solution:** Load on demand:

```typescript
class LazyEventLoader {
  private pool: SimplePool
  private relays: string[]
  private loadingPromises = new Map<string, Promise<Event | null>>()

  async loadEvent(id: string): Promise<Event | null> {
    // Return existing promise if loading
    if (this.loadingPromises.has(id)) {
      return this.loadingPromises.get(id)!
    }

    const promise = this.pool.get(this.relays, { ids: [id] })
    this.loadingPromises.set(id, promise)

    const result = await promise
    this.loadingPromises.delete(id)
    return result
  }

  async loadMany(ids: string[]): Promise<Map<string, Event>> {
    const results = new Map<string, Event>()
    const toLoad = ids.filter(id => !this.loadingPromises.has(id))

    if (toLoad.length > 0) {
      const events = await this.pool.querySync(this.relays, {
        ids: toLoad
      })

      events.forEach(e => results.set(e.id, e))
    }

    return results
  }
}
```
</lazy_loading>

<batch_operations>
## Batch Operations

**Problem:** Publishing many events one-by-one is slow.

**Solution:** Batch with rate limiting:

```typescript
class BatchPublisher {
  private queue: Event[] = []
  private publishing = false
  private batchSize = 10
  private delayMs = 100

  constructor(
    private pool: SimplePool,
    private relays: string[]
  ) {}

  add(event: Event) {
    this.queue.push(event)
    this.startPublishing()
  }

  private async startPublishing() {
    if (this.publishing) return
    this.publishing = true

    while (this.queue.length > 0) {
      const batch = this.queue.splice(0, this.batchSize)

      // Publish batch in parallel
      await Promise.allSettled(
        batch.flatMap(event => this.pool.publish(this.relays, event))
      )

      // Rate limit between batches
      if (this.queue.length > 0) {
        await new Promise(r => setTimeout(r, this.delayMs))
      }
    }

    this.publishing = false
  }
}
```
</batch_operations>

<metrics>
## Performance Metrics

Track performance for optimization:

```typescript
interface Metrics {
  queriesPerSecond: number
  averageLatencyMs: number
  cacheHitRate: number
  activeSubscriptions: number
  eventsProcessed: number
}

class MetricsCollector {
  private queryCount = 0
  private totalLatency = 0
  private cacheHits = 0
  private cacheMisses = 0
  private activeSubscriptions = 0
  private eventsProcessed = 0
  private lastReset = Date.now()

  recordQuery(latencyMs: number) {
    this.queryCount++
    this.totalLatency += latencyMs
  }

  recordCacheHit() { this.cacheHits++ }
  recordCacheMiss() { this.cacheMisses++ }
  incrementSubscriptions() { this.activeSubscriptions++ }
  decrementSubscriptions() { this.activeSubscriptions-- }
  recordEvent() { this.eventsProcessed++ }

  getMetrics(): Metrics {
    const elapsed = (Date.now() - this.lastReset) / 1000

    return {
      queriesPerSecond: this.queryCount / elapsed,
      averageLatencyMs: this.queryCount > 0 ? this.totalLatency / this.queryCount : 0,
      cacheHitRate: (this.cacheHits + this.cacheMisses) > 0
        ? this.cacheHits / (this.cacheHits + this.cacheMisses)
        : 0,
      activeSubscriptions: this.activeSubscriptions,
      eventsProcessed: this.eventsProcessed
    }
  }

  reset() {
    this.queryCount = 0
    this.totalLatency = 0
    this.cacheHits = 0
    this.cacheMisses = 0
    this.eventsProcessed = 0
    this.lastReset = Date.now()
  }
}
```
</metrics>

<best_practices>
## Scaling Best Practices

1. **Limit relay connections** - 3-5 relays is usually enough
2. **Cache aggressively** - Events are immutable, cache freely
3. **Use pagination** - Don't load everything at once
4. **Aggregate subscriptions** - Combine similar filters
5. **Close unused subscriptions** - Prevent memory leaks
6. **Rate limit publishing** - Respect relay limits
7. **Deduplicate early** - Before processing
8. **Lazy load references** - Load on demand
9. **Monitor metrics** - Know your bottlenecks
10. **Use ephemeral kinds wisely** - For true real-time only
</best_practices>
