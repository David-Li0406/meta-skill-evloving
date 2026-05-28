# Node.js Best Practices

**Version 1.0.0**  
January 2026

> **Note:**  
> This document is primarily for AI agents and LLMs to follow when maintaining,  
> generating, or refactoring Node.js codebases. Humans may also find it useful,  
> but guidance here is optimized for automation and consistency by AI-assisted workflows.

---

## Abstract

Comprehensive guide for Node.js development in 2025+, designed for AI agents and LLMs. Contains decision-making principles across 10 categories: framework selection, runtime considerations, architecture, error handling, async patterns, validation, security, testing, database access, and logging. Each section includes detailed explanations, real-world examples comparing incorrect vs. correct implementations, and decision trees to guide automated code generation.

**Philosophy:** Learn to THINK, not memorize code patterns. Every project deserves fresh consideration based on its requirements.

---

## Table of Contents

1. [Framework Selection](#1-framework-selection) — **CRITICAL**
2. [Runtime Considerations](#2-runtime-considerations) — **HIGH**
3. [Architecture Principles](#3-architecture-principles) — **HIGH**
4. [Error Handling](#4-error-handling) — **CRITICAL**
5. [Async Patterns](#5-async-patterns) — **CRITICAL**
6. [Validation](#6-validation) — **HIGH**
7. [Security](#7-security) — **CRITICAL**
8. [Testing](#8-testing) — **MEDIUM**
9. [Database Access](#9-database-access) — **HIGH**
10. [Logging & Monitoring](#10-logging--monitoring) — **MEDIUM**

---

## 1. Framework Selection

**Impact: CRITICAL (affects entire project architecture)**

Choose framework based on context, not habit. Ask these questions first:

### 1.1 Decision Tree

```
What are you building?
│
├── Edge/Serverless (Cloudflare Workers, Vercel Edge)
│   └── Hono ✓ (zero-dependency, ultra-fast cold starts)
│
├── High Performance API (>10k req/s)
│   └── Fastify ✓ (2-3x faster than Express)
│
├── Enterprise/Team with Java/C# background
│   └── NestJS ✓ (structured, DI, decorators)
│
├── Legacy/Maximum ecosystem compatibility
│   └── Express ✓ (mature, most middleware)
│
└── Full-stack with frontend
    └── Next.js API Routes or tRPC ✓
```

### 1.2 Framework Comparison

| Factor | Hono | Fastify | Express | NestJS |
|--------|------|---------|---------|--------|
| **Best for** | Edge, serverless | Performance | Legacy, learning | Enterprise |
| **Cold start** | ~5ms | ~50ms | ~100ms | ~200ms |
| **Requests/sec** | 150k+ | 75k+ | 25k+ | 20k+ |
| **Bundle size** | 14KB | 2MB | 1.5MB | 10MB+ |
| **TypeScript** | Native | Excellent | Good | Native |
| **Learning curve** | Low | Medium | Low | High |

### 1.3 Hono Example (Edge/Serverless)

**When to use:** Cloudflare Workers, Vercel Edge, Deno Deploy, Bun

```typescript
import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { jwt } from 'hono/jwt'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()

// Middleware
app.use('/*', cors())
app.use('/api/*', jwt({ secret: process.env.JWT_SECRET! }))

// Validation schema
const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
})

// Routes with validation
app.post('/api/users', zValidator('json', createUserSchema), async (c) => {
  const { email, name } = c.req.valid('json')
  const user = await createUser({ email, name })
  return c.json(user, 201)
})

app.get('/api/users/:id', async (c) => {
  const id = c.req.param('id')
  const user = await getUser(id)
  if (!user) {
    return c.json({ error: 'User not found' }, 404)
  }
  return c.json(user)
})

export default app
```

### 1.4 Fastify Example (High Performance)

**When to use:** High-throughput APIs, microservices, real-time applications

```typescript
import Fastify from 'fastify'
import cors from '@fastify/cors'
import jwt from '@fastify/jwt'
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox'
import { Type } from '@sinclair/typebox'

const fastify = Fastify({
  logger: true,
}).withTypeProvider<TypeBoxTypeProvider>()

// Plugins
await fastify.register(cors)
await fastify.register(jwt, { secret: process.env.JWT_SECRET! })

// Schema definitions
const CreateUserSchema = Type.Object({
  email: Type.String({ format: 'email' }),
  name: Type.String({ minLength: 2, maxLength: 100 }),
})

const UserResponseSchema = Type.Object({
  id: Type.String(),
  email: Type.String(),
  name: Type.String(),
  createdAt: Type.String(),
})

// Routes with schema validation
fastify.post('/api/users', {
  schema: {
    body: CreateUserSchema,
    response: { 201: UserResponseSchema },
  },
}, async (request, reply) => {
  const { email, name } = request.body
  const user = await createUser({ email, name })
  return reply.code(201).send(user)
})

fastify.get<{ Params: { id: string } }>('/api/users/:id', async (request, reply) => {
  const { id } = request.params
  const user = await getUser(id)
  if (!user) {
    return reply.code(404).send({ error: 'User not found' })
  }
  return user
})

await fastify.listen({ port: 3000 })
```

### 1.5 Questions to Ask User

Before implementing, ALWAYS ask:

1. "What's the deployment target?" (Edge, serverless, traditional server)
2. "Is cold start time critical?" (< 50ms requirement?)
3. "Does the team have existing framework experience?"
4. "What's the expected traffic volume?"
5. "Is there legacy Express code to maintain?"

---

## 2. Runtime Considerations

**Impact: HIGH (affects build process and deployment)**

### 2.1 Node.js 22+ Native TypeScript

**When to use:** Simple scripts, CLI tools, rapid prototyping

```bash
# Run TypeScript directly (Node.js 22+)
node --experimental-strip-types src/index.ts

# For production, still recommend build step
```

**Limitations:**
- No type checking at runtime
- No path aliases support
- Limited decorator support

### 2.2 Module System Decision

```
ESM (import/export)          CommonJS (require)
├── Modern standard          ├── Legacy compatibility
├── Better tree-shaking      ├── More packages support
├── Async module loading     ├── Simpler __dirname
├── Top-level await          └── Use for: legacy codebases
└── Use for: new projects
```

**ESM Configuration (package.json):**

```json
{
  "type": "module",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  },
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

**tsconfig.json for ESM:**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true
  },
  "include": ["src/**/*"]
}
```

### 2.3 Runtime Selection

| Runtime | Best For | Key Features |
|---------|----------|--------------|
| **Node.js** | General purpose | Largest ecosystem, stable |
| **Bun** | Performance | 3x faster, built-in bundler |
| **Deno** | Security-first | Permissions, built-in TS |

---

## 3. Architecture Principles

**Impact: HIGH (affects maintainability and testability)**

### 3.1 Layered Architecture

```
┌─────────────────────────────────────────┐
│           Controller Layer              │
│   • Handles HTTP specifics              │
│   • Input validation at boundary        │
│   • Route definitions                   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│           Service Layer                 │
│   • Business logic                      │
│   • Framework-agnostic                  │
│   • Orchestrates operations             │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          Repository Layer               │
│   • Data access only                    │
│   • Database queries                    │
│   • ORM interactions                    │
└─────────────────────────────────────────┘
```

### 3.2 Directory Structure

```
src/
├── controllers/          # HTTP handlers
│   └── user.controller.ts
├── services/             # Business logic
│   └── user.service.ts
├── repositories/         # Data access
│   └── user.repository.ts
├── models/               # Data models/entities
│   └── user.model.ts
├── middleware/           # Express/Fastify middleware
│   ├── auth.middleware.ts
│   └── error.middleware.ts
├── validators/           # Input validation schemas
│   └── user.validator.ts
├── utils/                # Shared utilities
│   └── logger.ts
├── types/                # TypeScript types
│   └── index.ts
├── config/               # Configuration
│   └── index.ts
└── index.ts              # Entry point
```

### 3.3 Implementation Example

**Controller Layer (user.controller.ts):**

```typescript
import { Request, Response, NextFunction } from 'express'
import { UserService } from '../services/user.service'
import { CreateUserDto, UpdateUserDto } from '../validators/user.validator'

export class UserController {
  constructor(private userService: UserService) {}

  async create(req: Request, res: Response, next: NextFunction) {
    try {
      const dto: CreateUserDto = req.body
      const user = await this.userService.create(dto)
      res.status(201).json(user)
    } catch (error) {
      next(error)
    }
  }

  async findById(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params
      const user = await this.userService.findById(id)
      res.json(user)
    } catch (error) {
      next(error)
    }
  }

  async update(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params
      const dto: UpdateUserDto = req.body
      const user = await this.userService.update(id, dto)
      res.json(user)
    } catch (error) {
      next(error)
    }
  }

  async delete(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params
      await this.userService.delete(id)
      res.status(204).send()
    } catch (error) {
      next(error)
    }
  }
}
```

**Service Layer (user.service.ts):**

```typescript
import { UserRepository } from '../repositories/user.repository'
import { CreateUserDto, UpdateUserDto } from '../validators/user.validator'
import { NotFoundError, ConflictError } from '../utils/errors'
import { hashPassword } from '../utils/crypto'

export class UserService {
  constructor(private userRepository: UserRepository) {}

  async create(dto: CreateUserDto) {
    // Check for duplicate email
    const existing = await this.userRepository.findByEmail(dto.email)
    if (existing) {
      throw new ConflictError('Email already registered')
    }

    // Hash password
    const hashedPassword = await hashPassword(dto.password)

    // Create user
    return this.userRepository.create({
      ...dto,
      password: hashedPassword,
    })
  }

  async findById(id: string) {
    const user = await this.userRepository.findById(id)
    if (!user) {
      throw new NotFoundError('User not found')
    }
    return user
  }

  async update(id: string, dto: UpdateUserDto) {
    const user = await this.findById(id)
    
    if (dto.email && dto.email !== user.email) {
      const existing = await this.userRepository.findByEmail(dto.email)
      if (existing) {
        throw new ConflictError('Email already taken')
      }
    }

    return this.userRepository.update(id, dto)
  }

  async delete(id: string) {
    await this.findById(id) // Ensure exists
    return this.userRepository.delete(id)
  }
}
```

**Repository Layer (user.repository.ts):**

```typescript
import { prisma } from '../config/database'
import { User } from '../models/user.model'

export class UserRepository {
  async create(data: Omit<User, 'id' | 'createdAt' | 'updatedAt'>) {
    return prisma.user.create({ data })
  }

  async findById(id: string) {
    return prisma.user.findUnique({ where: { id } })
  }

  async findByEmail(email: string) {
    return prisma.user.findUnique({ where: { email } })
  }

  async update(id: string, data: Partial<User>) {
    return prisma.user.update({ where: { id }, data })
  }

  async delete(id: string) {
    return prisma.user.delete({ where: { id } })
  }

  async findAll(options?: { skip?: number; take?: number }) {
    return prisma.user.findMany(options)
  }
}
```

### 3.4 When to Simplify

- **Small scripts:** Single file OK
- **Prototypes:** Less structure acceptable
- **Microservices:** May not need full layering

**Always ask:** "Will this project grow?"

---

## 4. Error Handling

**Impact: CRITICAL (affects debugging and user experience)**

### 4.1 Custom Error Classes

```typescript
// src/utils/errors.ts

export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public code: string = 'INTERNAL_ERROR',
    public isOperational: boolean = true
  ) {
    super(message)
    this.name = this.constructor.name
    Error.captureStackTrace(this, this.constructor)
  }
}

export class BadRequestError extends AppError {
  constructor(message: string = 'Bad request') {
    super(message, 400, 'BAD_REQUEST')
  }
}

export class UnauthorizedError extends AppError {
  constructor(message: string = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED')
  }
}

export class ForbiddenError extends AppError {
  constructor(message: string = 'Forbidden') {
    super(message, 403, 'FORBIDDEN')
  }
}

export class NotFoundError extends AppError {
  constructor(message: string = 'Resource not found') {
    super(message, 404, 'NOT_FOUND')
  }
}

export class ConflictError extends AppError {
  constructor(message: string = 'Resource conflict') {
    super(message, 409, 'CONFLICT')
  }
}

export class ValidationError extends AppError {
  constructor(
    message: string = 'Validation failed',
    public errors: Record<string, string[]> = {}
  ) {
    super(message, 422, 'VALIDATION_ERROR')
  }
}

export class TooManyRequestsError extends AppError {
  constructor(message: string = 'Too many requests') {
    super(message, 429, 'TOO_MANY_REQUESTS')
  }
}
```

### 4.2 Centralized Error Handler Middleware

```typescript
// src/middleware/error.middleware.ts

import { Request, Response, NextFunction } from 'express'
import { AppError, ValidationError } from '../utils/errors'
import { logger } from '../utils/logger'

interface ErrorResponse {
  success: false
  error: {
    code: string
    message: string
    errors?: Record<string, string[]>
  }
}

export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Log error
  logger.error({
    message: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method,
    userId: req.user?.id,
    requestId: req.headers['x-request-id'],
  })

  // Handle known operational errors
  if (err instanceof AppError && err.isOperational) {
    const response: ErrorResponse = {
      success: false,
      error: {
        code: err.code,
        message: err.message,
      },
    }

    // Add validation errors if present
    if (err instanceof ValidationError) {
      response.error.errors = err.errors
    }

    return res.status(err.statusCode).json(response)
  }

  // Handle Zod validation errors
  if (err.name === 'ZodError') {
    return res.status(422).json({
      success: false,
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Validation failed',
        errors: formatZodErrors(err),
      },
    })
  }

  // Handle Prisma errors
  if (err.name === 'PrismaClientKnownRequestError') {
    return handlePrismaError(err, res)
  }

  // Unknown errors - don't leak internal details
  return res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
    },
  })
}

// Async wrapper for route handlers
export function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<any>
) {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next)
  }
}
```

### 4.3 Status Code Reference

| Situation | Status | When to Use |
|-----------|--------|-------------|
| Bad input | 400 | Malformed JSON, missing required fields |
| No auth | 401 | Missing or invalid credentials |
| No permission | 403 | Valid auth, but action not allowed |
| Not found | 404 | Resource doesn't exist |
| Conflict | 409 | Duplicate entry, state conflict |
| Validation | 422 | Schema valid but business rules fail |
| Rate limit | 429 | Too many requests |
| Server error | 500 | Our fault, log everything |

---

## 5. Async Patterns

**Impact: CRITICAL (affects performance and scalability)**

### 5.1 Promise.all for Parallel Operations

**Incorrect: Sequential execution (slow)**

```typescript
async function getUserData(userId: string) {
  const user = await getUser(userId)
  const posts = await getPosts(userId)
  const followers = await getFollowers(userId)
  return { user, posts, followers }
}
// Total time: getUser + getPosts + getFollowers
```

**Correct: Parallel execution (fast)**

```typescript
async function getUserData(userId: string) {
  const [user, posts, followers] = await Promise.all([
    getUser(userId),
    getPosts(userId),
    getFollowers(userId),
  ])
  return { user, posts, followers }
}
// Total time: max(getUser, getPosts, getFollowers)
```

### 5.2 Promise.allSettled for Fault Tolerance

**When some operations can fail independently:**

```typescript
async function sendNotifications(userIds: string[]) {
  const results = await Promise.allSettled(
    userIds.map(id => sendNotification(id))
  )

  const succeeded = results.filter(r => r.status === 'fulfilled')
  const failed = results.filter(r => r.status === 'rejected')

  logger.info(`Sent ${succeeded.length}/${userIds.length} notifications`)
  
  if (failed.length > 0) {
    logger.error(`Failed notifications: ${failed.length}`)
  }

  return { succeeded: succeeded.length, failed: failed.length }
}
```

### 5.3 Promise.race for Timeout

```typescript
async function fetchWithTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number
): Promise<T> {
  const timeout = new Promise<never>((_, reject) => {
    setTimeout(() => reject(new Error('Request timeout')), timeoutMs)
  })
  
  return Promise.race([promise, timeout])
}

// Usage
const data = await fetchWithTimeout(fetchData(), 5000)
```

### 5.4 Avoiding Event Loop Blocking

**I/O-bound (async helps):**
- Database queries
- HTTP requests
- File system operations
- Network operations

**CPU-bound (async doesn't help):**
- Crypto operations
- Image processing
- Complex calculations
- JSON parsing large files

**Solution for CPU-bound work:**

```typescript
import { Worker } from 'worker_threads'

function runWorker<T>(workerPath: string, data: any): Promise<T> {
  return new Promise((resolve, reject) => {
    const worker = new Worker(workerPath, { workerData: data })
    worker.on('message', resolve)
    worker.on('error', reject)
    worker.on('exit', (code) => {
      if (code !== 0) {
        reject(new Error(`Worker stopped with exit code ${code}`))
      }
    })
  })
}

// Usage
const result = await runWorker('./workers/image-processor.js', { imagePath })
```

### 5.5 Never Use Sync Methods in Production

**Incorrect:**

```typescript
import { readFileSync, writeFileSync } from 'fs'

// BLOCKS EVENT LOOP!
const config = JSON.parse(readFileSync('config.json', 'utf-8'))
writeFileSync('output.json', JSON.stringify(data))
```

**Correct:**

```typescript
import { readFile, writeFile } from 'fs/promises'

const config = JSON.parse(await readFile('config.json', 'utf-8'))
await writeFile('output.json', JSON.stringify(data))
```

---

## 6. Validation

**Impact: HIGH (security and data integrity)**

### 6.1 Validation Library Selection

| Library | Best For | Bundle Size |
|---------|----------|-------------|
| **Zod** | TypeScript first, inference | 13KB |
| **Valibot** | Smaller bundle (tree-shakeable) | 1KB |
| **ArkType** | Performance critical | 8KB |
| **Yup** | Existing React Form usage | 15KB |

### 6.2 Zod Validation Example

```typescript
// src/validators/user.validator.ts
import { z } from 'zod'

export const createUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[a-z]/, 'Password must contain lowercase letter')
    .regex(/[0-9]/, 'Password must contain number'),
  name: z.string().min(2).max(100),
  role: z.enum(['user', 'admin']).default('user'),
})

export const updateUserSchema = createUserSchema.partial().omit({ password: true })

export const userIdSchema = z.object({
  id: z.string().uuid('Invalid user ID'),
})

// Type inference
export type CreateUserDto = z.infer<typeof createUserSchema>
export type UpdateUserDto = z.infer<typeof updateUserSchema>
```

### 6.3 Validation Middleware

```typescript
// src/middleware/validate.middleware.ts
import { Request, Response, NextFunction } from 'express'
import { AnyZodObject, ZodError } from 'zod'

export const validate = (schema: AnyZodObject) => 
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      await schema.parseAsync({
        body: req.body,
        query: req.query,
        params: req.params,
      })
      next()
    } catch (error) {
      if (error instanceof ZodError) {
        const errors: Record<string, string[]> = {}
        error.errors.forEach((err) => {
          const path = err.path.join('.')
          if (!errors[path]) errors[path] = []
          errors[path].push(err.message)
        })
        
        return res.status(422).json({
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Validation failed',
            errors,
          },
        })
      }
      next(error)
    }
  }

// Usage in routes
router.post('/users', validate(z.object({ body: createUserSchema })), userController.create)
```

### 6.4 Environment Variable Validation

```typescript
// src/config/env.ts
import { z } from 'zod'

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.string().transform(Number).default('3000'),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  REDIS_URL: z.string().url().optional(),
})

// Validate at startup - fail fast!
export const env = envSchema.parse(process.env)

// Type-safe environment access
export type Env = z.infer<typeof envSchema>
```

---

## 7. Security

**Impact: CRITICAL (protects users and data)**

### 7.1 Security Checklist

- [ ] **Input validation:** All inputs validated with schema
- [ ] **Parameterized queries:** No string concatenation for SQL
- [ ] **Password hashing:** bcrypt (rounds: 12) or argon2
- [ ] **JWT verification:** Always verify signature AND expiry
- [ ] **Rate limiting:** Protect all endpoints
- [ ] **Security headers:** helmet.js configured
- [ ] **HTTPS:** Everywhere in production
- [ ] **CORS:** Properly configured origins
- [ ] **Secrets:** Environment variables only
- [ ] **Dependencies:** npm audit regularly

### 7.2 Security Headers with Helmet

```typescript
import helmet from 'helmet'

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
}))
```

### 7.3 Rate Limiting

```typescript
import rateLimit from 'express-rate-limit'
import RedisStore from 'rate-limit-redis'
import { redis } from './config/redis'

// General API rate limit
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
  store: new RedisStore({
    sendCommand: (...args: string[]) => redis.call(...args),
  }),
  message: {
    success: false,
    error: {
      code: 'TOO_MANY_REQUESTS',
      message: 'Too many requests, please try again later',
    },
  },
})

// Strict rate limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5,
  message: {
    success: false,
    error: {
      code: 'TOO_MANY_REQUESTS',
      message: 'Too many login attempts, please try again later',
    },
  },
})

app.use('/api/', apiLimiter)
app.use('/api/auth/', authLimiter)
```

### 7.4 Password Hashing

```typescript
import bcrypt from 'bcrypt'

const SALT_ROUNDS = 12

export async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, SALT_ROUNDS)
}

export async function verifyPassword(
  password: string,
  hash: string
): Promise<boolean> {
  return bcrypt.compare(password, hash)
}
```

### 7.5 JWT Authentication

```typescript
import jwt from 'jsonwebtoken'
import { UnauthorizedError } from '../utils/errors'

interface JwtPayload {
  userId: string
  email: string
  role: string
}

export function generateTokens(payload: JwtPayload) {
  const accessToken = jwt.sign(payload, process.env.JWT_SECRET!, {
    expiresIn: '15m',
  })
  
  const refreshToken = jwt.sign(payload, process.env.JWT_REFRESH_SECRET!, {
    expiresIn: '7d',
  })
  
  return { accessToken, refreshToken }
}

export function verifyAccessToken(token: string): JwtPayload {
  try {
    return jwt.verify(token, process.env.JWT_SECRET!) as JwtPayload
  } catch (error) {
    throw new UnauthorizedError('Invalid or expired token')
  }
}

// Auth middleware
export function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization
  
  if (!authHeader?.startsWith('Bearer ')) {
    throw new UnauthorizedError('Missing authorization header')
  }
  
  const token = authHeader.slice(7)
  req.user = verifyAccessToken(token)
  next()
}
```

### 7.6 SQL Injection Prevention

**Incorrect: String concatenation**

```typescript
// VULNERABLE!
const query = `SELECT * FROM users WHERE email = '${email}'`
await db.query(query)
```

**Correct: Parameterized queries**

```typescript
// Prisma (safe by default)
const user = await prisma.user.findUnique({
  where: { email },
})

// Raw query with parameters
const users = await prisma.$queryRaw`
  SELECT * FROM users WHERE email = ${email}
`

// pg library
const result = await pool.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
)
```

---

## 8. Testing

**Impact: MEDIUM (ensures reliability)**

### 8.1 Test Strategy

| Type | Purpose | Tools | Coverage |
|------|---------|-------|----------|
| **Unit** | Business logic | node:test, Vitest | 80%+ |
| **Integration** | API endpoints | Supertest | Critical paths |
| **E2E** | Full user flows | Playwright | Happy paths |

### 8.2 Unit Testing with Node.js Built-in

```typescript
// src/services/__tests__/user.service.test.ts
import { describe, it, beforeEach, mock } from 'node:test'
import assert from 'node:assert'
import { UserService } from '../user.service'
import { UserRepository } from '../../repositories/user.repository'

describe('UserService', () => {
  let userService: UserService
  let mockRepository: UserRepository

  beforeEach(() => {
    mockRepository = {
      findByEmail: mock.fn(),
      create: mock.fn(),
      findById: mock.fn(),
    } as unknown as UserRepository
    
    userService = new UserService(mockRepository)
  })

  describe('create', () => {
    it('should create user when email is not taken', async () => {
      mockRepository.findByEmail = mock.fn(() => Promise.resolve(null))
      mockRepository.create = mock.fn(() => Promise.resolve({
        id: '1',
        email: 'test@example.com',
        name: 'Test User',
      }))

      const result = await userService.create({
        email: 'test@example.com',
        password: 'Password123',
        name: 'Test User',
      })

      assert.strictEqual(result.email, 'test@example.com')
    })

    it('should throw ConflictError when email is taken', async () => {
      mockRepository.findByEmail = mock.fn(() => Promise.resolve({
        id: '1',
        email: 'test@example.com',
      }))

      await assert.rejects(
        () => userService.create({
          email: 'test@example.com',
          password: 'Password123',
          name: 'Test User',
        }),
        { name: 'ConflictError' }
      )
    })
  })
})
```

### 8.3 Integration Testing with Supertest

```typescript
// src/__tests__/api/users.test.ts
import { describe, it, beforeAll, afterAll } from 'node:test'
import assert from 'node:assert'
import request from 'supertest'
import { app } from '../../app'
import { prisma } from '../../config/database'

describe('Users API', () => {
  beforeAll(async () => {
    await prisma.$connect()
  })

  afterAll(async () => {
    await prisma.user.deleteMany()
    await prisma.$disconnect()
  })

  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'test@example.com',
          password: 'Password123',
          name: 'Test User',
        })
        .expect(201)

      assert.strictEqual(response.body.email, 'test@example.com')
      assert.strictEqual(response.body.name, 'Test User')
      assert.ok(!response.body.password) // Password should not be returned
    })

    it('should return 422 for invalid email', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'invalid-email',
          password: 'Password123',
          name: 'Test User',
        })
        .expect(422)

      assert.strictEqual(response.body.error.code, 'VALIDATION_ERROR')
    })
  })
})
```

### 8.4 Test Priorities

1. **Critical paths:** Auth, payments, core business logic
2. **Edge cases:** Empty inputs, boundaries, nulls
3. **Error handling:** What happens when things fail
4. **NOT worth testing:** Framework code, trivial getters

---

## 9. Database Access

**Impact: HIGH (performance and data integrity)**

### 9.1 Prisma Best Practices

```typescript
// src/config/database.ts
import { PrismaClient } from '@prisma/client'

// Prevent multiple instances in development
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development' 
    ? ['query', 'error', 'warn'] 
    : ['error'],
})

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma
}
```

### 9.2 Transaction Patterns

```typescript
// Simple transaction
const [user, profile] = await prisma.$transaction([
  prisma.user.create({ data: userData }),
  prisma.profile.create({ data: profileData }),
])

// Interactive transaction
const result = await prisma.$transaction(async (tx) => {
  const user = await tx.user.findUnique({ where: { id } })
  
  if (!user) {
    throw new NotFoundError('User not found')
  }
  
  if (user.balance < amount) {
    throw new BadRequestError('Insufficient balance')
  }
  
  return tx.user.update({
    where: { id },
    data: { balance: { decrement: amount } },
  })
})
```

### 9.3 Query Optimization

```typescript
// Select only needed fields
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    email: true,
  },
})

// Pagination
const users = await prisma.user.findMany({
  skip: (page - 1) * pageSize,
  take: pageSize,
  orderBy: { createdAt: 'desc' },
})

// Eager loading relationships
const posts = await prisma.post.findMany({
  include: {
    author: { select: { name: true } },
    comments: { take: 5 },
  },
})
```

---

## 10. Logging & Monitoring

**Impact: MEDIUM (debugging and observability)**

### 10.1 Structured Logging with Pino

```typescript
// src/utils/logger.ts
import pino from 'pino'

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: process.env.NODE_ENV === 'development'
    ? { target: 'pino-pretty' }
    : undefined,
  base: {
    env: process.env.NODE_ENV,
    version: process.env.npm_package_version,
  },
})

// Request logging middleware
export function requestLogger(req: Request, res: Response, next: NextFunction) {
  const start = Date.now()
  
  res.on('finish', () => {
    logger.info({
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration: Date.now() - start,
      userAgent: req.headers['user-agent'],
      ip: req.ip,
    })
  })
  
  next()
}
```

### 10.2 Health Check Endpoint

```typescript
// Health check for load balancers
app.get('/health', async (req, res) => {
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    checks: {
      database: 'unknown',
      redis: 'unknown',
    },
  }

  try {
    await prisma.$queryRaw`SELECT 1`
    health.checks.database = 'ok'
  } catch {
    health.checks.database = 'error'
    health.status = 'degraded'
  }

  try {
    await redis.ping()
    health.checks.redis = 'ok'
  } catch {
    health.checks.redis = 'error'
    health.status = 'degraded'
  }

  const statusCode = health.status === 'ok' ? 200 : 503
  res.status(statusCode).json(health)
})
```

---

## Anti-Patterns Summary

### ❌ DON'T:

- Use Express for new edge/serverless projects
- Use sync methods (`readFileSync`, etc.) in production
- Put business logic in controllers
- Skip input validation
- Hardcode secrets
- Trust external data without validation
- Block event loop with CPU work
- Use `any` type
- Catch errors and ignore them
- String concatenate SQL queries

### ✅ DO:

- Choose framework based on context
- Ask user for preferences when unclear
- Use layered architecture for growing projects
- Validate all inputs at boundaries
- Use environment variables for secrets
- Use parameterized queries
- Profile before optimizing
- Use TypeScript strict mode
- Log errors with context
- Write tests for critical paths

---

## Decision Checklist

Before implementing any Node.js project:

- [ ] Asked user about stack preference?
- [ ] Chosen framework for THIS context? (not just default)
- [ ] Considered deployment target?
- [ ] Planned error handling strategy?
- [ ] Identified validation points?
- [ ] Considered security requirements?
- [ ] Planned database access patterns?
- [ ] Defined logging strategy?

---

> **Remember**: Node.js best practices are about decision-making, not memorizing patterns. Every project deserves fresh consideration based on its requirements.
