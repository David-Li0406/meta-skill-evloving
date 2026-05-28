# Data Layer Best Practices

This reference covers Spring Data JPA, repository patterns, transaction management, and database operations in Spring Boot.

## Spring Data JPA Setup

### Dependency

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>

<dependency>
    <groupId>org.postgresql</groupId>
    <artifactId>postgresql</artifactId>
    <scope>runtime</scope>
</dependency>
```

### Configuration

```yaml
# application.yml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: ${DB_USERNAME:user}
    password: ${DB_PASSWORD:pass}
    driver-class-name: org.postgresql.Driver
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000

  jpa:
    hibernate:
      ddl-auto: validate  # Never use update in production
    show-sql: false
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
        format_sql: true
        use_sql_comments: true
        jdbc:
          batch_size: 20
          order_inserts: true
          order_updates: true
```

## Entity Design

### Basic Entity

```java
@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 100)
    private String email;

    @Column(nullable = false)
    private String password;

    @Column(name = "first_name")
    private String firstName;

    @Column(name = "last_name")
    private String lastName;

    @Column(name = "created_at", updatable = false)
    @CreationTimestamp
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    @UpdateTimestamp
    private LocalDateTime updatedAt;

    @Version
    private Integer version;  // Optimistic locking

    // Constructors, getters, setters
}
```

### Entity Relationships

**One-to-Many:**

```java
@Entity
public class User {
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Order> orders = new ArrayList<>();
}

@Entity
public class Order {
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
}
```

**Many-to-Many:**

```java
@Entity
public class User {
    @ManyToMany(mappedBy = "students")
    private List<Course> courses = new ArrayList<>();
}

@Entity
public class Course {
    @ManyToMany(cascade = {CascadeType.PERSIST, CascadeType.MERGE})
    @JoinTable(
        name = "course_student",
        joinColumns = @JoinColumn(name = "course_id"),
        inverseJoinColumns = @JoinColumn(name = "student_id")
    )
    private List<User> students = new ArrayList<>();
}
```

**Best practices for relationships:**
- Use `FetchType.LAZY` for to-many relationships
- Use `mappedBy` for bidirectional relationships
- Avoid cascade operations unless necessary
- Use `@JoinColumn` for foreign key columns
- Implement `equals()` and `hashCode()` carefully for entities

## Repository Pattern

### Basic Repository

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    // Query methods
    Optional<User> findByEmail(String email);

    List<User> findByFirstNameAndLastName(String firstName, String lastName);

    List<User> findByCreatedAtAfter(LocalDateTime date);

    // Existence check
    boolean existsByEmail(String email);

    // Count
    long countByRole(Role role);

    // Delete
    void deleteByEmail(String email);

    // Pagination
    Page<User> findByRole(Role role, Pageable pageable);
}
```

### Custom Queries with @Query

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    @Query("SELECT u FROM User u WHERE u.email = :email")
    Optional<User> findByEmailCustom(@Param("email") String email);

    @Query("SELECT new com.example.dto.UserDTO(u.id, u.email, u.firstName) FROM User u")
    List<UserDTO> findAllAsDTO();

    @Query(value = "SELECT * FROM users WHERE email = :email", nativeQuery = true)
    Optional<User> findByEmailNative(@Param("email") String email);

    @Query("SELECT u FROM User u JOIN FETCH u.orders WHERE u.id = :id")
    Optional<User> findByIdWithOrders(@Param("id") Long id);

    @Modifying
    @Query("UPDATE User u SET u.lastName = :lastName WHERE u.id = :id")
    int updateLastName(@Param("id") Long id, @Param("lastName") String lastName);
}
```

### EntityGraph for N+1 Problem

**Problem: N+1 queries**

```java
// Without EntityGraph - generates N+1 queries
List<User> users = userRepository.findAll();
for (User user : users) {
    user.getOrders().size();  // Additional query for each user
}
```

**Solution: @EntityGraph**

```java
@Entity(attributeOverrides = {
    @AttributeOverride(name = "email", column = @Column(name = "email"))
})
@NamedEntityGraph(
    name = "User.withOrders",
    attributeNodes = @NamedAttributeNode("orders")
)
public class User {
    @OneToMany(mappedBy = "user")
    private List<Order> orders;
}

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    @EntityGraph(attributePaths = {"orders"})
    List<User> findAllWithOrders();

    @EntityGraph(attributePaths = {"orders", "orders.products"})
    List<User> findAllWithOrdersAndProducts();
}
```

### Custom Repository Implementation

**Custom interface:**

```java
public interface UserRepositoryCustom {
    List<User> findUsersWithComplexCriteria(String email, String name, LocalDate date);
}
```

**Implementation:**

```java
@Repository
public class UserRepositoryImpl implements UserRepositoryCustom {

    @PersistenceContext
    private EntityManager entityManager;

    @Override
    public List<User> findUsersWithComplexCriteria(String email, String name, LocalDate date) {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<User> query = cb.createQuery(User.class);
        Root<User> user = query.from(User.class);

        List<Predicate> predicates = new ArrayList<>();

        if (email != null) {
            predicates.add(cb.equal(user.get("email"), email));
        }

        if (name != null) {
            predicates.add(cb.like(user.get("firstName"), "%" + name + "%"));
        }

        if (date != null) {
            predicates.add(cb.greaterThanOrEqualTo(user.get("createdAt"), date));
        }

        query.where(cb.and(predicates.toArray(new Predicate[0])));

        return entityManager.createQuery(query).getResultList();
    }
}
```

**Use in repository:**

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long>, UserRepositoryCustom {
    // Inherits findUsersWithComplexCriteria
}
```

## Transaction Management

### @Transactional Annotation

```java
@Service
public class UserService {

    @Transactional  // Default: REQUIRED
    public void createUserWithOrders(CreateUserRequest request) {
        // All database operations in this method are in a single transaction
        User user = new User();
        user.setEmail(request.getEmail());
        userRepository.save(user);

        for (CreateOrderRequest orderReq : request.getOrders()) {
            Order order = new Order();
            order.setUser(user);
            orderRepository.save(order);
        }
        // If any exception occurs, entire transaction rolls back
    }

    @Transactional(
        propagation = Propagation.REQUIRES_NEW,
        isolation = Isolation.READ_COMMITTED,
        timeout = 30,
        readOnly = false,
        rollbackFor = Exception.class,
        noRollbackFor = BusinessException.class
    )
    public void methodWithCustomTransactionSettings() {
        // Custom transaction settings
    }
}
```

### Transaction Propagation

- **REQUIRED** (default): Join existing transaction or create new
- **REQUIRES_NEW**: Always create new transaction, suspend existing
- **SUPPORTS**: Use existing transaction, execute without transaction if none exists
- **NOT_SUPPORTED**: Execute without transaction, suspend existing
- **MANDATORY**: Must have existing transaction, throw exception if none
- **NEVER**: Must not have transaction, throw exception if one exists
- **NESTED**: Execute within nested transaction

### Transaction Best Practices

```java
// ✅ GOOD - Transaction at service layer
@Service
public class OrderService {

    @Transactional
    public Order createOrder(CreateOrderRequest request) {
        // Business logic and database operations
        Order order = new Order();
        orderRepository.save(order);

        inventoryService.updateStock(order);

        return order;
    }
}

// ❌ BAD - Transaction at controller layer
@RestController
public class OrderController {

    @Transactional
    @PostMapping("/orders")
    public Order createOrder(@RequestBody CreateOrderRequest request) {
        // Don't use transactions in controllers
    }
}
```

## DTO Projections

### Interface Projections

```java
public interface UserNameOnly {
    Long getId();
    String getEmail();
    String getFirstName();
}

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    List<UserNameOnly> findByRole(Role role);
}
```

### Class Projections

```java
public class UserSummary {
    private final Long id;
    private final String email;
    private final String fullName;

    public UserSummary(Long id, String email, String fullName) {
        this.id = id;
        this.email = email;
        this.fullName = fullName;
    }

    // Getters
}

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    @Query("SELECT new com.example.dto.UserSummary(u.id, u.email, CONCAT(u.firstName, ' ', u.lastName)) FROM User u")
    List<UserSummary> findAllSummaries();
}
```

### Dynamic Projections

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    <T> List<T> findByRole(Role role, Class<T> type);
}

// Usage
List<UserNameOnly> users = userRepository.findByRole(Role.USER, UserNameOnly.class);
```

## Pagination and Sorting

### Basic Pagination

```java
@RestController
public class UserController {

    @GetMapping("/users")
    public Page<UserDTO> getUsers(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "10") int size,
        @RequestParam(defaultValue = "id") String sortBy
    ) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(sortBy));
        return userService.findAll(pageable);
    }
}
```

### Advanced Sorting

```java
// Sort by multiple fields
Pageable pageable = PageRequest.of(0, 10, Sort.by(
    Sort.Order.desc("createdAt"),
    Sort.Order.asc("email")
));

// Case-insensitive sorting
Pageable pageable = PageRequest.of(0, 10,
    Sort.by("lastName").ignoreCase()
);
```

### Pagination with Specification

```java
public class UserSpecification {

    public static Specification<User> hasEmail(String email) {
        return (root, query, cb) ->
            email == null ? null : cb.equal(root.get("email"), email);
    }

    public static Specification<User> hasName(String name) {
        return (root, query, cb) ->
            name == null ? null : cb.like(root.get("firstName"), "%" + name + "%");
    }

    public static Specification<User> createdAfter(LocalDate date) {
        return (root, query, cb) ->
            date == null ? null : cb.greaterThanOrEqualTo(root.get("createdAt"), date);
    }
}

// Usage
Specification<User> spec = Specification.where(null)
    .and(UserSpecification.hasEmail("test@example.com"))
    .and(UserSpecification.hasName("John"))
    .and(UserSpecification.createdAfter(LocalDate.now()));

Page<User> users = userRepository.findAll(spec, PageRequest.of(0, 10));
```

## Auditing

### Enable Auditing

```java
@Configuration
@EnableJpaAuditing(auditorAwareRef = "auditorProvider")
public class JpaConfig {

    @Bean
    public AuditorAware<String> auditorProvider() {
        return () -> {
            Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
            if (authentication == null || !authentication.isAuthenticated()) {
                return Optional.empty();
            }
            return Optional.of(authentication.getName());
        };
    }
}
```

### Add Auditing Fields

```java
@Entity
@EntityListeners(AuditingEntityListener.class)
public class User {

    @CreatedDate
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @CreatedBy
    @Column(name = "created_by", updatable = false)
    private String createdBy;

    @LastModifiedBy
    @Column(name = "updated_by")
    private String updatedBy;
}
```

## Database Migrations

### Flyway

```xml
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
</dependency>
```

```yaml
spring:
  flyway:
    enabled: true
    locations: classpath:db/migration
    baseline-on-migrate: true
```

**Migration files:**

```sql
-- V1__Create_users_table.sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    version INT DEFAULT 0
);

-- V2__Add_roles_table.sql
CREATE TABLE roles (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);
```

### Liquibase

```xml
<dependency>
    <groupId>org.liquibase</groupId>
    <artifactId>liquibase-core</artifactId>
</dependency>
```

## Best Practices

1. **Always use transactions in service layer, not controllers**
2. **Use FetchType.LAZY for relationships**
3. **Solve N+1 problems with @EntityGraph or JOIN FETCH**
4. **Never expose entities to API - use DTOs**
5. **Use pagination for large datasets**
6. **Use optimistic locking with @Version**
7. **Implement proper equals() and hashCode() for entities**
8. **Use database migrations (Flyway/Liquibase)**
9. **Configure connection pooling (HikariCP)**
10. **Use DTO projections for read-only queries**

## Summary Checklist

- [ ] Configure JPA with proper dialect and connection pool
- [ ] Use FetchType.LAZY for relationships
- [ ] Implement repositories with Spring Data JPA
- [ ] Use @EntityGraph to solve N+1 queries
- [ ] Add @Transactional at service layer
- [ ] Use DTOs for API responses
- [ ] Implement pagination for large datasets
- [ ] Add auditing with @EnableJpaAuditing
- [ ] Configure database migrations
- [ ] Use connection pooling

## Resources

- [Spring Data JPA Documentation](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [Baeldung - Spring Data JPA](https://www.baeldung.com/tag/spring-data-jpa)
- [Hibernate Best Practices](https://thorben-janssen.com/best-practices/)
