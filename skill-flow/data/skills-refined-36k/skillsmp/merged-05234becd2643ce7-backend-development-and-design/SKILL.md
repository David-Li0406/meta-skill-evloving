---
name: backend-development-and-design
description: Use this skill for designing and developing backend systems, including APIs, microservices, and database architectures.
---

# Backend Development and Design

## Workflow

Follow this systematic design and development process:

1. **Requirements Analysis**
   - Gather functional requirements (features, operations)
   - Define non-functional requirements (performance, scalability, availability)
   - Identify constraints (budget, timeline, technology, compliance)

2. **Architecture Selection**
   - Choose architecture pattern (monolith, microservices, serverless)
   - Select technology stack based on requirements
   - Define service boundaries and responsibilities

3. **API Design**
   - Design RESTful endpoints with proper resource modeling
   - Define request/response schemas and contracts
   - Plan versioning strategy and documentation
   - Ensure consistent error responses and proper HTTP methods

4. **Database Design**
   - Model entities and relationships
   - Design schema with normalization (3NF default)
   - Plan indexing and migration strategies
   - Implement connection pooling

5. **Security Design**
   - Design authentication flow (OAuth 2.0, JWT)
   - Plan authorization model (RBAC, ABAC)
   - Define data encryption and protection strategy
   - Implement input validation and SQL injection prevention

6. **Scalability & Performance**
   - Design caching strategy (Redis, CDN)
   - Plan load balancing and auto-scaling
   - Define asynchronous processing with message queues

7. **Documentation**
   - Create API specifications (OpenAPI/Swagger)
   - Document architecture decisions with diagrams
   - Provide implementation guidelines and roadmap

## Output Structure

Present your backend design with these sections:

1. **System Overview** - High-level architecture, components, technology stack
2. **API Specification** - Endpoints, schemas, authentication, OpenAPI docs
3. **Database Design** - ERD, schema, indexes, migration plan
4. **Architecture Decisions** - Service decomposition, communication patterns, consistency model
5. **Security Implementation** - Authentication/authorization flows, encryption
6. **Scalability Plan** - Load balancing, caching, database scaling, auto-scaling
7. **Deployment Architecture** - Containers, infrastructure, CI/CD, monitoring
8. **Implementation Roadmap** - Phases, milestones, dependencies, risks

## Core Principles

- **API-first approach** - Design and document APIs before implementation
- **Security by design** - Build authentication, authorization, and encryption from the start
- **Design for scalability** - Plan for growth with caching, load balancing, and horizontal scaling
- **Plan for failure** - Include error handling, retries, circuit breakers, and graceful degradation
- **Document thoroughly** - Create clear API specs, architecture diagrams, and implementation guides

## API Response Template

```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "total": 100
  },
  "errors": null
}
```

## Error Response Template

```json
{
  "data": null,
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "Email is required",
      "field": "email"
    }
  ]
}
```

## Reliability Targets

- Uptime: 99.9%
- Error rate: <0.1%
- Response time: <200ms p95

## Examples

**Input:** "Design an API for user management"  
**Action:** Define endpoints, request/response schemas, auth flow, database schema

**Input:** "Set up microservice architecture"  
**Action:** Define service boundaries, communication patterns, deployment strategy