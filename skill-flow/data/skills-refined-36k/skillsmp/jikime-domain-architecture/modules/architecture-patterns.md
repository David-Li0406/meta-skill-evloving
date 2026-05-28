# Architecture Patterns

Detailed diagrams and explanations for the seven architecture patterns.

## Pattern 1: Layered Architecture (Simple)

```
┌─────────────────────────────────────────┐
│           PRESENTATION LAYER            │  Controllers, Views, API endpoints
├─────────────────────────────────────────┤
│           APPLICATION LAYER             │  Use cases, Services, DTOs
├─────────────────────────────────────────┤
│             DOMAIN LAYER                │  Entities, Business logic, Rules
├─────────────────────────────────────────┤
│          INFRASTRUCTURE LAYER           │  Database, External APIs, I/O
└─────────────────────────────────────────┘

✅ Use when: CRUD apps, small teams, quick prototypes
❌ Avoid when: Complex business logic, need for testability
```

## Pattern 2: Clean Architecture (Moderate)

```
┌───────────────────────────────────────────────────────┐
│                Frameworks & Drivers                    │
│  ┌───────────────────────────────────────────────┐   │
│  │              Interface Adapters                │   │
│  │  ┌───────────────────────────────────────┐   │   │
│  │  │          Application Layer            │   │   │
│  │  │  ┌───────────────────────────────┐   │   │   │
│  │  │  │         Domain Layer          │   │   │   │
│  │  │  │   (Entities & Business Rules) │   │   │   │
│  │  │  └───────────────────────────────┘   │   │   │
│  │  └───────────────────────────────────────┘   │   │
│  └───────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────┘

Dependency Rule: Dependencies point INWARD only
- Domain has NO external dependencies
- Application depends only on Domain
- Adapters depend on Application
- Frameworks depend on Adapters

✅ Use when: Complex business logic, long-lived projects, testability critical
❌ Avoid when: Simple CRUD, very tight deadlines
```

## Pattern 3: Hexagonal (Ports & Adapters)

```
                    ┌──────────────┐
                    │   REST API   │
                    └──────┬───────┘
                           │ Port
        ┌──────────────────▼──────────────────┐
        │                                      │
  Port  │         APPLICATION CORE            │  Port
  ◀─────│                                      │─────▶
        │    ┌────────────────────────┐       │
        │    │    Domain Logic        │       │
        │    │    (Pure Functions)    │       │
        │    └────────────────────────┘       │
        │                                      │
        └──────────────────┬──────────────────┘
                           │ Port
                    ┌──────▼───────┐
                    │   Database   │
                    └──────────────┘

Ports: Interfaces defined by the application
Adapters: Implementations that connect to external systems

✅ Use when: Need to swap external dependencies, multiple entry points
❌ Avoid when: Simple apps, single data source
```

## Pattern 4: Event-Driven Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────┐
│  Producer   │────▶│   Event Bus     │────▶│  Consumer A │
└─────────────┘     │  (Kafka/RabbitMQ)│     └─────────────┘
                    │                  │
                    │                  │────▶┌─────────────┐
                    │                  │     │  Consumer B │
                    │                  │     └─────────────┘
                    │                  │
                    │                  │────▶┌─────────────┐
                    └─────────────────┘     │  Consumer C │
                                            └─────────────┘

Event Types:
- Domain Events: Business-meaningful occurrences (OrderPlaced, UserRegistered)
- Integration Events: Cross-service communication
- Command Events: Request for action

✅ Use when: Loose coupling, async processing, scalability
❌ Avoid when: Strong consistency required, simple workflows
```

## Pattern 5: CQRS (Command Query Responsibility Segregation)

```
┌───────────────────────────────────────────────────────────┐
│                         API Gateway                        │
└───────────────────┬───────────────────┬───────────────────┘
                    │                   │
          ┌─────────▼─────────┐ ┌───────▼─────────┐
          │     Commands      │ │     Queries     │
          │   (Write Model)   │ │  (Read Model)   │
          └─────────┬─────────┘ └───────┬─────────┘
                    │                   │
          ┌─────────▼─────────┐ ┌───────▼─────────┐
          │  Domain Model     │ │  Denormalized   │
          │  (Normalized)     │ │  View Models    │
          └─────────┬─────────┘ └───────┬─────────┘
                    │                   │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │    Event Store    │
                    └───────────────────┘

✅ Use when: Different read/write scaling, complex queries, event sourcing
❌ Avoid when: Simple CRUD, small data sets
```

## Pattern 6: Modular Monolith (Recommended for Most)

```
┌─────────────────────────────────────────────────────────────┐
│                     SINGLE DEPLOYMENT UNIT                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Module A  │  │   Module B  │  │   Module C  │         │
│  │  ┌───────┐  │  │  ┌───────┐  │  │  ┌───────┐  │         │
│  │  │ API   │  │  │  │ API   │  │  │  │ API   │  │         │
│  │  ├───────┤  │  │  ├───────┤  │  │  ├───────┤  │         │
│  │  │Domain │  │  │  │Domain │  │  │  │Domain │  │         │
│  │  ├───────┤  │  │  ├───────┤  │  │  ├───────┤  │         │
│  │  │ Data  │  │  │  │ Data  │  │  │  │ Data  │  │         │
│  │  └───────┘  │  │  └───────┘  │  │  └───────┘  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │                │                │                  │
│         └────────────────┴────────────────┘                  │
│                    Shared Kernel (minimal)                   │
└─────────────────────────────────────────────────────────────┘

Module Communication:
- Public API: Well-defined interfaces between modules
- Shared Kernel: Minimal shared code (value objects, common types)
- Events: Async communication for loose coupling

✅ Use when: Medium-large projects, want microservices benefits without complexity
❌ Avoid when: Truly distributed team with separate deployment needs
```

## Pattern 7: Microservices (Complex)

```
┌─────────────────────────────────────────────────────────────────┐
│                         API Gateway                              │
└───────────┬───────────────┬───────────────┬─────────────────────┘
            │               │               │
   ┌────────▼────────┐ ┌────▼────────┐ ┌────▼────────┐
   │  User Service   │ │Order Service│ │Payment Svc  │
   │  ┌───────────┐  │ │ ┌─────────┐ │ │ ┌─────────┐ │
   │  │  REST API │  │ │ │REST API │ │ │ │REST API │ │
   │  ├───────────┤  │ │ ├─────────┤ │ │ ├─────────┤ │
   │  │  Domain   │  │ │ │ Domain  │ │ │ │ Domain  │ │
   │  ├───────────┤  │ │ ├─────────┤ │ │ ├─────────┤ │
   │  │  Postgres │  │ │ │  Mongo  │ │ │ │  Redis  │ │
   │  └───────────┘  │ │ └─────────┘ │ │ └─────────┘ │
   └─────────────────┘ └─────────────┘ └─────────────┘

Prerequisites (Don't start without):
- [ ] CI/CD pipeline mature
- [ ] Container orchestration (K8s)
- [ ] Service mesh / API gateway
- [ ] Distributed tracing
- [ ] Centralized logging

✅ Use when: Independent scaling, polyglot persistence, large distributed teams
❌ Avoid when: Small team, limited DevOps maturity, unclear domain boundaries
```

---

Version: 1.0.0
Source: jikime-domain-architecture SKILL.md
