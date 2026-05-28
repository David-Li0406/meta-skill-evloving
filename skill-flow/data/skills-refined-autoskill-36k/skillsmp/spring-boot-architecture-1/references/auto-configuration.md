# Spring Boot Auto-Configuration

## Custom Auto-Configuration

```java
// 1. Create auto-configuration class
@AutoConfiguration
@ConditionalOnClass(MyService.class)
@EnableConfigurationProperties(MyProperties.class)
public class MyAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    public MyService myService(MyProperties properties) {
        return new MyServiceImpl(properties);
    }

    @Bean
    @ConditionalOnProperty(
        prefix = "my.feature",
        name = "enabled",
        havingValue = "true",
        matchIfMissing = false
    )
    public FeatureService featureService() {
        return new FeatureServiceImpl();
    }
}

// 2. Register in META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
// com.example.autoconfigure.MyAutoConfiguration
```

## Conditional Annotations

```java
// Property conditions
@ConditionalOnProperty(name = "feature.enabled", havingValue = "true")
@ConditionalOnProperty(name = "feature.enabled", matchIfMissing = true)

// Class conditions
@ConditionalOnClass(DataSource.class)
@ConditionalOnMissingClass("org.mongodb.Driver")

// Bean conditions
@ConditionalOnBean(DataSource.class)
@ConditionalOnMissingBean(MyService.class)
@ConditionalOnSingleCandidate(DataSource.class)

// Resource conditions
@ConditionalOnResource(resources = "classpath:schema.sql")

// Web conditions
@ConditionalOnWebApplication
@ConditionalOnNotWebApplication
@ConditionalOnWebApplication(type = Type.SERVLET)
@ConditionalOnWebApplication(type = Type.REACTIVE)

// Expression conditions
@ConditionalOnExpression("${feature.a.enabled} and ${feature.b.enabled}")

// Cloud platform
@ConditionalOnCloudPlatform(CloudPlatform.KUBERNETES)
```

## Ordering Auto-Configuration

```java
@AutoConfiguration(
    after = DataSourceAutoConfiguration.class,
    before = JpaRepositoriesAutoConfiguration.class
)
public class MyAutoConfiguration {
    // Runs after DataSource, before JPA repositories
}

// With @AutoConfigureOrder (for non-auto-config)
@Configuration
@AutoConfigureOrder(Ordered.HIGHEST_PRECEDENCE)
public class EarlyConfiguration {}
```

## Creating Starters

```
my-spring-boot-starter/
├── pom.xml
├── src/main/java/
│   └── com/example/autoconfigure/
│       ├── MyAutoConfiguration.java
│       └── MyProperties.java
└── src/main/resources/
    └── META-INF/
        ├── spring/
        │   └── org.springframework.boot.autoconfigure.AutoConfiguration.imports
        └── additional-spring-configuration-metadata.json
```

**AutoConfiguration.imports:**
```
com.example.autoconfigure.MyAutoConfiguration
```

**Configuration metadata (IDE support):**
```json
{
  "properties": [
    {
      "name": "my.service.enabled",
      "type": "java.lang.Boolean",
      "description": "Enable MyService auto-configuration.",
      "defaultValue": true
    },
    {
      "name": "my.service.timeout",
      "type": "java.time.Duration",
      "description": "Connection timeout.",
      "defaultValue": "30s"
    }
  ]
}
```

## Debugging Auto-Configuration

```yaml
# Enable debug logging
debug: true

# Or specific logging
logging:
  level:
    org.springframework.boot.autoconfigure: DEBUG
```

```bash
# Actuator endpoint
GET /actuator/conditions

# Shows:
# - positiveMatches: Conditions that matched
# - negativeMatches: Conditions that didn't match
# - unconditionalClasses: Auto-configs without conditions
```

## Disabling Auto-Configuration

```java
@SpringBootApplication(exclude = {
    DataSourceAutoConfiguration.class,
    HibernateJpaAutoConfiguration.class
})
public class Application {}

// Or via properties
spring.autoconfigure.exclude=\
  org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration
```
