---
name: go-ddd-planner
description: >
  Create detailed implementation plans for Go projects using Clean Architecture
  and DDD. Triggers: planning complex features, architectural changes, multi-step
  tasks, new domain aggregates, bounded contexts, large refactoring efforts, or
  when requirements are unclear. Use before starting multi-file implementations.
license: MIT
compatibility: opencode
---

# Go DDD Implementation Planning Skill

Create comprehensive, actionable plans for complex Go features and refactoring using Clean Architecture and Domain-Driven Design principles.

## When This Skill MUST Be Used

**ALWAYS invoke this skill when the user's request involves ANY of these:**

- Complex features requiring multiple files or packages
- Architectural changes or large refactoring efforts
- New domain aggregates, services, or bounded contexts
- Work that will span multiple days or sessions
- Requirements that are unclear or need clarification
- Cross-cutting concerns (logging, auth, caching)
- Database schema changes with code implications
- API design with multiple endpoints
- Value object or entity design
- Event-driven patterns

**If the task involves more than 3 files or touches multiple layers, plan first.**

## Critical Safety Rules

**NEVER:**
- Start coding a complex feature without a plan
- Skip the codebase analysis step
- Ignore existing patterns in the codebase
- Create plans with vague steps like "implement the feature"
- Assume package structure without verifying
- Put business logic in application layer
- Emit events before persistence succeeds
- Validate in `Reconstitute()` (DB is trusted)

**ALWAYS:**
- Read existing code to understand current patterns
- Break down work into specific, actionable steps
- Include file paths and function names in the plan
- Identify dependencies between steps
- Include testing strategy
- Consider error handling and edge cases
- Keep domain layer pure (no external dependencies)

## Quick Reference

| Task | Command/Action |
|------|----------------|
| Understand structure | `tree -d -L 3 internal/` |
| Find interfaces | `rg "type.*interface" --type go` |
| Find constructors | `rg "func New" --type go \| head -20` |
| Check dependencies | `go mod graph \| grep "your/module"` |
| Find patterns | `rg "func.*Application" --type go` |

---

# Package Structure

Use flat packages (not Java-style nested):

```
internal/
├── domain/           # Pure business logic, no external deps
│   ├── order/       # Aggregate package
│   │   ├── order.go        # Aggregate root
│   │   ├── values.go       # Value objects
│   │   ├── events.go       # Domain events
│   │   ├── repository.go   # Repository interface
│   │   └── errors.go       # Sentinel errors
│   └── shared/      # Shared domain types
├── application/     # Use cases, orchestrates domain
│   └── order/
│       ├── application.go  # Commands/queries
│       └── adapter.go      # Legacy compatibility (if needed)
├── infra/           # External adapters
│   ├── mysqlrepo/   # Repository implementations
│   └── telebot/     # Telegram adapter
cmd/                 # Entry points with dependency wiring
```

**Flat Package Rules:**
- Group by concept, not technical type (`values.go`, not `valueobjects/`)
- Package name is part of API: `order.NewOrder()` not `order.OrderAggregate`
- Only split when package >1000 LOC or clear subdomain boundaries

---

# Aggregate Rules

- **Immutable state**: Private fields, exposed via getters
- **Validation in constructor**: `NewOrder()` validates, `Reconstitute()` does not
- **Events for side effects**: Aggregates emit events, cleared after persistence
- **Repository only for aggregate roots** (not child entities)

```go
// Constructor with validation - emits creation event
func NewOrder(id ID, userID user.ID, ...) (*Order, error) {
    if id < 0 {
        return nil, ErrInvalidOrderID
    }
    order := &Order{...}
    order.recordEvent(NewOrderCreated(...))
    return order, nil
}

// Reconstitute for DB loading - no validation, no events (DB is trusted)
func Reconstitute(id ID, userID user.ID, ...) *Order {
    return &Order{...}
}
```

---

# Event Collection Pattern

```go
type Order struct {
    // ... fields
    events []DomainEvent  // Uncommitted events
}

func (o *Order) recordEvent(e DomainEvent) { o.events = append(o.events, e) }
func (o *Order) DomainEvents() []DomainEvent { return o.events }
func (o *Order) ClearEvents() { o.events = nil }
```

**Publishing Lifecycle:**
1. Load aggregate (no events)
2. Call behavior method (events recorded)
3. Save to repository (transaction)
4. Publish events (after commit succeeds)
5. Clear events from aggregate

## Domain Events

- Named as past-tense facts: `OrderCreated`, `OrderCompleted`
- Immutable, include: AggregateID, OccurredAt, EventType, relevant data
- Only emit on actual state change (idempotent operations don't double-emit)

---

# Idempotent Operations

```go
func (o *Order) MarkAsShipped() error {
    if o.status == StatusShipped {
        return nil  // Already in desired state - no-op
    }
    o.status = StatusShipped
    o.recordEvent(NewOrderShipped(o.id))  // Only on actual change
    return nil
}
```

**Guidelines:**
- Check state before changing
- Return early if already in desired state
- Only emit events on actual changes

---

# Value Objects

| Type | When to Use | Example |
|------|-------------|---------|
| Type alias | Early stages, simple | `type UserID int64` |
| Simple struct | Validation needed | `CategoryID{value string}` |
| Rich struct | Complex behavior | `Money` with Add, Subtract |

**Rich Value Object Behaviors:**
- Accessors: `Int()`, `String()`, `IsZero()`
- Comparison: `Equals()`, `LessThan()`
- Arithmetic: `Add()`, `Subtract()` - return new instances (immutable)

**Collection Types:**
```go
type Tasks []*Task
func (t Tasks) UserIDs() []UserID           // Extract unique IDs
func (t Tasks) FilterByUserIDs(ids []UserID) Tasks  // Domain filtering
```

---

# Repository Pattern

- Interface in domain package (or application package for pragmatic Go)
- Implementation in `infra/mysqlrepo` using `Reconstitute()`

**Implementation Rules:**
- Separate DB models from domain aggregates
- Map nullable fields: `sql.NullString` -> `*string`
- Error mapping: `sql.ErrNoRows` -> `domain.ErrNotFound`

---

# Application Layer

- Use `Application` not `Service` (explicit DDD term)
- Orchestrates domain, no business logic
- Handle transactions, publish events after persistence

**Responsibilities:**
- Orchestrate workflows, coordinate aggregates
- Manage transactions, publish events
- Convert types (presentation <-> domain)
- **NOT**: Business logic (-> domain), direct DB queries (-> repositories)

**CQRS-lite Pattern:**
- Commands: Write operations with Command structs
- Queries: Read operations, return DTOs (not domain objects)

---

# Application Adapter Pattern

For gradual migration from legacy code:

```go
type LegacyAdapter struct {
    app *Application
}

var _ ports.OldInterface = (*LegacyAdapter)(nil)  // Compile-time check

func (a *LegacyAdapter) OldMethod(ctx context.Context, params OldParams) error {
    return a.app.NewUseCase(ctx, NewRequest{...})
}
```

---

# Task-Based Processing Pattern

For async/queue systems:

**Task Invariants:**
1. User-centric (`UserID` for batch operations)
2. Parkable (`ParkedUntil` for eventual consistency)
3. Lockable (implements `LockID()` for distributed processing)

| Pattern | When |
|---------|------|
| Parking | Expected delay (waiting for dependency) |
| Retry | Transient failure (network blip) |

---

# Dependency Rules

1. **Domain depends on nothing** (stdlib only)
2. **Application depends on Domain**
3. **Infrastructure depends on Domain + Application**
4. **cmd wires everything together**

```
cmd/ → infra/ → application/ → domain/
       ↓
    (external libs)
```

---

# Planning Process

## 1. Requirements Analysis

Before writing any plan, clarify:

```
- What is the goal?
- Who are the stakeholders?
- What are the success criteria?
- What constraints exist (time, tech, compatibility)?
- What assumptions are being made?
```

## 2. Codebase Analysis

```bash
# Understand current structure
tree -d -L 3 internal/

# Find related code
rg "type.*interface" --type go

# Check existing patterns
rg "func New" --type go | head -20
```

## 3. Architecture Review

For Go projects, consider each layer:

| Layer | Questions |
|-------|-----------|
| Domain | New aggregates? Value objects? Events? |
| Application | New use cases? Commands? Queries? |
| Infrastructure | New repositories? External adapters? |
| API | New endpoints? Request/response types? |

## 4. Step Breakdown

Create specific, actionable steps:

```markdown
### Phase 1: Domain Layer
1. **Create OrderID value object** (File: internal/domain/order/values.go)
   - Action: Add OrderID type with validation
   - Dependencies: None
   - Tests: internal/domain/order/values_test.go

2. **Create Order aggregate** (File: internal/domain/order/order.go)
   - Action: Define Order struct with NewOrder and Reconstitute
   - Dependencies: Step 1
   - Tests: internal/domain/order/order_test.go
```

---

# Plan Output Format

```markdown
# Implementation Plan: [Feature Name]

## Overview
[2-3 sentence summary of what we're building]

## Requirements
- [ ] Functional requirement 1
- [ ] Functional requirement 2
- [ ] Non-functional: performance, security, etc.

## Architecture Changes

### New Files
- `internal/domain/order/order.go` - Order aggregate
- `internal/domain/order/repository.go` - Repository interface

### Modified Files
- `internal/application/order/application.go` - Add CreateOrder use case
- `cmd/api/main.go` - Wire new dependencies

## Implementation Phases

### Phase 1: Domain Layer (Estimated: 2 hours)
| Step | File | Action | Dependencies |
|------|------|--------|--------------|
| 1.1 | values.go | Create OrderID | None |
| 1.2 | order.go | Create Order aggregate | 1.1 |
| 1.3 | repository.go | Define Repository interface | 1.2 |

### Phase 2: Application Layer (Estimated: 1 hour)
...

### Phase 3: Infrastructure Layer (Estimated: 2 hours)
...

### Phase 4: API Layer (Estimated: 1 hour)
...

## Testing Strategy
- Unit tests: All domain and application logic
- Integration tests: Repository implementations
- E2E tests: API endpoints

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Database migration | High | Run in staging first |
| Breaking API | Medium | Version endpoint |

## Success Criteria
- [ ] All tests passing
- [ ] Coverage > 80% on new code
- [ ] No lint errors
- [ ] Security scan clean
- [ ] Documentation updated
```

---

# Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Circular dependency | Wrong layer direction | Move interface to consumer package |
| Unclear ownership | Aggregate boundary wrong | Review DDD bounded context |
| Too many files | Over-engineering | Consolidate small packages |
| Test dependencies | Missing interfaces | Define ports at application layer |
| Hard to test | Concrete dependencies | Introduce interfaces at boundaries |

---

# Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Java-style nested packages | `valueobjects/`, `aggregate/` | Flat packages |
| Business logic in application layer | Wrong layer | Move to domain |
| Events published before persistence | Lost events on failure | Publish after commit |
| Validation in `Reconstitute()` | DB is trusted | Validate only in `New*()` |
| Using `Service` ambiguously | Unclear purpose | Use domain-specific names |
| Modifying aggregates directly | Bypasses invariants | Use methods |

---

# Example Requests

| User Request | Action |
|--------------|--------|
| "Add order management feature" | Full planning process: analyze, design layers, create phased plan |
| "Refactor the user module" | Analyze current state, identify issues, create migration plan |
| "Add caching to API" | Cross-cutting concern: identify touchpoints, plan infrastructure changes |
| "How should I structure this?" | Architecture review: recommend package structure |
| "Break down this feature" | Step breakdown with dependencies and estimates |
| "Create a new aggregate" | Design with NewX/Reconstitute, events, repository interface |
| "Design value objects" | Choose type alias vs struct based on validation needs |

---

# Quick Commands

```bash
# Find existing patterns
rg "type.*Repository interface" --type go
rg "func New.*Application" --type go

# Check package dependencies
go mod graph | grep "your/module"

# Visualize architecture (if go-cleanarch installed)
go-cleanarch -o arch.png ./...

# List all domain packages
find internal/domain -type d

# Check test coverage
go test -cover ./internal/domain/...
```
