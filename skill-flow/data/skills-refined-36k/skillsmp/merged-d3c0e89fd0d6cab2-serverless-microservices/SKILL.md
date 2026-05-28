---
name: serverless-microservices
description: Use this skill when developing scalable serverless architectures and microservices with FastAPI and Go, focusing on best practices for deployment, observability, and resilience.
---

# Serverless and Microservices Development

You are an expert in Python, FastAPI, Go, and serverless environments including AWS Lambda and Azure Functions.

## Core Principles

- Design services to be stateless; leverage external storage and caches (e.g., Redis) for maintaining state.
- Implement API gateways and reverse proxies like NGINX or Traefik for traffic management.
- Apply circuit breakers and retries for dependable service-to-service communication.
- Favor serverless deployment for reduced infrastructure overhead in scalable environments.
- Use asynchronous workers such as Celery or RQ for background tasks.

## Microservices Architecture

### FastAPI Microservices

- Integrate FastAPI with API gateways for rate limiting, request transformation, and security filtering.
- Maintain clear API separation aligned with microservices design.
- Employ message brokers like RabbitMQ or Kafka for event-driven systems.
- Optimize FastAPI for serverless deployment by minimizing cold starts and packaging applications as lightweight containers.

### Go Backend Development

- Follow Clean Architecture principles separating handlers, services, repositories, and domain models.
- Use interface-driven development with dependency injection.
- Implement explicit error handling with context wrapping and custom error types for domain-specific failures.

## Observability and Monitoring

- Use OpenTelemetry for distributed tracing and structured logging with ELK Stack integration.
- Monitor with Prometheus and Grafana, setting up alerting for critical metrics.
- Ensure correlation IDs propagate across service boundaries for effective tracing.

## Security Best Practices

- Implement OAuth2 for authentication and authorization.
- Apply rate limiting and DDoS protection measures.
- Enforce security headers (CORS, CSP) and validate all inputs at service boundaries.
- Use secrets management solutions (AWS Secrets Manager, Azure Key Vault).

## Performance Optimization

- Leverage FastAPI's async capabilities for concurrent connections and optimize for high throughput using read-optimized databases.
- Deploy caching layers (Redis, Memcached) and use load balancing and service mesh technologies like Istio.
- Minimize function package size for faster cold starts and implement connection pooling for database connections.

## Testing Strategies

- Write comprehensive unit tests for individual functions and integration tests for service interactions.
- Use contract testing for API boundaries and test locally with tools like SAM Local or LocalStack.
- Implement load testing for performance validation.

## Resilience and Error Handling

- Implement retries with exponential backoff and circuit breakers to prevent cascade failures.
- Design for graceful degradation and handle partial failures appropriately.
- Use dead letter queues for managing failed messages.

## Project Structure for Go Microservices

```
project/
  cmd/           # Application entry points
  internal/      # Private application code
  pkg/           # Public libraries
  api/           # API definitions (OpenAPI, protobuf)
  configs/       # Configuration files
  test/          # Additional test utilities
```