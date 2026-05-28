# Configuration Management Best Practices

This reference covers Spring Boot configuration including application properties, profiles, externalized configuration, and environment-specific settings.

## Application Properties

### Properties vs. YAML

**application.properties:**
```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/mydb
spring.datasource.username=user
spring.datasource.password=pass
spring.jpa.hibernate.ddl-auto=validate
server.port=8080
```

**application.yml (recommended):**
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: user
    password: pass
  jpa:
    hibernate:
      ddl-auto: validate
server:
  port: 8080
```

**YAML advantages:**
- More readable and hierarchical
- Supports complex structures
- Less repetition
- Better for large configurations

## Core Configuration

### Server Configuration

```yaml
server:
  port: 8080
  servlet:
    context-path: /api
    encoding:
      charset: UTF-8
      enabled: true
      force: true
  compression:
    enabled: true
    mime-types: text/html,text/xml,text/plain,text/css,application/json
  error:
    include-message: always
    include-binding-errors: always
    include-stacktrace: on-param  # never, always, on-param
    include-exception: false
  tomcat:
    threads:
      max: 200
      min-spare: 10
    max-connections: 10000
    accept-count: 100
```

### Database Configuration

```yaml
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
      pool-name: MyHikariPool

  jpa:
    hibernate:
      ddl-auto: validate  # none, validate, update, create, create-drop
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
        cache:
          use_second_level_cache: true
          use_query_cache: true
          region.factory_class: org.hibernate.cache.jcache.JCacheRegionFactory
```

### Logging Configuration

```yaml
logging:
  level:
    root: INFO
    com.example.myapp: DEBUG
    org.springframework.web: INFO
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql.BasicBinder: TRACE
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} - %msg%n"
    file: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
  file:
    name: logs/application.log
    max-size: 10MB
    max-history: 30
    total-size-cap: 1GB
```

## Profiles

### Profile-Specific Configuration

**application.yml (default):**
```yaml
spring:
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
```

**application-dev.yml:**
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb_dev
  jpa:
    show-sql: true

logging:
  level:
    com.example.myapp: DEBUG
```

**application-prod.yml:**
```yaml
spring:
  datasource:
    url: jdbc:postgresql://prod-server:5432/mydb_prod
    hikari:
      maximum-pool-size: 20
  jpa:
    show-sql: false

logging:
  level:
    com.example.myapp: INFO
  file:
    name: /var/log/myapp/application.log
```

**application-test.yml:**
```yaml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
  jpa:
    hibernate:
      ddl-auto: create-drop

logging:
  level:
    com.example.myapp: DEBUG
```

### Activate Profiles

**Command line:**
```bash
java -jar app.jar --spring.profiles.active=prod
```

**Environment variable:**
```bash
export SPRING_PROFILES_ACTIVE=prod
java -jar app.jar
```

**application.yml:**
```yaml
spring:
  profiles:
    active: dev
```

**Programmatic:**
```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication app = new SpringApplication(Application.class);
        app.setAdditionalProfiles("dev");
        app.run(args);
    }
}
```

## Type-Safe Configuration

### @ConfigurationProperties

**Properties:**
```yaml
app:
  name: My Application
  security:
    jwt:
      secret: mySecretKey
      expiration: 86400
  features:
    enable-cache: true
    max-upload-size: 10485760
```

**Configuration class:**
```java
@ConfigurationProperties(prefix = "app")
@Component
@Getter
@Setter
public class AppConfig {

    private String name;

    private Security security = new Security();

    private Features features = new Features();

    public static class Security {
        private Jwt jwt = new Jwt();

        public static class Jwt {
            private String secret;
            private Long expiration = 86400L;
        }
    }

    public static class Features {
        private boolean enableCache = false;
        private Long maxUploadSize = 10485760L;  // 10MB
    }
}
```

**Enable and use:**
```java
@SpringBootApplication
@EnableConfigurationProperties(AppConfig.class)
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

@Service
public class JwtService {

    @Autowired
    private AppConfig appConfig;

    public String generateToken() {
        String secret = appConfig.getSecurity().getJwt().getSecret();
        Long expiration = appConfig.getSecurity().getJwt().getExpiration();
        // ...
    }
}
```

### Constructor Binding (Immutable)

```java
@ConfigurationProperties(prefix = "app")
@ConstructorBinding
public class AppProperties {

    private final String name;
    private final Security security;

    public AppProperties(String name, Security security) {
        this.name = name;
        this.security = security;
    }

    public record Security(Jwt jwt) {
        public record Jwt(String secret, Long expiration) {}
    }
}
```

## Environment Variables

### Mapping Convention

Spring Boot automatically maps environment variables to properties:

```bash
# Environment variable → Property
SPRING_DATASOURCE_URL → spring.datasource.url
SPRING_DATASOURCE_USERNAME → spring.datasource.username
APP_SECURITY_JWT_SECRET → app.security.jwt.secret
```

**Use in application.yml:**
```yaml
spring:
  datasource:
    url: ${DATABASE_URL}
    username: ${DATABASE_USER:user}
    password: ${DATABASE_PASSWORD:pass}
```

### External Configuration Files

**Search locations (in order):**
1. `/config` subdirectory of current directory
2. Current directory
3. `/config` package in classpath
4. Classpath root

**Custom config location:**
```bash
java -jar app.jar --spring.config.location=file:/etc/myapp/application.yml
```

**Additional config location:**
```bash
java -jar app.jar --spring.config.additional-location=file:/etc/myapp/
```

## @Value Annotation

### Simple Values

```java
@Component
public class EmailService {

    @Value("${app.email.from:noreply@example.com}")
    private String fromEmail;

    @Value("${app.email.enabled:true}")
    private boolean enabled;

    @Value("${app.email.max-retries:3}")
    private int maxRetries;

    @Value("#{systemProperties['user.home']}")
    private String userHome;

    @Value("${app.list.values}")
    private String[] valuesArray;

    @Value("#{${app.map.values}}")
    private Map<String, String> valuesMap;
}
```

**application.yml:**
```yaml
app:
  email:
    from: admin@example.com
    enabled: true
    max-retries: 5
  list:
    values: one,two,three
  map:
    values: "{key1: 'value1', key2: 'value2'}"
```

### SpEL Expressions

```java
@Component
public class ConfigComponent {

    @Value("#{'${app.allowed.origins}'.split(',')}")
    private List<String> allowedOrigins;

    @Value("#{systemProperties['os.name']}")
    private String osName;

    @Value("#{T(java.lang.Math).random() * 100.0}")
    private double randomNumber;

    @Value("#{systemEnvironment['DATABASE_URL'] ?: 'jdbc:h2:mem:testdb'}")
    private String databaseUrl;
}
```

## Profile-Based Beans

### Conditional Beans

```java
@Configuration
public class DataSourceConfig {

    @Bean
    @Profile("dev")
    public DataSource devDataSource() {
        return new H2DataSource();
    }

    @Bean
    @Profile("prod")
    public DataSource prodDataSource() {
        return new PostgreSQLDataSource();
    }

    @Bean
    @Profile("!test")  // All profiles except test
    public EmailService emailService() {
        return new SmtpEmailService();
    }
}
```

### Custom Conditional

```java
@Configuration
public class CacheConfig {

    @Bean
    @ConditionalOnProperty(
        name = "app.cache.enabled",
        havingValue = "true",
        matchIfMissing = false
    )
    public CacheManager cacheManager() {
        return new ConcurrentMapCacheManager();
    }
}
```

## Property Encryption

### Jasypt for Sensitive Data

```xml
<dependency>
    <groupId>com.github.ulisesbocchio</groupId>
    <artifactId>jasypt-spring-boot-starter</artifactId>
    <version>3.0.5</version>
</dependency>
```

**Encrypt password:**
```bash
java -cp jasypt-1.9.3.jar org.jasypt.intf.cli.JasyptPBEStringEncryptionCLI \
  input="mySecretPassword" \
  password="encryptionPassword" \
  algorithm=PBEWithMD5AndDES
```

**Use encrypted value:**
```yaml
app:
  security:
    jwt:
      secret: ENC(encryptedValueHere)
```

**Provide encryption password:**
```bash
java -jar app.jar --jasypt.encryptor.password=encryptionPassword
```

Or environment variable:
```bash
export JASYPT_ENCRYPTOR_PASSWORD=encryptionPassword
java -jar app.jar
```

## Configuration Best Practices

1. **Externalize configuration** - Never hardcode config in code
2. **Use profiles** - Separate dev, test, prod configs
3. **Use environment variables** - For sensitive data
4. **Provide defaults** - Use `${VAR:default}` syntax
5. **Type-safe config** - Use @ConfigurationProperties over @Value
6. **Encrypt secrets** - Use Jasypt or external secret management
7. **Validate configuration** - Use @Validated with JSR-303
8. **Document configuration** - Include sample config files
9. **Use meaningful prefixes** - Group related properties
10. **Never commit secrets** - Add application-prod.yml to .gitignore

## Configuration Validation

```java
@ConfigurationProperties(prefix = "app")
@Validated
public class AppProperties {

    @NotBlank
    private String name;

    @Valid
    private Security security = new Security();

    @NotNull
    @Min(1024)
    @Max(65535)
    private Integer port;

    public static class Security {
        @NotBlank
        private String jwtSecret;

        @Min(3600)
        private Long jwtExpiration;
    }
}
```

## Summary Checklist

- [ ] Use YAML over properties for readability
- [ ] Configure profiles for different environments
- [ ] Use @ConfigurationProperties for type-safe config
- [ ] Externalize configuration with environment variables
- [ ] Provide defaults for all properties
- [ ] Encrypt sensitive data
- [ ] Validate configuration at startup
- [ ] Document all configuration options
- [ ] Never commit secrets to version control
- [ ] Use appropriate connection pooling settings

## Resources

- [Spring Boot Externalized Configuration](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.external-config)
- [Baeldung - Spring Boot Configuration](https://www.baeldung.com/configuration-properties-in-spring-boot)
- [Spring Boot Properties](https://docs.spring.io/spring-boot/docs/current/reference/html/application-properties.html)
