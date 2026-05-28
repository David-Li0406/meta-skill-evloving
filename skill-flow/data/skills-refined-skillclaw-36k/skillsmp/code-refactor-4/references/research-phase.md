# Research Phase: Advanced Techniques

## Table of Contents

1. [Multi-Component Research](#multi-component-research)
2. [Call Graph Construction](#call-graph-construction)
3. [Dependency Mapping Patterns](#dependency-mapping-patterns)
4. [Search Strategies](#search-strategies)

---

## Multi-Component Research

When refactoring spans multiple components, use parallel Explore agents:

```
Component A ──► Explore Agent 1 ──► research-a.md
Component B ──► Explore Agent 2 ──► research-b.md
Component C ──► Explore Agent 3 ──► research-c.md
                      │
                      ▼
              Synthesize findings
                      │
                      ▼
              01-research.md (combined)
```

**Synthesis questions:**
- Where do components interact?
- Are there shared dependencies?
- What's the order of refactoring (dependency graph)?
- Are there circular dependencies to break?

---

## Call Graph Construction

### Finding Callers (Dependents)

Search patterns to find who calls the component:

```bash
# Direct instantiation
grep -r "new ComponentName" --include="*.ts"

# Import statements
grep -r "import.*ComponentName" --include="*.ts"

# Method calls
grep -r "componentInstance\.\w+" --include="*.ts"

# Dependency injection
grep -r "ComponentName" */providers/* */modules/*
```

### Finding Dependencies (What It Calls)

1. Read the component's imports
2. Trace constructor parameters
3. Follow method calls to external modules
4. Check for dynamic imports or lazy loading

### Visualizing Depth

For complex components, show call depth:

```
OrderService.createOrder()
├── validateOrder()           [internal]
├── InventoryService.reserve() [external]
│   └── Database.update()     [infrastructure]
├── PaymentService.charge()    [external]
│   ├── StripeClient.create() [infrastructure]
│   └── Database.insert()     [infrastructure]
└── EventBus.emit()           [infrastructure]
```

---

## Dependency Mapping Patterns

### Direct Dependencies

```typescript
class PaymentService {
  constructor(
    private stripe: StripeClient,      // Direct dependency
    private repo: PaymentRepository,   // Direct dependency
    private events: EventEmitter       // Direct dependency
  ) {}
}
```

### Hidden Dependencies

Watch for dependencies not in constructor:

```typescript
class PaymentService {
  processPayment() {
    const config = Config.get('payment'); // Hidden: global config
    const logger = Logger.getInstance();   // Hidden: singleton
    fetch('https://api.example.com');      // Hidden: HTTP call
  }
}
```

**Document hidden dependencies separately** - they're often refactoring targets.

### Transitive Dependencies

Map what your dependencies depend on:

```
PaymentService
└── StripeClient
    └── HttpClient
        └── fetch (global)
└── PaymentRepository
    └── Database
        └── pg (connection pool)
```

---

## Search Strategies

### Starting Points

| Goal | Search Pattern |
|------|----------------|
| Find all usages | `grep "ClassName"` across codebase |
| Find instantiation | `grep "new ClassName"` |
| Find injection | Search DI container config |
| Find interface implementations | `grep "implements InterfaceName"` |
| Find method overrides | `grep "methodName.*override"` |

### Progressive Expansion

1. **Start narrow**: The component itself
2. **Expand to direct callers**: Who uses this?
3. **Expand to context**: What happens before/after calls?
4. **Expand to alternatives**: Are there similar components?

### Red Flags to Note

During research, flag these for Phase 2:

- Multiple instantiation patterns (inconsistency)
- Circular dependencies
- God objects (too many responsibilities)
- Feature envy (component reaching into others' internals)
- Inappropriate intimacy (components know too much about each other)
- Hidden state mutations
- Implicit contracts between components
