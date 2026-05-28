# Spring Cloud References

## References

- [**Service Discovery**](service-discovery.md) - Eureka, Consul, Kubernetes
- [**Circuit Breaker**](circuit-breaker.md) - Resilience4j patterns

## Quick Checks

- [ ] Use Resilience4j (not Hystrix - deprecated)
- [ ] Configure fallbacks for all external calls
- [ ] Set appropriate circuit breaker thresholds
- [ ] Use FeignClient for declarative HTTP clients
