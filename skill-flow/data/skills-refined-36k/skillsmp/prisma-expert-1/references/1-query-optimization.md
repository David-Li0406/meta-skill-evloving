# 1. Query Optimization & TypedSQL

**Impact: CRITICAL**

In 2026, raw SQL strings are an antipattern. Prisma 7 introduces **TypedSQL** to provide full type safety for hand-written queries.

## 1.1 TypedSQL: Safe Raw Queries

Instead of using `prisma.$queryRaw`, create `.sql` files in your `prisma/sql` directory.

**Example: `prisma/sql/get_top_users.sql`**
```sql
SELECT u.id, u.name, COUNT(p.id) as post_count
FROM "User" u
LEFT JOIN "Post" p ON p."authorId" = u.id
GROUP BY u.id
ORDER BY post_count DESC
LIMIT $1;
```

**Usage in code:**
```typescript
import { getTopUsers } from '@prisma/client/sql';

const topUsers = await prisma.$queryRawTyped(getTopUsers(10));
// topUsers is fully typed with id, name, and post_count!
```

## 1.2 Indexing Strategies and `nativeDistinct`

Proper indexing is the difference between a 10ms and a 10s query.

- **Composite Indexes**: Use them for queries with multiple filters.
- **Native Distinct**: Prisma 7 leverages Postgres' native `DISTINCT ON` for faster unique value extraction.

```prisma
model Post {
  id        String   @id @default(cuid())
  authorId  String
  category  String
  createdAt DateTime @default(now())

  @@index([authorId, category]) // Multi-column index
}
```

## 1.3 Avoiding N+1 with `select` and `include`

Always be intentional about what you fetch.

**❌ Slow (N+1 danger and over-fetching):**
```typescript
const users = await prisma.user.findMany({ include: { posts: true } });
```

**✅ Fast (Selective fetching):**
```typescript
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    _count: {
      select: { posts: true }
    }
  }
});
```

Using `_count` avoids fetching all post objects just to get the total number.
