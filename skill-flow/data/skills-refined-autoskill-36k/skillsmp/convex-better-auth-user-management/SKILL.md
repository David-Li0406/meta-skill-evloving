---
name: convex-better-auth-user-management
description: |
  Manage Better Auth user data in Convex component tables. Use when: (1) need to
  manually verify user email in development, (2) "Email not verified" error blocking
  login, (3) need to modify Better Auth user/session/account data directly, (4) can't
  write mutations to access component tables, (5) debugging auth issues in Convex +
  Better Auth setup. Covers CLI data access, export/import workflow, and common gotchas.
author: Claude Code
version: 1.0.0
date: 2026-01-21
---

# Convex Better Auth User Management

## Problem
Better Auth stores user data in Convex component tables that can't be accessed through
normal Convex queries/mutations. When you need to manually verify a user's email, modify
auth data, or debug authentication issues, standard approaches don't work.

## Context / Trigger Conditions
- "Email not verified" error when trying to log in
- Need to bypass email verification in local development
- Can't send verification emails (no email service configured)
- Writing a mutation to access Better Auth tables fails with errors like:
  - "Identifier betterAuth:user has invalid character ':'"
  - "getComponentContext is not a function"
- Need to inspect or modify user, session, or account data

## Solution

### 1. View Better Auth Component Tables

List available tables in the component:
```bash
npx convex data --component betterAuth
```
Common tables: `user`, `session`, `account`, `verification`

### 2. View User Data

```bash
npx convex data user --component betterAuth --limit 20
```

As JSON for processing:
```bash
npx convex data user --component betterAuth --format jsonl > users.jsonl
```

### 3. Modify User Data (Export/Import Workflow)

Since you can't write mutations to access component tables directly, use export/import:

```bash
# Export current data
npx convex data user --component betterAuth --format jsonl > /tmp/ba-users.jsonl

# Modify the file (e.g., set emailVerified: true)
sed -i 's/"emailVerified": false/"emailVerified": true/g' /tmp/ba-users.jsonl

# Or for a specific user:
sed -i 's/"email": "user@example.com", "emailVerified": false/"email": "user@example.com", "emailVerified": true/g' /tmp/ba-users.jsonl

# Reimport (replaces all data in the table)
npx convex import --component betterAuth --table user --replace /tmp/ba-users.jsonl --yes
```

### 4. Alternative: Disable Email Verification in Dev

In your Better Auth config (e.g., `convex/betterAuth.ts`):
```typescript
emailAndPassword: {
  enabled: true,
  requireEmailVerification: process.env.NODE_ENV === "production",
  // ...
}
```

Note: This only affects NEW signups. Existing unverified users still need manual verification.

## Verification

After modification:
```bash
npx convex data user --component betterAuth | grep "email@example.com"
```

Verify `emailVerified` shows `true`, then try logging in again.

## Example

**Scenario**: User signed up but email verification failed. Need to verify manually.

```bash
# Check current state
npx convex data user --component betterAuth --format pretty | grep -A2 "me@example.com"
# Shows: emailVerified: false

# Export, modify, reimport
npx convex data user --component betterAuth --format jsonl > /tmp/users.jsonl
sed -i 's/"email": "me@example.com", "emailVerified": false/"email": "me@example.com", "emailVerified": true/g' /tmp/users.jsonl
npx convex import --component betterAuth --table user --replace /tmp/users.jsonl --yes

# Verify
npx convex data user --component betterAuth | grep "me@example.com"
# Shows: emailVerified: true
```

## Notes

- **Import replaces ALL data**: The `--replace` flag deletes all existing rows before import.
  Export the full table first, modify, then reimport.
- **Can't write mutations for components**: Convex component tables use a different namespace.
  Direct DB queries like `ctx.db.query("betterAuth:user")` won't work from your app's mutations.
- **Session/Account tables**: Same pattern works for `session` and `account` tables if you
  need to debug auth sessions.
- **Production warning**: Only use this for development/debugging. In production, use proper
  email verification flows.

## Related

- Cloudflare Turnstile test keys for development: Use site key `1x00000000000000000000AA`
  to bypass CAPTCHA in automated testing/development.
- Admin email auto-grant: Set `ADMIN_EMAIL` env var to automatically grant admin to that
  user on first login sync.
