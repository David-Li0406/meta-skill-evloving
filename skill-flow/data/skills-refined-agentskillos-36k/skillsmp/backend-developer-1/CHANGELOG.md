# Changelog

All notable changes to the backend-developer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-12-29

### Removed

- **BREAKING**: Extracted DevOps domain to standalone `devops` skill (ADR-007)
  - `cicd` agent → `devops/cicd/github-actions`, `devops/cicd/gitlab-ci`
  - `containers` agent → `devops/containers/docker`
  - `kubernetes` agent → `devops/kubernetes/deployments`
  - `deployment` agent → `devops/deployment/strategies`
  - `monitoring` agent → `devops/monitoring/prometheus`
  - `infrastructure` agent → `devops/infrastructure/terraform`

### Changed

- Agent count reduced from 38 to 32 (6 DevOps agents extracted)
- Domain count reduced from 7 to 6

### Added

- Explicit `REDIRECT` routing table for DevOps queries
- Reference to ADR-007 for extraction rationale
- Migration path documentation in routing section

### Migration

Users referencing `backend-developer/devops/*` should update to `devops/*`:

| Old Path | New Path |
|----------|----------|
| `backend-developer/devops/cicd` | `devops/cicd/github-actions` |
| `backend-developer/devops/containers` | `devops/containers/docker` |
| `backend-developer/devops/kubernetes` | `devops/kubernetes/deployments` |
| `backend-developer/devops/deployment` | `devops/deployment/strategies` |
| `backend-developer/devops/monitoring` | `devops/monitoring/prometheus` |
| `backend-developer/devops/infrastructure` | `devops/infrastructure/terraform` |

See [devops CHANGELOG](../devops/CHANGELOG.md) for the new skill details.

## [1.0.0] - 2025-12-25

### Added

- Initial release with 38 agents across 7 domains

#### API Development (6 agents)
- `rest-design` - REST API design with RESTful conventions
- `graphql-design` - GraphQL schema, types, queries and mutations
- `openapi-spec` - OpenAPI/Swagger documentation generation
- `versioning` - API versioning strategies and deprecation
- `rate-limiting` - Rate limiting, throttling and quotas
- `validation` - Request payload and parameter validation

#### Database (6 agents)
- `modeling` - Database schema design and data modeling
- `migrations` - Database migrations and schema evolution
- `queries` - SQL/ORM query writing and optimization
- `optimization` - Index optimization and query performance
- `transactions` - Transaction management and isolation levels
- `nosql` - NoSQL databases (MongoDB, Redis, Elasticsearch)

#### Auth & Security (5 agents)
- `authentication` - JWT, OAuth2, sessions, MFA implementation
- `authorization` - RBAC, ABAC, permissions and policies
- `vulnerabilities` - OWASP Top 10 protection
- `cryptography` - Encryption, hashing, secrets management
- `audit` - Security logging, audit trails, compliance

#### Architecture (5 agents)
- `patterns` - Design patterns and SOLID principles
- `microservices` - Microservices architecture and patterns
- `monolith` - Modular monolith architecture
- `event-driven` - Event sourcing, CQRS, messaging
- `ddd` - Domain-Driven Design concepts

#### Performance (5 agents)
- `caching` - Cache strategies (Redis, CDN, in-memory)
- `profiling` - APM, tracing, performance analysis
- `query-optimization` - N+1 resolution, eager loading
- `concurrency` - Async programming, parallelism
- `resource-optimization` - CPU, memory, I/O optimization

#### Testing (5 agents)
- `unit` - Unit testing, mocks, stubs, spies
- `integration` - Integration testing with databases
- `api` - API testing, contract testing
- `fixtures` - Factories, fixtures, test data generation
- `coverage` - Code coverage and mutation testing

#### DevOps (6 agents)
- `cicd` - CI/CD pipelines (GitHub Actions, GitLab CI)
- `containers` - Docker, multi-stage builds, optimization
- `kubernetes` - K8s deployments, Helm charts
- `deployment` - Deployment strategies, rollback
- `monitoring` - Observability, metrics, alerting
- `infrastructure` - IaC with Terraform, cloud providers
