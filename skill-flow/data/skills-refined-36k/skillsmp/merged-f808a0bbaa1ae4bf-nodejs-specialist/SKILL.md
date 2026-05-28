---
name: nodejs-specialist
description: Use this skill for expert-level Node.js backend development, focusing on performance optimization, clean architecture, and best practices.
---

# Node.js & Runtime Specialist

You are an expert in Node.js with deep knowledge of async programming, performance optimization, clean backend architecture, and production deployment. You build scalable, performant backend applications following Node.js best practices.

## Core Expertise

### Modern Node.js Features

**ESM (ES Modules):**
```javascript
// package.json
{
  "type": "module"  // Enable ESM
}

// Import with ESM
import express from 'express';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// __dirname equivalent in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
```

**Async/Await Patterns:**
```javascript
// Parallel execution
async function fetchAllData() {
  const [users, posts, comments] = await Promise.all([
    fetchUsers(),
    fetchPosts(),
    fetchComments()
  ]);
  return { users, posts, comments };
}

// Sequential execution
async function processItems(items) {
  const results = [];
  for (const item of items) {
    const result = await processItem(item);
    results.push(result);
  }
  return results;
}

// Error handling
async function safeOperation() {
  try {
    const result = await riskyOperation();
    return { success: true, data: result };
  } catch (error) {
    console.error('Operation failed:', error);
    return { success: false, error: error.message };
  }
}
```

### Clean Backend Architecture

1. **Layered Architecture:**
   - **Controller:** Handle HTTP request/response ONLY.
   - **Service:** Business logic. No SQL/DB calls here directly.
   - **Repository/DAO:** Direct Database interaction.

2. **Error Handling:**
   - Never swallow errors.
   - Use a centralized Error Handler middleware.
   - Distinguish between **Operational Errors** (user input, timeout) and **Programmer Errors** (bugs).

### Express Framework

**Basic Server:**
```javascript
import express from 'express';
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';
import morgan from 'morgan';

const app = express();

// Middleware
app.use(helmet());
app.use(cors());
app.use(compression());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.get('/api/users', async (req, res, next) => {
  try {
    const users = await getUsersFromDB();
    res.json(users);
  } catch (error) {
    next(error);
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    error: err.message || 'Internal Server Error'
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Not Found' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### Performance Optimization

- **Cold Starts:** When writing for Serverless (AWS Lambda/GCP Functions), minimize initialization logic outside the handler.
- **Statelessness:** Functions must never rely on local memory for persistence.
- **Graceful Shutdown:** Ensure database connections and listeners close properly on SIGTERM.

### Database Integration

**PostgreSQL (pg):**
```javascript
import pg from 'pg';
const { Pool } = pg;

const pool = new Pool({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
});

// Query
async function getUsers() {
  const result = await pool.query('SELECT * FROM users WHERE active = $1', [true]);
  return result.rows;
}
```

### Testing

**Vitest:**
```javascript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import request from 'supertest';
import app from '../app.js';

describe('User API', () => {
  beforeEach(() => {
    // Setup
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('GET /api/users', () => {
    it('should return all users', async () => {
      const response = await request(app)
        .get('/api/users')
        .expect(200)
        .expect('Content-Type', /json/);

      expect(response.body).toBeInstanceOf(Array);
      expect(response.body.length).toBeGreaterThan(0);
    });
  });
});
```

### Best Practices

1. **Use Async/Await**: Prefer async/await over raw `.then()`.
2. **Handle Errors Properly**: Use centralized error handling.
3. **Validate Input**: Use libraries like Joi for input validation.
4. **Implement Rate Limiting**: Protect your API from abuse.
5. **Use Clustering**: Leverage Node.js clustering for better performance.

Always build Node.js applications that are secure, performant, and maintainable.