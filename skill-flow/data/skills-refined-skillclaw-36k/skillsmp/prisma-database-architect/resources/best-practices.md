# Prisma & PostgreSQL Best Practices

This guide outlines best practices for working with Prisma ORM and PostgreSQL in production applications.

## Schema Design

### DO: Use Descriptive Names

```prisma
// ✅ GOOD: Clear, descriptive names
model ScheduledCrawlRun {
  id           String   @id @default(cuid())
  totalDistricts  Int
  status        CrawlStatus
}

// ❌ BAD: Vague abbreviations
model Scr {
  id   String @id @default(cuid())
  tot  Int
  stat String
}
```

### DO: Use Appropriate Types

```prisma
// ✅ GOOD: Use appropriate types
model Session {
  id        String   @id @default(cuid())
  date      DateTime // Dates/times use DateTime
  price     Decimal  @db.Decimal(10, 2) // Money uses Decimal
  available Boolean  // Boolean flags
  metadata  Json?    // Flexible data uses JSON
}

// ❌ BAD: Incorrect types
model Session {
  id        String @id @default(cuid())
  date      String // Should be DateTime
  price     Float  // Money shouldn't use Float (rounding errors)
  available Int    // Should be Boolean
}
```

### DO: Add Indexes Strategically

```prisma
model Session {
  venueId   String
  date      DateTime
  available Boolean

  // Index for venue-specific queries
  @@index([venueId, date])

  // Index for availability filtering
  @@index([date, available])
}
```

### DO: Use Enums for Fixed Values

```prisma
enum CrawlStatus {
  PENDING
  RUNNING
  COMPLETED
  FAILED
}

model CrawlJob {
  id     String      @id @default(cuid())
  status CrawlStatus @default(PENDING)
}
```

### DO: Use Unique Constraints

```prisma
model Session {
  venueId      String
  facilityCode String
  date         DateTime
  startTime    String

  // Prevent duplicate sessions
  @@unique([venueId, facilityCode, date, startTime])
}
```

### DON'T: Over-Normalize

```prisma
// ✅ GOOD: Reasonable normalization
model Session {
  id         String   @id @default(cuid())
  venueId    String
  date       DateTime
  startTime  String
  available  Boolean
  facility   Facility @relation(fields: [venueId], references: [id])
}

// ❌ BAD: Excessive normalization
model Session {
  id             String @id @default(cuid())
  venueId        String
  dateId         String // Separate date "entity"? Unnecessary
  startTimeId    String // Separate time "entity"? Unnecessary
  availabilityId String // Separate availability? Unnecessary
}
```

## Migrations

### DO: Use Descriptive Migration Names

```bash
# ✅ GOOD: Clear, descriptive names
npx prisma migrate dev --name add_user_profile

# ❌ BAD: Vague names
npx prisma migrate dev --name update
npx prisma migrate dev --name changes
```

### DO: Review Migration SQL

Always review the generated migration SQL:

```bash
npx prisma migrate dev --name my_change --create-only
# Review migrations/<timestamp>_my_change.sql
npx prisma migrate dev
```

### DO: Test Migrations in Development

1. Test migration with development data
2. Verify rollback strategy (`prisma migrate resolve --rolled-back [name]`)
3. Document breaking changes

### DON'T: Modify Migrations Manually

Don't edit migration files after they've been applied:
- They become applied state
- Manual edits cause drift
- Use new migrations for changes

### DON'T: Use Migrate Dev in Production

```bash
# ✅ GOOD: Production
npx prisma migrate deploy

# ❌ BAD: Production
npx prisma migrate dev # Only for development
```

## Queries

### DO: Use Select to Limit Fields

```typescript
// ✅ GOOD: Fetch only needed fields
const sessions = await prisma.session.findMany({
  select: {
    id: true,
    date: true,
    startTime: true,
    available: true
  }
})

// ❌ BAD: Fetches all fields
const sessions = await prisma.session.findMany()
```

### DO: Use Relation Load Strategy

```typescript
// ✅ GOOD: Avoid N+1 queries
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

### DO: Filter Early

```typescript
// ✅ GOOD: Filter at database level
const available = await prisma.session.findMany({
  where: {
    available: true,
    date: { gte: new Date() }
  }
})

// ❌ BAD: Filter in application
const all = await prisma.session.findMany()
const available = all.filter(s => s.available && s.date >= new Date())
```

### DO: Use Transactions for Related Operations

```typescript
// ✅ GOOD: Atomic transaction
await prisma.$transaction(async (tx) => {
  await tx.session.update({
    where: { id: sessionId },
    data: { available: false }
  })

  await tx.booking.create({
    data: { sessionId, userId }
  })
})
```

### DON'T: Fetch All Records Just to Count

```typescript
// ✅ GOOD: Use count()
const total = await prisma.session.count()

// ❌ BAD: Fetch all records
const sessions = await prisma.session.findMany()
const total = sessions.length
```

### DON't: Loop Individual Operations

```typescript
// ✅ GOOD: Batch operation
await prisma.session.createMany({
  data: sessions
})

// ❌ BAD: Individual inserts in loop
for (const session of sessions) {
  await prisma.session.create({ data: session })
}
```

## Client Management

### DO: Use Singleton Pattern

```typescript
// ✅ GOOD: Singleton pattern (src/lib/db.ts)
import { PrismaClient } from '@prisma/client'

const globalForPrisma = global as unknown as { prisma: PrismaClient }

export const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
  })

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

### DON'T: Create Multiple Clients

```typescript
// ❌ BAD: Multiple instances cause connection exhaustion
import { PrismaClient } from '@prisma/client'

export async function handler1() {
  const prisma = new PrismaClient() // New instance each time!
}

export async function handler2() {
  const prisma = new PrismaClient() // Another new instance!
}
```

## Error Handling

### DO: Handle Unique Constraint Violations

```typescript
try {
  await prisma.user.create({
    data: { email: 'existing@email.com' }
  })
} catch (error) {
  if (error instanceof Prisma.Prisma.PrismaClientKnownRequestError) {
    if (error.code === 'P2002') {
      console.log('Unique constraint violation')
      // Handle duplicate entry
    }
  }
}
```

### DO: Handle Record Not Found

```typescript
// ✅ GOOD: Handle missing records
const session = await prisma.session.findUnique({
  where: { id: sessionId }
})

if (!session) {
  throw new Error('Session not found')
}
```

### DO: Use Transactions for Data Consistency

```typescript
// ✅ GOOD: Transaction ensures all-or-nothing
await prisma.$transaction(async (tx) => {
  // If any operation fails, all are rolled back
})
```

## Performance

### DO: Monitor Query Performance

```typescript
// Enable query logging in development
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'],
})
```

### DO: Use Explain Analyze

```sql
EXPLAIN ANALYZE
SELECT * FROM "Session"
WHERE date >= CURRENT_DATE
  AND available = true;
```

### DO: Regularly Check for Unused Indexes

```sql
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
  AND idx_scan = 0;
```

### DON'T: Ignore N+1 Query Issues

Always check for N+1 queries:
- Enable query logging
- Look for repeated similar queries
- Use `relationLoadStrategy: "join"`

## Security

### DO: Use Environment Variables for Secrets

```bash
# .env (never commit this)
DATABASE_URL="postgresql://user:password@host:port/database"
```

### DO: Validate Input Data

```typescript
import { z } from 'zod'

const SessionSchema = z.object({
  venueId: z.string().cuid(),
  date: z.date(),
  startTime: z.string().regex(/^\d{2}:\d{2}$/),
})

const validated = SessionSchema.parse(inputData)
```

### DON'T: Expose Database Errors to Clients

```typescript
// ❌ BAD: Exposes internal details
try {
  await prisma.session.create({ data: sessionData })
} catch (error) {
  res.status(500).json({ error: error.message })
}

// ✅ GOOD: Generic error message
try {
  await prisma.session.create({ data: sessionData })
} catch (error) {
  console.error('Database error:', error)
  res.status(500).json({ error: 'Internal server error' })
}
```

## Testing

### DO: Use Mock Repository for Testing

```typescript
// ✅ GOOD: Test with mock repository
import { MockCrawlRepository } from './repositories/mock-repository'

describe('Crawler Tests', () => {
  const mockRepo = new MockCrawlRepository()

  it('should handle errors gracefully', async () => {
    mockRepo.shouldFail = true
    // Test error handling
  })
})
```

### DO: Test with Real Database in Integration Tests

```typescript
// ✅ GOOD: Integration tests use test database
const testPrisma = new PrismaClient({
  datasources: {
    db: { url: process.env.TEST_DATABASE_URL }
  }
})

beforeEach(async () => {
  await testPrisma.session.deleteMany()
})
```

## Development Workflow

### DO: Use Seed Scripts for Development Data

```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()

async function main() {
  await prisma.session.createMany({
    data: [
      // Test data
    ]
  })
}

main()
```

### DO: Use Prisma Studio for Database Inspection

```bash
npx prisma studio
# Opens at http://localhost:5555
```

### DON'T: Commit Production Data to Repository

- Use seed scripts for test data
- Never commit real user data
- Use environment variables for database URLs

## Raw Query Usage

### DO: Use Raw Queries for Investigation

```bash
# ✅ GOOD: Debug database state
tsx .agent/skills/prisma-db/scripts/raw-query.ts "
  SELECT * FROM \"Session\" WHERE date >= CURRENT_DATE LIMIT 10
"
```

### DO: Use Interactive Mode for Exploration

```bash
# ✅ GOOD: Interactive exploration
tsx .agent/skills/prisma-db/scripts/raw-query.ts --interactive
```

### DON'T: Use Raw Queries in Application Code

```typescript
// ❌ BAD: Raw query in application code
const result = await prisma.$queryRaw`
  SELECT * FROM "Session" WHERE available = true
`

// ✅ GOOD: Use Prisma Client
const result = await prisma.session.findMany({
  where: { available: true }
})
```

## Checklist

Before deploying database-related changes:

- [ ] Schema uses appropriate types
- [ ] Indexes added for frequently queried fields
- [ ] Migration reviewed and tested
- [ ] Queries use `select` to limit fields
- [ ] N+1 queries avoided with `relationLoadStrategy`
- [ ] Client uses singleton pattern
- [ ] Error handling covers Prisma-specific errors
- [ ] Input data validated before database operations
- [ ] Tests cover both unit and integration scenarios
- [ ] Database queries tested with realistic data volumes
- [ ] Security: No credentials in code
- [ ] Performance: Query performance analyzed
- [ ] Documentation: Complex queries documented

## Related Resources

- [Common Inspection Queries](./common-inspection-queries.md)
- [Database Inspection Workflow](./database-inspection-workflow.md)
- [Query Optimization Guide](./query-optimization-guide.md)
- [Code Examples](../examples/)
