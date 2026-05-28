---
name: backend-fastify-api-development
description: Use this skill when building backend APIs with Fastify and TypeScript, including creating routes, handling requests, implementing validation, and configuring environment variables.
---

# Backend Fastify API Development

High-performance Node.js backend stack using Fastify and TypeScript.

## Setup

### Environment Setup

Use [asdf](https://asdf-vm.com/) to manage Node.js versions:

```bash
# Install Node.js plugin (one-time)
asdf plugin add nodejs

# Set project Node.js version
asdf set nodejs latest:22
```

This creates a `.tool-versions` file in the project root that ensures consistent Node.js versions across the team.

### Installation

```bash
npm install fastify @fastify/type-provider-typebox @sinclair/typebox @fastify/env @fastify/cors fastify-plugin
```

### Basic Fastify Setup

```typescript
import Fastify from 'fastify'
import { TypeBoxTypeProvider } from '@fastify/type-provider-typebox'

const app = Fastify({ logger: true }).withTypeProvider<TypeBoxTypeProvider>()
```

## Schema Definition

Define request and response schemas using TypeBox:

```typescript
import { Type, Static } from '@sinclair/typebox'

// Example User Schema
export const UserSchema = Type.Object({
  id: Type.String({ format: 'uuid' }),
  name: Type.String({ minLength: 1, maxLength: 100 }),
  email: Type.String({ format: 'email' }),
  createdAt: Type.String({ format: 'date-time' }),
}, { $id: 'UserResponse' })

export type User = Static<typeof UserSchema>
```

## Route Definition

Create routes with schema validation:

```typescript
app.post('/users', {
  schema: {
    body: CreateUserSchema,
    response: {
      201: UserSchema,
      400: BadRequestErrorResponse,
    },
  },
}, async (request, reply) => {
  const { name, email } = request.body
  const user = await createUser({ name, email })
  return reply.status(201).send(user)
})
```

## Error Handling

Implement a global error handler:

```typescript
app.setErrorHandler((error, request, reply) => {
  if (error.code === 'FST_ERR_VALIDATION') {
    return reply.status(400).send({
      type: 'BAD_REQUEST',
      status: 400,
      title: 'Validation Error',
      detail: error.message,
      instance: request.url,
      traceId: request.id,
    })
  }
  // Handle other errors
  return reply.status(500).send({
    type: 'INTERNAL_SERVER_ERROR',
    status: 500,
    title: 'Internal Server Error',
    detail: 'Something went wrong',
    instance: request.url,
    traceId: request.id,
  })
})
```

## Configuration Access

Access configuration through `fastify.config`:

```typescript
const port = fastify.config.PORT
const apiKey = fastify.config.API_KEY
```

## Common Patterns

### Plugin Pattern

```typescript
import fp from 'fastify-plugin'

export default fp(async (fastify, opts) => {
  fastify.decorate('myService', new MyService(fastify))
}, '5.x')
```

### Service Pattern

```typescript
export class MyService {
  constructor(private fastify: FastifyInstance) {}
  async doWork() {
    const apiKey = this.fastify.config.API_KEY
    this.fastify.log.info('Service method called')
  }
}
```

## Project Structure

```
backend/
├── src/
│   ├── plugins/          # Fastify plugins (env, auth, etc.)
│   ├── routes/           # HTTP route handlers
│   ├── services/         # Business logic classes
│   ├── utils/            # Shared utilities
│   ├── app.ts            # Plugin registration & setup
│   └── index.ts          # Server entry point
├── package.json
├── tsconfig.json
├── .env.example
└── .gitignore
```

## Quick Reference Commands

```bash
# Dev server with watch mode
npm run dev

# Build for production
npm run build

# Run production build
npm start

# Type check
npm run type-check
```

## Guidelines

1. Always define schemas with `Type.Object({ ... })`.
2. Add `$id` to all schemas for OpenAPI generation and reusability.
3. Use `preHandler` for protected routes and implement role-based permission checks.
4. Use standardized error responses across all routes.
5. Ensure to validate environment variables using `@fastify/env`.