---
name: Micronaut Reactive
description: Reactive types, HTTP clients, and non-blocking patterns.
metadata:
  labels: [java, micronaut, reactive]
  triggers:
    files: ['**/*.java']
    keywords: [Flux, Mono, Reactive, HttpClient, '@Client', Publisher, Flowable]
---

# Micronaut Reactive Standards

## Reactive Controllers

```java
@Controller("/users")
public class UserController {

    @Get("/{id}")
    public Mono<User> findById(Long id) {
        return userService.findById(id);
    }

    @Get(produces = MediaType.TEXT_EVENT_STREAM)
    public Flux<User> stream() {
        return userService.streamAll();
    }
}
```

## Declarative HTTP Client

```java
@Client("order-service")
public interface OrderClient {

    @Get("/orders/{userId}")
    Flux<Order> getOrders(Long userId);

    @Post("/orders")
    Mono<Order> createOrder(@Body CreateOrderRequest request);
}
```

## Low-Level Client

```java
@Singleton
public class ExternalApiService {

    private final HttpClient httpClient;

    public ExternalApiService(@Client("https://api.external.com") HttpClient httpClient) {
        this.httpClient = httpClient;
    }

    public Mono<ExternalData> fetchData(String id) {
        return Mono.from(httpClient.retrieve(
            HttpRequest.GET("/data/" + id),
            ExternalData.class
        ));
    }
}
```

## References

- [HTTP Client Patterns](references/http-client-patterns.md) - Retry, fallback, timeout
