---
name: mermaid-diagram
description: Generate well-structured Mermaid diagrams for visual documentation. Use when designing systems, documenting workflows, creating architecture diagrams, or any task requiring visual representation of processes, relationships, or structures. Triggers include requests like "create a diagram", "visualize this", "show the flow", "draw the architecture", or when explaining complex systems that benefit from visual aids.
---

# Mermaid Diagram

Generate proper, well-structured Mermaid diagrams for visual documentation and design presentations.

## Diagram Selection

| Need | Diagram | Reference |
|------|---------|-----------|
| Process flow, decisions | Flowchart | [flowchart.md](references/flowchart.md) |
| API/service interactions | Sequence | [sequence.md](references/sequence.md) |
| Object-oriented design | Class | [class.md](references/class.md) |
| Database schema | ER Diagram | [er.md](references/er.md) |
| State machines, lifecycles | State | [state.md](references/state.md) |
| Software architecture (C4) | C4 | [c4.md](references/c4.md) |
| Cloud/infrastructure | Architecture | [architecture.md](references/architecture.md) |
| Brainstorming, concepts | Mindmap | [mindmap.md](references/mindmap.md) |
| Timelines, charts, git | Other | [other-diagrams.md](references/other-diagrams.md) |

## Quick Examples

### Flowchart
```mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[Other]
    C --> E[End]
    D --> E
```

### Sequence
```mermaid
sequenceDiagram
    Client->>+API: Request
    API->>DB: Query
    DB-->>API: Data
    API-->>-Client: Response
```

### Class
```mermaid
classDiagram
    class Animal {
        +String name
        +makeSound()
    }
    Animal <|-- Dog
    Animal <|-- Cat
```

### ER
```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ITEM : contains
```

## Best Practices

1. **Choose the right diagram** - Match diagram type to what you're representing
2. **Keep it readable** - Limit nodes, use clear labels, avoid crossing lines
3. **Use direction** - `LR` for wide diagrams, `TD` for tall ones
4. **Group related items** - Use subgraphs, boundaries, or namespaces
5. **Add context** - Use notes and labels to explain non-obvious elements
6. **Style sparingly** - Only highlight what needs attention

## Output Format

Always wrap diagrams in fenced code blocks:

````
```mermaid
flowchart LR
    A --> B
```
````

Consult the appropriate reference file for detailed syntax before generating complex diagrams.
