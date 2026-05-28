---
name: backend-review
description: Use this skill when conducting comprehensive reviews of backend systems, including code quality, design architecture, API specifications, database structures, and security assessments.
---

# Backend Review

Conduct systematic reviews of backend systems to identify design flaws, security vulnerabilities, performance bottlenecks, and scalability issues. Produce actionable reports with specific findings, severity ratings, and implementation recommendations.

## Review Process

Follow this structured approach for comprehensive backend analysis:

### 1. Pre-Review Preparation

- Gather design documentation (architecture diagrams, API specs, database schemas).
- Understand requirements (functional, non-functional, compliance).
- Define review scope and priorities.
- Identify constraints (technology, budget, timeline).

### 2. Assess Technology Stack and Scope

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

### 3. Review Code Quality and Structure

Evaluate code organization, design patterns, and maintainability:

**Code Organization Checklist:**

```
☐ Proper layering (controllers → services → repositories → database)
☐ Consistent file and folder naming (kebab-case, camelCase, etc.)
☐ One class/function per file (or logically grouped)
☐ No circular dependencies between modules
☐ Clear separation of business logic and infrastructure code
```

**SOLID Principles Validation:**

- **Single Responsibility:** Each class/module has one reason to change.
- **Dependency Injection:** Dependencies injected, not hardcoded.
- **Error Handling Pattern:** Ensure proper error handling is implemented.

**Code Quality Issues to Flag:**

- Functions > 50 lines (should be split).
- Classes > 300 lines (too many responsibilities).
- Cyclomatic complexity > 10 (simplify logic).
- Code duplication > 5 lines (extract to function).
- Missing type definitions (TypeScript, type hints).
- Magic numbers (use named constants).

### 4. Validate API Design

Review API endpoints for REST, GraphQL, or gRPC implementations:

**REST API Review:**

- Evaluate resource modeling, HTTP method usage, and status codes.
- Check authentication, authorization, and security measures.

**GraphQL Review:**

- Assess schema design, type definitions, and query patterns.

**gRPC Review:**

- Validate service definitions and protobuf schemas.

### 5. Analyze Database Queries and Schema

Review database patterns, query optimization, and data integrity:

**SQL Injection Prevention:**

- Ensure parameterized queries are used to prevent vulnerabilities.

**N+1 Query Problem:**

- Optimize queries to avoid N+1 issues.

**Missing Indexes:**

- Recommend adding indexes for common queries.

### 6. Audit Security Vulnerabilities

Identify authentication, authorization, and data protection issues:

**Authentication Security:**

- Ensure strong password hashing and secure JWT configurations.

**Authorization Validation:**

- Check for proper authorization checks in sensitive operations.

**Input Validation:**

- Validate user inputs to prevent injection attacks.

### 7. Performance & Scalability

Assess caching strategies, database indexing, and scaling approaches:

- Review caching strategy (layers, invalidation, TTL).
- Evaluate horizontal/vertical scaling approach.

### 8. Report Generation

Categorize findings by severity (Critical, High, Medium, Low) and document detailed findings with examples. Provide specific, actionable recommendations and create architecture improvement diagrams.

## Severity Levels

Use these severity ratings for findings:

- **🔴 Critical**: Must fix before implementation.
- **🟠 High**: Should fix before go-live.
- **🟡 Medium**: Address in next iteration.
- **🟢 Low**: Track for future improvements.

## Report Structure

Present backend review findings with:

1. **Executive Summary** - Project context, review date, overall assessment.
2. **Review Scope** - What was reviewed, depth of review, focus areas.
3. **Key Findings Summary** - Overview of critical and high severity issues.
4. **Detailed Findings** - Each finding with severity, description, impact, recommendations, examples.
5. **Positive Observations** - Strengths and good design decisions.
6. **Recommendations** - Prioritized improvements with implementation guidance.
7. **Architecture Diagrams** - Current state and proposed improvements.
8. **Action Items** - Specific tasks with owners, deadlines, and status tracking.
9. **Next Steps** - Immediate actions, short-term tasks, follow-up review schedule.