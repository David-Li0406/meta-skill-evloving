---
name: spring-boot-development
description: Use this skill when you need expert guidance on developing applications with Spring Boot, including best practices for REST APIs, security, and microservices architecture.
---

# Skill body

## Core Principles

- Write clean, efficient, and well-documented Java code using Spring Boot conventions.
- Follow SOLID principles and RESTful API design patterns.
- Design applications for microservices architecture suitability.

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

## Spring Boot Fundamentals

- Utilize Spring Boot starters for rapid application development.
- Implement proper use of annotations (@SpringBootApplication, @RestController, @Service).
- Leverage Spring Boot's auto-configuration capabilities.
- Handle exceptions gracefully via @ControllerAdvice and @ExceptionHandler.

## Dependency Injection

- Prefer constructor injection over field injection for better testability.
- Use `@RequiredArgsConstructor` with Lombok for cleaner code.
- Keep constructors simple and avoid logic in them.

## REST API Design

- Use appropriate HTTP methods (GET, POST, PUT, DELETE, PATCH).
- Return proper HTTP status codes.
- Implement consistent error response formats.
- Use DTOs to control API contracts.
- Version APIs when needed.

## Data Access

### Spring Data JPA

- Define proper entity relationships (@OneToMany, @ManyToOne, etc.).
- Use lazy loading appropriately to avoid N+1 queries.
- Implement pagination for large result sets.
- Use query methods and @Query for custom queries.

### Database Migrations

- Use Flyway or Liquibase for schema migrations.
- Version migration scripts properly.
- Test migrations in development before production.

## Security

### Spring Security

- Implement authentication and authorization properly.
- Use BCrypt for password encoding.
- Configure CORS appropriately.
- Protect endpoints based on roles/permissions.

### Secure Coding

- Validate all user inputs.
- Sanitize data to prevent injection attacks.
- Avoid exposing sensitive information in responses.

## Testing

### Unit Testing

- Write comprehensive unit tests using JUnit 5 and Spring Boot Test.
- Mock dependencies with Mockito.
- Test business logic thoroughly.

### Integration Testing

- Use @SpringBootTest for integration tests.
- Use MockMvc for testing web layer components.

## Performance and Scalability

- Implement caching strategies using Spring Cache abstraction.
- Use @Async for asynchronous, non-blocking operations when appropriate.
- Optimize database queries using proper indexing and fetch strategies.

## Logging and Monitoring

- Use SLF4J with Logback for logging.
- Implement appropriate log levels (ERROR, WARN, INFO, DEBUG).
- Leverage Spring Boot Actuator for application monitoring and metrics.