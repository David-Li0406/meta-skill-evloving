---
name: planning
description: Planning phase guidelines including requirement gathering, MVP definition, and task breakdown.  Use when starting new features, creating specifications, or breaking down work.
---

# Planning Phase Instructions

## Development Methodology

### Incremental Development

Always follow this sequence:

1. **MVP** (Minimum Viable Product) - Core functionality only
2. **Product v1** - Essential features
3. **Product v2+** - Enhancements and optimizations

Never skip MVP phase. Build incrementally, validate early.

## Documentation Structure

### Templates Location

Use templates in `docs/template/`:

- `docs/template/requirement.template.md` - For feature specifications
- `docs/template/tasks_mvp.template.md` - For MVP task breakdown

### Document Placement

```
docs/
├── template/
│   ├── requirement.template.md
│   └── tasks-mvp.template.md
├── requirement.md
├── requirement-v1.md
├── requirement-v2.md
├── tasks-mvp.md
├── tasks-v1.md
└── tasks-v2.md
```

## Technology Stack

### Default Stack

- **Language**: TypeScript (preferred) or JavaScript
- **Testing**: Vitest
- **Package Manager**: pnpm

### Selection Criteria

When choosing technologies:

1. Check Context7 MCP tools for current best practices
2. Prioritize type safety and developer experience
3. Verify ecosystem maturity

Always consult Context7 before suggesting new libraries or frameworks.

## Planning Workflow

### 1. Requirement Gathering

- Use `docs/template/requirement.template. md`
- Define user stories and acceptance criteria
- Identify technical constraints
- **Get approval** before proceeding

### 2. MVP Scope Definition

- Use `docs/template/tasks-mvp.template.md`
- List only essential features
- Estimate complexity (S/M/L)
- **Get approval** before implementation

### 3. Task Breakdown

- Break features into <5 file changes per task
- Order tasks by dependency
- Flag risky items (DB schema, dependencies, CI/CD)
- **Get approval** before starting
