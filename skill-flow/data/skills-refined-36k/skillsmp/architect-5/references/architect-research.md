# architect Research

Research document for the software architecture skill.

## Phase 1: Upstream Survey

### 1.1 obra/superpowers Analysis

The [obra/superpowers](https://github.com/obra/superpowers) repository focuses on software development methodology and workflow skills rather than architecture-specific guidance. The skills library emphasizes:

- **Testing**: Test-driven development with RED-GREEN-REFACTOR cycles
- **Debugging**: Systematic root cause analysis
- **Collaboration**: Design refinement, planning, and code review workflows

**Design-Related Capability Found**: The closest architecture-adjacent feature is the **brainstorming skill**, described as providing "Socratic design refinement" that "refines rough ideas through questions, explores alternatives, presents design in sections for validation." However, this addresses requirements clarification rather than system architecture, distributed systems design, or technical architecture patterns.

**Conclusion**: No dedicated architecture-related skills, prompts, or tools exist in Superpowers. This represents an opportunity for architect to fill a gap.

### 1.2 VoltAgent/awesome-claude-code-subagents Analysis

The [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) repository contains several architecture-focused subagents:

| Subagent | Category | Description |
|----------|----------|-------------|
| **architect-reviewer** | Quality & Security | Architecture review specialist |
| **microservices-architect** | Core Development | Distributed systems designer |
| **cloud-architect** | Infrastructure | AWS/GCP/Azure specialist |
| **platform-engineer** | Infrastructure | Platform architecture expert |
| **llm-architect** | Data & AI | Large language model architect |

**Key Insight**: These subagents span system design, infrastructure planning, code structure review, and specialized domain architecture. The architect skill could incorporate concepts from all of these, particularly the architect-reviewer and microservices-architect patterns.

---

## Phase 2: Research Findings

### 2.1 Software Architecture Patterns

#### MVC (Model-View-Controller)

MVC remains relevant in 2025 for organizing code with clear separation of concerns.

**Key Benefits**:
- Testing pays dividends when responsibilities are split
- Unit tests target specific concerns, failures point to one place
- Controllers should be coordinators, not "business kitchens"

**Best Practices**:
- Combine MVC with service objects, serializers, and event-driven components
- Keep controllers thin, move business logic to services
- Use MVC for traditional web applications with clear request-response patterns

**Sources**:
- [Why MVC Architecture Still Matters in 2025](https://agamitechnologies.com/blog/why-mvc-architecture-still-matters-in-2025)

#### Microservices Architecture

Structures an application as a collection of small, autonomous services, each performing a specific function and communicating over a network.

**Key Benefits**:
- Services can be scaled independently for precise resource allocation
- Different microservices can use different technology stacks
- Well-suited for large, complex applications requiring flexibility and rapid deployment

**Best Practices**:
- Design around business capabilities, not technical layers
- Implement proper service boundaries using Domain-Driven Design concepts
- Use API gateways for external communication
- Implement circuit breakers for fault tolerance

**Example**: Netflix uses thousands of microservices handling everything from recommendations to billing.

**Sources**:
- [14 Software Architecture Patterns to Follow in 2025](https://www.mindinventory.com/blog/software-architecture-patterns/)
- [Microservices Pattern: Event-driven architecture](https://microservices.io/patterns/data/event-driven-architecture.html)

#### Hexagonal Architecture (Ports and Adapters)

Creates loosely coupled component-based applications by separating core business logic from external dependencies.

**Key Benefits**:
- Easily adapt to changes and integrate new technologies
- Services can be replaced or scaled without affecting core business logic
- Core logic remains agnostic to whether events come from HTTP, WebSocket, or message queues

**Real-World Examples**:
- Netflix uses hexagonal architecture with microservices for flexibility and decoupling
- PayPal separates transaction processing logic from APIs and UIs

**Best Practices**:
- Define clear ports (interfaces) for all external interactions
- Implement adapters for each external system (database, APIs, UI)
- Keep business logic in the core, free from framework dependencies

**Sources**:
- [Hexagonal Architecture - GeeksforGeeks](https://www.geeksforgeeks.org/system-design/hexagonal-architecture-system-design/)
- [Hexagonal Architecture: Principles and Benefits](https://www.aalpha.net/blog/hexagonal-architecture/)
- [HappyCoders Hexagonal Architecture Guide](https://www.happycoders.eu/software-craftsmanship/hexagonal-architecture/)

#### Event-Driven Architecture

Components communicate via asynchronous events rather than direct requests.

**Key Benefits**:
- Handles asynchronous data streams effectively
- Ideal for real-time applications and evolving needs
- Supports high-performance demands

**Best Practices**:
- Use message queues (RabbitMQ, AWS SQS, Kafka) for event handling
- Design for eventual consistency
- Implement proper event schemas and versioning

**Sources**:
- [Microservices Pattern: Event-driven architecture](https://microservices.io/patterns/data/event-driven-architecture.html)
- [5+ Software Architecture Patterns You Should Know in 2026](https://www.sayonetech.com/blog/software-architecture-patterns/)

#### Pattern Selection Guide

| Pattern | Best For | Avoid When |
|---------|----------|------------|
| MVC | Traditional web apps, CRUD operations | Complex domain logic, microservices |
| Microservices | Large teams, independent deployment | Small apps, tight budgets |
| Hexagonal | Testability, external system integration | Simple CRUD apps |
| Event-Driven | Real-time, high scalability | Strong consistency required |

---

### 2.2 Clean Architecture and Domain-Driven Design

#### Clean Architecture Layers

The purpose of Clean Architecture is to separate business logic from frameworks, databases, and UI.

**Layers** (inner to outer):
1. **Domain**: Core business rules and models
2. **Application**: Use cases, commands, queries, services
3. **Infrastructure**: Database, external APIs, storage
4. **Presentation**: API controllers, UI frameworks

**Key Rule**: Inner layers never depend on outer layers; outer layers depend on inner layers via interfaces.

**Sources**:
- [Clean Architecture and Domain-Driven Design in Practice 2025](https://wojciechowski.app/en/articles/clean-architecture-domain-driven-design-2025)
- [Understanding Clean Architecture and DDD](https://medium.com/bimar-teknoloji/understanding-clean-architecture-and-domain-driven-design-ddd-24e89caabc40)

#### Domain-Driven Design (DDD) Tactical Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| **Entities** | Objects with unique identity persisting over time | User, Order, Invoice |
| **Value Objects** | Objects holding data with no unique identity | Address, Money, DateRange |
| **Aggregates** | Cluster of entities treated as single unit | Order with OrderItems |
| **Repositories** | Interfaces for retrieving/storing aggregates | OrderRepository |
| **Services** | Business logic not belonging to entity/value object | PaymentService |

**Strategic Design Concepts**:
- **Bounded Contexts**: Explicit boundary within which a domain model exists
- **Ubiquitous Language**: Shared language between developers and domain experts
- **Context Mapping**: Relationships between bounded contexts

**When to Use DDD**:
- Complex domains and large-scale applications
- NOT for simple CRUD applications
- When collaboration with domain experts shapes the design

**Sources**:
- [GitHub: domain-driven-hexagon](https://github.com/Sairyss/domain-driven-hexagon)
- [Comparison of DDD and Clean Architecture Concepts](https://khalilstemmler.com/articles/software-design-architecture/domain-driven-design-vs-clean-architecture/)
- [KISS Clean Architecture With Domain-Driven Design](https://dzone.com/articles/kiss-clean-architecture-with-domain-driven-design)

#### SOLID Principles

| Principle | Description | Benefit |
|-----------|-------------|---------|
| **Single Responsibility** | One reason to change per class | Easier maintenance |
| **Open-Closed** | Open for extension, closed for modification | Extensibility |
| **Liskov Substitution** | Subtypes must be substitutable | Polymorphism, reusability |
| **Interface Segregation** | Don't depend on unused interfaces | Reduced coupling |
| **Dependency Inversion** | Depend on abstractions, not concretes | Testability, flexibility |

**Sources**:
- [SOLID Design Principles Explained - DigitalOcean](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design)
- [SOLID Principles with Real Life Examples - GeeksforGeeks](https://www.geeksforgeeks.org/system-design/solid-principle-in-programming-understand-with-real-life-examples/)
- [A Solid Guide to SOLID Principles - Baeldung](https://www.baeldung.com/solid-principles)

---

### 2.3 API Design Best Practices

#### REST (Representational State Transfer)

**Strengths**:
- Simple, widely adopted, extensive documentation
- Scalable due to stateless nature
- HTTP caching works out of the box

**Weaknesses**:
- Over-fetching and under-fetching data
- Bloated responses for complex resources

**Best Practices**:
- Use nouns for resources, verbs for actions
- Follow HTTP standards for status codes (200 success, 404 not found)
- Implement proper versioning (URL path or header)
- Use pagination and filtering for large datasets

**Sources**:
- [API Design Best Practices in 2025: REST, GraphQL, and gRPC](https://dev.to/cryptosandy/api-design-best-practices-in-2025-rest-graphql-and-grpc-2666)
- [REST vs GraphQL vs gRPC - Design Gurus](https://www.designgurus.io/blog/rest-graphql-grpc-system-design)

#### GraphQL

**Strengths**:
- Clients request exactly the data they need
- Single endpoint for all queries
- Eliminates N+1 query problem with batching
- Strong typing with schema introspection

**Weaknesses**:
- Lack of OpenAPI integration
- Caching more complex than REST
- Learning curve for teams

**Best Use Cases**:
- Complex applications with varied frontend data needs
- Mobile apps needing bandwidth efficiency
- Aggregating data from multiple sources

**Sources**:
- [The Complete Guide to API Types in 2026](https://dev.to/sizan_mahmud0_e7c3fd0cb68/the-complete-guide-to-api-types-in-2026-rest-graphql-grpc-soap-and-beyond-191)
- [Modern API Design Best Practices](https://dev.to/theodor_coin_4/modern-api-design-best-practices-rest-graphql-and-grpc-in-2025-1pdb)

#### gRPC

**Strengths**:
- Binary protocol (Protocol Buffers) - 3-10x smaller than JSON
- HTTP/2 multiplexing eliminates head-of-line blocking
- Bidirectional streaming support
- Strongly-typed contracts

**Weaknesses**:
- Steeper learning curve
- Less human-readable than REST
- Limited browser support

**Best Use Cases**:
- Microservices communication
- Real-time data transfer
- IoT devices requiring high performance
- Internal service-to-service communication

**Sources**:
- [gRPC vs REST vs GraphQL: The Ultimate API Showdown for 2025](https://medium.com/@sharmapraveen91/grpc-vs-rest-vs-graphql-the-ultimate-api-showdown-for-2025-developers-188320b4dc35)
- [When to Use REST vs. gRPC vs. GraphQL - Kong](https://konghq.com/blog/engineering/rest-vs-grpc-vs-graphql)

#### API Selection Guide

| API Style | Best For | Performance | Learning Curve |
|-----------|----------|-------------|----------------|
| REST | Public APIs, CRUD, simple apps | Good | Low |
| GraphQL | Complex queries, mobile apps | Good | Medium |
| gRPC | Microservices, real-time, IoT | Excellent | High |

---

### 2.4 Database Design Patterns

#### Normalization Best Practices

**Forms to Apply**:
1. **1NF**: Eliminate repeating groups, create separate tables
2. **2NF**: Remove partial dependencies on composite keys
3. **3NF**: Remove transitive dependencies

**Best Practices**:
- Apply normalization principles from the beginning
- Don't skip forms - work systematically from 1NF up
- For read-heavy applications, consider strategic denormalization
- Balance normal forms with performance requirements

**Sources**:
- [9 Key Database Design Best Practices for 2025](https://getnerdify.com/blog/database-design-best-practices)
- [Mastering Database Schema Design - Airbyte](https://airbyte.com/data-engineering-resources/database-schema-design)

#### Indexing Strategies

| Strategy | Description | Use When |
|----------|-------------|----------|
| **Composite Index** | Multiple columns in selectivity order | Multi-column WHERE clauses |
| **Covering Index** | Includes all query columns | Eliminating table lookups |
| **Foreign Key Index** | Index on FK columns | Improving JOIN performance |

**Best Practices**:
- Avoid over-indexing - analyze query patterns first
- Index columns in WHERE, JOIN, ORDER BY
- Monitor index bloat and fragmentation
- Rebuild indexes after large operations

**Sources**:
- [8 Essential Database Design Best Practices for 2025](https://kpinfo.tech/database-design-best-practices/)
- [Design Better Databases - DbSchema](https://dbschema.com/blog/design/database-design-best-practices-2025/)

#### Migration Best Practices

**Key Techniques**:
- **Expand-Contract Pattern**: Add new, migrate, remove old
- **Blue-Green Deployment**: Parallel environments for safe transitions
- **Schema-as-Code**: Treat database structures as software artifacts

**Process Recommendations**:
- Store all DDL and migration scripts in version control (Git)
- Establish Change Advisory Board (CAB) for review
- Plan for automated rollback capabilities
- Test migrations in non-production environments first

**Warning**: Over 80% of data migration projects fail to deliver on time or go over budget due to inadequate upfront analysis.

**Sources**:
- [Database Migration Checklist: Complete Guide For 2025 Success](https://savvycomsoftware.com/blog/database-migration-checklist/)
- [10 Essential Database Management Best Practices for 2025](https://www.flowgenius.ai/post/10-essential-database-management-best-practices-for-2025)

---

### 2.5 Monorepo vs Polyrepo Tradeoffs

#### Monorepo

**Advantages**:
- Centralized versioning with consistent history
- Atomic changes across multiple projects
- Unified tooling and bootstrapping
- Easier code sharing and dependency management

**Challenges**:
- Can become large and complex over time
- Git operations slow down at scale
- Space limitations on developer machines
- All teams affected by repository issues

**Tools**: Bazel, Lerna, Nx, Turborepo

**Real-World Example**: Google, Meta use monorepos with custom tooling

**Sources**:
- [Monorepo vs Polyrepo: Which One Should You Choose in 2025?](https://dev.to/md-afsar-mahmud/monorepo-vs-polyrepo-which-one-should-you-choose-in-2025-g77)
- [Monorepo vs Polyrepo - Aviator](https://www.aviator.co/blog/monorepo-vs-polyrepo/)

#### Polyrepo

**Advantages**:
- Lighter to clone and faster to understand
- Promotes independence and autonomy
- Better for security-sensitive code separation
- Teams can choose their own tooling

**Challenges**:
- Difficult to share code between projects
- Complex dependency management and versioning
- Changes in dependencies don't auto-rebuild dependants
- Communication overhead between teams

**Real-World Example**: Amazon, Netflix prefer polyrepos aligned with service ownership

**Sources**:
- [Monorepo vs. Polyrepo Pros, Cons, and Tools - Graphite](https://graphite.com/guides/monorepo-vs-polyrepo-pros-cons-tools)
- [Monorepo vs. Polyrepo: How to Choose - Buildkite](https://buildkite.com/resources/blog/monorepo-polyrepo-choosing/)

#### Selection Criteria

| Factor | Choose Monorepo | Choose Polyrepo |
|--------|-----------------|-----------------|
| Team Size | Small to medium | Large, distributed |
| Code Sharing | High | Low |
| Deployment | Unified pipeline | Independent releases |
| Tech Diversity | Similar stacks | Varied stacks |
| Security | Standard | Strict isolation needed |

---

### 2.6 Code Organization Patterns

#### Feature-Based Structure

Groups related files by domain/feature rather than technical type.

```
src/
  features/
    users/
      components/
      hooks/
      services/
      api/
    orders/
      components/
      hooks/
      services/
      api/
  shared/
    components/
    utils/
```

**Benefits**:
- More scalable for larger projects
- Easier to navigate by feature
- Better for team collaboration
- Simpler to delete entire features

**Sources**:
- [Feature-Based Directory Structure in Angular](https://medium.com/@sehban.alam/feature-based-directory-structure-in-angular-a-step-by-step-guide-to-clean-code-and-scalable-apps-f97f86e9bec9)
- [Part 2: Folder Structure - Building a Solid Foundation](https://dev.to/sathishskdev/part-2-folder-structure-building-a-solid-foundation-omh)

#### Layer-Based Structure

Separates code by technical responsibility.

```
src/
  presentation/
    components/
    pages/
  application/
    services/
    use-cases/
  domain/
    entities/
    value-objects/
  infrastructure/
    api/
    database/
```

**Benefits**:
- Clear separation of concerns
- Supports Clean Architecture principles
- Easy to understand layer responsibilities

**Drawbacks**:
- Related files far apart
- Doesn't scale well for large apps
- Easy to forget files when deleting features

**Sources**:
- [Flutter Project Structure: Feature-first or Layer-first?](https://codewithandrea.com/articles/flutter-project-structure/)
- [Popular React Folder Structures and Screaming Architecture](https://profy.dev/article/react-folder-structure)

#### Hybrid Approach (Recommended)

Feature-first with layers inside each feature:

```
src/
  features/
    users/
      data/       # APIs, repositories
      domain/     # Business logic, entities
      presentation/  # UI components
    orders/
      data/
      domain/
      presentation/
  core/
    theme/
    constants/
    utils/
  shared/
    components/
    hooks/
```

**Sources**:
- [Best Practices for Folder Structure in Large Flutter Projects (2025)](https://www.pravux.com/best-practices-for-folder-structure-in-large-flutter-projects-2025-guide/)
- [Recommended Folder Structure for React 2025](https://dev.to/pramod_boda/recommended-folder-structure-for-react-2025-48mc)

---

### 2.7 Dependency Injection and Inversion of Control

#### Core Concepts

**Inversion of Control (IoC)**: Transfers control of objects to a container or framework. The framework calls your code, not the other way around.

**Dependency Injection (DI)**: Dependencies are "injected" into a class rather than created by the class itself.

**Sources**:
- [Inversion of Control Containers and the Dependency Injection pattern - Martin Fowler](https://martinfowler.com/articles/injection.html)
- [Inversion of Control and Dependency Injection with Spring - Baeldung](https://www.baeldung.com/inversion-control-and-dependency-injection-in-spring)

#### Types of Dependency Injection

| Type | Description | Use When |
|------|-------------|----------|
| **Constructor Injection** | Dependencies passed via constructor | Required dependencies |
| **Setter Injection** | Dependencies set via setter methods | Optional dependencies |
| **Interface Injection** | Dependency provides injector method | Framework contracts |

#### Service Lifetimes

| Lifetime | Description | Thread Safety |
|----------|-------------|---------------|
| **Transient** | Created each request | Not required |
| **Scoped** | Created once per scope/request | Not required |
| **Singleton** | Created once, shared | Required |

**Sources**:
- [Dependency injection - .NET | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection)
- [IoC: A Comprehensive Guide for 2025](https://www.shadecoder.com/topics/inversion-of-control-ioc-a-comprehensive-guide-for-2025)

#### Best Practices

**Do**:
- Use constructor injection for required dependencies
- Restrict container usage to composition root
- Pass dependencies explicitly
- Define narrow, focused interfaces

**Avoid**:
- Treating container as global service locator (hides dependencies)
- Service locator pattern in business logic
- Scope mismatches between dependencies
- Leaking framework details into domain code

**Sources**:
- [Dependency Injection and Inversion of Control Patterns - Toptal](https://www.toptal.com/full-stack/exploring-dependency-injection-patterns)
- [Dependency Injection and Inversion of Control - Reflectoring](https://reflectoring.io/dependency-injection-and-inversion-of-control/)

---

### 2.8 Architecture Decision Records (ADRs)

#### What is an ADR?

An Architectural Decision Record (ADR) captures a single Architectural Decision and its rationale. It helps understand the reasons for a chosen architectural decision, along with its trade-offs and consequences.

**Sources**:
- [Architectural Decision Records (ADRs)](https://adr.github.io/)
- [GitHub: architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record)

#### Popular Templates

**1. Michael Nygard Template** (Minimal):
```markdown
# Title

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[Problem and forces at play]

## Decision
[The decision made]

## Consequences
[Results of the decision]
```

**2. MADR Template** (Comprehensive):
```markdown
# Title

## Status
## Context and Problem Statement
## Decision Drivers
## Considered Options
## Decision Outcome
### Positive Consequences
### Negative Consequences
## Pros and Cons of the Options
### Option 1
### Option 2
## Links
```

**Sources**:
- [ADR Templates](https://adr.github.io/adr-templates/)
- [MADR - Markdown Any Decision Records](https://adr.github.io/madr/)

#### Best Practices

**From AWS (March 2025)**:
- Centralize ADR storage for transparency
- Adopt readout meeting style (10-15 min reading, written comments)
- Keep participant list lean (under 10 people)
- Focus each ADR on a single decision

**From TechTarget (2025)**:
- Avoid combining multiple decisions in one document
- Establish consistency with simple, adaptable templates
- Implement peer-review practices
- All developers should understand how to contribute

**From Joel Parker Henderson**:
- Review each ADR one month later for after-action learning
- Consider "living document" approach with date-stamped updates
- Include business constraints, quality attributes, and consequences

**Sources**:
- [Master ADRs: Best Practices - AWS Architecture Blog](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)
- [8 Best Practices for Creating ADRs - TechTarget](https://www.techtarget.com/searchapparchitecture/tip/4-best-practices-for-creating-architecture-decision-records)
- [Maintain an ADR - Microsoft Azure](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)

---

### 2.9 CQRS and Event Sourcing

#### Command Query Responsibility Segregation (CQRS)

Separates read and write operations into distinct pathways.

**Core Principle**: A method should either read or write data - never both.

**Benefits**:
- Independent scaling of read and write sides
- Optimized data models for each operation
- Better performance for read-heavy or write-heavy systems

**Sources**:
- [CQRS Pattern - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)
- [CQRS and Event Sourcing in Java - Baeldung](https://www.baeldung.com/cqrs-event-sourcing-java)

#### Event Sourcing

Stores the complete history of changes as immutable events rather than just current state.

**Benefits**:
- Complete audit trail
- Ability to reconstruct state at any point in time
- Natural fit for event-driven architectures

**Sources**:
- [Event Sourcing pattern - Azure](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
- [Microservices Pattern: Event sourcing](https://microservices.io/patterns/data/event-sourcing.html)

#### When to Use

**Good Fit**:
- Complex business logic
- Finance, healthcare, real-time analytics
- Need for audit trails
- High scalability requirements

**Poor Fit**:
- Simple CRUD applications
- Small or simple domains
- Systems requiring strong consistency
- Low occurrence of conflicting updates

#### Key Challenges

| Challenge | Mitigation |
|-----------|------------|
| Eventual consistency | Design UI for stale data handling |
| Complexity | Only use when benefits justify cost |
| Messaging failures | Implement idempotency, retries |
| Event schema evolution | Version events, use upcasters |

**Sources**:
- [CQRS, Event Sourcing and Database Architecture - Upsolver](https://www.upsolver.com/blog/cqrs-event-sourcing-build-database-architecture)
- [1 Year of Event Sourcing and CQRS](https://itnext.io/1-year-of-event-sourcing-and-cqrs-fb9033ccd1c6)

---

## Audit Checklist Summary

### Critical

- [ ] **Separation of Concerns**: Business logic isolated from infrastructure/UI
- [ ] **SOLID Principles Adherence**: All five principles considered in design
- [ ] **API Versioning Strategy**: Breaking changes handled gracefully
- [ ] **Database Indexing**: Indexes on columns used in WHERE, JOIN, ORDER BY
- [ ] **Dependency Direction**: Inner layers never depend on outer layers
- [ ] **ADR Documentation**: Major architectural decisions recorded

### Important

- [ ] **Repository Pattern**: Data access abstracted behind interfaces
- [ ] **Bounded Contexts Defined**: Clear boundaries between domains (if using DDD)
- [ ] **Error Handling Strategy**: Consistent approach across layers
- [ ] **Migration Strategy**: Schema changes versioned and reversible
- [ ] **Code Organization**: Feature-based or hybrid structure for scalability
- [ ] **Constructor Injection**: Dependencies explicitly declared
- [ ] **Normalization Applied**: At least 3NF with strategic denormalization

### Recommended

- [ ] **Hexagonal Ports/Adapters**: External systems accessed through adapters
- [ ] **Event-Driven Where Appropriate**: Async communication for decoupling
- [ ] **CQRS for Complex Queries**: Separate read/write models if needed
- [ ] **Monorepo vs Polyrepo Decision**: Documented with rationale
- [ ] **API Style Selection**: REST/GraphQL/gRPC chosen for specific use cases
- [ ] **Service Lifetime Management**: Transient/Scoped/Singleton correctly applied
- [ ] **Monthly ADR Review**: After-action reviews for continuous improvement
- [ ] **Composite Indexes**: Multi-column queries optimized
- [ ] **Feature Flags for Migrations**: Gradual rollout capability

---

## References

### Architecture Patterns
- [14 Software Architecture Patterns to Follow in 2025](https://www.mindinventory.com/blog/software-architecture-patterns/)
- [5+ Software Architecture Patterns You Should Know in 2026](https://www.sayonetech.com/blog/software-architecture-patterns/)
- [Mastering Software Architecture: 6 Patterns Every Developer Should Know](https://dev.to/dev_tips/mastering-software-architecture-6-patterns-every-developer-should-know-and-actually-use-1aho)

### Clean Architecture & DDD
- [Clean Architecture and Domain-Driven Design in Practice 2025](https://wojciechowski.app/en/articles/clean-architecture-domain-driven-design-2025)
- [GitHub: domain-driven-hexagon](https://github.com/Sairyss/domain-driven-hexagon)
- [Comparison of DDD and Clean Architecture Concepts](https://khalilstemmler.com/articles/software-design-architecture/domain-driven-design-vs-clean-architecture/)

### API Design
- [API Design Best Practices in 2025](https://dev.to/cryptosandy/api-design-best-practices-in-2025-rest-graphql-and-grpc-2666)
- [The Complete Guide to API Types in 2026](https://dev.to/sizan_mahmud0_e7c3fd0cb68/the-complete-guide-to-api-types-in-2026-rest-graphql-grpc-soap-and-beyond-191)
- [REST vs GraphQL vs gRPC - Design Gurus](https://www.designgurus.io/blog/rest-graphql-grpc-system-design)

### Database Design
- [9 Key Database Design Best Practices for 2025](https://getnerdify.com/blog/database-design-best-practices)
- [Database Migration Checklist 2025](https://savvycomsoftware.com/blog/database-migration-checklist/)
- [Mastering Database Schema Design - Airbyte](https://airbyte.com/data-engineering-resources/database-schema-design)

### Code Organization
- [Feature-Based Directory Structure in Angular](https://medium.com/@sehban.alam/feature-based-directory-structure-in-angular-a-step-by-step-guide-to-clean-code-and-scalable-apps-f97f86e9bec9)
- [Flutter Project Structure: Feature-first or Layer-first?](https://codewithandrea.com/articles/flutter-project-structure/)
- [Recommended Folder Structure for React 2025](https://dev.to/pramod_boda/recommended-folder-structure-for-react-2025-48mc)

### Repository Strategy
- [Monorepo vs Polyrepo 2025](https://dev.to/md-afsar-mahmud/monorepo-vs-polyrepo-which-one-should-you-choose-in-2025-g77)
- [Monorepo vs. Polyrepo Pros, Cons, and Tools](https://graphite.com/guides/monorepo-vs-polyrepo-pros-cons-tools)
- [GitHub: monorepo-vs-polyrepo](https://github.com/joelparkerhenderson/monorepo-vs-polyrepo)

### Dependency Injection
- [Martin Fowler: Inversion of Control Containers and the Dependency Injection pattern](https://martinfowler.com/articles/injection.html)
- [Microsoft: Dependency injection - .NET](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection)
- [Toptal: Inversion of Control Patterns](https://www.toptal.com/full-stack/exploring-dependency-injection-patterns)

### ADRs
- [GitHub: architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record)
- [ADR Templates](https://adr.github.io/adr-templates/)
- [AWS: Master ADRs Best Practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)

### CQRS & Event Sourcing
- [Azure: CQRS Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)
- [Azure: Event Sourcing pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
- [Microservices.io: Event sourcing](https://microservices.io/patterns/data/event-sourcing.html)
