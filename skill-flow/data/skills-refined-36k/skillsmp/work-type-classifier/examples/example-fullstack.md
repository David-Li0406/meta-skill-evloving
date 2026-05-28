# Example: Fullstack Work Classification

## User Request
"Build a comment system with real-time updates"

## Classification Output

### Keyword Analysis

| Keyword | Found | Weight |
|---------|-------|--------|
| comment | ✅ | +1 BACKEND (data) |
| system | ✅ | neutral |
| real-time | ✅ | +2 BOTH (WebSocket) |
| updates | ✅ | +1 FRONTEND (UI) |

### Work Type Decision

```yaml
work_type: FULLSTACK
confidence: 0.90
reasoning: |
  - "comment system" requires both backend storage and frontend display
  - "real-time updates" requires WebSocket on both server and client
  - Feature spans full stack from database to UI
```

### Skills to Invoke

```yaml
skills_to_invoke:
  discipline:
    - superpowers:brainstorming
    - superpowers:test-driven-development
    - superpowers:verification-before-completion
  domain_specific:
    - frontend-design       # For comment UI
    - architecture-patterns # For real-time backend
    - webapp-testing        # For E2E verification
  agents:
    - schema-validator      # For database schema
```

### Output to auto-context.yaml

```yaml
work_type: FULLSTACK
detected_at: "2025-01-18T10:00:00Z"
keywords_found:
  - comment
  - real-time
  - updates
skills_to_invoke:
  discipline:
    - superpowers:brainstorming
    - superpowers:test-driven-development
  domain_specific:
    - frontend-design
    - architecture-patterns
    - webapp-testing
parallelization:
  enabled: true
  parallel_layers: true  # Backend and frontend can run in parallel
layers:
  backend:
    - database schema
    - WebSocket server
    - API endpoints
  frontend:
    - comment components
    - real-time hooks
    - UI state management
```
