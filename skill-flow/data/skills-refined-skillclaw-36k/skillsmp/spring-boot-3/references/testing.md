# Spring Boot Testing Best Practices

This reference covers testing strategies for Spring Boot applications including unit tests, integration tests, and test slicing.

## Testing Dependencies

Spring Boot Starter Test includes most testing dependencies:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

This includes:
- JUnit 5 (JUnit Jupiter)
- Spring Boot Test
- Spring Test
- AssertJ
- Hamcrest
- Mockito
- JSONassert
- JsonPath

**Additional dependencies for specific testing:**

```xml
<!-- For REST API testing -->
<dependency>
    <groupId>io.rest-assured</groupId>
    <artifactId>rest-assured</artifactId>
    <scope>test</scope>
</dependency>

<!-- For security testing -->
<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-test</artifactId>
    <scope>test</scope>
</dependency>
```

## Unit Testing

### Testing Service Layer with Mockito

```java
@ExtendWith(MockitoExtension.class)  // JUnit 5
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private UserService userService;

    @Test
    void findById_ShouldReturnUser_WhenUserExists() {
        // Given
        Long userId = 1L;
        User user = new User();
        user.setId(userId);
        user.setEmail("test@example.com");

        when(userRepository.findById(userId)).thenReturn(Optional.of(user));

        // When
        UserDTO result = userService.findById(userId);

        // Then
        assertNotNull(result);
        assertEquals(userId, result.getId());
        assertEquals("test@example.com", result.getEmail());

        verify(userRepository).findById(userId);
        verifyNoMoreInteractions(userRepository);
    }

    @Test
    void findById_ShouldThrowException_WhenUserNotFound() {
        // Given
        Long userId = 1L;
        when(userRepository.findById(userId)).thenReturn(Optional.empty());

        // When/Then
        assertThrows(ResourceNotFoundException.class, () -> userService.findById(userId));

        verify(userRepository).findById(userId);
    }

    @Test
    void create_ShouldEncodePassword_WhenCreatingUser() {
        // Given
        CreateUserRequest request = new CreateUserRequest();
        request.setEmail("test@example.com");
        request.setPassword("plainPassword");

        User savedUser = new User();
        savedUser.setId(1L);

        when(passwordEncoder.encode("plainPassword")).thenReturn("encodedPassword");
        when(userRepository.existsByEmail("test@example.com")).thenReturn(false);
        when(userRepository.save(any(User.class))).thenReturn(savedUser);

        // When
        UserDTO result = userService.create(request);

        // Then
        assertNotNull(result);
        assertEquals(1L, result.getId());

        verify(passwordEncoder).encode("plainPassword");
        verify(userRepository).existsByEmail("test@example.com");
        verify(userRepository).save(argThat(user ->
            "encodedPassword".equals(user.getPassword())
        ));
    }

    @Test
    void create_ShouldThrowException_WhenEmailExists() {
        // Given
        CreateUserRequest request = new CreateUserRequest();
        request.setEmail("existing@example.com");

        when(userRepository.existsByEmail("existing@example.com")).thenReturn(true);

        // When/Then
        assertThrows(DuplicateResourceException.class, () -> userService.create(request));

        verify(userRepository).existsByEmail("existing@example.com");
        verify(userRepository, never()).save(any());
    }
}
```

### Custom Assertions with AssertJ

```java
@Test
void findById_ShouldReturnUser_WhenUserExists() {
    // Given
    User user = new User();
    user.setId(1L);
    user.setEmail("test@example.com");
    user.setName("John Doe");

    when(userRepository.findById(1L)).thenReturn(Optional.of(user));

    // When
    UserDTO result = userService.findById(1L);

    // Then - AssertJ provides fluent assertions
    assertThat(result)
        .isNotNull()
        .satisfies(userDTO -> {
            assertThat(userDTO.getId()).isEqualTo(1L);
            assertThat(userDTO.getEmail()).isEqualTo("test@example.com");
            assertThat(userDTO.getName()).isEqualTo("John Doe");
        });
}
```

### Testing Exception Messages

```java
@Test
void findById_ShouldThrowException_WithCorrectMessage() {
    // Given
    Long userId = 999L;
    when(userRepository.findById(userId)).thenReturn(Optional.empty());

    // When/Then
    ResourceNotFoundException exception = assertThrows(
        ResourceNotFoundException.class,
        () -> userService.findById(userId)
    );

    assertThat(exception.getMessage())
        .isEqualTo("User not found with id: 999");
}
```

## Integration Testing

### @SpringBootTest for Full Application Context

```java
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class UserControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Test
    @WithMockUser(username = "admin", roles = "ADMIN")
    void getAllUsers_ShouldReturnUsers_WhenUsersExist() throws Exception {
        // Given
        User user = new User();
        user.setEmail("test@example.com");
        user.setPassword(passwordEncoder.encode("password"));
        userRepository.save(user);

        // When/Then
        mockMvc.perform(get("/api/users"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$").isArray())
            .andExpect(jsonPath("$[0].email").value("test@example.com"));
    }

    @Test
    void createUser_ShouldReturn201_WhenValidRequest() throws Exception {
        // Given
        CreateUserRequest request = new CreateUserRequest();
        request.setEmail("new@example.com");
        request.setPassword("Password123");
        request.setName("John Doe");

        // When/Then
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").exists())
            .andExpect(jsonPath("$.email").value("new@example.com"))
            .andExpect(jsonPath("$.password").doesNotExist());  // Password not exposed
    }

    @Test
    void createUser_ShouldReturn400_WhenInvalidEmail() throws Exception {
        // Given
        CreateUserRequest request = new CreateUserRequest();
        request.setEmail("invalid-email");

        // When/Then
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.message").value("Validation failed"))
            .andExpect(jsonPath("$.validationErrors.email").exists());
    }
}
```

### @TestConfiguration for Test-Specific Beans

```java
@TestConfiguration
public class TestConfig {

    @Bean
    @Primary
    public EmailService emailService() {
        return new EmailService() {
            @Override
            public void sendEmail(String to, String subject, String body) {
                // Do nothing in tests
            }
        };
    }
}
```

**Use test configuration:**

```java
@SpringBootTest
@Import(TestConfig.class)
class UserServiceIntegrationTest {
    // Uses test EmailService
}
```

## Test Slicing

### @WebMvcTest - Web Layer Only

Test only the web layer, without loading full application context:

```java
@WebMvcTest(UserController.class)
class UserControllerWebTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;  // Mock dependencies

    @Test
    void getUser_ShouldReturn200_WhenUserExists() throws Exception {
        // Given
        UserDTO user = new UserDTO(1L, "test@example.com");
        when(userService.findById(1L)).thenReturn(user);

        // When/Then
        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.email").value("test@example.com"));
    }

    @Test
    void getUser_ShouldReturn404_WhenUserNotFound() throws Exception {
        // Given
        when(userService.findById(1L))
            .throw(new ResourceNotFoundException("User not found"));

        // When/Then
        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isNotFound());
    }
}
```

### @DataJpaTest - Data Layer Only

Test JPA repositories:

```java
@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;  // For setting up test data

    @Autowired
    private UserRepository userRepository;

    @Test
    void findByEmail_ShouldReturnUser_WhenEmailExists() {
        // Given
        User user = new User();
        user.setEmail("test@example.com");
        user.setName("Test User");
        entityManager.persist(user);
        entityManager.flush();

        // When
        Optional<User> found = userRepository.findByEmail("test@example.com");

        // Then
        assertThat(found).isPresent();
        assertThat(found.get().getEmail()).isEqualTo("test@example.com");
    }

    @Test
    void existsByEmail_ShouldReturnTrue_WhenEmailExists() {
        // Given
        User user = new User();
        user.setEmail("test@example.com");
        entityManager.persist(user);

        // When
        boolean exists = userRepository.existsByEmail("test@example.com");

        // Then
        assertThat(exists).isTrue();
    }
}
```

### @JsonTest - JSON Serialization

Test JSON serialization/deserialization:

```java
@JsonTest
class UserJsonTest {

    @Autowired
    private JacksonTester<UserDTO> json;

    @Test
    void serialize_ShouldIncludeAllFields() throws Exception {
        // Given
        UserDTO user = new UserDTO(1L, "test@example.com");

        // When
        JsonContent<UserDTO> jsonContent = json.write(user);

        // Then
        assertThat(jsonContent)
            .extractingJsonPathNumberValue("$.id")
            .isEqualTo(1);
        assertThat(jsonContent)
            .extractingJsonPathStringValue("$.email")
            .isEqualTo("test@example.com");
    }

    @Test
    void deserialize_ShouldCreateUser() throws Exception {
        // Given
        String jsonString = "{\"id\":1,\"email\":\"test@example.com\"}";

        // When
        UserDTO user = json.parseObject(jsonString);

        // Then
        assertThat(user.getId()).isEqualTo(1);
        assertThat(user.getEmail()).isEqualTo("test@example.com");
    }
}
```

## Security Testing

### Test Authentication

```java
@SpringBootTest
@AutoConfigureMockMvc
class SecurityConfigTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void accessPublicEndpoint_ShouldSucceed_WithoutAuthentication() throws Exception {
        mockMvc.perform(get("/api/public/health"))
            .andExpect(status().isOk());
    }

    @Test
    void accessProtectedEndpoint_ShouldFail_WithoutAuthentication() throws Exception {
        mockMvc.perform(get("/api/users"))
            .andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(username = "user", roles = "USER")
    void accessProtectedEndpoint_ShouldSucceed_WithUserRole() throws Exception {
        mockMvc.perform(get("/api/users"))
            .andExpect(status().isOk());
    }

    @Test
    @WithMockUser(username = "admin", roles = "ADMIN")
    void accessAdminEndpoint_ShouldSucceed_WithAdminRole() throws Exception {
        mockMvc.perform(delete("/api/users/1"))
            .andExpect(status().isNoContent());
    }

    @Test
    @WithMockUser(username = "user", roles = "USER")
    void accessAdminEndpoint_ShouldFail_WithUserRole() throws Exception {
        mockMvc.perform(delete("/api/users/1"))
            .andExpect(status().isForbidden());
    }
}
```

### Test with JWT

```java
@SpringBootTest
@AutoConfigureMockMvc
class JwtAuthenticationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private JwtTokenProvider tokenProvider;

    @Test
    void accessEndpoint_WithValidJwt_ShouldSucceed() throws Exception {
        // Given
        String token = generateTestToken();

        // When/Then
        mockMvc.perform(get("/api/users")
                .header("Authorization", "Bearer " + token))
            .andExpect(status().isOk());
    }

    private String generateTestToken() {
        // Generate test JWT token
        UserDetails userDetails = User.withUsername("test@example.com")
            .password("password")
            .roles("USER")
            .build();

        UsernamePasswordAuthenticationToken authentication =
            new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());

        return tokenProvider.generateToken(authentication);
    }
}
```

## Test Data Management

### @Sql for Database Setup

```java
@SpringBootTest
class UserServiceIntegrationTest {

    @Sql(scripts = "/sql/test-data.sql")
    @Test
    void testWithTestData() {
        // Test with data loaded from SQL file
    }

    @Sql(scripts = {
        "/sql/cleanup.sql",
        "/sql/test-data.sql"
    })
    @Test
    void testWithCleanData() {
        // Clean and load fresh data
    }
}
```

### TestContainers for Real Database

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>postgresql</artifactId>
    <scope>test</scope>
</dependency>
```

```java
@SpringBootTest
@Testcontainers
class PostgresIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @DynamicPropertySource
    static void postgresProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Test
    void testWithRealPostgres() {
        // Tests run against real PostgreSQL container
    }
}
```

## Testing Best Practices

### 1. Arrange-Act-Assert (AAA) Pattern

```java
@Test
void testSomething() {
    // Arrange - Set up test data
    Long userId = 1L;
    User user = new User();
    user.setId(userId);

    // Act - Execute the method under test
    UserDTO result = userService.findById(userId);

    // Assert - Verify the result
    assertThat(result.getId()).isEqualTo(userId);
}
```

### 2. Descriptive Test Names

```java
// ✅ GOOD - Descriptive
@Test
void findById_ShouldReturnUser_WhenUserExists() { }

@Test
void create_ShouldThrowException_WhenEmailAlreadyExists() { }

// ❌ BAD - Vague
@Test
void testFindById() { }

@Test
void testCreate() { }
```

### 3. One Assertion Per Test

```java
// ✅ GOOD - Focused tests
@Test
void findById_ShouldReturnCorrectId() {
    UserDTO result = userService.findById(1L);
    assertThat(result.getId()).isEqualTo(1L);
}

@Test
void findById_ShouldReturnCorrectEmail() {
    UserDTO result = userService.findById(1L);
    assertThat(result.getEmail()).isEqualTo("test@example.com");
}

// Acceptable - Related assertions
@Test
void findById_ShouldReturnUserWithCorrectFields() {
    UserDTO result = userService.findById(1L);
    assertThat(result)
        .satisfies(user -> {
            assertThat(user.getId()).isEqualTo(1L);
            assertThat(user.getEmail()).isEqualTo("test@example.com");
        });
}
```

### 4. Use @Nested for Related Tests

```java
@DisplayName("UserService")
class UserServiceTest {

    @Nested
    @DisplayName("findById method")
    class FindByIdTests {

        @Test
        @DisplayName("should return user when user exists")
        void shouldReturnUserWhenExists() { }

        @Test
        @DisplayName("should throw exception when user not found")
        void shouldThrowWhenNotFound() { }
    }

    @Nested
    @DisplayName("create method")
    class CreateTests {

        @Test
        @DisplayName("should create user with valid data")
        void shouldCreateWithValidData() { }

        @Test
        @DisplayName("should throw exception when email exists")
        void shouldThrowWhenEmailExists() { }
    }
}
```

### 5. Avoid Code Duplication in Tests

```java
@SpringBootTest
abstract class BaseControllerTest {

    @Autowired
    protected MockMvc mockMvc;

    @Autowired
    protected ObjectMapper objectMapper;

    protected String toJson(Object object) throws Exception {
        return objectMapper.writeValueAsString(object);
    }
}

@RestControllerTest
class UserControllerTest extends BaseControllerTest {

    @Test
    void createUser_ShouldReturn201() throws Exception {
        CreateUserRequest request = new CreateUserRequest();
        // ...

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(toJson(request)))
            .andExpect(status().isCreated());
    }
}
```

## Summary Checklist

- [ ] Test service layer with mocks (@ExtendWith(MockitoExtension.class))
- [ ] Test controllers with @WebMvcTest
- [ ] Test repositories with @DataJpaTest
- [ ] Use @SpringBootTest for integration tests
- [ ] Use @TestConfiguration for test-specific beans
- [ ] Test security with @WithMockUser
- [ ] Follow AAA pattern (Arrange-Act-Assert)
- [ ] Use descriptive test names
- [ ] Keep tests focused and independent
- [ ] Mock external dependencies
- [ ] Use TestContainers for real database testing
- [ ] Test exception scenarios
- [ ] Verify mock interactions

## Resources

- [Spring Boot Testing: A Comprehensive Best Practices Guide](https://dev.to/ankitdevcode/spring-boot-testing-a-comprehensive-best-practices-guide-1do6)
- [Spring Boot Testing: From Unit to End-to-End Testing](https://rieckpil.de/spring-boot-testing-from-unit-to-end-to-end-testing/)
- [Spring Boot Test Documentation](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing)
