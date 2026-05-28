---
name: deepwiki-ascii-diagrams
description: ASCII diagram generation skill for creating professional architectural diagrams in text format. Supports C4 models, sequence diagrams, component diagrams, deployment diagrams, data flow diagrams, class diagrams, and integration diagrams for technical documentation.
tools: Read, Write
---

# ASCII Diagram Generation Skill

Professional ASCII-based diagram generation for technical documentation. This skill provides templates and guidelines for creating clean, maintainable architectural diagrams that integrate seamlessly into documentation systems.

## Diagram Standards

### ASCII Character Sets

**Standard Boxes (Components, Services)**
```
┌─────────────────┐
│   Component     │
│    or Service   │
└─────────────────┘
```

**Double-Line Boxes (External Systems, APIs)**
```
╔═════════════════╗
║   External      ║
║   System/API    ║
╚═════════════════╝
```

**Bold/Heavy Boxes (Databases, Storage)**
```
┏━━━━━━━━━━━━━━━━━┓
┃    Database     ┃
┃    or Storage   ┃
┗━━━━━━━━━━━━━━━━━┛
```

**Dashed Boxes (Optional, Conditional)**
```
┌┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┐
┆  Optional      ┆
┆  Component     ┆
└┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┘
```

### Connection Types

| Symbol | Meaning | Usage |
|--------|---------|-------|
| `────►` | Synchronous request | Direct API calls, HTTP requests |
| `◄────►` | Bidirectional | WebSocket, duplex connections |
| `- - - - ►` | Asynchronous/Event | Message queues, events, webhooks |
| `════════►` | Data flow | Large data transfers, streaming |
| `······►` | Optional/Conditional | Optional integrations |
| `~~~~►` | Real-time/WebSocket | WebSocket connections |

### Connection Labels

```
   "GET /api/users"
        ↓
    ┌────────┐
    │API     │
    │Gateway │
    └────────┘
        ↓
   "JSON response"
```

Connection labels should be placed:
- **Above arrows** for top-to-bottom flows
- **Beside arrows** for left-to-right flows
- **In brackets [like this]** for explanatory notes
- **With protocol names** for technical clarity

## Quality Guidelines

### Layout Principles

1. **Alignment**: Related components should align vertically or horizontally
2. **Spacing**: Minimum 2 characters between unconnected elements
3. **Consistency**: Use same box sizes for same-level components
4. **Hierarchy**: Position parent systems above children
5. **Flow Direction**: Left-to-right or top-to-bottom (consistent throughout)

### Readability Standards

- **Line Width**: Maximum 100 characters per line
- **Box Height**: Minimum 3 lines (1 content + 2 borders)
- **Box Width**: Minimum 15 characters for labels
- **Nesting**: Maximum 3 levels deep in containment hierarchies
- **Labels**: Always label connections with protocol/action names

### Naming Conventions

- **Component Names**: PascalCase, descriptive, concise
- **Connection Labels**: snake_case or UPPER_CASE for protocols (HTTP, TCP, gRPC)
- **Annotations**: [Lowercase description in brackets]

## Diagram Types

### 1. C4 Model Diagrams
Hierarchical system decomposition (System, Container, Component, Code)

**Best for**: Architecture documentation, system overviews

**Characteristics**:
- Shows hierarchical relationships
- Clear responsibility boundaries
- Progressive detail levels

### 2. Sequence Diagrams
Interaction flows between components over time

**Best for**: API flows, transaction sequences, user journeys

**Characteristics**:
- Time flows top to bottom
- Clear message ordering
- Actor/component lifelines

### 3. Component Diagrams
Internal structure of a system/container

**Best for**: Service internals, module relationships

**Characteristics**:
- Shows interfaces/ports
- Internal dependencies
- Clear component roles

### 4. Deployment Diagrams
Physical/cloud deployment architecture

**Best for**: Infrastructure documentation, deployment guides

**Characteristics**:
- Shows servers, containers, networks
- Resource allocation
- Environment separation

### 5. Data Flow Diagrams
Data movement through systems

**Best for**: ETL pipelines, data architecture, streaming flows

**Characteristics**:
- Focus on data transformations
- Clear source/destination
- Transformation steps highlighted

### 6. Class Diagrams
Object-oriented structure

**Best for**: Domain models, data structures

**Characteristics**:
- Shows attributes and methods
- Inheritance relationships
- Aggregation/composition

### 7. Integration Diagrams
System-to-system communication patterns

**Best for**: Microservices, third-party integrations

**Characteristics**:
- Multiple independent systems
- Clear integration points
- Protocol specification

## Common Patterns

### Layered Architecture
```
┌───────────────────────────────┐
│    Presentation Layer         │
├───────────────────────────────┤
│    Business Logic Layer       │
├───────────────────────────────┤
│    Data Access Layer          │
├───────────────────────────────┤
│    Database Layer             │
└───────────────────────────────┘
```

### Client-Server Pattern
```
┌─────────────┐                ┌──────────────┐
│   Client    │───HTTP────────►│   Server     │
│  (Browser)  │◄───JSON────────│ (REST API)   │
└─────────────┘                └──────────────┘
```

### Microservices Pattern
```
┌──────────────┐
│API Gateway   │
└──────┬───────┘
       │
   ┌───┼────┬────────┬────────┐
   │   │    │        │        │
   ▼   ▼    ▼        ▼        ▼
┌─────────────────────────────────┐
│User │Product│Order │Payment│Auth│
│Svc  │  Svc  │ Svc  │ Svc   │Svc │
└─────────────────────────────────┘
```

## Best Practices

### Do's ✓
- Use consistent spacing and alignment
- Label all connections with purpose/protocol
- Include data format in labels (JSON, XML, Binary)
- Add [bracketed notes] for clarification
- Test readability at actual line width
- Version control diagrams as code
- Use descriptive component names

### Don'ts ✗
- Mix connection styles without reason
- Create crossing lines (reorder components instead)
- Overcrowd diagrams (split complex ones)
- Use ambiguous or generic names
- Forget connection labels
- Make lines longer than 100 characters
- Stack too many layers deeply

## Integration with Documentation

These diagrams integrate with documentation systems via:

1. **Markdown Code Blocks**: Wrapped in triple backticks
2. **Alt Text**: Provide descriptive alt-text below diagrams
3. **Captions**: Add [bracketed explanatory captions]
4. **File Organization**: Store in `docs/diagrams/` directory
5. **Naming**: Use pattern `{system}-{diagram-type}.md` or `.txt`

### Markdown Example
````markdown
## System Architecture

```
┌──────────────┐
│   Service    │
└──────────────┘
```

[Description of what this diagram shows and key components]
````

## Examples Reference

See the template files for complete examples:
- `c4-diagram.md` - System hierarchy examples
- `sequence-diagram.md` - Interaction flow examples
- `component-diagram.md` - Internal structure examples
- `deployment-diagram.md` - Infrastructure examples
- `data-flow-diagram.md` - ETL and data pipeline examples
- `class-diagram.md` - Data model examples
- `integration-diagram.md` - Multi-system examples

## Tools and Utilities

### ASCII Box Drawing Tools
- Unicode box-drawing characters (see Diagram Standards section)
- Alignment: Use monospace font consistently
- Testing: View in Markdown preview before publishing

### Document Generation
- Integrate with Python documentation tools (Sphinx, MkDocs)
- Use UTF-8 encoding for box-drawing characters
- Render in monospace font (Courier New, Consolas, Menlo)

---

**Version**: 1.0
**Last Updated**: 2026-01-02
**Maintained by**: DeepWiki Documentation System
