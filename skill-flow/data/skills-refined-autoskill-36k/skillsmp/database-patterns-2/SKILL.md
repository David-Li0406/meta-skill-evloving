---
name: database-patterns
description: Provides Prisma-specific patterns for soft delete, transactions, optimistic locking, bulk operations, and performance optimization. This skill should be used when implementing data persistence, handling concurrent updates, managing complex multi-table operations, or optimizing query performance.
---

# Database Patterns Skill (Prisma/PostgreSQL)

**The Single Source of Truth for Database Interactions in Eridu Services.**

This skill provides mandatory patterns for using Prisma ORM effectively, ensuring data integrity, performance, and maintainability.

## 1. Soft Delete Pattern

**Rule**: NEVER permanently delete logic data. Use `deletedAt` timestamps.

### Schema Support
```prisma
model User {
  id        BigInt    @id @default(autoincrement())
  uid       String    @unique
  deletedAt DateTime? @map("deleted_at")
  
  @@index([deletedAt]) // Mandatory index for filtering
}
```

### Querying (The most common pitfall)
You **MUST** filter out deleted records in **every** query unless specifically introspecting history.

```typescript
// ✅ CORRECT
const activeUsers = await prisma.user.findMany({
  where: { deletedAt: null }
});

// ❌ WRONG (Returns deleted "zombie" records)
const users = await prisma.user.findMany();
```

### Implementing Soft Delete
```typescript
// ✅ CORRECT: Update timestamp
await prisma.user.update({
  where: { uid: 'u_1' },
  data: { deletedAt: new Date() }
});
```

---

## 2. Bulk Operations Pattern

**Rule**: NEVER loop over database calls. Use specialized bulk methods.

### Batch Insert
```typescript
// ✅ CORRECT: Single Query
await prisma.show.createMany({
  data: shows.map(s => ({ ...s, uid: generateUid() })),
  skipDuplicates: true // Optional resilience
});
```

### Batch Update
```typescript
// ✅ CORRECT: Update by criteria
await prisma.show.updateMany({
  where: { clientId: 1, deletedAt: null },
  data: { status: 'PUBLISHED' }
});
```

---

## 3. Transaction Pattern

**Rule**: Use `prisma.$transaction` for **Atomic Multi-Entity Operations**.

**Scenario**: Creating a Show requires creating ShowMCs and ShowPlatforms simultaneously.

```typescript
return prisma.$transaction(async (tx) => {
  // 1. Create Parent
  const show = await tx.show.create({ ... });

  // 2. Create Children (using tx, NOT prisma)
  await tx.showMC.createMany({
    data: mcs.map(mc => ({ showId: show.id, ... }))
  });

  return show;
});
```

**Critical Rules**:
1.  Always use `tx` inside the callback. Using `prisma` bypasses the transaction lock.
2.  Keep transactions **short**. Do not await external API calls inside a transaction.

---

## 4. Query Optimization Patterns

### N+1 Prevention (Eager Loading)
**Rule**: Fetch related data in a single query using `include`.

```typescript
// ✅ CORRECT: 1 Query
const shows = await prisma.show.findMany({
  include: { client: true }
});

// ❌ WRONG: 1 + N Queries
const shows = await prisma.show.findMany();
for (const show of shows) {
  await prisma.client.findUnique({ where: { id: show.clientId } });
}
```

### Parallel Execution
**Rule**: Independent queries should run concurrently.

```typescript
// ✅ CORRECT: Runs in parallel
const [users, count] = await Promise.all([
  prisma.user.findMany({ where }),
  prisma.user.count({ where })
]);

// ❌ WRONG: Runs sequentially (slower)
const users = await prisma.user.findMany({ where });
const count = await prisma.user.count({ where });
```

---

## 5. Nested Connect Pattern

**Rule**: Use `connect: { uid }` to link entities. avoids an extra read query to find the `id`.

```typescript
// ✅ CORRECT
await prisma.show.create({
  data: {
    client: { connect: { uid: 'client_123' } } // Prisma handles the lookup
  }
});

// ❌ WRONG
const client = await prisma.client.findUnique({ where: { uid: 'client_123' }});
await prisma.show.create({
  data: { clientId: client.id }
});
```

---

## 6. Optimistic Locking (Version Check)

**Rule**: Use a `version` integer to prevent overwriting concurrent updates.

```typescript
// 1. Check version in WHERE clause
const updated = await prisma.schedule.update({
  where: { uid: 's_1', version: 5 }, // Must match current version
  data: {
    ...data,
    version: { increment: 1 }
  }
});
// 2. Handle known error (P2025: Record not found) as a Version Conflict.
```

## Related Skills

- **[Repository Pattern](repository-pattern-nestjs/SKILL.md)**: How to wrap these patterns in a reusable class.
- **[Service Pattern](service-pattern-nestjs/SKILL.md)**: Where to use Transactions and business logic.
