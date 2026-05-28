---
name: neon-postgres
description: Use this skill when working with Neon serverless Postgres, including connection pooling, database branching, and integration with Prisma or Drizzle.
---

# Neon Postgres

## Patterns

### Prisma with Neon Connection

Configure Prisma for Neon with connection pooling using two connection strings:
- **DATABASE_URL**: Pooled connection for Prisma Client.
- **DIRECT_URL**: Direct connection for Prisma Migrate.

The pooled connection utilizes PgBouncer, allowing for up to 10,000 concurrent connections. The direct connection is required for migrations (DDL operations).

### Drizzle with Neon Serverless Driver

Integrate Drizzle ORM with Neon's serverless HTTP driver for edge/serverless environments. There are two driver options:
- **neon-http**: Best for single queries over HTTP (optimal for one-off queries).
- **neon-serverless**: Utilizes WebSocket for transactions and sessions.

### Connection Pooling with PgBouncer

Neon provides built-in connection pooling via PgBouncer with the following key limits:
- Up to 10,000 concurrent connections to the pooler.
- Connections still consume underlying Postgres connections.
- 7 connections are reserved for the Neon superuser.

Use the pooled endpoint for application connections and the direct endpoint for migrations.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | high | See docs |
| Issue | medium | See docs |
| Issue | medium | See docs |
| Issue | low | See docs |
| Issue | medium | See docs |
| Issue | high | See docs |