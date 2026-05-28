---
name: nodejs-backend-development
description: Use this skill when building production-ready Node.js backend services with Express or Fastify, implementing best practices for middleware, error handling, authentication, and database integration.
---

# Node.js Backend Development

Comprehensive guidance for building scalable, maintainable, and production-ready Node.js backend applications with modern frameworks, architectural patterns, and best practices.

## When to Use This Skill

- Creating backend API services or GraphQL servers
- Setting up Express or Fastify servers
- Implementing authentication and authorization
- Designing scalable backend architectures
- Integrating databases (SQL and NoSQL)
- Building real-time applications with WebSockets
- Implementing background job processing
- Handling environment configuration and error management

## Project Structure

```
backend/
├── src/
│   ├── index.js           # Entry point, server setup
│   ├── config/            # Configuration loader
│   ├── api/               # Route definitions and middleware
│   ├── services/          # Business logic
│   ├── repositories/      # Data access layer
│   ├── models/            # Data models
│   ├── utils/             # Helper functions
│   ├── tests/             # Test cases
│   └── lib/               # Shared utilities
├── .env.example
├── package.json
└── openapi.yaml
```

## Server Setup

### Express Server

```javascript
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';

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
  console.log(`${req.method} ${req.path}`);
  next();
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### Fastify Server

```javascript
import Fastify from 'fastify';
import helmet from '@fastify/helmet';
import cors from '@fastify/cors';
import compress from '@fastify/compress';

const fastify = Fastify({
  logger: true,
});

// Plugins
await fastify.register(helmet);
await fastify.register(cors, { origin: true });
await fastify.register(compress);

// Start server
const start = async () => {
  try {
    await fastify.listen({ port: process.env.PORT || 3000, host: '0.0.0.0' });
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
```

## Middleware Patterns

### Error Handling Middleware

```javascript
import { logger } from '../lib/logger.js';

export function errorHandler(err, req, res, next) {
  logger.error({
    error: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method
  });

  res.status(err.statusCode || 500).json({
    error: {
      message: err.message || 'An unexpected error occurred'
    }
  });
}
```

### Authentication Middleware

```javascript
import jwt from 'jsonwebtoken';

export const authenticate = async (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) return res.status(401).json({ message: 'No token provided' });

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET);
    req.user = payload;
    next();
  } catch (error) {
    return res.status(401).json({ message: 'Invalid token' });
  }
};
```

## Database Access

### PostgreSQL Client

```javascript
import { Pool } from 'pg';

const pool = new Pool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,
});

export const query = async (sql, params) => {
  const { rows } = await pool.query(sql, params);
  return rows;
};
```

## Services

### User Service Example

```javascript
import { query } from '../db/client.js';

export const userService = {
  async createUser(data) {
    const result = await query('INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *', [data.name, data.email]);
    return result[0];
  },
  async getUserById(id) {
    const result = await query('SELECT * FROM users WHERE id = $1', [id]);
    return result[0];
  },
};
```

## Best Practices

1. **Use TypeScript**: Type safety prevents runtime errors.
2. **Implement proper error handling**: Use custom error classes.
3. **Validate input**: Use libraries like Zod or Joi.
4. **Use environment variables**: Never hardcode secrets.
5. **Implement logging**: Use structured logging (Pino, Winston).
6. **Add rate limiting**: Prevent abuse.
7. **Use HTTPS**: Always in production.
8. **Implement health checks**: For monitoring.
9. **Write tests**: Unit, integration, and E2E tests.

## Related Skills

- **database** - Design PostgreSQL schemas with migrations, seeding, and data access patterns.
- **rest-api** - Write REST API endpoints with HTTP methods, status codes, and best practices.
- **authentication** - Implement secure authentication with JWT, sessions, and OAuth.
- **backend-testing** - Write tests for backend services, APIs, and database access.