# Microservice Template

Extends the Secure REST API template with Spring Cloud microservices patterns, service discovery, configuration server, and distributed tracing.

## Additional Dependencies

```xml
<properties>
    <spring-cloud.version>2023.0.0</spring-cloud.version>
</properties>

<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-dependencies</artifactId>
            <version>${spring-cloud.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <!-- Spring Cloud Config Client -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-config</artifactId>
    </dependency>

    <!-- Eureka Client (Service Discovery) -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-netflix-eureka-client</artifactId>
    </dependency>

    <!-- Spring Cloud Gateway (if API Gateway) -->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-gateway</artifactId>
    </dependency>

    <!-- Resilience4j (Circuit Breaker) -->
    <dependency>
        <groupId>io.github.resilience4j</groupId>
        <artifactId>resilience4j-spring-boot3</artifactId>
        <version>2.1.0</version>
    </dependency>

    <!-- Distributed Tracing -->
    <dependency>
        <groupId>io.micrometer</groupId>
        <artifactId>micrometer-tracing-bridge-brave</artifactId>
    </dependency>
    <dependency>
        <groupId>io.zipkin.reporter2</groupId>
        <artifactId>zipkin-reporter-brave</artifactId>
    </dependency>

    <!-- Kafka or RabbitMQ (optional) -->
    <dependency>
        <groupId>org.springframework.kafka</groupId>
        <artifactId>spring-kafka</artifactId>
    </dependency>
</dependencies>
```

## Configuration

### bootstrap.yml (Config Client)

```yaml
spring:
  application:
    name: user-service
  cloud:
    config:
      uri: http://localhost:8888
      fail-fast: true
      retry:
        initial-interval: 3000
        multiplier: 1.5
        max-interval: 20000
        max-attempts: 6
```

### application.yml (Microservice Config)

```yaml
spring:
  application:
    name: user-service

  cloud:
    config:
      import: optional:configserver:http://localhost:8888

eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka/
    register-with-eureka: true
    fetch-registry: true
  instance:
    prefer-ip-address: true
    lease-renewal-interval-in-seconds: 10
    lease-expiration-duration-in-seconds: 30

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  metrics:
    export:
      prometheus:
        enabled: true
    tags:
      application: ${spring.application.name}
  tracing:
    sampling:
      probability: 1.0  # Sample all requests
  zipkin:
    tracing:
      endpoint: http://localhost:9411/api/v2/spans

resilience4j:
  circuitbreaker:
    instances:
      userService:
        sliding-window-size: 10
        failure-rate-threshold: 50
        wait-duration-in-open-state: 10s
        permitted-number-of-calls-in-half-open-state: 3
  retry:
    instances:
      userService:
        max-attempts: 3
        wait-duration: 1s
        exponential-backoff-multiplier: 2
```

## Microservice Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     API Gateway                         │
│              (Port: 8080, Gateway)                      │
└────────────┬────────────────────────────────────────────┘
             │
    ┌────────┴────────┬───────────────┬──────────────┐
    │                 │               │              │
    ▼                 ▼               ▼              ▼
┌────────┐      ┌──────────┐    ┌─────────┐   ┌──────────┐
│ Config │      │  Eureka  │    │ User    │   │ Order    │
│ Server │      │ Server   │    │ Service │   │ Service  │
│:8888   │      │ :8761    │    │ :8081   │   │ :8082    │
└────────┘      └──────────┘    └─────────┘   └──────────┘
                                                │
                                                ▼
                                          ┌─────────┐
                                          │ Product │
                                          │ Service │
                                          │ :8083   │
                                          └─────────┘
```

## Service-to-Service Communication

### RestTemplate with Load Balancing

```java
@Configuration
public class RestTemplateConfig {

    @Bean
    @LoadBalanced
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}

@Service
public class OrderService {

    @Autowired
    private RestTemplate restTemplate;

    public UserDTO getUserById(Long userId) {
        // Service name instead of URL
        return restTemplate.getForObject(
            "http://user-service/api/users/" + userId,
            UserDTO.class
        );
    }
}
```

### Feign Client (Recommended)

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
```

```java
@FeignClient(name = "user-service", url = "${user-service.url:}")
public interface UserClient {

    @GetMapping("/api/users/{id}")
    UserDTO getUserById(@PathVariable Long id);

    @PostMapping("/api/users")
    UserDTO createUser(@RequestBody CreateUserRequest request);
}

@EnableFeignClients
@SpringBootApplication
public class OrderServiceApplication {
    // ...
}
```

## Circuit Breaker Pattern

```java
@Service
public class OrderService {

    @Autowired
    private UserClient userClient;

    @CircuitBreaker(name = "userService", fallbackMethod = "getUserFallback")
    @Retry(name = "userService")
    public UserDTO getUserWithCircuitBreaker(Long userId) {
        return userClient.getUserById(userId);
    }

    private UserDTO getUserFallback(Long userId, Exception ex) {
        // Fallback logic
        log.error("Error calling user service: {}", ex.getMessage());
        UserDTO fallback = new UserDTO();
        fallback.setId(userId);
        fallback.setEmail("unknown@example.com");
        return fallback;
    }
}
```

## Async Communication with Kafka

### Producer

```java
@Service
public class OrderEventPublisher {

    @Autowired
    private KafkaTemplate<String, OrderEvent> kafkaTemplate;

    public void publishOrderCreated(Order order) {
        OrderEvent event = OrderEvent.builder()
            .orderId(order.getId())
            .userId(order.getUserId())
            .status(order.getStatus())
            .build();

        kafkaTemplate.send("order-created", event);
    }
}
```

### Consumer

```java
@Service
public class OrderEventConsumer {

    @KafkaListener(topics = "order-created", groupId = "order-service")
    public void handleOrderCreated(OrderEvent event) {
        log.info("Received order created event: {}", event);
        // Process event
    }
}
```

## Docker Support

### Dockerfile

```dockerfile
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

COPY target/user-service.jar app.jar

EXPOSE 8081

ENTRYPOINT ["java", "-jar", "app.jar"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  config-server:
    build: ./config-server
    ports:
      - "8888:8888"
    environment:
      - SPRING_PROFILES_ACTIVE=docker

  eureka-server:
    build: ./eureka-server
    ports:
      - "8761:8761"
    depends_on:
      - config-server

  user-service:
    build: ./user-service
    ports:
      - "8081:8081"
    depends_on:
      - config-server
      - eureka-server
      - postgres
    environment:
      - SPRING_PROFILES_ACTIVE=docker

  order-service:
    build: ./order-service
    ports:
      - "8082:8082"
    depends_on:
      - config-server
      - eureka-server
      - postgres

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=microservices
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"

  zipkin:
    image: openzipkin/zipkin:latest
    ports:
      - "9411:9411"

  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

## Health Checks

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

## Distributed Tracing

### Adding Tracing to Requests

```java
@RestController
public class UserController {

    static final Tracer tracer = Tracer.create();

    @GetMapping("/api/users/{id}")
    public UserDTO getUser(@PathVariable Long id) {
        // Span automatically created by Spring Boot
        return userService.findById(id);
    }
}
```

### Manual Span Creation

```java
@Service
public class UserService {

    @Autowired
    private Tracer tracer;

    public UserDTO findById(Long id) {
        Span span = tracer.nextSpan().name("user-service-findById");
        try (Tracer.SpanInScope ws = tracer.withSpanInScope(span)) {
            span.tag("userId", String.valueOf(id));

            // Business logic

            span.event("User found");
            return userDTO;
        } finally {
            span.end();
        }
    }
}
```

## Microservice Patterns

### Saga Pattern (Distributed Transactions)

```java
@Service
public class OrderSagaOrchestrator {

    public void processOrder(Order order) {
        try {
            // Step 1: Create order
            orderService.createOrder(order);

            // Step 2: Reserve inventory
            inventoryService.reserve(order.getItems());

            // Step 3: Process payment
            paymentService.process(order.getPayment());

            // Step 4: Confirm order
            orderService.confirm(order.getId());
        } catch (Exception e) {
            // Compensating transactions
            paymentService.refund(order.getId());
            inventoryService.release(order.getItems());
            orderService.cancel(order.getId());
        }
    }
}
```

## API Gateway Configuration

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service
          predicates:
            - Path=/api/users/**
          filters:
            - StripPrefix=0

        - id: order-service
          uri: lb://order-service
          predicates:
            - Path=/api/orders/**
          filters:
            - StripPrefix=0
```

## Best Practices

1. **Use service discovery** - Don't hardcode URLs
2. **Implement circuit breakers** - Prevent cascading failures
3. **Use async communication** - For loosely coupled services
4. **Implement distributed tracing** - Debug issues across services
5. **Centralized configuration** - Externalize configuration
6. **API versioning** - Support multiple API versions
7. **Health checks** - Implement liveness and readiness probes
8. **Observability** - Metrics, logs, traces
9. **Fault tolerance** - Timeouts, retries, fallbacks
10. **Security** - JWT propagation between services

## Ports Reference

| Service | Port |
|---------|------|
| API Gateway | 8080 |
| Config Server | 8888 |
| Eureka Server | 8761 |
| User Service | 8081 |
| Order Service | 8082 |
| Product Service | 8083 |
| PostgreSQL | 5432 |
| Zipkin | 9411 |
| Prometheus | 9090 |
| Grafana | 3000 |

## See Also

- [Spring Cloud Documentation](https://spring.io/projects/spring-cloud)
- [Secure REST API Template](../rest-api-secure/) - Base for microservices
- [Resilience4j Documentation](https://resilience4j.readme.io/)
