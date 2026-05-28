# Diagram Generation Guide

Mermaid patterns for architecture visualization in Linear issues.

## Best Practices

- **Target 5-15 nodes per diagram** (readable, not overwhelming)
- **Use multiple small diagrams** over one massive one
- **Hand-craft when needed** - layer output is a starting point
- **Include data flow diagrams** for full-stack features
- **Add sequence diagrams** for interaction-heavy features
- **Use visual indicators**: green=done, yellow=pending, red=issue

## Diagram Assembly Workflow

1. Generate a base graph (layer or outline).
2. Prune to the smallest set of nodes that explain the change.
3. Rename nodes to match domain language from the issue.
4. Annotate arrows with verbs (fetch, write, validate, render).
5. Add a short legend if color or status is used.

## Package Dependencies

From `layer --mode=packages`:

```mermaid
flowchart TD
  subgraph root["Root Layer"]
    admin["services/admin"]
    api["services/api"]
  end
  subgraph leaf["Leaf Layer"]
    lib["lib/"]
  end
  admin --> lib
  api --> lib

  style lib fill:#9f9,stroke:#333
```

## Data Flow

Hand-crafted based on analysis:

```mermaid
flowchart LR
  subgraph Frontend
    UI[Component] --> Hook[useQuery]
  end
  subgraph Backend
    Handler[API Handler] --> DB[(Database)]
  end
  Hook -->|"fetch"| Handler
  DB -->|"response"| Handler
  Handler -->|"JSON"| Hook
  Hook --> UI
```

## Implementation Steps

Step-by-step visualization:

```mermaid
flowchart TD
  A[1. Migration] -->|"add columns"| B[2. Type Update]
  B -->|"update types"| C[3. Schema Update]
  C -->|"Zod schema"| D[4. UI Component]
  D -->|"render fields"| E[5. API Response]
  E -->|"return data"| F[6. Test]
```

## Sequence Diagram

For interaction-heavy features:

```mermaid
sequenceDiagram
  participant User
  participant Component
  participant Hook
  participant API
  participant DB

  User->>Component: Action
  Component->>Hook: Call hook
  Hook->>API: Fetch data
  API->>DB: Query
  DB-->>API: Results
  API-->>Hook: JSON response
  Hook-->>Component: State update
  Component-->>User: Re-render
```

## ER Diagram

For schema changes:

```mermaid
erDiagram
  USERS ||--o{ USER_APPS : has
  APPS ||--o{ USER_APPS : followed_by

  USERS {
    int id PK
    string email
  }

  APPS {
    int id PK
    string name
  }

  USER_APPS {
    int user_id PK,FK
    int app_id PK,FK
    timestamp created_at
  }
```

## C4 Context (lightweight)

Use when the issue crosses multiple systems.

```mermaid
flowchart LR
  User[User] --> Web[Web App]
  Web --> API[API Service]
  API --> DB[(Database)]
  API --> ThirdParty[External API]
```

## State Diagram

For stateful UI or workflow transitions.

```mermaid
stateDiagram-v2
  [*] --> Idle
  Idle --> Loading: submit
  Loading --> Success: ok
  Loading --> Error: fail
  Error --> Idle: retry
  Success --> [*]
```

## Call Graph (outline)

Use for narrow code paths to show function flow.

```mermaid
flowchart TD
  A[handler] --> B[validateInput]
  B --> C[callService]
  C --> D[writeDatabase]
```

## Legend Pattern

```mermaid
flowchart LR
  A[Existing]:::existing
  B[New]:::new
  C[Risk]:::risk

  classDef existing fill:#cfc,stroke:#333
  classDef new fill:#ccf,stroke:#333
  classDef risk fill:#fcc,stroke:#333
```

## Generation Commands

```bash
# Package-level dependencies (monorepos)
layer . --mode=packages --format=mermaid

# File-level import graph
layer . --mode=files --format=mermaid

# Pipe specific files to layer
fd -e ts . src/hooks src/components | layer --stdin --mode=files --format=mermaid

# Focused on specific package/area
layer . --focus="packages/auth" --depth=2 --format=mermaid

# Show what depends ON a package (upstream)
layer . --dependents="lib" --format=mermaid

# Show what a package depends ON (downstream)
layer . --dependencies="services/api" --format=mermaid

# Create shareable gist
layer . --mode=files --format=mermaid --gist --gist-description="$ISSUE_ID architecture"

# Call graph from outline (narrow scope)
outline --graph --format=mermaid src/**/*.ts
```
