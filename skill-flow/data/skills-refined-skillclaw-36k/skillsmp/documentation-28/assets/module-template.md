# {{MODULE_NAME}}

> {{ONE_LINE_DESCRIPTION}}

**Program:** {{PROGRAM_NAME}}
**Status:** {{X}}/{{TOTAL}} features complete

---

## Overview

{{MODULE_DESCRIPTION}}

### Purpose

{{WHY_THIS_MODULE_EXISTS}}

### Scope

**In Scope:**
- {{IN_SCOPE_1}}
- {{IN_SCOPE_2}}

**Out of Scope:**
- {{OUT_OF_SCOPE_1}}
- {{OUT_OF_SCOPE_2}}

---

## Features

| Feature | Status | Description | Priority |
|---------|--------|-------------|----------|
| [{{Feature 1}}](./{{feature-1}}.md) | ⏳ | {{Description}} | High |
| [{{Feature 2}}](./{{feature-2}}.md) | ⏳ | {{Description}} | Medium |
| [{{Feature 3}}](./{{feature-3}}.md) | ⏳ | {{Description}} | Low |

### Status Legend

| Icon | Status |
|------|--------|
| ⏳ | Planned |
| 🔄 | In Progress |
| ✅ | Complete |
| 🚫 | Blocked |

---

## Dependencies

### This Module Depends On

| Module | What We Use |
|--------|-------------|
| [{{Module A}}](../{{module-a}}/_{{module-a}}.md) | {{What we need from it}} |
| {{External API}} | {{What we use it for}} |

### Modules That Depend On This

| Module | What They Use |
|--------|---------------|
| [{{Module B}}](../{{module-b}}/_{{module-b}}.md) | {{What they need from us}} |

---

## Architecture

### Data Flow

```
{{DIAGRAM}}

Example:
┌──────────┐     ┌──────────┐     ┌──────────┐
│   User   │────▶│  Module  │────▶│ Database │
│   Input  │◀────│  Logic   │◀────│          │
└──────────┘     └──────────┘     └──────────┘
```

### Key Components

| Component | Responsibility |
|-----------|----------------|
| {{Component 1}} | {{What it does}} |
| {{Component 2}} | {{What it does}} |

### Public API

```typescript
// Exported from this module
export {
  {{function1}},
  {{function2}},
  {{Type1}},
  {{Type2}},
};
```

---

## Data Model

_Key entities managed by this module._

### {{Entity Name}}

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| {{field}} | {{type}} | {{description}} |

---

## Technical Decisions

### {{Decision 1 Title}}

**Context:** {{Why this decision was needed}}

**Decision:** {{What was decided}}

**Rationale:** {{Why this approach was chosen}}

---

## Testing Strategy

| Test Type | Coverage | Location |
|-----------|----------|----------|
| Unit | Core logic | `tests/unit/{{module}}/` |
| Integration | API endpoints | `tests/integration/{{module}}/` |
| E2E | Critical paths | `tests/e2e/` |

---

## Open Questions

- [ ] **Open:** {{Question 1}}
- [x] **Resolved:** {{Question 2}} → {{Answer}}

---

## Related Documentation

- [Program Overview](../../{{program}}.md)
- [Architecture Doc](/Documentation/architecture.md)
- [API Reference](/Documentation/api/{{module}}.md)
