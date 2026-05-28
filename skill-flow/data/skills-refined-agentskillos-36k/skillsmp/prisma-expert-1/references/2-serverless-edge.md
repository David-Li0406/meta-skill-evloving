# 2. Serverless & Edge Deployment

**Impact: CRITICAL**

Prisma 7 is designed for the edge. The new TypeScript-based query engine eliminates the need for the heavy Rust binary.

## 2.1 The Rust-free WASM Engine

To use Prisma in Edge runtimes (Vercel Edge, Cloudflare Workers), you must enable the WASM engine.

**`prisma/schema.prisma`**
```prisma
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["driverAdapters"]
}
```

**Client Initialization:**
```typescript
import { PrismaClient } from '@prisma/client'
import { PrismaNeon } from '@prisma/adapter-neon'
import { Pool } from '@neondatabase/serverless'

const pool = new Pool({ connectionString: process.env.DATABASE_URL })
const adapter = new PrismaNeon(pool)
export const prisma = new PrismaClient({ adapter })
```

## 2.2 Prisma Accelerate

Prisma Accelerate provides a global connection pool and cache via HTTP. It is the mandatory standard for high-traffic serverless apps in 2026.

**Benefits:**
- **Connection Pooling**: Prevents "Too many connections" errors in Lambda/Edge.
- **Global Caching**: Sub-millisecond reads from the nearest edge node.

```typescript
// query with caching
const user = await prisma.user.findUnique({
  where: { id: '123' },
  cacheStrategy: { swr: 60, ttl: 60 }, // Cache for 60s
});
```

## 2.3 Regional Execution

Always deploy your serverless functions in the **same region** as your database.
- If your DB is in `us-east-1` (N. Virginia), your Vercel/AWS functions should be in `us-east-1`.
- Internal latency can add 50-100ms per query if regions are mismatched.
