---
name: spring-boot-api-documentation
description: Use this skill to auto-generate comprehensive OpenAPI 3 documentation for Spring Boot REST APIs, including setup, configuration, and endpoint documentation.
---

# Spring Boot API Documentation with SpringDoc

Auto-generate OpenAPI 3 documentation for Spring Boot REST APIs using SpringDoc OpenAPI.

## When to Use

Use this skill when you need to:
- Set up SpringDoc OpenAPI in Spring Boot projects
- Generate OpenAPI 3.0 specifications for REST APIs
- Configure and customize Swagger UI
- Document request/response models with validation
- Implement API security documentation (JWT, OAuth2)
- Document pageable and sortable endpoints
- Add examples and schemas to API endpoints
- Support multiple API groups and versions
- Document error responses and exception handlers
- Auto-generate documentation when API endpoints change or controllers are modified

## Setup Dependencies

### Add Maven Dependencies

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.8.14</version> <!-- Use latest stable version -->
</dependency>
```

### Add Gradle Dependencies

```gradle
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.8.14'
```

## Configure SpringDoc

### Basic Configuration

```properties
# application.properties
springdoc.api-docs.path=/v3/api-docs
springdoc.swagger-ui.path=/swagger-ui.html
springdoc.swagger-ui.enabled=true
springdoc.api-docs.enabled=true
springdoc.packages-to-scan=com.example.controller
springdoc.paths-to-match=/api/**
```

```yaml
# application.yml
springdoc:
  api-docs:
    path: /v3/api-docs
    enabled: true
  swagger-ui:
    path: /swagger-ui.html
    enabled: true
  packages-to-scan: com.example.controller
  paths-to-match: /api/**
```

### Access Endpoints

After configuration:
- **OpenAPI JSON**: `http://localhost:8080/v3/api-docs`
- **Swagger UI**: `http://localhost:8080/swagger-ui.html`

## Document Controllers

### Basic Controller Documentation

```java
@RestController
@RequestMapping("/api/users")
@Tag(name = "User Management", description = "APIs for managing users")
public class UserController {

    @Operation(summary = "Get user by ID", description = "Returns a single user")
    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        // Implementation here
    }

    @Operation(summary = "Create user", description = "Creates a new user")
    @PostMapping
    public ResponseEntity<User> createUser(@Valid @RequestBody User user) {
        // Implementation here
    }
}
```

### Document Request Bodies

```java
@Operation(summary = "Create a new book")
@PostMapping
public Book createBook(@RequestBody Book book) {
    // Implementation here
}
```

## Document Models

### Entity with Validation

```java
@Schema(description = "User entity representing a system user")
public class User {
    @Schema(description = "Unique identifier", example = "12345", accessMode = Schema.AccessMode.READ_ONLY)
    private Long id;

    @NotBlank
    @Schema(description = "User's full name", example = "John Doe", requiredMode = Schema.RequiredMode.REQUIRED)
    private String name;

    @Email
    @Schema(description = "User's email address", example = "john.doe@example.com")
    private String email;
}
```

## Document Security

### JWT Bearer Authentication

```java
@Configuration
public class OpenAPISecurityConfig {
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .components(new Components()
                .addSecuritySchemes("bearer-jwt", new SecurityScheme()
                    .type(SecurityScheme.Type.HTTP)
                    .scheme("bearer")
                    .bearerFormat("JWT")
                    .description("JWT authentication")
                )
            );
    }
}
```

## Document Pagination

### Spring Data Pageable Support

```java
@GetMapping("/users")
@Operation(summary = "Get paginated users")
public Page<User> getUsers(@ParameterObject Pageable pageable) {
    // Implementation here
}
```

## Error Handling

### Global Exception Handler

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(EntityNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(EntityNotFoundException ex) {
        return new ErrorResponse("NOT_FOUND", ex.getMessage());
    }
}
```

## Best Practices

1. **Use descriptive operation summaries and descriptions**
2. **Document all response codes**
3. **Add examples to request/response bodies**
4. **Leverage JSR-303 validation annotations**
5. **Group related endpoints with @Tag**
6. **Document security requirements**
7. **Hide internal/admin endpoints appropriately**
8. **Customize Swagger UI for better UX**
9. **Version your API documentation**

## References

- [SpringDoc Official Documentation](https://springdoc.org/)
- [OpenAPI 3.0 Specification](https://swagger.io/specification/)
- [Swagger UI Configuration](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)