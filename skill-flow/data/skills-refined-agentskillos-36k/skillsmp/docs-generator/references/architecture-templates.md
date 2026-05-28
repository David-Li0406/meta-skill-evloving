# Architecture Documentation Templates

Templates for generating `docs/architecture/` files. Focus on **why** (decisions, rationale), not **how** (tutorials).

**Key principle**: Architecture docs explain structure, patterns, and rationale. Avoid line-number references that go stale—describe where things live by directory/module, not by line.

## 01-overview.md

```markdown
# System Overview

{1-2 paragraph high-level description of the system, its purpose, and key design goals.}

## Architecture Diagram

```mermaid
flowchart TB
    subgraph External
        User[User/Client]
        ExtAPI[External APIs]
    end

    subgraph Application
        Entry[Entry Point]
        Core[Core Logic]
        Data[Data Layer]
    end

    subgraph Infrastructure
        DB[(Database)]
        Cache[(Cache)]
    end

    User --> Entry
    Entry --> Core
    Core --> Data
    Data --> DB
    Data --> Cache
    Core --> ExtAPI
```

## Architecture Style

**Pattern**: {Monorepo / Layered / Modular / Microservices / Monolith}

**Rationale**: {Why this pattern was chosen. What problems it solves. What constraints it addresses.}

## Key Design Decisions

### {Decision 1 Title}

**Context**: {What situation or problem prompted this decision}

**Decision**: {What was decided}

**Rationale**: {Why this approach over alternatives}

**Trade-offs**: {What we gave up or accepted}

### {Decision 2 Title}

{Same structure}

## System Boundaries

| Boundary | Responsibility | Communication |
|----------|----------------|---------------|
| {Name} | {What it owns} | {How it talks to others} |

## Constraints

- {Technical constraint and why it exists}
- {Business constraint and its impact on architecture}
```

## 02-directory-structure.md

```markdown
# Directory Structure

## Layout

```
project-root/
├── src/                    # {Purpose}
│   ├── {folder}/           # {Purpose}
│   └── {folder}/           # {Purpose}
├── tests/                  # {Purpose}
├── docs/                   # Documentation
└── {config files}          # {Purpose}
```

## Design Rationale

### Why This Organization

{Explain the reasoning behind the directory structure. What principles guided the organization.}

### Module Boundaries

| Directory | Responsibility | Dependencies |
|-----------|----------------|--------------|
| `src/{module}` | {Single responsibility} | {What it depends on} |

### Colocation Strategy

{Explain what is colocated and why. E.g., tests next to source, types with implementations, etc.}

## Conventions

- **{Pattern}**: {Where it applies and why}
- **{Pattern}**: {Where it applies and why}

## Anti-patterns to Avoid

- **{Anti-pattern}**: {Why it's problematic in this codebase}
```

## 03-core-components.md

```markdown
# Core Components

## Component Overview

```mermaid
classDiagram
    class ComponentA {
        +responsibility1()
        +responsibility2()
    }
    class ComponentB {
        +responsibility()
    }
    ComponentA --> ComponentB : uses
```

## Components

### {Component Name}

**Responsibility**: {Single sentence describing what this component owns}

**Location**: `src/{path}/`

**Key interfaces**:
- `{InterfaceName}` — {Purpose}

**Dependencies**:
- `{Dependency}` — {Why it depends on this}

**Design rationale**: {Why this component exists as a separate unit. What would break if merged elsewhere.}

### {Next Component}

{Same structure}

## Component Interactions

| From | To | Purpose | Pattern |
|------|----|---------|---------|
| {A} | {B} | {Why A calls B} | {sync/async/event} |

## Ownership Boundaries

{Explain what each component owns exclusively. Clarify shared vs owned resources.}
```

## 04-data-flow.md

```markdown
# Data Flow

## Overview

{1 paragraph describing how data moves through the system at a high level.}

## Primary Flow

```mermaid
sequenceDiagram
    participant User
    participant Entry
    participant Core
    participant Data
    participant DB

    User->>Entry: Request
    Entry->>Core: Validated input
    Core->>Data: Query/Command
    Data->>DB: SQL/Query
    DB-->>Data: Result
    Data-->>Core: Domain object
    Core-->>Entry: Response data
    Entry-->>User: Response
```

## Data Transformations

| Stage | Input | Output | Transformation |
|-------|-------|--------|----------------|
| Entry | Raw request | Validated DTO | Validation, parsing |
| Core | DTO | Domain model | Business rules |
| Data | Domain model | Persistence model | Serialization |

## State Management

### Where State Lives

| State Type | Location | Rationale |
|------------|----------|-----------|
| {Type} | {Where} | {Why here} |

### State Flow Rules

- {Rule about state mutation}
- {Rule about state access}

## Error Flow

```mermaid
flowchart LR
    Error[Error occurs] --> Catch[Caught at boundary]
    Catch --> Transform[Transform to user error]
    Transform --> Log[Log internal details]
    Transform --> Return[Return safe message]
```

## Caching Strategy

{If applicable: what is cached, where, why, and invalidation strategy.}
```

## Mermaid Diagram Patterns

### Flowchart (System Overview)

```mermaid
flowchart TB
    subgraph GroupName[Label]
        A[Component]
        B[Component]
    end
    A --> B
```

### Sequence (Data Flow)

```mermaid
sequenceDiagram
    participant A
    participant B
    A->>B: Sync call
    B-->>A: Response
    A-)B: Async call
```

### Class (Components)

```mermaid
classDiagram
    class ClassName {
        +publicMethod()
        -privateField
    }
    ClassA --> ClassB : relationship
```

### ER (Data Models)

```mermaid
erDiagram
    User ||--o{ Order : places
    Order ||--|{ LineItem : contains
```

## Writing Guidelines

### Do

- Explain **why** decisions were made
- Document **trade-offs** accepted
- Describe **boundaries** and their purpose
- Include **constraints** that shaped the design
- Reference modules/directories (stable) not line numbers (unstable)

### Don't

- Write step-by-step tutorials
- Include implementation details that change frequently
- Repeat information from code comments
- Describe "how to use" (that's onboarding)
- Use line-number references that go stale
