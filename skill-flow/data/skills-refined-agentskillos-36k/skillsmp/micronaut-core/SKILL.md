---
name: Micronaut Core
description: Compile-time dependency injection, configuration, AOP, and startup optimization.
metadata:
  labels: [java, micronaut, di, aot]
  triggers:
    files: ['**/*.java', 'application.yml', 'application.properties']
    keywords: [Micronaut, '@Inject', '@Singleton', '@ConfigurationProperties', '@Factory', '@Controller']
---

# Micronaut Core Standards

## Compile-Time DI

```java
@Singleton
public class UserService {

    private final UserRepository repository;
    private final EventPublisher eventPublisher;

    // Constructor injection (preferred)
    public UserService(UserRepository repository, EventPublisher eventPublisher) {
        this.repository = repository;
        this.eventPublisher = eventPublisher;
    }
}

// Factory beans
@Factory
public class ClientFactory {

    @Singleton
    @Named("primary")
    public HttpClient primaryClient() {
        return HttpClient.create(URI.create("https://api.primary.com"));
    }

    @Singleton
    @Named("fallback")
    public HttpClient fallbackClient() {
        return HttpClient.create(URI.create("https://api.fallback.com"));
    }
}
```

## Configuration

```java
@ConfigurationProperties("app")
public record AppConfig(
    String name,
    int maxConnections,
    DatabaseConfig database
) {
    public record DatabaseConfig(
        String url,
        String username
    ) {}
}
```

```yaml
app:
  name: MyMicronautApp
  max-connections: 100
  database:
    url: jdbc:postgresql://localhost/db
    username: admin
```

## Controllers

```java
@Controller("/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @Get("/{id}")
    public User findById(Long id) {
        return userService.findById(id);
    }

    @Post
    @Status(HttpStatus.CREATED)
    public User create(@Valid @Body CreateUserRequest request) {
        return userService.create(request);
    }
}
```

## References

- [Compile-Time DI](references/compile-time-di.md) - AOT benefits, introspection
