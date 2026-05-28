---
name: Spring Boot Architecture
description: Application structure, auto-configuration, profiles, bean lifecycle, and configuration properties.
metadata:
  labels: [java, spring-boot, architecture, configuration]
  triggers:
    files: ['**/Application.java', '**/*Configuration.java', 'application.yml', 'application.properties', 'application-*.yml']
    keywords: [SpringBootApplication, Configuration, Bean, Profile, AutoConfiguration, ConfigurationProperties, EnableAutoConfiguration]
---

# Spring Boot Architecture Standards

## Application Entry Point

```java
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

// @SpringBootApplication combines:
// @Configuration - source of bean definitions
// @EnableAutoConfiguration - auto-configure based on classpath
// @ComponentScan - scan for components in this package and below
```

## Configuration Classes

```java
@Configuration
public class AppConfig {

    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder builder) {
        return builder
            .setConnectTimeout(Duration.ofSeconds(5))
            .setReadTimeout(Duration.ofSeconds(30))
            .build();
    }

    @Bean
    @ConditionalOnProperty(name = "app.feature.enabled", havingValue = "true")
    public FeatureService featureService() {
        return new FeatureServiceImpl();
    }
}

// Conditional beans
@ConditionalOnProperty(...)      // Based on property
@ConditionalOnClass(...)         // Based on class presence
@ConditionalOnMissingBean(...)   // If no other bean exists
@ConditionalOnBean(...)          // If another bean exists
@ConditionalOnExpression(...)    // SpEL expression
```

## Configuration Properties

```java
@ConfigurationProperties(prefix = "app")
@Validated
public record AppProperties(
    @NotBlank String name,
    @NotNull Duration timeout,
    @Valid DatabaseProperties database
) {
    public record DatabaseProperties(
        String host,
        int port,
        @NotBlank String username
    ) {}
}

// Enable in configuration
@Configuration
@EnableConfigurationProperties(AppProperties.class)
public class AppConfig {}

// Usage
@Service
public class MyService {
    private final AppProperties props;

    public MyService(AppProperties props) {
        this.props = props;
    }
}
```

```yaml
# application.yml
app:
  name: my-application
  timeout: 30s
  database:
    host: localhost
    port: 5432
    username: admin
```

## Profiles

```yaml
# application.yml (default)
spring:
  profiles:
    active: dev

---
spring:
  config:
    activate:
      on-profile: dev
server:
  port: 8080
logging:
  level:
    root: DEBUG

---
spring:
  config:
    activate:
      on-profile: prod
server:
  port: 80
logging:
  level:
    root: INFO
```

```java
// Profile-specific beans
@Configuration
@Profile("dev")
public class DevConfig {
    @Bean
    public DataSource dataSource() {
        return new EmbeddedDatabaseBuilder()
            .setType(EmbeddedDatabaseType.H2)
            .build();
    }
}

@Configuration
@Profile("prod")
public class ProdConfig {
    @Bean
    public DataSource dataSource(DataSourceProperties props) {
        return DataSourceBuilder.create()
            .url(props.getUrl())
            .username(props.getUsername())
            .password(props.getPassword())
            .build();
    }
}
```

## Bean Lifecycle

```java
@Component
public class MyComponent implements InitializingBean, DisposableBean {

    @PostConstruct
    public void init() {
        // Called after dependency injection
    }

    @Override
    public void afterPropertiesSet() {
        // Called after properties set
    }

    @PreDestroy
    public void cleanup() {
        // Called before destruction
    }

    @Override
    public void destroy() {
        // Called on shutdown
    }
}

// Or with @Bean
@Bean(initMethod = "init", destroyMethod = "cleanup")
public MyService myService() {
    return new MyService();
}
```

## Best Practices

1. **Use @ConfigurationProperties** over @Value for type-safe configuration
2. **Profiles for environment-specific** config, not feature flags
3. **Externalize configuration** - never hardcode secrets
4. **Use record classes** for immutable configuration properties
5. **Validate configuration** with @Validated and Jakarta constraints
6. **Auto-configuration order** matters - use @AutoConfigureAfter/@AutoConfigureBefore

## References

- [Auto-Configuration](references/auto-configuration.md) - Custom auto-config, conditions
- [Configuration Properties](references/configuration-properties.md) - Binding, validation, relaxed binding
