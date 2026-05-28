# Test Patterns

> Kotlin/Spring Boot/WebFlux 테스트 패턴 가이드

## 테스트 계층 구조

```text
테스트 피라미드
├─ E2E Tests (적음, 느림)
│   └─ 전체 시스템 통합
├─ Integration Tests (중간)
│   ├─ @DataR2dbcTest (Repository)
│   ├─ @WebFluxTest (Controller)
│   └─ @SpringBootTest (전체 컨텍스트)
└─ Unit Tests (많음, 빠름)
    └─ MockK + JUnit 5
```

## Unit Test Patterns

### 1. Service Layer Test

```kotlin
@ExtendWith(MockKExtension::class)
class UserServiceTest {

    @MockK
    private lateinit var userRepository: UserRepository

    @MockK
    private lateinit var eventPublisher: EventPublisher

    @InjectMockKs
    private lateinit var userService: UserService

    @BeforeEach
    fun setUp() {
        MockKAnnotations.init(this)
    }

    @Test
    fun `should create user and publish event`() {
        // Given
        val request = CreateUserRequest("test@example.com", "Test User")
        val savedUser = User(1L, "test@example.com", "Test User")

        every { userRepository.save(any()) } returns Mono.just(savedUser)
        every { eventPublisher.publish(any()) } returns Mono.empty()

        // When
        val result = userService.createUser(request)

        // Then
        StepVerifier.create(result)
            .expectNextMatches { it.email == "test@example.com" }
            .verifyComplete()

        verify { userRepository.save(any()) }
        verify { eventPublisher.publish(match { it is UserCreatedEvent }) }
    }

    @Test
    fun `should return empty when user not found`() {
        // Given
        every { userRepository.findById(any<Long>()) } returns Mono.empty()

        // When
        val result = userService.findById(999L)

        // Then
        StepVerifier.create(result)
            .verifyComplete()
    }
}
```

### 2. Reactive Stream Test with StepVerifier

```kotlin
@Test
fun `should emit items in order`() {
    val flux = userService.findAll()

    StepVerifier.create(flux)
        .expectNextCount(3)
        .verifyComplete()
}

@Test
fun `should handle error gracefully`() {
    every { userRepository.findById(any<Long>()) } returns
        Mono.error(DatabaseException("Connection failed"))

    val result = userService.findById(1L)

    StepVerifier.create(result)
        .expectError(ServiceException::class.java)
        .verify()
}

@Test
fun `should apply backpressure`() {
    val flux = userService.streamUsers()

    StepVerifier.create(flux, 2)  // Request only 2
        .expectNextCount(2)
        .thenCancel()
        .verify()
}
```

## Integration Test Patterns

### 1. Controller Test with WebTestClient

```kotlin
@WebFluxTest(UserController::class)
@Import(SecurityConfig::class)
class UserControllerTest {

    @Autowired
    private lateinit var webTestClient: WebTestClient

    @MockkBean
    private lateinit var userService: UserService

    @Test
    @WithMockUser(roles = ["USER"])
    fun `GET users should return paginated list`() {
        val users = listOf(
            User(1L, "user1@example.com"),
            User(2L, "user2@example.com")
        )
        every { userService.findAll(any()) } returns Flux.fromIterable(users)

        webTestClient.get()
            .uri("/api/users?page=0&size=10")
            .accept(MediaType.APPLICATION_JSON)
            .exchange()
            .expectStatus().isOk
            .expectHeader().contentType(MediaType.APPLICATION_JSON)
            .expectBodyList(UserResponse::class.java)
            .hasSize(2)
    }

    @Test
    fun `POST users without auth should return 401`() {
        webTestClient.post()
            .uri("/api/users")
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(CreateUserRequest("test@example.com"))
            .exchange()
            .expectStatus().isUnauthorized
    }

    @Test
    @WithMockUser(roles = ["ADMIN"])
    fun `DELETE user should return 204`() {
        every { userService.delete(1L) } returns Mono.empty()

        webTestClient.delete()
            .uri("/api/users/1")
            .exchange()
            .expectStatus().isNoContent
    }
}
```

### 2. Repository Test with @DataR2dbcTest

```kotlin
@DataR2dbcTest
@Import(R2dbcConfig::class)
@ActiveProfiles("test")
class UserRepositoryTest {

    @Autowired
    private lateinit var userRepository: UserRepository

    @Autowired
    private lateinit var databaseClient: DatabaseClient

    @BeforeEach
    fun setUp() {
        // 테스트 데이터 초기화
        databaseClient.sql("DELETE FROM users").then().block()
        databaseClient.sql("""
            INSERT INTO users (id, email, name, created_at)
            VALUES (1, 'test@example.com', 'Test User', NOW())
        """).then().block()
    }

    @Test
    fun `should find user by email`() {
        StepVerifier.create(userRepository.findByEmail("test@example.com"))
            .assertNext { user ->
                assertThat(user.email).isEqualTo("test@example.com")
                assertThat(user.name).isEqualTo("Test User")
            }
            .verifyComplete()
    }

    @Test
    fun `should save new user`() {
        val newUser = User(email = "new@example.com", name = "New User")

        StepVerifier.create(userRepository.save(newUser))
            .assertNext { saved ->
                assertThat(saved.id).isNotNull()
                assertThat(saved.email).isEqualTo("new@example.com")
            }
            .verifyComplete()
    }
}
```

### 3. Full Integration Test with @SpringBootTest

```kotlin
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
class UserIntegrationTest {

    @Autowired
    private lateinit var webTestClient: WebTestClient

    @Autowired
    private lateinit var userRepository: UserRepository

    @Test
    fun `full user lifecycle test`() {
        // Create
        val createResponse = webTestClient.post()
            .uri("/api/users")
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(CreateUserRequest("integration@test.com", "Test"))
            .exchange()
            .expectStatus().isCreated
            .expectBody(UserResponse::class.java)
            .returnResult()
            .responseBody!!

        val userId = createResponse.id

        // Read
        webTestClient.get()
            .uri("/api/users/$userId")
            .exchange()
            .expectStatus().isOk
            .expectBody()
            .jsonPath("$.email").isEqualTo("integration@test.com")

        // Update
        webTestClient.put()
            .uri("/api/users/$userId")
            .bodyValue(UpdateUserRequest("Updated Name"))
            .exchange()
            .expectStatus().isOk

        // Delete
        webTestClient.delete()
            .uri("/api/users/$userId")
            .exchange()
            .expectStatus().isNoContent

        // Verify deletion
        StepVerifier.create(userRepository.findById(userId))
            .verifyComplete()
    }
}
```

## Test Configuration

### application-test.yml

```yaml
spring:
  r2dbc:
    url: r2dbc:h2:mem:///testdb;DB_CLOSE_DELAY=-1
    username: sa
    password:

  flyway:
    enabled: false  # 테스트에서는 스키마 직접 생성

logging:
  level:
    org.springframework.r2dbc: DEBUG
    io.r2dbc.h2: DEBUG
```

### TestConfig.kt

```kotlin
@TestConfiguration
class TestConfig {

    @Bean
    fun testDatabaseClient(connectionFactory: ConnectionFactory): DatabaseClient {
        return DatabaseClient.create(connectionFactory)
    }

    @Bean
    fun schemaInitializer(databaseClient: DatabaseClient): ConnectionFactoryInitializer {
        val initializer = ConnectionFactoryInitializer()
        initializer.setConnectionFactory(connectionFactory)
        initializer.setDatabasePopulator(
            ResourceDatabasePopulator(ClassPathResource("schema.sql"))
        )
        return initializer
    }
}
```

## Common Assertions

### AssertJ + Reactor

```kotlin
// List assertions
assertThat(result).hasSize(3)
assertThat(result).extracting("email").contains("a@test.com", "b@test.com")

// Reactive assertions
StepVerifier.create(mono)
    .assertNext { assertThat(it.name).isEqualTo("Test") }
    .verifyComplete()

// Exception assertions
StepVerifier.create(mono)
    .expectErrorMatches { it is ValidationException && it.message == "Invalid" }
    .verify()
```

### JSON Path Assertions

```kotlin
webTestClient.get()
    .uri("/api/users")
    .exchange()
    .expectBody()
    .jsonPath("$.content").isArray
    .jsonPath("$.content.length()").isEqualTo(10)
    .jsonPath("$.content[0].email").exists()
    .jsonPath("$.totalElements").isNumber
```
