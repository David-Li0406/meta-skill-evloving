---
name: backend-fastify
description: Backend development using Fastify + TypeScript. Use when creating new backend APIs, adding routes, implementing services, working with plugins, or configuring environment variables.
---

# Backend Fastify Stack

High-performance Node.js backend stack:

- **Fastify 5.x** - Web framework
- **TypeScript** - Type safety
- **tsx** - Development with watch mode
- **pino-pretty** - Pretty logging for development
- **@fastify/env** - Environment variable validation with JSON Schema
- **@fastify/cors** - CORS support
- **fastify-plugin** - Plugin system

## Environment Setup

Use [asdf](https://asdf-vm.com/) to manage Node.js versions:

```bash
# Install Node.js plugin (one-time)
asdf plugin add nodejs

# Set project Node.js version
asdf set nodejs latest:22
```

This creates a `.tool-versions` file in the project root that ensures consistent Node.js versions across the team.

## Reference Files

| File | When to Use |
|------|-------------|
| [setup-guide.md](references/setup-guide.md) | Starting a new backend project from scratch |
| [patterns.md](references/patterns.md) | Implementing routes, services, schema validation |
| [authentication.md](references/authentication.md) | Adding JWT auth, authorization, protected routes |
| [api-design.md](references/api-design.md) | Swagger/OpenAPI integration, response format, errors |
| [mcp-integration.md](references/mcp-integration.md) | Integrating MCP server for AI agent access |
| [gotchas.md](references/gotchas.md) | Debugging issues, common mistakes and fixes |

## Quick Reference

### Commands

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

### Key Imports

```typescript
// Fastify types
import Fastify, { FastifyInstance, FastifyPluginAsync } from 'fastify'
import fp from 'fastify-plugin'

// Common plugins
import fastifyEnv from '@fastify/env'
import cors from '@fastify/cors'
```

### Configuration Access

Always access configuration through `fastify.config`, never `process.env` directly:

```typescript
// CORRECT - type-safe, validated at startup
const port = fastify.config.PORT
const apiKey = fastify.config.API_KEY

// WRONG - no validation, no type safety
const port = process.env.PORT  // Don't do this
```

### Response Format

```typescript
// Standard response structure
{
  success: boolean
  data?: T
  error?: string
  metadata?: { timestamp: Date }
}
```

### Plugin Pattern

```typescript
import fp from 'fastify-plugin'

export default fp(async (fastify, opts) => {
  // Plugin logic here
  fastify.decorate('something', value)
}, '5.x')
```

### Route Pattern

```typescript
import { FastifyPluginAsync } from 'fastify'

const routes: FastifyPluginAsync = async (fastify, opts) => {
  fastify.get('/', async (request, reply) => {
    return { success: true, data: 'example' }
  })
}

export default routes
```

### Service Pattern

```typescript
// 1. Create service class
export class MyService {
  constructor(private fastify: FastifyInstance) {}

  async doWork() {
    // Access config through fastify instance
    const apiKey = this.fastify.config.API_KEY
    this.fastify.log.info('Service method called')
  }
}

// 2. Declare module augmentation
declare module 'fastify' {
  interface FastifyInstance {
    myService: MyService
  }
}

// 3. Initialize and decorate in app.ts
fastify.decorate('myService', new MyService(fastify))
```

### Project Structure

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

### Common Gotchas

- **Plugin order matters**: Register env plugin first, then services, then routes
- **Config access**: Use `fastify.config.VAR` not `process.env.VAR`
- **Server ready**: Call `await server.ready()` before accessing config in index.ts
- **Path normalization**: Centralize path utilities, handle root '/' as special case
- **Package management**: Use `npm install <pkg>` not manual `package.json` edits
