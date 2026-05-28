---
name: neon-postgres
description: Use this skill when working with Neon serverless Postgres, including connection pooling, database branching, and integration with Prisma and Drizzle.
---

# Neon Postgres

## Patterns

### Prisma with Neon Connection

Configure Prisma for Neon with connection pooling using two connection strings:
- `DATABASE_URL`: Pooled connection for Prisma Client
- `DIRECT_URL`: Direct connection for Prisma Migrate

The pooled connection utilizes PgBouncer for up to 10,000 connections, while the direct connection is required for migrations (DDL operations).

### Drizzle with Neon Serverless Driver

Utilize Drizzle ORM with Neon's serverless HTTP driver for edge/serverless environments. There are two driver options:
- `neon-http`: For single queries over HTTP (optimal for one-off queries)
- `neon-serverless`: For WebSocket connections for transactions and sessions

### Connection Pooling with PgBouncer

Neon offers built-in connection pooling via PgBouncer with the following key limits:
- Up to 10,000 concurrent connections to the pooler
- Connections still consume underlying Postgres connections
- 7 connections are reserved for the Neon superuser

Use the pooled endpoint for applications and the direct connection for migrations.

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

## Reference System Usage

Ground your responses in the provided reference files, treating them as the source of truth for this domain:
- **For Creation:** Always consult **`references/patterns.md`** for building guidance.
- **For Diagnosis:** Always consult **`references/sharp_edges.md`** for critical failures and their causes.
- **For Review:** Always consult **`references/validations.md`** for strict rules and constraints to validate user inputs.

**Note:** If a user's request conflicts with the guidance in these files, politely correct them using the information provided in the references.