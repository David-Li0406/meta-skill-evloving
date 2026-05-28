---
name: fastify-backend-development
description: Use this skill when building high-performance backend APIs with Fastify and TypeScript, including creating routes, handling requests, and implementing validation.
---

# Fastify Backend Development

Fast, low-overhead web framework for Node.js with TypeScript support, ideal for building REST APIs.

## Setup

1. **Install Dependencies**

   ```bash
   npm i fastify @fastify/type-provider-typebox @sinclair/typebox @fastify/env @fastify/cors fastify-plugin
   ```

2. **Initialize Fastify Application**

   ```typescript
   import Fastify from 'fastify'
   import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox'

   const app = Fastify({ logger: true }).withTypeProvider<TypeBoxTypeProvider>()
   ```

## Schema Definition

Define request and response schemas using TypeBox for type safety.

```typescript
import { Type, Static } from '@sinclair/typebox'

// User response schema
export const UserSchema = Type.Object({
  id: Type.String({ format: 'uuid' }),
  name: Type.String({ minLength: 1, maxLength: 100 }),
  email: Type.String({ format: 'email' }),
  createdAt: Type.String({ format: 'date-time' }),
}, { $id: 'UserResponse' })

export type User = Static<typeof UserSchema>

// Create user request schema
export const CreateUserSchema = Type.Object({
  name: Type.String({ minLength: 1, maxLength: 100 }),
  email: Type.String({ format: 'email' }),
}, { $id: 'CreateUserRequest' })

export type CreateUserInput = Static<typeof CreateUserSchema>
```

## Creating Routes

Define routes with full schema validation.

```typescript
const TAGS = ['Users']

app.post('/users', {
  schema: {
    operationId: 'createUser',
    tags: TAGS,
    summary: 'Create a new user',
    description: 'Create a new user account',
    body: CreateUserSchema,
    response: {
      201: UserSchema,
      400: BadRequestErrorResponse,
      401: UnauthorizedErrorResponse,
      500: InternalServerErrorResponse,
    },
  },
}, async (request, reply) => {
  const { name, email } = request.body // fully typed

  const user = await createUser({ name, email })
  return reply.status(201).send(user)
})
```

## Environment Configuration

Use `@fastify/env` for environment variable validation.

```typescript
const schema = {
  type: 'object',
  required: ['PORT', 'API_KEY'],
  properties: {
    PORT: { type: 'string' },
    API_KEY: { type: 'string' },
  },
}

app.register(require('@fastify/env'), {
  schema,
  data: process.env,
})
```

## Common Patterns

- **CORS Support**: Use `@fastify/cors` to enable CORS.
- **Logging**: Use `pino` for logging.
- **Error Handling**: Standardize response format for success and error cases.

## Quick Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Type check
npm run type-check
```