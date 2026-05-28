---
name: nestjs-testing
description: Creates unit and e2e tests for NestJS applications using Jest and Supertest. Includes patterns for testing services, controllers, guards, and e2e tests with testcontainers.
---

# NestJS Testing Skill

Instructions for testing NestJS applications with Jest, including unit tests for services, controllers, guards, pipes, and interceptors, as well as e2e tests for HTTP endpoints.

## Tech Stack

- **Framework**: NestJS with `@nestjs/testing`
- **Testing Framework**: Jest with `ts-jest`
- **HTTP Testing**: Supertest
- **Mocking**: `@golevelup/ts-jest` for deep mocking with `createMock<T>()`
- **E2E Database**: `@testcontainers/postgresql` for isolated database tests
- **Optional**: `@suites/unit` for fully isolated unit testing

## Core Principles

### 1. Test Structure

- Place unit tests alongside source files with `.spec.ts` extension (e.g., `cats.service.spec.ts`)
- Place e2e tests in `test/` directory with `.e2e-spec.ts` extension (e.g., `cats.e2e-spec.ts`)
- Use `describe` blocks to group related tests by feature or method
- Use `it` for individual test cases with clear descriptions

### 2. Unit Tests vs E2E Tests

- **Unit Tests**: Test individual classes in isolation with mocked dependencies. Fast, focused, run frequently.
- **E2E Tests**: Test complete application flow through HTTP endpoints with real database (via testcontainers). Slower, comprehensive, validate integration.

### 3. Mocking Strategies

- Use `@golevelup/ts-jest`'s `createMock<T>()` for type-safe deep mocking (recommended)
- Use manual mocks with `jest.fn()` for simple cases
- Use `jest.spyOn()` for mocking specific methods on real objects
- Use `useValue`, `useClass`, or `useFactory` in `Test.createTestingModule()` to provide mocks
- Use `overrideProvider()`, `overrideGuard()`, `overrideInterceptor()`, `overrideFilter()`, `overridePipe()`, and `overrideModule()` for overriding in e2e tests

### 4. Test Coverage

- Test success paths
- Test error handling and edge cases
- Verify side effects on dependencies (method calls, arguments)
- Test both happy paths and failure scenarios

### 5. Test Lifecycle

- Use `beforeAll()` for one-time setup (app initialization, container startup)
- Use `beforeEach()` for per-test setup (fresh mocks, reset state)
- Use `afterAll()` for cleanup (close app, stop containers)
- Use `afterEach()` for per-test cleanup if needed

## Testing Patterns

### Unit Testing Services with createMock (Recommended)

Use `@golevelup/ts-jest`'s `createMock<T>()` for type-safe, deep mocking:

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { createMock, DeepMocked } from '@golevelup/ts-jest';
import { CatsService } from './cats.service';
import { CatsRepository } from './cats.repository';

describe('CatsService', () => {
  let service: CatsService;
  let repository: DeepMocked<CatsRepository>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        CatsService,
        {
          provide: CatsRepository,
          useValue: createMock<CatsRepository>(),
        },
      ],
    }).compile();

    service = module.get<CatsService>(CatsService);
    repository = module.get(CatsRepository);
  });

  it('should return all cats', async () => {
    const expectedCats = [{ id: 1, name: 'Fluffy' }];
    repository.findAll.mockResolvedValue(expectedCats);

    const result = await service.findAll();

    expect(result).toEqual(expectedCats);
    expect(repository.findAll).toHaveBeenCalled();
  });

  it('should throw NotFoundException when cat not found', async () => {
    repository.findOne.mockResolvedValue(null);

    await expect(service.findOne(999)).rejects.toThrow();
  });
});
```

### Unit Testing Services with Manual Mocks

For simpler cases, use manual mock objects:

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { CatsService } from './cats.service';
import { CatsRepository } from './cats.repository';

describe('CatsService', () => {
  let service: CatsService;
  let repository: jest.Mocked<CatsRepository>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        CatsService,
        {
          provide: CatsRepository,
          useValue: {
            findAll: jest.fn(),
            findOne: jest.fn(),
            create: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get<CatsService>(CatsService);
    repository = module.get(CatsRepository);
  });

  it('should find a cat by id', async () => {
    const expectedCat = { id: 1, name: 'Fluffy' };
    repository.findOne.mockResolvedValue(expectedCat);

    const result = await service.findOne(1);

    expect(result).toEqual(expectedCat);
    expect(repository.findOne).toHaveBeenCalledWith(1);
  });
});
```

### Unit Testing Controllers

```typescript
import { Test, TestingModule } from '@nestjs/testing';
import { createMock, DeepMocked } from '@golevelup/ts-jest';
import { CatsController } from './cats.controller';
import { CatsService } from './cats.service';

describe('CatsController', () => {
  let controller: CatsController;
  let service: DeepMocked<CatsService>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [CatsController],
      providers: [
        {
          provide: CatsService,
          useValue: createMock<CatsService>(),
        },
      ],
    }).compile();

    controller = module.get<CatsController>(CatsController);
    service = module.get(CatsService);
  });

  it('should return all cats', async () => {
    const expectedCats = [{ id: 1, name: 'Fluffy' }];
    service.findAll.mockResolvedValue(expectedCats);

    const result = await controller.findAll();

    expect(result).toEqual(expectedCats);
  });

  it('should create a cat', async () => {
    const createCatDto = { name: 'Fluffy', age: 3 };
    const expectedCat = { id: 1, ...createCatDto };
    service.create.mockResolvedValue(expectedCat);

    const result = await controller.create(createCatDto);

    expect(result).toEqual(expectedCat);
    expect(service.create).toHaveBeenCalledWith(createCatDto);
  });
});
```

### Testing Guards with createMock

```typescript
import { createMock } from '@golevelup/ts-jest';
import { ExecutionContext, UnauthorizedException } from '@nestjs/common';
import { AuthGuard } from './auth.guard';

describe('AuthGuard', () => {
  let guard: AuthGuard;

  beforeEach(() => {
    guard = new AuthGuard();
  });

  it('should return true when user is authenticated', () => {
    const mockContext = createMock<ExecutionContext>({
      switchToHttp: () => ({
        getRequest: () => ({
          user: { id: 'user-123' },
          params: {},
        }),
      }),
    });

    expect(guard.canActivate(mockContext)).toBe(true);
  });

  it('should throw UnauthorizedException when user is not authenticated', () => {
    const mockContext = createMock<ExecutionContext>({
      switchToHttp: () => ({
        getRequest: () => ({
          user: undefined,
        }),
      }),
    });

    expect(() => guard.canActivate(mockContext)).toThrow(UnauthorizedException);
  });
});
```

### Testing Guards with Manual Mocks

```typescript
import { ExecutionContext, UnauthorizedException } from '@nestjs/common';
import { MeGuard } from './me.guard';

describe('MeGuard', () => {
  let guard: MeGuard;

  beforeEach(() => {
    guard = new MeGuard();
  });

  it('should return true when user requests their own ID', () => {
    const mockContext = {
      switchToHttp: jest.fn().mockReturnValue({
        getRequest: jest.fn().mockReturnValue({
          user: { cerbereId: 'user-123' },
          params: { id: 'user-123' },
        }),
      }),
    } as unknown as ExecutionContext;

    expect(guard.canActivate(mockContext)).toBe(true);
  });

  it('should throw when user is not authenticated', () => {
    const mockContext = {
      switchToHttp: jest.fn().mockReturnValue({
        getRequest: jest.fn().mockReturnValue({
          user: undefined,
        }),
      }),
    } as unknown as ExecutionContext;

    expect(() => guard.canActivate(mockContext)).toThrow(UnauthorizedException);
  });
});
```

### Testing Pipes

```typescript
import { BadRequestException } from '@nestjs/common';
import { ValidationPipe } from './validation.pipe';

describe('ValidationPipe', () => {
  let pipe: ValidationPipe;

  beforeEach(() => {
    pipe = new ValidationPipe();
  });

  it('should pass valid data through', () => {
    const data = { name: 'Fluffy', age: 3 };
    const result = pipe.transform(data, { type: 'body', metatype: Object });

    expect(result).toEqual(data);
  });

  it('should throw BadRequestException on invalid data', () => {
    const data = { name: '', age: -1 };

    expect(() => pipe.transform(data, { type: 'body', metatype: Object }))
      .toThrow(BadRequestException);
  });
});
```

### E2E Testing with Testcontainers

Use testcontainers for isolated database testing:

```typescript
import * as dotenv from 'dotenv';
import path from 'path';

dotenv.config({
  path: path.join(__dirname, 'test.envfile'),
  override: true,
});

import { INestApplication } from '@nestjs/common';
import { Test, TestingModule } from '@nestjs/testing';
import request from 'supertest';
import type { App } from 'supertest/types';
import cookieParser from 'cookie-parser';
import { ApiModule } from '../src/api/api.module';
import { startPostgresContainer, getPostgresConnectionUri } from './testcontainer.config';
import { initTestContainerImports } from './init/initTestContainer';

describe('Cats (e2e)', () => {
  let app: INestApplication<App>;

  beforeAll(async () => {
    await startPostgresContainer();
    const connectionUri = getPostgresConnectionUri();

    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [...initTestContainerImports(connectionUri), ApiModule],
    })
      .overrideProvider(PGBOSS)
      .useValue(null) // Mock pg-boss in e2e tests
      .compile();

    app = moduleFixture.createNestApplication({ logger: false });
    app.use(cookieParser());
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it('/GET cats (200)', () => {
    return request(app.getHttpServer())
      .get('/cats')
      .expect(200);
  });

  it('/POST cats (201)', () => {
    const createCatDto = { name: 'Fluffy', age: 3 };

    return request(app.getHttpServer())
      .post('/cats')
      .send(createCatDto)
      .expect(201);
  });
});
```

### E2E Testing with Module Override

Use `overrideModule()` to replace entire modules with mocks:

```typescript
import { Module } from '@nestjs/common';
import { Test, TestingModule } from '@nestjs/testing';
import { createMock } from '@golevelup/ts-jest';
import { AppModule } from '../src/app.module';
import { InfraModule } from '../src/infra/infra.module';

// Create a mock module to replace the real one
@Module({
  providers: [
    {
      provide: ExternalService,
      useValue: createMock<ExternalService>(),
    },
  ],
  exports: [ExternalService],
})
class MockInfraModule {}

describe('App (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    })
      .overrideModule(InfraModule)
      .useModule(MockInfraModule)
      .compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });
});
```

### Overriding Providers, Guards, and Filters

```typescript
const moduleRef = await Test.createTestingModule({
  imports: [AppModule],
})
  // Override a provider with a mock value
  .overrideProvider(CatsService)
  .useValue(createMock<CatsService>())
  // Override a guard
  .overrideGuard(AuthGuard)
  .useValue({ canActivate: () => true })
  // Override a filter
  .overrideFilter(HttpExceptionFilter)
  .useClass(MockExceptionFilter)
  // Override an interceptor
  .overrideInterceptor(LoggingInterceptor)
  .useValue({ intercept: (ctx, next) => next.handle() })
  .compile();
```

### Isolated Unit Testing with Suites

For fully isolated unit tests, use `@suites/unit`:

```typescript
import { TestBed, type Mocked } from '@suites/unit';
import { UserService } from './user.service';
import { UserRepository } from './user.repository';
import { Logger } from '@nestjs/common';

describe('UserService (Suites)', () => {
  let service: UserService;
  let repository: Mocked<UserRepository>;
  let logger: Mocked<Logger>;

  beforeAll(async () => {
    // solitary() automatically mocks all dependencies
    const { unit, unitRef } = await TestBed.solitary(UserService).compile();

    service = unit;
    repository = unitRef.get(UserRepository);
    logger = unitRef.get(Logger);
  });

  it('should find user by id', async () => {
    const user = { id: '1', email: 'test@example.com', name: 'Test' };
    repository.findById.mockResolvedValue(user);

    const result = await service.findById('1');

    expect(result).toEqual(user);
    expect(logger.log).toHaveBeenCalled();
  });
});
```

## Workflow

1. **Identify**: Determine what needs testing (service, controller, guard, etc.)
2. **Setup**: Create test file alongside source with `.spec.ts` extension
3. **Mock**: Use `createMock<T>()` or manual mocks for dependencies
4. **Implement**: Write test cases covering success, error, and edge cases
5. **Validate**: Run with `npm test` (unit) or `npm run test:e2e` (e2e)

## Common Utilities

### createMock for ExecutionContext

```typescript
import { createMock } from '@golevelup/ts-jest';
import { ExecutionContext } from '@nestjs/common';

// Full type-safe mock with all methods stubbed
const mockContext = createMock<ExecutionContext>();

// With custom implementations
const mockContextWithData = createMock<ExecutionContext>({
  switchToHttp: () => ({
    getRequest: () => ({
      user: { id: 'user-123' },
      headers: { authorization: 'Bearer token' },
    }),
  }),
});
```

### Manual ExecutionContext Mock

```typescript
import { ExecutionContext } from '@nestjs/common';

function createMockExecutionContext(request: any): ExecutionContext {
  return {
    switchToHttp: () => ({
      getRequest: () => request,
      getResponse: () => ({}),
    }),
    getHandler: jest.fn(),
    getClass: jest.fn(),
  } as unknown as ExecutionContext;
}
```

### Mocking Request-Scoped Providers

```typescript
import { ContextIdFactory } from '@nestjs/core';

// Force all requests to use the same DI sub-tree
const contextId = ContextIdFactory.create();
jest
  .spyOn(ContextIdFactory, 'getByRequest')
  .mockImplementation(() => contextId);

// Resolve scoped providers
const scopedService = await moduleRef.resolve(ScopedService);
```

## Testing Checklist

- [ ] All public methods are tested
- [ ] Success paths are tested
- [ ] Error paths and exceptions are tested
- [ ] Edge cases are covered
- [ ] Mocks are properly typed (`DeepMocked<T>` or `jest.Mocked<T>`)
- [ ] Tests are isolated (no shared mutable state)
- [ ] Test file naming: `*.spec.ts` for unit, `*.e2e-spec.ts` for e2e
- [ ] E2E tests use testcontainers for database isolation
- [ ] External services are mocked (pg-boss, S3, SFTP, etc.)
- [ ] Tests pass locally before committing
