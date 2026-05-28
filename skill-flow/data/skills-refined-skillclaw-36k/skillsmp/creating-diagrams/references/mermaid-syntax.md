# Mermaid Syntax Reference

## Flowcharts

### Basic Structure

```mermaid
flowchart LR
    A[Start] --> B[Process]
    B --> C{Decision}
    C -->|Yes| D[Action 1]
    C -->|No| E[Action 2]
```

### Directions

* `LR` - Left to Right
* `TD` or `TB` - Top Down / Top to Bottom
* `RL` - Right to Left
* `BT` - Bottom to Top

### Node Shapes

| Syntax     | Shape             | Use For            |
| ---------- | ----------------- | ------------------ |
| `[Text]`   | Rectangle         | Processes, steps   |
| `(Text)`   | Rounded rectangle | Start/end          |
| `{Text}`   | Diamond           | Decisions          |
| `[(Text)]` | Cylinder          | Databases          |
| `([Text])` | Stadium           | Events             |
| `[[Text]]` | Subroutine        | External processes |
| `((Text))` | Circle            | Connectors         |

### Subgraphs

```mermaid
flowchart TB
    subgraph Frontend
        A[React] --> B[Redux]
    end
    subgraph Backend
        C[API] --> D[Database]
    end
    B --> C
```

## Sequence Diagrams

### Basic Structure

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant D as Database

    C->>A: POST /data
    A->>A: Validate
    A->>D: INSERT
    D-->>A: Success
    A-->>C: 201 Created
```

### Arrow Types

| Syntax | Meaning                       |
| ------ | ----------------------------- |
| `->`   | Solid line without arrow      |
| `-->`  | Dotted line without arrow     |
| `->>`  | Solid line with arrow         |
| `-->>` | Dotted line with arrow        |
| `-x`   | Solid line with cross (async) |
| `--x`  | Dotted line with cross        |

### Notes and Activations

```mermaid
sequenceDiagram
    participant A
    participant B

    A->>+B: Request
    Note right of B: Processing
    B-->>-A: Response
```

### Loops and Alternatives

```mermaid
sequenceDiagram
    participant A
    participant B

    loop Every minute
        A->>B: Heartbeat
    end

    alt Success
        B-->>A: OK
    else Failure
        B-->>A: Error
    end
```

## State Diagrams

### Basic Structure

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Review: Submit
    Review --> Approved: Approve
    Review --> Draft: Reject
    Approved --> Published: Publish
    Published --> [*]
```

### Composite States

```mermaid
stateDiagram-v2
    [*] --> Active
    state Active {
        [*] --> Idle
        Idle --> Processing: Start
        Processing --> Idle: Complete
    }
    Active --> [*]: Shutdown
```

## Class Diagrams

### Basic Structure

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
    }
    class Dog {
        +String breed
        +bark()
    }
    Animal <|-- Dog
```

### Relationships

| Syntax  | Meaning     |
| ------- | ----------- |
| `<\|--` | Inheritance |
| `*--`   | Composition |
| `o--`   | Aggregation |
| `-->`   | Association |
| `..>`   | Dependency  |
| `..\|>` | Realization |

## Gantt Charts

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD

    section Phase 1
    Research     :a1, 2025-01-01, 14d
    Design       :a2, after a1, 10d

    section Phase 2
    Development  :b1, after a2, 30d
    Testing      :b2, after b1, 14d
```

## Entity Relationship

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ LINE_ITEM : contains
    PRODUCT ||--o{ LINE_ITEM : "ordered in"
```

### Relationship Syntax

| Syntax | Meaning      |
| ------ | ------------ |
| `\|\|` | Exactly one  |
| `o\|`  | Zero or one  |
| `}o`   | Zero or more |
| `}\|`  | One or more  |

## Styling

### Node Colors

```mermaid
flowchart LR
    A[Default]
    B[Styled]:::highlight

    classDef highlight fill:#f96,stroke:#333
```

### Link Styles

```mermaid
flowchart LR
    A --> B
    B -.-> C
    C ==> D
```

* `-->` Solid arrow
* `-.->` Dotted arrow
* `==>` Thick arrow

## Tips

* Keep diagrams simple - split complex flows into multiple diagrams
* Use clear, descriptive labels
* Follow natural reading direction (LR or TD)
* Group related items with subgraphs
* Test rendering in target environment (GitHub, VS Code, etc.)
