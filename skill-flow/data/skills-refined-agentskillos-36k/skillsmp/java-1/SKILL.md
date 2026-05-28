---
name: java
description: "Java development process and modern practices review. Use when writing Java code, reviewing Java PRs, working with Spring Boot applications, implementing design patterns, or setting up project structure. Also use when code uses mutable state everywhere, null checks are scattered, Optional is misused, field injection is used, or old Java patterns persist. Essential for records, sealed classes, pattern matching, JUnit 5, Mockito, and modern Java (17+) features."
---

# Java Skill

## Overview

Modern Java is expressive and powerful. This skill guides writing clean, maintainable Java that leverages modern language features and frameworks properly.

**Core principle:** Favor immutability and composition. Modern Java (17+) provides the tools—records, sealed classes, pattern matching—use them.

## The Java Development Process

### Phase 1: Choose Modern Patterns

**Before writing implementation:**

1. **Use Records for Data**
   - Immutable data classes
   - Built-in equals, hashCode, toString
   - No boilerplate

2. **Handle Absence with Optional**
   - Return type only, not parameters
   - Chain operations, don't check `.isPresent()`

3. **Design for Immutability**
   - Final fields by default
   - Defensive copies for collections
   - Builder pattern for complex objects

### Phase 2: Implement Cleanly

**Write modern Java:**

1. **Use Records for DTOs**
   ```java
   // ✅ Modern: Record
   public record User(String name, String email, int age) {}

   // ❌ Legacy: Mutable POJO
   public class User {
       private String name;
       private String email;
       // getters, setters, equals, hashCode, toString...
   }
   ```

2. **Chain Optional Operations**
   ```java
   // ✅ Functional style
   String email = findUser(id)
       .map(User::email)
       .orElse("unknown@example.com");

   // ❌ Imperative style
   Optional<User> user = findUser(id);
   String email;
   if (user.isPresent()) {
       email = user.get().email();
   } else {
       email = "unknown@example.com";
   }
   ```

3. **Use Pattern Matching**
   ```java
   // ✅ Switch expressions
   String result = switch (status) {
       case ACTIVE -> "Active";
       case PENDING -> "Pending";
       case INACTIVE -> "Inactive";
   };

   // ✅ Pattern matching for instanceof
   if (shape instanceof Circle c) {
       return Math.PI * c.radius() * c.radius();
   }
   ```

### Phase 3: Review for Quality

**Before approving:**

1. **Check Immutability**
   - Records used for data?
   - Collections defensively copied?
   - No unnecessary mutability?

2. **Check Null Safety**
   - Optional used appropriately?
   - No null returns from methods?
   - Null checks at boundaries only?

3. **Check Spring Patterns**
   - Constructor injection used?
   - Transactions at service layer?
   - No business logic in controllers?

## Red Flags - STOP and Fix

### Optional Red Flags

```java
// Optional.get() without check
String name = optional.get();  // NoSuchElementException!

// Optional as parameter
void process(Optional<String> name) {  // Just use @Nullable

// Optional of nullable
Optional.of(nullableValue);  // NullPointerException!

// isPresent() + get() pattern
if (opt.isPresent()) {
    return opt.get();  // Use orElse, map, etc.
}
```

### Dependency Injection Red Flags

```java
// Field injection
@Autowired
private UserRepository userRepository;  // Hard to test!

// Circular dependencies
@Service class A { @Autowired B b; }
@Service class B { @Autowired A a; }  // Design problem

// @Autowired on setter
@Autowired
public void setRepository(Repo repo) {}  // Use constructor
```

### Design Red Flags

```java
// Mutable state in services
@Service
public class UserService {
    private List<User> cache = new ArrayList<>();  // Shared mutable state!
}

// Null return values
public User findById(Long id) {
    return repo.findById(id).orElse(null);  // Return Optional instead
}

// Checked exceptions for flow control
try {
    return findUser(id);
} catch (UserNotFoundException e) {
    return createUser(id);  // Use Optional
}
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "Optional is overhead" | JVM optimizes it. Correctness > micro-optimization. |
| "Records are too limited" | That's the point. Use classes when you need mutability. |
| "Field injection is cleaner" | It's untestable. Use constructor injection. |
| "We need setters for frameworks" | Modern frameworks work with immutables. Update them. |
| "Null is fine with documentation" | Documentation doesn't prevent NPEs. Use types. |
| "It's just internal code" | Internal code becomes public API. Write it right. |

## Java Quality Checklist

Before approving Java code:

- [ ] **Modern features**: Records, pattern matching, switch expressions
- [ ] **Immutability**: Final fields, defensive copies
- [ ] **Optional correct**: No `.get()`, no parameters, chained operations
- [ ] **Constructor injection**: No `@Autowired` on fields
- [ ] **No nulls**: Optional returns, validated inputs
- [ ] **Tests present**: Unit and integration tests
- [ ] **Linting clean**: SpotBugs, Checkstyle pass

## Quick Patterns

### Service Layer

```java
@Service
@RequiredArgsConstructor  // Lombok generates constructor
public class UserService {

    private final UserRepository userRepository;
    private final EventPublisher eventPublisher;

    @Transactional(readOnly = true)
    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }

    @Transactional
    public User create(CreateUserRequest request) {
        User user = User.builder()
            .name(request.name())
            .email(request.email())
            .build();

        User saved = userRepository.save(user);
        eventPublisher.publish(new UserCreatedEvent(saved));
        return saved;
    }
}
```

### Controller Layer

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public User createUser(@Valid @RequestBody CreateUserRequest request) {
        return userService.create(request);
    }
}
```

### Exception Handling

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleNotFound(ResourceNotFoundException ex) {
        return new ErrorResponse(ex.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse handleValidation(MethodArgumentNotValidException ex) {
        List<String> errors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .map(e -> e.getField() + ": " + e.getDefaultMessage())
            .toList();
        return new ErrorResponse("Validation failed", errors);
    }
}
```

## Quick Commands

```bash
# Build
mvn clean install
./gradlew build

# Test
mvn test
./gradlew test

# Static analysis
mvn spotbugs:check
mvn checkstyle:check

# Coverage report
mvn jacoco:report

# Run application
mvn spring-boot:run
./gradlew bootRun
```

## References

Detailed patterns and examples in `references/`:
- `modern-java.md` - Java 17+ features
- `spring-patterns.md` - Spring Boot best practices
- `testing-patterns.md` - JUnit 5 and Mockito patterns
