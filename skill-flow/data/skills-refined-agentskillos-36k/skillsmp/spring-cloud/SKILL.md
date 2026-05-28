---
name: Spring Cloud
description: Service discovery, configuration, circuit breakers, load balancing, and API gateway.
metadata:
  labels: [java, spring-boot, cloud, microservices]
  triggers:
    files: ['bootstrap.yml', 'application.yml', '**/*Discovery*.java', '**/*Client*.java']
    keywords: [SpringCloud, DiscoveryClient, CircuitBreaker, Resilience4j, FeignClient, Gateway, LoadBalancer]
---

# Spring Cloud Standards

## Service Discovery (Eureka)

```java
// Discovery Server
@SpringBootApplication
@EnableEurekaServer
public class DiscoveryServerApplication {}

// Client registration
@SpringBootApplication
@EnableDiscoveryClient
public class UserServiceApplication {}
```

```yaml
# Client configuration
spring:
  application:
    name: user-service
eureka:
  client:
    service-url:
      defaultZone: http://localhost:8761/eureka
  instance:
    prefer-ip-address: true
```

## Feign Client

```java
@FeignClient(
    name = "order-service",
    fallbackFactory = OrderClientFallbackFactory.class
)
public interface OrderClient {

    @GetMapping("/api/orders/{userId}")
    List<Order> getOrdersByUser(@PathVariable Long userId);

    @PostMapping("/api/orders")
    Order createOrder(@RequestBody CreateOrderRequest request);
}

@Component
public class OrderClientFallbackFactory implements FallbackFactory<OrderClient> {
    @Override
    public OrderClient create(Throwable cause) {
        return new OrderClient() {
            @Override
            public List<Order> getOrdersByUser(Long userId) {
                log.warn("Fallback: returning empty orders", cause);
                return List.of();
            }
            // ...
        };
    }
}
```

## Circuit Breaker (Resilience4j)

```java
@Service
public class PaymentService {

    @CircuitBreaker(name = "payment", fallbackMethod = "fallback")
    @Retry(name = "payment")
    @TimeLimiter(name = "payment")
    public CompletableFuture<PaymentResult> process(Payment payment) {
        return CompletableFuture.supplyAsync(() -> paymentGateway.process(payment));
    }

    public CompletableFuture<PaymentResult> fallback(Payment payment, Throwable t) {
        return CompletableFuture.completedFuture(PaymentResult.pending());
    }
}
```

```yaml
resilience4j:
  circuitbreaker:
    instances:
      payment:
        sliding-window-size: 10
        failure-rate-threshold: 50
        wait-duration-in-open-state: 30s
  retry:
    instances:
      payment:
        max-attempts: 3
        wait-duration: 500ms
```

## References

- [Service Discovery](references/service-discovery.md) - Eureka, Consul patterns
- [Circuit Breaker](references/circuit-breaker.md) - Resilience4j configuration
