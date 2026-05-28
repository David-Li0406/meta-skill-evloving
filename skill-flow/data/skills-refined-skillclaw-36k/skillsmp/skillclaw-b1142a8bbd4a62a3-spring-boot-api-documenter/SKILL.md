---
name: spring-boot-api-documenter
description: Use this skill to auto-generate OpenAPI 3 documentation for Spring Boot REST APIs, adapting to changes in API endpoints, controllers, or user requests for API documentation.
---

# Spring Boot API Documenter Skill

This skill auto-generates OpenAPI 3 documentation for Spring Boot REST APIs using the SpringDoc OpenAPI library.

## When to Use

Use this skill when you need to:
- Automatically generate OpenAPI specifications for REST APIs in Spring Boot applications.
- Document changes in API endpoints, controllers, or request/response DTOs.
- Respond to user requests for API documentation, Swagger, or OpenAPI.
- Configure documentation for security requirements and error responses.

## What It Generates

### OpenAPI 3.0/3.1 Specifications
- Endpoint descriptions from annotations and Javadoc.
- Request/response schemas.
- Authentication/security requirements.
- Example payloads.
- Error responses via @ControllerAdvice.
- Grouped API definitions.

### Spring Boot Integration
- Dependency configuration for SpringDoc OpenAPI.
- Swagger UI setup.
- application.properties/yml configuration.
- Security scheme definitions.
- GroupedOpenApi bean configurations.

## Quick Start

### Requirements
- **Spring Boot**: 3.0.0 or higher (for Spring Boot 3.x) or 4.0.0 or higher (for Spring Boot 4.x).
- **Java**: 17 or higher.

### Adding SpringDoc OpenAPI to Spring Boot

**Maven (WebMvc with Swagger UI):**

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.8.14</version> <!-- For Spring Boot 3.x -->
    <!-- or -->
    <version>3.0.0</version> <!-- For Spring Boot 4.x -->
</dependency>
```

**Maven (WebFlux with Swagger UI):**

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webflux-ui</artifactId>
    <version>2.8.14</version> <!-- For Spring Boot 3.x -->
    <!-- or -->
    <version>3.0.0</version> <!-- For Spring Boot 4.x -->
</dependency>
```

**Gradle (WebMvc with Swagger UI):**

```groovy
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.8.14' // For Spring Boot 3.x
// or
implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:3.0.0' // For Spring Boot 4.x
```

**Gradle (WebFlux with Swagger UI):**

```groovy
implementation 'org.springdoc:springdoc-openapi-starter-webflux-ui:2.8.14' // For Spring Boot 3.x
// or
implementation 'org.springdoc:springdoc-openapi-starter-webflux-ui:3.0.0' // For Spring Boot 4.x
```

### Default URLs After Setup

- **Swagger UI**: `http://localhost:8080/swagger-ui.html`
- **OpenAPI JSON**: `http://localhost:8080/v3/api-docs`
- **OpenAPI YAML**: `http://localhost:8080/v3/api-docs.yaml`