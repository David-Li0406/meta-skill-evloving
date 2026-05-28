# REST API Patterns with Spring Boot

This reference covers best practices for building RESTful APIs with Spring Boot, following REST principles and industry standards.

## RESTful API Design Principles

### Resource-Based URLs

Design URLs around resources (nouns), not actions (verbs):

```
✅ GOOD                      ❌ BAD
GET    /api/users            /api/getUsers
GET    /api/users/1          /api/users/get/1
POST   /api/users            /api/createUser
PUT    /api/users/1          /api/updateUser/1
DELETE /api/users/1          /api/deleteUser/1
```

### HTTP Methods Mapping

Use HTTP methods correctly:

| Method | Operation | Idempotent | Safe |
|--------|-----------|------------|-------|
| GET | Read resource | ✅ | ✅ |
| POST | Create resource | ❌ | ❌ |
| PUT | Update/Replace | ✅ | ❌ |
| PATCH | Partial update | ❌ | ❌ |
| DELETE | Delete resource | ✅ | ❌ |

**Idempotent:** Multiple identical requests have same effect as single request
**Safe:** Doesn't modify server state

### URL Naming Conventions

- Use **plural nouns** for collections: `/api/users`, `/api/products`
- Use **kebab-case** for multi-word resources: `/api/user-preferences`
- Use **lowercase**: `/api/users` (not `/api/Users`)
- Keep URLs **hierarchical**:
  - `/api/users/1/orders` - Orders for user 1
  - `/api/users/1/orders/2` - Order 2 for user 1

## Controller Best Practices

### Thin Controllers

Controllers should only handle HTTP concerns:

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor  // Lombok for constructor injection
public class UserController {

    private final UserService userService;

    @GetMapping("/{id}")
    public ResponseEntity<UserDTO> getById(@PathVariable Long id) {
        // Controller only handles HTTP mapping
        UserDTO user = userService.findById(id);
        return ResponseEntity.ok(user);
    }

    @PostMapping
    public ResponseEntity<UserDTO> create(@Valid @RequestBody CreateUserRequest request) {
        UserDTO created = userService.create(request);
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(created);
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserDTO> update(
        @PathVariable Long id,
        @Valid @RequestBody UpdateUserRequest request
    ) {
        UserDTO updated = userService.update(id, request);
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        userService.delete(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping
    public ResponseEntity<Page<UserDTO>> search(
        @RequestParam(required = false) String email,
        @RequestParam(required = false) String name,
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size,
        @RequestParam(defaultValue = "name") String sortBy
    ) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(sortBy));
        Page<UserDTO> results = userService.search(email, name, pageable);
        return ResponseEntity.ok(results);
    }
}
```

### Controller Responsibilities

**DO in controllers:**
- Map HTTP methods to service calls
- Extract request parameters, path variables, request body
- Return appropriate HTTP status codes
- Add response headers when needed
- Trigger validation with `@Valid`

**DON'T do in controllers:**
- Business logic
- Database access
- Data transformation (beyond DTO mapping)
- Complex validation rules

### Request Mapping Best Practices

**1. Use specific mapping annotations:**

```java
@GetMapping("/users/{id}")        // Better than @RequestMapping(method=GET)
@PostMapping("/users")
@PutMapping("/users/{id}")
@PatchMapping("/users/{id}")
@DeleteMapping("/users/{id}")
```

**2. Use `@RequestMapping` for class-level configuration:**

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    // All paths prefixed with /api/v1/users
}
```

**3. Support multiple media types if needed:**

```java
@GetMapping(value = "/{id}", produces = {MediaType.APPLICATION_JSON_VALUE, MediaType.APPLICATION_XML_VALUE})
public ResponseEntity<UserDTO> getUser(@PathVariable Long id) {
    // Supports both JSON and XML
}
```

### Parameter Handling

**Path variables:**

```java
@GetMapping("/users/{id}")
public ResponseEntity<UserDTO> getUser(@PathVariable Long id) {
    // /users/123 → id = 123
}

@GetMapping("/users/{userId}/orders/{orderId}")
public ResponseEntity<OrderDTO> getOrder(
    @PathVariable Long userId,
    @PathVariable Long orderId
) {
    // /users/1/orders/99 → userId=1, orderId=99
}
```

**Query parameters:**

```java
@GetMapping("/users")
public ResponseEntity<List<UserDTO>> searchUsers(
    @RequestParam(required = false) String email,
    @RequestParam(required = false) String name,
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "10") int size
) {
    // /users?email=test@example.com&page=1&size=20
}
```

**Request body:**

```java
@PostMapping
public ResponseEntity<UserDTO> createUser(
    @Valid @RequestBody CreateUserRequest request
) {
    // Request body validated and mapped to CreateUserRequest
}
```

## HTTP Status Codes

Use appropriate HTTP status codes:

### Success Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 OK | Success | GET, PUT, PATCH successful |
| 201 Created | Resource created | POST successful |
| 204 No Content | Success, no content | DELETE successful |

### Client Error Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 400 Bad Request | Invalid input | Validation failures |
| 401 Unauthorized | Not authenticated | Missing/invalid token |
| 403 Forbidden | No permission | Authenticated but not authorized |
| 404 Not Found | Resource missing | GET non-existent resource |
| 409 Conflict | Conflict | Duplicate resource |
| 422 Unprocessable Entity | Semantic errors | Well-formed but invalid data |

### Server Error Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 500 Internal Server Error | Server error | Unhandled exceptions |
| 503 Service Unavailable | Server down | Maintenance or overload |

**Implementation example:**

```java
@PostMapping
public ResponseEntity<UserDTO> create(@Valid @RequestBody CreateUserRequest request) {
    UserDTO created = userService.create(request);
    return ResponseEntity
        .status(HttpStatus.CREATED)  // 201
        .header("Location", "/api/users/" + created.getId())
        .body(created);
}

@DeleteMapping("/{id}")
public ResponseEntity<Void> delete(@PathVariable Long id) {
    userService.delete(id);
    return ResponseEntity.noContent().build();  // 204
}
```

## DTO Pattern

### Why Use DTOs?

**Never expose entities directly to APIs:**

```java
// ❌ BAD - Exposes entity
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userRepository.findById(id).get();
}

// ✅ GOOD - Uses DTO
@GetMapping("/users/{id}")
public UserDTO getUser(@PathVariable Long id) {
    return userService.findById(id);
}
```

**Problems with exposing entities:**
1. Exposes sensitive data (passwords, internal fields)
2. Tight coupling between API and database schema
3. JPA lazy loading issues (LazyInitializationException)
4. Infinite recursion in JSON serialization
5. Loss of control over API contract

### DTO Design

**Request DTOs:**

```java
public class CreateUserRequest {
    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    @NotBlank(message = "Password is required")
    @Size(min = 8, message = "Password must be at least 8 characters")
    private String password;

    @NotBlank(message = "Name is required")
    private String name;

    // Getters and setters
}
```

**Response DTOs:**

```java
public class UserDTO {
    private Long id;
    private String email;
    private String name;
    private LocalDateTime createdAt;

    // Note: No password!
    // Getters and setters
}
```

### DTO Mapping

**Manual mapping:**

```java
public class UserMapper {
    public static UserDTO toDTO(User user) {
        UserDTO dto = new UserDTO();
        dto.setId(user.getId());
        dto.setEmail(user.getEmail());
        dto.setName(user.getName());
        dto.setCreatedAt(user.getCreatedAt());
        return dto;
    }

    public static User toEntity(CreateUserRequest request) {
        User user = new User();
        user.setEmail(request.getEmail());
        user.setPassword(request.getPassword());
        user.setName(request.getName());
        return user;
    }
}
```

**Using MapStruct (recommended):**

```java
@Mapper(componentModel = "spring")
public interface UserMapper {
    UserDTO toDTO(User user);
    User toEntity(CreateUserRequest request);
    List<UserDTO> toDTOList(List<User> users);
}
```

## Pagination

For large datasets, use pagination:

```java
@GetMapping("/users")
public ResponseEntity<Page<UserDTO>> getUsers(
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "10") int size,
    @RequestParam(defaultValue = "name") String sortBy
) {
    Pageable pageable = PageRequest.of(page, size, Sort.by(sortBy));
    Page<UserDTO> users = userService.findAll(pageable);
    return ResponseEntity.ok(users);
}
```

**Service layer:**

```java
@Service
public class UserService {
    public Page<UserDTO> findAll(Pageable pageable) {
        Page<User> users = userRepository.findAll(pageable);
        return users.map(UserMapper::toDTO);
    }
}
```

**Response includes:**
```json
{
  "content": [...],
  "pageable": {...},
  "totalPages": 10,
  "totalElements": 100,
  "last": false,
  "first": true,
  "size": 10,
  "number": 0
}
```

## API Versioning

**Strategy 1: URL Path Versioning**

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserV1Controller {
    // Version 1 implementation
}

@RestController
@RequestMapping("/api/v2/users")
public class UserV2Controller {
    // Version 2 implementation
}
```

**Strategy 2: Header Versioning**

```java
@GetMapping(value = "/users", headers = "X-API-Version=1")
public List<UserDTO> getUsersV1() {
    // Version 1
}

@GetMapping(value = "/users", headers = "X-API-Version=2")
public List<UserDTO> getUsersV2() {
    // Version 2
}
```

**Recommendation:** Use URL path versioning for clarity and cacheability.

## HATEOAS (Hypermedia)

Add links to related resources:

```java
@GetMapping("/users/{id}")
public ResponseEntity<EntityModel<UserDTO>> getUser(@PathVariable Long id) {
    UserDTO user = userService.findById(id);

    EntityModel<UserDTO> resource = EntityModel.of(user,
        linkTo(methodOn(UserController.class).getUser(id)).withSelfRel(),
        linkTo(methodOn(UserController.class).getUsers()).withRel("users"),
        linkTo(methodOn(OrderController.class).getUserOrders(id)).withRel("orders")
    );

    return ResponseEntity.ok(resource);
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "_links": {
    "self": { "href": "/api/users/1" },
    "users": { "href": "/api/users" },
    "orders": { "href": "/api/users/1/orders" }
  }
}
```

## OpenAPI Documentation

Add Springdoc OpenAPI dependency:

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
</dependency>
```

**Configure:**

```java
@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("My API")
                .version("1.0")
                .description("API documentation"));
    }
}
```

**Annotate controllers:**

```java
@RestController
@RequestMapping("/api/users")
@Tag(name = "User", description = "User management APIs")
public class UserController {

    @GetMapping("/{id}")
    @Operation(summary = "Get user by ID")
    @ApiResponses({
        @ApiResponse(responseCode = "200", description = "User found"),
        @ApiResponse(responseCode = "404", description = "User not found")
    })
    public ResponseEntity<UserDTO> getById(
        @Parameter(description = "User ID") @PathVariable Long id
    ) {
        // ...
    }
}
```

Access Swagger UI at: `http://localhost:8080/swagger-ui.html`

## Summary Checklist

- [ ] Use plural nouns for resource URLs
- [ ] Map HTTP methods to CRUD operations correctly
- [ ] Keep controllers thin (HTTP concerns only)
- [ ] Always use DTOs for API contracts
- [ ] Return appropriate HTTP status codes
- [ ] Add validation to request DTOs
- [ ] Use pagination for large datasets
- [ ] Implement API versioning
- [ ] Add OpenAPI documentation
- [ ] Handle exceptions globally with @ControllerAdvice

## Resources

- [10 Spring Boot API Best Practices](https://medium.com/@himanshu675/10-spring-boot-api-best-practices-most-developers-learn-too-late-b11c6467c50c)
- [12 Spring Boot REST API Best Practices](https://www.codingshuttle.com/blogs/best-practices-for-writing-spring-boot-api/)
- [Building RESTful APIs with Spring Boot](https://blog.nashtechglobal.com/building-restful-apis-with-spring-boot-controllers-mapping-and-response-best-practices/)
- [Controller-Service-Repository Pattern](https://tom-collings.medium.com/controller-service-repository-16e29a4684e5)
