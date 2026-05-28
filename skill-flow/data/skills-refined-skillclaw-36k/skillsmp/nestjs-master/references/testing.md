# NestJS Testing Reference

## Setup

```bash
bun add -D @nestjs/testing jest @types/jest ts-jest supertest @types/supertest
```

```typescript
// jest.config.js
module.exports = {
  moduleFileExtensions: ['js', 'json', 'ts'],
  rootDir: 'src',
  testRegex: '.*\\.spec\\.ts$',
  transform: {
    '^.+\\.(t|j)s$': 'ts-jest',
  },
  collectCoverageFrom: ['**/*.(t|j)s', '!**/*.module.ts', '!**/main.ts'],
  coverageDirectory: '../coverage',
  testEnvironment: 'node',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
};
```

## Unit Testing

### Testing Services

```typescript
// user.service.spec.ts
describe('UserService', () => {
  let service: UserService;
  let repository: jest.Mocked<UserRepository>;

  beforeEach(async () => {
    const mockRepository = {
      findById: jest.fn(),
      findByEmail: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UserService,
        {
          provide: UserRepository,
          useValue: mockRepository,
        },
      ],
    }).compile();

    service = module.get<UserService>(UserService);
    repository = module.get(UserRepository);
  });

  describe('findById', () => {
    it('should return user when found', async () => {
      const mockUser = { id: '1', email: 'test@example.com', name: 'Test' };
      repository.findById.mockResolvedValue(mockUser);

      const result = await service.findById('1');

      expect(result).toEqual(mockUser);
      expect(repository.findById).toHaveBeenCalledWith('1');
    });

    it('should throw NotFoundException when user not found', async () => {
      repository.findById.mockResolvedValue(undefined);

      await expect(service.findById('999')).rejects.toThrow(NotFoundException);
    });
  });

  describe('create', () => {
    it('should create user with hashed password', async () => {
      const dto = { email: 'new@example.com', password: 'Password123!' };
      const mockUser = { id: '1', email: dto.email, passwordHash: 'hashed' };

      repository.findByEmail.mockResolvedValue(undefined);
      repository.create.mockResolvedValue(mockUser);

      const result = await service.create(dto);

      expect(result).toEqual(mockUser);
      expect(repository.create).toHaveBeenCalledWith(
        expect.objectContaining({
          email: dto.email,
          passwordHash: expect.any(String),
        }),
      );
    });

    it('should throw ConflictException if email exists', async () => {
      const dto = { email: 'existing@example.com', password: 'Password123!' };
      repository.findByEmail.mockResolvedValue({ id: '1', email: dto.email });

      await expect(service.create(dto)).rejects.toThrow(ConflictException);
    });
  });
});
```

### Testing with Drizzle

```typescript
// user.repository.spec.ts
describe('UserRepository', () => {
  let repository: UserRepository;
  let mockDb: jest.Mocked<DrizzleDB>;

  beforeEach(async () => {
    const mockSelect = jest.fn().mockReturnThis();
    const mockFrom = jest.fn().mockReturnThis();
    const mockWhere = jest.fn().mockReturnThis();
    const mockLimit = jest.fn();

    mockDb = {
      select: mockSelect,
      insert: jest.fn().mockReturnThis(),
      update: jest.fn().mockReturnThis(),
      delete: jest.fn().mockReturnThis(),
    } as any;

    // Chain mocks
    mockSelect.mockReturnValue({ from: mockFrom });
    mockFrom.mockReturnValue({ where: mockWhere });
    mockWhere.mockReturnValue({ limit: mockLimit });

    const module = await Test.createTestingModule({
      providers: [
        UserRepository,
        { provide: DRIZZLE, useValue: mockDb },
      ],
    }).compile();

    repository = module.get(UserRepository);
  });

  it('should find user by id', async () => {
    const mockUser = { id: '1', email: 'test@example.com' };
    // Setup the chain to return the user
    mockDb.select().from(users).where(any).limit.mockResolvedValue([mockUser]);

    const result = await repository.findById('1');

    expect(result).toEqual(mockUser);
  });
});
```

### Testing Guards

```typescript
// roles.guard.spec.ts
describe('RolesGuard', () => {
  let guard: RolesGuard;
  let reflector: Reflector;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [RolesGuard, Reflector],
    }).compile();

    guard = module.get<RolesGuard>(RolesGuard);
    reflector = module.get<Reflector>(Reflector);
  });

  const createMockContext = (user: Partial<AuthUser>): ExecutionContext => {
    return {
      switchToHttp: () => ({
        getRequest: () => ({ user }),
      }),
      getHandler: () => jest.fn(),
      getClass: () => jest.fn(),
    } as unknown as ExecutionContext;
  };

  it('should allow access when no roles required', () => {
    jest.spyOn(reflector, 'getAllAndOverride').mockReturnValue(undefined);
    const context = createMockContext({ id: '1', roles: [] });

    expect(guard.canActivate(context)).toBe(true);
  });

  it('should allow access when user has required role', () => {
    jest.spyOn(reflector, 'getAllAndOverride').mockReturnValue([Role.ADMIN]);
    const context = createMockContext({ id: '1', roles: [Role.ADMIN] });

    expect(guard.canActivate(context)).toBe(true);
  });

  it('should deny access when user lacks required role', () => {
    jest.spyOn(reflector, 'getAllAndOverride').mockReturnValue([Role.ADMIN]);
    const context = createMockContext({ id: '1', roles: [Role.USER] });

    expect(guard.canActivate(context)).toBe(false);
  });
});
```

### Testing Interceptors

```typescript
// transform.interceptor.spec.ts
describe('TransformInterceptor', () => {
  let interceptor: TransformInterceptor<any>;

  beforeEach(() => {
    interceptor = new TransformInterceptor();
  });

  it('should wrap response in standard format', (done) => {
    const mockData = { id: 1, name: 'Test' };
    const mockContext = {} as ExecutionContext;
    const mockHandler: CallHandler = {
      handle: () => of(mockData),
    };

    interceptor.intercept(mockContext, mockHandler).subscribe((result) => {
      expect(result).toEqual({
        success: true,
        data: mockData,
        timestamp: expect.any(String),
      });
      done();
    });
  });
});
```

## Integration Testing

### Testing Controllers with TestingModule

```typescript
// user.controller.spec.ts
describe('UserController', () => {
  let controller: UserController;
  let service: jest.Mocked<UserService>;

  beforeEach(async () => {
    const mockService = {
      findById: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
    };

    const module = await Test.createTestingModule({
      controllers: [UserController],
      providers: [
        { provide: UserService, useValue: mockService },
      ],
    }).compile();

    controller = module.get<UserController>(UserController);
    service = module.get(UserService);
  });

  describe('GET /users/:id', () => {
    it('should return user', async () => {
      const mockUser = { id: '1', email: 'test@example.com' };
      service.findById.mockResolvedValue(mockUser);

      const result = await controller.findOne('1');

      expect(result).toEqual(mockUser);
    });
  });

  describe('POST /users', () => {
    it('should create user', async () => {
      const dto = { email: 'new@example.com', password: 'Password123!' };
      const mockUser = { id: '1', ...dto };
      service.create.mockResolvedValue(mockUser);

      const result = await controller.create(dto);

      expect(result).toEqual(mockUser);
      expect(service.create).toHaveBeenCalledWith(dto);
    });
  });
});
```

## E2E Testing

### Setup

```typescript
// test/app.e2e-spec.ts
describe('AppController (e2e)', () => {
  let app: INestApplication;
  let db: DrizzleDB;

  beforeAll(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    })
      .overrideProvider(DRIZZLE)
      .useValue(testDb) // Use test database
      .compile();

    app = moduleFixture.createNestApplication();

    // Apply same pipes, guards as main.ts
    app.useGlobalPipes(new ValidationPipe({ whitelist: true }));
    app.useGlobalFilters(new AllExceptionsFilter());

    await app.init();

    db = moduleFixture.get(DRIZZLE);
  });

  beforeEach(async () => {
    // Clean database before each test
    await db.delete(users);
  });

  afterAll(async () => {
    await app.close();
  });

  describe('/users', () => {
    describe('POST /users', () => {
      it('should create a user', () => {
        return request(app.getHttpServer())
          .post('/users')
          .send({
            email: 'test@example.com',
            password: 'Password123!',
            name: 'Test User',
          })
          .expect(201)
          .expect((res) => {
            expect(res.body).toMatchObject({
              email: 'test@example.com',
              name: 'Test User',
            });
            expect(res.body).not.toHaveProperty('passwordHash');
          });
      });

      it('should reject invalid email', () => {
        return request(app.getHttpServer())
          .post('/users')
          .send({
            email: 'invalid-email',
            password: 'Password123!',
          })
          .expect(400);
      });

      it('should reject duplicate email', async () => {
        // Create first user
        await request(app.getHttpServer())
          .post('/users')
          .send({
            email: 'test@example.com',
            password: 'Password123!',
          })
          .expect(201);

        // Try to create duplicate
        return request(app.getHttpServer())
          .post('/users')
          .send({
            email: 'test@example.com',
            password: 'Password123!',
          })
          .expect(409);
      });
    });

    describe('GET /users/:id', () => {
      it('should return user', async () => {
        // Create user first
        const createRes = await request(app.getHttpServer())
          .post('/users')
          .send({
            email: 'test@example.com',
            password: 'Password123!',
          });

        return request(app.getHttpServer())
          .get(`/users/${createRes.body.id}`)
          .expect(200)
          .expect((res) => {
            expect(res.body.email).toBe('test@example.com');
          });
      });

      it('should return 404 for non-existent user', () => {
        return request(app.getHttpServer())
          .get('/users/00000000-0000-0000-0000-000000000000')
          .expect(404);
      });
    });
  });
});
```

### Authentication E2E Tests

```typescript
// test/auth.e2e-spec.ts
describe('Auth (e2e)', () => {
  let app: INestApplication;
  let accessToken: string;

  beforeAll(async () => {
    // ... setup
  });

  describe('POST /auth/register', () => {
    it('should register user and return tokens', () => {
      return request(app.getHttpServer())
        .post('/auth/register')
        .send({
          email: 'new@example.com',
          password: 'Password123!',
        })
        .expect(201)
        .expect((res) => {
          expect(res.body).toHaveProperty('accessToken');
          expect(res.body).toHaveProperty('refreshToken');
        });
    });
  });

  describe('POST /auth/login', () => {
    beforeEach(async () => {
      // Create user
      await request(app.getHttpServer())
        .post('/auth/register')
        .send({
          email: 'login@example.com',
          password: 'Password123!',
        });
    });

    it('should login and return tokens', async () => {
      const res = await request(app.getHttpServer())
        .post('/auth/login')
        .send({
          email: 'login@example.com',
          password: 'Password123!',
        })
        .expect(200);

      accessToken = res.body.accessToken;
      expect(accessToken).toBeDefined();
    });

    it('should reject invalid password', () => {
      return request(app.getHttpServer())
        .post('/auth/login')
        .send({
          email: 'login@example.com',
          password: 'WrongPassword!',
        })
        .expect(401);
    });
  });

  describe('Protected routes', () => {
    it('should access protected route with token', async () => {
      // Login first
      const loginRes = await request(app.getHttpServer())
        .post('/auth/login')
        .send({
          email: 'login@example.com',
          password: 'Password123!',
        });

      return request(app.getHttpServer())
        .get('/users/me')
        .set('Authorization', `Bearer ${loginRes.body.accessToken}`)
        .expect(200);
    });

    it('should reject request without token', () => {
      return request(app.getHttpServer())
        .get('/users/me')
        .expect(401);
    });
  });
});
```

## Test Utilities

### Factory Functions

```typescript
// test/factories/user.factory.ts
export const createUserFactory = (overrides?: Partial<NewUser>): NewUser => ({
  email: `test-${Date.now()}@example.com`,
  passwordHash: '$2b$12$hashedpassword',
  name: 'Test User',
  isActive: true,
  ...overrides,
});

// Usage in tests
const user = createUserFactory({ name: 'Custom Name' });
await db.insert(users).values(user);
```

### Database Helpers

```typescript
// test/helpers/database.ts
export async function cleanDatabase(db: DrizzleDB) {
  await db.delete(orderItems);
  await db.delete(orders);
  await db.delete(posts);
  await db.delete(users);
}

export async function seedTestUser(db: DrizzleDB): Promise<User> {
  const [user] = await db
    .insert(users)
    .values(createUserFactory())
    .returning();
  return user;
}
```

### Mock Utilities

```typescript
// test/mocks/types.ts
export type MockType<T> = {
  [P in keyof T]?: jest.Mock;
};

export function createMock<T>(): MockType<T> {
  return {} as MockType<T>;
}
```

## Testing Checklist

- [ ] Unit test all services with mocked dependencies
- [ ] Unit test guards and interceptors
- [ ] Integration test controllers with TestingModule
- [ ] E2E test critical user flows
- [ ] Test validation (invalid input rejection)
- [ ] Test authentication and authorization
- [ ] Test error handling (404, 409, 500)
- [ ] Use test database for E2E tests
- [ ] Clean database between tests
- [ ] Mock external services (email, payment, etc.)
- [ ] Test edge cases and boundary conditions
- [ ] Aim for 80%+ coverage on business logic
