# NuxtHub

**Check if installed:** Look for `@nuxthub/core` in package.json before using.

**Last updated:** 2025-12 (v0.10)

## Overview

NuxtHub is a full-stack Nuxt framework providing database, blob storage, KV storage, and caching with multi-cloud support. v0.10 introduced multi-vendor deployment and Drizzle ORM integration.

## Installation

```bash
npx nuxi module add @nuxthub/core
```

## Configuration

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ["@nuxthub/core"],
  hub: {
    db: "postgresql", // 'postgresql' | 'mysql' | 'sqlite' | false
    blob: true, // boolean | BlobConfig
    kv: true, // boolean | KVConfig
    cache: true, // boolean | CacheConfig
    dir: ".data", // Local dev storage directory
  },
})
```

## Multi-Vendor Support (v0.10)

NuxtHub auto-detects deployment providers:

| Feature  | Cloudflare  | Vercel        | AWS |
| -------- | ----------- | ------------- | --- |
| Database | D1 (SQLite) | -             | -   |
| Blob     | R2          | Vercel Blob   | S3  |
| KV       | Workers KV  | Vercel KV     | -   |
| Cache    | KV          | Runtime Cache | -   |

Fallbacks: PGLite (local PostgreSQL), filesystem storage.

---

## Database (Drizzle ORM)

### Dependencies

```bash
# PostgreSQL
pnpm add drizzle-orm drizzle-kit postgres @electric-sql/pglite

# MySQL
pnpm add drizzle-orm drizzle-kit mysql2

# SQLite
pnpm add drizzle-orm drizzle-kit @libsql/client
```

### Schema Definition

Schemas auto-scan from:

- `server/db/schema.ts`
- `server/db/schema/*.ts`
- `server/db/schema.{dialect}.ts`

```typescript
// server/db/schema.ts
import { pgTable, text, serial, timestamp } from "drizzle-orm/pg-core"

export const users = pgTable("users", {
  id: serial().primaryKey(),
  name: text().notNull(),
  email: text().notNull().unique(),
  createdAt: timestamp().notNull().defaultNow(),
})

export const posts = pgTable("posts", {
  id: serial().primaryKey(),
  title: text().notNull(),
  content: text(),
  authorId: serial().references(() => users.id),
})
```

### Database Operations

```typescript
// server/api/users.get.ts
import { db, schema } from "hub:db"
import { eq } from "drizzle-orm"

export default defineEventHandler(async () => {
  // Select all
  return await db.select().from(schema.users)

  // Or use query API
  return await db.query.users.findMany()
})
```

```typescript
// server/api/users.post.ts
import { db, schema } from "hub:db"

export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  const [user] = await db
    .insert(schema.users)
    .values({ name: body.name, email: body.email })
    .returning()

  return user
})
```

```typescript
// server/api/users/[id].patch.ts
import { db, schema } from "hub:db"
import { eq } from "drizzle-orm"

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, "id")
  const body = await readBody(event)

  const [updated] = await db
    .update(schema.users)
    .set({ name: body.name })
    .where(eq(schema.users.id, Number(id)))
    .returning()

  return updated
})
```

```typescript
// server/api/users/[id].delete.ts
import { db, schema } from "hub:db"
import { eq } from "drizzle-orm"

export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, "id")

  await db.delete(schema.users).where(eq(schema.users.id, Number(id)))

  return { success: true }
})
```

### Type Sharing

```typescript
// shared/types/db.ts (auto-imports to client/server)
import { users, posts } from "hub:db:schema"

export type User = typeof users.$inferSelect
export type NewUser = typeof users.$inferInsert
export type Post = typeof posts.$inferSelect
```

### Migrations CLI

```bash
npx nuxt db generate      # Generate migration files
npx nuxt db migrate       # Apply pending migrations
npx nuxt db drop [TABLE]  # Drop a table
npx nuxt db sql [QUERY]   # Execute raw SQL
npx nuxt db mark-as-migrated [NAME]  # Mark as applied
```

Migration files: `server/db/migrations/{dialect}/`

### Database Seeding

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  nitro: {
    experimental: { tasks: true },
  },
})
```

```typescript
// server/tasks/seed.ts
import { db, schema } from "hub:db"

export default defineTask({
  meta: { name: "db:seed" },
  async run() {
    await db.insert(schema.users).values([
      { name: "Alice", email: "alice@example.com" },
      { name: "Bob", email: "bob@example.com" },
    ])
    return { result: "Database seeded" }
  },
})
```

Run via Nuxt DevTools → Tasks tab.

---

## Blob Storage

### Configuration

```typescript
export default defineNuxtConfig({
  hub: {
    blob: true,
  },
})
```

Provider packages:

- Vercel: `@vercel/blob`
- AWS S3: `aws4fetch`
- Cloudflare: auto-configured via wrangler

### Server API

```typescript
// server/api/files/index.get.ts
export default defineEventHandler(async () => {
  const blobs = await hubBlob().list({
    limit: 100,
    prefix: "uploads/",
  })
  return blobs
})
```

```typescript
// server/api/files/[...pathname].get.ts
export default defineEventHandler(async (event) => {
  const pathname = getRouterParam(event, "pathname")
  return hubBlob().serve(event, pathname)
})
```

```typescript
// server/api/files/upload.post.ts
export default defineEventHandler(async (event) => {
  return hubBlob().handleUpload(event, {
    formKey: "file",
    multiple: false,
    ensure: {
      maxSize: "10MB",
      types: ["image/jpeg", "image/png", "image/webp"],
    },
  })
})
```

### Blob Methods

| Method                            | Description                                  |
| --------------------------------- | -------------------------------------------- |
| `list(options?)`                  | List blobs with pagination, prefix filtering |
| `head(pathname)`                  | Get blob metadata                            |
| `get(pathname)`                   | Get blob data as Blob object                 |
| `serve(event, pathname)`          | Serve blob with proper headers               |
| `put(pathname, body, options?)`   | Upload blob                                  |
| `del(pathname \| pathnames[])`    | Delete blob(s)                               |
| `handleUpload(event, options)`    | Validate and upload in one call              |
| `createMultipartUpload(pathname)` | Start chunked upload                         |
| `handleMultipartUpload(event)`    | Auto multipart handler                       |

### Vue Composables

```vue
<script setup lang="ts">
const { upload, isUploading } = useUpload("/api/files/upload")

async function handleFile(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (file) {
    const blob = await upload(file)
    console.log("Uploaded:", blob)
  }
}
</script>
```

```vue
<script setup lang="ts">
// For large files
const { upload, progress } = useMultipartUpload("/api/files/multipart")
</script>
```

### Validation

```typescript
// Validate before upload
ensureBlob(file, {
  maxSize: "5MB",
  types: ["image/jpeg", "image/png"],
})
```

---

## KV Storage

### Configuration

```typescript
export default defineNuxtConfig({
  hub: {
    kv: true,
  },
})
```

Provider packages:

- Upstash: `@upstash/redis`
- Redis: `ioredis`

### Server API

```typescript
// Auto-imported on server
import { kv } from "hub:kv"

// Set value (with optional TTL in seconds)
await kv.set("user:123", { name: "Alice", role: "admin" })
await kv.set("session:abc", { userId: 123 }, { ttl: 3600 })

// Get value
const user = await kv.get("user:123")

// Check existence
const exists = await kv.has("user:123")

// Delete
await kv.del("user:123")

// List keys (with optional prefix)
const keys = await kv.keys()
const userKeys = await kv.keys("user")

// Clear namespace
await kv.clear()
await kv.clear("session") // Clear all session:* keys
```

### Constraints

- Max value size: 25 MiB
- Max key length: 512 bytes
- Use colons for namespacing: `user:123`, `session:abc`

---

## Cache

### Configuration

```typescript
export default defineNuxtConfig({
  hub: {
    cache: true,
  },
})
```

### Cached Event Handlers

```typescript
// server/api/posts.get.ts
export default cachedEventHandler(
  async () => {
    const posts = await db.query.posts.findMany()
    return posts
  },
  {
    maxAge: 60 * 60, // 1 hour
    staleMaxAge: 60 * 60 * 24, // Serve stale for 24h while revalidating
    name: "posts",
    getKey: () => "all",
  },
)
```

### Cached Functions

```typescript
// server/utils/github.ts
export const getGitHubStars = defineCachedFunction(
  async (repo: string) => {
    const data = await $fetch(`https://api.github.com/repos/${repo}`)
    return data.stargazers_count
  },
  {
    maxAge: 60 * 60,
    name: "github-stars",
    getKey: (repo) => repo,
  },
)
```

### Route Rules (Hybrid Caching)

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    "/api/posts": { cache: { maxAge: 3600 } },
    "/api/user/**": { cache: false },
  },
})
```

### Cache Invalidation

```typescript
// Manual invalidation
const storage = useStorage("cache")
await storage.removeItem("nitro:handlers:posts:all.json")
await storage.removeItem("nitro:functions:github-stars:nuxt/nuxt.json")
```

Cache key pattern: `${group}:${name}:${getKey()}.json`

---

## Local Development

### DevTools Integration

NuxtHub integrates with Nuxt DevTools providing:

- Drizzle Studio for database management
- Blob storage browser
- KV storage inspector
- Cache management

### Storage Directory

Local data stored in `.data/` directory (auto-added to .gitignore).

---

## Migration from v0.9

### Config Changes

```typescript
// Before (v0.9)
hub: {
  database: true,
}

// After (v0.10)
hub: {
  db: 'sqlite',  // Explicit dialect
}
```

### File Structure

```
# Before
server/database/schema.ts

# After
server/db/schema.ts
```

### API Changes

```typescript
// Before (v0.9)
const db = hubDatabase()

// After (v0.10)
import { db, schema } from "hub:db"
```

---

## Environment Variables

### Cloudflare D1 over HTTP

```env
NUXT_HUB_CLOUDFLARE_ACCOUNT_ID=your-account-id
NUXT_HUB_CLOUDFLARE_API_TOKEN=your-api-token
NUXT_HUB_CLOUDFLARE_DATABASE_ID=your-d1-id
```

### AWS S3

```env
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-bucket
```

### Upstash Redis

```env
UPSTASH_REDIS_REST_URL=your-url
UPSTASH_REDIS_REST_TOKEN=your-token
```

---

## Important Notes

### NuxtHub Admin Sunset

- December 31, 2025: NuxtHub Admin sunset
- February 2, 2026: Legacy CLI/GitHub Actions deprecated
- Migrate to native provider deployment (Workers Builds, Vercel CLI, etc.)

### Legacy Docs

Access v0.9 docs at: https://legacy.hub.nuxt.com

### Official Docs

For latest features: https://hub.nuxt.com/docs
