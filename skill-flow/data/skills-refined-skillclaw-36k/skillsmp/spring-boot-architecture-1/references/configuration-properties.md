# Configuration Properties

## Type-Safe Configuration

```java
// Using record (immutable, recommended)
@ConfigurationProperties(prefix = "app")
@Validated
public record AppProperties(
    @NotBlank String name,
    @NotNull Duration timeout,
    @Min(1) @Max(100) int maxRetries,
    @Valid ServerProperties server,
    Map<String, String> metadata,
    List<String> allowedOrigins
) {
    public record ServerProperties(
        String host,
        @Min(1) @Max(65535) int port,
        boolean ssl
    ) {}
}

// Using class (when mutability needed)
@ConfigurationProperties(prefix = "app")
@Validated
public class AppProperties {
    @NotBlank
    private String name;

    @DurationUnit(ChronoUnit.SECONDS)
    private Duration timeout = Duration.ofSeconds(30);

    // getters and setters
}
```

## Binding Configuration

```yaml
# application.yml
app:
  name: My Application
  timeout: 30s           # Duration
  max-retries: 3         # kebab-case → camelCase
  server:
    host: localhost
    port: 8080
    ssl: true
  metadata:
    version: "1.0"
    env: production
  allowed-origins:
    - http://localhost:3000
    - https://example.com
```

## Relaxed Binding

Spring Boot supports multiple formats:

```yaml
# All equivalent for "firstName" property
app:
  firstName: John       # standard camel case
  first-name: John      # kebab-case (recommended in YAML)
  first_name: John      # underscore notation
  FIRST_NAME: John      # uppercase (environment variables)
```

## Validation

```java
@ConfigurationProperties(prefix = "app.database")
@Validated
public record DatabaseProperties(
    @NotBlank String url,
    @NotBlank String username,
    @NotBlank String password,
    @Min(1) @Max(100) int poolSize,
    @DurationMin(seconds = 1) @DurationMax(minutes = 5) Duration connectionTimeout
) {}

// Custom validation
public record SecurityProperties(
    @NotBlank String secretKey
) {
    public SecurityProperties {
        if (secretKey.length() < 32) {
            throw new IllegalArgumentException("Secret key must be at least 32 characters");
        }
    }
}
```

## Nested Properties

```java
@ConfigurationProperties(prefix = "app")
public record AppProperties(
    @NestedConfigurationProperty
    DatabaseProperties database,

    @NestedConfigurationProperty
    CacheProperties cache,

    Map<String, ServiceProperties> services
) {
    public record DatabaseProperties(
        String url,
        String username
    ) {}

    public record CacheProperties(
        Duration ttl,
        int maxSize
    ) {}

    public record ServiceProperties(
        String url,
        Duration timeout
    ) {}
}
```

```yaml
app:
  database:
    url: jdbc:postgresql://localhost/db
    username: admin
  cache:
    ttl: 5m
    max-size: 1000
  services:
    user-service:
      url: http://users:8080
      timeout: 10s
    order-service:
      url: http://orders:8080
      timeout: 30s
```

## Constructor Binding

```java
// Immutable with constructor binding (default for records)
@ConfigurationProperties(prefix = "app")
public record AppProperties(
    String name,
    Duration timeout,
    ServerProperties server
) {
    // Default values via compact constructor
    public AppProperties {
        if (timeout == null) {
            timeout = Duration.ofSeconds(30);
        }
    }

    public record ServerProperties(String host, int port) {
        public ServerProperties {
            if (port == 0) {
                port = 8080;
            }
        }
    }
}
```

## Enabling Configuration Properties

```java
// Option 1: On configuration class
@Configuration
@EnableConfigurationProperties(AppProperties.class)
public class AppConfig {}

// Option 2: Component scan (not recommended)
@ConfigurationProperties(prefix = "app")
@Component  // Scanned automatically
public class AppProperties {}

// Option 3: ConfigurationPropertiesScan
@SpringBootApplication
@ConfigurationPropertiesScan("com.example.config")
public class Application {}
```

## Environment Variable Override

```bash
# Override nested properties
APP_DATABASE_URL=jdbc:postgresql://prod/db
APP_SERVER_PORT=80

# Override list items
APP_ALLOWED_ORIGINS_0=http://example.com
APP_ALLOWED_ORIGINS_1=http://api.example.com

# Override map items
APP_SERVICES_USERSERVICE_URL=http://users:8080
```
