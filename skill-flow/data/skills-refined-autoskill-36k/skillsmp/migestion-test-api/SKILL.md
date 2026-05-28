---
name: migestion-test-api
description: >
  API testing patterns for MiGestion - Jest, Supertest, mocking.
  Trigger: When writing or running API unit tests.
license: MIT
metadata:
  author: migestion
  version: '1.0'
  scope: [api]
  auto_invoke: 'Writing API unit tests'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Test Structure

```
tests/
├── __mocks__/
│   └── prisma.ts           # Prisma mock
├── modules/
│   ├── clients/
│   │   ├── clients.service.test.ts
│   │   ├── clients.repository.test.ts
│   │   └── clients.controller.test.ts
│   └── auth/
│       └── auth.service.test.ts
```

## Prisma Mock

```typescript
// tests/__mocks__/prisma.ts
import { PrismaClient } from '@prisma/client';

const mockPrismaClient = {
  example: {
    findFirst: jest.fn(),
    findMany: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    delete: jest.fn(),
    count: jest.fn(),
  },
  // ... other models
};

jest.mock('@prisma/client', () => ({
  PrismaClient: jest.fn(() => mockPrismaClient),
}));

export const prisma = mockPrismaClient as any;
```

## Service Test

```typescript
import * as clientsRepository from '../../src/modules/clients/clients.repository';
import * as clientsService from '../../src/modules/clients/clients.service';
import { NotFoundError } from '../../src/shared/errors/app-error';

describe('clientsService.getById', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should return client when found', async () => {
    const mockClient = {
      id: 'client-1',
      tenantId: 'tenant-1',
      companyName: 'Test Company',
    };

    jest.spyOn(clientsRepository, 'findById').mockResolvedValue(mockClient as any);

    const result = await clientsService.getById('tenant-1', 'client-1');

    expect(clientsRepository.findById).toHaveBeenCalledWith('tenant-1', 'client-1');
    expect(result).toHaveProperty('id', 'client-1');
  });

  it('should throw NotFoundError when client not found', async () => {
    jest.spyOn(clientsRepository, 'findById').mockResolvedValue(null);

    await expect(clientsService.getById('tenant-1', 'non-existent')).rejects.toThrow(NotFoundError);
  });
});
```

## Repository Test

```typescript
import { prisma } from '../../__mocks__/prisma';
import * as clientsRepository from '../../src/modules/clients/clients.repository';

describe('clientsRepository.findById', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should find client by id and tenantId', async () => {
    const mockClient = {
      id: 'client-1',
      tenantId: 'tenant-1',
      companyName: 'Test Company',
    };

    prisma.client.findFirst.mockResolvedValue(mockClient);

    const result = await clientsRepository.findById('tenant-1', 'client-1');

    expect(prisma.client.findFirst).toHaveBeenCalledWith({
      where: { id: 'client-1', tenantId: 'tenant-1' },
    });
    expect(result).toEqual(mockClient);
  });
});
```

## Controller Test

```typescript
import request from 'supertest';
import app from '../../src/app';
import * as clientsService from '../../src/modules/clients/clients.service';

describe('clientsController.list', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should return list of clients', async () => {
    const mockResponse = {
      clients: [{ id: '1', companyName: 'Test' }],
      meta: { total: 1, page: 1, limit: 20 },
    };

    jest.spyOn(clientsService, 'list').mockResolvedValue(mockResponse as any);

    const response = await request(app).get('/clients').set('x-tenant-id', 'tenant-1').expect(200);

    expect(response.body).toEqual({
      success: true,
      data: mockResponse,
    });
  });
});
```

## Integration Test (with Express)

```typescript
import request from 'supertest';
import app from '../../src/app';
import { setupTestDb, teardownTestDb } from '../helpers/test-db';

describe('Client API Integration', () => {
  let tenantId: string;

  beforeAll(async () => {
    const db = await setupTestDb();
    tenantId = db.tenantId;
  });

  afterAll(async () => {
    await teardownTestDb();
  });

  it('should create client and retrieve it', async () => {
    const createResponse = await request(app)
      .post('/clients')
      .set('x-tenant-id', tenantId)
      .set('authorization', 'Bearer valid-token')
      .send({
        companyName: 'Test Company',
        contactName: 'John Doe',
        status: 'active',
      })
      .expect(201);

    const clientId = createResponse.body.data.id;

    const getResponse = await request(app)
      .get(`/clients/${clientId}`)
      .set('x-tenant-id', tenantId)
      .set('authorization', 'Bearer valid-token')
      .expect(200);

    expect(getResponse.body.data.companyName).toBe('Test Company');
  });
});
```

## Mocking External Services

```typescript
import * as redis from '../../src/infrastructure/redis';

describe('Service with cache', () => {
  beforeEach(() => {
    jest.spyOn(redis, 'get').mockResolvedValue(null);
    jest.spyOn(redis, 'set').mockResolvedValue('OK');
  });

  it('should fetch from database when cache miss', async () => {
    const result = await service.getData('key');

    expect(redis.get).toHaveBeenCalledWith('key');
    expect(redis.set).toHaveBeenCalled();
  });
});
```

## Test Helpers

```typescript
// tests/helpers/auth.ts
export function mockAuthMiddleware(overrides = {}) {
  return (req: any, res: any, next: any) => {
    req.user = {
      id: 'user-1',
      tenantId: 'tenant-1',
      role: 'OWNER',
      ...overrides,
    };
    req.tenantId = 'tenant-1';
    next();
  };
}

// tests/helpers/test-db.ts
export async function setupTestDb() {
  // Create test database or transaction
  return { tenantId: 'test-tenant' };
}

export async function teardownTestDb() {
  // Cleanup test database or rollback transaction
}
```

## Commands

```bash
npm run test:api                    # Run all API tests
npm run test:api -- --watch         # Watch mode
npm run test:api -- --coverage      # Coverage report
npm run test:api -- clients.service.test.ts  # Run specific test file
```

## Jest Config

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src', '<rootDir>/tests'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  collectCoverageFrom: ['src/**/*.ts', '!src/**/*.d.ts', '!src/server.ts'],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
};
```

## Related Skills

- `migestion-api` - API patterns being tested
- `jest` - General Jest testing patterns
