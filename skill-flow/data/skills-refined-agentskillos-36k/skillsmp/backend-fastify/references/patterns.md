# Development Patterns

Patterns for building features in Fastify + TypeScript backends.

## Typed Route Handlers

Use generic type parameters for type-safe request handling:

```typescript
interface ReadQuerystring {
  path: string
  ref?: string
  metadataOnly?: boolean
}

fastify.get<{ Querystring: ReadQuerystring }>('/api/read', {
  schema: {
    querystring: {
      type: 'object',
      required: ['path'],
      properties: {
        path: { type: 'string', description: 'File path to read' },
        ref: { type: 'string', default: 'main' },
        metadataOnly: { type: 'boolean', default: false }
      }
    }
  }
}, async (request, reply) => {
  const { path, ref = 'main', metadataOnly } = request.query
  // TypeScript knows the types
})
```

### POST with Body Types

```typescript
interface CreateBody {
  name: string
  content: string
  tags?: string[]
}

fastify.post<{ Body: CreateBody }>('/api/items', {
  schema: {
    body: {
      type: 'object',
      required: ['name', 'content'],
      properties: {
        name: { type: 'string', minLength: 1 },
        content: { type: 'string' },
        tags: { type: 'array', items: { type: 'string' } }
      }
    }
  }
}, async (request, reply) => {
  const { name, content, tags = [] } = request.body
})
```

### Route with Path Parameters

```typescript
interface ItemParams {
  id: string
}

fastify.get<{ Params: ItemParams }>('/api/items/:id', async (request, reply) => {
  const { id } = request.params
})
```

## JSON Schema Validation

Fastify validates requests against JSON Schema automatically:

```typescript
const routes: FastifyPluginAsync = async (fastify, opts) => {
  fastify.post('/api/users', {
    schema: {
      body: {
        type: 'object',
        required: ['email', 'password'],
        properties: {
          email: { type: 'string', format: 'email' },
          password: { type: 'string', minLength: 8 },
          role: { type: 'string', enum: ['user', 'admin'], default: 'user' }
        }
      },
      response: {
        201: {
          type: 'object',
          properties: {
            success: { type: 'boolean' },
            data: {
              type: 'object',
              properties: {
                id: { type: 'string' },
                email: { type: 'string' }
              }
            }
          }
        },
        400: {
          type: 'object',
          properties: {
            success: { type: 'boolean' },
            error: { type: 'string' }
          }
        }
      }
    }
  }, async (request, reply) => {
    // request.body is validated before handler runs
  })
}
```

## Service Architecture

### Single-Responsibility Services

Each service handles one domain:

```typescript
// src/services/user-service.ts
import { FastifyInstance } from 'fastify'

export class UserService {
  constructor(private fastify: FastifyInstance) {}

  async findById(id: string) {
    // Access config through fastify instance, not process.env
    const dbUrl = this.fastify.config.DATABASE_URL
    this.fastify.log.debug({ id }, 'Finding user by ID')
    // ... implementation
  }

  async create(email: string, password: string) {
    // ... implementation
  }

  async updateRole(id: string, role: string) {
    // ... implementation
  }
}
```

### Service Registration in app.ts

```typescript
import { FastifyPluginAsync } from 'fastify'
import fp from 'fastify-plugin'
import { UserService } from './services/user-service'
import { EmailService } from './services/email-service'

declare module 'fastify' {
  interface FastifyInstance {
    userService: UserService
    emailService: EmailService
  }
}

export const app: FastifyPluginAsync = async (fastify, opts) => {
  // 1. Register environment configuration FIRST
  await fastify.register(envPlugin)

  // 2. Initialize services (order matters if they depend on each other)
  const userService = new UserService(fastify)
  const emailService = new EmailService(fastify)

  // 3. Decorate fastify instance
  fastify.decorate('userService', userService)
  fastify.decorate('emailService', emailService)

  // 4. Register routes (they can now access services)
  await fastify.register(userRoutes, { prefix: '/api/users' })
}

export default fp(app, '5.x')
```

### Inter-Service Communication

When services need to communicate:

```typescript
export class OrderService {
  private userService: UserService | null = null

  constructor(private fastify: FastifyInstance) {}

  setUserService(userService: UserService) {
    this.userService = userService
  }

  async createOrder(userId: string, items: Item[]) {
    if (!this.userService) {
      throw new Error('UserService not configured')
    }
    const user = await this.userService.findById(userId)
    // ... create order
  }
}

// In app.ts
const userService = new UserService(fastify)
const orderService = new OrderService(fastify)
orderService.setUserService(userService)
```

## Structured Logging

### Request/Response Logging Hooks

```typescript
// In app.ts
fastify.addHook('onRequest', (req, reply, done) => {
  // Skip health checks to reduce log noise
  if (req.raw.url?.startsWith('/api/health')) {
    done()
    return
  }

  req.log.info({
    reqId: req.id,
    req: {
      method: req.raw.method,
      url: req.raw.url,
      host: req.headers.host,
      remoteAddress: req.ip
    }
  }, 'incoming request')
  done()
})

fastify.addHook('onResponse', (req, reply, done) => {
  if (req.raw.url?.startsWith('/api/health')) {
    done()
    return
  }

  req.log.info({
    reqId: req.id,
    res: { statusCode: reply.statusCode },
    responseTime: reply.elapsedTime
  }, 'request completed')
  done()
})
```

### Logging in Services

```typescript
export class PaymentService {
  constructor(private fastify: FastifyInstance) {}

  async processPayment(orderId: string, amount: number) {
    this.fastify.log.info({ orderId, amount }, 'Processing payment')

    try {
      // ... process
      this.fastify.log.info({ orderId }, 'Payment successful')
    } catch (error) {
      this.fastify.log.error({ orderId, error }, 'Payment failed')
      throw error
    }
  }
}
```

## Caching Patterns

### In-Memory Caching

```typescript
export class ConfigService {
  private cache: Map<string, { value: unknown; expires: number }> = new Map()
  private readonly TTL = 5 * 60 * 1000 // 5 minutes

  constructor(private fastify: FastifyInstance) {}

  async get<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
    const cached = this.cache.get(key)

    if (cached && cached.expires > Date.now()) {
      this.fastify.log.debug({ key }, 'Cache hit')
      return cached.value as T
    }

    this.fastify.log.debug({ key }, 'Cache miss, fetching')
    const value = await fetcher()
    this.cache.set(key, { value, expires: Date.now() + this.TTL })
    return value
  }

  invalidate(key: string) {
    this.cache.delete(key)
  }

  clear() {
    this.cache.clear()
  }
}
```

### Query Result Caching

```typescript
export class DataService {
  private routesCache: Route[] | null = null

  constructor(private fastify: FastifyInstance) {}

  async getRoutes(): Promise<Route[]> {
    if (this.routesCache) {
      return this.routesCache
    }

    const routes = await this.fetchRoutesFromDatabase()
    this.routesCache = routes
    return routes
  }

  invalidateRoutesCache() {
    this.routesCache = null
  }
}
```

## Path Utilities

Centralize path handling to avoid inconsistencies:

```typescript
// src/utils/path-utils.ts
import path from 'path'

export function trimSlashes(p: string): string {
  return p.replace(/^\/+|\/+$/g, '')
}

export function normalizeLibraryPath(library: string | undefined): string {
  if (!library || library === '/') {
    return ''
  }
  return trimSlashes(library)
}

export function buildFullPath(library: string | undefined, filePath: string): string {
  const normalizedLibrary = normalizeLibraryPath(library)
  const normalizedPath = trimSlashes(filePath)

  if (!normalizedLibrary) {
    return normalizedPath
  }

  return path.join(normalizedLibrary, normalizedPath)
}
```

## Route Organization

### Route Module Pattern

```typescript
// src/routes/users.ts
import { FastifyPluginAsync } from 'fastify'

const userRoutes: FastifyPluginAsync = async (fastify, opts) => {
  const userService = fastify.userService

  fastify.get('/', async (request, reply) => {
    const users = await userService.findAll()
    return { success: true, data: users }
  })

  fastify.get<{ Params: { id: string } }>('/:id', async (request, reply) => {
    const { id } = request.params
    const user = await userService.findById(id)
    if (!user) {
      reply.code(404)
      return { success: false, error: 'User not found' }
    }
    return { success: true, data: user }
  })

  fastify.post<{ Body: { email: string; password: string } }>('/', async (request, reply) => {
    const { email, password } = request.body
    const user = await userService.create(email, password)
    reply.code(201)
    return { success: true, data: user }
  })
}

export default userRoutes
```

### Route Registration with Prefixes

```typescript
// In app.ts
await fastify.register(userRoutes, { prefix: '/api/users' })
await fastify.register(orderRoutes, { prefix: '/api/orders' })
await fastify.register(healthRoutes, { prefix: '/api/health' })
```

## Package Management

Always use npm commands to manage dependencies:

- Always use `npm install <package-name>` to add dependencies
- Never manually edit `package.json` to add packages
- This ensures the latest compatible versions are installed and `package-lock.json` stays in sync

### Adding Dependencies

```bash
# Runtime dependencies
npm install fastify-plugin @fastify/cors pino

# Development dependencies
npm install -D @types/node typescript
```

### Why This Matters

- `npm install` automatically resolves to the latest compatible version
- Manual edits can introduce version mismatches
- `package-lock.json` won't be properly updated with manual edits
- Dependency tree conflicts are harder to debug after manual edits
