---
name: backend-development
description: Use this skill when designing backend systems, including APIs, microservices, and database architectures, to ensure scalability, reliability, and maintainability.
---

# Backend Development

## Workflow

Follow this systematic design process:

1. **Requirements Analysis**
   - Gather functional requirements (features, operations).
   - Define non-functional requirements (performance, scalability, availability).
   - Identify constraints (budget, timeline, technology, compliance).

2. **Architecture Selection**
   - Choose architecture pattern (monolith, microservices, serverless).
   - Select technology stack based on requirements.
   - Define service boundaries and responsibilities.

3. **API Design**
   - Design RESTful endpoints with proper resource modeling.
   - Define request/response schemas and contracts.
   - Plan versioning strategy and documentation.
   - Ensure consistent error responses and proper HTTP methods.

4. **Database Design**
   - Model entities and relationships.
   - Design schema with normalization and appropriate indexing.
   - Plan migration strategy and connection pooling.

5. **Security Design**
   - Design authentication flow (OAuth 2.0, JWT).
   - Plan authorization model (RBAC, ABAC).
   - Define data encryption and protection strategy.

6. **Scalability & Performance**
   - Design caching strategy (Redis, CDN).
   - Plan load balancing and auto-scaling.
   - Define asynchronous processing with message queues.

7. **Documentation**
   - Create API specifications (OpenAPI/Swagger).
   - Document architecture decisions and provide implementation guidelines.

## Output Structure

Present your backend design with these sections:

1. **System Overview** - High-level architecture, components, technology stack.
2. **API Specification** - Endpoints, schemas, authentication, OpenAPI docs.
3. **Database Design** - ERD, schema, indexes, migration plan.
4. **Architecture Decisions** - Service decomposition, communication patterns, consistency model.
5. **Security Implementation** - Authentication and authorization strategies.

## API Response Template

```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100
    }
  },
  "errors": null
}
```

## Error Response Template

```json
{
  "success": false,
  "data": null,
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "Invalid input",
      "field": "email"
    }
  ]
}
```