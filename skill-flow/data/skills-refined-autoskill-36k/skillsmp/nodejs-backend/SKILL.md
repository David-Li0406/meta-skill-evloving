---
name: nodejs-backend
description: Build Node.js backend services with Express/Fastify, PostgreSQL, and services pattern. Use when creating backend APIs, setting up servers, or connecting to databases.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# NodeJS Backend Skill

Build backend services with Node.js following project conventions for structure, database access, and error handling.

---

## When to Use

- Creating backend API services
- Setting up Express or Fastify servers
- Connecting to PostgreSQL databases
- Implementing middleware patterns
- Handling environment configuration

---

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

---

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

// Body parsing
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

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

// Start server
const port = config.port;
app.listen(port, () => {
  logger.info(`Server running on port ${port}`);
});
```

### Fastify Server

```javascript
// src/index.js
import Fastify from 'fastify';
import { config } from './config/index.js';
import { setupRoutes } from './api/routes.js';

const fastify = Fastify({
  logger: true
});

// Body parsing (built-in)
// Request validation (use @fastify/type-provider-json-schema-to-ts)

// Routes
setupRoutes(fastify);

// Start server
const start = async () => {
  try {
    await fastify.listen({ port: config.port, host: '0.0.0.0' });
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
```

---

## Configuration

### Environment Variables

```javascript
// src/config/index.js

/**
 * Application configuration
 * All environment variables validated at startup
 */
export const config = {
  env: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '3000', 10),

  db: {
    host: requireEnv('DB_HOST'),
    port: parseInt(process.env.DB_PORT || '5432', 10),
    database: requireEnv('DB_NAME'),
    user: requireEnv('DB_USER'),
    password: requireEnv('DB_PASSWORD'),
    ssl: process.env.DB_SSL === 'true',
    maxConnections: parseInt(process.env.DB_MAX_CONNECTIONS || '10', 10)
  },

  jwt: {
    secret: requireEnv('JWT_SECRET'),
    expiresIn: process.env.JWT_EXPIRES_IN || '1h'
  },

  cors: {
    origin: process.env.CORS_ORIGIN || '*'
  }
};

/**
 * Require environment variable or throw
 * @param {string} name - Variable name
 * @returns {string} - Variable value
 */
function requireEnv(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}
```

### .env.example

```bash
# Server
NODE_ENV=development
PORT=3000

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=
DB_SSL=false
DB_MAX_CONNECTIONS=10

# Authentication
JWT_SECRET=change-this-in-production
JWT_EXPIRES_IN=1h

# CORS
CORS_ORIGIN=http://localhost:5173
```

---

## Database Access

### PostgreSQL Client

```javascript
// src/db/client.js
import pg from 'pg';
import { config } from '../config/index.js';
import { logger } from '../lib/logger.js';

const { Pool } = pg;

export const db = new Pool({
  host: config.db.host,
  port: config.db.port,
  database: config.db.database,
  user: config.db.user,
  password: config.db.password,
  ssl: config.db.ssl ? { rejectUnauthorized: false } : false,
  max: config.db.maxConnections
});

// Log connection events
db.on('connect', () => {
  logger.debug('Database client connected');
});

db.on('error', (err) => {
  logger.error('Database error', err);
});

/**
 * Execute query with parameters
 * @param {string} sql - SQL query
 * @param {any[]} params - Query parameters
 * @returns {Promise<pg.QueryResult>}
 */
export async function query(sql, params = []) {
  const start = Date.now();
  try {
    const result = await db.query(sql, params);
    logger.debug({
      sql: sql.slice(0, 100),
      duration: Date.now() - start,
      rows: result.rowCount
    });
    return result;
  } catch (error) {
    logger.error({ sql: sql.slice(0, 100), error: error.message });
    throw error;
  }
}

/**
 * Execute queries in a transaction
 * @param {Function} fn - Function receiving client
 * @returns {Promise<any>}
 */
export async function transaction(fn) {
  const client = await db.connect();
  try {
    await client.query('BEGIN');
    const result = await fn(client);
    await client.query('COMMIT');
    return result;
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}
```

### Query Files

```javascript
// src/db/queries/users.js

export const userQueries = {
  findById: `
    SELECT id, email, name, role, created_at, updated_at
    FROM users
    WHERE id = $1
  `,

  findByEmail: `
    SELECT id, email, name, role, password_hash, created_at
    FROM users
    WHERE email = $1
  `,

  create: `
    INSERT INTO users (email, name, password_hash)
    VALUES ($1, $2, $3)
    RETURNING id, email, name, role, created_at
  `,

  update: `
    UPDATE users
    SET name = COALESCE($2, name),
        email = COALESCE($3, email),
        updated_at = NOW()
    WHERE id = $1
    RETURNING id, email, name, role, updated_at
  `,

  delete: `
    DELETE FROM users WHERE id = $1
  `,

  list: `
    SELECT id, email, name, role, created_at
    FROM users
    ORDER BY created_at DESC
    LIMIT $1 OFFSET $2
  `,

  count: `
    SELECT COUNT(*) as total FROM users
  `
};
```

---

## Services

### Service Pattern

```javascript
// src/services/user.js
import { query, transaction } from '../db/client.js';
import { userQueries } from '../db/queries/users.js';
import { NotFoundError, ConflictError } from '../lib/errors.js';
import { hashPassword, verifyPassword } from '../lib/auth.js';

/**
 * User service - business logic for user operations
 */
export const userService = {
  /**
   * Get user by ID
   * @param {string} id - User ID
   * @returns {Promise<object>} User data
   */
  async getById(id) {
    const result = await query(userQueries.findById, [id]);
    if (result.rows.length === 0) {
      throw new NotFoundError('User not found');
    }
    return result.rows[0];
  },

  /**
   * Create new user
   * @param {object} data - User data
   * @returns {Promise<object>} Created user
   */
  async create(data) {
    const { email, name, password } = data;

    // Check for existing email
    const existing = await query(userQueries.findByEmail, [email]);
    if (existing.rows.length > 0) {
      throw new ConflictError('Email already registered');
    }

    const passwordHash = await hashPassword(password);
    const result = await query(userQueries.create, [email, name, passwordHash]);
    return result.rows[0];
  },

  /**
   * Update user
   * @param {string} id - User ID
   * @param {object} data - Update data
   * @returns {Promise<object>} Updated user
   */
  async update(id, data) {
    const { name, email } = data;
    const result = await query(userQueries.update, [id, name, email]);
    if (result.rows.length === 0) {
      throw new NotFoundError('User not found');
    }
    return result.rows[0];
  },

  /**
   * List users with pagination
   * @param {object} options - Pagination options
   * @returns {Promise<object>} Users and pagination info
   */
  async list({ limit = 20, offset = 0 } = {}) {
    const [usersResult, countResult] = await Promise.all([
      query(userQueries.list, [limit, offset]),
      query(userQueries.count)
    ]);

    return {
      data: usersResult.rows,
      pagination: {
        total: parseInt(countResult.rows[0].total, 10),
        limit,
        offset,
        hasMore: offset + usersResult.rows.length < countResult.rows[0].total
      }
    };
  }
};
```

---

## Middleware

### Error Handler

```javascript
// src/api/middleware/error.js
import { logger } from '../../lib/logger.js';
import { AppError } from '../../lib/errors.js';

/**
 * Global error handler middleware
 */
export function errorHandler(err, req, res, next) {
  // Log error
  logger.error({
    error: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method
  });

  // Handle known errors
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        ...(err.details && { details: err.details })
      }
    });
  }

  // Handle validation errors (from express-validator, etc.)
  if (err.name === 'ValidationError') {
    return res.status(422).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Validation failed',
        details: err.errors
      }
    });
  }

  // Handle database errors
  if (err.code === '23505') {  // PostgreSQL unique violation
    return res.status(409).json({
      error: {
        code: 'CONFLICT',
        message: 'Resource already exists'
      }
    });
  }

  // Unknown errors - don't expose details
  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred'
    }
  });
}
```

### Custom Errors

```javascript
// src/lib/errors.js

/**
 * Base application error
 */
export class AppError extends Error {
  constructor(message, statusCode, code, details = null) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
    this.details = details;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class NotFoundError extends AppError {
  constructor(message = 'Resource not found') {
    super(message, 404, 'NOT_FOUND');
  }
}

export class BadRequestError extends AppError {
  constructor(message = 'Bad request', details = null) {
    super(message, 400, 'BAD_REQUEST', details);
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED');
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Forbidden') {
    super(message, 403, 'FORBIDDEN');
  }
}

export class ConflictError extends AppError {
  constructor(message = 'Conflict') {
    super(message, 409, 'CONFLICT');
  }
}

export class ValidationError extends AppError {
  constructor(errors) {
    super('Validation failed', 422, 'VALIDATION_ERROR', { errors });
  }
}
```

---

## Logging

```javascript
// src/lib/logger.js

const levels = { error: 0, warn: 1, info: 2, debug: 3 };
const currentLevel = levels[process.env.LOG_LEVEL || 'info'];

function formatMessage(level, data) {
  const timestamp = new Date().toISOString();
  const message = typeof data === 'string' ? { message: data } : data;
  return JSON.stringify({ timestamp, level, ...message });
}

export const logger = {
  error(data) {
    if (currentLevel >= levels.error) {
      console.error(formatMessage('error', data));
    }
  },
  warn(data) {
    if (currentLevel >= levels.warn) {
      console.warn(formatMessage('warn', data));
    }
  },
  info(data) {
    if (currentLevel >= levels.info) {
      console.log(formatMessage('info', data));
    }
  },
  debug(data) {
    if (currentLevel >= levels.debug) {
      console.log(formatMessage('debug', data));
    }
  }
};
```

---

## Checklist

When building Node.js backends:

- [ ] Use ES modules (`"type": "module"` in package.json)
- [ ] Validate all environment variables at startup
- [ ] Create .env.example with all required variables
- [ ] Use connection pooling for database
- [ ] Implement proper error handling middleware
- [ ] Use structured logging (JSON format)
- [ ] Separate routes, handlers, and services
- [ ] Use parameterized queries (prevent SQL injection)
- [ ] Implement graceful shutdown
- [ ] Add request logging
- [ ] Write tests for services
- [ ] Document API with OpenAPI

## Related Skills

- **database** - Design PostgreSQL schemas with migrations, seeding, and d...
- **rest-api** - Write REST API endpoints with HTTP methods, status codes,...
- **authentication** - Implement secure authentication with JWT, sessions, OAuth...
- **backend-testing** - Write tests for backend services, APIs, and database access
