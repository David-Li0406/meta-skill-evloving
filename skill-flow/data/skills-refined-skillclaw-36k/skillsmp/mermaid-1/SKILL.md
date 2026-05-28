---
name: mermaid
description: "Create text-based diagrams using Mermaid syntax. Perfect for version-controlled diagrams that render in GitHub, documentation sites, and markdown files."
allowed-tools: [Read, Write, Edit, Bash]
---

# Nano Banana - Mermaid Diagrams

## Overview

Create diagrams using Mermaid's text-based syntax. Mermaid diagrams are version-controllable, render natively in GitHub/GitLab, and are perfect for documentation.

**Key Features:**
- 📝 **Text-Based**: Diagrams as code, easy to version control
- 🔄 **Git-Friendly**: Diff-able, merge-able, reviewable
- 🌐 **Wide Support**: GitHub, GitLab, Notion, Obsidian, and more
- 🎨 **Customizable**: Themes and styling options

## When to Use Mermaid

| Use Mermaid When... | Use AI Diagrams When... |
|---------------------|------------------------|
| Diagrams need version control | One-off visualization needed |
| Team collaboration on diagrams | High visual polish required |
| Diagrams in markdown docs | Complex custom styling needed |
| Frequent diagram updates | Photo-realistic or artistic |
| GitHub/GitLab rendering | Publication-quality required |

## Supported Diagram Types

### 1. Flowcharts

```mermaid
flowchart TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Great!]
    B -->|No| D[Debug]
    D --> B
    C --> E[End]
```

**Syntax:**
```
flowchart TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Great!]
    B -->|No| D[Debug]
    D --> B
    C --> E[End]
```

**Directions:** `TD` (top-down), `LR` (left-right), `BT` (bottom-top), `RL` (right-left)

**Node Shapes:**
- `[text]` - Rectangle
- `(text)` - Rounded rectangle
- `{text}` - Diamond (decision)
- `([text])` - Stadium
- `[[text]]` - Subroutine
- `[(text)]` - Cylinder (database)

### 2. Sequence Diagrams

```mermaid
sequenceDiagram
    participant U as User
    participant A as App
    participant S as Server
    participant D as Database

    U->>A: Click Login
    A->>S: POST /auth/login
    S->>D: Query user
    D-->>S: User data
    S-->>A: JWT Token
    A-->>U: Redirect to dashboard
```

**Syntax:**
```
sequenceDiagram
    participant U as User
    participant A as App
    participant S as Server

    U->>A: Request
    A->>S: Forward
    S-->>A: Response
    A-->>U: Display
```

**Arrow Types:**
- `->` Solid line without arrow
- `-->` Dotted line without arrow
- `->>` Solid line with arrow
- `-->>` Dotted line with arrow
- `-x` Solid line with X
- `--x` Dotted line with X

### 3. Class Diagrams

```mermaid
classDiagram
    class User {
        +String id
        +String email
        +String name
        +login()
        +logout()
    }
    class Order {
        +String id
        +Date created
        +List~Item~ items
        +calculateTotal()
    }
    class Item {
        +String name
        +Float price
        +Int quantity
    }

    User "1" --> "*" Order : places
    Order "*" --> "*" Item : contains
```

### 4. Entity Relationship Diagrams

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "ordered in"

    USER {
        int id PK
        string email
        string name
    }
    ORDER {
        int id PK
        int user_id FK
        date created_at
    }
    LINE_ITEM {
        int order_id FK
        int product_id FK
        int quantity
    }
    PRODUCT {
        int id PK
        string name
        decimal price
    }
```

**Relationship Syntax:**
- `||--||` One to one
- `||--o{` One to many
- `}o--o{` Many to many

### 5. State Diagrams

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Review : Submit
    Review --> Approved : Approve
    Review --> Draft : Request Changes
    Approved --> Published : Publish
    Published --> Archived : Archive
    Archived --> [*]
```

### 6. Gantt Charts

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD

    section Planning
    Requirements     :a1, 2024-01-01, 7d
    Design           :a2, after a1, 14d

    section Development
    Backend API      :b1, after a2, 21d
    Frontend UI      :b2, after a2, 21d
    Integration      :b3, after b1, 7d

    section Testing
    QA Testing       :c1, after b3, 14d
    UAT              :c2, after c1, 7d
```

### 7. Pie Charts

```mermaid
pie title Technology Stack Distribution
    "Python" : 40
    "JavaScript" : 30
    "Go" : 20
    "Other" : 10
```

### 8. Git Graphs

```mermaid
gitGraph
    commit
    commit
    branch feature
    checkout feature
    commit
    commit
    checkout main
    merge feature
    commit
    branch hotfix
    checkout hotfix
    commit
    checkout main
    merge hotfix
```

## Using Mermaid in Documentation

### In Markdown Files

~~~markdown
# Architecture Overview

```mermaid
flowchart LR
    Client --> API
    API --> Database
    API --> Cache
```
~~~

### In GitHub README

GitHub automatically renders Mermaid in markdown files. Just use the fenced code block with `mermaid` language identifier.

### Export to PNG/SVG

Use Mermaid CLI for image export:

```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Export to PNG
mmdc -i diagram.mmd -o diagram.png

# Export to SVG
mmdc -i diagram.mmd -o diagram.svg

# With custom theme
mmdc -i diagram.mmd -o diagram.png -t dark
```

## Themes

```mermaid
%%{init: {'theme': 'forest'}}%%
flowchart LR
    A --> B --> C
```

**Available Themes:**
- `default` - Default Mermaid theme
- `forest` - Green tones
- `dark` - Dark mode
- `neutral` - Grayscale
- `base` - Minimal styling

## Best Practices

### Keep It Simple
```
# ✅ Good - Clear and readable
flowchart LR
    A[Input] --> B[Process] --> C[Output]

# ❌ Avoid - Too complex
flowchart LR
    A --> B --> C --> D --> E --> F --> G --> H
    B --> X --> Y --> Z
    C --> X
    D --> Y
```

### Use Meaningful Labels
```
# ✅ Good - Descriptive labels
flowchart TD
    Auth[Authentication Service] --> Users[(User Database)]

# ❌ Avoid - Generic labels
flowchart TD
    A --> B
```

### Group Related Elements
```mermaid
flowchart TB
    subgraph Frontend
        UI[React App]
        State[Redux Store]
    end

    subgraph Backend
        API[REST API]
        DB[(PostgreSQL)]
    end

    UI --> API
    API --> DB
```

## Integration with Nano Banana

For simple, version-controlled diagrams → Use **Mermaid**
For publication-quality, complex visuals → Use **diagram** skill

**Hybrid Approach:**
1. Draft diagram structure in Mermaid
2. Iterate on the design in version control
3. When finalized, generate polished version with `diagram` skill

## Resources

- [Mermaid Documentation](https://mermaid.js.org/intro/)
- [Live Editor](https://mermaid.live/)
- [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli)
- [GitHub Mermaid Support](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)
