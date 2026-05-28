# Optimization Patterns

Detailed code examples for frontend, backend, and algorithm optimizations.

## Frontend Optimizations

### Bundle Size Reduction

```typescript
// ❌ Import entire library (adds 70KB+)
import _ from 'lodash';
import { format } from 'date-fns';

// ✅ Tree-shakeable imports (adds ~2KB each)
import debounce from 'lodash/debounce';
import { format } from 'date-fns/format';

// ✅ Dynamic imports for code splitting
const HeavyComponent = lazy(() => import('./HeavyComponent'));
const ChartLibrary = lazy(() => import('recharts'));
```

### Rendering Optimization

```typescript
// ❌ Re-renders on every parent update
function ProductList({ products, filter }) {
  const filtered = products.filter(p => p.category === filter);
  return filtered.map(p => <ProductCard key={p.id} product={p} />);
}

// ✅ Memoized computation + component
const ProductList = memo(function ProductList({ products, filter }) {
  const filtered = useMemo(
    () => products.filter(p => p.category === filter),
    [products, filter]
  );

  return filtered.map(p => <ProductCard key={p.id} product={p} />);
});

// ✅ Virtualized list for 1000+ items
import { FixedSizeList } from 'react-window';

function VirtualizedList({ items }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {({ index, style }) => (
        <div style={style}>{items[index].name}</div>
      )}
    </FixedSizeList>
  );
}
```

### Image Optimization

```html
<!-- ❌ Unoptimized -->
<img src="hero.jpg" />

<!-- ✅ Fully optimized -->
<img
  src="hero.webp"
  srcset="hero-400.webp 400w, hero-800.webp 800w, hero-1200.webp 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  loading="lazy"
  decoding="async"
  alt="Hero image"
  width="1200"
  height="600"
/>

<!-- ✅ Next.js Image component -->
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority={false}
  placeholder="blur"
/>
```

---

## Backend Optimizations

### N+1 Query Resolution

```typescript
// ❌ N+1 Problem - 101 queries for 100 users
async function getUsers() {
  const users = await db.user.findMany();
  for (const user of users) {
    user.orders = await db.order.findMany({ where: { userId: user.id } });
  }
  return users;
}

// ✅ Eager loading - 1 query with JOIN
async function getUsers() {
  return db.user.findMany({
    include: { orders: true }
  });
}

// ✅ DataLoader for GraphQL (batching)
const userLoader = new DataLoader(async (userIds) => {
  const users = await db.user.findMany({
    where: { id: { in: userIds } }
  });
  return userIds.map(id => users.find(u => u.id === id));
});
```

### Multi-Layer Caching

```typescript
// 3-tier caching strategy
class CacheService {
  private memoryCache = new Map<string, { data: any; expiry: number }>();

  async get<T>(key: string): Promise<T | null> {
    // L1: In-memory (fastest, ~0.1ms)
    const memory = this.memoryCache.get(key);
    if (memory && memory.expiry > Date.now()) {
      return memory.data;
    }

    // L2: Redis (fast, ~1-5ms)
    const redis = await this.redis.get(key);
    if (redis) {
      const data = JSON.parse(redis);
      this.memoryCache.set(key, { data, expiry: Date.now() + 60000 });
      return data;
    }

    // L3: Database (slow, ~10-100ms)
    return null;
  }

  async set<T>(key: string, data: T, ttl: number): Promise<void> {
    // Write to all layers
    this.memoryCache.set(key, { data, expiry: Date.now() + 60000 });
    await this.redis.setex(key, ttl, JSON.stringify(data));
  }
}
```

### Async Processing with Queue

```typescript
// ❌ Blocking operation (user waits 5+ minutes)
app.post('/upload', async (req, res) => {
  await processVideo(req.file);  // Takes 5 minutes
  res.send('Done');
});

// ✅ Queue for background processing
import { Queue, Worker } from 'bullmq';

const videoQueue = new Queue('video-processing');

app.post('/upload', async (req, res) => {
  const job = await videoQueue.add('process', {
    fileId: req.file.id,
    userId: req.user.id
  });
  res.json({ jobId: job.id, status: 'processing' });
});

// Separate worker process
new Worker('video-processing', async (job) => {
  await processVideo(job.data.fileId);
  await notifyUser(job.data.userId, 'Video ready!');
});
```

---

## Algorithm Optimizations

```typescript
// ❌ O(n²) - Nested loops
function findDuplicates(arr: number[]): number[] {
  const duplicates: number[] = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j] && !duplicates.includes(arr[i])) {
        duplicates.push(arr[i]);
      }
    }
  }
  return duplicates;
}

// ✅ O(n) - Hash map
function findDuplicates(arr: number[]): number[] {
  const seen = new Set<number>();
  const duplicates = new Set<number>();
  for (const item of arr) {
    if (seen.has(item)) duplicates.add(item);
    seen.add(item);
  }
  return [...duplicates];
}

// ❌ O(n) lookup in array
const users = [{ id: 1, name: 'A' }, { id: 2, name: 'B' }, ...];
const user = users.find(u => u.id === targetId);

// ✅ O(1) lookup with Map
const userMap = new Map(users.map(u => [u.id, u]));
const user = userMap.get(targetId);
```

---

Version: 1.0.0
Source: jikime-workflow-performance SKILL.md
