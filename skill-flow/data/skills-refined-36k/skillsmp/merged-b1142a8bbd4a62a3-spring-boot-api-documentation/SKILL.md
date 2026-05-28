---
name: spring-boot-api-documentation
description: Use this skill to auto-generate OpenAPI 3 documentation for Spring Boot REST APIs, applicable for both Spring Boot 3.x and 4.x projects. Activate when API endpoints change, controllers are modified, or documentation requests are made.
---

# Spring Boot API Documentation Skill

Auto-generate OpenAPI 3 documentation for Spring Boot REST APIs using springdoc-openapi.

## When to Use

Use this skill when you need to:
- Auto-generate OpenAPI specifications for REST APIs in Spring Boot 3.x or 4.x.
- Document API endpoints when they are added or modified.
- Respond to user requests for API documentation, Swagger, or OpenAPI.
- Configure security schemes and grouped API definitions.

## Setup Dependencies

### Add Maven Dependencies

For Spring Boot 3.x:

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.8.14</version>
</dependency>
```

For Spring Boot 4.x:

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>3.0.0</version>
</dependency>
```

### Add Gradle Dependencies

For Spring Boot 3.x:

```gradle
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.8.14'
```

For Spring Boot 4.x:

```gradle
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:3.0.0'
```

## Default URLs After Setup

- **Swagger UI**: `http://localhost:8080/swagger-ui.html`
- **OpenAPI JSON**: `http://localhost:8080/v3/api-docs`
- **OpenAPI YAML**: `http://localhost:8080/v3/api-docs.yaml`

## Documenting Controllers

### Basic REST Controller Example

```java
@RestController
@RequestMapping("/api/users")
@Tag(name = "User Management", description = "APIs for managing users")
public class UserController {

    @GetMapping("/{id}")
    @Operation(summary = "Get user by ID", description = "Returns a single user")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "User found",
            content = @Content(schema = @Schema(implementation = User.class))),
        @ApiResponse(responseCode = "404", description = "User not found")
    })
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    @Operation(summary = "Create user", description = "Creates a new user")
    @ApiResponse(responseCode = "201", description = "User created successfully")
    public ResponseEntity<User> createUser(@Valid @RequestBody User user) {
        User created = userService.save(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
```

### Documenting DTOs

```java
@Schema(description = "User entity representing a system user")
public class User {
    @Schema(description = "Unique identifier", example = "12345", accessMode = Schema.AccessMode.READ_ONLY)
    private Long id;

    @Schema(description = "User's full name", example = "John Doe", requiredMode = Schema.RequiredMode.REQUIRED)
    @NotBlank
    private String name;

    @Schema(description = "User's email address", example = "john.doe@example.com", format = "email")
    @Email
    private String email;

    @Schema(description = "Account creation timestamp", example = "2025-01-15T10:30:00Z")
    private Instant createdAt;

    @Schema(description = "User's role in the system", example = "ADMIN")
    private UserRole role;
}
```

## Security Configuration

### Security Scheme Example

```java
@Configuration
@OpenAPIDefinition(
    info = @Info(
        title = "My Application API",
        version = "1.0.0",
        description = "REST API documentation"
    )
)
@SecurityScheme(
    name = "bearerAuth",
    type = SecuritySchemeType.HTTP,
    scheme = "bearer",
    bearerFormat = "JWT",
    description = "JWT Authentication"
)
public class OpenApiSecurityConfig {
    // Additional security configuration
}
```

## Grouping APIs

### Example of Grouped APIs

```java
@Bean
public GroupedOpenApi publicApi() {
    return GroupedOpenApi.builder()
            .group("public-api")
            .pathsToMatch("/api/public/**")
            .build();
}

@Bean
public GroupedOpenApi adminApi() {
    return GroupedOpenApi.builder()
            .group("admin-api")
            .pathsToMatch("/api/admin/**")
            .build();
}
```

## Best Practices

1. **Use OpenAPI annotations** to enhance auto-generated documentation.
2. **Document all request/response DTOs** with `@Schema`.
3. **Group related APIs** logically using `GroupedOpenApi`.
4. **Secure your documentation** in production environments.
5. **Provide examples** in your API documentation for clarity.

## References

- [springdoc-openapi GitHub](https://github.com/springdoc/springdoc-openapi)
- [OpenAPI 3 Specification](https://spec.openapis.org/oas/v3.1.0)
- [Swagger UI Configuration](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/)