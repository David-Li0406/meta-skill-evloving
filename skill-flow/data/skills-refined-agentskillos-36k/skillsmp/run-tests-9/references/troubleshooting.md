# Test Troubleshooting

> 일반적인 테스트 문제 해결 가이드

## 컴파일 오류

### 1. Mock 라이브러리 누락

**증상:**
```
e: Unresolved reference: MockK
e: Unresolved reference: every
```

**해결:**
```kotlin
// build.gradle.kts
testImplementation("io.mockk:mockk:1.13.8")
testImplementation("com.ninja-squad:springmockk:4.0.2")
```

### 2. Reactor Test 누락

**증상:**
```
e: Unresolved reference: StepVerifier
```

**해결:**
```kotlin
testImplementation("io.projectreactor:reactor-test")
```

### 3. Kotlin 코루틴 테스트

**증상:**
```
e: Suspend function can only be called from a coroutine or another suspend function
```

**해결:**
```kotlin
testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test")

// 테스트에서
@Test
fun `test suspend function`() = runTest {
    val result = suspendFunction()
    assertThat(result).isNotNull()
}
```

## 런타임 오류

### 1. Mock 초기화 실패

**증상:**
```
kotlin.UninitializedPropertyAccessException: lateinit property has not been initialized
```

**해결:**
```kotlin
@ExtendWith(MockKExtension::class)  // 이 어노테이션 추가
class MyTest {
    @MockK
    lateinit var repository: Repository

    @BeforeEach
    fun setUp() {
        MockKAnnotations.init(this)  // 또는 명시적 초기화
    }
}
```

### 2. WebFlux 테스트 컨텍스트 오류

**증상:**
```
No qualifying bean of type 'UserService' available
```

**해결:**
```kotlin
@WebFluxTest(UserController::class)
@Import(SecurityConfig::class)  // 필요한 설정 Import
class UserControllerTest {

    @MockkBean  // @MockK가 아닌 @MockkBean 사용
    private lateinit var userService: UserService
}
```

### 3. R2DBC 연결 실패

**증상:**
```
R2dbcNonTransientResourceException: Connection refused
```

**해결:**
```yaml
# application-test.yml
spring:
  r2dbc:
    url: r2dbc:h2:mem:///testdb;DB_CLOSE_DELAY=-1  # 인메모리 H2 사용
```

### 4. Reactive Stream 타임아웃

**증상:**
```
java.lang.AssertionError: VerifySubscriber timed out
```

**해결:**
```kotlin
// 타임아웃 증가
StepVerifier.create(slowMono)
    .expectNextCount(1)
    .verifyComplete(Duration.ofSeconds(30))

// 또는 가상 시간 사용
StepVerifier.withVirtualTime { delayedMono }
    .thenAwait(Duration.ofSeconds(10))
    .expectNext("result")
    .verifyComplete()
```

## 테스트 격리 문제

### 1. 테스트 간 상태 공유

**증상:**
- 개별 실행 시 통과, 전체 실행 시 실패
- 테스트 순서에 따라 결과 달라짐

**해결:**
```kotlin
@BeforeEach
fun setUp() {
    // 상태 초기화
    clearAllMocks()
    repository.deleteAll().block()
}

@AfterEach
fun tearDown() {
    // 정리
}
```

### 2. 트랜잭션 롤백 안 됨

**증상:**
- 테스트 데이터가 DB에 남아있음

**해결:**
```kotlin
@DataR2dbcTest
@Transactional  // R2DBC는 기본 롤백 안 됨
@Rollback  // 명시적 롤백
class RepositoryTest {

    // 또는 수동 정리
    @AfterEach
    fun cleanup() {
        repository.deleteAll().block()
    }
}
```

### 3. 포트 충돌

**증상:**
```
Port 8080 is already in use
```

**해결:**
```kotlin
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class IntegrationTest {
    @LocalServerPort
    private var port: Int = 0
}
```

## Mock 관련 문제

### 1. Final 클래스/메서드 Mock

**증상:**
```
MockK could not mock final class
```

**해결:**
```kotlin
// MockK는 기본적으로 final 지원하지만, 문제 시:
@MockK(relaxed = true)
lateinit var finalClass: FinalClass

// 또는 인터페이스 추출 후 Mock
```

### 2. Suspend 함수 Mock

**증상:**
```
coEvery not working properly
```

**해결:**
```kotlin
// coEvery 사용 (suspend 함수용)
coEvery { repository.findById(any()) } returns user

// coVerify로 검증
coVerify { repository.findById(1L) }
```

### 3. Reactive 스트림 Mock

**증상:**
```
every returns Mono but test expects...
```

**해결:**
```kotlin
// Mono 반환
every { service.findById(any()) } returns Mono.just(user)

// 빈 Mono
every { service.findById(999L) } returns Mono.empty()

// 에러 Mono
every { service.findById(-1L) } returns Mono.error(NotFoundException())

// Flux 반환
every { service.findAll() } returns Flux.fromIterable(users)
```

## 성능 문제

### 1. 느린 테스트 실행

**진단:**
```bash
./gradlew test --profile
# build/reports/profile/ 에서 시간 소요 분석
```

**해결:**
```kotlin
// 1. 병렬 실행
// build.gradle.kts
tasks.test {
    maxParallelForks = Runtime.getRuntime().availableProcessors()
}

// 2. 불필요한 Spring 컨텍스트 로딩 제거
@WebFluxTest  // @SpringBootTest 대신 슬라이스 테스트

// 3. 무거운 초기화 공유
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class SharedSetupTest {
    @BeforeAll
    fun heavySetup() { ... }
}
```

### 2. 메모리 부족

**증상:**
```
java.lang.OutOfMemoryError: Java heap space
```

**해결:**
```kotlin
// build.gradle.kts
tasks.test {
    jvmArgs = listOf("-Xmx2g", "-XX:+UseG1GC")
}
```

## 디버깅 팁

### 상세 로그 활성화

```bash
./gradlew test --info --stacktrace

# 또는 특정 테스트만
./gradlew test --tests "*UserServiceTest*" --debug
```

### Reactor 디버그 모드

```kotlin
// 테스트 설정에 추가
@BeforeAll
fun enableReactorDebug() {
    Hooks.onOperatorDebug()
}

// 또는 ReactorDebugAgent
ReactorDebugAgent.init()
```

### 실패 테스트만 재실행

```bash
./gradlew test --rerun-tasks --tests "*failing*"
```
