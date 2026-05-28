# Better Auth + Kysely Integration

Complete guide for integrating Better Auth with Kysely.

## Installation

```bash
# npm
npm install better-auth kysely

# pnpm
pnpm add better-auth kysely

# yarn
yarn add better-auth kysely

# bun
bun add better-auth kysely
```

### Database Driver (choose one)

```bash
# PostgreSQL
npm install pg
# or: pnpm add pg

# MySQL
npm install mysql2
# or: pnpm add mysql2

# SQLite
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
│       ├── index.ts          # Kysely instance
│       └── types.ts          # Database types
└── .env
```

## Step-by-Step Setup

### 1. Define Database Types

```typescript
// src/db/types.ts
import type { Generated, Insertable, Selectable, Updateable } from "kysely";

export interface Database {
  user: UserTable;
  session: SessionTable;
  account: AccountTable;
  verification: VerificationTable;
  // Add your app tables here
}

export interface UserTable {
  id: string;
  name: string;
  email: string;
  emailVerified: boolean;
  image: string | null;
  createdAt: Generated<Date>;
  updatedAt: Date;
}

export interface SessionTable {
  id: string;
  expiresAt: Date;
  token: string;
  ipAddress: string | null;
  userAgent: string | null;
  userId: string;
  createdAt: Generated<Date>;
  updatedAt: Date;
}

export interface AccountTable {
  id: string;
  accountId: string;
  providerId: string;
  userId: string;
  accessToken: string | null;
  refreshToken: string | null;
  idToken: string | null;
  accessTokenExpiresAt: Date | null;
  refreshTokenExpiresAt: Date | null;
  scope: string | null;
  password: string | null;
  createdAt: Generated<Date>;
  updatedAt: Date;
}

export interface VerificationTable {
  id: string;
  identifier: string;
  value: string;
  expiresAt: Date;
  createdAt: Generated<Date>;
  updatedAt: Date;
}

// Type helpers
export type User = Selectable<UserTable>;
export type NewUser = Insertable<UserTable>;
export type UserUpdate = Updateable<UserTable>;
```

### 2. Create Kysely Instance

**PostgreSQL:**

```typescript
// src/db/index.ts
import { Kysely, PostgresDialect } from "kysely";
import { Pool } from "pg";
import type { Database } from "./types";

const dialect = new PostgresDialect({
  pool: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
});

export const db = new Kysely<Database>({ dialect });
```

**MySQL:**

```typescript
import { Kysely, MysqlDialect } from "kysely";
import { createPool } from "mysql2";

const dialect = new MysqlDialect({
  pool: createPool({
    uri: process.env.DATABASE_URL,
  }),
});

export const db = new Kysely<Database>({ dialect });
```

**SQLite:**

```typescript
import { Kysely, SqliteDialect } from "kysely";
import Database from "better-sqlite3";

const dialect = new SqliteDialect({
  database: new Database("./dev.db"),
});

export const db = new Kysely<Database>({ dialect });
```

### 3. Configure Better Auth

```typescript
// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { kyselyAdapter } from "better-auth/adapters/kysely";
import { db } from "@/db";

export const auth = betterAuth({
  database: kyselyAdapter(db, {
    provider: "pg", // "pg" | "mysql" | "sqlite"
  }),
  emailAndPassword: {
    enabled: true,
  },
});

export type Auth = typeof auth;
```

### 4. Create Tables

```typescript
// src/db/migrate.ts
import { db } from "./index";
import { sql } from "kysely";

async function migrate() {
  // User table
  await db.schema
    .createTable("user")
    .ifNotExists()
    .addColumn("id", "text", (col) => col.primaryKey())
    .addColumn("name", "text", (col) => col.notNull())
    .addColumn("email", "text", (col) => col.notNull().unique())
    .addColumn("emailVerified", "boolean", (col) => col.defaultTo(false).notNull())
    .addColumn("image", "text")
    .addColumn("createdAt", "timestamp", (col) => col.defaultTo(sql`now()`).notNull())
    .addColumn("updatedAt", "timestamp", (col) => col.notNull())
    .execute();

  // Session table
  await db.schema
    .createTable("session")
    .ifNotExists()
    .addColumn("id", "text", (col) => col.primaryKey())
    .addColumn("expiresAt", "timestamp", (col) => col.notNull())
    .addColumn("token", "text", (col) => col.notNull().unique())
    .addColumn("ipAddress", "text")
    .addColumn("userAgent", "text")
    .addColumn("userId", "text", (col) => col.notNull().references("user.id").onDelete("cascade"))
    .addColumn("createdAt", "timestamp", (col) => col.defaultTo(sql`now()`).notNull())
    .addColumn("updatedAt", "timestamp", (col) => col.notNull())
    .execute();

  await db.schema
    .createIndex("session_userId_idx")
    .ifNotExists()
    .on("session")
    .column("userId")
    .execute();

  // Account table
  await db.schema
    .createTable("account")
    .ifNotExists()
    .addColumn("id", "text", (col) => col.primaryKey())
    .addColumn("accountId", "text", (col) => col.notNull())
    .addColumn("providerId", "text", (col) => col.notNull())
    .addColumn("userId", "text", (col) => col.notNull().references("user.id").onDelete("cascade"))
    .addColumn("accessToken", "text")
    .addColumn("refreshToken", "text")
    .addColumn("idToken", "text")
    .addColumn("accessTokenExpiresAt", "timestamp")
    .addColumn("refreshTokenExpiresAt", "timestamp")
    .addColumn("scope", "text")
    .addColumn("password", "text")
    .addColumn("createdAt", "timestamp", (col) => col.defaultTo(sql`now()`).notNull())
    .addColumn("updatedAt", "timestamp", (col) => col.notNull())
    .execute();

  await db.schema
    .createIndex("account_userId_idx")
    .ifNotExists()
    .on("account")
    .column("userId")
    .execute();

  // Verification table
  await db.schema
    .createTable("verification")
    .ifNotExists()
    .addColumn("id", "text", (col) => col.primaryKey())
    .addColumn("identifier", "text", (col) => col.notNull())
    .addColumn("value", "text", (col) => col.notNull())
    .addColumn("expiresAt", "timestamp", (col) => col.notNull())
    .addColumn("createdAt", "timestamp", (col) => col.defaultTo(sql`now()`).notNull())
    .addColumn("updatedAt", "timestamp", (col) => col.notNull())
    .execute();

  console.log("Migration complete");
}

migrate().catch(console.error);
```

Or use Better Auth CLI and convert:

```bash
# Generate schema
npx @better-auth/cli generate

# Then convert to Kysely migrations manually
```

## Querying Auth Tables

```typescript
import { db } from "@/db";

// Get user by email
const user = await db
  .selectFrom("user")
  .where("email", "=", "test@example.com")
  .selectAll()
  .executeTakeFirst();

// Get user with sessions (manual join)
const userWithSessions = await db
  .selectFrom("user")
  .where("user.id", "=", userId)
  .leftJoin("session", "session.userId", "user.id")
  .selectAll()
  .execute();

// Count sessions
const count = await db
  .selectFrom("session")
  .where("userId", "=", userId)
  .select(db.fn.count("id").as("count"))
  .executeTakeFirst();

// Delete expired sessions
await db
  .deleteFrom("session")
  .where("expiresAt", "<", new Date())
  .execute();
```

## Common Issues & Solutions

### Issue: Type errors with adapter

**Solution:** Ensure your Database interface matches the adapter expectations:

```typescript
import type { Kysely } from "kysely";
import type { Database } from "./types";

// Correct type
const db: Kysely<Database> = new Kysely<Database>({ dialect });
```

### Issue: Missing columns after adding plugins

**Solution:** Add plugin tables to your types and migrations:

```typescript
// For 2FA plugin
export interface TwoFactorTable {
  id: string;
  secret: string;
  backupCodes: string;
  userId: string;
}

export interface Database {
  // ... existing
  twoFactor: TwoFactorTable;
}
```

## Environment Variables

```env
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# MySQL
DATABASE_URL=mysql://user:password@localhost:3306/mydb

# SQLite
DATABASE_URL=./dev.db
```

## Full Example

```typescript
// src/db/index.ts
import { Kysely, PostgresDialect } from "kysely";
import { Pool } from "pg";
import type { Database } from "./types";

export const db = new Kysely<Database>({
  dialect: new PostgresDialect({
    pool: new Pool({
      connectionString: process.env.DATABASE_URL,
    }),
  }),
});

// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { kyselyAdapter } from "better-auth/adapters/kysely";
import { nextCookies } from "better-auth/next-js";
import { db } from "@/db";

export const auth = betterAuth({
  database: kyselyAdapter(db, {
    provider: "pg",
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
  plugins: [nextCookies()],
});
```
