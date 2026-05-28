# Mermaid Diagrams

## Configuration

```yaml
# mkdocs.yml
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
```

## Syntax

All diagrams use mermaid code fence:

````markdown
```mermaid
[diagram code]
```
````

## Flowcharts

```mermaid
graph LR
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

**Direction:** `TB` (top-bottom), `BT`, `LR` (left-right), `RL`

**Node shapes:**
- `[text]` - rectangle
- `(text)` - rounded
- `{text}` - diamond
- `((text))` - circle

## Sequence Diagrams

```mermaid
sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello
    B-->>A: Hi back
    A->>B: How are you?
    Note over A,B: Conversation
```

**Arrows:** `->>` solid, `-->>` dashed, `-x` cross end

## State Diagrams

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Running: start
    Running --> Idle: stop
    Running --> [*]: finish
```

## Class Diagrams

```mermaid
classDiagram
    Animal <|-- Duck
    Animal <|-- Fish
    Animal: +int age
    Animal: +move()
    Duck: +swim()
```

## Entity-Relationship

```mermaid
erDiagram
    USER ||--o{ POST : creates
    USER {
        int id
        string name
    }
    POST {
        int id
        string title
    }
```

**Relationships:** `||` one, `o{` many, `|{` one-or-more
