---
name: cross-documentation-verification
description: Verify consistency and alignment across multiple documentation artifacts (epics, features, waves, ADRs, architecture docs) to detect conflicts, gaps, duplication, and misalignment. Identifies when new features contradict existing patterns, when ADRs conflict, when wave plans deviate from feature specifications, and when implementation docs drift from architecture. Use when finalizing features, before wave implementation, after architecture changes, during conformance reviews, or when detecting documentation drift.
---

# Cross-Documentation Verification

Verifies consistency and alignment across multiple documentation artifacts to detect conflicts, gaps, duplication, and misalignment.

## Quick Start

**Verify feature aligns with architecture:**
```
"Verify feature-5.1 is consistent with Architecture.md and related ADRs"
```

**Check wave aligns with feature:**
```
"Check wave-5.1.1 plan aligns with feature-5.1 specification"
```

**Find conflicting ADRs:**
```
"Verify all ADRs are consistent with each other, identify conflicts"
```

## Core Workflow

### Step 1: Identify Documentation Scope

Determine which documents to verify:

**For Feature Verification**:
- Target: `Docs/implementation/_main/feature-{n}.{m}-{name}.md`
- Check against:
  - `Docs/architecture/_main/05-Architecture.md`
  - `Docs/architecture/decisions/ADR-*.md` (relevant ADRs)
  - Parent epic: `Docs/planning/_main/epic-{n}-{name}.md`
  - Related features: Other feature-{n}.* files

**For Wave Verification**:
- Target: `Docs/implementation/iterations/wave-{n}.{m}.{s}-{name}.md`
- Check against:
  - Parent feature: `feature-{n}.{m}-{name}.md`
  - Architecture docs
  - Relevant ADRs
  - Previous waves from same feature

**For ADR Consistency**:
- Target: All `Docs/architecture/decisions/ADR-*.md`
- Check for:
  - Conflicting decisions
  - Superseded ADRs not marked
  - Missing dependencies between ADRs

**For Architecture Drift**:
- Target: `Docs/architecture/_main/05-Architecture.md`
- Check against:
  - Recent feature plans
  - Recent wave implementations
  - ADRs created after architecture doc

### Step 2: Extract Key Elements

For each document, extract:

#### Architecture Documents
- Component structure
- Technology stack
- Design patterns
- Data flow
- API standards
- Integration points

#### ADRs
- Decision made
- Technology/pattern required
- Constraints imposed
- Superseded decisions
- Related ADRs

#### Epic Plans
- Epic scope
- Success criteria
- Constraints
- Dependencies
- Planned features

#### Feature Plans
- Feature scope
- Technical approach
- Architecture decisions
- Technology choices
- Integration points
- Planned waves
- Dependencies on other features

#### Wave Plans
- Wave scope
- User stories included
- Implementation approach
- Technical decisions
- Dependencies

### Step 3: Run Cross-Verification Checks

Execute verification checks from `references/verification-checklist.md`:

#### Hierarchical Consistency
✅ **Epic → Feature → Wave alignment**:
- Feature scope fits within epic scope?
- Wave deliverables match feature requirements?
- No scope creep or deviation?

✅ **Dependencies resolved**:
- All referenced dependencies exist?
- Dependency versions consistent?
- Circular dependencies detected?

#### Technical Consistency
✅ **Technology Stack**:
- All features use approved technologies?
- No conflicting framework versions?
- Technology choices consistent across features?

✅ **Design Patterns**:
- Pattern usage consistent across features?
- No contradictory pattern guidance?
- Patterns match ADR decisions?

✅ **API Contracts**:
- Endpoint naming consistent?
- Response formats aligned?
- Versioning strategy consistent?

#### Decision Consistency
✅ **ADR Conflicts**:
- No contradictory ADRs?
- Superseded ADRs properly marked?
- ADR dependencies documented?

✅ **Feature-ADR Alignment**:
- Features follow ADR decisions?
- Deviations justified and documented?
- New patterns have ADRs?

#### Content Consistency
✅ **Duplication**:
- No duplicate content across docs?
- Single source of truth maintained?
- Cross-references used appropriately?

✅ **Gaps**:
- All referenced docs exist?
- No missing sections?
- All decisions documented?

### Step 4: Identify Issues

Categorize findings:

**CONFLICT (🔴)**: Must resolve before proceeding
- Feature contradicts ADR decision
- Wave scope differs from feature specification
- ADRs make contradictory decisions
- Technology stack mismatch

**GAP (🟡)**: Should fill, may cause confusion
- Missing ADR for new pattern
- Undocumented dependency
- Missing cross-reference
- Incomplete section

**DUPLICATION (🟠)**: Should consolidate
- Same information in multiple places
- Contradictory versions of same info
- Redundant documentation

**DRIFT (🔵)**: Consider updating
- Architecture doc outdated
- Feature doesn't match current patterns
- ADR no longer relevant

### Step 5: Generate Verification Report

Create report in `Docs/reports/verification/cross-doc-{artifact}-{date}.md`:

```markdown
# Cross-Documentation Verification Report

**Target**: [Document being verified]
**Date**: YYYY-MM-DD
**Documents Checked**: X documents across Y categories

## Executive Summary
[1-2 sentence summary of consistency status]

## Consistency Score: XX/100

## Conflicts (Must Resolve)
### Conflict 1: [Description]
- **Location 1**: [Doc A: section/line]
- **Location 2**: [Doc B: section/line]
- **Conflict**: [What contradicts]
- **Impact**: [Why this matters]
- **Resolution**: [How to resolve]

## Gaps (Should Fill)
[Similar format]

## Duplication (Should Consolidate)
[Similar format]

## Drift (Consider Updating)
[Similar format]

## Positive Findings
- ✅ [What aligns well]
- ✅ [What aligns well]

## Recommendations
1. [Action item 1]
2. [Action item 2]
```

Use `scripts/calculate_consistency_score.py` to compute overall score.

## Key Concepts

**Cross-Documentation Verification**: Process of checking multiple documents for consistency, conflicts, gaps, and duplication

**Hierarchical Consistency**: Alignment across Epic → Feature → Wave hierarchy

**Technical Consistency**: Alignment of technology choices, patterns, and approaches across features

**Decision Consistency**: Alignment of architectural decisions across ADRs

**Content Consistency**: Avoidance of duplication and gaps in documentation

**Consistency Score**: 0-100 metric calculated as:
- Conflicts: -20 points each
- Gaps: -5 points each
- Duplication: -3 points each
- Drift: -1 point each
- Base: 100 points
- Minimum: 0 points

## Available Resources

### Scripts
- **scripts/calculate_consistency_score.py** — Calculates consistency score from issue counts
  ```bash
  python scripts/calculate_consistency_score.py --conflicts 1 --gaps 3 --duplication 2 --drift 5
  # Output: Consistency Score: 68/100
  ```

- **scripts/find_cross_references.py** — Finds all cross-references between documents
  ```bash
  python scripts/find_cross_references.py --doc feature-5.1-global-services.md
  # Output: JSON map of all referenced documents
  ```

- **scripts/detect_duplication.py** — Detects duplicate content across documents
  ```bash
  python scripts/detect_duplication.py --dir Docs/
  # Output: List of duplicate content blocks with similarity scores
  ```

### References
- **references/verification-checklist.md** — Comprehensive checklist of verification points
- **references/common-conflicts.md** — Examples of common documentation conflicts
- **references/consistency-patterns.md** — Patterns for maintaining consistency

## Verification Phases

### Phase 1: Feature Design Verification
**When**: During `/design-features` (after Step 4 - Document ADRs)
**Focus**: Feature consistency with architecture and ADRs
**Output**: Feature alignment report
**Gate**: Medium threshold (70+ score to proceed)

### Phase 2: Wave Design Verification
**When**: During `/design-waves` (before implementation)
**Focus**: Wave plan consistency with feature specification
**Output**: Wave alignment report
**Gate**: High threshold (80+ score to implement)

### Phase 3: Post-Wave Verification
**When**: During `/implement-waves` (after completion)
**Focus**: Implementation matches wave plan and feature spec
**Output**: Implementation alignment report
**Gate**: Critical threshold (90+ score for production)

### Phase 4: Architecture Review
**When**: Periodic (quarterly or after major changes)
**Focus**: Overall documentation consistency
**Output**: Architecture consistency report
**Gate**: Informational (no blocking)

## Common Conflict Patterns

**Conflict 1: Technology Mismatch**
- Issue: Feature specifies React, ADR requires Vue
- Check: Compare feature tech stack against ADR decisions
- Fix: Update feature to use ADR technology or create new ADR

**Conflict 2: Pattern Contradiction**
- Issue: Feature A uses singleton, Feature B uses factory for same concern
- Check: Compare pattern usage across related features
- Fix: Align on single pattern or document when each applies

**Conflict 3: API Contract Deviation**
- Issue: Wave plan changes API format from feature specification
- Check: Compare wave API design against feature API contract
- Fix: Restore feature contract or update feature doc with justification

**Conflict 4: Superseded ADR**
- Issue: Feature follows ADR-010, but ADR-025 supersedes it
- Check: Verify ADR status and superseded relationships
- Fix: Update feature to follow current ADR

## Output Format

**Console Output**:
```
Cross-Documentation Verification
================================

Target: feature-5.1-global-services-foundation.md
Documents Checked: 8 (Architecture, 3 ADRs, Epic-5, 3 related features)

Consistency Score: 82/100 ✅

Conflicts: 1
  🔴 Feature specifies FastAPI, ADR-001 requires Express.js

Gaps: 2
  🟡 No ADR for caching strategy mentioned in feature
  🟡 Missing cross-reference to dependent feature-4.3

Duplication: 1
  🟠 Architecture section duplicated in feature and epic

Drift: 3
  🔵 Architecture doc doesn't mention new microservices pattern
  🔵 Feature approach differs slightly from established pattern
  🔵 ADR-015 may be outdated

Positive Findings:
  ✅ Epic scope alignment perfect
  ✅ All dependencies properly documented
  ✅ Naming conventions consistent

Recommendation: REVISE - Resolve conflict before implementation
Report: Docs/reports/verification/cross-doc-feature-5.1-2025-01-21.md
```

## Integration with Workflow

**`/design-features` integration**:
```markdown
## Step 5: Verify Cross-Documentation Consistency

After completing feature design:
- Invoke `cross-documentation-verification` skill
- Review consistency report
- Resolve CONFLICTS before proceeding
- Document GAPS as follow-up tasks
```

**`/design-waves` integration**:
```markdown
## Step 3: Verify Wave-Feature Alignment

Before finalizing wave plan:
- Verify wave aligns with parent feature
- Check for scope creep or deviation
- Ensure all dependencies resolved
- Score ≥80 required before creating work items
```

**`/implement-waves` integration**:
```markdown
## Step 6: Verify Implementation Alignment

After wave completion:
- Verify implementation matches wave plan
- Check implementation matches feature spec
- Verify no undocumented architecture changes
- Score ≥90 required for merge
```

**Periodic Architecture Review**:
```markdown
## Quarterly Documentation Audit

Every quarter:
- Run cross-verification on all features
- Check ADR consistency
- Update architecture doc if drifted
- Consolidate duplicate content
```

## Success Criteria

- ✅ Consistency score calculated accurately
- ✅ All conflicts identified with locations
- ✅ All gaps documented
- ✅ Duplication detected with similarity scores
- ✅ Drift areas identified
- ✅ Report generated in standard format
- ✅ Decision made (PROCEED/REVISE/BLOCK) based on score

## Tips for High Consistency

1. **Cross-reference early** - Link documents as you create them
2. **Single source of truth** - Avoid duplicating content
3. **Update related docs** - When changing one doc, update references
4. **Mark superseded decisions** - Keep ADR status current
5. **Verify iteratively** - Check at design, pre-implementation, post-implementation
6. **Use verification hooks** - Automate verification in workflow
7. **Maintain traceability** - Epic → Feature → Wave → User Story → Task

## Examples

### Example 1: Feature Verification

**Command**:
```
"Verify feature-5.1-global-services aligns with Architecture.md and ADRs"
```

**Process**:
1. Read feature-5.1-global-services.md
2. Read Docs/architecture/_main/05-Architecture.md
3. Identify relevant ADRs (ADR-018 singleton, ADR-012 security)
4. Extract key elements from each
5. Run verification checks
6. Generate report

**Report Findings**:
- ✅ Architecture alignment: Good
- 🔴 Conflict: Feature uses MongoDB, ADR-003 requires PostgreSQL
- 🟡 Gap: No ADR for caching strategy
- 🟠 Duplication: Tech stack listed in feature and epic

**Score**: 72/100 (1 conflict, 1 gap, 1 duplication)
**Recommendation**: REVISE - Fix database choice

---

### Example 2: Wave-Feature Verification

**Command**:
```
"Verify wave-5.1.1 aligns with feature-5.1-global-services"
```

**Process**:
1. Read wave-5.1.1-foundation-setup.md
2. Read feature-5.1-global-services.md
3. Extract scope and technical approach
4. Compare wave deliverables against feature requirements
5. Check for scope creep or deviation

**Report Findings**:
- ✅ Scope alignment: Perfect match
- ✅ Technical approach: Follows feature specification
- 🔵 Drift: Wave adds logging detail not in feature (minor enhancement)

**Score**: 99/100 (0 conflicts, 0 gaps, 0 duplication, 1 drift)
**Recommendation**: PROCEED - Minor drift is acceptable enhancement

---

### Example 3: ADR Consistency Check

**Command**:
```
"Check all ADRs for conflicts and missing superseded markings"
```

**Process**:
1. Read all ADR files in Docs/architecture/decisions/
2. Extract decisions, status, superseded relationships
3. Build decision dependency graph
4. Check for conflicts and missing relationships

**Report Findings**:
- 🔴 Conflict: ADR-010 requires REST, ADR-020 requires GraphQL (same API)
- 🟡 Gap: ADR-015 superseded by ADR-025, but not marked
- ✅ All other ADRs consistent

**Score**: 85/100 (1 conflict, 1 gap)
**Recommendation**: REVISE - Clarify REST vs GraphQL decision

---

**Last Updated**: 2025-01-21
