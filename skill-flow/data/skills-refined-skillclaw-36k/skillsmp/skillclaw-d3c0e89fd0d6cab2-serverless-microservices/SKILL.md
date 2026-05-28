---
name: serverless-microservices
description: Use this skill when developing scalable serverless microservices with FastAPI and Go, focusing on best practices for architecture, observability, and security.
---

# Serverless Microservices Development

You are an expert in building serverless microservices using FastAPI/Python and Go, leveraging cloud-native patterns and best practices.

## Core Principles

- Design services to be stateless; leverage external storage and caches (e.g., Redis) for maintaining state.
- Implement API gateways and reverse proxies like NGINX, Traefik, or Kong for traffic management.
- Apply circuit breakers and retries for dependable service-to-service communication.
- Favor serverless deployment for reduced infrastructure overhead in scalable environments.
- Use asynchronous workers such as Celery or RQ for background tasks.

## FastAPI Microservices

### Asynchronous Processing
- Handle asynchronous tasks with Celery or RQ.
- Implement proper task queuing and worker management.
- Design for eventual consistency in distributed systems.

### Observability
- Use OpenTelemetry for distributed tracing.
- Implement structured logging with ELK Stack integration.
- Set up Prometheus and Grafana for monitoring and alerting.
- Ensure correlation IDs propagate across service boundaries.

### Security
- Implement OAuth2 for authentication and authorization.
- Apply rate limiting and DDoS protection.
- Validate all inputs at service boundaries.
- Use secrets management (AWS Secrets Manager, Azure Key Vault).

## Go Backend Development for Microservices

### Architecture
- Follow Clean Architecture pattern separating handlers, services, repositories, and domain models.
- Apply domain-driven design principles.
- Use interface-driven development with dependency injection.

### Project Structure
```
project/
  cmd/           # Application entry points
  internal/      # Private application code
  pkg/           # Public libraries
  api/           # API definitions (OpenAPI, protobuf)
  configs/       # Configuration files
  test/          # Additional test utilities
```

### Error Handling
- Use explicit error handling with context wrapping.
- Return errors with sufficient context for debugging.
- Implement custom error types for domain-specific failures.

### Concurrency
- Manage goroutines safely with proper lifecycle management.
- Propagate context through all function calls.
- Use channels appropriately for communication.

### Testing
- Write comprehensive unit tests with table-driven patterns.
- Use mocks for external dependencies.
- Separate fast unit tests from integration tests.
- Implement end-to-end tests for comprehensive coverage.

## Performance Optimization

- Optimize FastAPI for AWS Lambda and Azure Functions by minimizing cold starts.
- Package applications as lightweight containers or standalone binaries.
- Use managed databases (DynamoDB, Cosmos DB, Aurora Serverless).
- Implement automatic scaling for variable workloads.
- Design for idempotency to handle retries safely.

## Monitoring and Observability

- Monitor with Prometheus and Grafana.
- Implement structured logging practices.
- Integrate centralized logging solutions for better traceability.