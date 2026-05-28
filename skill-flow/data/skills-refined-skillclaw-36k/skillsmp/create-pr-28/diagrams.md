# Mermaid Diagram Guidelines

Create diagrams that accurately represent changes. Complexity should match PR scope.

## Architecture Diagrams

### Simple Component Change

```mermaid
flowchart TD
    A[Component] --> B[Hook]
    B --> C[Provider]
```

### Multi-Service Integration

```mermaid
graph TB
    subgraph "Application"
        W[withOTelSpan]
    end

    subgraph "Instrumented Services"
        AL[Algolia]
        SS[Shopify Storefront]
        CS[Contentstack]
    end

    subgraph "Monitoring"
        S[Span table]
    end

    AL --> W
    SS --> W
    CS --> W
    W -->|OTLP export| S
```

## Data Flow Diagrams

### Simple Flow

```mermaid
sequenceDiagram
    participant C as Component
    participant P as Provider
    C->>P: dispatch
    P-->>C: updated state
```

### Multi-Step Flow with Conditionals

```mermaid
sequenceDiagram
    participant App as Application
    participant OTel as Wrapper
    participant Svc as External Service
    participant NR as Monitoring

    App->>OTel: Request
    OTel->>OTel: Start span
    OTel->>Svc: HTTP request
    Svc-->>OTel: Response
    OTel->>OTel: End span

    alt Server-side
        OTel->>NR: OTLP export
    else Browser-side
        OTel->>NR: Events API
    end

    OTel-->>App: Return response
```

## Tips

- Use subgraphs to group related components
- Use `alt` blocks in sequence diagrams for conditional flows
- Label arrows with actions/data being passed
- Match diagram complexity to PR complexity
- Include all affected services for integration changes
- Mermaid diagrams render natively in GitHub PR descriptions

## When to Include Diagrams

**Include architecture diagram when:**
- Adding new components or services
- Changing how components interact
- Integration with external systems

**Include data flow diagram when:**
- Changing request/response patterns
- Adding new API calls
- Modifying state management

**Skip diagrams when:**
- Simple bug fixes
- Documentation changes
- Minor refactors with no structural changes
