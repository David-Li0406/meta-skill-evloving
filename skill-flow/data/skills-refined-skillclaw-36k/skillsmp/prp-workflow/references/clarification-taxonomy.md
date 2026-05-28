# PRP Clarification Taxonomy

Use this taxonomy to analyze PRPs for ambiguities. Mark each category as: **Clear** / **Partial** / **Missing**.

## Coverage Categories

### 1. Functional Scope & Behavior
- Core user goals & success criteria
- Explicit out-of-scope declarations
- User roles / personas differentiation
- Primary workflows and interactions

### 2. Domain & Data Model
- Entities, attributes, relationships
- Identity & uniqueness rules
- Lifecycle/state transitions
- Data volume / scale assumptions

### 3. Interaction & UX Flow
- Critical user journeys / sequences
- Error/empty/loading states
- Accessibility or localization requirements
- Input validation rules

### 4. Non-Functional Quality Attributes
- Performance (latency, throughput targets)
- Scalability (horizontal/vertical, limits)
- Reliability & availability (uptime, recovery)
- Observability (logging, metrics, tracing)
- Security & privacy (auth, data protection, threats)
- Compliance / regulatory constraints

### 5. Integration & External Dependencies
- External services/APIs and failure modes
- Data import/export formats
- Protocol/versioning assumptions
- Third-party library constraints

### 6. Edge Cases & Failure Handling
- Negative scenarios (invalid input, missing data)
- Rate limiting / throttling
- Conflict resolution (concurrent edits)
- Degraded mode operations

### 7. Constraints & Tradeoffs
- Technical constraints (language, storage, hosting)
- Explicit tradeoffs or rejected alternatives
- Budget/timeline constraints affecting scope

### 8. Terminology & Consistency
- Canonical glossary terms
- Avoided synonyms / deprecated terms
- Domain-specific language definitions

### 9. Completion Signals
- Acceptance criteria testability
- Measurable Definition of Done indicators
- Success metrics

### 10. Misc / Placeholders
- TODO markers / unresolved decisions
- Ambiguous adjectives ("robust", "intuitive", "fast")
- Vague requirements without concrete criteria

## Prioritization

Generate questions using **(Impact × Uncertainty)** heuristic:
- Cover highest-impact categories first
- Balance coverage across categories
- Exclude already-answered questions
- Favor questions that reduce rework risk

## Question Constraints

- Maximum 5 questions per session
- Each answerable with either:
  - Multiple-choice (2-5 mutually exclusive options)
  - Short phrase (≤5 words)
- Only include if materially impacts architecture, data modeling, test design, UX, or compliance

## PRP Integration Table

After each answer, update the appropriate PRP section:

| Type | Target Section | Action |
|------|----------------|--------|
| Functional ambiguity | Success Criteria / Requirements | Add/update specific capability |
| User interaction | User Stories / Workflows | Add clarified role/constraint/scenario |
| Data model | Data Models and Structure | Add fields, types, relationships |
| Non-functional | Success Criteria | Add measurable criteria |
| Edge case | Known Gotchas / Edge Cases | Add bullet or subsection |
| Terminology | Throughout | Normalize term |
| Security/privacy | Implementation Blueprint / Gotchas | Add auth/data protection rules |
| Performance | Success Criteria / Gotchas | Add latency/throughput targets |
| Integration | Integration Points / Context | Add service details, failure modes |

## Coverage Summary Template

| Category | Status | Notes |
|----------|--------|-------|
| Functional Scope | Resolved/Clear/Deferred/Outstanding | Brief note if not Clear |
| Domain & Data Model | ... | ... |
| Interaction & UX Flow | ... | ... |
| Non-Functional Attributes | ... | ... |
| Integration & Dependencies | ... | ... |
| Edge Cases & Failures | ... | ... |
| Constraints & Tradeoffs | ... | ... |
| Terminology | ... | ... |
| Completion Signals | ... | ... |

**Status Definitions:**
- **Resolved**: Was Partial/Missing, now addressed
- **Clear**: Already sufficient
- **Deferred**: Exceeds quota OR better for execution phase
- **Outstanding**: Still Partial/Missing but low impact
