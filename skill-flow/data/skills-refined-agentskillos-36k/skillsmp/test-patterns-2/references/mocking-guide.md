# Mock 전략 및 패턴 가이드

NestJS 테스트에서 효과적인 Mock 전략을 설명합니다.

## Mock vs Stub vs Fake

| 유형 | 설명 | 사용 시점 |
|------|------|----------|
| **Mock** | 호출 여부/횟수/인자 검증 가능 | 상호작용 검증 필요 시 |
| **Stub** | 미리 정의된 값만 반환 | 단순 반환값만 필요 시 |
| **Fake** | 실제 동작하는 가벼운 구현 | 복잡한 로직 테스트 시 |

## Jest Mock 패턴

### 기본 Mock 생성

```typescript
// 객체 Mock
const mockUserRepository = {
  findById: jest.fn(),
  findByEmail: jest.fn(),
  save: jest.fn(),
  update: jest.fn(),
  delete: jest.fn(),
};

// 함수 Mock
const mockHashFunction = jest.fn();
```

### 타입 안전한 Mock

```typescript
// Partial Mock with type safety
const mockUserRepository: jest.Mocked<UserRepository> = {
  findById: jest.fn(),
  findByEmail: jest.fn(),
  save: jest.fn(),
  update: jest.fn(),
  delete: jest.fn(),
} as any;

// 또는 Pick을 사용한 부분 Mock
type UserRepositoryMock = jest.Mocked<Pick<UserRepository, 'findById' | 'save'>>;
```

### Mock 반환값 설정

```typescript
// 단일 반환값
mockRepository.findById.mockReturnValue(user);

// Promise 반환
mockRepository.findById.mockResolvedValue(user);

// Promise 거부
mockRepository.findById.mockRejectedValue(new Error('DB Error'));

// 호출별 다른 반환값
mockRepository.findById
  .mockResolvedValueOnce(user1)
  .mockResolvedValueOnce(user2)
  .mockResolvedValue(null);

// 동적 반환값
mockRepository.findById.mockImplementation((id) => {
  if (id === 'user-1') return Promise.resolve(user1);
  if (id === 'user-2') return Promise.resolve(user2);
  return Promise.resolve(null);
});
```

## NestJS DI Mock 패턴

### Provider Mock

```typescript
const module: TestingModule = await Test.createTestingModule({
  providers: [
    UserService,
    {
      provide: UserRepository,
      useValue: mockUserRepository,
    },
    {
      provide: ConfigService,
      useValue: {
        get: jest.fn((key: string) => {
          const config = {
            JWT_SECRET: 'test-secret',
            JWT_EXPIRY: '1h',
          };
          return config[key];
        }),
      },
    },
  ],
}).compile();
```

### Class Mock

```typescript
// 클래스 전체 Mock
jest.mock('./user.repository');

// 특정 메서드만 Mock
jest.spyOn(userRepository, 'findById').mockResolvedValue(user);
```

### External Module Mock

```typescript
// 외부 모듈 Mock
jest.mock('@nestjs/axios', () => ({
  HttpService: jest.fn().mockImplementation(() => ({
    get: jest.fn(),
    post: jest.fn(),
  })),
}));
```

## Guard/Interceptor Mock

### Guard Mock

```typescript
const module: TestingModule = await Test.createTestingModule({
  controllers: [UserController],
  providers: [
    {
      provide: APP_GUARD,
      useValue: { canActivate: () => true },
    },
  ],
}).compile();
```

### ExecutionContext Mock

```typescript
const mockExecutionContext: ExecutionContext = {
  switchToHttp: () => ({
    getRequest: () => ({
      user: { id: 'user-123', role: 'admin' },
      headers: { authorization: 'Bearer token' },
    }),
    getResponse: () => ({}),
  }),
  getClass: () => UserController,
  getHandler: () => jest.fn(),
} as any;
```

## Repository Mock 패턴

### TypeORM Repository Mock

```typescript
const mockRepository = {
  find: jest.fn(),
  findOne: jest.fn(),
  save: jest.fn(),
  update: jest.fn(),
  delete: jest.fn(),
  createQueryBuilder: jest.fn(() => ({
    where: jest.fn().mockReturnThis(),
    andWhere: jest.fn().mockReturnThis(),
    orderBy: jest.fn().mockReturnThis(),
    skip: jest.fn().mockReturnThis(),
    take: jest.fn().mockReturnThis(),
    getMany: jest.fn().mockResolvedValue([]),
    getOne: jest.fn().mockResolvedValue(null),
  })),
};
```

### QueryBuilder Mock

```typescript
// 체이닝 지원 Mock
const createQueryBuilderMock = () => {
  const qb = {
    where: jest.fn().mockReturnThis(),
    andWhere: jest.fn().mockReturnThis(),
    orWhere: jest.fn().mockReturnThis(),
    orderBy: jest.fn().mockReturnThis(),
    skip: jest.fn().mockReturnThis(),
    take: jest.fn().mockReturnThis(),
    select: jest.fn().mockReturnThis(),
    leftJoin: jest.fn().mockReturnThis(),
    getMany: jest.fn(),
    getOne: jest.fn(),
    getCount: jest.fn(),
  };
  return qb;
};
```

## Mock 리셋 및 정리

```typescript
describe('UserService', () => {
  beforeEach(() => {
    // 각 테스트 전 Mock 리셋
    jest.clearAllMocks();
  });

  afterEach(() => {
    // 모든 Mock 리셋 (구현 포함)
    jest.resetAllMocks();
  });

  afterAll(() => {
    // 모든 Mock 복원
    jest.restoreAllMocks();
  });
});
```

## 피해야 할 패턴

### 1. 과도한 Mock

```typescript
// ❌ Bad: 테스트 대상의 내부 로직까지 Mock
mockService.validateInput.mockReturnValue(true);
mockService.processData.mockReturnValue(result);
mockService.formatOutput.mockReturnValue(formatted);
// 실제로 테스트하는 게 없음!

// ✅ Good: 외부 의존성만 Mock
mockRepository.save.mockResolvedValue(entity);
// 서비스의 validate, process, format 로직은 실제로 실행
```

### 2. 구현 세부사항에 의존

```typescript
// ❌ Bad: 내부 구현에 의존
expect(mockRepository.save).toHaveBeenCalledWith({
  ...dto,
  createdAt: expect.any(Date),
  updatedAt: expect.any(Date),
  version: 1,
  // 내부 구현이 바뀌면 테스트 깨짐
});

// ✅ Good: 결과에 집중
expect(result.id).toBeDefined();
expect(result.email).toBe(dto.email);
```
