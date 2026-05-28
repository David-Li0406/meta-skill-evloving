---
name: nodejs-backend-development
description: Use this skill when building production-ready Node.js backend services with Express or Fastify, implementing best practices for middleware, error handling, and database integration.
---

# Skill body

## When to Use

- Creating backend API services (REST or GraphQL)
- Setting up Express or Fastify servers
- Implementing authentication and authorization
- Designing scalable backend architectures
- Integrating databases (SQL and NoSQL)
- Building real-time applications with WebSockets
- Implementing background job processing

## Project Structure

```
backend/
├── src/
│   ├── index.js           # Entry point, server setup
│   ├── config/
│   │   ├── index.js       # Configuration loader
│   │   └── database.js    # Database configuration
│   ├── api/
│   │   ├── routes.js      # Route definitions
│   │   ├── middleware/    # Express middleware
│   │   │   ├── auth.js
│   │   │   ├── validate.js
│   │   │   └── error.js
│   │   └── handlers/      # Route handlers
│   │       ├── users.js
│   │       └── products.js
│   ├── services/          # Business logic
│   │   ├── user.js
│   │   └── product.js
│   ├── db/
│   │   ├── client.js      # Database client
│   │   ├── queries/       # SQL queries
│   │   └── migrations/    # Database migrations
│   └── lib/               # Shared utilities
│       ├── logger.js
│       └── errors.js
├── test/
│   ├── api/
│   └── services/
├── .env.example
├── package.json
└── openapi.yaml
```

## Server Setup

### Express Server

```javascript
// src/index.js
import express from 'express';
import { config } from './config/index.js';
import { setupRoutes } from './api/routes.js';
import { errorHandler } from './api/middleware/error.js';
import { logger } from './lib/logger.js';
import { db } from './db/client.js';

const app = express();

// Security middleware
app.use(helmet());
app.use(cors({ origin: process.env.ALLOWED_ORIGINS?.split(',') }));
app.use(compression());

// Body parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Request logging
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    logger.info({
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration: Date.now() - start
    });
  });
  next();
});

// Routes
setupRoutes(app);

// Error handling (must be last)
app.use(errorHandler);

// Graceful shutdown
async function shutdown() {
  logger.info('Shutting down...');
  await db.end();
  process.exit(0);
}

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
```

### Fastify Server

```javascript
import Fastify from 'fastify';
import helmet from '@fastify/helmet';
import cors from '@fastify/cors';
import compress from '@fastify/compress';

const fastify = Fastify({
  logger: {
    level: process.env.LOG_LEVEL || 'info',
    transport: {
      target: 'pino-pretty',
      options: { colorize: true },
    },
  },
});

// Plugins
await fastify.register(helmet);
await fastify.register(cors, { origin: true });
await fastify.register(compress);

// Type-safe routes with schema validation
fastify.post<{
  Body: { name: string; email: string };
  Reply: { id: string; name: string };
}>(
  '/users',
  {
    schema: {
      body: {
        type: 'object',
        required: ['name', 'email'],
        properties: {
          name: { type: 'string' },
          email: { type: 'string' }
        }
      }
    },
    handler: async (request, reply) => {
      // Handler logic here
    }
  }
);
```