---
name: Quarkus Core
description: CDI dependency injection, configuration, dev mode, and extensions.
metadata:
  labels: [java, quarkus, di, configuration]
  triggers:
    files: ['**/*.java', 'application.properties', 'pom.xml']
    keywords: [Quarkus, '@Inject', '@ApplicationScoped', '@ConfigProperty', Arc, QuarkusApplication]
---

# Quarkus Core Standards

## CDI (ArC) Dependency Injection

```java
@ApplicationScoped
public class UserService {

    @Inject
    UserRepository userRepository;

    @Inject
    @ConfigProperty(name = "app.max-users", defaultValue = "1000")
    int maxUsers;

    public User findById(Long id) {
        return userRepository.findById(id);
    }
}

// Bean scopes
@ApplicationScoped  // Single instance per application
@RequestScoped      // Per HTTP request
@Singleton          // Like ApplicationScoped but not proxied
@Dependent          // New instance each injection
```

## Configuration

```java
@ConfigMapping(prefix = "app")
public interface AppConfig {
    String name();
    int maxConnections();
    Optional<String> description();
    DatabaseConfig database();

    interface DatabaseConfig {
        String url();
        String username();
    }
}

// Usage
@Inject
AppConfig config;
```

```properties
# application.properties
app.name=MyApp
app.max-connections=100
app.database.url=jdbc:postgresql://localhost/db
app.database.username=admin

# Profile-specific
%dev.app.database.url=jdbc:h2:mem:test
%prod.app.database.url=${DB_URL}
```

## Dev Mode

```bash
# Live reload
./mvnw quarkus:dev

# Continuous testing
./mvnw quarkus:dev -Dquarkus.test.continuous-testing=enabled

# Dev UI at http://localhost:8080/q/dev
```

## References

- [CDI Patterns](references/cdi-patterns.md) - Producers, qualifiers, interceptors
