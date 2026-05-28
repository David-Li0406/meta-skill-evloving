---
name: node-patterns
description: Node.js patterns for Express/Fastify, async operations, and streams
license: MIT
---

# Node.js Patterns Skill

Server-side JavaScript patterns for Express, Fastify, async operations, streams, and production best practices.

## When to Use

- Building Node.js backend services
- Implementing REST APIs with Express or Fastify
- Working with async patterns and streams
- Structuring Node.js projects

## Project Structure

```
src/
├── index.ts              # Entry point
├── app.ts                # App setup (middleware, routes)
├── config/
│   ├── index.ts          # Config loader
│   └── env.ts            # Environment validation
├── routes/
│   ├── index.ts          # Route aggregator
│   ├── users.ts
│   └── posts.ts
├── controllers/
│   ├── users.controller.ts
│   └── posts.controller.ts
├── services/
│   ├── users.service.ts
│   └── posts.service.ts
├── repositories/
│   ├── users.repository.ts
│   └── posts.repository.ts
├── middleware/
│   ├── auth.ts
│   ├── error-handler.ts
│   └── validate.ts
├── utils/
│   ├── logger.ts
│   └── errors.ts
└── types/
    └── index.ts
```

## Express Patterns

### App Setup

```typescript
// src/app.ts
import express, { Express } from 'express'
import helmet from 'helmet'
import cors from 'cors'
import compression from 'compression'
import { errorHandler } from './middleware/error-handler'
import { notFoundHandler } from './middleware/not-found'
import routes from './routes'

export function createApp(): Express {
  const app = express()

  // Security middleware
  app.use(helmet())
  app.use(cors({ origin: process.env.CORS_ORIGIN }))

  // Body parsing
  app.use(express.json({ limit: '10kb' }))
  app.use(express.urlencoded({ extended: true }))

  // Compression
  app.use(compression())

  // Routes
  app.use('/api/v1', routes)

  // Error handling (must be last)
  app.use(notFoundHandler)
  app.use(errorHandler)

  return app
}
```

### Router Pattern

```typescript
// src/routes/users.ts
import { Router } from 'express'
import { UsersController } from '../controllers/users.controller'
import { authenticate } from '../middleware/auth'
import { validate } from '../middleware/validate'
import { createUserSchema, updateUserSchema } from '../schemas/user.schema'

const router = Router()
const controller = new UsersController()

router.get('/', controller.findAll)
router.get('/:id', controller.findById)
router.post('/', validate(createUserSchema), controller.create)
router.patch('/:id', authenticate, validate(updateUserSchema), controller.update)
router.delete('/:id', authenticate, controller.delete)

export default router
```

### Controller Pattern

```typescript
// src/controllers/users.controller.ts
import { Request, Response, NextFunction } from 'express'
import { UsersService } from '../services/users.service'
import { asyncHandler } from '../utils/async-handler'

export class UsersController {
  private service = new UsersService()

  findAll = asyncHandler(async (req: Request, res: Response) => {
    const { page = 1, limit = 10 } = req.query
    const result = await this.service.findAll({
      page: Number(page),
      limit: Number(limit),
    })
    res.json(result)
  })

  findById = asyncHandler(async (req: Request, res: Response) => {
    const user = await this.service.findById(req.params.id)
    res.json(user)
  })

  create = asyncHandler(async (req: Request, res: Response) => {
    const user = await this.service.create(req.body)
    res.status(201).json(user)
  })

  update = asyncHandler(async (req: Request, res: Response) => {
    const user = await this.service.update(req.params.id, req.body)
    res.json(user)
  })

  delete = asyncHandler(async (req: Request, res: Response) => {
    await this.service.delete(req.params.id)
    res.status(204).send()
  })
}
```

### Async Handler

```typescript
// src/utils/async-handler.ts
import { Request, Response, NextFunction, RequestHandler } from 'express'

type AsyncRequestHandler = (
  req: Request,
  res: Response,
  next: NextFunction
) => Promise<any>

export function asyncHandler(fn: AsyncRequestHandler): RequestHandler {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next)
  }
}
```

### Error Handling

```typescript
// src/utils/errors.ts
export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public code?: string
  ) {
    super(message)
    this.name = 'AppError'
    Error.captureStackTrace(this, this.constructor)
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404, 'NOT_FOUND')
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 400, 'VALIDATION_ERROR')
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED')
  }
}
```

```typescript
// src/middleware/error-handler.ts
import { ErrorRequestHandler } from 'express'
import { AppError } from '../utils/errors'
import { logger } from '../utils/logger'

export const errorHandler: ErrorRequestHandler = (err, req, res, next) => {
  logger.error(err)

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      status: 'error',
      code: err.code,
      message: err.message,
    })
  }

  // Prisma errors
  if (err.code === 'P2025') {
    return res.status(404).json({
      status: 'error',
      code: 'NOT_FOUND',
      message: 'Resource not found',
    })
  }

  // Default error
  res.status(500).json({
    status: 'error',
    code: 'INTERNAL_ERROR',
    message: process.env.NODE_ENV === 'production'
      ? 'Internal server error'
      : err.message,
  })
}
```

## Fastify Patterns

### App Setup

```typescript
// src/app.ts
import Fastify, { FastifyInstance } from 'fastify'
import cors from '@fastify/cors'
import helmet from '@fastify/helmet'
import rateLimit from '@fastify/rate-limit'
import { usersRoutes } from './routes/users'
import { errorHandler } from './plugins/error-handler'

export async function buildApp(): Promise<FastifyInstance> {
  const app = Fastify({
    logger: true,
    trustProxy: true,
  })

  // Plugins
  await app.register(cors, { origin: process.env.CORS_ORIGIN })
  await app.register(helmet)
  await app.register(rateLimit, { max: 100, timeWindow: '1 minute' })

  // Custom plugins
  await app.register(errorHandler)

  // Routes
  await app.register(usersRoutes, { prefix: '/api/v1/users' })

  return app
}
```

### Route with Schema Validation

```typescript
// src/routes/users.ts
import { FastifyPluginAsync } from 'fastify'
import { Type, Static } from '@sinclair/typebox'

const UserSchema = Type.Object({
  id: Type.String(),
  email: Type.String({ format: 'email' }),
  name: Type.String(),
})

const CreateUserSchema = Type.Object({
  email: Type.String({ format: 'email' }),
  name: Type.String({ minLength: 1 }),
  password: Type.String({ minLength: 8 }),
})

type User = Static<typeof UserSchema>
type CreateUser = Static<typeof CreateUserSchema>

export const usersRoutes: FastifyPluginAsync = async (app) => {
  app.get<{ Reply: User[] }>(
    '/',
    {
      schema: {
        response: { 200: Type.Array(UserSchema) },
      },
    },
    async (request, reply) => {
      return await usersService.findAll()
    }
  )

  app.post<{ Body: CreateUser; Reply: User }>(
    '/',
    {
      schema: {
        body: CreateUserSchema,
        response: { 201: UserSchema },
      },
    },
    async (request, reply) => {
      const user = await usersService.create(request.body)
      return reply.status(201).send(user)
    }
  )
}
```

## Async Patterns

### Promise.all with Error Handling

```typescript
// Process multiple items in parallel with individual error handling
async function processItems(items: Item[]): Promise<Result[]> {
  const results = await Promise.allSettled(
    items.map(item => processItem(item))
  )

  const successful: Result[] = []
  const failed: { item: Item; error: Error }[] = []

  results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      successful.push(result.value)
    } else {
      failed.push({ item: items[index], error: result.reason })
    }
  })

  if (failed.length > 0) {
    logger.warn(`${failed.length} items failed processing`, { failed })
  }

  return successful
}
```

### Concurrency Control

```typescript
// Process with limited concurrency
async function processWithConcurrency<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  concurrency: number
): Promise<R[]> {
  const results: R[] = []
  const executing: Promise<void>[] = []

  for (const item of items) {
    const promise = processor(item).then(result => {
      results.push(result)
    })

    executing.push(promise)

    if (executing.length >= concurrency) {
      await Promise.race(executing)
      executing.splice(
        executing.findIndex(p => p === promise),
        1
      )
    }
  }

  await Promise.all(executing)
  return results
}

// Usage
const results = await processWithConcurrency(urls, fetchUrl, 5)
```

### Retry Pattern

```typescript
interface RetryOptions {
  maxAttempts: number
  delayMs: number
  backoffMultiplier?: number
  shouldRetry?: (error: Error) => boolean
}

async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions
): Promise<T> {
  const {
    maxAttempts,
    delayMs,
    backoffMultiplier = 2,
    shouldRetry = () => true,
  } = options

  let lastError: Error
  let delay = delayMs

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error

      if (attempt === maxAttempts || !shouldRetry(lastError)) {
        throw lastError
      }

      logger.warn(`Attempt ${attempt} failed, retrying in ${delay}ms`)
      await sleep(delay)
      delay *= backoffMultiplier
    }
  }

  throw lastError!
}

// Usage
const data = await withRetry(() => fetchFromAPI(), {
  maxAttempts: 3,
  delayMs: 1000,
  shouldRetry: (err) => err.message.includes('timeout'),
})
```

### Circuit Breaker

```typescript
enum CircuitState {
  CLOSED,
  OPEN,
  HALF_OPEN,
}

class CircuitBreaker {
  private state = CircuitState.CLOSED
  private failures = 0
  private lastFailureTime?: number
  private successCount = 0

  constructor(
    private readonly threshold: number = 5,
    private readonly timeout: number = 30000,
    private readonly halfOpenSuccesses: number = 2
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === CircuitState.OPEN) {
      if (Date.now() - this.lastFailureTime! > this.timeout) {
        this.state = CircuitState.HALF_OPEN
        this.successCount = 0
      } else {
        throw new Error('Circuit breaker is OPEN')
      }
    }

    try {
      const result = await fn()

      if (this.state === CircuitState.HALF_OPEN) {
        this.successCount++
        if (this.successCount >= this.halfOpenSuccesses) {
          this.reset()
        }
      }

      return result
    } catch (error) {
      this.recordFailure()
      throw error
    }
  }

  private recordFailure(): void {
    this.failures++
    this.lastFailureTime = Date.now()

    if (this.failures >= this.threshold) {
      this.state = CircuitState.OPEN
    }
  }

  private reset(): void {
    this.state = CircuitState.CLOSED
    this.failures = 0
    this.successCount = 0
  }
}
```

## Stream Patterns

### Transform Stream

```typescript
import { Transform, TransformCallback } from 'stream'

class JSONLineTransform extends Transform {
  private buffer = ''

  constructor() {
    super({ objectMode: true })
  }

  _transform(chunk: Buffer, encoding: string, callback: TransformCallback): void {
    this.buffer += chunk.toString()
    const lines = this.buffer.split('\n')
    this.buffer = lines.pop() || ''

    for (const line of lines) {
      if (line.trim()) {
        try {
          this.push(JSON.parse(line))
        } catch (error) {
          this.emit('error', new Error(`Invalid JSON: ${line}`))
        }
      }
    }

    callback()
  }

  _flush(callback: TransformCallback): void {
    if (this.buffer.trim()) {
      try {
        this.push(JSON.parse(this.buffer))
      } catch (error) {
        this.emit('error', new Error(`Invalid JSON: ${this.buffer}`))
      }
    }
    callback()
  }
}

// Usage
import { createReadStream } from 'fs'
import { pipeline } from 'stream/promises'

await pipeline(
  createReadStream('data.jsonl'),
  new JSONLineTransform(),
  async function* (source) {
    for await (const record of source) {
      yield processRecord(record)
    }
  },
  createWriteStream('output.jsonl')
)
```

### Streaming HTTP Response

```typescript
import { Readable } from 'stream'

app.get('/stream', async (req, res) => {
  res.setHeader('Content-Type', 'application/json')
  res.setHeader('Transfer-Encoding', 'chunked')

  const cursor = db.collection.find().cursor()

  res.write('[\n')
  let first = true

  for await (const doc of cursor) {
    if (!first) res.write(',\n')
    first = false
    res.write(JSON.stringify(doc))
  }

  res.write('\n]')
  res.end()
})
```

## Validation with Zod

```typescript
import { z } from 'zod'
import { Request, Response, NextFunction } from 'express'

const createUserSchema = z.object({
  body: z.object({
    email: z.string().email(),
    name: z.string().min(1).max(100),
    password: z.string().min(8),
    role: z.enum(['user', 'admin']).default('user'),
  }),
  query: z.object({}).optional(),
  params: z.object({}).optional(),
})

type CreateUserRequest = z.infer<typeof createUserSchema>

function validate<T extends z.ZodSchema>(schema: T) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse({
      body: req.body,
      query: req.query,
      params: req.params,
    })

    if (!result.success) {
      return res.status(400).json({
        status: 'error',
        code: 'VALIDATION_ERROR',
        errors: result.error.flatten().fieldErrors,
      })
    }

    req.body = result.data.body
    next()
  }
}

// Usage
router.post('/users', validate(createUserSchema), controller.create)
```

## Environment Configuration

```typescript
// src/config/env.ts
import { z } from 'zod'

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.string().transform(Number).default('3000'),
  DATABASE_URL: z.string(),
  JWT_SECRET: z.string().min(32),
  CORS_ORIGIN: z.string().url().optional(),
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
})

export type Env = z.infer<typeof envSchema>

function validateEnv(): Env {
  const result = envSchema.safeParse(process.env)

  if (!result.success) {
    console.error('Invalid environment variables:')
    console.error(result.error.flatten().fieldErrors)
    process.exit(1)
  }

  return result.data
}

export const env = validateEnv()
```

## Graceful Shutdown

```typescript
// src/index.ts
import { createApp } from './app'
import { env } from './config/env'
import { logger } from './utils/logger'
import { db } from './db'

async function main() {
  const app = createApp()

  const server = app.listen(env.PORT, () => {
    logger.info(`Server running on port ${env.PORT}`)
  })

  // Graceful shutdown
  const shutdown = async (signal: string) => {
    logger.info(`${signal} received, shutting down gracefully`)

    server.close(async () => {
      logger.info('HTTP server closed')

      try {
        await db.$disconnect()
        logger.info('Database connection closed')
        process.exit(0)
      } catch (error) {
        logger.error('Error during shutdown', error)
        process.exit(1)
      }
    })

    // Force shutdown after 30s
    setTimeout(() => {
      logger.error('Forced shutdown after timeout')
      process.exit(1)
    }, 30000)
  }

  process.on('SIGTERM', () => shutdown('SIGTERM'))
  process.on('SIGINT', () => shutdown('SIGINT'))
}

main().catch(error => {
  logger.error('Failed to start server', error)
  process.exit(1)
})
```

## Best Practices

1. **Always validate input** - use Zod or similar at API boundaries
2. **Use async/await** - avoid callback hell
3. **Handle errors properly** - don't swallow errors, use error boundaries
4. **Implement graceful shutdown** - clean up connections on exit
5. **Use environment variables** - never hardcode secrets
6. **Structure by feature** - not by technical layer for larger apps
7. **Use TypeScript** - type safety prevents runtime errors
8. **Log meaningfully** - structured logging with levels
9. **Rate limit APIs** - protect against abuse
10. **Use health checks** - `/health` endpoint for monitoring
