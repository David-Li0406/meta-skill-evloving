# Authentication Patterns

Patterns for implementing JWT authentication and authorization in Fastify backends.

## Dependencies

```bash
npm install jsonwebtoken
npm install -D @types/jsonwebtoken
```

## Environment Configuration

Add auth-related config to your env plugin:

```typescript
// src/plugins/env.ts
const schema = {
  type: 'object',
  required: ['JWT_SECRET'],
  properties: {
    JWT_SECRET: {
      type: 'string',
      minLength: 32,
      description: 'Secret key for JWT signing'
    },
    JWT_ISSUER: {
      type: 'string',
      default: 'my-app'
    },
    JWT_AUDIENCE: {
      type: 'string',
      default: 'my-app-users'
    },
    JWT_EXPIRES_IN: {
      type: 'string',
      default: '24h'
    }
  }
}

declare module 'fastify' {
  interface FastifyInstance {
    config: {
      JWT_SECRET: string
      JWT_ISSUER: string
      JWT_AUDIENCE: string
      JWT_EXPIRES_IN: string
      // ... other config
    }
  }
}
```

## Auth Middleware

### Bearer Token Extraction

```typescript
// src/middleware/auth.ts
import { FastifyRequest } from 'fastify'

function extractBearerToken(request: FastifyRequest): string | null {
  const authHeader = request.headers.authorization
  if (!authHeader) return null

  const parts = authHeader.split(' ')
  if (parts.length !== 2 || parts[0].toLowerCase() !== 'bearer') {
    return null
  }
  return parts[1]
}
```

### JWT Payload Type

```typescript
export interface JWTPayload {
  sub: string           // User ID
  email: string
  groups: string[]      // Roles/permissions
  iat: number          // Issued at
  exp: number          // Expiration
}

// Extend FastifyRequest to include user
declare module 'fastify' {
  interface FastifyRequest {
    user?: JWTPayload
  }
}
```

### Required Authentication

Use when endpoint requires a valid token:

```typescript
import jwt from 'jsonwebtoken'
import { FastifyRequest, FastifyReply } from 'fastify'

export async function verifyJWT(
  request: FastifyRequest,
  reply: FastifyReply
): Promise<void> {
  const token = extractBearerToken(request)

  if (!token) {
    reply.code(401).send({
      success: false,
      error: 'Authentication required'
    })
    return
  }

  try {
    // Access config through request.server, not process.env
    const config = request.server.config
    const decoded = jwt.verify(token, config.JWT_SECRET, {
      issuer: config.JWT_ISSUER,
      audience: config.JWT_AUDIENCE
    }) as JWTPayload

    request.user = decoded
  } catch (error) {
    request.log.debug({ error }, 'JWT verification failed')
    reply.code(401).send({
      success: false,
      error: 'Invalid or expired token'
    })
  }
}
```

### Optional Authentication

Use when endpoint works with or without authentication:

```typescript
export async function optionalAuth(
  request: FastifyRequest,
  reply: FastifyReply
): Promise<void> {
  const token = extractBearerToken(request)

  if (!token) {
    // No token is fine, continue without user
    return
  }

  try {
    const config = request.server.config
    const decoded = jwt.verify(token, config.JWT_SECRET, {
      issuer: config.JWT_ISSUER,
      audience: config.JWT_AUDIENCE
    }) as JWTPayload

    request.user = decoded
  } catch (error) {
    // Invalid token with optional auth - log but continue
    request.log.debug({ error }, 'Optional auth token invalid, continuing without user')
  }
}
```

### Group-Based Authorization

Require specific groups/roles:

```typescript
export function requireGroups(requiredGroups: string[]) {
  return async function (
    request: FastifyRequest,
    reply: FastifyReply
  ): Promise<void> {
    // First verify the JWT
    await verifyJWT(request, reply)

    // If verifyJWT sent a response, stop
    if (reply.sent) return

    // Check if user has at least one required group
    const hasRequiredGroup = requiredGroups.some(
      group => request.user!.groups.includes(group)
    )

    if (!hasRequiredGroup) {
      reply.code(403).send({
        success: false,
        error: 'Insufficient permissions',
        required: requiredGroups,
        actual: request.user!.groups
      })
      return
    }
  }
}
```

## Using Auth in Routes

### Protected Route

```typescript
import { verifyJWT } from '../middleware/auth'

const routes: FastifyPluginAsync = async (fastify, opts) => {
  // Single route protection
  fastify.get('/profile', {
    preHandler: verifyJWT
  }, async (request, reply) => {
    // request.user is guaranteed to exist
    const userId = request.user!.sub
    return { success: true, data: { userId } }
  })
}
```

### Route with Role Requirement

```typescript
import { requireGroups } from '../middleware/auth'

const adminRoutes: FastifyPluginAsync = async (fastify, opts) => {
  fastify.delete<{ Params: { id: string } }>('/users/:id', {
    preHandler: requireGroups(['admin'])
  }, async (request, reply) => {
    // Only admins can reach here
    const { id } = request.params
    await fastify.userService.delete(id)
    return { success: true }
  })
}
```

### Optional Auth Route

```typescript
import { optionalAuth } from '../middleware/auth'

const routes: FastifyPluginAsync = async (fastify, opts) => {
  fastify.get('/items', {
    preHandler: optionalAuth
  }, async (request, reply) => {
    const items = await fastify.itemService.findAll()

    // Customize response based on auth status
    if (request.user) {
      // Authenticated users see more details
      return { success: true, data: items }
    } else {
      // Anonymous users see limited data
      return { success: true, data: items.map(i => ({ id: i.id, name: i.name })) }
    }
  })
}
```

## Global Auth Hook

Apply optional auth globally, then require it on specific routes:

```typescript
// In app.ts
export const app: FastifyPluginAsync = async (fastify, opts) => {
  await fastify.register(envPlugin)

  // Global optional auth (skips health checks)
  fastify.addHook('onRequest', async (request, reply) => {
    if (request.raw.url?.startsWith('/api/health')) {
      return
    }
    await optionalAuth(request, reply)
  })

  // Register routes - they can check request.user or use preHandler for required auth
  await fastify.register(publicRoutes, { prefix: '/api' })
  await fastify.register(protectedRoutes, { prefix: '/api' })
}
```

## Token Generation

Service for creating tokens:

```typescript
// src/services/auth-service.ts
import jwt from 'jsonwebtoken'
import bcrypt from 'bcrypt'
import { FastifyInstance } from 'fastify'
import { JWTPayload } from '../middleware/auth'

export class AuthService {
  constructor(private fastify: FastifyInstance) {}

  generateToken(user: { id: string; email: string; groups: string[] }): string {
    const config = this.fastify.config

    const payload: Omit<JWTPayload, 'iat' | 'exp'> = {
      sub: user.id,
      email: user.email,
      groups: user.groups
    }

    return jwt.sign(payload, config.JWT_SECRET, {
      issuer: config.JWT_ISSUER,
      audience: config.JWT_AUDIENCE,
      expiresIn: config.JWT_EXPIRES_IN
    })
  }

  async validateCredentials(email: string, password: string): Promise<User | null> {
    // Note: Requires userService to be decorated on fastify instance before AuthService is used
    const user = await this.fastify.userService.findByEmail(email)
    if (!user) return null

    const valid = await this.comparePassword(password, user.passwordHash)
    if (!valid) return null

    return user
  }

  private async comparePassword(plain: string, hash: string): Promise<boolean> {
    return bcrypt.compare(plain, hash)
  }
}
```

## Login Route

```typescript
const authRoutes: FastifyPluginAsync = async (fastify, opts) => {
  fastify.post<{ Body: { email: string; password: string } }>('/login', {
    schema: {
      body: {
        type: 'object',
        required: ['email', 'password'],
        properties: {
          email: { type: 'string', format: 'email' },
          password: { type: 'string', minLength: 1 }
        }
      }
    }
  }, async (request, reply) => {
    const { email, password } = request.body

    const user = await fastify.authService.validateCredentials(email, password)

    if (!user) {
      reply.code(401)
      return { success: false, error: 'Invalid credentials' }
    }

    const token = fastify.authService.generateToken({
      id: user.id,
      email: user.email,
      groups: user.groups
    })

    return {
      success: true,
      data: {
        token,
        user: { id: user.id, email: user.email }
      }
    }
  })
}
```

## Security Considerations

1. **Never log tokens**: Ensure JWT tokens are not logged in request/response hooks
2. **Use strong secrets**: JWT_SECRET should be at least 32 characters, randomly generated
3. **Set appropriate expiration**: Balance security vs user experience
4. **Validate issuer/audience**: Prevents token reuse across different applications
5. **Use HTTPS**: Always require HTTPS in production to protect tokens in transit
