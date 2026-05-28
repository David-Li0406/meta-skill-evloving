---
name: test-patterns
description: Use when writing tests, understanding AAA pattern, or setting up Testcontainers. CSO keywords: jest mock, beforeEach, 테스트 작성, AAA 패턴, testcontainers, 통합 테스트, integration test
---

# Test Patterns Skill

NestJS 프로젝트에서 효과적인 테스트를 작성하기 위한 패턴과 베스트 프랙티스를 제공합니다.

## 활성화 조건

다음 상황에서 이 스킬이 자동 활성화됩니다:

- 테스트 파일 (*.spec.ts, *.test.ts) 작성/수정 시
- `/test-scaffold` 커맨드 실행 시
- "테스트 작성", "테스트 패턴" 관련 요청 시

## 핵심 원칙

### 테스트 피라미드

```
         /\
        /E2E\       ← 적게 (느림, 비쌈)
       /──────\
      /Integration\  ← 중간
     /──────────────\
    /   Unit Tests   \  ← 많이 (빠름, 저렴)
   /──────────────────\
```

- **Unit Tests**: 70-80% - 개별 함수/클래스 격리 테스트
- **Integration Tests**: 15-20% - 모듈 간 상호작용
- **E2E Tests**: 5-10% - 전체 사용자 시나리오

### AAA 패턴 (Arrange-Act-Assert)

모든 테스트는 세 단계로 구성합니다:

```typescript
it('should return user when found', async () => {
  // Arrange - 테스트 데이터 및 Mock 설정
  const userId = 'user-123';
  const expectedUser = { id: userId, name: 'Test' };
  mockRepository.findById.mockResolvedValue(expectedUser);

  // Act - 테스트 대상 실행
  const result = await service.findById(userId);

  // Assert - 결과 검증
  expect(result).toEqual(expectedUser);
  expect(mockRepository.findById).toHaveBeenCalledWith(userId);
});
```

### Given-When-Then 패턴 (대안)

BDD 스타일 선호 시:

```typescript
describe('Given a valid user ID', () => {
  describe('When findById is called', () => {
    it('Then it should return the user', async () => {
      // ...
    });
  });
});
```

## NestJS Testing Module

### 기본 구조

```typescript
import { Test, TestingModule } from '@nestjs/testing';

describe('UserService', () => {
  let service: UserService;
  let module: TestingModule;

  beforeEach(async () => {
    module = await Test.createTestingModule({
      providers: [
        UserService,
        {
          provide: UserRepository,
          useValue: mockUserRepository,
        },
      ],
    }).compile();

    service = module.get<UserService>(UserService);
  });

  afterEach(async () => {
    await module.close();  // 리소스 정리 필수
  });
});
```

### Mock 생성 패턴

```typescript
// 타입 안전한 Mock
const mockRepository = {
  findById: jest.fn(),
  save: jest.fn(),
  delete: jest.fn(),
} as jest.Mocked<Pick<UserRepository, 'findById' | 'save' | 'delete'>>;

// 또는 createMock 유틸리티
function createMockRepository<T>(): jest.Mocked<T> {
  return {
    // 공통 메서드들
  } as any;
}
```

## References

자세한 패턴은 다음 파일들을 참조하세요:

- `references/aaa-pattern.md` - AAA 패턴 상세 가이드
- `references/mocking-guide.md` - Mock 전략 및 패턴
- `references/nestjs-testing.md` - NestJS 테스팅 모듈 심화

## 피해야 할 안티패턴

### 1. 과도한 Mock

```typescript
// ❌ Bad: 모든 것을 Mock
mockService.validateUser.mockReturnValue(true);
mockService.hashPassword.mockReturnValue('hashed');
mockService.createUser.mockReturnValue(user);
// 실제 로직을 전혀 테스트하지 않음

// ✅ Good: 외부 의존성만 Mock
mockRepository.save.mockResolvedValue(user);
// 서비스의 실제 로직은 테스트
```

### 2. 구현 세부사항 테스트

```typescript
// ❌ Bad: 내부 구현에 의존
expect(service['privateMethod']).toHaveBeenCalled();

// ✅ Good: 공개 인터페이스만 테스트
expect(result).toEqual(expectedOutput);
```

### 3. 테스트 간 상태 공유

```typescript
// ❌ Bad: 공유 상태
let sharedUser;
beforeAll(() => { sharedUser = createUser(); });

// ✅ Good: 테스트마다 새 상태
beforeEach(() => {
  // 각 테스트마다 초기화
});
```

## 커버리지 가이드라인

| 영역 | 목표 커버리지 | 우선순위 |
|------|--------------|----------|
| 비즈니스 로직 | 90%+ | 높음 |
| 컨트롤러 | 80%+ | 중간 |
| 유틸리티 | 90%+ | 높음 |
| 설정/모듈 | 낮음 | 낮음 |

**중요**: 100% 커버리지가 목표가 아닙니다. 의미 있는 테스트에 집중하세요.

## Integration Testing with Testcontainers

### Testsuite 3.x 구조

```typescript
// 테스트 스위트 구조화
describe('UserModule (Integration)', () => {
  let app: INestApplication;
  let container: StartedPostgreSqlContainer;

  beforeAll(async () => {
    // Testcontainers로 DB 시작
    container = await new PostgreSqlContainer()
      .withDatabase('test_db')
      .start();

    // 동적 환경 변수 설정
    process.env.DATABASE_URL = container.getConnectionUri();

    const moduleRef = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleRef.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    await app.close();
    await container.stop();
  });

  // 테스트 케이스...
});
```

### 주요 Testcontainers

| Container | 용도 | 패키지 |
|-----------|------|--------|
| PostgreSqlContainer | PostgreSQL DB | @testcontainers/postgresql |
| RedisContainer | Redis 캐시 | @testcontainers/redis |
| KafkaContainer | Kafka 메시지큐 | @testcontainers/kafka |
| GenericContainer | 커스텀 컨테이너 | testcontainers |

### References
- `references/testcontainers.md` - Testcontainers 심화 가이드
