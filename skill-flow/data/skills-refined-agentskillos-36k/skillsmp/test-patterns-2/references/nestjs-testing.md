# NestJS Testing Module 심화 가이드

NestJS의 Testing Module을 활용한 효과적인 테스트 작성법을 설명합니다.

## Testing Module 기본

### 모듈 생성

```typescript
import { Test, TestingModule } from '@nestjs/testing';

describe('UserService', () => {
  let service: UserService;
  let module: TestingModule;

  beforeEach(async () => {
    module = await Test.createTestingModule({
      providers: [UserService],
    }).compile();

    service = module.get<UserService>(UserService);
  });

  afterEach(async () => {
    // 중요: 리소스 정리
    await module.close();
  });
});
```

### 의존성 주입

```typescript
// 기본 Provider
{
  provide: UserRepository,
  useValue: mockUserRepository,
}

// 클래스 사용
{
  provide: UserRepository,
  useClass: MockUserRepository,
}

// 팩토리 사용
{
  provide: UserRepository,
  useFactory: (configService: ConfigService) => {
    return new UserRepository(configService.get('DB_URL'));
  },
  inject: [ConfigService],
}
```

## Service 테스트

### 기본 구조

```typescript
describe('UserService', () => {
  let service: UserService;
  let repository: jest.Mocked<UserRepository>;

  beforeEach(async () => {
    const mockRepository = {
      findById: jest.fn(),
      save: jest.fn(),
    };

    const module = await Test.createTestingModule({
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
      const user = { id: '1', name: 'Test' };
      repository.findById.mockResolvedValue(user);

      const result = await service.findById('1');

      expect(result).toEqual(user);
    });

    it('should throw NotFoundException when not found', async () => {
      repository.findById.mockResolvedValue(null);

      await expect(service.findById('1')).rejects.toThrow(NotFoundException);
    });
  });
});
```

## Controller 테스트

### 기본 구조

```typescript
describe('UserController', () => {
  let controller: UserController;
  let service: jest.Mocked<UserService>;

  beforeEach(async () => {
    const mockService = {
      findById: jest.fn(),
      create: jest.fn(),
    };

    const module = await Test.createTestingModule({
      controllers: [UserController],
      providers: [
        {
          provide: UserService,
          useValue: mockService,
        },
      ],
    }).compile();

    controller = module.get<UserController>(UserController);
    service = module.get(UserService);
  });

  describe('GET /users/:id', () => {
    it('should return user', async () => {
      const user = { id: '1', name: 'Test' };
      service.findById.mockResolvedValue(user);

      const result = await controller.findById('1');

      expect(result).toEqual(user);
      expect(service.findById).toHaveBeenCalledWith('1');
    });
  });
});
```

## E2E 테스트

### 설정

```typescript
// test/app.e2e-spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../src/app.module';

describe('AppController (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  it('/users (GET)', () => {
    return request(app.getHttpServer())
      .get('/users')
      .expect(200)
      .expect((res) => {
        expect(res.body).toBeInstanceOf(Array);
      });
  });
});
```

### 인증 포함 테스트

```typescript
describe('UserController (e2e)', () => {
  let app: INestApplication;
  let authToken: string;

  beforeAll(async () => {
    // ... app 초기화

    // 테스트용 토큰 발급
    const loginResponse = await request(app.getHttpServer())
      .post('/auth/login')
      .send({ email: 'test@test.com', password: 'password' });

    authToken = loginResponse.body.accessToken;
  });

  it('/users/me (GET) - 인증 필요', () => {
    return request(app.getHttpServer())
      .get('/users/me')
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200);
  });

  it('/users/me (GET) - 인증 없이 401', () => {
    return request(app.getHttpServer())
      .get('/users/me')
      .expect(401);
  });
});
```

## Guard 테스트

```typescript
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

  it('should allow access when user has required role', () => {
    jest.spyOn(reflector, 'get').mockReturnValue(['admin']);

    const context = createMockExecutionContext({
      user: { role: 'admin' },
    });

    expect(guard.canActivate(context)).toBe(true);
  });

  it('should deny access when user lacks required role', () => {
    jest.spyOn(reflector, 'get').mockReturnValue(['admin']);

    const context = createMockExecutionContext({
      user: { role: 'user' },
    });

    expect(guard.canActivate(context)).toBe(false);
  });
});

// Helper
function createMockExecutionContext(request: Partial<Request>): ExecutionContext {
  return {
    switchToHttp: () => ({
      getRequest: () => request,
    }),
    getHandler: () => jest.fn(),
    getClass: () => jest.fn(),
  } as any;
}
```

## Interceptor 테스트

```typescript
describe('LoggingInterceptor', () => {
  let interceptor: LoggingInterceptor;

  beforeEach(() => {
    interceptor = new LoggingInterceptor();
  });

  it('should log request and response', async () => {
    const consoleSpy = jest.spyOn(console, 'log');

    const context = createMockExecutionContext({
      method: 'GET',
      url: '/users',
    });

    const next: CallHandler = {
      handle: () => of({ id: '1', name: 'Test' }),
    };

    await interceptor.intercept(context, next).toPromise();

    expect(consoleSpy).toHaveBeenCalled();
  });
});
```

## Pipe 테스트

```typescript
describe('ParseIntPipe', () => {
  let pipe: ParseIntPipe;

  beforeEach(() => {
    pipe = new ParseIntPipe();
  });

  it('should return number for valid string', () => {
    expect(pipe.transform('123', { type: 'param' })).toBe(123);
  });

  it('should throw BadRequestException for invalid string', () => {
    expect(() => pipe.transform('abc', { type: 'param' }))
      .toThrow(BadRequestException);
  });
});
```

## 테스트 데이터베이스

### In-Memory DB

```typescript
// SQLite in-memory for testing
TypeOrmModule.forRoot({
  type: 'sqlite',
  database: ':memory:',
  entities: [User, Post],
  synchronize: true,
});
```

### Test Containers

```typescript
import { PostgreSqlContainer } from '@testcontainers/postgresql';

describe('UserRepository (integration)', () => {
  let container: StartedPostgreSqlContainer;

  beforeAll(async () => {
    container = await new PostgreSqlContainer().start();
    // container.getConnectionUri()로 연결
  });

  afterAll(async () => {
    await container.stop();
  });
});
```

## 팁

1. **모듈은 항상 close()**: afterEach에서 `await module.close()` 호출
2. **Mock은 beforeEach에서 리셋**: `jest.clearAllMocks()`
3. **E2E는 beforeAll 사용**: 앱 초기화는 한 번만
4. **테스트 격리**: 테스트 간 상태 공유 금지
5. **실제 DB는 Integration에서**: Unit은 Mock, Integration은 실제 DB
