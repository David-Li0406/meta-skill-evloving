---
name: neon-postgres-serverless
description: Use this skill when deploying serverless applications with Neon PostgreSQL, leveraging features like connection pooling, branching, and autoscaling.
---

# Neon PostgreSQL Serverless Skill

This skill covers the use of Neon PostgreSQL as a serverless database, including connection pooling, branching, autoscaling, and instant provisioning.

## Quick Start

### Create Database

1. Go to [console.neon.tech](https://console.neon.tech)
2. Create a new project
3. Copy the connection string

### Installation

```bash
# npm
npm install @neondatabase/serverless

# pnpm
pnpm add @neondatabase/serverless

# yarn
yarn add @neondatabase/serverless

# bun
bun add @neondatabase/serverless
```

## Connection Strings

```env
# Direct connection (for migrations, scripts)
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# Pooled connection (for application)
DATABASE_URL_POOLED=postgresql://user:password@ep-xxx-pooler.region.aws.neon.tech/dbname?sslmode=require
```

## Core Concepts

### Neon Architecture
- **Projects**: Top-level container for databases and branches
- **Databases**: Postgres databases within a project
- **Branches**: Git-like database copies for development
- **Compute**: Autoscaling Postgres instances
- **Storage**: Separated from compute for instant branching

### Key Features
- **Serverless**: Pay-per-use, scales to zero
- **Branching**: Instant database copies from any point in time
- **Autoscaling**: Compute scales based on load
- **Instant Provisioning**: Databases ready in seconds
- **Connection Pooling**: Built-in PgBouncer support

## Connection Methods

### HTTP (Serverless - Recommended)

Best for: Edge functions, serverless, one-shot queries

```typescript
import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!);

// Simple query
const posts = await sql`SELECT * FROM posts WHERE published = true`;

// With parameters
const post = await sql`SELECT * FROM posts WHERE id = ${postId}`;

// Insert
await sql`INSERT INTO posts (title, content) VALUES (${title}, ${content})`;
```

### WebSocket (Connection Pooling)

Best for: Long-running connections, transactions

```typescript
import { Pool } from "@neondatabase/serverless";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

const client = await pool.connect();
try {
  await client.query("BEGIN");
  await client.query("INSERT INTO posts (title) VALUES ($1)", [title]);
  await client.query("COMMIT");
} catch (e) {
  await client.query("ROLLBACK");
  throw e;
} finally {
  client.release();
}
```

## Branching

Neon branches are copy-on-write clones of your database.

### CLI Commands

```bash
# Install Neon CLI
npm install -g neonctl

# Login
neonctl auth

# List branches
neonctl branches list

# Create branch
neonctl branches create --name feature-x

# Get connection string
neonctl connection-string feature-x

# Delete branch
neonctl branches delete feature-x
```

### Branch Workflow

```bash
# Create branch for feature
neonctl branches create --name feature-auth --parent main

# Get connection string for branch
export DATABASE_URL=$(neonctl connection-string feature-auth)

# Work on feature...

# When done, merge via application migrations
neonctl branches delete feature-auth
```

## Autoscaling

Configure in Neon console:

- **Min compute**: 0.25 CU (can scale to zero)
- **Max compute**: Up to 8 CU
- **Scale to zero delay**: 5 minutes (default)

### Handle Cold Starts

```typescript
import { neon } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!, {
  fetchOptions: {
    // Increase timeout for cold starts
    signal: AbortSignal.timeout(10000),
  },
});
```

## Best Practices

### 1. Use HTTP for Serverless

```typescript
// Good - HTTP for serverless
import { neon } from "@neondatabase/serverless";
const sql = neon(process.env.DATABASE_URL!);

// Avoid - Pool in serverless (connection exhaustion)
import { Pool } from "@neondatabase/serverless";
const pool = new Pool({ connectionString: process.env.DATABASE_URL });
```

### 2. Connection String per Environment

```env
# .env.development
DATABASE_URL=postgresql://...@ep-dev-branch...

# .env.production
DATABASE_URL=postgresql://...@ep-main...
```

### 3. Use Prepared Statements

```typescript
// Good - parameterized query
const result = await sql`SELECT * FROM users WHERE id = ${userId}`;

// Bad - string interpolation (SQL injection risk)
const result = await sql(`SELECT * FROM users WHERE id = '${userId}'`);
```

### 4. Handle Errors

```typescript
import { neon, NeonDbError } from "@neondatabase/serverless";

const sql = neon(process.env.DATABASE_URL!);

try {
  await sql`INSERT INTO users (email) VALUES (${email})`;
} catch (error) {
  if (error instanceof NeonDbError) {
    if (error.code === "23505") {
      // Unique violation
      throw new Error("Email already exists");
    }
  }
  throw error;
}
```

## Environment Variables

### Required Variables
```bash
# Neon connection strings
DATABASE_URL="postgresql://user:pass@ep-xxx-pooler.region.aws.neon.tech/db?sslmode=require"
DIRECT_URL="postgresql://user:pass@ep-xxx.region.aws.neon.tech/db?sslmode=require"

# API access (for CLI/automation)
NEON_API_KEY="your_api_key"

# Project configuration
NEON_PROJECT_ID="your_project_id"
```

## Common Patterns

### API Route with Caching
```typescript
import { neon } from "@neondatabase/serverless";

export const runtime = "edge";

export async function GET() {
  const sql = neon(process.env.DATABASE_URL!);

  const users = await sql`SELECT * FROM users ORDER BY created_at DESC LIMIT 10`;

  return Response.json(users, {
    headers: {
      "Cache-Control": "s-maxage=60, stale-while-revalidate",
    },
  });
}
```

### Connection Testing
```typescript
async function testConnection() {
  const sql = neon(process.env.DATABASE_URL!);

  try {
    const result = await sql`SELECT version()`;
    console.log("✅ Connected to Neon:", result[0].version);
    return true;
  } catch (error) {
    console.error("❌ Connection failed:", error);
    return false;
  }
}
```

### Troubleshooting

#### Connection Issues
```typescript
// Check SSL requirement
const url = new URL(process.env.DATABASE_URL!);
if (!url.searchParams.has("sslmode")) {
  url.searchParams.set("sslmode", "require");
}

// Verify endpoint type
// -pooler: For application queries
// direct: For migrations and admin tasks

// Test connectivity
import { neon } from "@neondatabase/serverless";
const sql = neon(process.env.DATABASE_URL!);
await sql`SELECT 1`; // Should succeed
```

This skill provides comprehensive coverage of Neon PostgreSQL serverless database, including connection pooling, branching, ORM integrations, serverless deployment patterns, and production best practices.