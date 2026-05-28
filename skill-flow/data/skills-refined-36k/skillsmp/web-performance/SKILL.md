---
name: web-performance
description: Performance patterns for Apollo caching, Redis, and CloudFront optimization
user-invocable: false
---

# Web Performance Skill

**Version:** 1.0
**Stack:** Apollo Client/Server + Redis + CloudFront + S3

> Performance optimization across the stack: caching, bundle size, and infrastructure.

---

## Core Principles

1. **Measure First** — Profile before optimizing. Don't guess.
2. **Cache at Every Layer** — CDN → API → Database → In-Memory.
3. **Minimize Payload** — Send only what's needed.
4. **Defer Non-Critical** — Load critical path first, everything else later.
5. **Perceived Performance** — Optimistic UI makes things feel faster.

---

## Core Web Vitals Targets

| Metric | What It Measures | Target | Critical |
|--------|------------------|--------|----------|
| **LCP** (Largest Contentful Paint) | Main content loaded | < 2.5s | < 4s |
| **INP** (Interaction to Next Paint) | Input responsiveness | < 200ms | < 500ms |
| **CLS** (Cumulative Layout Shift) | Visual stability | < 0.1 | < 0.25 |

---

## Apollo Client Caching

### Cache Configuration

```typescript
// apollo/client.ts
import { ApolloClient, InMemoryCache } from '@apollo/client';

const cache = new InMemoryCache({
  typePolicies: {
    Query: {
      fields: {
        // Merge paginated results
        products: {
          keyArgs: ['filter', 'orderBy'], // Cache separately per filter
          merge(existing, incoming, { args }) {
            if (!args?.after) {
              // First page - replace cache
              return incoming;
            }
            // Subsequent pages - append
            return {
              ...incoming,
              edges: [...(existing?.edges || []), ...incoming.edges],
            };
          },
        },
      },
    },

    Product: {
      fields: {
        // Computed field from cache
        formattedPrice: {
          read(_, { readField }) {
            const price = readField('price');
            return `$${(price / 100).toFixed(2)}`;
          },
        },
      },
    },
  },
});

export const client = new ApolloClient({
  uri: '/graphql',
  cache,
  defaultOptions: {
    watchQuery: {
      // Stale-while-revalidate by default
      fetchPolicy: 'cache-and-network',
      nextFetchPolicy: 'cache-first',
    },
  },
});
```

### Fetch Policies

| Policy | Use Case |
|--------|----------|
| `cache-first` | Static data (categories, config) |
| `cache-and-network` | Data that changes (products, user data) |
| `network-only` | Always fresh (order status, real-time) |
| `cache-only` | Offline mode, known-cached data |

```typescript
// Static data - cache forever
const { data } = useQuery(GET_CATEGORIES, {
  fetchPolicy: 'cache-first',
});

// User data - stale-while-revalidate
const { data } = useQuery(GET_CURRENT_USER, {
  fetchPolicy: 'cache-and-network',
});

// Order status - always fresh
const { data } = useQuery(GET_ORDER_STATUS, {
  fetchPolicy: 'network-only',
  pollInterval: 5000, // Poll every 5s
});
```

### Optimistic Updates

```typescript
const [addToCart] = useMutation(ADD_TO_CART, {
  // Show result immediately
  optimisticResponse: {
    addToCart: {
      __typename: 'CartItem',
      id: `temp-${Date.now()}`,
      productId,
      quantity: 1,
      product: {
        __typename: 'Product',
        id: productId,
        name: product.name,
        price: product.price,
      },
    },
  },

  // Update cache without refetching
  update(cache, { data: { addToCart } }) {
    cache.modify({
      fields: {
        cart(existingItems = []) {
          const newItemRef = cache.writeFragment({
            data: addToCart,
            fragment: CART_ITEM_FRAGMENT,
          });
          return [...existingItems, newItemRef];
        },
        cartTotal(existing = 0) {
          return existing + addToCart.product.price;
        },
      },
    });
  },
});
```

---

## Redis Caching

### Caching Strategy

```typescript
// services/cache.ts
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

interface CacheOptions {
  ttl?: number;  // Seconds
  tags?: string[];
}

export const cache = {
  async get<T>(key: string): Promise<T | null> {
    const data = await redis.get(key);
    return data ? JSON.parse(data) : null;
  },

  async set<T>(key: string, value: T, options: CacheOptions = {}): Promise<void> {
    const { ttl = 3600 } = options; // Default 1 hour
    await redis.setex(key, ttl, JSON.stringify(value));
  },

  async invalidate(pattern: string): Promise<void> {
    const keys = await redis.keys(pattern);
    if (keys.length) {
      await redis.del(...keys);
    }
  },
};
```

### Cache-Aside Pattern

```typescript
// services/product.service.ts
export class ProductService {
  async findById(id: string) {
    const cacheKey = `product:${id}`;

    // Try cache first
    const cached = await cache.get<Product>(cacheKey);
    if (cached) {
      return cached;
    }

    // Cache miss - fetch from database
    const product = await this.prisma.product.findUnique({
      where: { id },
      include: { category: true },
    });

    if (product) {
      // Cache for 1 hour
      await cache.set(cacheKey, product, { ttl: 3600 });
    }

    return product;
  }

  async update(id: string, input: UpdateProductInput) {
    const product = await this.prisma.product.update({
      where: { id },
      data: input,
    });

    // Invalidate cache
    await cache.invalidate(`product:${id}`);
    await cache.invalidate('products:*'); // Invalidate list caches

    return product;
  }
}
```

### TTL Guidelines

| Data Type | TTL | Reason |
|-----------|-----|--------|
| Static config | 24h+ | Rarely changes |
| Product catalog | 1h | Changes occasionally |
| User sessions | 30m | Security balance |
| Cart data | 7d | User convenience |
| Search results | 5m | Balance freshness/speed |
| Real-time data | No cache | Must be live |

---

## CloudFront & S3 Optimization

### Static Asset Caching

```typescript
// CloudFront cache behaviors (CDK example)
const distribution = new cloudfront.Distribution(this, 'Distribution', {
  defaultBehavior: {
    origin: new origins.S3Origin(bucket),
    cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
    viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
  },
  additionalBehaviors: {
    // Immutable assets (hashed filenames)
    '/static/*': {
      origin: new origins.S3Origin(bucket),
      cachePolicy: new cloudfront.CachePolicy(this, 'ImmutableCache', {
        defaultTtl: Duration.days(365),
        maxTtl: Duration.days(365),
        minTtl: Duration.days(365),
      }),
    },
    // API - no caching at CDN
    '/graphql': {
      origin: new origins.HttpOrigin(apiDomain),
      cachePolicy: cloudfront.CachePolicy.CACHING_DISABLED,
      allowedMethods: cloudfront.AllowedMethods.ALLOW_ALL,
    },
  },
});
```

### Image Optimization

```typescript
// Generate optimized image URLs
function getImageUrl(key: string, options: ImageOptions = {}) {
  const { width, height, quality = 80, format = 'webp' } = options;

  // Use CloudFront image resizing or external service
  const params = new URLSearchParams();
  if (width) params.set('w', String(width));
  if (height) params.set('h', String(height));
  params.set('q', String(quality));
  params.set('fm', format);

  return `${CDN_URL}/${key}?${params.toString()}`;
}

// React component
function ProductImage({ product, size = 'medium' }) {
  const sizes = { small: 150, medium: 300, large: 600 };
  const width = sizes[size];

  return (
    <img
      src={getImageUrl(product.imageKey, { width, format: 'webp' })}
      srcSet={`
        ${getImageUrl(product.imageKey, { width, format: 'webp' })} 1x,
        ${getImageUrl(product.imageKey, { width: width * 2, format: 'webp' })} 2x
      `}
      alt={product.name}
      loading="lazy"
      decoding="async"
      width={width}
      height={width}
    />
  );
}
```

---

## Bundle Optimization

### Code Splitting

```typescript
// Route-based splitting
import { lazy, Suspense } from 'react';

const ProductPage = lazy(() => import('./features/products/ProductPage'));
const CheckoutPage = lazy(() => import('./features/checkout/CheckoutPage'));
const AdminDashboard = lazy(() => import('./features/admin/Dashboard'));

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/products/:id" element={<ProductPage />} />
        <Route path="/checkout" element={<CheckoutPage />} />
        <Route path="/admin/*" element={<AdminDashboard />} />
      </Routes>
    </Suspense>
  );
}
```

### Dynamic Imports for Heavy Libraries

```typescript
// ❌ Bad - Loads chart library on every page
import { Chart } from 'chart.js';

// ✅ Good - Loads only when needed
async function renderChart(data) {
  const { Chart } = await import('chart.js');
  // Use chart...
}

// Or with React
const ChartComponent = lazy(() =>
  import('./ChartComponent').then(module => ({
    default: module.ChartComponent,
  }))
);
```

### Bundle Size Guidelines

| Category | Target | Action if Exceeded |
|----------|--------|-------------------|
| Initial JS | < 100KB gzipped | Code split, tree shake |
| Vendor chunk | < 150KB gzipped | Lazy load, find alternatives |
| Route chunk | < 50KB gzipped | Split further |
| Total initial load | < 200KB gzipped | Audit dependencies |

### Analyzing Bundle

```bash
# Create bundle analysis
npm run build -- --analyze

# Or with source-map-explorer
npx source-map-explorer build/static/js/*.js
```

---

## React Performance

### Memoization

```typescript
// Expensive computation
const sortedProducts = useMemo(
  () => products.sort((a, b) => a.price - b.price),
  [products]
);

// Stable callback for child components
const handleAddToCart = useCallback(
  (productId: string) => {
    addToCart({ variables: { productId } });
  },
  [addToCart]
);

// Memoized component for lists
const ProductCard = memo(function ProductCard({ product, onAddToCart }) {
  return (
    <article className="product-card">
      {/* ... */}
    </article>
  );
});
```

### When NOT to Memoize

```typescript
// ❌ Don't memoize simple values
const fullName = useMemo(() => `${first} ${last}`, [first, last]); // Just inline it
const fullName = `${first} ${last}`;

// ❌ Don't memoize if always changes
const timestamp = useMemo(() => Date.now(), []); // Defeats the purpose

// ❌ Don't memoize inline handlers on non-memoized children
<button onClick={() => doThing()}>Click</button> // Fine if button isn't memoized
```

### Virtualization for Long Lists

```typescript
import { useVirtualizer } from '@tanstack/react-virtual';

function ProductList({ products }) {
  const parentRef = useRef(null);

  const virtualizer = useVirtualizer({
    count: products.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 200, // Estimated row height
    overscan: 5,
  });

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map(virtualItem => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            <ProductCard product={products[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## Database Performance

### Prisma Query Optimization

```typescript
// ✅ Select only needed fields
const products = await prisma.product.findMany({
  select: {
    id: true,
    name: true,
    price: true,
    // Don't select description if not needed
  },
});

// ✅ Use include sparingly
const order = await prisma.order.findUnique({
  where: { id },
  include: {
    items: {
      include: {
        product: {
          select: { id: true, name: true, price: true },
        },
      },
    },
    // Don't include user if not needed
  },
});

// ✅ Use raw queries for complex aggregations
const stats = await prisma.$queryRaw`
  SELECT
    category_id,
    COUNT(*) as product_count,
    AVG(price) as avg_price
  FROM products
  WHERE active = true
  GROUP BY category_id
`;
```

### Index Strategy

```prisma
// prisma/schema.prisma
model Product {
  id         String   @id @default(uuid())
  name       String
  price      Int
  categoryId String
  active     Boolean  @default(true)
  createdAt  DateTime @default(now())

  category   Category @relation(fields: [categoryId], references: [id])

  // Compound index for common queries
  @@index([categoryId, active])
  @@index([active, createdAt(sort: Desc)])
  // Full-text search (PostgreSQL)
  @@index([name], type: Gin)
}
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Fetching all fields** | Over-fetching, slow | Select only needed fields |
| **No pagination** | Memory issues, slow | Cursor-based pagination |
| **Cache everything** | Stale data, complexity | Cache strategically by TTL |
| **Premature optimization** | Wasted effort | Measure first, optimize hotspots |
| **Sync heavy operations** | Blocks response | Background jobs (Bull) |
| **No CDN for static assets** | Slow global delivery | CloudFront for static files |
| **Unoptimized images** | Huge downloads | Resize, compress, WebP |
| **Blocking bundle** | Slow initial load | Code split, lazy load |

---

## Checklist

### Frontend
- [ ] Code split by route
- [ ] Heavy libraries lazy loaded
- [ ] Images lazy loaded
- [ ] Images optimized (WebP, sized)
- [ ] Bundle < 200KB initial
- [ ] useMemo/useCallback where beneficial
- [ ] Long lists virtualized

### Apollo
- [ ] Cache policies configured
- [ ] Pagination merges correctly
- [ ] Optimistic updates for mutations
- [ ] Fetch policy matches data freshness needs

### Redis
- [ ] Hot data cached
- [ ] TTLs appropriate for data type
- [ ] Cache invalidation on updates
- [ ] Connection pooling configured

### Database
- [ ] Indices on filtered/sorted columns
- [ ] Select only needed fields
- [ ] N+1 queries eliminated (DataLoader)
- [ ] Expensive queries analyzed

### CDN
- [ ] Static assets on CloudFront
- [ ] Immutable assets cached forever
- [ ] Dynamic content not cached at edge
- [ ] HTTPS enforced

---

## When to Consider Alternatives

| Situation | Consider |
|-----------|----------|
| Global real-time data | Redis Pub/Sub or WebSockets |
| Heavy computation | Background workers (Bull) |
| Large file uploads | Direct S3 presigned URLs |
| Search-heavy | Elasticsearch or Algolia |
| Edge computing needs | CloudFront Functions or Lambda@Edge |
