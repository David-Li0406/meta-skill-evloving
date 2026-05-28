---
name: architecture-review
description: Evaluate system architecture, module boundaries, coupling, cohesion, and scalability patterns. Use when planning new features, reviewing system design, assessing technical debt at a systemic level, or when the codebase feels tangled.
---

# Architecture Review

Evaluate overall system design for maintainability, scalability, and adherence to established patterns.

## Scope

### 1. Module Boundaries (per AGENTS.md)
- Features grouped by domain inside `/app` and `/components`
- Shared utilities properly placed under `/lib`
- Clear separation between UI, state management, data fetching, and business logic
- No circular dependencies between modules

### 2. Data Layer Architecture (per CLAUDE.md)
- Two-layer approach consistency:
  - `lib/queries/` - Low-level Drizzle operations
  - `lib/data/` - Business logic assembly with permissions
- React `cache()` usage for request deduplication
- Permission checks enforced at data layer, not scattered
- Parallel data loading with `Promise.all()` where appropriate

### 3. Route Organization
- Consistent patterns in `app/(dashboard)/` routes
- Slug-based URL conventions maintained
- Server Components vs Client Components properly split
- Server Actions in `_actions/` directories

### 4. Coupling Analysis
- Feature modules should be independently deployable in concept
- Shared components shouldn't have feature-specific logic
- Database schema changes shouldn't require touching many features
- Look for "shotgun surgery" patterns

### 5. Cohesion Evaluation
- Related functionality grouped together
- Single Responsibility Principle at module level
- Files approaching 300 lines indicate need to split (per AGENTS.md)
- Functions exceeding 50 lines need decomposition

### 6. API Design (per AGENTS.md)
- RESTful patterns followed
- Versioned under `/api/v{n}`
- Consistent request/response contracts
- Typed responses with Zod validation

### 7. State Management Patterns
- Server-first pattern consistency
- TanStack React Query only for client mutations/polling
- Provider composition in `components/providers/`
- No state duplication between server and client

### 8. Error Handling Architecture
- Standardized error classes from `lib/errors/http.ts`
- Consistent `{ ok: boolean, data?, error? }` API responses
- React Query retry policies for external calls
- Graceful degradation with sensible fallbacks

## Output Format

```
[LAYER: DATA|UI|API|STATE|MODULE]
[SEVERITY: CRITICAL|HIGH|MEDIUM|LOW]
Area: Component/module/pattern affected
Issue: Brief description
Impact: How this affects maintainability/scalability
Current State: What exists now
Recommended: Architectural improvement
Migration Effort: LOW|MEDIUM|HIGH
```

## Actions

1. Map the dependency graph between major modules
2. Identify feature boundaries and cross-cutting concerns
3. Review data flow from API to UI
4. Check for proper layer separation
5. Evaluate consistency with established patterns

## Architecture Principles (from AGENTS.md)

- **Modular Architecture**: Group by domain
- **Single Responsibility**: One clear purpose per module
- **Separation of Concerns**: UI ≠ state ≠ data ≠ business logic
- **DRY**: Abstract when pattern appears 3+ times
- **Reuse > Rebuild**: Prefer existing modules before new abstractions

## Post-Review

Generate:
- Architecture diagram of current state
- Dependency heat map (high coupling areas)
- Recommended refactoring roadmap
- Risk assessment for proposed changes
- Suggested module boundary adjustments
