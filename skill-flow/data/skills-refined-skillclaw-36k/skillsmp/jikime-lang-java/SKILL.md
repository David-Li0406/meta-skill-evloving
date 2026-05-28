---
name: jikime-lang-java
description: Java 21 LTS development specialist covering Spring Boot 3.3, virtual threads, pattern matching, and enterprise patterns. Use when building enterprise applications, microservices, or Spring projects.
version: 1.0.0
tags: ["language", "java", "spring-boot", "jpa", "hibernate", "virtual-threads", "enterprise"]
triggers:
  keywords: ["java", "spring", "spring-boot", "jpa", "hibernate", "maven", "gradle", "자바"]
  phases: ["run"]
  agents: ["backend"]
  languages: ["java"]
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2000
user-invocable: false
---

# Java Development Guide

Java 21 LTS / Spring Boot 3.3 개발을 위한 간결한 가이드.

## Quick Reference

| 용도 | 도구 | 특징 |
|------|------|------|
| Framework | **Spring Boot 3.3** | 자동 설정, 임베디드 서버 |
| ORM | **Spring Data JPA** | 리포지토리 패턴 |
| Build | **Maven/Gradle** | 의존성 관리 |
| Testing | **JUnit 5** | 모던 테스팅 |

## Project Setup

```bash
# Spring Initializr
curl https://start.spring.io/starter.zip \
  -d dependencies=web,data-jpa,postgresql \
  -d javaVersion=21 \
  -d type=maven-project \
  -o project.zip
```

## Spring Boot Patterns

### REST Controller

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {
    private final UserService userService;

    @GetMapping
    public List<UserResponse> list() {
        return userService.findAll();
    }

    @GetMapping("/{id}")
    public UserResponse get(@PathVariable Long id) {
        return userService.findById(id)
            .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserResponse create(@Valid @RequestBody UserRequest request) {
        return userService.create(request);
    }
}
```

### Service Layer

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserService {
    private final UserRepository userRepository;

    public List<UserResponse> findAll() {
        return userRepository.findAll().stream()
            .map(UserResponse::from)
            .toList();
    }

    public Optional<UserResponse> findById(Long id) {
        return userRepository.findById(id)
            .map(UserResponse::from);
    }

    @Transactional
    public UserResponse create(UserRequest request) {
        User user = User.builder()
            .name(request.name())
            .email(request.email())
            .build();
        return UserResponse.from(userRepository.save(user));
    }
}
```

### JPA Entity

```java
@Entity
@Table(name = "users")
@Getter @NoArgsConstructor(access = AccessLevel.PROTECTED)
public class User {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @OneToMany(mappedBy = "author", cascade = CascadeType.ALL)
    private List<Post> posts = new ArrayList<>();

    @Builder
    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }
}
```

### Repository

```java
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);

    @Query("SELECT u FROM User u WHERE u.name LIKE %:name%")
    List<User> searchByName(@Param("name") String name);
}
```

## Java 21 Features

### Record

```java
public record UserRequest(
    @NotBlank String name,
    @Email String email
) {}

public record UserResponse(
    Long id,
    String name,
    String email
) {
    public static UserResponse from(User user) {
        return new UserResponse(user.getId(), user.getName(), user.getEmail());
    }
}
```

### Virtual Threads

```java
@Bean
public TomcatProtocolHandlerCustomizer<?> protocolHandlerVirtualThreadExecutorCustomizer() {
    return protocolHandler -> {
        protocolHandler.setExecutor(Executors.newVirtualThreadPerTaskExecutor());
    };
}

// 또는 application.yml
spring:
  threads:
    virtual:
      enabled: true
```

### Pattern Matching

```java
// Switch expression
String result = switch (status) {
    case PENDING -> "Processing";
    case APPROVED -> "Approved";
    case REJECTED -> "Rejected";
};

// Pattern matching for instanceof
if (obj instanceof User user) {
    System.out.println(user.getName());
}
```

## Testing

```java
@SpringBootTest
@AutoConfigureMockMvc
class UserControllerTest {
    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void shouldReturnUser() throws Exception {
        var user = new UserResponse(1L, "John", "john@example.com");
        when(userService.findById(1L)).thenReturn(Optional.of(user));

        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("John"));
    }

    @Test
    void shouldCreateUser() throws Exception {
        var request = new UserRequest("John", "john@example.com");
        var response = new UserResponse(1L, "John", "john@example.com");
        when(userService.create(any())).thenReturn(response);

        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {"name": "John", "email": "john@example.com"}
                    """))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(1));
    }
}
```

## Project Structure

```
src/main/java/com/example/
├── Application.java
├── config/
├── controller/
├── service/
├── repository/
├── entity/
└── dto/
src/test/java/com/example/
└── controller/
```

## Best Practices

- **Record**: DTO에 Record 사용
- **Constructor Injection**: @RequiredArgsConstructor 사용
- **Validation**: @Valid와 Bean Validation
- **Exception Handling**: @ControllerAdvice 사용
- **Virtual Threads**: I/O 바운드 작업에 활용

---

Last Updated: 2026-01-21
Version: 2.0.0
