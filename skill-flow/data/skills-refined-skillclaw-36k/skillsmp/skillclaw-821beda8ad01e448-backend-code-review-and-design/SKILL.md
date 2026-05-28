---
name: backend-code-review-and-design
description: Use this skill when conducting comprehensive reviews of backend code and design, including API specifications, database architecture, and security assessments to identify vulnerabilities and performance issues.
---

# Backend Code and Design Review

Conduct thorough reviews of backend code and design to identify security vulnerabilities, performance bottlenecks, and architectural concerns. Produce actionable reports with specific findings and recommendations.

## Review Process

Follow this structured approach for comprehensive backend analysis:

### 1. Assess Technology Stack and Scope

Identify technologies and critical areas before starting:

**Technology Inventory:**

```
Backend Language: Node.js/Python/Java/Go/C#
Framework: Express/FastAPI/Spring Boot/Gin/ASP.NET
Database: PostgreSQL/MySQL/MongoDB/Redis
Architecture: Monolith/Microservices/Serverless
Deployment: AWS/GCP/Azure/Docker/Kubernetes
```

**Critical Review Areas (prioritize these):**

- Authentication and authorization logic
- Payment processing and financial transactions
- Data access layers (ORM queries, raw SQL)
- External API integrations and webhooks
- Background jobs and async processing
- File upload and download handlers

**Example Scope Definition:**

```
Review: User authentication service
Files: src/auth/*.ts (15 files, ~2000 lines)
Priority: High (handles user credentials and sessions)
Focus: Security vulnerabilities, JWT implementation, session management
```

### 2. Review Code Quality and Structure

Evaluate code organization, design patterns, and maintainability:

**Code Organization Checklist:**

```
☐ Proper layering (controllers → services → repositories → database)
☐ Consistent file and folder naming (kebab-case, camelCase, etc.)
☐ One class/function per file (or logically grouped)
☐ No circular dependencies between modules
☐ Clear separation of business logic and infrastructure code
```

### 3. API Design Review

- Evaluate RESTful resource modeling, HTTP method usage, status codes
- Review GraphQL schema design, type definitions, query patterns
- Assess gRPC service definitions and protobuf schemas
- Validate API versioning strategy and documentation
- Check authentication, authorization, and security measures

### 4. Database Design Validation

- Review data modeling, entity relationships, normalization
- Assess schema design, column types, constraints, indexes
- Evaluate query patterns and N+1 query prevention
- Check data integrity rules and referential integrity
- Review scalability approach (sharding, replicas, caching)

### 5. Architecture Assessment

- Evaluate service boundaries and decomposition
- Review communication patterns (sync/async, event-driven)
- Assess resilience patterns (circuit breakers, retries, timeouts)
- Check service discovery and load balancing design
- Validate data management and consistency strategies

### 6. Security Review

- Evaluate authentication mechanisms (OAuth 2.0, JWT)
- Review authorization model (RBAC, ABAC)
- Assess data protection measures and compliance with security standards

### 7. Reporting

Produce detailed review reports with:

- Severity-rated findings
- Actionable recommendations
- Architecture diagrams (if applicable)
- Implementation suggestions for identified issues