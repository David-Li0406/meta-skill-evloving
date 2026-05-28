# Common Documentation Conflicts

Examples of common conflicts found during cross-documentation verification and how to resolve them.

---

## Technology Stack Conflicts

### Conflict Type 1: Framework Version Mismatch

**Example**:
```
🔴 CONFLICT: feature-5.1 specifies React 18, feature-5.2 specifies React 17
```

**Impact**: Build failures, incompatible dependencies, maintenance burden

**Resolution Options**:
1. Align on single version (upgrade or downgrade)
2. Document why different versions needed (monorepo with isolated apps)
3. Create ADR documenting version strategy

**Recommended**: Align on latest stable version unless technical constraint

---

### Conflict Type 2: Competing Frameworks

**Example**:
```
🔴 CONFLICT: feature-4.1 uses Express, feature-5.1 uses Fastify, both for same API service
```

**Impact**: Architectural inconsistency, increased complexity, team confusion

**Resolution Options**:
1. Standardize on one framework (create/update ADR)
2. Document service boundary if justified (different services, different frameworks)
3. Migrate existing feature to chosen framework

**Recommended**: Create ADR choosing one framework, migrate non-conforming code

---

### Conflict Type 3: ADR Violation

**Example**:
```
🔴 CONFLICT: feature-5.1 uses MongoDB, ADR-003 requires PostgreSQL for relational data
```

**Impact**: Non-compliance with architectural decision, precedent for violations

**Resolution Options**:
1. Change feature to use PostgreSQL (follow ADR)
2. Justify MongoDB usage and create new ADR (if valid reason)
3. Update ADR-003 if decision changed

**Recommended**: Follow ADR unless compelling reason to change architecture

---

## Design Pattern Conflicts

### Conflict Type 4: Inconsistent Pattern Application

**Example**:
```
🔴 CONFLICT: feature-4.2 uses singleton for ConfigManager, feature-5.1 uses factory pattern
```

**Impact**: Inconsistent codebase, confusion about which pattern to use

**Resolution Options**:
1. Standardize on singleton (create ADR if none exists)
2. Document when to use each pattern (create decision matrix)
3. Refactor one feature to match the other

**Recommended**: Create ADR documenting pattern choice, refactor to align

---

### Conflict Type 5: Pattern vs ADR Mismatch

**Example**:
```
🔴 CONFLICT: wave-5.1.1 implements repository pattern, ADR-020 requires direct ORM usage
```

**Impact**: ADR non-compliance, architectural drift

**Resolution Options**:
1. Remove repository pattern, use direct ORM (follow ADR)
2. Update ADR-020 to allow repository pattern (if better approach)
3. Document exception for this specific case

**Recommended**: Follow ADR unless compelling reason found, then update ADR

---

## API Contract Conflicts

### Conflict Type 6: Endpoint Naming Inconsistency

**Example**:
```
🔴 CONFLICT: feature-4.1 uses /api/v1/users, feature-5.1 uses /users/v1
```

**Impact**: API inconsistency, developer confusion, documentation overhead

**Resolution Options**:
1. Standardize on /api/v1/resource format (create API standards ADR)
2. Create API gateway with consistent external interface
3. Document both patterns with usage guidelines

**Recommended**: Create API standards ADR, migrate to consistent format

---

### Conflict Type 7: Response Format Mismatch

**Example**:
```
🔴 CONFLICT: feature-4.1 returns { data, meta }, feature-5.1 returns { result, pagination }
```

**Impact**: Client confusion, inconsistent error handling, integration issues

**Resolution Options**:
1. Standardize on single response format (create API contract ADR)
2. Version APIs separately if serving different clients
3. Use API gateway to normalize responses

**Recommended**: Create API contract ADR with standard envelope, refactor APIs

---

### Conflict Type 8: Error Format Inconsistency

**Example**:
```
🔴 CONFLICT: feature-4.1 errors { error: "message" }, feature-5.1 errors { code, message, details }
```

**Impact**: Inconsistent error handling, client complexity

**Resolution Options**:
1. Standardize on structured error format (ADR)
2. Implement error middleware to normalize
3. Version APIs with different error formats

**Recommended**: Adopt structured format { code, message, details }, create ADR

---

## Data Model Conflicts

### Conflict Type 9: Field Definition Mismatch

**Example**:
```
🔴 CONFLICT: feature-4.1 defines User.email as required, feature-5.1 defines as optional
```

**Impact**: Data integrity issues, validation inconsistency, bugs

**Resolution Options**:
1. Standardize field definition (required or optional)
2. Document business rule changes if intentional
3. Create migration if changing requirement

**Recommended**: Align on single definition, update all features, document in data model ADR

---

### Conflict Type 10: Entity Duplication

**Example**:
```
🔴 CONFLICT: feature-4.2 defines Customer entity, feature-5.1 defines Client entity (same concept)
```

**Impact**: Data duplication, synchronization issues, confusion

**Resolution Options**:
1. Merge into single entity (Customer or Client)
2. Clarify if truly different concepts
3. Create shared data model

**Recommended**: Merge into single entity, update both features, create shared model ADR

---

## ADR Conflicts

### Conflict Type 11: Contradictory Decisions

**Example**:
```
🔴 CONFLICT: ADR-010 requires REST for external API, ADR-020 requires GraphQL for external API
```

**Impact**: Architectural confusion, implementation paralysis

**Resolution Options**:
1. Supersede one ADR with the other
2. Clarify scope (REST for public API, GraphQL for partner API)
3. Create new ADR consolidating decisions

**Recommended**: Create new ADR clarifying when to use each, supersede conflicting ADRs

---

### Conflict Type 12: Unsuperseded ADR

**Example**:
```
🔴 CONFLICT: ADR-005 requires JWT, ADR-015 requires OAuth2, ADR-005 not marked superseded
```

**Impact**: Unclear which decision current, risk of using old approach

**Resolution Options**:
1. Update ADR-005 status to "Superseded by ADR-015"
2. Clarify if both are valid for different use cases
3. Create decision matrix ADR

**Recommended**: Update ADR-005 status, add superseded-by relationship

---

## Hierarchical Conflicts

### Conflict Type 13: Scope Creep

**Example**:
```
🔴 CONFLICT: epic-5 scope is "Data Management", feature-5.3 includes "Payment Processing"
```

**Impact**: Epic boundaries unclear, organizational confusion

**Resolution Options**:
1. Move feature-5.3 to correct epic (e.g., epic-6 Commerce)
2. Expand epic-5 scope if justified
3. Split feature into two features in different epics

**Recommended**: Move feature to correct epic, update numbering if needed

---

### Conflict Type 14: Wave Deviation

**Example**:
```
🔴 CONFLICT: feature-5.1 specifies "use existing auth", wave-5.1.2 implements new auth system
```

**Impact**: Scope deviation, wasted effort, architectural drift

**Resolution Options**:
1. Update wave to follow feature specification
2. Update feature specification if approach changed
3. Document reason for deviation in both docs

**Recommended**: Clarify with stakeholders, align wave with feature or update feature plan

---

## Content Conflicts

### Conflict Type 15: Contradictory Information

**Example**:
```
🟠 DUPLICATION: epic-5.md says "3 features planned", feature list shows 5 features
```

**Impact**: Documentation unreliable, trust erosion

**Resolution Options**:
1. Update epic to match reality (5 features)
2. Remove incorrect information
3. Use cross-references instead of duplicating

**Recommended**: Update epic, use cross-reference to feature list

---

### Conflict Type 16: Outdated Reference

**Example**:
```
🔵 DRIFT: Architecture.md references 3-tier architecture, recent features use microservices
```

**Impact**: Documentation-reality gap, onboarding confusion

**Resolution Options**:
1. Update Architecture.md to reflect microservices
2. Document evolution path (3-tier → microservices)
3. Create migration ADR explaining transition

**Recommended**: Update Architecture.md, create ADR documenting architectural evolution

---

## Resolution Decision Tree

```
Is there a CONFLICT?
├─ Yes
│  ├─ Is there an ADR covering this?
│  │  ├─ Yes → Follow ADR, update non-conforming doc
│  │  └─ No → Create ADR documenting decision
│  └─ Which document is authoritative?
│     ├─ Architecture/ADR → Update feature/wave
│     ├─ Feature → Update wave
│     └─ Unclear → Escalate to architect
└─ No
   └─ Is there a GAP?
      ├─ Yes → Fill gap with missing information
      └─ No → Is there DUPLICATION?
         ├─ Yes → Consolidate, use cross-references
         └─ No → Is there DRIFT?
            ├─ Yes → Update outdated information
            └─ No → All good ✅
```

---

## Conflict Prevention Best Practices

1. **Cross-reference, don't duplicate**: Link to source of truth
2. **Update related docs**: When changing one, check dependencies
3. **Mark superseded decisions**: Keep ADR status current
4. **Verify before finalizing**: Run verification before approval
5. **Single source of truth**: Designate authoritative document
6. **Document deviations**: If must deviate, document why
7. **Regular audits**: Periodic cross-documentation verification
8. **Traceability**: Maintain Epic → Feature → Wave → Story chain

---

**Last Updated**: 2025-01-21
