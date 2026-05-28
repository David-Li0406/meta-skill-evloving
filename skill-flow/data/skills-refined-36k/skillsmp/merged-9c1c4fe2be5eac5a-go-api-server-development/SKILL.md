---
name: go-api-server-development
description: Use this skill for building robust HTTP services and REST APIs in Golang, following best practices for design, error handling, and security.
---

# Go API Server Development Standards

## **Priority: P0 (CRITICAL)**

## Core Principles

- Always use the latest stable version of Go (1.22 or newer) and be familiar with RESTful API design principles and the `net/http` package.
- Follow user requirements carefully and describe the API structure, endpoints, and data flow in detail.
- Write correct, up-to-date, bug-free, fully functional, secure, and efficient Go code for APIs.
- Prioritize security, scalability, and maintainability in your API designs.

## Router Selection

- **Standard Lib (`net/http`)**: Use for simple services or when zero dependencies are required. Utilize `http.ServeMux` for routing.
- **Echo (`labstack/echo`)**: Recommended for production REST APIs with excellent middleware support.
- **Gin (`gin-gonic/gin`)**: High-performance alternative.

## API Development Guidelines

### Routing and HTTP Handling

- Implement proper HTTP method handling (GET, POST, PUT, DELETE, PATCH).
- Use appropriate HTTP status codes for responses and enforce `application/json` for REST APIs.
- Implement input validation for request bodies, query parameters, and path parameters.

### Error Handling

- Implement structured error responses in JSON format and log errors appropriately for debugging and monitoring.

### JSON Handling

- Use `encoding/json` for JSON serialization/deserialization and handle parsing errors gracefully.

### Concurrency

- Leverage Go's built-in concurrency features and use goroutines for concurrent operations where beneficial.

### Middleware

- Implement middleware for cross-cutting concerns (logging, authentication, rate limiting) and use middleware chaining for composable request processing.
- Always include `/health` and `/ready` endpoints.

### Security

- Implement authentication and authorization where appropriate, use HTTPS in production, and validate/sanitize all user inputs.

### Logging

- Use standard library logging with structured output and avoid logging sensitive information.

### Testing

- Write unit tests for handlers and business logic, and implement integration tests for API endpoints.

## Anti-Patterns

- **Business Logic in Handlers**: Handlers should only parse requests, call services, and format responses.
- **Global Router**: Avoid using global router variables; pass router instances instead.

## References

- [Middleware Patterns](references/middleware-patterns.md)
- [Graceful Shutdown](references/graceful-shutdown.md)