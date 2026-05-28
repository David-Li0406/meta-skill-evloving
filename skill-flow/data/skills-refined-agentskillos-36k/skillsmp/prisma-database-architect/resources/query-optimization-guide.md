# Query Optimization Guide

This guide provides comprehensive strategies for optimizing database queries with Prisma and PostgreSQL.

## Core Principles

1. **Fetch Only What You Need**: Use `select` to limit fields
2. **Avoid N+1 Queries**: Use proper relation loading strategies
3. **Index Strategically**: Add indexes for frequently queried fields
4. **Use Aggregations**: Prefer `count()`, `sum()` over fetching all records
5. **Filter Early**: Apply `where` clauses before fetching data

## Optimization Techniques

### 1. Select Specific Fields

**Problem**: Fetching unnecessary fields wastes memory and bandwidth

**Solution**: Use `select` to fetch only required fields

```typescript
// ❌ BAD: Fetches all fields
const sessions = await prisma.session.findMany({
  where: { date: { gte: new Date() } }
})

// ✅ GOOD: Fetches only needed fields
const sessions = await prisma.session.findMany({
  where: { date: { gte: new Date() } },
  select: {
    id: true,
    date: true,
    startTime: true,
    available: true
  }
})
```

**Impact**: Reduces data transfer by 50-80% depending on schema size

### 2. Avoid N+1 Queries

**Problem**: Querying relations separately causes N+1 query problem

**Solution**: Use `relationLoadStrategy: "join"` (Prisma v5.10+)

```typescript
// ❌ BAD: N+1 queries (separate query for each relation)
const posts = await prisma.post.findMany({
  include: { comments: true }
})

// ✅ GOOD: Single query with JOIN
const posts = await prisma.post.findMany({
  relationLoadStrategy: 'join',
  include: {
    comments: {
      select: { id: true, content: true },
      take: 5
    }
  }
})
```

**Impact**: Reduces queries from N+1 to 1-2 queries, 10-100x faster

### 3. Use Count Efficiently

**Problem**: Fetching all records just to count them

**Solution**: Use dedicated `count()` method

```typescript
// ❌ BAD: Fetches all records
const sessions = await prisma.session.findMany()
const total = sessions.length

// ✅ GOOD: Count at database level
const total = await prisma.session.count()

// ✅ EVEN BETTER: Count with filtering
const available = await prisma.session.count({
  where: {
    available: true,
    date: { gte: new Date() }
  }
})
```

**Impact**: 100-1000x faster for large tables

### 4. Index Frequently Queried Fields

**Problem**: Scanning entire table to find records

**Solution**: Add indexes for fields in `where` clauses

**Schema** (`schema.prisma`):

```prisma
model Session {
  id        String   @id @default(cuid())
  venueId   String
  date      DateTime
  available Boolean
  startTime String

  // Indexes for common query patterns
  @@index([venueId, date])      // Venue-specific queries
  @@index([date, available])     // Availability filtering
  @@index([available])           // Global availability queries
}
```

**Impact**: 10-1000x faster depending on table size

### 5. Use Pagination

**Problem**: Fetching thousands of records at once

**Solution**: Use `take` and `skip` for pagination

```typescript
const sessions = await prisma.session.findMany({
  where: { date: { gte: new Date() } },
  select: {
    id: true,
    date: true,
    startTime: true,
    available: true
  },
  orderBy: { date: 'asc' },
  take: 20,   // Limit to 20 records
  skip: 0     // Offset for next page
})
```

**Impact**: Reduces memory usage and improves response time

### 6. Batch Operations

**Problem**: Individual inserts/updates in a loop

**Solution**: Use `createMany` or `updateMany`

```typescript
// ❌ BAD: Individual operations
for (const session of sessions) {
  await prisma.session.create({ data: session })
}

// ✅ GOOD: Batch operation
await prisma.session.createMany({
  data: sessions,
  skipDuplicates: true
})
```

**Impact**: 10-100x faster for bulk operations

### 7. Use Transactions for Atomic Operations

**Problem**: Multiple round trips for related operations

**Solution**: Use `$transaction` for atomic operations

```typescript
const result = await prisma.$transaction(async (tx) => {
  // All operations in single transaction
  const user = await tx.user.update({
    where: { id: userId },
    data: { credits: { decrement: amount } }
  })

  const payment = await tx.payment.create({
    data: { userId, amount }
  })

  return { user, payment }
})
```

**Impact**: Reduces round trips and ensures data consistency

### 8. Optimize Relation Loading

**Problem**: Fetching entire related objects

**Solution**: Use nested `select` for relations

```typescript
// ❌ BAD: Fetches entire facility object
const sessions = await prisma.session.findMany({
  include: { facility: true }
})

// ✅ GOOD: Fetches only needed fields
const sessions = await prisma.session.findMany({
  select: {
    id: true,
    date: true,
    startTime: true,
    facility: {
      select: {
        name: true,
        district: {
          select: {
            name: true
          }
        }
      }
    }
  }
})
```

**Impact**: Reduces data transfer significantly

## Index Optimization

### Composite Indexes

Create composite indexes for multi-field queries:

```prisma
model Session {
  venueId   String
  date      DateTime
  available Boolean

  // Optimize queries filtering by venueId AND date
  @@index([venueId, date])

  // Optimize queries filtering by date AND available
  @@index([date, available])
}
```

**Rule**: Order fields by selectivity (most selective first)

### Index Types

```prisma
model User {
  email    String @unique  // B-tree index (default)
  name     String

  // Full-text search (PostgreSQL)
  @@index([name], type: FullText)
}
```

### Index Maintenance

Regularly check for unused indexes:

```sql
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND idx_scan = 0
ORDER BY tablename, indexname;
```

Remove unused indexes to improve write performance.

## Query Patterns

### Pagination with Cursor

For large datasets, use cursor-based pagination:

```typescript
const firstPage = await prisma.session.findMany({
  take: 20,
  orderBy: { createdAt: 'asc' }
})

const lastItem = firstPage[firstPage.length - 1]

const nextPage = await prisma.session.findMany({
  take: 20,
  skip: 1, // Skip the cursor
  cursor: { id: lastItem.id },
  orderBy: { createdAt: 'asc' }
})
```

### Aggregation Queries

Use aggregation functions for statistics:

```typescript
const stats = await prisma.session.aggregate({
  where: { date: { gte: new Date() } },
  _count: { id: true },
  _avg: { price: true },
  _sum: { price: true },
  _min: { date: true },
  _max: { date: true }
})
```

### Grouping Results

Use `groupBy` for aggregated views:

```typescript
const sessionsByDate = await prisma.session.groupBy({
  by: ['date'],
  where: { date: { gte: new Date() } },
  _count: { id: true },
  _count: {
    available: true
  }
})
```

## Performance Monitoring

### Enable Query Logging

**Development** (`.env`):

```env
DATABASE_URL="postgresql://..."
LOG_LEVEL=debug
```

**Prisma Client**:

```typescript
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'],
})
```

### Analyze Query Performance

Use `EXPLAIN ANALYZE` for slow queries:

```sql
EXPLAIN ANALYZE
SELECT * FROM "Session"
WHERE date >= CURRENT_DATE
  AND available = true;
```

Look for:

- Sequential scans on large tables (need indexes)
- High cost numbers (inefficient queries)
- Filter conditions (missing indexes)

### Monitor Index Usage

```sql
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan as scans,
  idx_tup_read as tuples_read,
  idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY scans DESC;
```

## Common Performance Issues

### Issue 1: Missing Indexes

**Symptoms**:

- Slow queries on large tables
- Sequential scans in EXPLAIN output

**Solution**:

- Add indexes for frequently filtered fields
- Use composite indexes for multi-field queries

### Issue 2: N+1 Queries

**Symptoms**:

- Many database round trips
- Slow response times with relations

**Solution**:

- Use `relationLoadStrategy: "join"`
- Use nested `select` for relations
- Batch queries when possible

### Issue 3: Over-Fetching

**Symptoms**:

- Large response payloads
- Slow network transfer

**Solution**:

- Always use `select` to limit fields
- Avoid `include` without field selection
- Use pagination for large result sets

### Issue 4: Inefficient Aggregations

**Symptoms**:

- Fetching all records to calculate stats
- High memory usage

**Solution**:

- Use dedicated aggregation methods (`count()`, `aggregate()`, `groupBy()`)
- Filter before aggregating

## Optimization Checklist

Before deploying queries to production, verify:

- [ ] Used `select` to limit fetched fields
- [ ] Added indexes for fields in `where` clauses
- [ ] Used `relationLoadStrategy: "join"` for relations
- [ ] Implemented pagination for large result sets
- [ ] Used `count()` or `aggregate()` instead of fetching all records
- [ ] Batched operations where possible
- [ ] Analyzed query performance with `EXPLAIN ANALYZE`
- [ ] Tested with realistic data volumes

## Performance Benchmarks

Typical improvements with optimization:

| Technique | Before | After | Improvement |
|-----------|--------|-------|-------------|
| Select fields | 100ms | 20ms | 5x faster |
| Avoid N+1 | 1000ms | 50ms | 20x faster |
| Add index | 500ms | 5ms | 100x faster |
| Use count() | 200ms | 2ms | 100x faster |
| Batch insert | 5000ms | 200ms | 25x faster |

## Related Resources

- [Common Inspection Queries](./common-inspection-queries.md)
- [Database Inspection Workflow](./database-inspection-workflow.md)
- [Best Practices](./best-practices.md)
- [Code Examples](../examples/optimized-query.ts)
