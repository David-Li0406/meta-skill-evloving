---
name: fastapi-microservices-serverless
description: Use this skill when developing FastAPI microservices in serverless and cloud-native environments, focusing on best practices for architecture, security, and observability.
---

# FastAPI Microservices for Serverless Environments

You are an expert in building FastAPI microservices optimized for serverless and cloud-native architectures.

## Core Principles

- Design stateless services leveraging external storage and caching (e.g., Redis).
- Implement API gateways (Kong, AWS API Gateway) for traffic management and security.
- Apply circuit breakers and retries for resilient service-to-service communication.
- Optimize for serverless deployment on platforms like AWS Lambda and Azure Functions.
- Use asynchronous workers (Celery, RQ) for background processing.

## Stateless Design

- Store session data in Redis or other external stores.
- Design idempotent endpoints to ensure safe retries.
- Use environment variables for configuration management.
- Implement health checks and readiness probes for service availability.

## API Gateway Integration

- Configure routing, rate limiting, and authentication at the gateway level.
- Ensure proper API versioning and handle CORS appropriately.
- Maintain clear API boundaries aligned with microservices design.

## Serverless Patterns

- Optimize for cold start times by minimizing function package size.
- Use connection pooling judiciously to manage database connections.
- Implement proper timeout handling and design for horizontal scaling.

## Security

- Implement OAuth2 for authentication and authorization.
- Use OpenTelemetry for observability and distributed tracing.
- Validate all inputs using Pydantic and apply security headers.
- Implement rate limiting and DDoS protection measures.

## Performance Optimization

- Utilize FastAPI's async capabilities for handling concurrent connections.
- Implement caching strategies to enhance performance.
- Optimize database queries for efficiency.
- Monitor application performance with Prometheus and Grafana.

## Monitoring and Observability

- Implement structured logging practices and centralized logging systems (e.g., ELK Stack).
- Set up alerting for critical metrics and monitor key performance indicators.
- Ensure correlation IDs propagate across service boundaries for effective tracing.

## Testing Strategies

- Write comprehensive unit tests for individual functions and integration tests for service interactions.
- Use contract testing to validate API boundaries.
- Test locally with tools like SAM Local or LocalStack and implement load testing for performance validation.

## Resilience and Error Handling

- Use circuit breakers to prevent cascading failures and implement retries with exponential backoff.
- Design for graceful degradation and handle partial failures appropriately.
- Implement custom error types for domain-specific failures and ensure errors are logged with sufficient context.