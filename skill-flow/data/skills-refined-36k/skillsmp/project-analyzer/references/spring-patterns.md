# Spring Boot / Spring Cloud Technology Patterns

This reference provides common technology patterns and search strategies for Java/Spring Boot projects.

## Common Spring Boot Starter Patterns

### Web & REST
- `spring-boot-starter-web` - Spring MVC, Tomcat
- `spring-boot-starter-webflux` - Reactive web with Netty

### Data Access
- `spring-boot-starter-data-jpa` - JPA with Hibernate
- `spring-boot-starter-data-redis` - Redis integration
- `mybatis-spring-boot-starter` - MyBatis ORM
- `mybatis-plus-boot-starter` - MyBatis enhancement

### Spring Cloud Components
- `spring-cloud-starter-gateway` - API Gateway
- `spring-cloud-starter-openfeign` - Declarative REST client
- `spring-cloud-starter-alibaba-nacos-discovery` - Service discovery
- `spring-cloud-starter-alibaba-nacos-config` - Configuration management
- `spring-cloud-starter-netflix-eureka-client` - Eureka client

### Messaging
- `spring-boot-starter-amqp` - RabbitMQ
- `spring-kafka` - Apache Kafka
- `rocketmq-spring-boot-starter` - RocketMQ

### Observability
- `spring-boot-starter-actuator` - Health checks, metrics
- `micrometer-registry-prometheus` - Prometheus metrics

## Common Configuration Patterns

### Multi-Environment Setup

Look for:
- `application.yml` (base configuration)
- `application-dev.yml` (development)
- `application-test.yml` (testing)
- `application-prod.yml` (production)
- `bootstrap.yml` (Spring Cloud bootstrap)

Active profile indicators:
```yaml
spring:
  profiles:
    active: dev
```

### Nacos Configuration Pattern

```yaml
spring:
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848
        namespace: ${NACOS_NAMESPACE:}
      config:
        server-addr: localhost:8848
        namespace: ${NACOS_NAMESPACE:}
        group: DEFAULT_GROUP
        file-extension: yaml
```

### Database Configuration Pattern

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/dbname?useUnicode=true&characterEncoding=utf8
    driver-class-name: com.mysql.cj.jdbc.Driver
    username: ${DB_USERNAME:root}
    password: ${DB_PASSWORD:}
```

### Redis Configuration Pattern

```yaml
spring:
  redis:
    host: ${REDIS_HOST:localhost}
    port: ${REDIS_PORT:6379}
    password: ${REDIS_PASSWORD:}
    database: 0
```

## Common Annotation Patterns

### Spring Boot Entry Points
```java
@SpringBootApplication
@EnableDiscoveryClient  // For Nacos/Eureka
@EnableFeignClients     // For Feign clients
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### Configuration Classes
```java
@Configuration
@ConfigurationProperties(prefix = "custom")
@EnableScheduling
@EnableAsync
@EnableCaching
```

### REST Controllers
```java
@RestController
@RequestMapping("/api/v1")
@Api(tags = "User Management")  // Swagger
@Slf4j  // Lombok logging
```

### Service Layer
```java
@Service
@Transactional
@Slf4j
```

### Data Access
```java
@Mapper  // MyBatis
@Repository  // JPA
```

### Scheduled Tasks
```java
@Scheduled(cron = "0 0 2 * * ?")
@Scheduled(fixedRate = 60000)
```

### Message Listeners
```java
@RabbitListener(queues = "queue-name")
@KafkaListener(topics = "topic-name")
```

### AOP & Interceptors
```java
@Aspect
@Component
@ControllerAdvice  // Global exception handler
@RestControllerAdvice
```

## Common Package Structures

### Standard Layered Structure
```
com.company.project/
├── controller/     - REST endpoints
├── service/        - Business logic
│   └── impl/
├── dao/           - Data access (MyBatis)
├── mapper/        - MyBatis mappers
├── repository/    - JPA repositories
├── entity/        - Database entities
├── model/         - Domain models
│   ├── dto/       - Data transfer objects
│   ├── vo/        - View objects
│   └── bo/        - Business objects
├── config/        - Configuration classes
├── exception/     - Custom exceptions
├── util/          - Utilities
├── constant/      - Constants
├── aspect/        - AOP aspects
└── interceptor/   - Interceptors
```

### Domain-Driven Design Structure
```
com.company.project/
├── interfaces/     - API layer (controllers)
├── application/    - Application services
├── domain/         - Domain models & services
│   ├── model/
│   ├── service/
│   └── repository/
├── infrastructure/ - Infrastructure implementations
└── common/         - Shared components
```

## Search Commands by Category

### Finding Technology Stack
```bash
# Spring Boot version
grep -r "spring-boot-starter-parent" --include="pom.xml"

# All Spring dependencies
grep -r "spring-boot-starter" --include="pom.xml"

# Database frameworks
grep -r "mybatis\|spring-data-jpa\|hibernate" --include="pom.xml"

# Message queues
grep -r "amqp\|kafka\|rocketmq" --include="pom.xml"

# Spring Cloud components
grep -r "spring-cloud-starter" --include="pom.xml"
```

### Finding Configuration
```bash
# All YAML configs
find . -name "*.yml" -o -name "*.yaml"

# All properties files
find . -name "*.properties"

# Nacos configuration
grep -r "nacos" --include="*.yml" --include="*.yaml"

# Database connections
grep -r "url:\|jdbc:" --include="*.yml" --include="*.yaml" --include="*.properties"

# Active profiles
grep -r "spring.profiles.active" --include="*.yml" --include="*.yaml" --include="*.properties"
```

### Finding Key Components
```bash
# Application entry points
grep -r "@SpringBootApplication" --include="*.java"

# Controllers
grep -r "@RestController\|@Controller" --include="*.java"

# Services
grep -r "@Service" --include="*.java"

# Configuration classes
grep -r "@Configuration" --include="*.java"

# Scheduled tasks
grep -r "@Scheduled" --include="*.java"

# Message listeners
grep -r "@RabbitListener\|@KafkaListener" --include="*.java"

# Exception handlers
grep -r "@ControllerAdvice\|@RestControllerAdvice" --include="*.java"
```

## Internal SDK Identification

### Common Internal GroupId Patterns
Chinese companies often use:
- `com.company.*`
- `cn.company.*`
- Company abbreviations

### Search for Internal Dependencies
```bash
# Find groupIds in dependencies
grep -r "<groupId>" --include="pom.xml" | sort | uniq

# Find system-scoped dependencies (often internal JARs)
grep -r "scope>system" --include="pom.xml" -A 2

# Find local JAR references
find . -type d -name "lib" -o -name "libs"
find . -name "*.jar"
```

### Identifying SDK Purpose
Look for naming patterns:
- `*-client` → External API client
- `*-api` → API definitions
- `*-common` → Shared utilities
- `*-sdk` → General SDK
- `*-starter` → Spring Boot starter
- `ai-*` / `*-ai` → AI-related
- `payment-*` → Payment integration

## Development Environment Indicators

### Docker Compose
```bash
find . -name "docker-compose*.yml"
```

Common services in docker-compose:
- MySQL / PostgreSQL
- Redis
- RabbitMQ / Kafka
- Nacos
- Elasticsearch
- MongoDB

### README Files
```bash
find . -name "README*" -o -name "readme*"
find . -type d -name "doc" -o -name "docs"
```

### Scripts
```bash
find . -name "*.sh" | head -20
```

Common scripts:
- `start.sh` / `startup.sh`
- `deploy.sh`
- `init.sh` / `setup.sh`
