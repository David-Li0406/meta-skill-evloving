# Validation and Error Handling Best Practices

This reference covers input validation, error handling, and creating robust error responses in Spring Boot applications.

## Bean Validation

### Dependency

Spring Boot Starter Validation includes Hibernate Validator:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

### Common Validation Annotations

```java
public class CreateUserRequest {

    @NotNull(message = "Name is required")
    @Size(min = 2, max = 50, message = "Name must be between 2 and 50 characters")
    private String name;

    @NotBlank(message = "Email cannot be blank")
    @Email(message = "Email must be valid")
    private String email;

    @NotNull(message = "Age is required")
    @Min(value = 18, message = "Age must be at least 18")
    @Max(value = 120, message = "Age must be less than 120")
    private Integer age;

    @Pattern(regexp = "^\\+?[0-9]{10,15}$", message = "Phone number must be valid")
    private String phone;

    @Past(message = "Birth date must be in the past")
    private LocalDate birthDate;

    @NotEmpty(message = "Skills cannot be empty")
    private List<@NotBlank(message = "Skill cannot be blank") String> skills;

    @AssertTrue(message = "Terms must be accepted")
    private boolean termsAccepted;
}
```

**Annotation reference:**
- `@NotNull` - Cannot be null
- `@NotBlank` - String cannot be null or empty (trimmed length > 0)
- `@NotEmpty` - Collection/array/map cannot be null or empty
- `@Size(min, max)` - Size constraint for strings, collections, arrays
- `@Min`, `@Max` - Numeric value constraint
- `@DecimalMin`, `@DecimalMax` - For BigDecimal/BigInteger
- `@Negative`, `@Positive` - Negative/positive numbers
- `@Email` - Email format
- `@Pattern` - Regex pattern
- `@Past`, `@Future` - Date validation
- `@PastOrPresent`, `@FutureOrPresent` - Date inclusive validation
- `@URL` - URL format
- `@Digits` - Numeric value within range
- `@AssertTrue`, `@AssertFalse` - Boolean validation

### Enabling Validation

**In controllers:**

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @PostMapping
    public ResponseEntity<UserDTO> create(
        @Valid @RequestBody CreateUserRequest request  // @Valid triggers validation
    ) {
        UserDTO created = userService.create(request);
        return ResponseEntity.ok(created);
    }

    @PostMapping("/batch")
    public ResponseEntity<List<UserDTO>> createBatch(
        @Valid @RequestBody List<@Valid CreateUserRequest> requests  // Validate each item
    ) {
        List<UserDTO> created = userService.createBatch(requests);
        return ResponseEntity.ok(created);
    }
}
```

**In services:**

```java
@Service
public class UserService {

    public void createUser(@Valid CreateUserRequest request) {
        // @Valid works in services too
    }
}
```

**For path variables and query parameters:**

```java
@GetMapping("/users/{id}")
public ResponseEntity<UserDTO> getUser(
    @PathVariable @Min(1) Long id,  // Validate path variable
    @RequestParam(required = false)
    @Size(min = 2, max = 50)
    String name  // Validate query parameter
) {
    // ...
}
```

### Custom Validators

**Create custom annotation:**

```java
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = PasswordValidator.class)
public @interface ValidPassword {

    String message() default "Password must contain uppercase, lowercase, digit, and special character";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
```

**Implement validator:**

```java
public class PasswordValidator implements ConstraintValidator<ValidPassword, String> {

    @Override
    public boolean isValid(String password, ConstraintValidatorContext context) {
        if (password == null) {
            return false;
        }

        boolean hasUppercase = !password.equals(password.toLowerCase());
        boolean hasLowercase = !password.equals(password.toUpperCase());
        boolean hasDigit = password.matches(".*\\d.*");
        boolean hasSpecial = !password.matches("[A-Za-z0-9]*");

        return hasUppercase && hasLowercase && hasDigit && hasSpecial;
    }
}
```

**Use custom validator:**

```java
public class CreateUserRequest {
    @ValidPassword
    private String password;
}
```

## Global Exception Handling

### @ControllerAdvice

Handle exceptions globally:

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFound(
        ResourceNotFoundException ex
    ) {
        logger.error("Resource not found: {}", ex.getMessage());

        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.NOT_FOUND.value())
            .message(ex.getMessage())
            .timestamp(LocalDateTime.now())
            .build();

        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    @ExceptionHandler(DuplicateResourceException.class)
    public ResponseEntity<ErrorResponse> handleDuplicateResource(
        DuplicateResourceException ex
    ) {
        logger.error("Duplicate resource: {}", ex.getMessage());

        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.CONFLICT.value())
            .message(ex.getMessage())
            .timestamp(LocalDateTime.now())
            .build();

        return ResponseEntity.status(HttpStatus.CONFLICT).body(error);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationExceptions(
        MethodArgumentNotValidException ex
    ) {
        Map<String, String> errors = new HashMap<>();

        ex.getBindingResult().getFieldErrors().forEach(error -> {
            String fieldName = error.getField();
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
        });

        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.BAD_REQUEST.value())
            .message("Validation failed")
            .timestamp(LocalDateTime.now())
            .validationErrors(errors)
            .build();

        return ResponseEntity.badRequest().body(error);
    }

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> handleHttpMessageNotReadable(
        HttpMessageNotReadableException ex
    ) {
        String errorMessage = "Malformed JSON request";

        if (ex.getCause() instanceof JsonMappingException) {
            errorMessage = "Invalid request format";
        }

        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.BAD_REQUEST.value())
            .message(errorMessage)
            .timestamp(LocalDateTime.now())
            .build();

        return ResponseEntity.badRequest().body(error);
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGlobalException(
        Exception ex
    ) {
        logger.error("Unexpected error occurred", ex);

        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
            .message("An unexpected error occurred")
            .timestamp(LocalDateTime.now())
            .build();

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

### Custom Exceptions

**Base exception class:**

```java
public abstract class BaseException extends RuntimeException {
    public BaseException(String message) {
        super(message);
    }

    public BaseException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

**Specific exceptions:**

```java
public class ResourceNotFoundException extends BaseException {
    public ResourceNotFoundException(String resource, Long id) {
        super(String.format("%s not found with id: %s", resource, id));
    }

    public ResourceNotFoundException(String message) {
        super(message);
    }
}

public class DuplicateResourceException extends BaseException {
    public DuplicateResourceException(String resource, String field, String value) {
        super(String.format("%s already exists with %s: %s", resource, field, value));
    }
}

public class BusinessException extends BaseException {
    public BusinessException(String message) {
        super(message);
    }

    public BusinessException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

**Use custom exceptions:**

```java
@Service
public class UserService {

    public UserDTO findById(Long id) {
        return userRepository.findById(id)
            .map(UserMapper::toDTO)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
    }

    public UserDTO create(CreateUserRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new DuplicateResourceException("User", "email", request.getEmail());
        }

        // ... create user
    }
}
```

### Error Response DTO

**Standardized error response:**

```java
@Getter
@Builder
@Setter
public class ErrorResponse {
    private int status;
    private String message;
    private LocalDateTime timestamp;
    private Map<String, String> validationErrors;
    private String path;  // Request path
}
```

**Include request path:**

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(
        Exception ex,
        HttpServletRequest request
    ) {
        ErrorResponse error = ErrorResponse.builder()
            .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
            .message("An unexpected error occurred")
            .timestamp(LocalDateTime.now())
            .path(request.getRequestURI())
            .build();

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

## Exception Handling in Controllers

### @ExceptionHandler for Controller-Specific Errors

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        ErrorResponse error = new ErrorResponse(
            HttpStatus.NOT_FOUND.value(),
            ex.getMessage(),
            LocalDateTime.now()
        );
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserDTO> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }
}
```

### @ResponseStatus

Simple exception handling:

```java
@ResponseStatus(HttpStatus.NOT_FOUND)
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) {
        super(message);
    }
}

@ResponseStatus(HttpStatus.BAD_REQUEST)
public class InvalidUserInputException extends RuntimeException {
    public InvalidUserInputException(String message) {
        super(message);
    }
}
```

## ResponseStatusException

Quick exception handling without custom classes:

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping("/{id}")
    public ResponseEntity<UserDTO> getUser(@PathVariable Long id) {
        return userRepository.findById(id)
            .map(UserMapper::toDTO)
            .map(ResponseEntity::ok)
            .orElseThrow(() -> new ResponseStatusException(
                HttpStatus.NOT_FOUND,
                "User not found with id: " + id
            ));
    }

    @PostMapping
    public ResponseEntity<UserDTO> create(@Valid @RequestBody CreateUserRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new ResponseStatusException(
                HttpStatus.CONFLICT,
                "Email already exists: " + request.getEmail()
            );
        }

        UserDTO created = userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
```

## Validation Groups

Validate different fields in different scenarios:

```java
public class UserDTO {

    @NotNull(groups = OnCreate.class)
    @Null(groups = OnUpdate.class)
    private Long id;

    @NotNull(groups = {OnCreate.class, OnUpdate.class})
    private String name;

    public interface OnCreate {}
    public interface OnUpdate {}
}
```

**Use in controller:**

```java
@RestController
public class UserController {

    @PostMapping
    public ResponseEntity<UserDTO> create(
        @Validated(OnCreate.class) @RequestBody UserDTO user
    ) {
        // id must be null, name must be not null
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserDTO> update(
        @PathVariable Long id,
        @Validated(OnUpdate.class) @RequestBody UserDTO user
    ) {
        // id must be null, name must be not null
    }
}
```

## Manual Validation

Validate programmatically:

```java
@Service
public class UserService {

    @Autowired
    private Validator validator;

    public void validateUser(UserDTO user) {
        Set<ConstraintViolation<UserDTO>> violations = validator.validate(user);

        if (!violations.isEmpty()) {
            Map<String, String> errors = violations.stream()
                .collect(Collectors.toMap(
                    violation -> violation.getPropertyPath().toString(),
                    ConstraintViolation::getMessage
                ));

            throw new ValidationException("Validation failed", errors);
        }
    }
}
```

## Testing Exception Handling

**Test validation:**

```java
@SpringBootTest
@AutoConfigureMockMvc
class UserControllerValidationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void createUser_WithInvalidEmail_Returns400() throws Exception {
        CreateUserRequest request = new CreateUserRequest();
        request.setEmail("invalid-email");

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.message").value("Validation failed"))
            .andExpect(jsonPath("$.validationErrors.email").exists());
    }

    @Test
    void getUser_WithNonExistentId_Returns404() throws Exception {
        mockMvc.perform(get("/api/users/999"))
            .andExpect(status().isNotFound())
            .andExpect(jsonPath("$.message").value("User not found with id: 999"));
    }
}
```

## Best Practices

1. **Validate early** - Validate at controller entry point with `@Valid`
2. **Use specific exceptions** - Create exception classes for different error scenarios
3. **Consistent error format** - Use standardized ErrorResponse for all errors
4. **Log errors appropriately** - Log server errors, don't necessarily log client errors
5. **Never expose stack traces** - Don't include internal details in error responses
6. **Use appropriate HTTP status codes** - 400, 401, 403, 404, 409, 500
7. **Internationalize error messages** - Use MessageSource for i18n
8. **Document error responses** - Include in API documentation

## Summary Checklist

- [ ] Add validation dependency
- [ ] Use Bean Validation annotations on DTOs
- [ ] Enable validation with @Valid in controllers
- [ ] Create custom validators for complex rules
- [ ] Implement @ControllerAdvice for global exception handling
- [ ] Create custom exception classes
- [ ] Use standardized error response format
- [ ] Log errors appropriately
- [ ] Test exception handling
- [ ] Document error responses in API docs

## Resources

- [Best Practices for Exception Handling in Spring Boot](https://medium.com/@aishwaryakempu3/best-practices-for-exception-handling-in-spring-boot-1c5ee1357375)
- [Guide to Spring Boot Error Handling for REST APIs](https://www.toptal.com/developers/java/spring-boot-rest-api-error-handling)
- [Validation in Spring Boot](https://www.baeldung.com/spring-boot-bean-validation)
- [A Guide to Input Validation with Spring Boot](https://snyk.io/blog/guide-to-input-validation-with-spring-boot/)
- [Get Started with Custom Error Handling in Spring Boot](https://auth0.com/blog/get-started-with-custom-error-handling-in-spring-boot-java/)
