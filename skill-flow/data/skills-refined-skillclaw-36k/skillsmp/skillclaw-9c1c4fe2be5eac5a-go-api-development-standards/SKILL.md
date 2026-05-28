---
name: go-api-development-standards
description: Use this skill when developing RESTful APIs in Go, focusing on best practices for structure, error handling, and security.
---

# Go API Development Standards

## Core Principles

- Always use the latest stable version of Go (1.22 or newer) and be familiar with RESTful API design principles and the `net/http` package.
- Follow user requirements carefully and to the letter.
- Plan the API structure, endpoints, and data flow in detail before implementation.
- Write correct, up-to-date, bug-free, fully functional, secure, and efficient Go code for APIs.
- Prioritize security, scalability, and maintainability in your API designs.

## Routing and HTTP Handling

- Use `http.ServeMux` for routing.
- Implement proper HTTP method handling (GET, POST, PUT, DELETE, PATCH).
- Use appropriate HTTP status codes for responses.
- Enforce `application/json` as the content type for REST APIs.

## Error Handling

- Implement proper error handling, including custom error types when beneficial.
- Return appropriate HTTP status codes with error responses.
- Use structured error responses in JSON format.
- Log errors appropriately for debugging and monitoring.

## Input Validation

- Implement input validation for API endpoints.
- Validate request bodies, query parameters, and path parameters.
- Return clear validation error messages to clients.
- Sanitize inputs to prevent injection attacks.

## JSON Handling

- Use `encoding/json` for JSON serialization/deserialization.
- Implement proper struct tags for JSON field mapping.
- Handle JSON parsing errors gracefully.

## Middleware

- Use middleware for cross-cutting concerns (logging, authentication, rate limiting).
- Implement middleware chaining for composable request processing.
- Include CORS handling where needed.
- Add request/response logging middleware.

## Concurrency

- Leverage Go's built-in concurrency features for API performance.
- Use goroutines for concurrent operations where beneficial.
- Implement proper synchronization for shared state.
- Use context for request cancellation and timeouts.

## Anti-Patterns

- Avoid placing business logic in handlers; handlers should only parse requests, call services, and format responses.
- Do not use global router variables; pass router instances instead.

## Health Checks

- Always include `/health` and `/ready` endpoints to monitor service status.