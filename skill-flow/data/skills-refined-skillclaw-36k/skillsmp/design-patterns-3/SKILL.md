---
name: design-patterns
description: Software design patterns for architecture, components, databases, and APIs
---

# Design Patterns

A technology-agnostic skill for software architecture and design patterns.

## Architectural Patterns

### Layered Architecture

```yaml
pattern: layered_architecture
description: "Separation of concerns through horizontal layers"

layers:
  presentation:
    responsibility: "User interface and input handling"
    communicates_with: [application]

  application:
    responsibility: "Business logic orchestration"
    communicates_with: [domain, infrastructure]

  domain:
    responsibility: "Core business rules and entities"
    communicates_with: [none - pure domain logic]

  infrastructure:
    responsibility: "External systems, persistence, APIs"
    communicates_with: [domain]

rules:
  - "Dependencies point inward (presentation → domain)"
  - "Each layer only knows about adjacent layers"
  - "Domain layer has no external dependencies"
```

### Clean Architecture

```yaml
pattern: clean_architecture
description: "Dependency inversion with entities at center"

rings:
  entities:
    description: "Enterprise business rules"
    dependencies: none

  use_cases:
    description: "Application business rules"
    dependencies: [entities]

  interface_adapters:
    description: "Controllers, presenters, gateways"
    dependencies: [use_cases, entities]

  frameworks:
    description: "External frameworks and drivers"
    dependencies: [interface_adapters]

key_principle: "Dependencies always point inward"
```

### Hexagonal Architecture (Ports & Adapters)

```yaml
pattern: hexagonal_architecture
description: "Core logic isolated from external concerns"

components:
  core:
    description: "Domain logic, independent of I/O"
    contains: [entities, services, ports]

  ports:
    description: "Interfaces defining boundaries"
    types:
      - primary: "Driven by external (API, UI)"
      - secondary: "Driving external (DB, messaging)"

  adapters:
    description: "Implementations connecting to external systems"
    examples:
      - "REST controller (primary adapter)"
      - "Repository implementation (secondary adapter)"

benefit: "Core can be tested without external systems"
```

## Component Design Patterns

### Repository Pattern

```yaml
pattern: repository
description: "Abstract data access behind collection-like interface"

structure:
  interface:
    methods:
      - "find(id): Entity"
      - "findAll(criteria): Entity[]"
      - "save(entity): void"
      - "delete(entity): void"

  implementation:
    responsibility: "Handle actual persistence"
    examples:
      - DatabaseRepository
      - InMemoryRepository
      - CacheDecoratorRepository

use_when:
  - "Separate domain from data access"
  - "Enable testing with in-memory implementations"
  - "Support multiple data sources"
```

### Service Pattern

```yaml
pattern: service
description: "Encapsulate business operations"

types:
  domain_service:
    description: "Operations that don't belong to a single entity"
    example: "TransferService for money transfers between accounts"

  application_service:
    description: "Orchestrate use cases"
    example: "OrderService coordinating payment, inventory, shipping"

  infrastructure_service:
    description: "External system interactions"
    example: "EmailService, PaymentGatewayService"

guidelines:
  - "Services are stateless"
  - "One public method per specific operation"
  - "Coordinate, don't contain business rules"
```

### Factory Pattern

```yaml
pattern: factory
description: "Encapsulate object creation logic"

types:
  simple_factory:
    use_when: "Creation logic is complex but static"
    example: "UserFactory.create(type)"

  factory_method:
    use_when: "Subclasses need to determine creation"
    example: "Abstract Document with createPage() method"

  abstract_factory:
    use_when: "Create families of related objects"
    example: "UIFactory creating buttons, dialogs, menus"

benefits:
  - "Centralize creation logic"
  - "Enforce invariants at creation"
  - "Support testing with mock factories"
```

## Database Design Patterns

### Entity Relationship Patterns

```yaml
patterns:
  one_to_many:
    description: "Parent has many children"
    implementation:
      - "Foreign key in child table"
      - "ON DELETE CASCADE if children are owned"
    example: "User has many Posts"

  many_to_many:
    description: "Both sides have many of each other"
    implementation:
      - "Junction/pivot table"
      - "Consider if junction has attributes"
    example: "Users and Roles via user_roles table"

  one_to_one:
    description: "Exactly one on each side"
    implementation:
      - "Foreign key with unique constraint"
      - "Or same primary key in both tables"
    example: "User has one Profile"
```

### Query Optimization Patterns

```yaml
optimization_patterns:
  indexing:
    description: "Speed up queries on specific columns"
    guidelines:
      - "Index columns in WHERE, JOIN, ORDER BY"
      - "Consider composite indexes for multi-column queries"
      - "Avoid over-indexing (slows writes)"

  eager_loading:
    description: "Load related data in fewer queries"
    use_when: "Always need related data"
    avoid_when: "Related data rarely used"

  pagination:
    description: "Limit result set size"
    techniques:
      - "LIMIT/OFFSET for simple cases"
      - "Cursor-based for large datasets"
```

## API Design Patterns

### RESTful Resource Design

```yaml
rest_patterns:
  resource_naming:
    rules:
      - "Use nouns, not verbs (/users, not /getUsers)"
      - "Use plural form (/users, not /user)"
      - "Use kebab-case for multi-word (/user-profiles)"
      - "Nest for relationships (/users/{id}/posts)"

  http_methods:
    GET: "Retrieve resource(s)"
    POST: "Create new resource"
    PUT: "Replace entire resource"
    PATCH: "Partial update"
    DELETE: "Remove resource"

  response_codes:
    200: "OK - Successful GET, PUT, PATCH"
    201: "Created - Successful POST"
    204: "No Content - Successful DELETE"
    400: "Bad Request - Invalid input"
    401: "Unauthorized - Auth required"
    403: "Forbidden - No permission"
    404: "Not Found - Resource doesn't exist"
    422: "Unprocessable - Validation failed"
    500: "Server Error - Unexpected failure"
```

### Request/Response Patterns

```yaml
patterns:
  envelope:
    description: "Wrap response in metadata"
    structure:
      data: "The actual response data"
      meta: "Pagination, timestamps, etc."
      errors: "Error details if applicable"

  hateoas:
    description: "Include links to related actions"
    example:
      data: {id: 1, name: "..."}
      links:
        self: "/users/1"
        posts: "/users/1/posts"
        delete: "/users/1"
```

## Integration

### Used By Agents

```yaml
primary_users:
  - design-architect: "Pattern selection and application"

secondary_users:
  - code-developer: "Implementing designed patterns"
  - quality-reviewer: "Validating pattern compliance"
```
