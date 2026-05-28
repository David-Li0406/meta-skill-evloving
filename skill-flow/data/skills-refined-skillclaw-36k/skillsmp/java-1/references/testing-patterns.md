# Java Testing Patterns

## JUnit 5 Fundamentals

### Test Lifecycle

```java
@TestInstance(Lifecycle.PER_CLASS)
class UserServiceTest {

    @BeforeAll
    void setupAll() {
        // Run once before all tests
    }

    @BeforeEach
    void setup() {
        // Run before each test
    }

    @Test
    @DisplayName("should create user with valid input")
    void createUser_ValidInput_ReturnsUser() {
        // Given
        var input = new CreateUserRequest("john@example.com");

        // When
        var result = userService.create(input);

        // Then
        assertThat(result.email()).isEqualTo("john@example.com");
    }

    @AfterEach
    void teardown() {
        // Run after each test
    }
}
```

### Parameterized Tests

```java
@ParameterizedTest
@CsvSource({
    "john@example.com, true",
    "invalid-email, false",
    "'', false",
    ", false"
})
void validateEmail_ReturnsExpected(String email, boolean expected) {
    assertThat(validator.isValid(email)).isEqualTo(expected);
}

@ParameterizedTest
@MethodSource("userProvider")
void processUser_WithVariousInputs(User user, String expected) {
    assertThat(processor.process(user)).isEqualTo(expected);
}

static Stream<Arguments> userProvider() {
    return Stream.of(
        Arguments.of(new User("active", true), "processed"),
        Arguments.of(new User("inactive", false), "skipped")
    );
}

@ParameterizedTest
@EnumSource(value = Status.class, names = {"ACTIVE", "PENDING"})
void handleStatus_ActiveAndPending(Status status) {
    assertDoesNotThrow(() -> handler.handle(status));
}
```

### Nested Tests

```java
@DisplayName("UserService")
class UserServiceTest {

    @Nested
    @DisplayName("when creating users")
    class WhenCreating {

        @Test
        void shouldCreateWithValidInput() { }

        @Test
        void shouldRejectInvalidEmail() { }

        @Nested
        @DisplayName("with admin privileges")
        class WithAdminPrivileges {

            @Test
            void shouldAllowBulkCreate() { }
        }
    }

    @Nested
    @DisplayName("when deleting users")
    class WhenDeleting {

        @Test
        void shouldSoftDelete() { }
    }
}
```

## Mockito Patterns

### Basic Mocking

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PaymentService paymentService;

    @InjectMocks
    private OrderService orderService;

    @Test
    void processOrder_ValidOrder_Succeeds() {
        // Given
        when(userRepository.findById(1L)).thenReturn(Optional.of(testUser));
        when(paymentService.charge(any())).thenReturn(PaymentResult.success());

        // When
        var result = orderService.process(new Order(1L, 100.0));

        // Then
        assertThat(result.isSuccess()).isTrue();
        verify(paymentService).charge(argThat(p -> p.amount() == 100.0));
    }
}
```

### Argument Captors

```java
@Captor
private ArgumentCaptor<AuditEvent> eventCaptor;

@Test
void createUser_LogsAuditEvent() {
    userService.create(new User("john"));

    verify(auditService).log(eventCaptor.capture());

    var event = eventCaptor.getValue();
    assertThat(event.type()).isEqualTo("USER_CREATED");
    assertThat(event.data()).containsKey("username");
}
```

### Stubbing Chains

```java
// Builder pattern mocking
when(builder.withName(any())).thenReturn(builder);
when(builder.withEmail(any())).thenReturn(builder);
when(builder.build()).thenReturn(expectedResult);

// Consecutive returns
when(service.getNext())
    .thenReturn("first")
    .thenReturn("second")
    .thenThrow(new NoMoreException());

// Answer for dynamic responses
when(repository.save(any())).thenAnswer(invocation -> {
    User user = invocation.getArgument(0);
    return user.withId(UUID.randomUUID());
});
```

## AssertJ Patterns

```java
// Collection assertions
assertThat(users)
    .hasSize(3)
    .extracting(User::name)
    .containsExactly("Alice", "Bob", "Charlie");

// Exception assertions
assertThatThrownBy(() -> service.process(null))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessageContaining("cannot be null");

// Soft assertions (collect all failures)
SoftAssertions.assertSoftly(softly -> {
    softly.assertThat(user.name()).isEqualTo("John");
    softly.assertThat(user.email()).contains("@");
    softly.assertThat(user.age()).isGreaterThan(0);
});

// Custom condition
Condition<User> active = new Condition<>(
    u -> u.status() == Status.ACTIVE, "active user"
);
assertThat(users).areAtLeast(2, active);
```

## Integration Testing

### Spring Boot Test Slices

```java
// Controller tests only
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void getUser_ReturnsUser() throws Exception {
        when(userService.findById(1L)).thenReturn(testUser);

        mockMvc.perform(get("/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("John"));
    }
}

// Repository tests only
@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private UserRepository repository;

    @Test
    void findByEmail_ReturnsUser() {
        entityManager.persist(new User("john@example.com"));

        var found = repository.findByEmail("john@example.com");

        assertThat(found).isPresent();
    }
}
```

### Testcontainers

```java
@SpringBootTest
@Testcontainers
class IntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
        .withDatabaseName("testdb");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Test
    void integrationTest() {
        // Test with real PostgreSQL
    }
}
```

## Test Data Builders

```java
public class UserTestBuilder {
    private String name = "John Doe";
    private String email = "john@example.com";
    private Status status = Status.ACTIVE;

    public static UserTestBuilder aUser() {
        return new UserTestBuilder();
    }

    public UserTestBuilder withName(String name) {
        this.name = name;
        return this;
    }

    public UserTestBuilder inactive() {
        this.status = Status.INACTIVE;
        return this;
    }

    public User build() {
        return new User(name, email, status);
    }
}

// Usage
var user = aUser().withName("Jane").inactive().build();
```

## Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Test name `test1` | Unclear intent | Use descriptive names |
| Single assertion per test (extreme) | Verbose, slow | Group related assertions |
| Mocking everything | Brittle tests | Mock boundaries only |
| Sleeping in tests | Slow, flaky | Use awaitility or mocks |
| Testing private methods | Breaks encapsulation | Test through public API |
| No test data cleanup | Test pollution | Use @DirtiesContext or cleanup |
