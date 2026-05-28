---
name: Spring Boot Web
description: REST controller patterns, request handling, validation, exception handling, and WebFlux.
metadata:
  labels: [java, spring-boot, web, rest, api]
  triggers:
    files: ['**/*Controller.java', '**/*RestController.java']
    keywords: [Controller, RestController, RequestMapping, GetMapping, PostMapping, PutMapping, DeleteMapping, ResponseBody, RequestBody, PathVariable, RequestParam]
---

# Spring Boot Web Standards

## REST Controller

```java
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping
    public List<UserResponse> findAll(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        return userService.findAll(PageRequest.of(page, size))
            .map(UserResponse::from)
            .getContent();
    }

    @GetMapping("/{id}")
    public UserResponse findById(@PathVariable Long id) {
        return userService.findById(id)
            .map(UserResponse::from)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserResponse create(@Valid @RequestBody CreateUserRequest request) {
        User user = userService.create(request);
        return UserResponse.from(user);
    }

    @PutMapping("/{id}")
    public UserResponse update(
            @PathVariable Long id,
            @Valid @RequestBody UpdateUserRequest request) {
        User user = userService.update(id, request);
        return UserResponse.from(user);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        userService.delete(id);
    }
}
```

## Request DTOs with Validation

```java
public record CreateUserRequest(
    @NotBlank @Size(min = 2, max = 100)
    String name,

    @NotBlank @Email
    String email,

    @NotBlank @Size(min = 8)
    @Pattern(regexp = "^(?=.*[A-Za-z])(?=.*\\d).*$",
             message = "must contain letters and numbers")
    String password
) {}

public record UpdateUserRequest(
    @Size(min = 2, max = 100)
    String name,

    @Email
    String email
) {}
```

## Response DTOs

```java
public record UserResponse(
    Long id,
    String name,
    String email,
    LocalDateTime createdAt
) {
    public static UserResponse from(User user) {
        return new UserResponse(
            user.getId(),
            user.getName(),
            user.getEmail(),
            user.getCreatedAt()
        );
    }
}

// Paginated response
public record PageResponse<T>(
    List<T> content,
    int page,
    int size,
    long totalElements,
    int totalPages,
    boolean last
) {
    public static <T> PageResponse<T> from(Page<T> page) {
        return new PageResponse<>(
            page.getContent(),
            page.getNumber(),
            page.getSize(),
            page.getTotalElements(),
            page.getTotalPages(),
            page.isLast()
        );
    }
}
```

## Exception Handling

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(ResourceNotFoundException ex) {
        return new ErrorResponse("NOT_FOUND", ex.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleValidation(MethodArgumentNotValidException ex) {
        Map<String, String> errors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .collect(Collectors.toMap(
                FieldError::getField,
                FieldError::getDefaultMessage,
                (a, b) -> a
            ));
        return new ErrorResponse("VALIDATION_ERROR", "Validation failed", errors);
    }

    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ErrorResponse handleGeneric(Exception ex) {
        log.error("Unexpected error", ex);
        return new ErrorResponse("INTERNAL_ERROR", "An unexpected error occurred");
    }
}

public record ErrorResponse(
    String code,
    String message,
    Map<String, String> details
) {
    public ErrorResponse(String code, String message) {
        this(code, message, null);
    }
}
```

## Request Mapping Options

```java
// Path variables
@GetMapping("/{userId}/orders/{orderId}")
public Order getOrder(
    @PathVariable Long userId,
    @PathVariable Long orderId) {}

// Query parameters
@GetMapping("/search")
public List<User> search(
    @RequestParam String query,
    @RequestParam(required = false) String status,
    @RequestParam(defaultValue = "name") String sortBy) {}

// Headers
@PostMapping
public void create(
    @RequestHeader("X-Request-Id") String requestId,
    @RequestHeader(value = "X-Tenant-Id", required = false) String tenantId) {}

// Request body
@PostMapping
public void create(@RequestBody @Valid CreateRequest request) {}

// Multipart file
@PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
public void upload(@RequestPart("file") MultipartFile file) {}
```

## Best Practices

1. **Use records for DTOs** - immutable, concise
2. **Validate at controller level** with @Valid
3. **Return appropriate HTTP status codes**
4. **Use @RestControllerAdvice** for global exception handling
5. **Never expose entities** - always use DTOs
6. **Version your API** - /api/v1/resource

## References

- [REST Controller Patterns](references/rest-controller-patterns.md) - Advanced patterns
- [Validation Patterns](references/validation-patterns.md) - Custom validators, groups
- [Exception Handling](references/exception-handling.md) - Global handlers, ProblemDetail
