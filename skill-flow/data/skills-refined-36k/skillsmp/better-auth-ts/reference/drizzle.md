# Better Auth + Drizzle ORM Integration

Complete guide for integrating Better Auth with Drizzle ORM.

## Installation

```bash
# npm
npm install better-auth drizzle-orm drizzle-kit
npm install -D @types/node

# pnpm
pnpm add better-auth drizzle-orm drizzle-kit
pnpm add -D @types/node

# yarn
yarn add better-auth drizzle-orm drizzle-kit
yarn add -D @types/node

# bun
bun add better-auth drizzle-orm drizzle-kit
bun add -D @types/node
```

### Database Driver (choose one)

```bash
# PostgreSQL
npm install pg
# or: pnpm add pg

# MySQL
npm install mysql2
# or: pnpm add mysql2

# SQLite (libsql/turso)
npm install @libsql/client
# or: pnpm add @libsql/client

# SQLite (better-sqlite3)
npm install better-sqlite3
# or: pnpm add better-sqlite3
```

## File Structure

```
project/
├── src/
│   ├── lib/
│   │   ├── auth.ts           # Better Auth config
│   │   └── auth-client.ts    # Client config
│   └── db/
│       ├── index.ts          # Drizzle instance
│       ├── schema.ts         # Your app schema
│       └── auth-schema.ts    # Generated auth schema
├── drizzle.config.ts         # Drizzle Kit config
└── .env
```

## Step-by-Step Setup

### 1. Create Drizzle Instance

```typescript
// src/db/index.ts
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import * as schema from "./schema";
import * as authSchema from "./auth-schema";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export const db = drizzle(pool, {
  schema: { ...schema, ...authSchema },
});

export type Database = typeof db;
```

**For MySQL:**
```typescript
import { drizzle } from "drizzle-orm/mysql2";
import mysql from "mysql2/promise";

const connection = await mysql.createConnection({
  uri: process.env.DATABASE_URL,
});

export const db = drizzle(connection, { schema: { ...schema, ...authSchema } });
```

**For SQLite (libsql/Turso):**
```typescript
import { drizzle } from "drizzle-orm/libsql";
import { createClient } from "@libsql/client";

const client = createClient({
  url: process.env.DATABASE_URL!,
  authToken: process.env.DATABASE_AUTH_TOKEN,
});

export const db = drizzle(client, { schema: { ...schema, ...authSchema } });
```

### 2. Configure Better Auth

```typescript
// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "@/db";
import * as authSchema from "@/db/auth-schema";

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg", // "pg" | "mysql" | "sqlite"
    schema: authSchema,
  }),
  emailAndPassword: {
    enabled: true,
  },
});

export type Auth = typeof auth;
```

### 3. Generate Auth Schema

```bash
# Generate Drizzle schema from your auth config
npx @better-auth/cli generate --output src/db/auth-schema.ts
```

This reads your `auth.ts` and generates the exact schema for your plugins.

### 4. Create Drizzle Config

```typescript
// drizzle.config.ts
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: ["./src/db/schema.ts", "./src/db/auth-schema.ts"],
  out: "./drizzle",
  dialect: "postgresql", // "postgresql" | "mysql" | "sqlite"
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
});
```

### 5. Run Migrations

```bash
# Generate migration files
npx drizzle-kit generate

# Push to database (dev)
npx drizzle-kit push

# Or run migrations (production)
npx drizzle-kit migrate
```

## Adding Plugins

When you add Better Auth plugins, regenerate the schema:

```typescript
// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { twoFactor, organization } from "better-auth/plugins";

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg",
    schema: authSchema,
  }),
  plugins: [
    twoFactor(),
    organization(),
  ],
});
```

Then regenerate:

```bash
# Regenerate schema with new plugin tables
npx @better-auth/cli generate --output src/db/auth-schema.ts

# Generate new migration
npx drizzle-kit generate

# Push changes
npx drizzle-kit push
```

## Custom User Fields

```typescript
// src/lib/auth.ts
export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg",
    schema: authSchema,
  }),
  user: {
    additionalFields: {
      role: {
        type: "string",
        defaultValue: "user",
      },
      plan: {
        type: "string",
        defaultValue: "free",
      },
    },
  },
});
```

After adding custom fields:
```bash
npx @better-auth/cli generate --output src/db/auth-schema.ts
npx drizzle-kit generate
npx drizzle-kit push
```

## Querying Auth Tables with Drizzle

```typescript
import { db } from "@/db";
import { user, session, account } from "@/db/auth-schema";
import { eq } from "drizzle-orm";

// Get user by email
const userByEmail = await db.query.user.findFirst({
  where: eq(user.email, "test@example.com"),
});

// Get user with sessions
const userWithSessions = await db.query.user.findFirst({
  where: eq(user.id, userId),
  with: {
    sessions: true,
  },
});

// Get user with accounts (OAuth connections)
const userWithAccounts = await db.query.user.findFirst({
  where: eq(user.id, userId),
  with: {
    accounts: true,
  },
});

// Count active sessions
const activeSessions = await db
  .select({ count: sql<number>`count(*)` })
  .from(session)
  .where(eq(session.userId, userId));
```

## Common Issues & Solutions

### Issue: Schema not found

```
Error: Schema "authSchema" is not defined
```

**Solution:** Ensure you're importing and passing the schema correctly:

```typescript
import * as authSchema from "@/db/auth-schema";

drizzleAdapter(db, {
  provider: "pg",
  schema: authSchema, // Not { authSchema }
});
```

### Issue: Table already exists

```
Error: relation "user" already exists
```

**Solution:** Use `drizzle-kit push` with `--force` or drop existing tables:

```bash
npx drizzle-kit push --force
```

### Issue: Type mismatch after regenerating

**Solution:** Clear Drizzle cache and regenerate:

```bash
rm -rf node_modules/.drizzle
npx @better-auth/cli generate --output src/db/auth-schema.ts
npx drizzle-kit generate
```

### Issue: Relations not working

**Solution:** Ensure your Drizzle instance includes both schemas:

```typescript
export const db = drizzle(pool, {
  schema: { ...schema, ...authSchema }, // Both schemas
});
```

## Environment Variables

```env
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# MySQL
DATABASE_URL=mysql://user:password@localhost:3306/mydb

# SQLite (local)
DATABASE_URL=file:./dev.db

# Turso
DATABASE_URL=libsql://your-db.turso.io
DATABASE_AUTH_TOKEN=your-token
```

## Production Considerations

1. **Use migrations, not push** in production:
   ```bash
   npx drizzle-kit migrate
   ```

2. **Version control your migrations**:
   ```
   drizzle/
   ├── 0000_initial.sql
   ├── 0001_add_2fa.sql
   └── meta/
   ```

3. **Backup before schema changes**

4. **Test migrations in staging first**

## Full Example

```typescript
// src/db/index.ts
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import * as schema from "./schema";
import * as authSchema from "./auth-schema";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export const db = drizzle(pool, {
  schema: { ...schema, ...authSchema },
});

// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { nextCookies } from "better-auth/next-js";
import { twoFactor } from "better-auth/plugins";
import { db } from "@/db";
import * as authSchema from "@/db/auth-schema";

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: "pg",
    schema: authSchema,
  }),
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  plugins: [
    nextCookies(),
    twoFactor(),
  ],
});
```
