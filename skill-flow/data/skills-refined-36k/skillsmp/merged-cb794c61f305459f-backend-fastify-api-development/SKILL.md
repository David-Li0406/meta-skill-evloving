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

### Key Imports

```typescript
// Fastify types
import Fastify, { FastifyInstance, FastifyPluginAsync } from 'fastify'
import fp from 'fastify-plugin'

// Common plugins
import fastifyEnv from '@fastify/env'
import cors from '@fastify/cors'
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

## Route Creation

### Basic Route Example

```typescript
const routes: FastifyPluginAsync = async (fastify, opts) => {
  fastify.get('/users', {
    schema: {
      response: {
        200: Type.Array(UserSchema),
      },
    },
  }, async () => {
    return await listUsers()
  })
}

export default routes
```

### Route with Full Schema

```typescript
app.post('/users', {
  schema: {
    operationId: 'createUser',
    summary: 'Create a new user',
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
const globalErrorHandler = (error, request, reply) => {
  if (error.code === 'FST_ERR_VALIDATION') {
    return reply.status(400).send({
      type: 'BAD_REQUEST',
      status: 400,
      title: 'Validation Error',
      detail: error.message,
      instance: request.url,
    })
  }
  request.log.error(error)
  return reply.status(500).send({
    type: 'INTERNAL_SERVER_ERROR',
    status: 500,
    title: 'Internal Server Error',
    detail: 'Something went wrong',
  })
}

app.setErrorHandler(globalErrorHandler)
```

## Configuration Access

Always access configuration through `fastify.config`, never `process.env` directly:

```typescript
const port = fastify.config.PORT
const apiKey = fastify.config.API_KEY
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

## Common Guidelines

1. Define schemas with `Type.Object({ ... })` for full JSON Schema.
2. Use `$id` for all schemas for OpenAPI generation and reusability.
3. Add `operationId`, `tags`, and `summary` to all routes for documentation.
4. Use standardized error responses across all routes.
5. Use Fastify plugins with `fp()` for dependency injection.

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