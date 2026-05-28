---
name: nuxthub
description: Use this skill when building NuxtHub v0.10.4 applications, which provide database (Drizzle ORM with SQLite/PostgreSQL/MySQL), KV storage, blob storage, and cache APIs, along with multi-cloud deployment support.
---

# NuxtHub v0.10.4

Full-stack Nuxt framework with database, KV, blob, and cache. Multi-cloud support (Cloudflare, Vercel, Deno, Netlify).

**For Nuxt server patterns:** use `nuxt` skill (server.md)  
**For content with database:** use `nuxt-content` skill

## Installation

```bash
npx nuxi module add hub
```

## Configuration

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['@nuxthub/core'],
  hub: {
    db: 'sqlite', // 'sqlite' | 'postgresql' | 'mysql'
    kv: true,
    blob: true,
    cache: true,
    dir: '.data', // local storage directory
    remote: false, // use production bindings in dev (v0.10.4+)
  },
})
```

### Advanced Config

```ts
hub: {
  db: {
    dialect: 'postgresql',
    driver: 'postgres-js', // Optional: auto-detected
    casing: 'snake_case',  // camelCase JS -> snake_case DB
    migrationsDirs: ['server/db/custom-migrations/'],
    applyMigrationsDuringBuild: true // default
  },
  remote: true // Use production Cloudflare bindings in dev (v0.10.4+)
}
```

**Remote mode:** When enabled, connects to production D1/KV/R2 during local development instead of local emulation. Useful for testing with production data.

## Database

Type-safe SQL via Drizzle ORM. `db` and `schema` are auto-imported on server-side.

### Schema Definition

Place in `server/db/schema.ts` or `server/db/schema/*.ts`:

```ts
// server/db/schema.ts (SQLite)
import { integer, sqliteTable, text } from 'drizzle-orm/sqlite-core'

export const users = sqliteTable('users', {
  id: integer().primaryKey({ autoIncrement: true }),
  name: text().notNull(),
  email: text().notNull().unique(),
  createdAt: integer({ mode: 'timestamp' }).notNull(),
})
```

PostgreSQL variant:

```ts
import { pgTable, serial, text, timestamp } from 'drizzle-orm/pg-core'

export const users = pgTable('users', {
  id: serial().primaryKey(),
  name: text().notNull(),
  email: text().notNull().unique(),
  createdAt: timestamp().notNull().defaultNow(),
})
```

### Database API

```ts
// db and schema are auto-imported on server-side
import { db, schema } from 'hub:db'

// Select
const users = await db.select().from(schema.users)
```