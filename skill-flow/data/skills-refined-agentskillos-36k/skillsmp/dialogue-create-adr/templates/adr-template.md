# ADR-NNN: [Title]

Date: YYYY-MM-DD
Status: Proposed
Actor: human:<id> | ai:<id>

## References

List documents, decisions, and other artefacts relevant to this ADR:

| Reference | Relationship | Context |
|-----------|--------------|---------|
| THY-NNN | DERIVES_FROM | Theoretical grounding for this decision |
| REF-NNN | REFERENCES | Supporting reference material |
| DEC-YYYYMMDD-HHMMSS | TRACES_TO | Related logged decision |
| SH-NNN / FW-NNN | BLOCKS | task this decision unblocks |
| ADR-NNN | SUPERSEDES | Previous ADR this replaces (if applicable) |

**Reference patterns** (from schema_information-reference.md):
- Documents: `THY-NNN`, `REF-NNN`, `STR-NNN`, `F-N`, `C-N`, `O-N`, `I-N`, `G-N`, `E-N`
- Decisions: `DEC-YYYYMMDD-HHMMSS`
- Observations: `OBS-YYYYMMDD-HHMMSS`
- tasks: `SH-NNN`, `CD-NNN`, `FW-NNN`
- Actors: `human:<id>`, `ai:<id>`
- External: URLs

**Relationship types**: DERIVES_FROM, TRACES_TO, REFERENCES, SUPERSEDES, REQUIRES, BLOCKS, INFORMS

## Context

What issue or situation motivated this decision? Include:
- The problem or opportunity being addressed
- Relevant constraints or requirements
- Why a decision is needed now

## Decision

What change are we making? State the decision clearly and concisely.

## Alternatives Considered

For each alternative evaluated:

### Alternative 1: [Name]
**Pros:**
-

**Cons:**
-

### Alternative 2: [Name]
**Pros:**
-

**Cons:**
-

(Add more alternatives as needed)

## Consequences

What becomes easier or harder as a result of this decision?

**Positive:**
-

**Negative/Trade-offs:**
-

## Rationale

Why is this the right choice? Include:
- Key factors that influenced the decision
- Evidence or reasoning that supports the choice
- Why alternatives were rejected

---

## ADR Status Lifecycle

| Status | Meaning |
|--------|---------|
| **Proposed** | Initial state; under consideration |
| **Accepted** | Approved and in effect |
| **Deprecated** | No longer recommended; kept for history |
| **Superseded** | Replaced by another ADR (note which one) |

## Framework Grounding

ADRs are:
- **Content Domain**: STR (Strategy) — rationale, decisions, business justification
- **Temporal Class**: Standing — quarterly or less updates, years lifespan
- **Knowledge Type**: Attempting to capture embedded knowledge through formal alternatives analysis

Cross-references ensure traceability to:
- Theoretical foundations (THY documents)
- Related decisions (DEC entries in decision log)
- tasks that prompted the decision (SH, FW, CD)
- Previous ADRs (for supersession chains)
