---
name: Database & Prisma
description: PostgreSQL 16, Prisma ORM, migrations, seeding, and advanced query patterns.
---

# Database & Prisma

## Context

- **Database**: PostgreSQL 16 (Alpine)
- **ORM**: Prisma 5.x
- **Schema**: `packages/database/prisma/schema.prisma`
- **Client**: Generated to `@packages/database`

---

## Core Principles

1. **Single Source of Truth**: The `schema.prisma` file defines all models.
2. **Type Safety**: Use generated Prisma types everywhere. Never manually type DB responses.
3. **Migrations First**: Always use migrations, never direct SQL in production.

---

## Schema Location

```
packages/database/
├── prisma/
│   ├── schema.prisma    # Main schema
│   ├── migrations/      # Version-controlled migrations
│   └── seed.ts          # Development seeding
├── src/
│   └── index.ts         # Re-exports prisma client
└── package.json
```

---

## Commands

```bash
# Generate Prisma client (after schema change)
pnpm db:generate

# Create and apply migration
pnpm db:migrate --name describe_change

# Push changes (prototyping only, no migration)
pnpm db:push

# Open Prisma Studio
pnpm db:studio

# Seed database
pnpm db:seed
```

---

## Schema Best Practices

### Enums for Finite States

```prisma
enum MissionStatus {
  DRAFT
  PUBLISHED
  ASSIGNED
  COMPLETED
  CANCELLED
}
```

### Indexes for Performance

```prisma
model Mission {
  id        String   @id @default(cuid())
  userId    String
  status    MissionStatus
  createdAt DateTime @default(now())

  @@index([userId])
  @@index([status, createdAt])
}
```

### Explicit Relation Names

```prisma
model User {
  sentMessages     Message[] @relation("SentMessages")
  receivedMessages Message[] @relation("ReceivedMessages")
}
```

---

## Transactions

**ALWAYS** use transactions for multi-step operations:

```typescript
await prisma.$transaction(async (tx) => {
  const mission = await tx.mission.create({ data: missionData });
  await tx.notification.create({ 
    data: { userId: mission.userId, type: 'MISSION_CREATED' } 
  });
  return mission;
});
```

---

## Production Migrations

### Via Coolify Deployment

1. Migrations run automatically via `prisma migrate deploy` in Dockerfile.
2. Ensure `DATABASE_URL` is set in Coolify environment.

### Manual Migration

```bash
# SSH into server or use Coolify terminal
npx prisma migrate deploy
```

---

## Common Patterns

### Soft Deletes

```prisma
model User {
  deletedAt DateTime?
}
```

```typescript
// Query active users only
const users = await prisma.user.findMany({
  where: { deletedAt: null }
});
```

### Pagination

```typescript
const { skip, take } = { skip: (page - 1) * limit, take: limit };
const [items, total] = await prisma.$transaction([
  prisma.mission.findMany({ skip, take, orderBy: { createdAt: 'desc' } }),
  prisma.mission.count()
]);
```
