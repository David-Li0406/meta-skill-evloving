---
name: Java Project Structure
description: Standard project layout, package conventions, module system, and layered architecture patterns.
metadata:
  labels: [java, project, architecture, structure]
  triggers:
    files: ['pom.xml', 'build.gradle', 'build.gradle.kts', 'settings.gradle', 'module-info.java']
    keywords: [src/main/java, src/test/java, module-info, package, module]
---

# Java Project Structure Standards

## Standard Maven/Gradle Layout

```
project-root/
├── src/
│   ├── main/
│   │   ├── java/           # Application source code
│   │   │   └── com/example/app/
│   │   │       ├── Application.java
│   │   │       ├── config/
│   │   │       ├── controller/
│   │   │       ├── service/
│   │   │       ├── repository/
│   │   │       ├── model/
│   │   │       └── exception/
│   │   └── resources/      # Configuration files
│   │       ├── application.yml
│   │       ├── application-dev.yml
│   │       ├── application-prod.yml
│   │       └── db/migration/
│   └── test/
│       ├── java/           # Test source code
│       │   └── com/example/app/
│       │       ├── controller/
│       │       ├── service/
│       │       └── repository/
│       └── resources/      # Test resources
│           └── application-test.yml
├── pom.xml                 # Maven build
├── build.gradle.kts        # or Gradle build
└── README.md
```

## Package Naming Conventions

```java
// Reverse domain name + project + layer
com.company.project.controller
com.company.project.service
com.company.project.repository
com.company.project.model
com.company.project.dto
com.company.project.exception
com.company.project.config
com.company.project.util

// Feature-based alternative
com.company.project.user.controller
com.company.project.user.service
com.company.project.order.controller
com.company.project.order.service
```

## Layered Architecture

```
┌─────────────────────────────────────────┐
│           Controller Layer              │  ← HTTP handling, validation
├─────────────────────────────────────────┤
│            Service Layer                │  ← Business logic
├─────────────────────────────────────────┤
│          Repository Layer               │  ← Data access
├─────────────────────────────────────────┤
│           Model/Entity                  │  ← Domain objects
└─────────────────────────────────────────┘

// Dependency rules:
// Controller → Service → Repository → Model
// NEVER: Repository → Service or Model → anything
```

```java
// Controller - handles HTTP
@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;
    // Only UserService, never UserRepository
}

// Service - business logic
@Service
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
    // Can use multiple repositories and services
}

// Repository - data access
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    // Only data operations
}
```

## DTO Pattern

```java
// Separate DTOs for request/response
public record CreateUserRequest(
    @NotBlank String name,
    @Email String email
) {}

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

// Mapper interface
public interface UserMapper {
    User toEntity(CreateUserRequest request);
    UserResponse toResponse(User user);
}
```

## Module System (JPMS)

```java
// module-info.java
module com.example.app {
    // Dependencies
    requires java.sql;
    requires spring.boot;
    requires spring.boot.autoconfigure;
    requires spring.web;

    // What we export
    exports com.example.app.api;
    exports com.example.app.model;

    // Internal packages (not exported)
    // com.example.app.internal is hidden

    // Reflection access for frameworks
    opens com.example.app.model to spring.core;
    opens com.example.app to spring.beans;
}
```

## Multi-Module Project

```
parent-project/
├── pom.xml                    # Parent POM
├── core/                      # Shared domain, utils
│   ├── pom.xml
│   └── src/main/java/
├── api/                       # REST API module
│   ├── pom.xml
│   └── src/main/java/
├── service/                   # Business logic
│   ├── pom.xml
│   └── src/main/java/
└── infrastructure/            # External integrations
    ├── pom.xml
    └── src/main/java/
```

## Best Practices

1. **One class per file** - class name matches file name
2. **Package by layer OR feature** - pick one, be consistent
3. **Keep packages flat** - avoid deep nesting
4. **Separate DTOs from entities** - never expose entities in API
5. **module-info.java** for libraries, optional for applications
6. **Resources alongside code** - feature-specific configs with feature

## References

- [Maven Project Layout](references/maven-project-layout.md) - Complete structure, profiles
- [Module System](references/module-system.md) - JPMS patterns, migration
