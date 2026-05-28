# Testing Guide - Backend Testing Strategies

Complete guide to testing backend services with Jest and best practices.

## Table of Contents

- [Unit Testing](#unit-testing)
- [Integration Testing](#integration-testing)
- [Mocking Strategies](#mocking-strategies)
- [Test Data Management](#test-data-management)
- [Testing Authenticated Routes](#testing-authenticated-routes)
- [Coverage Targets](#coverage-targets)

---

## Unit Testing

### Test Structure

```typescript
// services/userService.test.ts
import { UserService } from './userService';
import { UserRepository } from '../repositories/UserRepository';

jest.mock('../repositories/UserRepository');

describe('UserService', () => {
    let service: UserService;
    let mockRepository: jest.Mocked<UserRepository>;

    beforeEach(() => {
        mockRepository = {
            findByEmail: jest.fn(),
            create: jest.fn(),
        } as any;

        service = new UserService();
        (service as any).userRepository = mockRepository;
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    describe('create', () => {
        it('should throw error if email exists', async () => {
            mockRepository.findByEmail.mockResolvedValue({ id: '123' });

            await expect(service.create({
                email: 'test@test.com',
                name: 'Test'
            })).rejects.toThrow('Email already exists');
        });

        it('should create user if email is unique', async () => {
            mockRepository.findByEmail.mockResolvedValue(null);
            mockRepository.create.mockResolvedValue({ 
                id: '123', 
                email: 'test@test.com' 
            });

            const result = await service.create({
                email: 'test@test.com',
                name: 'Test'
            });

            expect(result.id).toBe('123');
            expect(mockRepository.create).toHaveBeenCalledWith({
                email: 'test@test.com',
                name: 'Test'
            });
        });
    });
});
```

### Naming Conventions

```typescript
describe('ServiceName', () => {
    describe('methodName', () => {
        it('should [expected behavior] when [condition]', () => {});
        it('should throw [error] when [condition]', () => {});
    });
});
```

---

## Integration Testing

### Database Integration Test

```typescript
// integration/user.integration.test.ts
import { PrismaClient } from '@prisma/client';
import { UserService } from '../services/UserService';

describe('User Integration', () => {
    let prisma: PrismaClient;
    let userService: UserService;

    beforeAll(async () => {
        prisma = new PrismaClient();
        userService = new UserService();
    });

    afterAll(async () => {
        await prisma.$disconnect();
    });

    beforeEach(async () => {
        // Clean test data
        await prisma.user.deleteMany({
            where: { email: { contains: '@test.com' } }
        });
    });

    it('should create and retrieve user', async () => {
        const created = await userService.create({
            email: 'integration@test.com',
            name: 'Integration Test'
        });

        const retrieved = await userService.findById(created.id);
        expect(retrieved?.email).toBe('integration@test.com');
    });
});
```

---

## Mocking Strategies

### Mock External Services

```typescript
// Mock Sentry
jest.mock('@sentry/node', () => ({
    captureException: jest.fn(),
    init: jest.fn(),
}));

// Mock external API
jest.mock('../services/ExternalApiService', () => ({
    ExternalApiService: {
        fetchData: jest.fn().mockResolvedValue({ data: 'mocked' }),
    },
}));
```

### Mock Database

```typescript
// Mock PrismaService
jest.mock('../database/PrismaService', () => ({
    PrismaService: {
        main: {
            user: {
                findUnique: jest.fn(),
                create: jest.fn(),
                update: jest.fn(),
                delete: jest.fn(),
            },
        },
    },
}));
```

### Partial Mocks

```typescript
// Keep some real implementations
jest.mock('../utils/helpers', () => ({
    ...jest.requireActual('../utils/helpers'),
    sendEmail: jest.fn().mockResolvedValue(true),
}));
```

---

## Test Data Management

### Test Factories

```typescript
// test/factories/userFactory.ts
export function createTestUser(overrides: Partial<User> = {}): User {
    return {
        id: 'test-uuid',
        email: 'test@test.com',
        name: 'Test User',
        role: 'USER',
        createdAt: new Date(),
        updatedAt: new Date(),
        ...overrides,
    };
}

// Usage
const user = createTestUser({ role: 'ADMIN' });
```

### Test Database Seeding

```typescript
// test/setup/seed.ts
export async function seedTestData(prisma: PrismaClient) {
    await prisma.user.createMany({
        data: [
            { email: 'admin@test.com', name: 'Admin', role: 'ADMIN' },
            { email: 'user@test.com', name: 'User', role: 'USER' },
        ],
    });
}

export async function cleanTestData(prisma: PrismaClient) {
    await prisma.user.deleteMany({
        where: { email: { contains: '@test.com' } }
    });
}
```

---

## Testing Authenticated Routes

### Mock Authentication Middleware

```typescript
// Mock auth middleware
jest.mock('../middleware/AuthMiddleware', () => ({
    AuthMiddleware: {
        verifyToken: (req, res, next) => {
            res.locals.user = {
                id: 'test-user-id',
                email: 'test@test.com',
                role: 'USER',
            };
            next();
        },
    },
}));
```

### Test with Supertest

```typescript
import request from 'supertest';
import app from '../app';

describe('User API', () => {
    it('should return 401 without token', async () => {
        const response = await request(app)
            .get('/api/users')
            .expect(401);

        expect(response.body.error).toBe('Unauthorized');
    });

    it('should return users with valid token', async () => {
        const response = await request(app)
            .get('/api/users')
            .set('Authorization', 'Bearer valid-test-token')
            .expect(200);

        expect(response.body.success).toBe(true);
    });
});
```

---

## Coverage Targets

### Recommended Coverage

- **Unit Tests**: 70%+ coverage
- **Integration Tests**: Critical paths covered
- **E2E Tests**: Happy paths covered

### Run Coverage

```bash
npm test -- --coverage
```

### Jest Configuration

```json
{
    "jest": {
        "collectCoverageFrom": [
            "src/**/*.ts",
            "!src/**/*.test.ts",
            "!src/**/*.d.ts"
        ],
        "coverageThreshold": {
            "global": {
                "branches": 70,
                "functions": 70,
                "lines": 70,
                "statements": 70
            }
        }
    }
}
```

---

**Related Files:**
- [SKILL.md](../SKILL.md)
- [async-and-errors.md](async-and-errors.md)
- [validation-patterns.md](validation-patterns.md)
