---
id: java-spring-boot-patterns
name: "Java Spring Boot"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Java Spring Boot

## Overview

Spring Boot is an opinionated framework for building production-ready Spring applications. This methodology covers project setup, layered architecture, and best practices for enterprise Java development.

## When to Use

- Enterprise applications
- Microservices architecture
- REST APIs
- Applications requiring robust dependency injection
- Projects with complex transaction management

## Key Principles

1. **Convention over configuration** - Sensible defaults
2. **Dependency injection** - Loose coupling through IoC
3. **Layered architecture** - Separation of concerns
4. **Aspect-oriented programming** - Cross-cutting concerns
5. **Production-ready** - Actuator, metrics, health checks

## Best Practices

### Project Structure

```
src/main/java/com/example/app/
├── Application.java
├── config/
│   ├── SecurityConfig.java
│   ├── WebConfig.java
│   └── OpenApiConfig.java
├── controller/
│   ├── UserController.java
│   └── advice/
│       └── GlobalExceptionHandler.java
├── service/
│   ├── UserService.java
│   └── impl/
│       └── UserServiceImpl.java
├── repository/
│   └── UserRepository.java
├── entity/
│   ├── User.java
│   └── BaseEntity.java
├── dto/
│   ├── request/
│   │   ├── CreateUserRequest.java
│   │   └── UpdateUserRequest.java
│   └── response/
│       └── UserResponse.java
├── mapper/
│   └── UserMapper.java
├── exception/
│   ├── ResourceNotFoundException.java
│   └── BusinessException.java
└── util/
    └── Constants.java

src/main/resources/
├── application.yml
├── application-dev.yml
└── application-prod.yml

src/test/java/com/example/app/
├── controller/
├── service/
└── repository/
```

### Entity Layer

```java
// entity/BaseEntity.java
package com.example.app.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.Instant;
import java.util.UUID;

@Getter
@Setter
@MappedSuperclass
public abstract class BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt;

    @Version
    private Long version;
}

// entity/User.java
package com.example.app.entity;

import jakarta.persistence.*;
import lombok.*;

import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "users", indexes = {
    @Index(name = "idx_users_email", columnList = "email", unique = true),
    @Index(name = "idx_users_organization", columnList = "organization_id")
})
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User extends BaseEntity {

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String password;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    @Builder.Default
    private UserRole role = UserRole.MEMBER;

    @Column(name = "is_active")
    @Builder.Default
    private boolean active = true;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "organization_id", nullable = false)
    private Organization organization;

    @OneToMany(mappedBy = "author", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private Set<Post> posts = new HashSet<>();

    public enum UserRole {
        ADMIN, MODERATOR, MEMBER
    }

    public void addPost(Post post) {
        posts.add(post);
        post.setAuthor(this);
    }

    public void removePost(Post post) {
        posts.remove(post);
        post.setAuthor(null);
    }
}
```

### Repository Layer

```java
// repository/UserRepository.java
package com.example.app.repository;

import com.example.app.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface UserRepository extends JpaRepository<User, UUID>, JpaSpecificationExecutor<User> {

    Optional<User> findByEmail(String email);

    boolean existsByEmailAndOrganizationId(String email, UUID organizationId);

    @Query("SELECT u FROM User u WHERE u.organization.id = :orgId AND u.active = true")
    Page<User> findActiveByOrganization(@Param("orgId") UUID organizationId, Pageable pageable);

    @Query("""
        SELECT u FROM User u
        WHERE u.organization.id = :orgId
        AND (LOWER(u.name) LIKE LOWER(CONCAT('%', :search, '%'))
             OR LOWER(u.email) LIKE LOWER(CONCAT('%', :search, '%')))
        """)
    Page<User> searchInOrganization(
        @Param("orgId") UUID organizationId,
        @Param("search") String search,
        Pageable pageable
    );

    @Modifying
    @Query("UPDATE User u SET u.active = false WHERE u.id = :id")
    void deactivate(@Param("id") UUID id);
}

// repository/specification/UserSpecification.java
package com.example.app.repository.specification;

import com.example.app.entity.User;
import com.example.app.entity.User.UserRole;
import org.springframework.data.jpa.domain.Specification;

import java.util.UUID;

public class UserSpecification {

    public static Specification<User> inOrganization(UUID organizationId) {
        return (root, query, cb) ->
            cb.equal(root.get("organization").get("id"), organizationId);
    }

    public static Specification<User> hasRole(UserRole role) {
        return (root, query, cb) -> cb.equal(root.get("role"), role);
    }

    public static Specification<User> isActive(boolean active) {
        return (root, query, cb) -> cb.equal(root.get("active"), active);
    }

    public static Specification<User> searchByNameOrEmail(String search) {
        return (root, query, cb) -> {
            String pattern = "%" + search.toLowerCase() + "%";
            return cb.or(
                cb.like(cb.lower(root.get("name")), pattern),
                cb.like(cb.lower(root.get("email")), pattern)
            );
        };
    }
}
```

### Service Layer

```java
// service/UserService.java
package com.example.app.service;

import com.example.app.dto.request.CreateUserRequest;
import com.example.app.dto.request.UpdateUserRequest;
import com.example.app.dto.response.UserResponse;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.UUID;

public interface UserService {
    UserResponse create(CreateUserRequest request, UUID organizationId);
    UserResponse getById(UUID id);
    UserResponse update(UUID id, UpdateUserRequest request);
    void delete(UUID id);
    Page<UserResponse> search(UUID organizationId, String search, String role, Pageable pageable);
}

// service/impl/UserServiceImpl.java
package com.example.app.service.impl;

import com.example.app.dto.request.CreateUserRequest;
import com.example.app.dto.request.UpdateUserRequest;
import com.example.app.dto.response.UserResponse;
import com.example.app.entity.User;
import com.example.app.exception.ResourceNotFoundException;
import com.example.app.exception.BusinessException;
import com.example.app.mapper.UserMapper;
import com.example.app.repository.UserRepository;
import com.example.app.repository.OrganizationRepository;
import com.example.app.service.UserService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

import static com.example.app.repository.specification.UserSpecification.*;

@Service
@RequiredArgsConstructor
@Slf4j
@Transactional(readOnly = true)
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final OrganizationRepository organizationRepository;
    private final UserMapper userMapper;
    private final PasswordEncoder passwordEncoder;

    @Override
    @Transactional
    public UserResponse create(CreateUserRequest request, UUID organizationId) {
        log.info("Creating user with email: {}", request.email());

        if (userRepository.existsByEmailAndOrganizationId(request.email(), organizationId)) {
            throw new BusinessException("User with this email already exists");
        }

        var organization = organizationRepository.findById(organizationId)
            .orElseThrow(() -> new ResourceNotFoundException("Organization", organizationId));

        var user = User.builder()
            .name(request.name())
            .email(request.email().toLowerCase())
            .password(passwordEncoder.encode(request.password()))
            .role(request.role() != null ? request.role() : User.UserRole.MEMBER)
            .organization(organization)
            .build();

        user = userRepository.save(user);
        log.info("Created user with id: {}", user.getId());

        return userMapper.toResponse(user);
    }

    @Override
    public UserResponse getById(UUID id) {
        return userRepository.findById(id)
            .map(userMapper::toResponse)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
    }

    @Override
    @Transactional
    public UserResponse update(UUID id, UpdateUserRequest request) {
        var user = userRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));

        if (request.name() != null) {
            user.setName(request.name());
        }
        if (request.email() != null) {
            user.setEmail(request.email().toLowerCase());
        }
        if (request.role() != null) {
            user.setRole(request.role());
        }

        return userMapper.toResponse(userRepository.save(user));
    }

    @Override
    @Transactional
    public void delete(UUID id) {
        if (!userRepository.existsById(id)) {
            throw new ResourceNotFoundException("User", id);
        }
        userRepository.deactivate(id);
        log.info("Deactivated user with id: {}", id);
    }

    @Override
    public Page<UserResponse> search(UUID organizationId, String search, String role, Pageable pageable) {
        Specification<User> spec = Specification.where(inOrganization(organizationId))
            .and(isActive(true));

        if (search != null && !search.isBlank()) {
            spec = spec.and(searchByNameOrEmail(search));
        }
        if (role != null && !role.isBlank()) {
            spec = spec.and(hasRole(User.UserRole.valueOf(role.toUpperCase())));
        }

        return userRepository.findAll(spec, pageable)
            .map(userMapper::toResponse);
    }
}
```

### DTO and Mapper

```java
// dto/request/CreateUserRequest.java
package com.example.app.dto.request;

import com.example.app.entity.User.UserRole;
import jakarta.validation.constraints.*;

public record CreateUserRequest(
    @NotBlank @Size(min = 2, max = 100)
    String name,

    @NotBlank @Email
    String email,

    @NotBlank @Size(min = 8)
    String password,

    UserRole role
) {}

// dto/response/UserResponse.java
package com.example.app.dto.response;

import com.example.app.entity.User.UserRole;
import java.time.Instant;
import java.util.UUID;

public record UserResponse(
    UUID id,
    String name,
    String email,
    UserRole role,
    boolean active,
    Instant createdAt,
    Instant updatedAt
) {}

// mapper/UserMapper.java
package com.example.app.mapper;

import com.example.app.dto.response.UserResponse;
import com.example.app.entity.User;
import org.mapstruct.Mapper;
import org.mapstruct.MappingConstants;

@Mapper(componentModel = MappingConstants.ComponentModel.SPRING)
public interface UserMapper {
    UserResponse toResponse(User user);
}
```

### Controller Layer

```java
// controller/UserController.java
package com.example.app.controller;

import com.example.app.dto.request.CreateUserRequest;
import com.example.app.dto.request.UpdateUserRequest;
import com.example.app.dto.response.UserResponse;
import com.example.app.service.UserService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Tag(name = "Users", description = "User management API")
public class UserController {

    private final UserService userService;

    @GetMapping
    @Operation(summary = "Search users")
    public Page<UserResponse> search(
        @AuthenticationPrincipal AuthUser authUser,
        @RequestParam(required = false) String search,
        @RequestParam(required = false) String role,
        @PageableDefault(size = 20, sort = "createdAt") Pageable pageable
    ) {
        return userService.search(authUser.getOrganizationId(), search, role, pageable);
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get user by ID")
    public UserResponse getById(@PathVariable UUID id) {
        return userService.getById(id);
    }

    @PostMapping
    @Operation(summary = "Create new user")
    public ResponseEntity<UserResponse> create(
        @AuthenticationPrincipal AuthUser authUser,
        @Valid @RequestBody CreateUserRequest request
    ) {
        var response = userService.create(request, authUser.getOrganizationId());
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PatchMapping("/{id}")
    @Operation(summary = "Update user")
    public UserResponse update(
        @PathVariable UUID id,
        @Valid @RequestBody UpdateUserRequest request
    ) {
        return userService.update(id, request);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    @Operation(summary = "Delete user")
    public void delete(@PathVariable UUID id) {
        userService.delete(id);
    }
}
```

### Exception Handling

```java
// exception/ResourceNotFoundException.java
package com.example.app.exception;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String resource, Object id) {
        super(String.format("%s not found with id: %s", resource, id));
    }
}

// controller/advice/GlobalExceptionHandler.java
package com.example.app.controller.advice;

import com.example.app.exception.BusinessException;
import com.example.app.exception.ResourceNotFoundException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;

@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ProblemDetail handleNotFound(ResourceNotFoundException ex) {
        var problem = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
        problem.setProperty("timestamp", Instant.now());
        return problem;
    }

    @ExceptionHandler(BusinessException.class)
    public ProblemDetail handleBusiness(BusinessException ex) {
        var problem = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, ex.getMessage());
        problem.setProperty("timestamp", Instant.now());
        return problem;
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getFieldErrors()
            .forEach(e -> errors.put(e.getField(), e.getDefaultMessage()));

        var problem = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "Validation failed");
        problem.setProperty("errors", errors);
        problem.setProperty("timestamp", Instant.now());
        return problem;
    }

    @ExceptionHandler(Exception.class)
    public ProblemDetail handleGeneral(Exception ex) {
        log.error("Unexpected error", ex);
        var problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.INTERNAL_SERVER_ERROR,
            "An unexpected error occurred"
        );
        problem.setProperty("timestamp", Instant.now());
        return problem;
    }
}
```

## Anti-patterns

### Avoid: Anemic Domain Model

```java
// BAD - logic in service, entity is just data
public class User {
    private String email;
    // only getters/setters
}

public class UserService {
    public void promoteToAdmin(User user) {
        user.setRole(Role.ADMIN);
    }
}

// GOOD - rich domain model
public class User {
    public void promote() {
        if (this.role == Role.ADMIN) {
            throw new IllegalStateException("Already admin");
        }
        this.role = Role.ADMIN;
    }
}
```

### Avoid: N+1 Queries

```java
// BAD - N+1 query
List<User> users = userRepository.findAll();
users.forEach(u -> System.out.println(u.getOrganization().getName()));

// GOOD - fetch join
@Query("SELECT u FROM User u JOIN FETCH u.organization")
List<User> findAllWithOrganization();
```

## References

- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Spring Data JPA](https://spring.io/projects/spring-data-jpa)
- [Baeldung Spring Tutorials](https://www.baeldung.com/spring-boot)
- [Spring Guides](https://spring.io/guides)
