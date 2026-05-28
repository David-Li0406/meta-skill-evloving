---
name: mermaid-diagrams
description: 'Create and embed Mermaid diagrams in Markdown files for visualizing documentation, features, architecture, workflows, and processes. Use when asked to "add a diagram", "create a flowchart", "visualize the workflow", "show the architecture", or when documentation needs visual enhancement. Supports flowcharts, sequence diagrams, class diagrams, state diagrams, ER diagrams, Gantt charts, pie charts, and more.'
---

# Mermaid Diagrams

Create visual diagrams directly in Markdown files using Mermaid syntax. Diagrams render automatically on GitHub, in VS Code, and many other Markdown viewers.

## When to Use This Skill

- User asks to "add a diagram", "create a chart", "visualize", or "show graphically"
- Documentation needs visual representation of workflows, processes, or architecture
- Feature files or ADRs would benefit from visual diagrams
- Explaining complex logic flows, state machines, or relationships
- Creating documentation for system architecture or data models
- Visualizing timelines, schedules, or project plans

## Supported Diagram Types

| Type | Use For | Example Triggers |
|------|---------|------------------|
| **Flowchart** | Processes, decision trees, workflows | "show the flow", "decision logic" |
| **Sequence Diagram** | Interactions, API calls, message flows | "show the sequence", "API interaction" |
| **Class Diagram** | Object structures, relationships | "class structure", "data model" |
| **State Diagram** | State machines, transitions | "state transitions", "lifecycle" |
| **Entity Relationship** | Database schemas, data models | "database schema", "ER diagram" |
| **Gantt Chart** | Timelines, project schedules | "timeline", "project schedule" |
| **Pie Chart** | Proportions, distributions | "distribution", "breakdown" |
| **Git Graph** | Git branching strategies | "git workflow", "branching strategy" |
| **Mindmap** | Hierarchical concepts | "concept map", "hierarchy" |
| **Timeline** | Historical events, milestones | "history", "milestones" |
| **Quadrant Chart** | 2D categorization | "prioritization", "quadrants" |
| **User Journey** | User experiences, flows | "user flow", "journey map" |

## Creating Mermaid Diagrams

### Basic Syntax

Wrap Mermaid code in fenced code blocks with `mermaid` language identifier:

````markdown
```mermaid
<diagram-type>
  <diagram-content>
```
````

### Flowchart Example

````markdown
```mermaid
flowchart TD
    Start([Start]) --> Input[Get User Input]
    Input --> Validate{Valid?}
    Validate -->|Yes| Process[Process Data]
    Validate -->|No| Error[Show Error]
    Process --> Save[(Save to DB)]
    Save --> End([End])
    Error --> Input
```
````

### Sequence Diagram Example

````markdown
```mermaid
sequenceDiagram
    participant User
    participant API
    participant Database

    User->>API: POST /create
    API->>Database: INSERT query
    Database-->>API: Success
    API-->>User: 201 Created
```
````

### Class Diagram Example

````markdown
```mermaid
classDiagram
    class Module {
        +String name
        +String version
        +deploy()
        +validate()
    }
    class Resource {
        +String id
        +Map tags
    }
    Module --> Resource : creates
```
````

### State Diagram Example

````markdown
```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> Running : start
    Running --> Completed : success
    Running --> Failed : error
    Failed --> Pending : retry
    Completed --> [*]
```
````

### Entity Relationship Diagram Example

````markdown
```mermaid
erDiagram
    MODULE ||--o{ RESOURCE : creates
    MODULE {
        string name
        string version
        string provider
    }
    RESOURCE {
        string id
        string type
        map tags
    }
```
````

### Gantt Chart Example

````markdown
```mermaid
gantt
    title Implementation Timeline
    dateFormat YYYY-MM-DD
    section Phase 1
    Design           :2026-01-01, 7d
    Implementation   :2026-01-08, 14d
    section Phase 2
    Testing          :2026-01-22, 7d
    Deployment       :2026-01-29, 3d
```
````

## Best Practices

### 1. Choose the Right Diagram Type

| Need | Recommended Type |
|------|------------------|
| Show process steps | Flowchart |
| Show interactions | Sequence Diagram |
| Show data structure | Class Diagram or ER Diagram |
| Show state changes | State Diagram |
| Show timeline | Gantt Chart or Timeline |
| Show proportions | Pie Chart |
| Show branching | Git Graph |
| Show concepts | Mindmap |

### 2. Keep Diagrams Simple

- **Limit nodes**: 10-15 nodes per diagram (split complex flows)
- **Use clear labels**: Short, descriptive text
- **Avoid clutter**: One main concept per diagram
- **Use subgraphs**: Group related elements

### 3. Use Consistent Styling

````markdown
```mermaid
flowchart LR
    style Start fill:#90EE90
    style End fill:#FFB6C1
    style Error fill:#FFA07A

    Start --> Process
    Process --> End
    Process --> Error
```
````

### 4. Add Descriptive Context

Always add explanatory text before and/or after diagrams:

````markdown
## Deployment Workflow

The following diagram shows the complete deployment process from code commit to production:

```mermaid
flowchart TD
    Commit --> CI
    CI --> Test
    Test --> Deploy
```

After deployment, the system automatically runs health checks and monitoring.
````

## Common Patterns

### Agent Handoff Workflow

````markdown
```mermaid
flowchart LR
    Plan[Implementation Plan] --> Shaper[Scenario Shaper]
    Shaper --> Tester[Terraform Tester]
    Tester --> Module[Module Specialist]
    Module --> Docs[Documentation]
    Docs --> Examples[Examples]

    Module -.feedback.-> Tester
    Module -.feedback.-> Shaper
    Docs -.feedback.-> Module
    Examples -.feedback.-> Module
```
````

### TDD Workflow

````markdown
```mermaid
stateDiagram-v2
    [*] --> WriteScenario
    WriteScenario --> WriteTest
    WriteTest --> RunTest
    RunTest --> TestFails
    TestFails --> Implement
    Implement --> RunTest
    RunTest --> TestPasses
    TestPasses --> Refactor
    Refactor --> [*]
```
````

### Module Architecture

````markdown
```mermaid
graph TB
    subgraph "Module Root"
        Main[main.tf]
        Vars[variables.tf]
        Outputs[outputs.tf]
    end

    subgraph "Examples"
        Basic[examples/basic/]
        Complete[examples/complete/]
    end

    subgraph "Tests"
        Unit[tests/unit.tftest.hcl]
        Integration[tests/integration.tftest.hcl]
    end

    Main --> Examples
    Tests -.validates.-> Main
```
````

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Diagram not rendering | Check syntax, ensure language is `mermaid` not `mmd` |
| Syntax errors | Validate at [Mermaid Live Editor](https://mermaid.live/) |
| Diagram too complex | Split into multiple smaller diagrams |
| Text overlapping | Use shorter labels or adjust direction (TD, LR, etc.) |
| Links not clickable | Use `click` syntax: `click Node "https://url"` |

## Advanced Features

### Clickable Nodes

````markdown
```mermaid
flowchart LR
    A[Documentation] --> B[Examples]
    click A "https://github.com/repo/docs" "View Docs"
    click B "https://github.com/repo/examples" "View Examples"
```
````

### Styling and Themes

````markdown
```mermaid
%%{init: {'theme':'forest'}}%%
flowchart TD
    A --> B
```
````

Available themes: `default`, `forest`, `dark`, `neutral`, `base`

### Subgraphs for Organization

````markdown
```mermaid
flowchart TB
    subgraph "Frontend"
        UI[User Interface]
        API[API Client]
    end

    subgraph "Backend"
        Server[API Server]
        DB[(Database)]
    end

    UI --> API
    API --> Server
    Server --> DB
```
````

## References

- **Mermaid Syntax Reference**: <https://mermaid.js.org/intro/syntax-reference.html>
- **GitHub Diagrams Documentation**: <https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams>
- **Mermaid Live Editor**: <https://mermaid.live/> (for testing/validation)
- **Flowchart Syntax**: <https://mermaid.js.org/syntax/flowchart.html>
- **Sequence Diagram Syntax**: <https://mermaid.js.org/syntax/sequenceDiagram.html>
- **Class Diagram Syntax**: <https://mermaid.js.org/syntax/classDiagram.html>
- **State Diagram Syntax**: <https://mermaid.js.org/syntax/stateDiagram.html>
- **ER Diagram Syntax**: <https://mermaid.js.org/syntax/entityRelationshipDiagram.html>
- **Gantt Chart Syntax**: <https://mermaid.js.org/syntax/gantt.html>

## Quick Start Checklist

- [ ] Identify what needs visualization
- [ ] Choose appropriate diagram type
- [ ] Draft diagram structure (nodes, connections, flow)
- [ ] Add Mermaid code block to Markdown file
- [ ] Validate syntax at [mermaid.live](https://mermaid.live/)
- [ ] Add explanatory text around diagram
- [ ] Test rendering on GitHub/VS Code
- [ ] Refine styling and layout if needed
