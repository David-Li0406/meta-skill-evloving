---
name: jest
description: >
  Jest unit testing patterns and best practices.
  Trigger: When writing unit tests for TypeScript/JavaScript code.
license: MIT
metadata:
  author: migestion
  version: '1.0'
  scope: [api, web]
  auto_invoke: 'Writing unit tests'
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Test Structure

```typescript
// ✅ Describe blocks group related tests
describe('ClientService', () => {
  describe('getById', () => {
    it('should return client when found', async () => {
      // ...
    });

    it('should throw NotFoundError when not found', async () => {
      // ...
    });
  });
});
```

## beforeEach/afterEach

```typescript
describe('ClientService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  afterEach(() => {
    // Cleanup
  });
});
```

## Mocking Functions

```typescript
// ✅ Mock function
const mockFetch = jest.fn().mockResolvedValue({ data: [] });

// ✅ Spy on existing function
jest.spyOn(clientsRepository, 'findById').mockResolvedValue(mockClient);

// ✅ Mock implementation
jest.spyOn(service, 'process').mockImplementation(async data => ({ ...data, processed: true }));

// ✅ Restore original
afterAll(() => {
  jest.restoreAllMocks();
});
```

## Mocking Modules

```typescript
// ✅ Mock module
jest.mock('../utils/logger', () => ({
  logger: {
    info: jest.fn(),
    error: jest.fn(),
  },
}));

// ✅ Partial mock
jest.mock('redis', () => ({
  ...jest.requireActual('redis'),
  createClient: jest.fn(),
}));
```

## Async Tests

```typescript
// ✅ Async/await
it('should fetch data', async () => {
  const result = await service.getData();
  expect(result).toBeDefined();
});

// ✅ Async error
it('should throw error', async () => {
  await expect(service.getData()).rejects.toThrow(Error);
});

// ✅ Resolves
it('should resolve with data', async () => {
  await expect(service.getData()).resolves.toEqual({ data: [] });
});
```

## Assertions

```typescript
// ✅ Equality
expect(result).toEqual(expected);
expect(result).toMatchObject({ id: '1' });

// ✅ Truthy/falsy
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();

// ✅ Numbers
expect(count).toBe(10);
expect(count).toBeGreaterThan(5);
expect(count).toBeLessThan(20);
expect(count).toBeCloseTo(3.14, 2);

// ✅ Strings
expect(text).toContain('substring');
expect(text).toMatch(/regex/);

// ✅ Arrays
expect(array).toHaveLength(5);
expect(array).toContain('item');
expect(array).toEqual(expect.arrayContaining([1, 2, 3]));

// ✅ Objects
expect(obj).toHaveProperty('name');
expect(obj).toMatchObject({ name: 'John' });

// ✅ Functions
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(1);
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');

// ✅ Errors
expect(fn).toThrow();
expect(fn).toThrow(Error);
expect(fn).toThrow('error message');
expect(fn).toThrow(/regex/);
```

## Test Data Fixtures

```typescript
// fixtures/clients.ts
export const mockClient = {
  id: 'client-1',
  tenantId: 'tenant-1',
  companyName: 'Test Company',
  contactName: 'John Doe',
  status: 'active',
};

export const mockClients = [mockClient];

// Test usage
import { mockClient } from '../fixtures/clients';
```

## Prisma Mock

```typescript
// tests/__mocks__/prisma.ts
import { PrismaClient } from '@prisma/client';

const mockPrismaClient = {
  client: {
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

## HTTP Testing (Supertest)

```typescript
import request from 'supertest';
import app from '../app';

it('should GET /clients', async () => {
  const response = await request(app).get('/clients').set('x-tenant-id', 'tenant-1').expect(200);

  expect(response.body).toEqual({
    success: true,
    data: expect.any(Object),
  });
});
```

## Configuration

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

## Commands

```bash
npm run test:api                    # Run API tests
npm run test:web                    # Run Web tests
npm run test:api -- --watch         # Watch mode
npm run test:api -- --coverage      # Coverage report
npm run test:api -- clients.service.test.ts  # Specific test file
```

## Related Skills

- `migestion-test-api` - API testing patterns
- `migestion-test-web` - E2E testing patterns
