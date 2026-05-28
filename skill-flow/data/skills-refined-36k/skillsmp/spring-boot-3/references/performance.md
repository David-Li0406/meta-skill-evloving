# Performance Optimization Best Practices

This reference covers caching strategies, database optimization, async processing, and performance tuning for Spring Boot applications.

## Caching

### Enable Caching

**Dependency:**

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-cache</artifactId>
</dependency>

<dependency>
    <groupId>com.github.ben-manes.caffeine</groupId>
    <artifactId>caffeine</artifactId>
</dependency>
```

**Configuration:**

```java
@Configuration
@EnableCaching
public class CacheConfig {

    @Bean
    public CacheManager cacheManager() {
        CaffeineCacheManager cacheManager = new CaffeineCacheManager();
        cacheManager.setCaffeine(Caffeine.newBuilder()
            .maximumSize(1000)
            .expireAfterWrite(10, TimeUnit.MINUTES)
            .recordStats());
        return cacheManager;
    }
}
```

### Using Cache Annotations

```java
@Service
public class UserService {

    @Cacheable(value = "users", key = "#id")
    public UserDTO findById(Long id) {
        // Result cached automatically
        return userRepository.findById(id)
            .map(UserMapper::toDTO)
            .orElseThrow(() -> new ResourceNotFoundException("User not found"));
    }

    @Cacheable(value = "users", key = "#email")
    public UserDTO findByEmail(String email) {
        // Cached by email
    }

    @CacheEvict(value = "users", key = "#id")
    public void deleteUser(Long id) {
        // Cache cleared on delete
        userRepository.deleteById(id);
    }

    @CachePut(value = "users", key = "#result.id")
    public UserDTO updateUser(Long id, UpdateUserRequest request) {
        // Cache updated with new value
        User user = userRepository.findById(id).orElseThrow();
        user.setEmail(request.getEmail());
        return UserMapper.toDTO(userRepository.save(user));
    }

    @CacheEvict(value = "users", allEntries = true)
    public void clearAllCache() {
        // Clear all users cache
    }

    @Caching(evict = {
        @CacheEvict(value = "users", key = "#id"),
        @CacheEvict(value = "user-orders", key = "#id")
    })
    public void deleteUserWithOrders(Long id) {
        // Evict from multiple caches
    }
}
```

### Cache Configuration

```yaml
spring:
  cache:
    type: caffeine
    caffeine:
      spec: maximumSize=1000,expireAfterWrite=10m
    cache-names: users,products,orders
```

### Multi-Level Caching

```java
@Service
public class ProductService {

    @Cacheable(value = "products", key = "#id")
    public ProductDTO findById(Long id) {
        return productRepository.findById(id)
            .map(ProductMapper::toDTO)
            .orElse(null);
    }
}
```

## Database Performance

### Connection Pooling (HikariCP)

HikariCP is the default connection pool in Spring Boot:

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
      pool-name: MyAppHikariPool
      connection-test-query: SELECT 1
      leak-detection-threshold: 60000
```

**Optimal pool size formula:**
```
pool_size = (core_count * 2) + effective_spindle_count
```

For database: `pool_size = core_count * 2`

### Solve N+1 Query Problem

**Problem:**

```java
// Without optimization - N+1 queries
List<Order> orders = orderRepository.findAll();
for (Order order : orders) {
    order.getProducts().size();  // Additional query for each order
}
```

**Solution 1: EntityGraph**

```java
@Entity
@NamedEntityGraph(
    name = "Order.withProducts",
    attributeNodes = @NamedAttributeNode("products")
)
public class Order {
    @OneToMany(fetch = FetchType.LAZY)
    private List<Product> products;
}

@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    @EntityGraph(attributePaths = {"products"})
    List<Order> findAll();
}
```

**Solution 2: JOIN FETCH**

```java
@Query("SELECT o FROM Order o JOIN FETCH o.products")
List<Order> findAllWithProducts();
```

**Solution 3: @BatchSize**

```java
@Entity
public class Order {
    @OneToMany(fetch = FetchType.LAZY)
    @BatchSize(size = 50)
    private List<Product> products;
}
```

### Batch Operations

**Enable JDBC batching:**

```yaml
spring:
  jpa:
    properties:
      hibernate:
        jdbc:
          batch_size: 50
          order_inserts: true
          order_updates: true
```

**Batch insert:**

```java
@Service
public class DataImportService {

    @Transactional
    public void importUsers(List<UserDTO> userDTOs) {
        List<User> users = userDTOs.stream()
            .map(UserMapper::toEntity)
            .collect(Collectors.toList());

        userRepository.saveAll(users);  // Batches automatically
        userRepository.flush();  // Flush batch
    }
}
```

### DTO Projections for Read-Only

```java
// Instead of fetching full entities
public interface UserNameOnly {
    Long getId();
    String getName();
}

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    List<UserNameOnly> findByActiveTrue();
}
```

### Database Indexing

```java
@Entity
@Table(name = "users", indexes = {
    @Index(name = "idx_user_email", columnList = "email"),
    @Index(name = "idx_user_name", columnList = "last_name, first_name"),
    @Index(name = "idx_user_created", columnList = "created_at")
})
public class User {
    @Column(nullable = false, unique = true)
    private String email;

    @Column(name = "created_at")
    private LocalDateTime createdAt;
}
```

## Async Processing

### Enable Async

```java
@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {

    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
}
```

### Async Methods

```java
@Service
public class EmailService {

    @Async
    public void sendEmail(String to, String subject, String body) {
        // Runs asynchronously in separate thread
        emailClient.send(to, subject, body);
    }

    @Async
    public CompletableFuture<Boolean> sendEmailAsync(String to, String subject) {
        // Returns CompletableFuture
        emailClient.send(to, subject, "");
        return CompletableFuture.completedFuture(true);
    }
}
```

**Usage:**

```java
@RestController
public class UserController {

    @Autowired
    private EmailService emailService;

    @PostMapping("/users")
    public ResponseEntity<UserDTO> create(@RequestBody CreateUserRequest request) {
        UserDTO created = userService.create(request);

        // Email sent asynchronously, doesn't block response
        emailService.sendEmail(request.getEmail(), "Welcome", "...");

        return ResponseEntity.ok(created);
    }
}
```

### Async with Return Value

```java
@Service
public class ReportService {

    @Async
    public CompletableFuture<ReportDTO> generateReport(Long userId) {
        ReportDTO report = reportGenerator.generate(userId);
        return CompletableFuture.completedFuture(report);
    }
}
```

**Usage:**

```java
@RestController
public class ReportController {

    @GetMapping("/reports/{id}")
    public CompletableFuture<ReportDTO> getReport(@PathVariable Long id) {
        // Spring MVC handles CompletableFuture automatically
        return reportService.generateReport(id);
    }
}
```

## Spring Boot Actuator for Monitoring

### Enable Actuator

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

### Configure Endpoints

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
      base-path: /actuator
  endpoint:
    health:
      show-details: always
      probes:
        enabled: true
  metrics:
    export:
      prometheus:
        enabled: true
```

### Key Endpoints

- `/actuator/health` - Application health
- `/actuator/metrics` - Application metrics
- `/actuator/info` - Application information
- `/actuator/prometheus` - Prometheus metrics
- `/actuator/threaddump` - Thread dump
- `/actuator/heapdump` - Heap dump

### Custom Health Indicators

```java
@Component
public class DatabaseHealthIndicator implements HealthIndicator {

    @Autowired
    private DataSource dataSource;

    @Override
    public Health health() {
        try (Connection connection = dataSource.getConnection()) {
            if (connection.isValid(1)) {
                return Health.up()
                    .withDetail("database", "PostgreSQL")
                    .build();
            }
        } catch (SQLException e) {
            return Health.down()
                .withDetail("error", e.getMessage())
                .build();
        }
    }
}
```

### Custom Metrics

```java
@Component
public class UserMetrics {

    private final MeterRegistry meterRegistry;
    private final Counter userCreatedCounter;

    public UserMetrics(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.userCreatedCounter = Counter.builder("users.created")
            .description("Number of users created")
            .register(meterRegistry);
    }

    public void incrementUserCreated() {
        userCreatedCounter.increment();
    }
}
```

## Lazy Initialization

### Enable Lazy Initialization

**Spring Boot 2.2+:**

```yaml
spring:
  main:
    lazy-initialization: true
```

**Or programmatically:**

```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplicationBuilder builder = new SpringApplicationBuilder(Application.class);
        builder.lazyInitialization(true);
        builder.run(args);
    }
}
```

**Benefits:**
- Faster startup time
- Reduced memory footprint
- Beans created only when needed

**Caution:** Can hide configuration errors

## JVM Tuning

### JVM Options for Production

```bash
java -jar app.jar \
  -Xms512m \
  -Xmx2g \
  -XX:+UseG1GC \
  -XX:MaxGCPauseMillis=200 \
  -XX:+HeapDumpOnOutOfMemoryError \
  -XX:HeapDumpPath=/var/log/myapp/ \
  -XX:+PrintGCDetails \
  -XX:+PrintGCDateStamps \
  -Xloggc:/var/log/myapp/gc.log
```

### Container/Cloud Optimization

```bash
# For containers, aware of container limits
java -jar app.jar \
  -XX:+UseContainerSupport \
  -XX:MaxRAMPercentage=75.0
```

## Performance Testing

### JMH (Java Microbenchmark Harness)

```xml
<dependency>
    <groupId>org.openjdk.jmh</groupId>
    <artifactId>jmh-core</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.openjdk.jmh</groupId>
    <artifactId>jmh-generator-annprocess</artifactId>
    <scope>test</scope>
</dependency>
```

```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MILLISECONDS)
@State(Scope.Benchmark)
public class UserServiceBenchmark {

    @Autowired
    private UserService userService;

    @Benchmark
    public UserDTO benchmarkFindById() {
        return userService.findById(1L);
    }
}
```

### Load Testing with Gatling

```scala
import io.gatling.core.Predef._
import io.gatling.http.Predef._

class UserApiSimulation extends Simulation {

  val httpProtocol = http
    .baseUrl("http://localhost:8080")
    .acceptHeader("application/json")

  val scn = scenario("Get User")
    .exec(http("Get User by ID")
      .get("/api/users/1")
      .check(status.is(200)))

  setUp(
    scn.inject(
      rampUsersPerSec(1) to (100) during (60 seconds)
    )
  ).protocols(httpProtocol)
}
```

## Performance Best Practices

1. **Use caching** - Cache frequently accessed data
2. **Enable connection pooling** - Configure HikariCP properly
3. **Solve N+1 queries** - Use EntityGraph or JOIN FETCH
4. **Use DTO projections** - For read-only queries
5. **Implement pagination** - For large datasets
6. **Use async processing** - For non-blocking operations
7. **Monitor with Actuator** - Track performance metrics
8. **Optimize database** - Add indexes, tune queries
9. **Use lazy loading** - But beware of LazyInitializationException
10. **Batch operations** - For bulk inserts/updates
11. **Profile before optimizing** - Use profilers to find bottlenecks
12. **Test under load** - Simulate production traffic

## Monitoring Tools

- **Spring Boot Actuator** - Built-in metrics and health
- **Micrometer** - Metrics facade for Prometheus, Graphite, etc.
- **Prometheus + Grafana** - Metrics collection and visualization
- **Java Melody** - Performance monitoring
- **JProfiler/YourKit** - Profiling tools

## Summary Checklist

- [ ] Enable and configure caching with Caffeine
- [ ] Optimize connection pool settings
- [ ] Solve N+1 query problems
- [ ] Use DTO projections for read queries
- [ ] Implement async processing
- [ ] Enable Spring Boot Actuator
- [ ] Add custom health indicators
- [ ] Configure JVM options
- [ ] Add database indexes
- [ ] Implement batch operations
- [ ] Profile application performance
- [ ] Load test before deployment

## Resources

- [Spring Boot: Best Practices for Scalable Applications](https://www.codewalnut.com/insights/spring-boot-best-practices-for-scalable-applications)
- [Java Microservices Architecture Guide](https://medium.com/@shahharsh172/java-microservices-architecture-guide-spring-boot-best-practices-for-production-2025-9aa5c287248f)
- [Spring Boot Performance Tuning](https://www.baeldung.com/spring-boot-performance)
- [Caffeine GitHub](https://github.com/ben-manes/caffeine)
