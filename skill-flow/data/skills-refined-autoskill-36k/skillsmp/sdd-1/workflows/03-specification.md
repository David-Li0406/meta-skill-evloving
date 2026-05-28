# Phase 3: Feature Specification Workflow

## Purpose

Create `specs/$FEATURE/spec.md` - comprehensive feature specification with functional requirements, user stories, and acceptance criteria.

**Command**: `/feature "description"`
**Requires**: (Optional) `memory/product.md`, `memory/constitution.md`
**Output**: `specs/$FEATURE/spec.md`
**Auto-Chains**: → Phase 5 (`/plan`)

---

## Feature Naming Convention

**Format**: `NNN-feature-name`
- NNN: 3-digit sequential number (001, 002, ...)
- feature-name: kebab-case descriptive name

**Examples**:
- `001-therapy-app`
- `007-voice-agent`
- `015-auth-oauth`

**To determine next number:**
```bash
ls -d specs/[0-9]* 2>/dev/null | tail -1 | sed 's/.*\/\([0-9]*\).*/\1/'
```

---

## Step 1: Quality Gate Check

**Before creating specification:**

```markdown
## Pre-Specification Quality Gate

| Check | Status | Details |
|-------|--------|---------|
| Product clarity | [PASS/FAIL] | Is user problem clear? |
| Scope defined | [PASS/FAIL] | Are boundaries set? |
| Complexity assessed | [PASS/FAIL] | Need Phase 0 first? |

**Score**: X/3 (minimum 2/3 to proceed)
```

**If complexity is high**: Trigger Phase 0 first (see 00-system-understanding.md)

---

## Step 2: Intelligence Gathering

**Execute BEFORE writing spec:**

```bash
# 1. Check existing specs for patterns
ls specs/*/spec.md 2>/dev/null

# 2. Search for related code
project-intel.mjs --search "<feature-keywords>" --json

# 3. Check for existing implementations
project-intel.mjs --search "<similar-feature>" --json

# 4. Review product.md for alignment
cat memory/product.md | head -50
```

---

## Step 3: User Clarification (If Needed)

**Ask max 5 clarifying questions:**

| Category | Question Pattern |
|----------|------------------|
| Scope | "Should this include X or is that separate?" |
| Priority | "Which capability is most important?" |
| Constraints | "Are there performance/security requirements?" |
| Integration | "How should this integrate with existing Y?" |
| Edge Cases | "What should happen when Z occurs?" |

**Use AskUserQuestion tool** for structured input.

---

## Step 4: Create Specification

### 4.1 Directory Setup

```bash
mkdir -p specs/$FEATURE
```

### 4.2 Spec Template

```markdown
# Feature Specification: [Feature Name]

**Spec ID**: $FEATURE
**Created**: [timestamp]
**Status**: Draft

---

## Overview

### Problem Statement
[What problem does this feature solve?]

### Proposed Solution
[High-level description of the solution]

### Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

---

## Functional Requirements

### FR-001: [Requirement Name]
**Priority**: P1/P2/P3
**Description**: [Detailed requirement]
**Rationale**: [Why this is needed]

### FR-002: [Requirement Name]
**Priority**: P1/P2/P3
**Description**: [Detailed requirement]
**Rationale**: [Why this is needed]

[Continue for all FRs...]

---

## User Stories

### US-1: [Story Title]
**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria**:
- [ ] AC-1.1: [Criterion 1]
- [ ] AC-1.2: [Criterion 2]
- [ ] AC-1.3: [Criterion 3]

**Priority**: P1

### US-2: [Story Title]
[Continue pattern...]

---

## Non-Functional Requirements

### NFR-001: Performance
- [Specific performance requirement]

### NFR-002: Security
- [Specific security requirement]

### NFR-003: Reliability
- [Specific reliability requirement]

---

## Constraints & Assumptions

### Constraints
1. [Technical constraint]
2. [Business constraint]

### Assumptions
1. [Assumption that must hold]
2. [Dependency assumption]

---

## Out of Scope

- [Explicitly excluded item 1]
- [Explicitly excluded item 2]

---

## Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| [Dependency 1] | Internal/External | Ready/Pending |

---

## Open Questions

- [ ] [Question needing clarification] - [NEEDS CLARIFICATION]
- [ ] [Question for later phases]

---

## References

- product.md: [Relevant section]
- constitution.md: [Relevant articles]
- Existing code: [Related implementations]

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [date] | Claude | Initial specification |
```

---

## Step 5: Validate Specification

**Quality Checklist:**

```markdown
## Specification Quality Checklist

### Completeness
- [ ] Problem statement clear
- [ ] All functional requirements listed
- [ ] User stories cover all FRs
- [ ] Each story has ≥2 acceptance criteria
- [ ] NFRs defined (performance, security)
- [ ] Out of scope explicitly stated

### Clarity
- [ ] No ambiguous language ("should", "might")
- [ ] Acceptance criteria are testable
- [ ] No [NEEDS CLARIFICATION] markers remaining
- [ ] Dependencies identified

### Alignment
- [ ] Traces to product.md (if exists)
- [ ] Follows constitution.md principles (if exists)
- [ ] Consistent with existing specs
```

---

## Step 6: Register in Master Todo

**Add entry to todos/master-todo.md:**

```markdown
### Spec $NUMBER: [Feature Name]
- Status: Specified
- Spec: [specs/$FEATURE/spec.md](specs/$FEATURE/spec.md)
- Plan: Pending
- Progress: 0/X tasks
```

---

## Quality Gates

| Gate | Requirement | Enforcement |
|------|-------------|-------------|
| FR Coverage | All features have requirements | Count FRs ≥ 3 |
| AC Minimum | Each story has ≥2 ACs | Check all US-* sections |
| Testability | ACs can be tested | No vague language |
| Traceability | Links to product/constitution | References section populated |
| No Ambiguity | No [NEEDS CLARIFICATION] | Grep for marker |

---

## Markers for Clarification

**When something needs clarification:**

```markdown
### FR-005: [Requirement]
**Description**: User authentication via [NEEDS CLARIFICATION: OAuth or magic link?]
```

**If markers present**: Phase 4 (`/clarify`) must run before Phase 5.

---

## Auto-Chain to Phase 5

**After spec.md passes quality gates:**

```markdown
## Phase 3 → Phase 5 Handoff

✅ specs/$FEATURE/spec.md created
✅ X functional requirements defined
✅ Y user stories with Z acceptance criteria
✅ No [NEEDS CLARIFICATION] markers
✅ Registered in master-todo.md

**Automatically invoking**: /plan
```

---

## Common Mistakes

| Mistake | Impact | Prevention |
|---------|--------|------------|
| Vague ACs | Untestable | Use specific, measurable criteria |
| Missing NFRs | Late-stage issues | Always define P/S/R |
| Over-specification | Implementation constraints | Focus on what, not how |
| Missing edge cases | Bugs in production | Ask about failure modes |

---

## Version

**Version**: 1.0.0
**Last Updated**: 2025-12-30
