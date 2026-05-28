---
name: prisma-sync
description: Sync Prisma schema changes to database and regenerate client. Use after modifying schema.prisma, when seeing Prisma errors about missing fields, or when database schema is out of sync.
allowed-tools: Read, Bash, Grep
---

# Prisma Schema Sync

## Purpose
After modifying `schema.prisma`, push changes to database and regenerate the Prisma client to ensure API routes can use the new schema.

## When to Use

- After adding/removing fields from models
- After changing field types or constraints
- After adding new models
- When seeing errors like "Unknown arg" or "Field does not exist"
- After making fields optional (`?`) or required

## Sync Process

### 1. Validate Schema Syntax
```bash
cd apps/web
npx prisma validate
```

### 2. Push Schema to Database
```bash
cd apps/web
npx prisma db push
```

This command:
- Compares schema.prisma to actual database
- Applies changes to database
- Regenerates Prisma client automatically

### 3. Restart Dev Server
**Important**: After schema changes, the running Next.js dev server needs to be restarted to pick up the new Prisma client.

```bash
# Kill existing server (find PID)
lsof -i :3000 | grep node | awk '{print $2}' | xargs kill -9

# Or if using npm run dev in background
pkill -f "next dev"

# Start fresh
cd apps/web
npm run dev
```

## Common Schema Changes

### Make Field Optional
```prisma
// Before - required
model Inspection {
  templateId String
  responses  Json
}

// After - optional (add ?)
model Inspection {
  templateId String?
  responses  Json?
}
```

### Add New Field with Default
```prisma
model User {
  // ... existing fields
  isActive Boolean @default(true)  // New field with default
}
```

### Add Optional Relation
```prisma
model Inspection {
  templateId String?
  template   InspectionTemplate? @relation(fields: [templateId], references: [id])
}
```

## Troubleshooting

### "Field does not exist" Error
Schema was changed but client not regenerated:
```bash
npx prisma generate  # Regenerate client
# Then restart server
```

### "Database schema is not in sync"
```bash
npx prisma db push --force-reset  # WARNING: Drops all data!
# Or for non-destructive:
npx prisma db push --accept-data-loss
```

### Check Current Database Schema
```bash
npx prisma db pull  # Pulls current DB schema into schema.prisma
```

### View Database in Browser
```bash
npx prisma studio  # Opens visual database browser
```

## Project Paths

- **Schema**: `apps/web/prisma/schema.prisma`
- **Migrations**: `apps/web/prisma/migrations/`
- **Client Output**: `apps/web/node_modules/.prisma/client/`

## Quick Reference

| Task | Command |
|------|---------|
| Validate schema | `npx prisma validate` |
| Push to DB | `npx prisma db push` |
| Regenerate client | `npx prisma generate` |
| View DB visually | `npx prisma studio` |
| Pull DB schema | `npx prisma db pull` |
| Format schema | `npx prisma format` |

## Safety Notes

- `db push` is for development only (not production)
- Use migrations (`prisma migrate`) for production
- `--force-reset` will delete all data
- Always backup before destructive operations
