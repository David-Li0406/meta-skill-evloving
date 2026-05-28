---
id: bun-runtime
name: "Bun Runtime"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Bun Runtime

## Overview

Bun is a modern JavaScript/TypeScript runtime designed for speed, featuring a built-in bundler, test runner, and package manager. This methodology covers project setup, Bun-specific APIs, and best practices for building high-performance applications.

## When to Use

- New TypeScript projects requiring maximum performance
- Development tooling (bundling, testing)
- APIs where startup time matters
- Replacing Node.js for speed improvements
- Monorepo workspaces with fast installs

## Key Principles

1. **Native TypeScript** - No transpilation needed
2. **Drop-in replacement** - Node.js API compatibility
3. **All-in-one tooling** - Runtime, bundler, test runner, package manager
4. **Performance first** - Optimized for speed
5. **Web standards** - Fetch, WebSocket, Workers built-in

## Best Practices

### Project Setup

```bash
# Initialize new project
bun init

# Project structure created:
# ├── .gitignore
# ├── bun.lockb
# ├── index.ts
# ├── package.json
# ├── README.md
# └── tsconfig.json

# Install dependencies
bun add express zod
bun add -d @types/express typescript

# Run TypeScript directly
bun run index.ts

# Watch mode
bun --watch run index.ts
```

### Configuration

```json
// package.json
{
  "name": "my-bun-app",
  "type": "module",
  "scripts": {
    "dev": "bun --watch run src/index.ts",
    "start": "bun run src/index.ts",
    "test": "bun test",
    "build": "bun build ./src/index.ts --outdir ./dist --target bun"
  },
  "dependencies": {
    "hono": "^4.0.0",
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@types/bun": "^1.0.0"
  }
}
```

```toml
# bunfig.toml
[install]
# Use frozen lockfile in CI
frozen-lockfile = true

[run]
# Bun.serve() for HTTP
bun = true

[test]
# Test configuration
coverage = true
coverageDir = "./coverage"
timeout = 5000

[build]
# Bundle configuration
minify = true
sourcemap = "external"
```

### Native HTTP Server

```typescript
// src/server.ts
const server = Bun.serve({
  port: 3000,

  fetch(request: Request): Response | Promise<Response> {
    const url = new URL(request.url);

    // Routing
    if (url.pathname === '/') {
      return new Response('Hello from Bun!');
    }

    if (url.pathname === '/api/users' && request.method === 'GET') {
      return handleGetUsers(request);
    }

    if (url.pathname === '/api/users' && request.method === 'POST') {
      return handleCreateUser(request);
    }

    // Dynamic routes
    const userMatch = url.pathname.match(/^\/api\/users\/(\w+)$/);
    if (userMatch) {
      const userId = userMatch[1];
      return handleGetUser(request, userId);
    }

    return new Response('Not Found', { status: 404 });
  },

  // WebSocket support
  websocket: {
    open(ws) {
      console.log('WebSocket connected');
    },
    message(ws, message) {
      ws.send(`Echo: ${message}`);
    },
    close(ws) {
      console.log('WebSocket disconnected');
    },
  },

  // Error handling
  error(error: Error): Response {
    console.error(error);
    return new Response('Internal Server Error', { status: 500 });
  },
});

console.log(`Server running at http://localhost:${server.port}`);

// Handler functions
async function handleGetUsers(_request: Request): Promise<Response> {
  const users = await db.users.findMany();
  return Response.json({ data: users });
}

async function handleCreateUser(request: Request): Promise<Response> {
  const body = await request.json();
  const user = await db.users.create({ data: body });
  return Response.json({ data: user }, { status: 201 });
}

async function handleGetUser(_request: Request, id: string): Promise<Response> {
  const user = await db.users.findUnique({ where: { id } });
  if (!user) {
    return Response.json({ error: 'User not found' }, { status: 404 });
  }
  return Response.json({ data: user });
}
```

### Using Hono Framework

```typescript
// src/index.ts
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { jwt } from 'hono/jwt';
import { zValidator } from '@hono/zod-validator';
import { z } from 'zod';

const app = new Hono();

// Middleware
app.use('*', logger());
app.use('/api/*', cors());

// Public routes
app.get('/', (c) => c.json({ message: 'Hello Hono + Bun!' }));

// Auth routes
app.post(
  '/api/auth/login',
  zValidator(
    'json',
    z.object({
      email: z.string().email(),
      password: z.string().min(8),
    })
  ),
  async (c) => {
    const { email, password } = c.req.valid('json');
    const user = await authService.authenticate(email, password);
    const token = await authService.generateToken(user);
    return c.json({ token });
  }
);

// Protected routes
const api = new Hono();
api.use('*', jwt({ secret: Bun.env.JWT_SECRET! }));

api.get('/users', async (c) => {
  const users = await userService.getUsers();
  return c.json({ data: users });
});

api.get('/users/:id', async (c) => {
  const id = c.req.param('id');
  const user = await userService.getUser(id);
  if (!user) {
    return c.json({ error: 'Not found' }, 404);
  }
  return c.json({ data: user });
});

api.post(
  '/users',
  zValidator(
    'json',
    z.object({
      email: z.string().email(),
      name: z.string().min(1),
    })
  ),
  async (c) => {
    const data = c.req.valid('json');
    const user = await userService.createUser(data);
    return c.json({ data: user }, 201);
  }
);

app.route('/api', api);

// Start server
export default {
  port: Bun.env.PORT || 3000,
  fetch: app.fetch,
};
```

### File Operations

```typescript
// File reading
const file = Bun.file('data.json');
const content = await file.text();
const json = await file.json();
const bytes = await file.arrayBuffer();

// File writing
await Bun.write('output.txt', 'Hello World');
await Bun.write('data.json', JSON.stringify({ key: 'value' }));

// Streaming large files
const bigFile = Bun.file('large.csv');
const stream = bigFile.stream();

for await (const chunk of stream) {
  // Process chunk
}

// Copy file
await Bun.write('copy.txt', Bun.file('original.txt'));

// Check file exists
const exists = await Bun.file('path.txt').exists();

// File info
const file = Bun.file('example.txt');
console.log({
  size: file.size,
  type: file.type,
  lastModified: file.lastModified,
});
```

### Environment Variables

```typescript
// Access environment variables
const dbUrl = Bun.env.DATABASE_URL;
const port = Bun.env.PORT || 3000;

// Type-safe environment
interface Env {
  DATABASE_URL: string;
  JWT_SECRET: string;
  PORT?: string;
}

function getEnv(): Env {
  const required = ['DATABASE_URL', 'JWT_SECRET'];

  for (const key of required) {
    if (!Bun.env[key]) {
      throw new Error(`Missing required environment variable: ${key}`);
    }
  }

  return Bun.env as unknown as Env;
}

const env = getEnv();
```

### Testing

```typescript
// tests/users.test.ts
import { describe, it, expect, beforeEach, mock } from 'bun:test';
import { createApp } from '../src/app';

describe('Users API', () => {
  let app: ReturnType<typeof createApp>;

  beforeEach(() => {
    app = createApp();
  });

  it('should return empty users list', async () => {
    const response = await app.request('/api/users');

    expect(response.status).toBe(200);

    const data = await response.json();
    expect(data.users).toEqual([]);
  });

  it('should create a user', async () => {
    const response = await app.request('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'test@example.com',
        name: 'Test User',
      }),
    });

    expect(response.status).toBe(201);

    const data = await response.json();
    expect(data.data.email).toBe('test@example.com');
  });

  it('should validate email format', async () => {
    const response = await app.request('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'invalid',
        name: 'Test',
      }),
    });

    expect(response.status).toBe(400);
  });
});

// Mocking
import { userService } from '../src/services';

describe('with mocks', () => {
  it('should use mock', async () => {
    const mockGetUser = mock(() =>
      Promise.resolve({ id: '1', name: 'Mock User' })
    );

    // Use mock in test
    userService.getUser = mockGetUser;

    const result = await userService.getUser('1');
    expect(result.name).toBe('Mock User');
    expect(mockGetUser).toHaveBeenCalledWith('1');
  });
});
```

### Database with Drizzle

```typescript
// src/db/index.ts
import { drizzle } from 'drizzle-orm/bun-sqlite';
import { Database } from 'bun:sqlite';
import * as schema from './schema';

const sqlite = new Database('app.db');
export const db = drizzle(sqlite, { schema });

// src/db/schema.ts
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';

export const users = sqliteTable('users', {
  id: text('id').primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  createdAt: integer('created_at', { mode: 'timestamp' })
    .notNull()
    .default(sql`CURRENT_TIMESTAMP`),
});

// Usage
import { db } from './db';
import { users } from './db/schema';
import { eq } from 'drizzle-orm';

const allUsers = await db.select().from(users);
const user = await db.select().from(users).where(eq(users.id, '1'));
await db.insert(users).values({ id: '1', email: 'a@b.com', name: 'Test' });
```

### Bundling

```bash
# Build for production
bun build ./src/index.ts --outdir ./dist --target bun --minify

# Build for Node.js
bun build ./src/index.ts --outdir ./dist --target node

# Build for browser
bun build ./src/client.ts --outdir ./dist --target browser

# Multiple entry points
bun build ./src/index.ts ./src/worker.ts --outdir ./dist

# With source maps
bun build ./src/index.ts --outdir ./dist --sourcemap=external
```

## Anti-patterns

### Avoid: Ignoring Node.js Compatibility

```typescript
// BAD - assuming full Node.js compatibility
import { exec } from 'child_process';  // May differ

// GOOD - use Bun-native APIs or check compatibility
import { $ } from 'bun';
await $`ls -la`;

// Or use Bun.spawn
const proc = Bun.spawn(['ls', '-la']);
const output = await new Response(proc.stdout).text();
```

### Avoid: Not Using Native APIs

```typescript
// BAD - using third-party for what Bun provides
import fetch from 'node-fetch';
import bcrypt from 'bcrypt';

// GOOD - use built-in
const response = await fetch(url);  // Built-in

// Bun.password for hashing
const hash = await Bun.password.hash(password);
const valid = await Bun.password.verify(password, hash);
```

## References

- [Bun Documentation](https://bun.sh/docs)
- [Hono Documentation](https://hono.dev/)
- [Drizzle ORM](https://orm.drizzle.team/)
- [Bun GitHub](https://github.com/oven-sh/bun)
