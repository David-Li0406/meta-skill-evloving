# Spring Boot Best Practices

## Dependency Injection

### Constructor Injection (Preferred)

```java
@Service
public class UserService {

    private final UserRepository userRepository;
    private final EventPublisher eventPublisher;
    private final UserMapper userMapper;

    // Constructor injection - immutable, testable
    public UserService(
            UserRepository userRepository,
            EventPublisher eventPublisher,
            UserMapper userMapper) {
        this.userRepository = userRepository;
        this.eventPublisher = eventPublisher;
        this.userMapper = userMapper;
    }
}

// Or with Lombok
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;
    private final EventPublisher eventPublisher;
    private final UserMapper userMapper;
}
```

### Avoid Field Injection

```java
// ❌ Field injection - hard to test, hides dependencies
@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;
}

// ❌ Setter injection - allows partial initialization
@Service
public class UserService {
    private UserRepository userRepository;

    @Autowired
    public void setUserRepository(UserRepository repo) {
        this.userRepository = repo;
    }
}
```

## Service Layer Patterns

### Transactional Boundaries

```java
@Service
@Transactional
public class OrderService {

    // Read-only transactions for queries
    @Transactional(readOnly = true)
    public Optional<Order> findById(Long id) {
        return orderRepository.findById(id);
    }

    // Write transaction (default)
    public Order createOrder(CreateOrderRequest request) {
        Order order = orderMapper.toEntity(request);
        Order saved = orderRepository.save(order);
        eventPublisher.publish(new OrderCreatedEvent(saved));
        return saved;
    }

    // Explicit rollback rules
    @Transactional(rollbackFor = {BusinessException.class})
    public void processOrder(Long orderId) {
        // Rolls back on BusinessException
    }
}
```

### Service Method Patterns

```java
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    // Return Optional for single entity lookups
    @Transactional(readOnly = true)
    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }

    // Return collection directly (empty list is valid)
    @Transactional(readOnly = true)
    public List<User> findByRole(Role role) {
        return userRepository.findByRole(role);
    }

    // Return created entity
    @Transactional
    public User create(CreateUserRequest request) {
        validateRequest(request);
        User user = userMapper.toEntity(request);
        return userRepository.save(user);
    }

    // Void for updates with side effects
    @Transactional
    public void updateEmail(Long userId, String newEmail) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new UserNotFoundException(userId));
        user.setEmail(newEmail);
        // No explicit save - JPA dirty checking
    }
}
```

## Controller Patterns

### REST Controller Structure

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Validated
public class UserController {

    private final UserService userService;

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(UserResponse::from)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping
    public List<UserResponse> listUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return userService.findAll(PageRequest.of(page, size))
            .map(UserResponse::from)
            .getContent();
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserResponse createUser(@Valid @RequestBody CreateUserRequest request) {
        User created = userService.create(request);
        return UserResponse.from(created);
    }

    @PutMapping("/{id}")
    public UserResponse updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UpdateUserRequest request) {
        User updated = userService.update(id, request);
        return UserResponse.from(updated);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteUser(@PathVariable Long id) {
        userService.delete(id);
    }
}
```

### Validation

```java
// Request validation with Bean Validation
public record CreateUserRequest(
    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100)
    String name,

    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    String email,

    @NotNull
    @Min(0)
    @Max(150)
    Integer age
) {}

// Custom validator
@Documented
@Constraint(validatedBy = UniqueEmailValidator.class)
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface UniqueEmail {
    String message() default "Email already exists";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
```

## Exception Handling

### Global Exception Handler

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(ResourceNotFoundException ex) {
        log.debug("Resource not found: {}", ex.getMessage());
        return new ErrorResponse(
            HttpStatus.NOT_FOUND.value(),
            ex.getMessage(),
            Instant.now()
        );
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleValidation(MethodArgumentNotValidException ex) {
        List<FieldError> errors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .map(e -> new FieldError(e.getField(), e.getDefaultMessage()))
            .toList();

        return new ErrorResponse(
            HttpStatus.BAD_REQUEST.value(),
            "Validation failed",
            errors,
            Instant.now()
        );
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorResponse handleGeneric(Exception ex) {
        log.error("Unexpected error", ex);
        return new ErrorResponse(
            HttpStatus.INTERNAL_SERVER_ERROR.value(),
            "An unexpected error occurred",
            Instant.now()
        );
    }
}
```

## Configuration Patterns

### Type-Safe Configuration

```java
@ConfigurationProperties(prefix = "app.mail")
@Validated
public record MailProperties(
    @NotBlank String host,
    @Min(1) @Max(65535) int port,
    @NotBlank String username,
    String password,
    @NotNull Duration timeout
) {}

// Enable in application
@SpringBootApplication
@ConfigurationPropertiesScan
public class Application {}

// application.yml
// app:
//   mail:
//     host: smtp.example.com
//     port: 587
//     username: user
//     timeout: 30s
```

### Profile-Specific Configuration

```java
@Configuration
public class DataSourceConfig {

    @Bean
    @Profile("dev")
    public DataSource devDataSource() {
        return DataSourceBuilder.create()
            .url("jdbc:h2:mem:devdb")
            .build();
    }

    @Bean
    @Profile("prod")
    public DataSource prodDataSource(DatabaseProperties props) {
        return DataSourceBuilder.create()
            .url(props.url())
            .username(props.username())
            .password(props.password())
            .build();
    }
}
```

## Testing Patterns

### Service Layer Tests

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    void findById_existingUser_returnsUser() {
        // Given
        User user = new User(1L, "John", "john@example.com");
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));

        // When
        Optional<User> result = userService.findById(1L);

        // Then
        assertThat(result).isPresent();
        assertThat(result.get().getName()).isEqualTo("John");
        verify(userRepository).findById(1L);
    }

    @Test
    void findById_nonExistingUser_returnsEmpty() {
        when(userRepository.findById(99L)).thenReturn(Optional.empty());

        Optional<User> result = userService.findById(99L);

        assertThat(result).isEmpty();
    }
}
```

### Integration Tests

```java
@SpringBootTest
@AutoConfigureMockMvc
@Testcontainers
class UserControllerIT {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15");

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Test
    void createUser_validRequest_returnsCreated() throws Exception {
        var request = new CreateUserRequest("John", "john@example.com", 25);

        mockMvc.perform(post("/api/v1/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.name").value("John"))
            .andExpect(jsonPath("$.email").value("john@example.com"));
    }
}
```

## Security Patterns

### Method Security

```java
@Service
@RequiredArgsConstructor
public class OrderService {

    @PreAuthorize("hasRole('ADMIN') or #userId == authentication.principal.id")
    public List<Order> findByUserId(Long userId) {
        return orderRepository.findByUserId(userId);
    }

    @PreAuthorize("hasRole('ADMIN')")
    public void deleteOrder(Long orderId) {
        orderRepository.deleteById(orderId);
    }

    @PostAuthorize("returnObject.userId == authentication.principal.id")
    public Order findById(Long id) {
        return orderRepository.findById(id)
            .orElseThrow(() -> new OrderNotFoundException(id));
    }
}
```
