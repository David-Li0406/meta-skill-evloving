---
name: c4-diagram-generator
description: Use this skill to generate architecture documentation and diagrams using the C4 model in Mermaid syntax. Activate when asked to create architecture diagrams, document system architecture, or visualize software structure.
---

# C4 Diagram Generator

Generate software architecture documentation and diagrams using C4 model diagrams in Mermaid syntax.

## Workflow

1. **Understand scope** - Determine which C4 level(s) are needed based on audience.
2. **Analyze codebase** - Explore the system to identify components, containers, and relationships.
3. **Generate diagrams** - Create Mermaid C4 diagrams at appropriate abstraction levels.
4. **Document** - Write diagrams to markdown files with explanatory context.

## C4 Diagram Levels

Select the appropriate level based on the documentation need:

| Level | Diagram Type | Audience | Shows | When to Create |
|-------|--------------|----------|-------|----------------|
| 1     | **C4Context** | Everyone | System + external actors | Always (required) |
| 2     | **C4Container** | Technical | Apps, databases, services | Always (required) |
| 3     | **C4Component** | Developers | Internal components | Only if adds value |
| 4     | **C4Deployment** | DevOps | Infrastructure nodes | For production systems |
| -     | **C4Dynamic** | Technical | Request flows (numbered) | For complex workflows |

**Key Insight:** "Context + Container diagrams are sufficient for most software development teams." Only create Component/Code diagrams when they genuinely add value.

## Quick Start Examples

### System Context (Level 1)
```mermaid
C4Context
  title System Context - <system-name>

  Person(user, "User", "Description")
  System(app, "<App Name>", "Description")
  System_Ext(browser, "Web Browser", "Description")

  Rel(user, app, "Uses")
  Rel(app, browser, "Persists data to", "Storage")
```

### Container Diagram (Level 2)
```mermaid
C4Container
  title Container Diagram - <system-name>

  Person(user, "User", "Description")

  Container_Boundary(app, "<App Name>") {
    Container(spa, "SPA", "Technology", "Description")
    ContainerDb(db, "Database", "Technology", "Description")
  }

  Rel(user, spa, "Uses")
  Rel(spa, db, "Reads/writes")
```

### Component Diagram (Level 3)
```mermaid
C4Component
  title Component Diagram - <feature-name>

  Container(views, "Views", "Description")

  Container_Boundary(feature, "<Feature Name>") {
    Component(comp1, "Component 1", "Technology", "Description")
    Component(comp2, "Component 2", "Technology", "Description")
  }

  Rel(views, comp1, "Uses")
  Rel(comp1, comp2, "Interacts with")
```

### Deployment Diagram
```mermaid
C4Deployment
  title Deployment Diagram - <environment>

  Deployment_Node(node, "Node Type", "Description") {
    Container(app, "Application", "Technology", "Description")
  }

  Rel(app, db, "Reads/writes", "Protocol")
```

## Element Syntax

### People and Systems
```
Person(alias, "Label", "Description")
System(alias, "Label", "Description")
System_Ext(alias, "Label", "Description")
```

### Containers
```
Container(alias, "Label", "Technology", "Description")
ContainerDb(alias, "Label", "Technology", "Description")
```

### Components
```
Component(alias, "Label", "Technology", "Description")
```

### Relationships
```
Rel(from, to, "Label")
```

## Best Practices

1. **Every element must have**: Name, Type, Technology (where applicable), and Description.
2. **Use unidirectional arrows only** - Bidirectional arrows create ambiguity.
3. **Label arrows with action verbs** - "Sends email using", "Reads from", not just "uses".
4. **Stay under 20 elements per diagram** - Split complex systems into multiple diagrams.

## Output Location

Write architecture documentation to `docs/architecture/` with naming convention:
- `c4-context.md` - System context diagram
- `c4-containers.md` - Container diagram
- `c4-components-{feature}.md` - Component diagrams per feature
- `c4-deployment.md` - Deployment diagram
- `c4-dynamic-{flow}.md` - Dynamic diagrams for specific flows

## Validation

After saving the diagram, always instruct the user to validate:

```
✅ Diagram created: {path}

📋 VALIDATION REQUIRED:
1. Open the file in VS Code
2. Install Mermaid Preview extension if needed
3. Verify diagram renders correctly
4. Report any syntax errors
```

## References

- [C4 Syntax Documentation](references/c4-syntax.md) - Complete Mermaid C4 syntax
- [Common Mistakes](references/common-mistakes.md) - Anti-patterns to avoid
- [Advanced Patterns](references/advanced-patterns.md) - Microservices, event-driven, deployment