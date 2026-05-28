# Backend Developer Skill

Expert en développement backend - APIs, bases de données, architecture, sécurité, performance et DevOps.

## Quick Start

Invoquez ce skill quand vous avez besoin d'aide sur :
- Conception et développement d'APIs REST/GraphQL
- Modélisation et optimisation de bases de données
- Authentification, autorisation et sécurité
- Architecture logicielle (microservices, DDD, event-driven)
- Optimisation des performances
- Tests backend
- DevOps et infrastructure

## Domaines

| Domaine | Agents | Description |
|---------|--------|-------------|
| [API](#api-development) | 6 | REST, GraphQL, OpenAPI, versioning |
| [Database](#database) | 6 | Modeling, migrations, queries, NoSQL |
| [Auth & Security](#auth--security) | 5 | JWT, OAuth, OWASP, cryptography |
| [Architecture](#architecture) | 5 | Patterns, microservices, DDD |
| [Performance](#performance) | 5 | Caching, profiling, optimization |
| [Testing](#testing) | 5 | Unit, integration, API tests |
| [DevOps](#devops) | 6 | CI/CD, Docker, Kubernetes |

**Total : 38 agents spécialisés** *(+ 7 orchestrateurs de domaine)*

## API Development

| Agent | Responsabilité |
|-------|----------------|
| `rest-design` | Conception d'APIs REST selon les conventions RESTful |
| `graphql-design` | Schémas GraphQL, types, queries, mutations |
| `openapi-spec` | Documentation OpenAPI/Swagger |
| `versioning` | Stratégies de versioning d'API |
| `rate-limiting` | Rate limiting, throttling, quotas |
| `validation` | Validation des payloads et paramètres |

## Database

| Agent | Responsabilité |
|-------|----------------|
| `modeling` | Conception de schémas et modèles de données |
| `migrations` | Gestion des migrations de base de données |
| `queries` | Écriture et optimisation de requêtes SQL/ORM |
| `optimization` | Indexation et optimisation des performances |
| `transactions` | Gestion des transactions et isolation |
| `nosql` | MongoDB, Redis, Elasticsearch |

## Auth & Security

| Agent | Responsabilité |
|-------|----------------|
| `authentication` | JWT, OAuth2, sessions, MFA |
| `authorization` | RBAC, ABAC, permissions |
| `vulnerabilities` | Protection OWASP Top 10 |
| `cryptography` | Chiffrement, hashing, secrets |
| `audit` | Logging sécurité, audit trail |

## Architecture

| Agent | Responsabilité |
|-------|----------------|
| `patterns` | Design patterns, principes SOLID |
| `microservices` | Architecture microservices |
| `monolith` | Monolithe modulaire |
| `event-driven` | Event sourcing, CQRS, messaging |
| `ddd` | Domain-Driven Design |

## Performance

| Agent | Responsabilité |
|-------|----------------|
| `caching` | Stratégies de cache (Redis, CDN) |
| `profiling` | APM, tracing, analyse |
| `query-optimization` | Résolution N+1, eager loading |
| `concurrency` | Programmation asynchrone |
| `resource-optimization` | Optimisation CPU, mémoire, I/O |

## Testing

| Agent | Responsabilité |
|-------|----------------|
| `unit` | Tests unitaires, mocks, stubs |
| `integration` | Tests d'intégration avec DB |
| `api` | Tests API, contract testing |
| `fixtures` | Factories, fixtures, seeds |
| `coverage` | Couverture et mutation testing |

## DevOps

| Agent | Responsabilité |
|-------|----------------|
| `cicd` | GitHub Actions, GitLab CI |
| `containers` | Docker, multi-stage builds |
| `kubernetes` | K8s, Helm charts |
| `deployment` | Stratégies de déploiement |
| `monitoring` | Observabilité, alerting |
| `infrastructure` | Terraform, IaC |

## Exemples d'Utilisation

```
"Je veux créer une API REST pour gérer des utilisateurs"
→ Route vers: api/rest-design

"Comment sécuriser mon endpoint avec JWT?"
→ Route vers: auth-security/authentication

"Mes requêtes sont lentes, comment optimiser?"
→ Route vers: database/optimization + performance/caching

"J'ai besoin de configurer une pipeline CI/CD"
→ Route vers: devops/cicd
```

## Technologies Supportées

### Langages
Node.js/TypeScript, Python, Go, Java/Kotlin, PHP, Rust

### Frameworks
Express, NestJS, FastAPI, Django, Spring Boot, Laravel

### Bases de données
PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch

### Infrastructure
Docker, Kubernetes, AWS, GCP, Azure, Terraform

## Principes

Chaque agent suit le principe **SRP (Single Responsibility Principle)** :
- Une responsabilité unique et claire
- Délégation explicite vers d'autres agents
- Template de sortie standardisé

## Guides

- [Getting Started](./docs/getting-started.md) - Workflow recommandé et exemples concrets

## Version

Voir [CHANGELOG.md](./CHANGELOG.md) pour l'historique des versions.
