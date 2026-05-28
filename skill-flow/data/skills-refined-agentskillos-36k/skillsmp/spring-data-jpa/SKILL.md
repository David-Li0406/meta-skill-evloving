---
name: Spring Data JPA
description: Entity mapping, repositories, transactions, queries, auditing, and fetching strategies.
metadata:
  labels: [java, spring-boot, jpa, database, hibernate]
  triggers:
    files: ['**/*Entity.java', '**/*Repository.java', '**/*Jpa*.java']
    keywords: [Entity, Id, Repository, JpaRepository, Transactional, Query, ManyToOne, OneToMany, ManyToMany, JoinColumn]
---

# Spring Data JPA Standards

## Entity Definition

```java
@Entity
@Table(name = "users")
@Getter @Setter
@NoArgsConstructor
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String passwordHash;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private UserStatus status = UserStatus.ACTIVE;

    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Order> orders = new ArrayList<>();

    @CreatedDate
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;

    // Business methods
    public void addOrder(Order order) {
        orders.add(order);
        order.setUser(this);
    }

    public void removeOrder(Order order) {
        orders.remove(order);
        order.setUser(null);
    }
}
```

## Repository

```java
public interface UserRepository extends JpaRepository<User, Long> {

    // Derived query methods
    Optional<User> findByEmail(String email);

    List<User> findByStatus(UserStatus status);

    boolean existsByEmail(String email);

    // JPQL query
    @Query("SELECT u FROM User u WHERE u.status = :status AND u.createdAt > :since")
    List<User> findActiveUsersSince(
        @Param("status") UserStatus status,
        @Param("since") LocalDateTime since
    );

    // Native query
    @Query(value = "SELECT * FROM users WHERE email LIKE %:domain", nativeQuery = true)
    List<User> findByEmailDomain(@Param("domain") String domain);

    // Modifying query
    @Modifying
    @Query("UPDATE User u SET u.status = :status WHERE u.id = :id")
    int updateStatus(@Param("id") Long id, @Param("status") UserStatus status);

    // Projection
    @Query("SELECT u.id as id, u.name as name, u.email as email FROM User u")
    List<UserSummary> findAllSummaries();

    // Pagination
    Page<User> findByStatus(UserStatus status, Pageable pageable);

    // Specification (dynamic queries)
    List<User> findAll(Specification<User> spec);
}

// Projection interface
public interface UserSummary {
    Long getId();
    String getName();
    String getEmail();
}
```

## Transactions

```java
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final InventoryService inventoryService;

    @Transactional
    public Order createOrder(CreateOrderRequest request) {
        Order order = new Order();
        // ... setup order

        for (OrderItem item : request.items()) {
            inventoryService.decreaseStock(item.productId(), item.quantity());
        }

        return orderRepository.save(order);
    }

    @Transactional(readOnly = true)
    public Order findById(Long id) {
        return orderRepository.findById(id)
            .orElseThrow(() -> new OrderNotFoundException(id));
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void processPayment(Long orderId) {
        // Runs in new transaction
    }

    @Transactional(
        isolation = Isolation.SERIALIZABLE,
        timeout = 30,
        rollbackFor = PaymentException.class,
        noRollbackFor = NotificationException.class
    )
    public void processWithOptions(Long orderId) {
        // Custom transaction settings
    }
}
```

## Relationships

```java
// Many-to-One (owning side)
@Entity
public class Order {
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
}

// One-to-Many (inverse side)
@Entity
public class User {
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Order> orders = new ArrayList<>();
}

// Many-to-Many
@Entity
public class Student {
    @ManyToMany
    @JoinTable(
        name = "student_courses",
        joinColumns = @JoinColumn(name = "student_id"),
        inverseJoinColumns = @JoinColumn(name = "course_id")
    )
    private Set<Course> courses = new HashSet<>();
}

// One-to-One
@Entity
public class User {
    @OneToOne(mappedBy = "user", cascade = CascadeType.ALL, orphanRemoval = true)
    private UserProfile profile;
}
```

## Auditing

```java
@Configuration
@EnableJpaAuditing
public class JpaConfig {}

@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseEntity {

    @CreatedDate
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @LastModifiedDate
    private LocalDateTime updatedAt;

    @CreatedBy
    @Column(updatable = false)
    private String createdBy;

    @LastModifiedBy
    private String updatedBy;
}

@Component
public class AuditorAwareImpl implements AuditorAware<String> {
    @Override
    public Optional<String> getCurrentAuditor() {
        return Optional.ofNullable(SecurityContextHolder.getContext().getAuthentication())
            .map(Authentication::getName);
    }
}
```

## Best Practices

1. **Use @ManyToOne with LAZY** - avoid N+1 queries
2. **Fetch eagerly with JOIN FETCH** when needed
3. **Use @Transactional(readOnly = true)** for read operations
4. **Avoid @ManyToMany** - use explicit join table entity
5. **Use projections** for read-only queries
6. **Paginate large result sets**

## References

- [Entity Mapping](references/entity-mapping.md) - Inheritance, embeddables, converters
- [Repository Patterns](references/repository-patterns.md) - Specifications, custom repos
- [Fetching Strategies](references/fetching-strategies.md) - N+1, EntityGraph, batch
