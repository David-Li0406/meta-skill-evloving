# Common Gotchas

Issues frequently encountered in Fastify development and how to resolve them.

## Configuration Access

### Problem: Using process.env Directly

```typescript
// WRONG - bypasses validation, no type safety
const apiKey = process.env.API_KEY
const port = parseInt(process.env.PORT || '3000')
```

### Solution: Always Use fastify.config

```typescript
// CORRECT - validated at startup, type-safe
const apiKey = fastify.config.API_KEY
const port = fastify.config.PORT
```

In services, access config through the fastify instance:

```typescript
export class MyService {
  constructor(private fastify: FastifyInstance) {}

  async doWork() {
    // Access config through fastify, never process.env
    const apiKey = this.fastify.config.API_KEY
  }
}
```

---

## Server Ready State

### Problem: Accessing Config Before Ready

```typescript
// WRONG - config may not be loaded yet
const server = Fastify({ ... })
server.register(app)
console.log(server.config.PORT)  // undefined or error
```

### Solution: Wait for server.ready()

```typescript
// CORRECT
const server = Fastify({ ... })
server.register(app)

const start = async () => {
  await server.ready()  // Wait for plugins to load
  const port = server.config.PORT  // Now safe to access
  await server.listen({ port, host: server.config.HOST })
}

start()
```

---

## Plugin Registration Order

### Problem: Routes Registered Before Dependencies

```typescript
// WRONG - routes can't access services
export const app: FastifyPluginAsync = async (fastify, opts) => {
  await fastify.register(userRoutes)  // Error: userService undefined
  await fastify.register(envPlugin)
  fastify.decorate('userService', new UserService(fastify))
}
```

### Solution: Correct Registration Order

```typescript
// CORRECT - env → services → routes
export const app: FastifyPluginAsync = async (fastify, opts) => {
  // 1. Environment configuration FIRST
  await fastify.register(envPlugin)

  // 2. Initialize services
  const userService = new UserService(fastify)
  fastify.decorate('userService', userService)

  // 3. Register routes LAST
  await fastify.register(userRoutes)
}
```

---

## App Architecture

### Problem: Factory Function Instead of Plugin

```typescript
// WRONG - harder to compose and test
export async function buildApp() {
  const fastify = Fastify({ ... })
  // setup...
  return fastify
}
```

### Solution: Use FastifyPluginAsync Pattern

```typescript
// CORRECT - composable plugin pattern
export const app: FastifyPluginAsync = async (fastify, opts) => {
  // Plugin logic here
}

export default fp(app, '5.x')

// In index.ts
const server = Fastify({ logger: { ... } })
server.register(app)
```

---

## Route Prefix Consistency

### Problem: Inconsistent API Paths

```typescript
// WRONG - mixing prefixed and non-prefixed
fastify.get('/health', ...)           // /health
fastify.get('/api/users', ...)        // /api/users
await fastify.register(routes, { prefix: '/api' })  // Confusing
```

### Solution: Consistent Prefix Strategy

```typescript
// CORRECT - all API routes under /api
await fastify.register(healthRoutes, { prefix: '/api/health' })
await fastify.register(userRoutes, { prefix: '/api/users' })
await fastify.register(orderRoutes, { prefix: '/api/orders' })
```

---

## Path Handling

### Problem: Inconsistent Path Normalization

```typescript
// WRONG - duplicated path logic, inconsistent handling
// In route A:
const fullPath = library ? `${library}/${path}` : path

// In route B:
const fullPath = library + '/' + path

// In route C:
const fullPath = [library, path].filter(Boolean).join('/')
```

### Solution: Centralized Path Utilities

```typescript
// src/utils/path-utils.ts
import path from 'path'

export function trimSlashes(p: string): string {
  return p.replace(/^\/+|\/+$/g, '')
}

export function normalizePath(basePath: string | undefined, filePath: string): string {
  const normalizedBase = basePath && basePath !== '/' ? trimSlashes(basePath) : ''
  const normalizedFile = trimSlashes(filePath)

  if (!normalizedBase) {
    return normalizedFile
  }

  return path.join(normalizedBase, normalizedFile)
}

// Use everywhere:
import { normalizePath } from '../utils/path-utils'
const fullPath = normalizePath(library, path)
```

---

## Object Enumeration

### Problem: Object.entries() Missing Properties

```typescript
// WRONG - may miss properties on some objects
const children = await someLibrary.getChildren()
for (const [name, child] of Object.entries(children)) {
  // May not enumerate all properties
}
```

### Solution: Use for...in for External Objects

```typescript
// CORRECT - enumerates all enumerable properties
const children = await someLibrary.getChildren()
for (const name in children) {
  const child = children[name]
  // Processes all properties
}
```

---

## Schema Drift

### Problem: Swagger Schema Out of Sync

```typescript
// Schema says one thing...
schema: {
  response: {
    200: {
      properties: {
        id: { type: 'string' },
        name: { type: 'string' }
      }
    }
  }
}

// ...but implementation returns something else
return {
  id: item.id,
  name: item.name,
  createdAt: item.createdAt  // Not in schema!
}
```

### Solution: Keep Schemas in Sync

1. Define response types that match schemas
2. Use TypeScript to enforce consistency
3. Test actual responses against schemas

```typescript
interface ItemResponse {
  id: string
  name: string
  createdAt: string
}

// Schema matches the type
schema: {
  response: {
    200: {
      properties: {
        id: { type: 'string' },
        name: { type: 'string' },
        createdAt: { type: 'string' }
      }
    }
  }
}

// Implementation returns typed response
const response: ItemResponse = {
  id: item.id,
  name: item.name,
  createdAt: item.createdAt.toISOString()
}
return response
```

---

## Logging Noise

### Problem: Health Checks Flooding Logs

```typescript
// Every health check probe logs:
// [12:00:01] incoming request GET /api/health
// [12:00:01] request completed 200
// [12:00:02] incoming request GET /api/health
// [12:00:02] request completed 200
// ... repeated every second
```

### Solution: Filter Health Checks from Logging

```typescript
fastify.addHook('onRequest', (req, reply, done) => {
  // Skip logging for health checks
  if (req.raw.url?.startsWith('/api/health')) {
    done()
    return
  }

  req.log.info({ /* request details */ }, 'incoming request')
  done()
})

fastify.addHook('onResponse', (req, reply, done) => {
  if (req.raw.url?.startsWith('/api/health')) {
    done()
    return
  }

  req.log.info({ /* response details */ }, 'request completed')
  done()
})
```

---

## Error Handling

### Problem: Unhandled Errors Crash Server

```typescript
// WRONG - unhandled promise rejection
fastify.get('/data', async (request, reply) => {
  const data = await externalApi.fetch()  // May throw
  return data
})
```

### Solution: Proper Error Handling

```typescript
// CORRECT - handle errors gracefully
fastify.get('/data', async (request, reply) => {
  try {
    const data = await externalApi.fetch()
    return { success: true, data }
  } catch (error) {
    request.log.error(error, 'Failed to fetch data')
    reply.code(500)
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    }
  }
})
```

---

## Service Dependencies

### Problem: Circular Service Dependencies

```typescript
// WRONG - circular dependency
class ServiceA {
  constructor(private serviceB: ServiceB) {}
}

class ServiceB {
  constructor(private serviceA: ServiceA) {}
}

// Can't instantiate either first
```

### Solution: Use Setter Injection

```typescript
// CORRECT - setter injection breaks the cycle
class ServiceA {
  private serviceB: ServiceB | null = null

  constructor(private fastify: FastifyInstance) {}

  setServiceB(serviceB: ServiceB) {
    this.serviceB = serviceB
  }
}

class ServiceB {
  constructor(private fastify: FastifyInstance) {}
}

// In app.ts
const serviceA = new ServiceA(fastify)
const serviceB = new ServiceB(fastify)
serviceA.setServiceB(serviceB)
```

---

## TypeScript Declaration Merging

### Problem: TypeScript Doesn't Know About Decorations

```typescript
// Error: Property 'userService' does not exist on type 'FastifyInstance'
const user = await fastify.userService.findById(id)
```

### Solution: Declare Module Augmentation

```typescript
// At the top of app.ts or in a types file
declare module 'fastify' {
  interface FastifyInstance {
    userService: UserService
    config: {
      PORT: number
      HOST: string
      // ... all config properties
    }
  }
}
```

---

## Testing Considerations

### Problem: Testing Routes Without Full Server

```typescript
// WRONG - starts actual server
const server = await buildApp()
await server.listen({ port: 3000 })
// test...
await server.close()
```

### Solution: Use inject() for Testing

```typescript
// CORRECT - no actual server needed
import { app } from './app'

test('GET /api/health returns healthy', async () => {
  const fastify = Fastify()
  await fastify.register(app)
  await fastify.ready()

  const response = await fastify.inject({
    method: 'GET',
    url: '/api/health'
  })

  expect(response.statusCode).toBe(200)
  expect(JSON.parse(response.body)).toMatchObject({
    status: 'healthy'
  })
})
```
