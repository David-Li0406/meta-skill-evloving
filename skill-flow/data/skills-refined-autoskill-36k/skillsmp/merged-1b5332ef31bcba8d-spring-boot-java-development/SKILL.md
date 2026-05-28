---
name: spring-boot-java-development
description: Use this skill for expert guidance in Spring Boot and Java development, focusing on best practices for RESTful APIs, security, testing, and microservices architecture.
---

# Spring Boot and Java Development

You are an expert in Java programming, Spring Boot, Spring Framework, REST APIs, JPA, and microservices. This skill provides comprehensive guidelines and best practices for building robust, secure, and maintainable enterprise applications.

## Core Principles

- Write clean, efficient, and well-documented Java code using Spring Boot conventions.
- Follow SOLID principles and RESTful API design patterns.
- Prefer constructor injection over field injection for better testability.

## Project Structure

Organize code using the standard layered architecture:

```
project/
├── controllers/     # REST controllers
├── services/        # Business logic
├── repositories/    # Data access layer
├── models/          # Domain entities and DTOs
└── configurations/  # Spring configurations
```

## Spring Boot Fundamentals

- Utilize Spring Boot starters for rapid application development.
- Implement proper use of annotations (@SpringBootApplication, @RestController, @Service).
- Handle exceptions globally via @ControllerAdvice and @ExceptionHandler.

## REST API Design

- Use appropriate HTTP methods (GET, POST, PUT, DELETE).
- Return proper HTTP status codes.
- Implement consistent error response formats.
- Use DTOs to control API contracts and version APIs when needed.

## Data Access with Spring Data JPA

- Define proper entity relationships (@OneToMany, @ManyToOne).
- Use lazy loading appropriately to avoid N+1 queries.
- Implement pagination for large result sets.

## Security Best Practices

- Implement Spring Security for authentication and authorization.
- Use BCrypt for password encoding.
- Validate all user inputs to prevent injection attacks.

## Testing Guidelines

### Unit Testing

- Write comprehensive unit tests using JUnit 5 and Mockito.
- Mock dependencies and test business logic thoroughly.

### Integration Testing

- Use @SpringBootTest for integration tests.
- Test REST endpoints with MockMvc.

## Performance Optimization

- Implement caching strategies using Spring Cache abstraction.
- Use @Async for non-blocking operations when appropriate.
- Optimize database queries using proper indexing and fetch strategies.

## Logging and Monitoring

- Use SLF4J with Logback for structured logging.
- Leverage Spring Boot Actuator for health checks and metrics.

## API Documentation

- Use Springdoc OpenAPI for comprehensive API documentation.
- Provide detailed annotations for endpoints, parameters, and responses.

## Build and Deployment

- Use Maven or Gradle for dependency management and builds.
- Implement multi-stage Docker builds for optimized container images.
- Configure CI/CD pipelines for automated testing and deployment.

## General Best Practices

- Follow RESTful API design principles with proper HTTP methods and status codes.
- Design for microservices architecture when appropriate.
- Maintain high cohesion within components and low coupling between them.

## Anti-Patterns to Avoid

- Field injection
- Business logic in controllers
- No exception handling
- Exposing entities directly
- Hardcoded configuration

## Resources

- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Spring Framework](https://spring.io/projects/spring-framework)
- [Spring Data JPA](https://spring.io/projects/spring-data-jpa)
- [Spring Security](https://spring.io/projects/spring-security)
- [Baeldung](https://www.baeldung.com/)