---
name: backend-patterns
description: API design, database operations, error handling, and backend architecture patterns. Use when creating APIs, database schemas, or server-side logic.
---

# Backend Patterns

Comprehensive patterns for API design, database operations, error handling, and backend architecture.

## When to Use

- Creating API endpoints
- Designing database schemas
- Implementing business logic
- Error handling and logging
- Background jobs and queues
- Caching strategies

## API Design Patterns

### RESTful API Structure

```typescript
// app/api/users/route.ts
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const page = parseInt(searchParams.get('page') || '1')
  const limit = parseInt(searchParams.get('limit') || '10')

  const users = await db.users.findMany({
    skip: (page - 1) * limit,
    take: limit
  })

  return NextResponse.json({
    success: true,
    data: users,
    pagination: {
      page,
      limit,
      total: await db.users.count()
    }
  })
}

export async function POST(request: Request) {
  const body = await request.json()

  // Validate input
  const validated = CreateUserSchema.parse(body)

  const user = await db.users.create({ data: validated })

  return NextResponse.json(
    { success: true, data: user },
    { status: 201 }
  )
}

// app/api/users/[id]/route.ts
export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const user = await db.users.findUnique({
    where: { id: params.id }
  })

  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    )
  }

  return NextResponse.json({ success: true, data: user })
}

export async function PATCH(
  request: Request,
  { params }: { params: { id: string } }
) {
  const body = await request.json()
  const validated = UpdateUserSchema.parse(body)

  const user = await db.users.update({
    where: { id: params.id },
    data: validated
  })

  return NextResponse.json({ success: true, data: user })
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  await db.users.delete({ where: { id: params.id } })

  return NextResponse.json({ success: true }, { status: 204 })
}
```

### Consistent API Response Format

```typescript
type ApiResponse<T> = {
  success: true
  data: T
  meta?: {
    pagination?: {
      page: number
      limit: number
      total: number
    }
  }
} | {
  success: false
  error: string
  details?: any
}

// Success response helper
function successResponse<T>(data: T, meta?: any): Response {
  return NextResponse.json({ success: true, data, meta })
}

// Error response helper
function errorResponse(error: string, status: number, details?: any): Response {
  return NextResponse.json(
    { success: false, error, details },
    { status }
  )
}

// Usage
export async function GET(request: Request) {
  try {
    const users = await db.users.findMany()
    return successResponse(users)
  } catch (error) {
    return errorResponse('Failed to fetch users', 500)
  }
}
```

### API Versioning

```typescript
// app/api/v1/users/route.ts
export async function GET(request: Request) {
  // Version 1 implementation
  return NextResponse.json({ version: 1, users: [] })
}

// app/api/v2/users/route.ts
export async function GET(request: Request) {
  // Version 2 implementation with breaking changes
  return NextResponse.json({ version: 2, data: { users: [] } })
}
```

### Request Validation

```typescript
import { z } from 'zod'

const CreateMarketSchema = z.object({
  name: z.string().min(3).max(100),
  description: z.string().min(10).max(1000),
  category: z.enum(['politics', 'sports', 'entertainment', 'crypto']),
  endDate: z.string().datetime(),
  options: z.array(z.object({
    name: z.string().min(1).max(50),
    probability: z.number().min(0).max(1).optional()
  })).min(2).max(10)
})

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const validated = CreateMarketSchema.parse(body)

    // Safe to use validated data
    const market = await db.markets.create({ data: validated })

    return NextResponse.json({ success: true, data: market })

  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        {
          success: false,
          error: 'Validation failed',
          details: error.errors
        },
        { status: 400 }
      )
    }

    return NextResponse.json(
      { success: false, error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

## Database Patterns

### Database Schema Design

```typescript
// Prisma schema example
model User {
  id            String   @id @default(cuid())
  email         String   @unique
  name          String
  passwordHash  String
  role          Role     @default(USER)
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt

  posts         Post[]
  comments      Comment[]

  @@index([email])
  @@index([createdAt])
}

model Post {
  id          String   @id @default(cuid())
  title       String
  content     String   @db.Text
  published   Boolean  @default(false)
  authorId    String
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  author      User     @relation(fields: [authorId], references: [id], onDelete: Cascade)
  comments    Comment[]
  tags        Tag[]

  @@index([authorId])
  @@index([published])
  @@index([createdAt])
  @@fulltext([title, content]) // For search
}

model Comment {
  id        String   @id @default(cuid())
  content   String   @db.Text
  postId    String
  authorId  String
  createdAt DateTime @default(now())

  post      Post     @relation(fields: [postId], references: [id], onDelete: Cascade)
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)

  @@index([postId])
  @@index([authorId])
}

enum Role {
  USER
  MODERATOR
  ADMIN
}
```

### Transaction Patterns

```typescript
// ❌ WRONG: No transaction (race condition)
export async function transferFunds(fromId: string, toId: string, amount: number) {
  const sender = await db.accounts.findUnique({ where: { id: fromId } })

  if (sender.balance < amount) {
    throw new Error('Insufficient funds')
  }

  // Race condition: balance could change between these operations
  await db.accounts.update({
    where: { id: fromId },
    data: { balance: sender.balance - amount }
  })

  await db.accounts.update({
    where: { id: toId },
    data: { balance: { increment: amount } }
  })
}

// ✅ CORRECT: Use transactions
export async function transferFunds(fromId: string, toId: string, amount: number) {
  await db.$transaction(async (tx) => {
    // Lock sender account for update
    const sender = await tx.accounts.findUnique({
      where: { id: fromId }
    })

    if (!sender || sender.balance < amount) {
      throw new Error('Insufficient funds')
    }

    // Atomic updates
    await tx.accounts.update({
      where: { id: fromId },
      data: { balance: { decrement: amount } }
    })

    await tx.accounts.update({
      where: { id: toId },
      data: { balance: { increment: amount } }
    })

    // Create transaction record
    await tx.transactions.create({
      data: {
        fromId,
        toId,
        amount,
        status: 'completed'
      }
    })
  })
}
```

### Query Optimization

```typescript
// ❌ WRONG: N+1 query problem
const users = await db.users.findMany()
for (const user of users) {
  user.posts = await db.posts.findMany({
    where: { authorId: user.id }
  })
}

// ✅ CORRECT: Use includes/eager loading
const users = await db.users.findMany({
  include: {
    posts: true
  }
})

// ✅ CORRECT: Select only needed fields
const users = await db.users.findMany({
  select: {
    id: true,
    name: true,
    email: true,
    posts: {
      select: {
        id: true,
        title: true,
        createdAt: true
      }
    }
  }
})

// ✅ CORRECT: Pagination for large datasets
const posts = await db.posts.findMany({
  take: 20,
  skip: (page - 1) * 20,
  orderBy: { createdAt: 'desc' }
})
```

### Supabase Patterns

```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY! // Use service key for server-side
)

// Basic CRUD operations
export async function getMarkets() {
  const { data, error } = await supabase
    .from('markets')
    .select('*')
    .order('created_at', { ascending: false })

  if (error) throw error
  return data
}

export async function getMarketById(id: string) {
  const { data, error } = await supabase
    .from('markets')
    .select(`
      *,
      creator:users(id, name, avatar),
      bets(id, amount, outcome)
    `)
    .eq('id', id)
    .single()

  if (error) throw error
  return data
}

export async function createMarket(market: MarketInput) {
  const { data, error } = await supabase
    .from('markets')
    .insert(market)
    .select()
    .single()

  if (error) throw error
  return data
}

// Full-text search
export async function searchMarkets(query: string) {
  const { data, error } = await supabase
    .from('markets')
    .select('*')
    .textSearch('fts', query, {
      type: 'websearch',
      config: 'english'
    })

  if (error) throw error
  return data
}
```

## Error Handling Patterns

### Structured Error Classes

```typescript
// Define error hierarchy
export class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public code?: string,
    public details?: any
  ) {
    super(message)
    this.name = this.constructor.name
  }
}

export class ValidationError extends AppError {
  constructor(message: string, details?: any) {
    super(400, message, 'VALIDATION_ERROR', details)
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(404, `${resource} not found: ${id}`, 'NOT_FOUND')
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(401, message, 'UNAUTHORIZED')
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Forbidden') {
    super(403, message, 'FORBIDDEN')
  }
}

// Usage
export async function getUser(id: string) {
  const user = await db.users.findUnique({ where: { id } })

  if (!user) {
    throw new NotFoundError('User', id)
  }

  return user
}
```

### Global Error Handler

```typescript
// lib/error-handler.ts
export function handleApiError(error: unknown): Response {
  // Log error for monitoring
  console.error('API Error:', error)

  // Handle known errors
  if (error instanceof AppError) {
    return NextResponse.json(
      {
        success: false,
        error: error.message,
        code: error.code,
        details: error.details
      },
      { status: error.statusCode }
    )
  }

  // Handle Zod validation errors
  if (error instanceof z.ZodError) {
    return NextResponse.json(
      {
        success: false,
        error: 'Validation failed',
        code: 'VALIDATION_ERROR',
        details: error.errors
      },
      { status: 400 }
    )
  }

  // Handle database errors
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    if (error.code === 'P2002') {
      return NextResponse.json(
        { success: false, error: 'Duplicate entry', code: 'DUPLICATE' },
        { status: 409 }
      )
    }
  }

  // Generic error (don't expose internals)
  return NextResponse.json(
    {
      success: false,
      error: 'Internal server error',
      code: 'INTERNAL_ERROR'
    },
    { status: 500 }
  )
}

// Usage in API route
export async function GET(request: Request) {
  try {
    const data = await fetchData()
    return NextResponse.json({ success: true, data })
  } catch (error) {
    return handleApiError(error)
  }
}
```

### Graceful Degradation

```typescript
export async function searchMarketsWithFallback(query: string) {
  try {
    // Try semantic search with Redis
    const results = await searchVectorDatabase(query)
    return { results, method: 'semantic' }

  } catch (error) {
    console.warn('Vector search failed, falling back to full-text:', error)

    try {
      // Fallback to Supabase full-text search
      const results = await supabase
        .from('markets')
        .select('*')
        .textSearch('fts', query)

      return { results: results.data, method: 'fulltext' }

    } catch (fallbackError) {
      console.error('Full-text search failed, using substring:', fallbackError)

      // Last resort: substring match
      const results = await supabase
        .from('markets')
        .select('*')
        .ilike('name', `%${query}%`)

      return { results: results.data, method: 'substring' }
    }
  }
}
```

## Caching Patterns

### Redis Caching

```typescript
import Redis from 'ioredis'

const redis = new Redis(process.env.REDIS_URL!)

// Cache-aside pattern
export async function getMarketWithCache(id: string) {
  const cacheKey = `market:${id}`

  // Try cache first
  const cached = await redis.get(cacheKey)
  if (cached) {
    return JSON.parse(cached)
  }

  // Fetch from database
  const market = await db.markets.findUnique({ where: { id } })

  if (market) {
    // Cache for 5 minutes
    await redis.setex(cacheKey, 300, JSON.stringify(market))
  }

  return market
}

// Cache invalidation
export async function updateMarket(id: string, data: any) {
  const market = await db.markets.update({
    where: { id },
    data
  })

  // Invalidate cache
  await redis.del(`market:${id}`)

  return market
}

// Bulk cache invalidation
export async function invalidateMarketCaches(ids: string[]) {
  const keys = ids.map(id => `market:${id}`)
  if (keys.length > 0) {
    await redis.del(...keys)
  }
}
```

### In-Memory Caching

```typescript
import { LRUCache } from 'lru-cache'

// Cache with automatic eviction
const cache = new LRUCache<string, any>({
  max: 500,              // Max 500 items
  ttl: 1000 * 60 * 5,    // 5 minutes TTL
  updateAgeOnGet: true,
  updateAgeOnHas: false
})

export async function getCachedData(key: string, fetcher: () => Promise<any>) {
  // Check cache
  const cached = cache.get(key)
  if (cached) return cached

  // Fetch and cache
  const data = await fetcher()
  cache.set(key, data)
  return data
}
```

## Background Jobs

### Queue Pattern (BullMQ)

```typescript
import { Queue, Worker } from 'bullmq'

// Define job queue
const emailQueue = new Queue('email', {
  connection: {
    host: process.env.REDIS_HOST,
    port: parseInt(process.env.REDIS_PORT!)
  }
})

// Add job to queue
export async function sendWelcomeEmail(userId: string, email: string) {
  await emailQueue.add('welcome', {
    userId,
    email
  }, {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000
    }
  })
}

// Process jobs
const emailWorker = new Worker('email', async (job) => {
  const { userId, email } = job.data

  switch (job.name) {
    case 'welcome':
      await sendEmail({
        to: email,
        subject: 'Welcome!',
        template: 'welcome',
        data: { userId }
      })
      break

    default:
      throw new Error(`Unknown job: ${job.name}`)
  }
}, {
  connection: {
    host: process.env.REDIS_HOST,
    port: parseInt(process.env.REDIS_PORT!)
  }
})

emailWorker.on('failed', (job, error) => {
  console.error(`Job ${job?.id} failed:`, error)
})
```

## Middleware Patterns

```typescript
// Authentication middleware
export async function withAuth(handler: Function) {
  return async (request: Request, ...args: any[]) => {
    const token = request.cookies.get('token')?.value

    if (!token) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    const user = await verifyToken(token)
    if (!user) {
      return NextResponse.json(
        { error: 'Invalid token' },
        { status: 401 }
      )
    }

    // Add user to request context
    request.user = user
    return handler(request, ...args)
  }
}

// Usage
export const GET = withAuth(async (request: Request) => {
  const userId = request.user.id
  // Handle request
})
```

## Best Practices

- **API Design**: RESTful conventions, consistent response format, versioning
- **Validation**: Validate all inputs with schemas (Zod, Joi)
- **Error Handling**: Structured error classes, global error handler
- **Database**: Use transactions, optimize queries, add indexes
- **Caching**: Cache-aside pattern, invalidation strategy
- **Security**: Authentication on all protected routes, authorization checks
- **Logging**: Structured logs, no sensitive data
- **Testing**: Unit tests for business logic, integration tests for APIs
- **Documentation**: OpenAPI/Swagger specs for APIs
- **Monitoring**: Health checks, error tracking (Sentry), performance metrics
