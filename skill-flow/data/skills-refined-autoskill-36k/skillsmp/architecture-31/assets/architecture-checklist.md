# Architecture Review Checklist

## Pre-Review

- [ ] Understand the feature/change being reviewed
- [ ] Know the current architecture context
- [ ] Have access to relevant ADRs

---

## North Star Check

- [ ] **Locality:** Does this change touch 1-2 modules, or many?
- [ ] **Independence:** Can this be deployed without coordinating with other teams?
- [ ] **Simplicity:** Is this the simplest solution that works?

**Red flag:** If change touches 5+ unrelated files, stop and reconsider boundaries.

---

## Layer Compliance

### 3-Tier Architecture

- [ ] Files are in correct tier (01-presentation / 02-logic / 03-data)
- [ ] No reverse imports (data→logic, logic→presentation)
- [ ] No layer skipping (presentation→data directly)

### Dependency Direction

```
Valid:   Presentation → Logic → Data ✅
Invalid: Data → Logic ❌
Invalid: Presentation → Data (skipping) ❌
```

- [ ] All imports follow valid direction
- [ ] Interfaces at boundaries (if needed)

---

## Module Boundaries

### Structure

- [ ] Module has single index.ts entry point
- [ ] Internal files not imported directly from outside
- [ ] Public API is minimal and intentional

### Data Ownership

- [ ] Each module owns its data exclusively
- [ ] No direct database access across modules
- [ ] Cross-module data accessed via APIs

### Communication

- [ ] Clear communication pattern chosen (API, events, props)
- [ ] No shared mutable state
- [ ] Coupling is intentional and documented

---

## Red Flags

### Dumping Grounds

- [ ] No additions to `shared/common/utils` without clear ownership
- [ ] Shared code has specific purpose, not "stuff we use everywhere"

### Coupling Issues

- [ ] No cross-module direct imports
- [ ] No framework magic hiding control flow
- [ ] Dependencies are explicit, not implicit

### Size Issues

- [ ] Components < 200 lines (max 300)
- [ ] Services < 300 lines (max 400)
- [ ] Modules don't have >10 public exports

---

## Circular Dependencies

- [ ] No circular imports between modules
- [ ] Run `scripts/analyze_dependencies.py` if unsure
- [ ] If cycles exist, plan to break them

---

## Testing Considerations

### Test Distribution

- [ ] Heavy unit tests for domain logic
- [ ] Integration tests at module boundaries
- [ ] Minimal E2E for critical paths

### Testability

- [ ] New code is unit testable in isolation
- [ ] Dependencies can be mocked/stubbed
- [ ] No hidden global state

---

## Observability

### Logging

- [ ] Structured logging (JSON, not string concat)
- [ ] Appropriate log levels (error, warn, info, debug)
- [ ] No sensitive data in logs

### Error Handling

- [ ] Errors are caught and reported
- [ ] No silent failures
- [ ] Error boundaries at appropriate levels

### Tracing

- [ ] Correlation IDs for cross-service calls (if applicable)
- [ ] Key operations are measurable

---

## Documentation

### Code

- [ ] Public APIs have clear documentation
- [ ] Complex logic has explanatory comments
- [ ] Types are self-documenting

### Architecture

- [ ] Significant decisions have ADRs
- [ ] Module responsibilities are documented
- [ ] Diagrams updated if structure changed

---

## Extraction Readiness

If considering extracting to separate service:

- [ ] Clear, stable contract exists
- [ ] Team ownership boundaries match
- [ ] Independent deployment provides real benefit
- [ ] Simpler options exhausted first

**Remember:** Don't extract for "cleanliness" alone.

---

## Final Checks

- [ ] Change follows North Star (small changes stay local)
- [ ] No new red flags introduced
- [ ] Architecture is easier to understand, not harder
- [ ] Future developers will thank you, not curse you

---

## Review Outcome

| Outcome | Action |
|---------|--------|
| ✅ Approved | Proceed with implementation |
| ⚠️ Minor issues | Fix before merge |
| ❌ Major issues | Redesign required |

**Notes:**

_[Add specific feedback here]_
