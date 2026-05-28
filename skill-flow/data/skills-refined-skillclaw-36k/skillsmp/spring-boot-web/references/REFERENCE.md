# Spring Boot Web References

## References

- [**REST Controller Patterns**](rest-controller-patterns.md) - HATEOAS, async controllers, streaming
- [**Validation Patterns**](validation-patterns.md) - Custom validators, validation groups, cross-field
- [**Exception Handling**](exception-handling.md) - RFC 7807 ProblemDetail, error responses

## Quick Checks

- [ ] Use @RestController for REST APIs
- [ ] Validate input with @Valid on @RequestBody
- [ ] Use records for request/response DTOs
- [ ] Return proper HTTP status codes
- [ ] Global exception handling with @RestControllerAdvice
- [ ] Never expose JPA entities in API responses
- [ ] Version API endpoints (/api/v1/...)
