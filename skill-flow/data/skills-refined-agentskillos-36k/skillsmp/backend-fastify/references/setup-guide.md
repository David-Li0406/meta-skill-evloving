# Fastify Backend Setup Guide

This guide documents the complete process for bootstrapping a Fastify backend following the loop project patterns.

## Prerequisites

- Node.js 22.x
- npm

### Node.js Version Management with asdf

Use [asdf](https://asdf-vm.com/) to manage Node.js versions consistently across the team:

```bash
# Install Node.js plugin (one-time setup)
asdf plugin add nodejs

# Set project Node.js version (creates .tool-versions file)
asdf set nodejs latest:22
```

The `.tool-versions` file created by `asdf set` ensures all team members use the same Node.js version.

## Stack Overview

- **Fastify 5.x** - High-performance web framework
- **TypeScript** - Type safety
- **tsx** - Development with watch mode
- **pino-pretty** - Pretty logging for development
- **@fastify/env** - Environment variable validation with JSON Schema
- **@fastify/cors** - CORS support
- **fastify-plugin** - Plugin system

## Step-by-Step Setup

### 1. Initialize Backend Package

```bash
mkdir -p backend && cd backend
npm init -y
```

Update `package.json` scripts:

```json
{
  "name": "backend",
  "version": "1.0.0",
  "description": "Backend API server",
  "main": "dist/index.js",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "type-check": "tsc --noEmit"
  }
}
```

**Commit:** `feat(backend): initialize backend package`

---

### 2. Install Dependencies

```bash
npm install fastify fastify-plugin @fastify/env @fastify/cors pino-pretty
npm install -D typescript tsx @types/node
```

**Commit:** `build(backend): install Fastify and dependencies`

---

### 3. Create TypeScript Configuration

**Create `tsconfig.json`:**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**Create `.gitignore`:**

```
node_modules/
dist/
.env
*.log
.DS_Store
```

**Commit:** `config(backend): add TypeScript configuration and gitignore`

---

### 4. Create Directory Structure

```bash
mkdir -p src/{plugins,routes,services}
```

---

### 5. Create Environment Plugin

**Create `src/plugins/env.ts`:**

```typescript
import fp from 'fastify-plugin'
import fastifyEnv from '@fastify/env'

const schema = {
  type: 'object',
  required: [], // Add required env vars here
  properties: {
    PORT: {
      type: 'number',
      default: 3001
    },
    HOST: {
      type: 'string',
      default: '0.0.0.0'
    },
    NODE_ENV: {
      type: 'string',
      enum: ['development', 'production', 'test'],
      default: 'development'
    },
    LOG_LEVEL: {
      type: 'string',
      enum: ['fatal', 'error', 'warn', 'info', 'debug', 'trace'],
      default: 'info'
    },
  }
}

// TypeScript declaration merging for type safety
declare module 'fastify' {
  interface FastifyInstance {
    config: {
      PORT: number
      HOST: string
      NODE_ENV: 'development' | 'production' | 'test'
      LOG_LEVEL: 'fatal' | 'error' | 'warn' | 'info' | 'debug' | 'trace'
    }
  }
}

export default fp(async (fastify) => {
  await fastify.register(fastifyEnv, {
    schema,
    dotenv: true // Load .env file
  })
})
```

**Create `.env.example`:**

```
PORT=3001
HOST=0.0.0.0
NODE_ENV=development
LOG_LEVEL=info
```

**Key patterns:**

- JSON Schema validation ensures type safety at startup
- Declaration merging provides TypeScript type safety
- `dotenv: true` automatically loads `.env` file
- Failed validation prevents server from starting

**Commit:** `feat(backend): add environment configuration plugin`

---

### 6. Create a Basic Service

Services encapsulate business logic and are decorated onto the Fastify instance.

**Example `src/services/example-service.ts`:**

```typescript
import { FastifyInstance } from 'fastify'

export class ExampleService {
  constructor(private fastify: FastifyInstance) {}

  // Service methods here
  async doSomething() {
    this.fastify.log.info('Service method called')
    return { success: true }
  }
}
```

---

### 7. Create Routes

Routes are Fastify plugins that define HTTP endpoints.

**Create `src/routes/health.ts`:**

```typescript
import { FastifyPluginAsync } from 'fastify'

const healthRoutes: FastifyPluginAsync = async (fastify, opts) => {
  fastify.get('/', async (request, reply) => {
    return {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'backend-service',
      version: '1.0.0',
      environment: fastify.config.NODE_ENV
    }
  })
}

export default healthRoutes
```

**Commit:** `feat(backend): add health check route`

---

### 8. Create app.ts

The app file registers all plugins, services, and routes.

**Create `src/app.ts`:**

```typescript
import { FastifyPluginAsync } from 'fastify'
import fp from 'fastify-plugin'
import cors from '@fastify/cors'

// Import plugins
import envPlugin from './plugins/env'

// Import services
import { ExampleService } from './services/example-service'

// Import routes
import healthRoutes from './routes/health'

// TypeScript declaration merging for services
declare module 'fastify' {
  interface FastifyInstance {
    exampleService: ExampleService
  }
}

export const app: FastifyPluginAsync = async (fastify, opts) => {
  // 1. Register environment configuration FIRST
  await fastify.register(envPlugin)

  // Update log level from config
  fastify.log.level = fastify.config.LOG_LEVEL

  // 2. Initialize services
  const exampleService = new ExampleService(fastify)

  // 3. Decorate fastify instance with services
  fastify.decorate('exampleService', exampleService)

  // 4. Register CORS
  await fastify.register(cors, {
    origin: fastify.config.NODE_ENV === 'production' ? false : true,
    credentials: true
  })

  // 5. Add custom logging hooks (excluding health checks)
  fastify.addHook('onRequest', (req, reply, done) => {
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

  // 6. Register routes with /api prefix
  await fastify.register(healthRoutes, { prefix: '/api/health' })

  // 7. Log successful startup
  fastify.addHook('onReady', async () => {
    fastify.log.info('Backend initialized successfully')
    fastify.log.info(`Environment: ${fastify.config.NODE_ENV}`)
    fastify.log.info('Available API endpoints:')
    fastify.log.info('  GET /api/health - Health check')
  })
}

export default fp(app, '5.x')
```

**Key patterns:**

- Register env plugin FIRST before anything else
- Initialize services and decorate Fastify instance for type-safe access
- Custom logging hooks skip health checks to reduce noise
- Routes registered with `/api` prefix
- `onReady` hook logs startup info

**Commit:** `feat(backend): add app.ts with plugin registration`

---

### 9. Create index.ts Entry Point

**Create `src/index.ts`:**

```typescript
import Fastify from 'fastify'
import { app } from './app'

const server = Fastify({
  logger: {
    level: 'info', // Will be updated after env config loads
    transport: {
      target: 'pino-pretty',
      options: {
        translateTime: 'HH:MM:ss Z',
        ignore: 'pid,hostname'
      }
    }
  },
  disableRequestLogging: true // We use custom hooks in app.ts
})

// Register the app
server.register(app)

// Graceful shutdown handlers
const gracefulShutdown = async (signal: string) => {
  server.log.info(`Received ${signal}, shutting down gracefully`)
  try {
    await server.close()
    server.log.info('Server closed successfully')
    process.exit(0)
  } catch (error) {
    server.log.error(error, 'Error during shutdown')
    process.exit(1)
  }
}

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'))
process.on('SIGINT', () => gracefulShutdown('SIGINT'))

// Start the server
const start = async () => {
  try {
    // Wait for ready so env config is loaded
    await server.ready()

    const port = server.config.PORT
    const host = server.config.HOST

    await server.listen({ port, host })

    server.log.info(`Backend listening at http://${host}:${port}`)
    server.log.info(`Environment: ${server.config.NODE_ENV}`)

    if (server.config.NODE_ENV !== 'production') {
      server.log.info(`API endpoints: http://localhost:${port}/api/`)
      server.log.info(`Health check: http://localhost:${port}/api/health`)
    }
  } catch (err) {
    server.log.error(err)
    process.exit(1)
  }
}

start()
```

**Key patterns:**

- pino-pretty for readable dev logs
- `disableRequestLogging: true` because we use custom hooks
- Graceful shutdown handlers for SIGTERM/SIGINT
- `await server.ready()` before accessing config
- Pretty startup logging

**Commit:** `feat(backend): add index.ts entry point with graceful shutdown`

---

## Running the Backend

```bash
# Development with watch mode
npm run dev

# Build for production
npm run build

# Run production build
npm start

# Type check only
npm run type-check
```

---

## VSCode Debugging

Configure VSCode to debug the backend with breakpoints, variable inspection, and step-through execution.

### Launch Configuration

**Create `.vscode/launch.json`:**

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Backend",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/backend/src/index.ts",
      "cwd": "${workspaceFolder}/backend",
      "runtimeExecutable": "npx",
      "runtimeArgs": ["tsx"],
      "envFile": "${workspaceFolder}/backend/.env",
      "console": "integratedTerminal",
      "sourceMaps": true,
      "skipFiles": ["<node_internals>/**", "**/node_modules/**"]
    }
  ]
}
```

**Key patterns:**

- `runtimeExecutable: "npx"` with `runtimeArgs: ["tsx"]` runs TypeScript directly without pre-compilation
- `envFile` loads environment variables from `.env` file
- `sourceMaps: true` enables breakpoints in TypeScript source files
- `skipFiles` excludes Node internals and dependencies from step-through
- `console: "integratedTerminal"` shows pino-pretty formatted logs

### Using the Debugger

1. **Set breakpoints** - Click the gutter next to line numbers in any `.ts` file
2. **Start debugging** - Press `F5` or select "Debug Backend" from the Run and Debug panel
3. **Debug controls** - Use Continue (F5), Step Over (F10), Step Into (F11), Step Out (Shift+F11)
4. **Inspect variables** - Hover over variables or use the Variables panel

**Commit:** `config(backend): add VSCode debugging configuration`

---

## Vite Proxy Configuration (Frontend Integration)

To proxy frontend API requests to the backend during development:

**Update `vite.config.ts`:**

```typescript
export default defineConfig({
  // ... other config
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:3001",
        changeOrigin: true,
      },
    },
  },
})
```

**Commit:** `config: add Vite proxy for backend API requests`

---

## Key Fastify Patterns

### Service Pattern

```typescript
// 1. Create service class
export class MyService {
  constructor(private fastify: FastifyInstance) {}

  async doWork() {
    // Access config: this.fastify.config.SOME_VAR
    // Access logger: this.fastify.log.info('...')
  }
}

// 2. Declare module augmentation
declare module 'fastify' {
  interface FastifyInstance {
    myService: MyService
  }
}

// 3. Initialize and decorate in app.ts
const myService = new MyService(fastify)
fastify.decorate('myService', myService)

// 4. Use in routes
fastify.get('/example', async (request, reply) => {
  return fastify.myService.doWork()
})
```

### Route Pattern

```typescript
import { FastifyPluginAsync } from 'fastify'

const routes: FastifyPluginAsync = async (fastify, opts) => {
  fastify.get('/', async (request, reply) => {
    return { data: 'example' }
  })

  fastify.post<{ Body: MyType }>('/', async (request, reply) => {
    const { field } = request.body
    return { success: true }
  })
}

export default routes
```

### Plugin Pattern

```typescript
import fp from 'fastify-plugin'

export default fp(async (fastify, opts) => {
  // Plugin logic here
  fastify.decorate('something', value)
}, '5.x') // Fastify version constraint
```

---

## Common Gotchas

### Environment Variables Must Be Declared

All env vars must be in the schema or they won't be accessible. Use `required: []` array for mandatory vars.

### Services Need Declaration Merging

Without declaration merging, TypeScript won't know about decorated services.

### Plugin Registration Order Matters

Always register env plugin first, then services, then routes.

### Use await server.ready()

Access `server.config` only after `await server.ready()` in index.ts.

### Logging Hooks vs Built-in Logging

Use `disableRequestLogging: true` and custom hooks to control what gets logged.

---

## Project Structure

```
backend/
├── src/
│   ├── plugins/
│   │   └── env.ts           # Environment config with validation
│   ├── routes/
│   │   └── health.ts        # HTTP endpoints
│   ├── services/
│   │   └── example-service.ts  # Business logic
│   ├── app.ts               # Plugin registration & setup
│   └── index.ts             # Server entry point
├── dist/                    # Compiled output (gitignored)
├── node_modules/            # Dependencies (gitignored)
├── package.json
├── tsconfig.json
├── .env                     # Environment variables (gitignored)
├── .env.example             # Template for .env
└── .gitignore
```

---

## Additional Resources

- [Fastify Documentation](https://fastify.dev/)
- [Pino Logger](https://getpino.io/)
- [JSON Schema](https://json-schema.org/)
