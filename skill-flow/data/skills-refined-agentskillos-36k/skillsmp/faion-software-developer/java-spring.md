# Java Spring Boot Backend Development

**Java backend patterns for production-grade applications with Spring Boot framework.**

---

## Spring Boot Patterns

### Problem
Structure Spring Boot applications with clean architecture.

### Framework: Controller Layer

```java
// src/main/java/com/example/controller/UserController.java

package com.example.controller;

import com.example.dto.CreateUserRequest;
import com.example.dto.UpdateUserRequest;
import com.example.dto.UserResponse;
import com.example.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping
    public ResponseEntity<Page<UserResponse>> listUsers(Pageable pageable) {
        return ResponseEntity.ok(userService.findAll(pageable));
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }

    @PostMapping
    public ResponseEntity<UserResponse> createUser(
            @Valid @RequestBody CreateUserRequest request) {
        UserResponse user = userService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }

    @PutMapping("/{id}")
    public ResponseEntity<UserResponse> updateUser(
            @PathVariable Long id,
            @Valid @RequestBody UpdateUserRequest request) {
        return ResponseEntity.ok(userService.update(id, request));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.delete(id);
        return ResponseEntity.noContent().build();
    }
}
```

### Service Layer

```java
// src/main/java/com/example/service/UserService.java

package com.example.service;

import com.example.dto.CreateUserRequest;
import com.example.dto.UpdateUserRequest;
import com.example.dto.UserResponse;
import com.example.entity.User;
import com.example.exception.ResourceNotFoundException;
import com.example.mapper.UserMapper;
import com.example.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;
    private final PasswordEncoder passwordEncoder;

    public Page<UserResponse> findAll(Pageable pageable) {
        return userRepository.findAll(pageable)
                .map(userMapper::toResponse);
    }

    public UserResponse findById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User", id));
        return userMapper.toResponse(user);
    }

    @Transactional
    public UserResponse create(CreateUserRequest request) {
        User user = userMapper.toEntity(request);
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user = userRepository.save(user);
        return userMapper.toResponse(user);
    }

    @Transactional
    public UserResponse update(Long id, UpdateUserRequest request) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User", id));
        userMapper.updateEntity(user, request);
        user = userRepository.save(user);
        return userMapper.toResponse(user);
    }

    @Transactional
    public void delete(Long id) {
        if (!userRepository.existsById(id)) {
            throw new ResourceNotFoundException("User", id);
        }
        userRepository.deleteById(id);
    }
}
```

---

## JPA/Hibernate Patterns

### Problem
Efficient database access with JPA.

### Framework: Entity Definition

```java
// src/main/java/com/example/entity/User.java

package com.example.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "users")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String password;

    @Column(name = "is_active")
    @Builder.Default
    private Boolean isActive = true;

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(
        name = "user_roles",
        joinColumns = @JoinColumn(name = "user_id"),
        inverseJoinColumns = @JoinColumn(name = "role_id")
    )
    @Builder.Default
    private Set<Role> roles = new HashSet<>();

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private Set<Order> orders = new HashSet<>();

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    // Helper methods
    public void addRole(Role role) {
        roles.add(role);
    }

    public void removeRole(Role role) {
        roles.remove(role);
    }
}
```

### Repository with Custom Queries

```java
// src/main/java/com/example/repository/UserRepository.java

package com.example.repository;

import com.example.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByEmail(String email);

    boolean existsByEmail(String email);

    @Query("SELECT u FROM User u WHERE u.isActive = true")
    Page<User> findAllActive(Pageable pageable);

    @Query("SELECT u FROM User u JOIN FETCH u.roles WHERE u.id = :id")
    Optional<User> findByIdWithRoles(@Param("id") Long id);

    @Query("""
        SELECT u FROM User u
        WHERE (:name IS NULL OR LOWER(u.name) LIKE LOWER(CONCAT('%', :name, '%')))
        AND (:email IS NULL OR LOWER(u.email) LIKE LOWER(CONCAT('%', :email, '%')))
        AND (:isActive IS NULL OR u.isActive = :isActive)
        """)
    Page<User> search(
            @Param("name") String name,
            @Param("email") String email,
            @Param("isActive") Boolean isActive,
            Pageable pageable
    );

    @Modifying
    @Query("UPDATE User u SET u.isActive = false WHERE u.lastLoginAt < :cutoffDate")
    int deactivateInactiveUsers(@Param("cutoffDate") LocalDateTime cutoffDate);
}
```

---

## JUnit Testing

### Problem
Write comprehensive tests for Spring Boot applications.

### Framework: Controller Tests

```java
// src/test/java/com/example/controller/UserControllerTest.java

package com.example.controller;

import com.example.dto.CreateUserRequest;
import com.example.dto.UserResponse;
import com.example.service.UserService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @MockBean
    private UserService userService;

    @Test
    void createUser_WithValidData_ReturnsCreated() throws Exception {
        CreateUserRequest request = new CreateUserRequest(
                "John Doe", "john@example.com", "password123"
        );
        UserResponse response = new UserResponse(1L, "John Doe", "john@example.com");

        when(userService.create(any(CreateUserRequest.class))).thenReturn(response);

        mockMvc.perform(post("/api/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("John Doe"))
                .andExpect(jsonPath("$.email").value("john@example.com"));
    }

    @Test
    void createUser_WithInvalidEmail_ReturnsBadRequest() throws Exception {
        CreateUserRequest request = new CreateUserRequest(
                "John Doe", "invalid-email", "password123"
        );

        mockMvc.perform(post("/api/v1/users")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.errors.email").exists());
    }

    @Test
    void getUser_WhenExists_ReturnsUser() throws Exception {
        UserResponse response = new UserResponse(1L, "John Doe", "john@example.com");
        when(userService.findById(1L)).thenReturn(response);

        mockMvc.perform(get("/api/v1/users/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.name").value("John Doe"));
    }
}
```

### Service Tests

```java
// src/test/java/com/example/service/UserServiceTest.java

package com.example.service;

import com.example.dto.CreateUserRequest;
import com.example.dto.UserResponse;
import com.example.entity.User;
import com.example.exception.ResourceNotFoundException;
import com.example.mapper.UserMapper;
import com.example.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private UserMapper userMapper;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private UserService userService;

    private User user;
    private UserResponse userResponse;

    @BeforeEach
    void setUp() {
        user = User.builder()
                .id(1L)
                .name("John Doe")
                .email("john@example.com")
                .password("encoded")
                .build();
        userResponse = new UserResponse(1L, "John Doe", "john@example.com");
    }

    @Test
    void findById_WhenUserExists_ReturnsUser() {
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
        when(userMapper.toResponse(user)).thenReturn(userResponse);

        UserResponse result = userService.findById(1L);

        assertThat(result.getId()).isEqualTo(1L);
        assertThat(result.getName()).isEqualTo("John Doe");
    }

    @Test
    void findById_WhenUserNotExists_ThrowsException() {
        when(userRepository.findById(999L)).thenReturn(Optional.empty());

        assertThatThrownBy(() -> userService.findById(999L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessageContaining("User");
    }

    @Test
    void create_EncodesPassword() {
        CreateUserRequest request = new CreateUserRequest(
                "John", "john@example.com", "plaintext"
        );
        when(passwordEncoder.encode("plaintext")).thenReturn("encoded");
        when(userMapper.toEntity(request)).thenReturn(user);
        when(userRepository.save(any(User.class))).thenReturn(user);
        when(userMapper.toResponse(user)).thenReturn(userResponse);

        userService.create(request);

        verify(passwordEncoder).encode("plaintext");
    }
}
```

---

## Spring Async

### Problem
Process background tasks asynchronously.

### Framework: Async Configuration

```java
// src/main/java/com/example/config/AsyncConfig.java

package com.example.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;

@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(4);
        executor.setMaxPoolSize(8);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("Async-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }

    @Bean(name = "emailExecutor")
    public Executor emailExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(2);
        executor.setMaxPoolSize(4);
        executor.setQueueCapacity(50);
        executor.setThreadNamePrefix("Email-");
        executor.initialize();
        return executor;
    }
}
```

### Async Service

```java
// src/main/java/com/example/service/NotificationService.java

package com.example.service;

import com.example.entity.Order;
import com.example.entity.User;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.util.concurrent.CompletableFuture;

@Service
@RequiredArgsConstructor
@Slf4j
public class NotificationService {

    private final EmailService emailService;
    private final SmsService smsService;

    @Async("emailExecutor")
    public CompletableFuture<Void> sendOrderConfirmation(Order order) {
        log.info("Sending order confirmation for order: {}", order.getId());
        try {
            emailService.send(
                    order.getUser().getEmail(),
                    "Order Confirmation",
                    buildOrderEmailBody(order)
            );
            return CompletableFuture.completedFuture(null);
        } catch (Exception e) {
            log.error("Failed to send order confirmation", e);
            return CompletableFuture.failedFuture(e);
        }
    }

    @Async("taskExecutor")
    public CompletableFuture<Void> sendWelcomeNotifications(User user) {
        CompletableFuture<Void> emailFuture = CompletableFuture.runAsync(() ->
                emailService.send(user.getEmail(), "Welcome!", buildWelcomeEmail(user))
        );

        CompletableFuture<Void> smsFuture = CompletableFuture.runAsync(() ->
                smsService.send(user.getPhone(), "Welcome to our service!")
        );

        return CompletableFuture.allOf(emailFuture, smsFuture)
                .exceptionally(ex -> {
                    log.error("Failed to send welcome notifications", ex);
                    return null;
                });
    }

    private String buildOrderEmailBody(Order order) {
        return "Your order #" + order.getId() + " has been confirmed.";
    }

    private String buildWelcomeEmail(User user) {
        return "Welcome, " + user.getName() + "!";
    }
}
```

---

## Sources

- [Spring Boot Reference](https://docs.spring.io/spring-boot/docs/current/reference/html/)
- [Spring Data JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
