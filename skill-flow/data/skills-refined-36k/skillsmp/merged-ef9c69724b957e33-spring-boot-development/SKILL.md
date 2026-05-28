---
name: spring-boot-development
description: Use this skill for expert guidance in Spring Boot application development, focusing on best practices for RESTful APIs, security, testing, and deployment.
---

# Spring Boot Development

This skill provides comprehensive guidance for developing applications using Spring Boot, including best practices, design patterns, and essential features.

## Core Principles

- Write clean, efficient, and well-documented Java code using Spring Boot conventions.
- Use Spring Boot 3.x with Java 17+ features (e.g., records, sealed classes).
- Prefer constructor injection over field injection for better testability.
- Follow SOLID principles and RESTful API design patterns.
- Design applications suitable for microservices architecture.

## Project Structure

Organize code using the standard layered pattern:

```
project/
├── controllers/     # REST controllers
├── services/        # Business logic
├── repositories/    # Data access layer
├── models/          # Domain entities and DTOs
└── configurations/  # Spring configurations
```

## Spring Boot Specifics

- Leverage Spring Boot starters for rapid application development.
- Use auto-configuration effectively to minimize boilerplate.
- Implement proper annotations (`@SpringBootApplication`, `@RestController`, `@Service`, `@Repository`).
- Handle exceptions globally via `@ControllerAdvice` and `@ExceptionHandler`.

## REST API Design

- Use appropriate HTTP methods (GET, POST, PUT, DELETE, PATCH).
- Return proper HTTP status codes.
- Implement a consistent error response format.
- Use DTOs to control the API contract and version APIs when needed.

## Data Access

### Spring Data JPA

- Define proper entity relationships (`@OneToMany`, `@ManyToOne`, etc.).
- Use lazy loading appropriately to avoid N+1 queries.
- Implement pagination for large result sets.
- Use query methods and `@Query` for custom queries.

### Database Migrations

- Use Flyway or Liquibase for schema migrations.
- Version migration scripts properly and test them in development before production.

## Security

### Spring Security

- Implement authentication and authorization properly.
- Use BCrypt for password encoding and configure CORS appropriately.
- Protect endpoints based on roles/permissions and use HTTPS in production.

### Secure Coding

- Validate all user inputs and sanitize data to prevent injection attacks.
- Avoid exposing sensitive information in responses.

## Testing

### Unit Testing

- Use JUnit 5 for unit tests and mock dependencies with Mockito.
- Test business logic thoroughly following the Given-When-Then pattern.

### Integration Testing

- Use `@SpringBootTest` for integration tests and `MockMvc` for web layer testing.
- Test database operations with test containers and security configurations.

## Performance

### Caching

- Use Spring Cache abstraction and configure appropriate cache providers (e.g., Redis, Caffeine).
- Set proper TTL for cached data and implement cache eviction strategies.

### Async Processing

- Use `@Async` for non-blocking operations and configure thread pools appropriately.

## Logging and Monitoring

### Logging

- Use SLF4J with Logback for structured logging.
- Log at appropriate levels and include correlation IDs for tracing.

### Monitoring

- Use Spring Boot Actuator for health checks and metrics.
- Monitor application performance and export metrics to monitoring systems.

## API Documentation

- Use Springdoc OpenAPI for comprehensive API documentation.
- Document all endpoints with descriptions and keep documentation up to date with code.

## Best Practices

- Follow RESTful API design principles with proper HTTP methods and status codes.
- Maintain high cohesion within components and low coupling between them.
- Implement proper error handling with meaningful error responses.

## Resources

- Spring Boot Documentation: https://spring.io/projects/spring-boot
- Spring Framework: https://spring.io/projects/spring-framework
- Spring Data JPA: https://spring.io/projects/spring-data-jpa
- Spring Security: https://spring.io/projects/spring-security
- Baeldung: https://www.baeldung.com/