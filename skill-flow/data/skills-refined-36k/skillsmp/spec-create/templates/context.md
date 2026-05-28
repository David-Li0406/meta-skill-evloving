# Context: ${TASK_NAME}

<!--
Implementation context for ${TASK_NAME}.
This is a "lab notebook" - tactical details updated as you work.
-->

---

<!-- Include when: claude_plan exists in spec.md frontmatter -->
## Native Plan

**Source:** `${CLAUDE_PLAN_PATH}`

- **Goal:** ${PLAN_GOAL}
- **Approach:** ${PLAN_APPROACH}
- **Open questions resolved:** ${RESOLVED_QUESTIONS}

---

## Key Files

<!--
List files relevant to this work with line ranges and descriptions.
Update as you discover more during implementation.
-->

### ${AREA_1}

| File | Lines | Description |
|------|-------|-------------|
| `${FILE_PATH}` | ${LINE_RANGE} | ${DESCRIPTION} |

### ${AREA_2}

| File | Lines | Description |
|------|-------|-------------|
| `${FILE_PATH}` | ${LINE_RANGE} | ${DESCRIPTION} |

---

## Architecture Decisions

<!--
Log decisions as they happen during implementation.
Use AD-N prefix for numbering.
-->

### AD-1: ${DECISION_TITLE}

**Context:** ${CONTEXT}

**Decision:** ${DECISION}

**Alternatives:**
- ${ALTERNATIVE_A}: ${TRADE_OFFS}
- ${ALTERNATIVE_B}: ${TRADE_OFFS}

**Impact:** ${IMPACT}

---

## Constraints

<!--
Technical and business constraints affecting implementation.
-->

### Technical

- ${CONSTRAINT}: ${RATIONALE}

### Business

- ${CONSTRAINT}: ${RATIONALE}

---

<!-- Include when: User opted in to "Tech Decisions" during validation (Features only) -->
## Tech Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| ${DECISION_AREA} | ${CHOICE} | ${WHY} |

### ${DECISION_1_NAME}

**Options considered:**
- ${OPTION_A}: ${PROS_CONS}
- ${OPTION_B}: ${PROS_CONS}

**Selected:** ${CHOICE}
**Rationale:** ${WHY}

---

<!-- Include when: User opted in to "Data Model" during validation (Features only) -->
## Data Model

### Entities

| Entity | Purpose | Key Fields |
|--------|---------|------------|
| ${ENTITY} | ${PURPOSE} | ${FIELDS} |

### Relationships

```
${ENTITY_A} ──1:N──► ${ENTITY_B}
${ENTITY_B} ──N:M──► ${ENTITY_C}
```

### Schema

```yaml
${ENTITY}:
  ${FIELD}: ${TYPE}
  ${FIELD_2}: ${TYPE}
```

---

## Gotchas & Learnings

<!--
Capture surprises, edge cases, and lessons learned during implementation.
-->

- ${GOTCHA}

---

## Open Questions

<!--
Track unresolved questions. Remove when resolved.
-->

- [ ] ${QUESTION}

---

## Future Considerations

<!--
Items identified but deferred. Not in scope but worth tracking.
-->

- ${CONSIDERATION}
