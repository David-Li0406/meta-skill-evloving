# Cross-Documentation Verification Checklist

Comprehensive checklist for verifying consistency across documentation artifacts.

---

## Hierarchical Consistency

### Epic → Feature Alignment

- [ ] **Feature scope within epic scope**: All features belong to parent epic
- [ ] **Feature goals support epic goals**: Features contribute to epic success criteria
- [ ] **No overlapping features**: Features have clear, distinct boundaries
- [ ] **Feature dependencies resolved**: All prerequisite features identified
- [ ] **Epic constraints followed**: Features respect epic-level constraints

**Check Method**:
1. Read epic-{n}.md and extract scope, goals, constraints
2. Read all feature-{n}.*.md files for that epic
3. Verify each feature scope fits within epic scope
4. Check for feature overlap or gaps

**Violation Example**:
```
🔴 CONFLICT: feature-5.1 includes payment processing, but epic-5 scope is "Data Management"
```

---

### Feature → Wave Alignment

- [ ] **Wave scope within feature scope**: All waves deliver part of feature
- [ ] **Wave deliverables complete feature**: All feature requirements covered
- [ ] **No duplicate deliverables**: Waves have distinct responsibilities
- [ ] **Wave order logical**: Dependencies respected in wave sequence
- [ ] **Feature technical approach followed**: Waves implement feature design

**Check Method**:
1. Read feature-{n}.{m}.md and extract scope, requirements, technical approach
2. Read all wave-{n}.{m}.*.md files for that feature
3. Map wave deliverables to feature requirements
4. Identify gaps or duplicate deliverables

**Violation Example**:
```
🔴 CONFLICT: wave-5.1.2 implements authentication, but feature-5.1 specifies using existing auth service
```

---

### Wave → User Story Alignment

- [ ] **User stories within wave scope**: Stories belong to wave
- [ ] **User stories complete wave**: All wave deliverables covered
- [ ] **Story dependencies resolved**: Prerequisites identified
- [ ] **Story size appropriate**: Fits within wave
- [ ] **Acceptance criteria clear**: Verifiable conditions

**Check Method**:
1. Read wave-{n}.{m}.{s}.md and extract scope, deliverables
2. List user stories in wave
3. Verify stories cover all deliverables
4. Check story dependencies

**Violation Example**:
```
🟡 GAP: wave-5.1.1 deliverable "logging setup" has no corresponding user story
```

---

## Technical Consistency

### Technology Stack Consistency

- [ ] **Same framework across features**: No conflicting frameworks
- [ ] **Consistent library versions**: No version conflicts
- [ ] **Approved technologies only**: All match ADR decisions
- [ ] **No redundant libraries**: Single library per concern
- [ ] **Dependencies declared**: All imports in package files

**Check Method**:
1. Extract technology stack from each feature plan
2. Compare against approved stack in ADRs
3. Check for version conflicts
4. Verify dependencies in package.json/requirements.txt

**Violation Examples**:
```
🔴 CONFLICT: feature-5.1 uses React 18, feature-5.2 uses React 17
🔴 CONFLICT: feature-4.1 uses Express, feature-5.1 uses Fastify (ADR requires Express)
```

---

### Design Pattern Consistency

- [ ] **Same pattern for same concern**: Consistent approach
- [ ] **Pattern matches ADR**: Follows architectural decisions
- [ ] **No contradictory patterns**: Patterns don't conflict
- [ ] **Pattern variation justified**: Documented why different
- [ ] **Pattern documented**: Others can recognize it

**Check Method**:
1. Identify patterns used in each feature (singleton, factory, etc.)
2. Check same concern uses same pattern across features
3. Verify patterns match ADR guidance

**Violation Examples**:
```
🔴 CONFLICT: feature-4.2 uses singleton for ConfigManager, feature-5.1 uses factory
🟡 GAP: feature-5.1 uses observer pattern, but no ADR documents this
```

---

### API Contract Consistency

- [ ] **Endpoint naming consistent**: RESTful conventions
- [ ] **Response format aligned**: Same structure across APIs
- [ ] **Error codes consistent**: Standard error format
- [ ] **Versioning strategy followed**: /v1/, /v2/ consistent
- [ ] **Authentication consistent**: Same auth mechanism

**Check Method**:
1. Extract API endpoints from each feature
2. Check naming conventions match
3. Compare response formats
4. Verify authentication approach

**Violation Examples**:
```
🔴 CONFLICT: feature-4.1 uses /api/v1/users, feature-5.1 uses /users (no version)
🟡 GAP: feature-5.1 error format differs from standard { code, message, details }
```

---

### Data Model Consistency

- [ ] **Entity relationships aligned**: No conflicting relationships
- [ ] **Field names consistent**: Same entity uses same fields
- [ ] **Data types consistent**: No type conflicts
- [ ] **Validation rules aligned**: Same rules for same fields
- [ ] **No duplicate entities**: Single source of truth

**Check Method**:
1. Extract data models from each feature
2. Check for entity overlap or conflicts
3. Verify field naming and types consistent

**Violation Examples**:
```
🔴 CONFLICT: feature-4.1 defines User.email as required, feature-5.1 defines as optional
🟠 DUPLICATION: feature-4.2 and feature-5.1 both define Customer entity
```

---

## Decision Consistency

### ADR Self-Consistency

- [ ] **No contradictory decisions**: ADRs don't conflict
- [ ] **Superseded ADRs marked**: Status updated
- [ ] **ADR dependencies documented**: Related ADRs linked
- [ ] **Decision dates logical**: No time paradoxes
- [ ] **All ADRs have status**: Accepted/Superseded/Deprecated

**Check Method**:
1. Read all ADRs in Docs/architecture/decisions/
2. Build decision graph
3. Identify conflicts
4. Verify superseded relationships

**Violation Examples**:
```
🔴 CONFLICT: ADR-010 requires REST, ADR-020 requires GraphQL (both for same API)
🟡 GAP: ADR-015 superseded by ADR-025, but status not updated
```

---

### Feature-ADR Alignment

- [ ] **Features follow ADR decisions**: Compliant with architecture
- [ ] **Deviations justified**: Documented in feature or ADR
- [ ] **New patterns have ADRs**: Architectural changes documented
- [ ] **ADRs referenced**: Features cite relevant ADRs
- [ ] **Technology matches ADRs**: Framework/library choices aligned

**Check Method**:
1. Read feature plan
2. Extract technology and pattern choices
3. Compare against relevant ADRs
4. Identify deviations

**Violation Examples**:
```
🔴 CONFLICT: feature-5.1 uses MongoDB, ADR-003 requires PostgreSQL
🟡 GAP: feature-5.1 introduces caching pattern, but no ADR documents approach
```

---

### Architecture-Feature Alignment

- [ ] **Component structure matches**: Feature fits in architecture
- [ ] **Layer boundaries respected**: No layer violations
- [ ] **Integration points correct**: Matches architecture diagram
- [ ] **Data flow consistent**: Follows architectural data flow
- [ ] **Security model followed**: Authentication/authorization aligned

**Check Method**:
1. Read Docs/architecture/_main/05-Architecture.md
2. Extract component structure, layers, integration points
3. Read feature plan
4. Verify feature components fit architecture

**Violation Examples**:
```
🔴 CONFLICT: feature-5.1 adds new layer "caching" not in architecture
🟡 GAP: feature-5.1 references "notification service" not in architecture diagram
```

---

## Content Consistency

### Duplication Detection

- [ ] **No duplicate sections**: Same content in multiple docs
- [ ] **Single source of truth**: Reference, don't duplicate
- [ ] **Cross-references used**: Links instead of copying
- [ ] **Consistent information**: No contradictory versions
- [ ] **DRY principle followed**: Don't repeat yourself

**Check Method**:
1. Use detect_duplication.py script
2. Review sections with >80% similarity
3. Consolidate duplicate content

**Violation Examples**:
```
🟠 DUPLICATION: Architecture section in both epic-5.md and feature-5.1.md (95% similar)
🟠 DUPLICATION: Tech stack listed in feature-5.1.md and wave-5.1.1.md
```

---

### Gap Detection

- [ ] **All references exist**: No broken links
- [ ] **All sections complete**: No TODO markers
- [ ] **All dependencies documented**: Prerequisites identified
- [ ] **All decisions documented**: No implicit choices
- [ ] **All terms defined**: Glossary complete

**Check Method**:
1. Use find_cross_references.py --check-missing
2. Search for TODO, TBD, FIXME markers
3. Verify all referenced docs exist

**Violation Examples**:
```
🟡 GAP: feature-5.1 references ADR-030 which doesn't exist
🟡 GAP: wave-5.1.1 has section "## Security Approach" marked TODO
```

---

### Cross-Reference Validation

- [ ] **All links valid**: No 404s
- [ ] **Relative paths correct**: Links work from doc location
- [ ] **Bidirectional references**: Parent/child linked both ways
- [ ] **Reference text accurate**: Link text describes target
- [ ] **No orphaned documents**: All docs referenced somewhere

**Check Method**:
1. Use find_cross_references.py
2. Verify all markdown links resolve
3. Check parent references child, child references parent

**Violation Examples**:
```
🟡 GAP: epic-5.md references feature-5.1.md, but feature-5.1.md doesn't reference epic-5.md
🟡 GAP: wave-5.1.1.md link to feature-5.1.md is broken (wrong path)
```

---

## Drift Detection

### Architecture Drift

- [ ] **Recent features match architecture**: Current approach aligned
- [ ] **Patterns still valid**: No outdated patterns
- [ ] **Component structure current**: Matches implementation
- [ ] **Integration points accurate**: Reflects actual integrations
- [ ] **Technology stack current**: No deprecated technologies

**Check Method**:
1. Read Docs/architecture/_main/05-Architecture.md
2. Compare against recent feature plans (last 3 months)
3. Identify mismatches

**Violation Examples**:
```
🔵 DRIFT: Architecture shows 3-tier, recent features use microservices
🔵 DRIFT: Architecture specifies REST, recent features use GraphQL
```

---

### ADR Drift

- [ ] **ADRs reflect current decisions**: Not outdated
- [ ] **Superseded ADRs marked**: Status current
- [ ] **No implicit superseding**: Changes documented
- [ ] **ADR dates recent**: Within relevance window
- [ ] **Consequences still valid**: No changed assumptions

**Check Method**:
1. Read all ADRs
2. Check status and dates
3. Compare against recent implementation choices

**Violation Examples**:
```
🔵 DRIFT: ADR-005 from 2023 requires Express, all 2025 features use Fastify
🔵 DRIFT: ADR-010 status "Accepted", but later features don't follow it
```

---

## Validation Process

For comprehensive cross-documentation verification:

1. **Scope Identification**
   - Determine target document
   - Identify related documents to check

2. **Content Extraction**
   - Read all relevant documents
   - Extract key elements (scope, tech, decisions, patterns)

3. **Consistency Checks**
   - Run hierarchical checks
   - Run technical checks
   - Run decision checks
   - Run content checks
   - Run drift checks

4. **Issue Categorization**
   - CONFLICT: Must resolve
   - GAP: Should fill
   - DUPLICATION: Should consolidate
   - DRIFT: Consider updating

5. **Score Calculation**
   ```
   Score = 100 - (conflicts × 20) - (gaps × 5) - (duplication × 3) - (drift × 1)
   ```

6. **Report Generation**
   - List all issues by category
   - Provide resolution guidance
   - Calculate consistency score
   - Make recommendation

---

## Quick Reference: Issue Severity

**CONFLICT (🔴)**: -20 points each
- Contradictory decisions
- Breaking changes
- Incompatible approaches

**GAP (🟡)**: -5 points each
- Missing documentation
- Broken references
- Incomplete sections

**DUPLICATION (🟠)**: -3 points each
- Duplicate content
- Redundant information
- Multiple sources of truth

**DRIFT (🔵)**: -1 point each
- Outdated information
- Evolution without updates
- Pattern changes

---

**Last Updated**: 2025-01-21
