---
name: better-auth-best-practices
description: Use this skill when you need to integrate Better Auth, a comprehensive TypeScript authentication framework, into your application.
---

# Better Auth Integration Guide

**Always consult [better-auth.com/docs](https://better-auth.com/docs) for code examples and latest API.**

Better Auth is a TypeScript-first, framework-agnostic auth framework supporting email/password, OAuth, magic links, passkeys, and more via plugins.

## Quick Reference

### Environment Variables
- `BETTER_AUTH_SECRET` - Encryption secret (min 32 chars). Generate: `openssl rand -base64 32`
- `BETTER_AUTH_URL` - Base URL (e.g., `https://example.com`)

Only define `baseURL`/`secret` in config if env vars are NOT set.

### File Location
CLI looks for `auth.ts` in: `./`, `./lib`, `./utils`, or under `./src`. Use `--config` for custom path.

### CLI Commands
- `npx @better-auth/cli@latest migrate` - Apply schema (built-in adapter)
- `npx @better-auth/cli@latest generate` - Generate schema for Prisma/Drizzle
- `npx @better-auth/cli mcp --cursor` - Add MCP to AI tools

**Re-run after adding/changing plugins.**

## Core Config Options

| Option             | Notes                                          |
| ------------------ | ---------------------------------------------- |
| `appName`          | Optional display name                          |
| `baseURL`          | Only if `BETTER_AUTH_URL` not set             |
| `basePath`         | Default `/api/auth`. Set `/` for root.        |
| `secret`           | Only if `BETTER_AUTH_SECRET` not set          |
| `database`         | Required for most features. See adapters docs.|
| `secondaryStorage` | Redis/KV for sessions & rate limits            |
| `emailAndPassword` | `{ enabled: true }` to activate                |
| `socialProviders`  | `{ google: { clientId, clientSecret }, ... }`|
| `plugins`          | Array of plugins                               |
| `trustedOrigins`   | CSRF whitelist                                 |

## Database

**Direct connections:** Pass `pg.Pool`, `mysql2` pool, `better-sqlite3`, or `bun:sqlite` instance.

**ORM adapters:** Import from `better-auth/adapters/drizzle`, `better-auth/adapters/prisma`, `better-auth/adapters/mongodb`.

**Critical:** Better Auth uses adapter model names, NOT underlying table names. If Prisma model is `User` mapping to table `users`, use `modelName: "user"` (Prisma reference), not `"users"`.

## Session Management

**Storage priority:**
1. If `secondaryStorage` defined → sessions go there (not DB)
2. Set `session.storeSessionInDatabase: true` to also persist to DB
3. No database + `cookieCache` → fully stateless mode

**Cookie cache strategies:**
- `compact` (default) - Base64url + HMAC. Smallest.
- `jwt` - Standard JWT. Readable but signed.
- `jwe` - JSON Web Encryption.