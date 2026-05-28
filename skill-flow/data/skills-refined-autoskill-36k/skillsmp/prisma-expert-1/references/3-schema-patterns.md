# 3. Advanced Schema Patterns

**Impact: HIGH**

A well-designed schema is the foundation of a performant database.

## 3.1 Mapped Enums and Postgres-native types

Use `@map` to decouple your code-level enums from database-level strings.

```prisma
enum Role {
  USER  @map("user")
  ADMIN @map("admin")
}

model User {
  id   String @id
  role Role   @default(USER)
  
  @@map("users") // Maps model name to lowercase plural in DB
}
```

## 3.2 Prisma Pulse (Real-time CDC)

Prisma Pulse allows you to subscribe to database changes in real-time. This replaces complex polling or manual event triggering.

```typescript
const stream = await prisma.user.subscribe();

for await (const event of stream) {
  if (event.action === 'create') {
    console.log('New user created:', event.after.email);
  }
}
```

## 3.3 Relational Integrity

Always use explicit relation names for clarity in complex schemas.

```prisma
model User {
  id            String @id
  writtenPosts  Post[] @relation("WrittenPosts")
  pinnedPost    Post?  @relation("PinnedPost")
}

model Post {
  id          String @id
  authorId    String
  author      User   @relation("WrittenPosts", fields: [authorId], references: [id])
  pinnedBy    User?  @relation("PinnedPost", fields: [pinnedById], references: [id])
  pinnedById  String? @unique
}
```
Using `@unique` on `pinnedById` ensures a 1:1 relation where a user can only have one pinned post.
