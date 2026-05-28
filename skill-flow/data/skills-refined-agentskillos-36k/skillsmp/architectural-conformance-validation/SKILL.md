---
name: architectural-conformance-validation
description: Validate that newly designed or implemented features conform to existing architectural patterns, design decisions (ADRs), and technical standards. Includes pattern validation, ADR compliance checking, technology stack verification, and conformance scoring. Use when reviewing feature plans, validating wave designs, verifying post-implementation code, checking architectural drift, or any architecture compliance validation.
---

# Architectural Conformance Validation

Validates that features, waves, and implementation code conform to established architectural patterns, ADR decisions, and technical standards.

## Quick Start

**Validate feature plan:**
```
"Validate architectural conformance for feature-5.1-global-services-foundation.md against Architecture.md and ADRs"
```

**Check wave design:**
```
"Check wave-5.1.1 conforms to singleton pattern from ADR-018"
```

**Verify implementation:**
```
"Verify src/services/ conforms to architecture documented in ADRs"
```

## Core Workflow

### Step 1: Load Architecture Context

Read architectural standards and decisions:

1. **Architecture Document**: `Docs/architecture/_main/05-Architecture.md`
   - Extract: Component structure, design patterns, tech stack, data flow, API standards

2. **ADR Directory**: `Docs/architecture/decisions/`
   - Read `README.md` for ADR index
   - Identify relevant ADRs for the feature/component being validated
   - Read `references/adr-compliance-checklist.md` for validation criteria

3. **Previous Features**: `Docs/implementation/_main/feature-*.md`
   - Identify established patterns from implemented features
   - Note consistency expectations

### Step 2: Analyze Target Artifact

Determine what's being validated:

**For Feature Plans** (`Docs/implementation/_main/feature-*.md`):
- Extract proposed architecture approach
- Identify technology choices
- Note design patterns mentioned
- Find integration points

**For Wave Plans** (`Docs/implementation/iterations/wave-*.md`):
- Extract implementation approach
- Identify specific patterns to be used
- Note technical decisions

**For Source Code** (`src/`, `tests/`):
- Analyze actual implementation
- Identify patterns used
- Check naming conventions
- Verify structure matches architecture

### Step 3: Run Conformance Checks

Execute validation checks from `references/validation-checklist.md`:

#### Pattern Conformance
✅ **Design Patterns**: Singleton, Factory, Dependency Injection, Observer, etc.
- Does implementation follow documented pattern?
- Are pattern variations justified?
- Is pattern application consistent?

✅ **Architectural Patterns**: MVC, Layered, Microservices, Event-Driven, etc.
- Does component fit into defined architecture?
- Are layer boundaries respected?
- Is separation of concerns maintained?

#### ADR Compliance
✅ **Technology Decisions**:
- Uses approved frameworks/libraries from ADRs?
- Follows technology constraints?
- Justifies any deviations?

✅ **Security/Compliance Decisions**:
- Implements security patterns from ADRs?
- Follows authentication/authorization standards?
- Meets compliance requirements (HIPAA, PCI DSS)?

✅ **Algorithm/Approach Decisions**:
- Uses documented algorithms?
- Follows performance optimization decisions?
- Implements error handling as specified?

#### Structural Conformance
✅ **Component Structure**:
- Matches architecture diagram?
- Naming conventions followed?
- Directory structure consistent?

✅ **API Contracts**:
- REST/GraphQL standards followed?
- Error response format consistent?
- Versioning strategy followed?

✅ **Data Flow**:
- Follows documented data flow?
- Uses established data models?
- Respects data boundaries?

### Step 4: Identify Violations and Gaps

For each check, categorize findings:

**CRITICAL (🔴)**: Must fix before implementation
- Violates security ADR
- Breaks established API contract
- Incompatible with architecture

**WARNING (🟡)**: Should fix, may cause issues
- Pattern variation without justification
- Missing error handling pattern
- Inconsistent naming

**INFO (🔵)**: Nice to have, best practice
- Could use more common pattern
- Documentation enhancement opportunity
- Optimization possibility

### Step 5: Generate Conformance Report

Create validation report in `Docs/reports/architecture/conformance-{artifact}-{date}.md`:

```markdown
# Architectural Conformance Report

**Artifact**: [Feature/Wave/Code path]
**Date**: YYYY-MM-DD
**Overall Score**: XX/100

## Executive Summary
[1-2 sentence summary of conformance status]

## Conformance Score Breakdown
- Design Patterns: XX/100
- ADR Compliance: XX/100
- Structural Standards: XX/100
- Technology Stack: XX/100

## Critical Issues (Must Fix)
### Issue 1: [Description]
- **Location**: [File:line or section]
- **Violation**: [What standard violated]
- **ADR Reference**: [ADR-XXX]
- **Impact**: [Why this matters]
- **Remediation**: [How to fix]

## Warnings (Should Fix)
[Similar format]

## Information (Consider)
[Similar format]

## Positive Findings
- ✅ [What conforms well]
- ✅ [What conforms well]

## Recommendations
1. [Action item 1]
2. [Action item 2]
```

Use `scripts/calculate_conformance_score.py` to compute overall score.

## Key Concepts

**Architectural Conformance**: Degree to which implementation aligns with documented architecture

**Design Pattern**: Reusable solution to common problem (Singleton, Factory, Observer, etc.)

**ADR (Architectural Decision Record)**: Document capturing significant architectural decision with context, options considered, decision made, and consequences

**Technology Stack**: Approved frameworks, libraries, languages, and tools

**Conformance Score**: 0-100 metric calculated as:
- Critical violations: -20 points each
- Warnings: -5 points each
- Info items: -1 point each
- Base: 100 points
- Minimum: 0 points

## Available Resources

### Scripts
- **scripts/calculate_conformance_score.py** — Calculates conformance score from violation counts
  ```bash
  python scripts/calculate_conformance_score.py --critical 2 --warnings 5 --info 3
  # Output: Conformance Score: 65/100
  ```

- **scripts/extract_adr_requirements.py** — Extracts checkable requirements from ADRs
  ```bash
  python scripts/extract_adr_requirements.py --adr Docs/architecture/decisions/ADR-018-singleton-pattern.md
  # Output: JSON list of requirements to check
  ```

### References
- **references/validation-checklist.md** — Comprehensive checklist of all validation points
- **references/adr-compliance-checklist.md** — How to validate against specific ADR types
- **references/common-patterns.md** — Reference for recognizing standard design patterns
- **references/scoring-rubric.md** — Detailed scoring methodology

## Validation Phases

### Phase 1: Feature Design Validation
**When**: During `/design-features` (Step 4 - Document ADRs)
**Focus**: Proposed architecture approach
**Output**: Design conformance report
**Gate**: Medium threshold (70+ score to proceed)

### Phase 2: Wave Design Validation
**When**: During `/design-waves` (before implementation)
**Focus**: Implementation plan details
**Output**: Implementation approach conformance
**Gate**: High threshold (80+ score to implement)

### Phase 3: Post-Implementation Validation
**When**: During `/implement-waves` (Step 5 - Architecture Review)
**Focus**: Actual code implementation
**Output**: Code conformance report with file:line references
**Gate**: Critical threshold (90+ score for production)

## Common Violation Patterns

**Anti-Pattern 1: Technology Creep**
- Issue: Introducing new library not in approved stack
- Check: Compare imports/dependencies against tech stack ADR
- Fix: Use approved alternative or create ADR for new tech

**Anti-Pattern 2: Pattern Misapplication**
- Issue: Using Singleton when Factory would be appropriate
- Check: Verify pattern choice aligns with use case
- Fix: Refactor to correct pattern or justify deviation

**Anti-Pattern 3: Implicit Decisions**
- Issue: Making architectural choice without documenting
- Check: Look for new patterns/approaches without ADR
- Fix: Create ADR documenting decision and rationale

**Anti-Pattern 4: Architecture Drift**
- Issue: Small deviations accumulating over time
- Check: Compare against original architecture diagram
- Fix: Refactor to align or update architecture doc

## Output Format

**Console Output**:
```
Architectural Conformance Validation
====================================

Target: feature-5.1-global-services-foundation.md
Architecture: Docs/architecture/_main/05-Architecture.md
ADRs Checked: 3 (ADR-012, ADR-015, ADR-018)

Conformance Score: 85/100 ✅

Critical Issues: 0
Warnings: 3
  ⚠️  Feature doesn't specify error handling pattern (ADR-015)
  ⚠️  Logging approach differs from established pattern
  ⚠️  Missing integration test strategy

Information: 2
  ℹ️  Consider documenting retry logic
  ℹ️  Could add performance benchmarks

Positive Findings:
  ✅ Uses singleton pattern correctly (ADR-018)
  ✅ Technology stack matches approved list
  ✅ Component structure follows architecture diagram

Recommendation: PROCEED with minor adjustments
Report: Docs/reports/architecture/conformance-feature-5.1-2025-01-21.md
```

**Report File**: Detailed markdown report with all findings, remediation steps, and references

## Integration with Workflow

**`/design-features` integration**:
```markdown
## Step 4: Document Architectural Decisions (ADR)

... existing ADR creation steps ...

### Step 4.5: Validate Architectural Conformance

For each Feature plan created:
- Invoke `architectural-conformance-validation` skill
- Review conformance report
- Address CRITICAL issues before proceeding
- Document WARNING items as technical debt
```

**`/design-waves` integration**:
```markdown
## Step 2.5: Validate Wave Design Conformance

Before finalizing wave plan:
- Validate wave approach conforms to feature architecture
- Check ADR compliance for implementation details
- Ensure score ≥80 before creating Azure DevOps work items
```

**`/implement-waves` integration**:
```markdown
## Step 5: Final Architecture Review

- **system-architect**: Run conformance validation
  - Validate src/ against Docs/architecture/_main/05-Architecture.md
  - Check ADR compliance in implementation
  - Generate conformance report
  - Block merge if score <90
```

## Success Criteria

- ✅ Conformance score calculated accurately
- ✅ All violations categorized by severity
- ✅ Each violation references specific ADR or architecture doc
- ✅ Remediation steps provided for each violation
- ✅ Report generated in standard format
- ✅ Decision made (PROCEED/REVISE/BLOCK) based on score and phase

## Tips for High Conformance

1. **Review ADRs early** - Check relevant ADRs before design
2. **Ask "why" for deviations** - Justify any architectural changes
3. **Document new patterns** - Create ADR for novel approaches
4. **Stay consistent** - Follow established patterns from previous features
5. **Validate iteratively** - Check at design, pre-implementation, and post-implementation
6. **Update architecture docs** - Keep Architecture.md current as patterns evolve
