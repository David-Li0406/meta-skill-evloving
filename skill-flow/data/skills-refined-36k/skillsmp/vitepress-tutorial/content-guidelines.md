# Content Writing Guidelines

## Core Principles

1. **Explain "How", not "What to do"** - Focus on implementation details, not usage instructions
2. **Reference Real Code** - Always include actual source file paths and line numbers
3. **Visual First** - Use Mermaid diagrams before lengthy text explanations
4. **Progressive Depth** - Start with overview, then dive into details

## Chapter Structure

### Standard Chapter Template

```markdown
---
outline: [2, 3]
prev:
  text: 'Previous Chapter'
  link: '/module/prev'
next:
  text: 'Next Chapter'
  link: '/module/next'
---

# Chapter Title

Brief introduction (2-3 sentences) explaining what this chapter covers.

## Overview Diagram

\`\`\`mermaid
flowchart TD
    A[Step 1] --> B[Step 2]
    B --> C[Step 3]
\`\`\`

## Source Location

\`\`\`
path/to/source/
├── file1.go      # Description
├── file2.go      # Description
└── subdir/
    └── file3.go  # Description
\`\`\`

## Core Concept 1

**Source**: `path/to/file.go`

Explanation of the concept.

\`\`\`go
// path/to/file.go

func ExampleFunction() {
    // Key implementation
}
\`\`\`

### Sub-topic

More detailed explanation with code.

## Core Concept 2

...

## Summary

- **Point 1** - Brief recap
- **Point 2** - Brief recap
- **Point 3** - Brief recap

Next chapter: [Next Topic](/module/next)
```

## Source Code References

### Inline Reference
```markdown
The `CreateSandbox` function in `apps/runner/pkg/docker/create.go` handles...
```

### Block Reference
```markdown
**Source**: `apps/runner/pkg/docker/create.go`

\`\`\`go
// apps/runner/pkg/docker/create.go

func (d *DockerClient) CreateSandbox(ctx context.Context, opts CreateOptions) error {
    // Implementation
}
\`\`\`
```

### With Line Numbers
```markdown
**Source**: `apps/runner/pkg/docker/create.go:45-67`
```

## Mermaid Diagram Patterns

### Architecture Diagram
```markdown
\`\`\`mermaid
flowchart TD
    subgraph External
        Client[SDK Client]
    end

    subgraph Internal
        API[API Server]
        Worker[Worker]
        DB[(Database)]
    end

    Client --> API
    API --> Worker
    Worker --> DB
\`\`\`
```

### Sequence Diagram
```markdown
\`\`\`mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant D as Database

    C->>A: Request
    A->>D: Query
    D-->>A: Result
    A-->>C: Response
\`\`\`
```

### State Diagram
```markdown
\`\`\`mermaid
stateDiagram-v2
    [*] --> Creating
    Creating --> Started: success
    Creating --> Error: failure
    Started --> Stopped: stop
    Stopped --> Started: start
    Stopped --> [*]: destroy
\`\`\`
```

### Flowchart with Decision
```markdown
\`\`\`mermaid
flowchart TD
    A[Start] --> B{Condition?}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
\`\`\`
```

## Tables

### API Endpoint Table
```markdown
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sandboxes` | POST | Create sandbox |
| `/sandboxes/{id}` | GET | Get sandbox |
| `/sandboxes/{id}` | DELETE | Delete sandbox |
```

### Data Structure Table
```markdown
| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Unique identifier |
| `status` | `enum` | Current state |
| `createdAt` | `time.Time` | Creation timestamp |
```

### Comparison Table
```markdown
| Aspect | Option A | Option B |
|--------|----------|----------|
| Performance | Fast | Slower |
| Complexity | High | Low |
| Use Case | Production | Development |
```

## Code Block Best Practices

### Language Specification
```markdown
\`\`\`go
// Go code
\`\`\`

\`\`\`typescript
// TypeScript code
\`\`\`

\`\`\`bash
# Shell commands
\`\`\`

\`\`\`json
{
  "json": "data"
}
\`\`\`
```

### Highlighting Key Lines
```markdown
\`\`\`go{3-5}
func Example() {
    // Normal line
    // Highlighted line 1
    // Highlighted line 2
    // Highlighted line 3
    // Normal line
}
\`\`\`
```

### Simplified Code
When showing implementation patterns, simplify error handling:
```markdown
\`\`\`go
// Simplified - error handling omitted for clarity
result, _ := doSomething()
\`\`\`
```

## Writing Style

### Language
- **Content**: Chinese (Simplified)
- **Code comments**: English
- **Technical terms**: Keep in English (API, Docker, Daemon, etc.)

### Tone
- Direct and technical
- Avoid marketing language
- Assume reader has programming experience

### Length Guidelines
- Chapter: 200-400 lines
- Section: 50-100 lines
- Paragraph: 3-5 sentences
- Code blocks: 10-30 lines (simplify if longer)

## Navigation

### Chapter Ordering
1. Overview/Introduction first
2. Core concepts in logical order
3. Advanced topics last
4. Summary/Conclusion at end

### Cross-References
```markdown
See [Lifecycle Management](/sandbox/lifecycle) for details.

As discussed in the [Architecture](/introduction/architecture) chapter...
```

### Callouts (Custom Containers)
```markdown
::: tip
Helpful tip here.
:::

::: warning
Important warning.
:::

::: danger
Critical information.
:::

::: info
Additional context.
:::
```

## Content Checklist

Before completing a chapter:

- [ ] Frontmatter with prev/next links
- [ ] Source file paths included
- [ ] At least one Mermaid diagram
- [ ] Code blocks have language specified
- [ ] Summary section at end
- [ ] No orphan links
- [ ] Chinese content, English code comments
