# Spring Boot Project Structure Best Practices

This reference provides detailed guidance on organizing Spring Boot projects for scalability and maintainability.

## Architecture Patterns

### Layered Architecture (Classic)

The traditional approach organizes code by technical layer:

```
com.example.myapp/
├── controller/          # Presentation layer - HTTP endpoints
├── service/             # Business logic layer
├── repository/          # Data access layer
├── model/ or entity/    # JPA entities
├── dto/                 # Data Transfer Objects
├── config/              # Configuration classes
├── exception/           # Custom exceptions
└── util/                # Utility classes
```

**Pros:**
- Simple to understand
- Clear separation of concerns
- Works well for small to medium apps

**Cons:**
- Doesn't scale well for large apps
- Harder to find related code
- Can lead to circular dependencies

### Feature-Based Architecture (Scalable)

Organize by business domain/feature instead of technical layer:

```
com.example.myapp/
├── user/
│   ├── Usercontroller.java
│   ├── UserService.java
│   ├── UserRepository.java
│   ├── User.java
│   ├── UserDTO.java
│   └── UserMapper.java
├── order/
│   ├── OrderController.java
│   ├── OrderService.java
│   ├── OrderRepository.java
│   ├── Order.java
│   ├── OrderDTO.java
│   └── OrderMapper.java
├── product/
│   ├── ProductController.java
│   ├── ProductService.java
│   └── ProductRepository.java
├── shared/
│   ├── config/
│   ├── exceptions/
│   ├── dtos/
│   └── utils/
└── MyApplication.java
```

**Pros:**
- Scales beautifully for large apps
- Easy to locate all related code
- Clear feature boundaries
- Supports independent feature development

**Cons:**
- More initial complexity
- Requires discipline to maintain boundaries

**Recommendation:** Use feature-based organization for applications with more than 5-6 entities or complex business logic.

### Domain-Driven Design (DDD) Style

For complex domains, use DDD principles:

```
com.example.myapp/
├── domain/
│   ├── model/
│   ├── repository/
│   └── service/
├── application/
│   ├── service/
│   └── dto/
├── infrastructure/
│   ├── persistence/
│   ├── config/
│   └── security/
└── interfaces/
    ├── rest/
    └── dto/
```

This follows clean architecture principles with clear dependency direction.

## Package Structure Best Practices

### 1. Base Package Structure

Always start with a reverse domain name:

```java
package com.companyname.appname;
```

Example: `com.example.ecommerce`

### 2. Application Class

Place main application class at the root of your base package:

```java
package com.example.myapp;

@SpringBootApplication
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

This allows Spring to automatically discover all components in subpackages.

### 3. Layer Organization

For layer-based architecture:

```
com.example.myapp
├── controller/
│   ├── UserController.java
│   └── OrderController.java
├── service/
│   ├── UserService.java
│   └── OrderService.java
├── repository/
│   ├── UserRepository.java
│   └── OrderRepository.java
├── entity/
│   ├── User.java
│   └── Order.java
├── dto/
│   ├── UserDTO.java
│   └── OrderDTO.java
├── config/
│   ├── SecurityConfig.java
│   └── DatabaseConfig.java
├── exception/
│   ├── ResourceNotFoundException.java
│   └── GlobalExceptionHandler.java
└── util/
    └── DateUtils.java
```

### 4. Feature Organization

For feature-based architecture:

```
com.example.myapp
├── user/
│   ├── api/
│   │   ├── Usercontroller.java
│   │   └── UserDTO.java
│   ├── domain/
│   │   ├── User.java
│   │   └── UserRepository.java
│   └── service/
│   │   └── UserService.java
├── order/
│   ├── api/
│   │   ├── OrderController.java
│   │   └── OrderDTO.java
│   ├── domain/
│   │   ├── Order.java
│   │   └── OrderRepository.java
│   └── service/
│   │   └── OrderService.java
└── shared/
    ├── config/
    ├── exception/
    └── util/
```

## Configuration Placement

### Global Configuration

Place application-wide configuration in the `config` package:

```
config/
├── SecurityConfig.java         # Spring Security
├── DatabaseConfig.java         # Database configuration
├── CacheConfig.java            # Caching setup
├── AsyncConfig.java            # Async execution
├── ValidationConfig.java       # Custom validators
└── WebConfig.java              # MVC configuration
```

### Feature-Specific Configuration

If a configuration is feature-specific, place it within the feature package:

```
user/
└── config/
    └── UserAuditConfig.java    # User-specific config
```

## Exception Handling Organization

Create dedicated exception package structure:

```
exception/
├── GlobalExceptionHandler.java      # @ControllerAdvice
├── ResourceNotFoundException.java   # 404 errors
├── DuplicateResourceException.java  # 409 errors
├── BusinessException.java           # Base business exception
├── dto/
│   └── ErrorResponse.java           # Error response format
└── enums/
    └── ErrorCode.java               # Error code constants
```

## Test Organization

Mirror your main package structure in test directory:

```
src/test/java/com/example/myapp/
├── controller/
│   ├── UserControllerTest.java
│   └── OrderControllerTest.java
├── service/
│   ├── UserServiceTest.java
│   └── OrderServiceTest.java
├── repository/
│   └── UserRepositoryTest.java
└── config/
    └── SecurityConfigTest.java
```

### Test Structure Options

**Option 1: Test class naming**
- `UserServiceTest` - Unit tests
- `UserServiceIntegrationTest` - Integration tests
- `UserServiceTest` - Combined (use `@Nested` for organization)

**Option 2: Separate test packages**
- `com.example.myapp.service.UserServiceTest` - Unit tests
- `com.example.myapp.service.int.UserServiceIntegrationTest` - Integration tests

## Resource File Organization

```
src/main/resources/
├── application.yml              # Main configuration
├── application-dev.yml          # Development profile
├── application-test.yml         # Test profile
├── application-prod.yml         # Production profile
├── static/                      # Static assets (CSS, JS, images)
├── templates/                   # Thymeleaf templates
├── db/
│   └── migration/               # Database migrations
│       ├── V1__init_schema.sql
│       └── V2__add_users.sql
└── i18n/                        # Internationalization
    ├── messages.properties
    └── messages_fr.properties
```

## Module Structure (Multi-Module Projects)

For large applications, consider multi-module Maven/Gradle structure:

```
myapp/
├── myapp-core/              # Core business logic
├── myapp-api/               # REST API layer
├── myapp-persistence/       # Data access
├── myapp-security/          # Security module
├── myapp-common/            # Shared utilities
└── myapp-frontend/          # Web UI (optional)
```

**pom.xml example:**
```xml
<modules>
    <module>myapp-core</module>
    <module>myapp-api</module>
    <module>myapp-persistence</module>
    <module>myapp-security</module>
    <module>myapp-common</module>
</modules>
```

## Naming Conventions

### Classes

- **Controllers**: `{Entity}Controller` or `{Resource}Controller`
  - Examples: `UserController`, `OrderController`, `ProductController`

- **Services**: `{Entity}Service` or `{Feature}Service`
  - Examples: `UserService`, `OrderService`, `PaymentService`

- **Repositories**: `{Entity}Repository`
  - Examples: `UserRepository`, `OrderRepository`

- **Entities**: `{Entity}` (domain noun)
  - Examples: `User`, `Order`, `Product`

- **DTOs**: `{Entity}DTO`, `{Operation}{Entity}Request/Response`
  - Examples: `UserDTO`, `CreateUserRequest`, `UpdateUserRequest`, `UserResponse`

- **Exceptions**: `{Problem}Exception`
  - Examples: `ResourceNotFoundException`, `DuplicateResourceException`

- **Config classes**: `{Feature}Config`
  - Examples: `SecurityConfig`, `CacheConfig`, `DatabaseConfig`

### Packages

- Use lowercase
- Use singular nouns
- Avoid abbreviations (use `repository` not `repo`, `util` not `utils`)
- Be consistent across the project

## Dependencies Between Layers

**Allowed dependencies (direction matters):**

```
Controller → Service → Repository → Entity
    ↓         ↓          ↓
   DTO      DTO      Entity
```

**Rules:**
- Controllers can depend on Services and DTOs
- Services can depend on Repositories, Entities, and DTOs
- Repositories can depend on Entities
- Entities should never depend on any other application layer

**Anti-patterns to avoid:**
- ❌ Service calling Controller
- ❌ Repository calling Service
- ❌ Entity calling Service
- ❌ Circular dependencies between packages

## Summary Checklist

- [ ] Choose architecture pattern (layer vs feature-based)
- [ ] Set up base package with reverse domain
- [ ] Place main application class at root
- [ ] Create consistent package structure
- [ ] Organize config classes in dedicated package
- [ ] Set up exception handling package
- [ ] Mirror structure in test directory
- [ ] Use consistent naming conventions
- [ ] Avoid circular dependencies
- [ ] Document architecture decisions

## Resources

- [SpringBoot Best Practice Architecture](https://github.com/tomoyane/springboot-bestpractice)
- [Best Practices for Spring Boot Project Structure](https://codingnomads.com/java-spring-project-structure-best-practices)
- [Spring Boot Architecture Guide](https://www.geeksforgeeks.org/springboot/spring-boot-architecture/)
