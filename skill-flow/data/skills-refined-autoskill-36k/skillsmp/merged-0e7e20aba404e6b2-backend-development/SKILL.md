---
name: backend-development
description: Use this skill when building robust backend systems with modern technologies, frameworks, and best practices for APIs, authentication, security, and performance optimization.
---

# Backend Development Skill

Production-ready backend development with modern technologies, best practices, and proven patterns.

## When to Use

- Designing RESTful, GraphQL, or gRPC APIs
- Building authentication/authorization systems
- Optimizing database queries and schemas
- Implementing caching and performance optimization
- Mitigating OWASP Top 10 security vulnerabilities
- Designing scalable microservices
- Testing strategies (unit, integration, E2E)
- Setting up CI/CD pipelines and deployment
- Monitoring and debugging production systems

## Technology Selection Guide

**Languages:** Node.js/TypeScript (full-stack), Python (data/ML), Go (concurrency), Rust (performance)  
**Frameworks:** NestJS, FastAPI, Django, Express, Gin  
**Databases:** PostgreSQL (ACID), MongoDB (flexible schema), Redis (caching)  
**APIs:** REST (simple), GraphQL (flexible), gRPC (performance)  

## Key Best Practices (2025)

**Security:** Use Argon2id for passwords, parameterized queries to prevent SQL injection, OAuth 2.1 with PKCE, implement rate limiting, and apply security headers.  
**Performance:** Utilize Redis caching, database indexing, and CDNs to enhance performance.  
**Testing:** Follow the 70-20-10 testing pyramid and employ contract testing for microservices.  
**DevOps:** Implement blue-green/canary deployments and feature flags for safer releases.

## Quick Decision Matrix

| Need | Choose |
|------|--------|
| Fast development | Node.js + NestJS |
| Data/ML integration | Python + FastAPI |
| High concurrency | Go + Gin |
| Max performance | Rust + Axum |
| ACID transactions | PostgreSQL |
| Flexible schema | MongoDB |
| Caching | Redis |
| Internal services | gRPC |
| Public APIs | GraphQL/REST |
| Real-time events | Kafka |

## Implementation Checklist

**API:** Choose style → Design schema → Validate input → Add auth → Rate limiting → Documentation → Error handling  
**Database:** Choose DB → Design schema → Create indexes → Connection pooling → Migration strategy → Backup/restore → Test performance  
**Security:** Address OWASP Top 10 → Use parameterized queries → Implement OAuth 2.1 + JWT → Apply security headers → Enforce rate limiting → Validate input  
**Testing:** Aim for Unit 70% → Integration 20% → E2E 10% → Conduct load tests → Perform migration tests → Execute contract tests (microservices)  
**Deployment:** Use Docker → Set up CI/CD → Implement blue-green/canary → Utilize feature flags → Ensure monitoring → Set up logging → Conduct health checks  

## Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OAuth 2.1: https://oauth.net/2.1/
- OpenTelemetry: https://opentelemetry.io/