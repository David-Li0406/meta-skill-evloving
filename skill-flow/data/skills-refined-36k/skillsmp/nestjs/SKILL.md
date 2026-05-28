---
name: nestjs
description: NestJS 프레임워크 개발 가이드. NestJS 프로젝트, @nestjs 패키지, .controller.ts, .service.ts, .module.ts, .guard.ts, .pipe.ts, .interceptor.ts, .filter.ts, .gateway.ts 파일 작업 시 자동 적용. 133개의 공식 문서 포함.
---

# NestJS 개발 가이드

NestJS 공식 문서 기반 개발 레퍼런스. 133개 문서 포함.

## 적용 시점

- NestJS 프로젝트 코드 작성/리뷰 시
- @nestjs 패키지 사용 시
- Controllers, Services, Modules, Guards, Pipes, Interceptors 작업 시
- GraphQL, WebSockets, Microservices 구현 시

## 문서 카테고리

### Overview (핵심)

| 파일 | 설명 |
|------|------|
| `docs/introduction.md` | NestJS 소개 |
| `docs/first-steps.md` | 첫 번째 앱 만들기 |
| `docs/controllers.md` | HTTP 요청 처리, 라우팅 |
| `docs/components.md` | 프로바이더, 서비스 |
| `docs/modules.md` | 모듈 시스템 |
| `docs/middlewares.md` | 미들웨어 |
| `docs/exception-filters.md` | 예외 처리 |
| `docs/pipes.md` | 데이터 변환/유효성 검사 |
| `docs/guards.md` | 인증/인가 |
| `docs/interceptors.md` | 요청/응답 가로채기 |
| `docs/custom-decorators.md` | 커스텀 데코레이터 |

### Fundamentals (기초)

| 파일 | 설명 |
|------|------|
| `docs/fundamentals/dependency-injection.md` | 의존성 주입 |
| `docs/fundamentals/async-components.md` | 비동기 프로바이더 |
| `docs/fundamentals/dynamic-modules.md` | 동적 모듈 |
| `docs/fundamentals/provider-scopes.md` | 인스턴스 스코프 |
| `docs/fundamentals/circular-dependency.md` | 순환 의존성 해결 |
| `docs/fundamentals/module-reference.md` | 모듈 참조 |
| `docs/fundamentals/lazy-loading-modules.md` | 지연 로딩 |
| `docs/fundamentals/execution-context.md` | 실행 컨텍스트 |
| `docs/fundamentals/lifecycle-events.md` | 생명주기 이벤트 |
| `docs/fundamentals/discovery-service.md` | 메타데이터 탐색 |
| `docs/fundamentals/platform-agnosticism.md` | 플랫폼 독립성 |
| `docs/fundamentals/unit-testing.md` | 테스트 작성 |

### Techniques (기법)

| 파일 | 설명 |
|------|------|
| `docs/techniques/configuration.md` | 환경 설정 |
| `docs/techniques/sql.md` | 데이터베이스 (TypeORM) |
| `docs/techniques/mongo.md` | MongoDB |
| `docs/techniques/validation.md` | 유효성 검사 |
| `docs/techniques/caching.md` | 캐싱 |
| `docs/techniques/serialization.md` | 직렬화 |
| `docs/techniques/versioning.md` | API 버전 관리 |
| `docs/techniques/task-scheduling.md` | 작업 스케줄링 |
| `docs/techniques/queues.md` | 큐 처리 |
| `docs/techniques/logger.md` | 로깅 |
| `docs/techniques/cookies.md` | 쿠키 |
| `docs/techniques/events.md` | 이벤트 |
| `docs/techniques/compression.md` | 압축 |
| `docs/techniques/file-upload.md` | 파일 업로드 |
| `docs/techniques/streaming-files.md` | 파일 스트리밍 |
| `docs/techniques/http-module.md` | HTTP 요청 |
| `docs/techniques/sessions.md` | 세션 |
| `docs/techniques/mvc.md` | MVC 패턴 |
| `docs/techniques/performance.md` | Fastify 성능 |
| `docs/techniques/server-sent-events.md` | SSE |

### Security (보안)

| 파일 | 설명 |
|------|------|
| `docs/security/authentication.md` | 인증 |
| `docs/security/authorization.md` | 인가 |
| `docs/security/encryption-hashing.md` | 암호화/해싱 |
| `docs/security/helmet.md` | HTTP 헤더 보안 |
| `docs/security/cors.md` | CORS |
| `docs/security/csrf.md` | CSRF 방어 |
| `docs/security/rate-limiting.md` | 요청 제한 |

### GraphQL

| 파일 | 설명 |
|------|------|
| `docs/graphql/quick-start.md` | 시작하기 |
| `docs/graphql/resolvers-map.md` | 리졸버 |
| `docs/graphql/mutations.md` | 뮤테이션 |
| `docs/graphql/subscriptions.md` | 구독 |
| `docs/graphql/scalars.md` | 스칼라 타입 |
| `docs/graphql/directives.md` | 디렉티브 |
| `docs/graphql/interfaces.md` | 인터페이스 |
| `docs/graphql/unions-and-enums.md` | 유니온/이넘 |
| `docs/graphql/field-middleware.md` | 필드 미들웨어 |
| `docs/graphql/mapped-types.md` | 매핑 타입 |
| `docs/graphql/plugins.md` | 플러그인 |
| `docs/graphql/complexity.md` | 복잡도 제한 |
| `docs/graphql/extensions.md` | 확장 |
| `docs/graphql/cli-plugin.md` | CLI 플러그인 |
| `docs/graphql/schema-generator.md` | SDL 생성 |
| `docs/graphql/sharing-models.md` | 모델 공유 |
| `docs/graphql/guards-interceptors.md` | 가드/인터셉터 |
| `docs/graphql/federation.md` | 페더레이션 |

### WebSockets

| 파일 | 설명 |
|------|------|
| `docs/websockets/gateways.md` | 게이트웨이 |
| `docs/websockets/exception-filters.md` | 예외 필터 |
| `docs/websockets/pipes.md` | 파이프 |
| `docs/websockets/guards.md` | 가드 |
| `docs/websockets/interceptors.md` | 인터셉터 |
| `docs/websockets/adapter.md` | 어댑터 |

### Microservices

| 파일 | 설명 |
|------|------|
| `docs/microservices/basics.md` | 기초 |
| `docs/microservices/redis.md` | Redis |
| `docs/microservices/mqtt.md` | MQTT |
| `docs/microservices/nats.md` | NATS |
| `docs/microservices/rabbitmq.md` | RabbitMQ |
| `docs/microservices/kafka.md` | Kafka |
| `docs/microservices/grpc.md` | gRPC |
| `docs/microservices/custom-transport.md` | 커스텀 트랜스포터 |
| `docs/microservices/exception-filters.md` | 예외 필터 |
| `docs/microservices/pipes.md` | 파이프 |
| `docs/microservices/guards.md` | 가드 |
| `docs/microservices/interceptors.md` | 인터셉터 |

### OpenAPI (Swagger)

| 파일 | 설명 |
|------|------|
| `docs/openapi/introduction.md` | 소개 |
| `docs/openapi/types-and-parameters.md` | 타입/파라미터 |
| `docs/openapi/operations.md` | 작업 |
| `docs/openapi/security.md` | 보안 |
| `docs/openapi/mapped-types.md` | 매핑 타입 |
| `docs/openapi/decorators.md` | 데코레이터 |
| `docs/openapi/cli-plugin.md` | CLI 플러그인 |
| `docs/openapi/other-features.md` | 기타 기능 |

### CLI

| 파일 | 설명 |
|------|------|
| `docs/cli/overview.md` | CLI 개요 |
| `docs/cli/workspaces.md` | 모노레포/워크스페이스 |
| `docs/cli/libraries.md` | 라이브러리 |
| `docs/cli/usages.md` | 사용법 |
| `docs/cli/scripts.md` | 스크립트 |

### Recipes (레시피)

| 파일 | 설명 |
|------|------|
| `docs/recipes/repl.md` | REPL |
| `docs/recipes/crud-generator.md` | CRUD 생성기 |
| `docs/recipes/swc.md` | SWC (빠른 컴파일) |
| `docs/recipes/passport.md` | Passport 인증 |
| `docs/recipes/hot-reload.md` | 핫 리로드 |
| `docs/recipes/mikroorm.md` | MikroORM |
| `docs/recipes/sql-typeorm.md` | TypeORM |
| `docs/recipes/mongodb.md` | Mongoose |
| `docs/recipes/sql-sequelize.md` | Sequelize |
| `docs/recipes/router-module.md` | 라우터 모듈 |
| `docs/recipes/terminus.md` | 헬스 체크 |
| `docs/recipes/cqrs.md` | CQRS |
| `docs/recipes/documentation.md` | Compodoc |
| `docs/recipes/prisma.md` | Prisma |
| `docs/recipes/sentry.md` | Sentry |
| `docs/recipes/serve-static.md` | 정적 파일 |
| `docs/recipes/nest-commander.md` | Commander |
| `docs/recipes/async-local-storage.md` | Async Local Storage |
| `docs/recipes/necord.md` | Necord (Discord) |
| `docs/recipes/suites.md` | Suites (Automock) |

### FAQ

| 파일 | 설명 |
|------|------|
| `docs/faq/serverless.md` | 서버리스 |
| `docs/faq/http-adapter.md` | HTTP 어댑터 |
| `docs/faq/keep-alive-connections.md` | Keep-Alive |
| `docs/faq/global-prefix.md` | 전역 접두사 |
| `docs/faq/raw-body.md` | Raw body |
| `docs/faq/hybrid-application.md` | 하이브리드 앱 |
| `docs/faq/multiple-servers.md` | HTTPS/다중 서버 |
| `docs/faq/request-lifecycle.md` | 요청 생명주기 |
| `docs/faq/errors.md` | 일반적 오류 |

### 기타

| 파일 | 설명 |
|------|------|
| `docs/deployment.md` | 배포 |
| `docs/application-context.md` | 독립 실행형 앱 |
| `docs/migration.md` | 마이그레이션 가이드 |
| `docs/devtools/overview.md` | Devtools |
| `docs/devtools/ci-cd.md` | CI/CD 통합 |

---

## 핵심 패턴 요약

### 요청 처리 순서

```
Middleware → Guards → Interceptors (pre) → Pipes → Controller → Interceptors (post) → Exception Filter
```

### 모듈 구조

```typescript
@Module({
  imports: [OtherModule],
  controllers: [UserController],
  providers: [UserService],
  exports: [UserService],
})
export class UserModule {}
```

### 컨트롤러

```typescript
@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Get()
  findAll() { return this.userService.findAll(); }

  @Get(':id')
  findOne(@Param('id', ParseIntPipe) id: number) { return this.userService.findOne(id); }

  @Post()
  create(@Body() dto: CreateUserDto) { return this.userService.create(dto); }
}
```

### 서비스

```typescript
@Injectable()
export class UserService {
  constructor(@InjectRepository(User) private repo: Repository<User>) {}

  findAll() { return this.repo.find(); }
}
```

### 유효성 검사

```typescript
// DTO
export class CreateUserDto {
  @IsString() @MinLength(2) name: string;
  @IsEmail() email: string;
}

// main.ts
app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
```

### 가드

```typescript
@Injectable()
export class AuthGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    return this.validate(request);
  }
}
```

### CLI 명령어

```bash
nest new project-name       # 새 프로젝트
nest g resource users       # CRUD 리소스
nest g module users         # 모듈
nest g controller users     # 컨트롤러
nest g service users        # 서비스
nest g guard auth           # 가드
nest g pipe validation      # 파이프
```

---

## 사용법

상세 내용이 필요하면 `docs/` 폴더의 해당 파일을 Read 도구로 읽으세요.

예시:
- Controllers 상세: `docs/controllers.md`
- TypeORM 설정: `docs/recipes/sql-typeorm.md`
- 인증 구현: `docs/security/authentication.md`
