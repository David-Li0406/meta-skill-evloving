# Documentation Consistency Patterns

Patterns and best practices for maintaining consistency across documentation artifacts.

---

## Pattern 1: Single Source of Truth (SSOT)

**Problem**: Same information duplicated in multiple documents, leading to inconsistency when one is updated but others aren't.

**Solution**: Designate one document as authoritative, others reference it.

**Example**:

❌ **Bad** (Duplication):
```markdown
<!-- epic-5.md -->
## Technology Stack
- Frontend: React 18
- Backend: Node.js + Express
- Database: PostgreSQL

<!-- feature-5.1.md -->
## Technology Stack
- Frontend: React 18
- Backend: Node.js + Express
- Database: PostgreSQL
```

✅ **Good** (Single Source):
```markdown
<!-- epic-5.md -->
## Technology Stack
See [Technology Stack ADR](../architecture/decisions/ADR-001-tech-stack.md)

<!-- feature-5.1.md -->
## Technology Stack
Follows Epic 5 technology decisions. See [Epic 5](../../planning/_main/epic-5-data-management.md#technology-stack)
```

**Benefits**:
- Updates in one place
- Always consistent
- Clear authority

---

## Pattern 2: Bidirectional References

**Problem**: Parent document references child, but child doesn't reference parent, making navigation difficult.

**Solution**: Maintain bidirectional links between related documents.

**Example**:

❌ **Bad** (One-way reference):
```markdown
<!-- epic-5.md -->
## Features
- [Feature 5.1 - Global Services](../../implementation/_main/feature-5.1-global-services.md)

<!-- feature-5.1.md -->
# Feature 5.1: Global Services
[No reference back to Epic 5]
```

✅ **Good** (Bidirectional):
```markdown
<!-- epic-5.md -->
## Features
- [Feature 5.1 - Global Services](../../implementation/_main/feature-5.1-global-services.md)

<!-- feature-5.1.md -->
# Feature 5.1: Global Services

**Parent Epic**: [Epic 5 - Data Management](../../planning/_main/epic-5-data-management.md)
```

**Benefits**:
- Easy navigation both directions
- Clear relationships
- Better context

---

## Pattern 3: Explicit Superseding

**Problem**: ADRs evolve, but old decisions not marked as superseded, causing confusion.

**Solution**: Explicitly mark superseded ADRs with reference to replacement.

**Example**:

❌ **Bad** (Unmarked superseding):
```markdown
<!-- ADR-010-use-rest.md -->
**Status**: Accepted
[No mention of ADR-020]

<!-- ADR-020-use-graphql.md -->
**Status**: Accepted
**Context**: We need more flexible API queries...
```

✅ **Good** (Explicit superseding):
```markdown
<!-- ADR-010-use-rest.md -->
**Status**: Superseded by [ADR-020](ADR-020-use-graphql.md)
**Superseded Date**: 2025-01-15

<!-- ADR-020-use-graphql.md -->
**Status**: Accepted
**Supersedes**: [ADR-010 - Use REST](ADR-010-use-rest.md)
**Context**: After experience with ADR-010's REST approach, we found...
```

**Benefits**:
- Clear decision history
- No confusion about current approach
- Audit trail

---

## Pattern 4: Hierarchical Numbering

**Problem**: Difficult to understand relationships between epics, features, and waves.

**Solution**: Use hierarchical numbering that encodes relationships.

**Example**:

❌ **Bad** (Flat numbering):
```
epic-5.md
feature-23.md (belongs to epic-5)
feature-24.md (belongs to epic-5)
wave-101.md (belongs to feature-23)
```

✅ **Good** (Hierarchical):
```
epic-5-data-management.md
feature-5.1-global-services.md (epic 5, feature 1)
feature-5.2-data-pipeline.md (epic 5, feature 2)
wave-5.1.1-foundation-setup.md (epic 5, feature 1, wave 1)
wave-5.1.2-core-services.md (epic 5, feature 1, wave 2)
```

**Benefits**:
- Relationship obvious from name
- Easy to find related documents
- Scalable numbering scheme

---

## Pattern 5: Progressive Disclosure

**Problem**: Documents become massive, hard to navigate, duplicating information at different levels of detail.

**Solution**: Summary at parent level, details in child documents.

**Example**:

❌ **Bad** (All details in parent):
```markdown
<!-- epic-5.md -->
## Feature 5.1: Global Services
[3 pages of detailed feature specification]

## Feature 5.2: Data Pipeline
[3 pages of detailed feature specification]
```

✅ **Good** (Summary + links):
```markdown
<!-- epic-5.md -->
## Feature 5.1: Global Services
Provides globally accessible services (logging, config, auth) for the platform.

**Key deliverables**: Singleton services, centralized configuration, shared logging

**Details**: See [Feature 5.1 specification](../../implementation/_main/feature-5.1-global-services.md)

## Feature 5.2: Data Pipeline
...
```

**Benefits**:
- Epic remains readable overview
- Details where needed
- Avoid duplication

---

## Pattern 6: Dependency Declaration

**Problem**: Implicit dependencies cause issues when implementing features in wrong order.

**Solution**: Explicitly declare dependencies at each level.

**Example**:

❌ **Bad** (Implicit dependency):
```markdown
<!-- feature-5.2.md -->
## Technical Approach
We'll use the logging service for all operations.
[No mention that feature-5.1 must be implemented first]
```

✅ **Good** (Explicit dependency):
```markdown
<!-- feature-5.2.md -->
## Dependencies

### Feature Dependencies
- **Depends on**: [Feature 5.1 - Global Services](feature-5.1-global-services.md)
  - **Reason**: Requires logging and config services
  - **Specific requirement**: Logging service must be operational

### External Dependencies
- PostgreSQL 14+
- Redis 6+

## Technical Approach
Uses the logging service from Feature 5.1 for all operations...
```

**Benefits**:
- Clear implementation order
- Explicit requirements
- Prevents surprises

---

## Pattern 7: Version Consistency Matrix

**Problem**: Multiple features using different versions of same library, causing dependency conflicts.

**Solution**: Maintain version matrix in central location.

**Example**:

✅ **Central Version Matrix** (in ADR or Architecture doc):
```markdown
<!-- ADR-001-tech-stack.md -->
## Approved Technology Versions

| Technology | Version | Features Using | Notes |
|------------|---------|----------------|-------|
| React | 18.2.0 | 5.1, 5.2, 6.1 | Standard for all new features |
| Express | 4.18.2 | 5.1, 5.2 | API framework |
| PostgreSQL | 14.x | All features | Database |
| TypeScript | 5.0+ | All features | Language |

**Version Update Process**: Create new ADR to change versions
```

**Benefits**:
- Single source for versions
- Easy to spot conflicts
- Clear update process

---

## Pattern 8: ADR Cross-Reference Map

**Problem**: ADRs reference each other but relationships not clear.

**Solution**: Maintain ADR relationship map.

**Example**:

✅ **ADR Relationship Section**:
```markdown
<!-- ADR-020-graphql-api.md -->
## Related ADRs

**Supersedes**:
- [ADR-010 - Use REST API](ADR-010-use-rest.md)

**Depends on**:
- [ADR-001 - Technology Stack](ADR-001-tech-stack.md) - Requires Node.js + Express
- [ADR-005 - Authentication](ADR-005-jwt-auth.md) - GraphQL uses JWT auth

**Related**:
- [ADR-015 - Error Handling](ADR-015-error-handling.md) - GraphQL errors follow this format

**Influenced by**:
- [ADR-008 - API Versioning](ADR-008-api-versioning.md) - GraphQL handles versioning differently
```

**Benefits**:
- Clear ADR relationships
- Easy to find related decisions
- Understand decision dependencies

---

## Pattern 9: Traceability Chain

**Problem**: Hard to trace from business requirement down to implementation task.

**Solution**: Maintain clear traceability at each level.

**Example**:

✅ **Full Traceability**:
```markdown
<!-- epic-5.md -->
**Business Goal**: Improve data management efficiency by 50%
**Success Metrics**: Query time < 100ms, 99.9% uptime

<!-- feature-5.1.md -->
**Epic**: [Epic 5 - Data Management](../../planning/_main/epic-5-data-management.md)
**Contributes to**: Epic success metric "99.9% uptime" via centralized logging

<!-- wave-5.1.1.md -->
**Feature**: [Feature 5.1 - Global Services](../../implementation/_main/feature-5.1-global-services.md)
**Implements**: Foundation for centralized logging service

<!-- User Story US-5.1.1.1 -->
**Wave**: [Wave 5.1.1 - Foundation Setup](../iterations/wave-5.1.1-foundation-setup.md)
**Implements**: Logging service singleton class

<!-- Task T-5.1.1.1.1 -->
**User Story**: US-5.1.1.1 - Implement logging service
**Implements**: Create LoggerService class with getInstance method
```

**Benefits**:
- Full traceability
- Impact analysis possible
- Clear purpose at each level

---

## Pattern 10: Architecture Evolution Documentation

**Problem**: Architecture changes over time but evolution not documented, causing confusion.

**Solution**: Document architectural evolution explicitly.

**Example**:

✅ **Evolution Section in Architecture Doc**:
```markdown
<!-- 05-Architecture.md -->
## Architectural Evolution

### Phase 1: Monolith (2024-01 to 2024-06)
- Single application
- See [ADR-001](../decisions/ADR-001-monolith-start.md)

### Phase 2: Service Extraction (2024-07 to 2024-12)
- Extract auth service
- Extract payment service
- See [ADR-015](../decisions/ADR-015-service-extraction.md)

### Phase 3: Microservices (2025-01 onwards) ← Current
- Full microservices architecture
- Service mesh with Istio
- See [ADR-025](../decisions/ADR-025-microservices-migration.md)

**Migration Status**: 60% complete (see [migration tracker](../migration-status.md))
```

**Benefits**:
- Understand why things are the way they are
- Clear direction
- Context for decisions

---

## Pattern 11: Conflict Resolution Markers

**Problem**: When conflicts arise, resolution not documented.

**Solution**: Add resolution markers to documents.

**Example**:

✅ **Conflict Resolution Note**:
```markdown
<!-- feature-5.1.md -->
## Technology Stack

**Framework**: Express 4.18.2

> **Note**: Original design specified Fastify (2025-01-10), changed to Express to align with Epic 5 standard (2025-01-12). See [discussion](link-to-discussion) and [ADR-001](../architecture/decisions/ADR-001-tech-stack.md).
```

**Benefits**:
- Understand why decision changed
- Prevent re-introducing conflicts
- Audit trail

---

## Pattern 12: Periodic Consistency Audits

**Problem**: Documentation drifts over time without regular checks.

**Solution**: Schedule regular cross-documentation verification.

**Example**:

✅ **Audit Schedule**:
```markdown
<!-- Docs/DOCUMENTATION-MAINTENANCE.md -->
## Documentation Audit Schedule

### Quarterly (every 3 months)
- [ ] Run cross-documentation-verification on all features
- [ ] Check ADR consistency
- [ ] Update Architecture.md with any drift
- [ ] Consolidate duplicate content

### After Each Epic
- [ ] Verify epic-feature-wave alignment
- [ ] Check for conflicting patterns
- [ ] Update version matrix

### Before Major Release
- [ ] Full documentation review
- [ ] Verify all cross-references valid
- [ ] Check for outdated information
```

**Benefits**:
- Proactive drift detection
- Prevents accumulation of issues
- Maintains documentation quality

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Copy-Paste Documentation
**Problem**: Copying sections between documents instead of referencing
**Fix**: Use Single Source of Truth pattern

### ❌ Anti-Pattern 2: Implicit Dependencies
**Problem**: Features depend on others but not documented
**Fix**: Use Dependency Declaration pattern

### ❌ Anti-Pattern 3: Orphaned Documents
**Problem**: Documents not referenced by any parent
**Fix**: Use Bidirectional References pattern

### ❌ Anti-Pattern 4: Stealth Superseding
**Problem**: New ADR replaces old one without marking it
**Fix**: Use Explicit Superseding pattern

### ❌ Anti-Pattern 5: Mega-Documents
**Problem**: Single document contains everything
**Fix**: Use Progressive Disclosure pattern

---

## Consistency Checklist

Before finalizing any documentation:

- [ ] Used SSOT pattern (no duplication)
- [ ] Added bidirectional references
- [ ] Declared all dependencies explicitly
- [ ] Followed hierarchical numbering
- [ ] Maintained traceability chain
- [ ] Checked for conflicts with related docs
- [ ] Used cross-references instead of copying
- [ ] Updated version matrix if applicable
- [ ] Marked superseded decisions if applicable
- [ ] Verified all links work

---

**Last Updated**: 2025-01-21
