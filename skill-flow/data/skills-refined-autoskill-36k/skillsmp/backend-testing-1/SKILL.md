---
name: backend-testing
description: Write tests for backend services, APIs, and database access. Use when testing Express/Fastify handlers, services with database calls, or integration tests.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Backend Testing Skill

Write and maintain tests for backend services using Node.js native test runner with patterns for database mocking, API testing, and integration tests.

## Test Categories

| Type | Purpose | Database | Speed |
|------|---------|----------|-------|
| Unit | Service logic in isolation | Mocked | Fast |
| Integration | Service + real database | Test DB | Medium |
| API | HTTP endpoints | Mocked or Test DB | Medium |
| E2E | Full request flow | Test DB | Slow |

## Directory Structure

```
test/
├── unit/
│   └── services/
│       └── user.test.js
├── integration/
│   └── services/
│       └── user.integration.test.js
├── api/
│   └── auth.api.test.js
├── helpers/
│   ├── db.js          # Test database utilities
│   ├── request.js     # HTTP request helpers
│   └── mocks.js       # Common mocks
└── fixtures/
    └── users.json
```

## Unit Testing Services

### Mocking Database Access

```javascript
import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert';
import { mock } from 'node:test';

// Service under test
import { UserService } from '../../src/services/user.js';

describe('UserService', () => {
  let mockDb;
  let service;

  beforeEach(() => {
    // Create mock database client
    mockDb = {
      query: mock.fn()
    };
    service = new UserService(mockDb);
  });

  describe('findById', () => {
    it('should return user when found', async () => {
      const mockUser = { id: '123', email: 'test@example.com' };
      mockDb.query.mock.mockImplementation(() => ({
        rows: [mockUser]
      }));

      const result = await service.findById('123');

      assert.deepStrictEqual(result, mockUser);
      assert.strictEqual(mockDb.query.mock.calls.length, 1);
    });

    it('should return null when not found', async () => {
      mockDb.query.mock.mockImplementation(() => ({ rows: [] }));

      const result = await service.findById('nonexistent');

      assert.strictEqual(result, null);
    });

    it('should throw on database error', async () => {
      mockDb.query.mock.mockImplementation(() => {
        throw new Error('Connection failed');
      });

      await assert.rejects(
        () => service.findById('123'),
        { message: 'Connection failed' }
      );
    });
  });
});
```

### Service with Dependencies

```javascript
import { describe, it, beforeEach } from 'node:test';
import { mock } from 'node:test';

describe('OrderService', () => {
  let mockDb;
  let mockEmailService;
  let mockPaymentService;
  let service;

  beforeEach(() => {
    mockDb = { query: mock.fn() };
    mockEmailService = { send: mock.fn() };
    mockPaymentService = { charge: mock.fn() };

    service = new OrderService({
      db: mockDb,
      email: mockEmailService,
      payment: mockPaymentService
    });
  });

  it('should create order and send confirmation', async () => {
    mockDb.query.mock.mockImplementation(() => ({
      rows: [{ id: 'order-1' }]
    }));
    mockPaymentService.charge.mock.mockImplementation(() => ({
      success: true
    }));

    await service.create({ userId: '123', items: [] });

    assert.strictEqual(mockEmailService.send.mock.calls.length, 1);
    assert.strictEqual(
      mockEmailService.send.mock.calls[0].arguments[0].type,
      'order_confirmation'
    );
  });
});
```

## Integration Testing with Test Database

### Test Database Setup

```javascript
// test/helpers/db.js
import pg from 'pg';

const TEST_DATABASE_URL = process.env.TEST_DATABASE_URL
  || 'postgresql://localhost:5432/myapp_test';

let pool;

/**
 * Get or create test database pool
 * @returns {pg.Pool}
 */
export function getTestPool() {
  if (!pool) {
    pool = new pg.Pool({ connectionString: TEST_DATABASE_URL });
  }
  return pool;
}

/**
 * Run migrations on test database
 */
export async function migrateTestDb() {
  const { migrate } = await import('../../src/db/migrate.js');
  await migrate(getTestPool());
}

/**
 * Truncate all tables (preserves schema)
 */
export async function truncateAll() {
  const pool = getTestPool();
  await pool.query(`
    DO $$ DECLARE
      r RECORD;
    BEGIN
      FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename != 'migrations') LOOP
        EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' CASCADE';
      END LOOP;
    END $$;
  `);
}

/**
 * Close test database pool
 */
export async function closeTestDb() {
  if (pool) {
    await pool.end();
    pool = null;
  }
}

/**
 * Insert fixture data
 * @param {string} table
 * @param {Object[]} rows
 */
export async function insertFixtures(table, rows) {
  const pool = getTestPool();
  for (const row of rows) {
    const keys = Object.keys(row);
    const values = Object.values(row);
    const placeholders = keys.map((_, i) => `$${i + 1}`).join(', ');
    await pool.query(
      `INSERT INTO ${table} (${keys.join(', ')}) VALUES (${placeholders})`,
      values
    );
  }
}
```

### Integration Test Example

```javascript
// test/integration/services/user.integration.test.js
import { describe, it, before, after, beforeEach } from 'node:test';
import assert from 'node:assert';
import {
  getTestPool,
  migrateTestDb,
  truncateAll,
  closeTestDb,
  insertFixtures
} from '../../helpers/db.js';
import { UserService } from '../../../src/services/user.js';

describe('UserService (integration)', () => {
  let service;

  before(async () => {
    await migrateTestDb();
    service = new UserService(getTestPool());
  });

  beforeEach(async () => {
    await truncateAll();
  });

  after(async () => {
    await closeTestDb();
  });

  describe('create', () => {
    it('should insert user into database', async () => {
      const user = await service.create({
        email: 'test@example.com',
        name: 'Test User',
        password: 'hashed_password'
      });

      assert.ok(user.id);
      assert.strictEqual(user.email, 'test@example.com');

      // Verify in database
      const pool = getTestPool();
      const result = await pool.query(
        'SELECT * FROM users WHERE id = $1',
        [user.id]
      );
      assert.strictEqual(result.rows.length, 1);
    });

    it('should reject duplicate email', async () => {
      await insertFixtures('users', [{
        id: '550e8400-e29b-41d4-a716-446655440000',
        email: 'existing@example.com',
        name: 'Existing',
        password_hash: 'hash',
        role: 'user',
        created_at: new Date(),
        updated_at: new Date()
      }]);

      await assert.rejects(
        () => service.create({
          email: 'existing@example.com',
          name: 'New User',
          password: 'password'
        }),
        { code: 'EMAIL_EXISTS' }
      );
    });
  });
});
```

## API Endpoint Testing

### HTTP Request Helper

```javascript
// test/helpers/request.js

/**
 * Create test HTTP client for Express app
 * @param {Express} app
 * @returns {Object}
 */
export function createTestClient(app) {
  let server;
  let baseUrl;

  return {
    async start() {
      return new Promise((resolve) => {
        server = app.listen(0, () => {
          const { port } = server.address();
          baseUrl = `http://localhost:${port}`;
          resolve();
        });
      });
    },

    async stop() {
      return new Promise((resolve) => {
        server?.close(resolve);
      });
    },

    async request(method, path, options = {}) {
      const url = `${baseUrl}${path}`;
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        body: options.body ? JSON.stringify(options.body) : undefined
      });

      return {
        status: response.status,
        headers: Object.fromEntries(response.headers),
        body: await response.json().catch(() => null)
      };
    },

    get(path, options) { return this.request('GET', path, options); },
    post(path, options) { return this.request('POST', path, options); },
    patch(path, options) { return this.request('PATCH', path, options); },
    delete(path, options) { return this.request('DELETE', path, options); }
  };
}
```

### API Test Example

```javascript
// test/api/auth.api.test.js
import { describe, it, before, after, beforeEach } from 'node:test';
import assert from 'node:assert';
import { createApp } from '../../src/index.js';
import { createTestClient } from '../helpers/request.js';
import { migrateTestDb, truncateAll, closeTestDb } from '../helpers/db.js';

describe('Auth API', () => {
  let client;
  let app;

  before(async () => {
    await migrateTestDb();
    app = createApp({ isTest: true });
    client = createTestClient(app);
    await client.start();
  });

  beforeEach(async () => {
    await truncateAll();
  });

  after(async () => {
    await client.stop();
    await closeTestDb();
  });

  describe('POST /api/auth/register', () => {
    it('should create user and return tokens', async () => {
      const res = await client.post('/api/auth/register', {
        body: {
          email: 'new@example.com',
          name: 'New User',
          password: 'SecurePass123'
        }
      });

      assert.strictEqual(res.status, 201);
      assert.ok(res.body.user.id);
      assert.strictEqual(res.body.user.email, 'new@example.com');
      assert.ok(res.body.accessToken);
      assert.ok(res.body.refreshToken);
    });

    it('should reject weak password', async () => {
      const res = await client.post('/api/auth/register', {
        body: {
          email: 'new@example.com',
          name: 'New User',
          password: '123'
        }
      });

      assert.strictEqual(res.status, 400);
      assert.strictEqual(res.body.error.code, 'VALIDATION_ERROR');
    });

    it('should reject duplicate email', async () => {
      // First registration
      await client.post('/api/auth/register', {
        body: {
          email: 'dupe@example.com',
          name: 'First',
          password: 'SecurePass123'
        }
      });

      // Duplicate attempt
      const res = await client.post('/api/auth/register', {
        body: {
          email: 'dupe@example.com',
          name: 'Second',
          password: 'SecurePass123'
        }
      });

      assert.strictEqual(res.status, 409);
    });
  });

  describe('POST /api/auth/login', () => {
    beforeEach(async () => {
      await client.post('/api/auth/register', {
        body: {
          email: 'user@example.com',
          name: 'Test User',
          password: 'SecurePass123'
        }
      });
    });

    it('should return tokens for valid credentials', async () => {
      const res = await client.post('/api/auth/login', {
        body: {
          email: 'user@example.com',
          password: 'SecurePass123'
        }
      });

      assert.strictEqual(res.status, 200);
      assert.ok(res.body.accessToken);
    });

    it('should reject invalid password', async () => {
      const res = await client.post('/api/auth/login', {
        body: {
          email: 'user@example.com',
          password: 'WrongPassword'
        }
      });

      assert.strictEqual(res.status, 401);
    });
  });
});
```

### Authenticated Request Testing

```javascript
describe('Protected Endpoints', () => {
  let authToken;

  beforeEach(async () => {
    await truncateAll();

    // Create and login test user
    await client.post('/api/auth/register', {
      body: {
        email: 'auth@example.com',
        name: 'Auth User',
        password: 'SecurePass123'
      }
    });

    const loginRes = await client.post('/api/auth/login', {
      body: { email: 'auth@example.com', password: 'SecurePass123' }
    });
    authToken = loginRes.body.accessToken;
  });

  it('should access protected route with token', async () => {
    const res = await client.get('/api/auth/me', {
      headers: { Authorization: `Bearer ${authToken}` }
    });

    assert.strictEqual(res.status, 200);
    assert.strictEqual(res.body.user.email, 'auth@example.com');
  });

  it('should reject request without token', async () => {
    const res = await client.get('/api/auth/me');

    assert.strictEqual(res.status, 401);
  });
});
```

## Mocking External Services

### HTTP Client Mocking

```javascript
import { mock } from 'node:test';

describe('PaymentService', () => {
  let originalFetch;

  beforeEach(() => {
    originalFetch = global.fetch;
    global.fetch = mock.fn();
  });

  afterEach(() => {
    global.fetch = originalFetch;
  });

  it('should call payment provider API', async () => {
    global.fetch.mock.mockImplementation(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ transaction_id: 'txn_123' })
      })
    );

    const result = await paymentService.charge({
      amount: 1000,
      currency: 'USD'
    });

    assert.strictEqual(result.transactionId, 'txn_123');
    assert.strictEqual(global.fetch.mock.calls.length, 1);

    const [url, options] = global.fetch.mock.calls[0].arguments;
    assert.ok(url.includes('/charges'));
    assert.strictEqual(options.method, 'POST');
  });
});
```

## Test Configuration

### package.json Scripts

```json
{
  "scripts": {
    "test": "node --test",
    "test:unit": "node --test test/unit/**/*.test.js",
    "test:integration": "node --test test/integration/**/*.test.js",
    "test:api": "node --test test/api/**/*.test.js",
    "test:coverage": "node --test --experimental-test-coverage",
    "test:watch": "node --test --watch"
  }
}
```

### Environment Variables

```bash
# .env.test
NODE_ENV=test
TEST_DATABASE_URL=postgresql://localhost:5432/myapp_test
LOG_LEVEL=error
JWT_SECRET=test-secret-key
```

## Test Checklist

Before completing a backend feature:

- [ ] Unit tests for service methods with mocked dependencies
- [ ] Integration tests for database operations
- [ ] API tests for all endpoints
- [ ] Error case coverage (validation, auth, not found)
- [ ] Edge cases (empty results, pagination bounds)
- [ ] Authentication/authorization checks tested

## Running Tests

```bash
# All tests
npm test

# By category
npm run test:unit
npm run test:integration
npm run test:api

# Single file
node --test test/api/auth.api.test.js

# With coverage
npm run test:coverage

# Watch mode during development
npm run test:watch
```

## Related Skills

- [unit-testing](../unit-testing/SKILL.md) - General unit testing patterns
- [e2e-testing](../e2e-testing/SKILL.md) - Playwright browser testing
- [nodejs-backend](../nodejs-backend/SKILL.md) - Backend architecture patterns
