# Phase 2: Constitution Generation Workflow

## Purpose

Derive `memory/constitution.md` - technical principles that emerge FROM user needs defined in product.md. Every principle traces back to user requirements with CoD^Σ evidence.

**Command**: `/generate-constitution`
**Requires**: `memory/product.md`
**Output**: `memory/constitution.md`
**Next**: Manual progression to Phase 3 (`/feature`)

---

## Prerequisites

- `memory/product.md` exists and is complete
- User needs and JTBD are clearly defined

---

## Step 1: Validate Prerequisites

```bash
# Check product.md exists
if [ ! -f memory/product.md ]; then
  echo "ERROR: Run /define-product first"
  exit 1
fi

# Verify completeness
grep -c "Jobs To Be Done" memory/product.md
grep -c "Scope Boundaries" memory/product.md
```

---

## Step 2: Extract User Needs

**Parse product.md for derivable principles:**

| Product Element | Derived Principle Category |
|-----------------|---------------------------|
| Personas | Architecture (who uses what) |
| JTBD | Feature priorities |
| Success metrics | Quality gates |
| Scope boundaries | Constraints |
| Frustrations | Requirements |

**Example Derivation:**
```
User Need: "I want to have a meaningful conversation"
  → Technical Principle: Responses must be contextually aware
  → Implementation: Use memory/context in prompts
  → Quality Gate: Context utilization > 80%
```

---

## Step 3: Define 7 Articles

**Standard Article Structure:**

### Article I: Intelligence-First Development
**Derived From**: [User need from product.md]
**Principle**: Query intelligence sources before reading files
**Enforcement**: All analyses must start with project-intel.mjs queries
**CoD^Σ Trace**: UserNeed@product.md:X → TechnicalRequirement

### Article II: Evidence-Based Claims
**Derived From**: [User need]
**Principle**: All claims require file:line references
**Enforcement**: CoD^Σ traces in all reports
**CoD^Σ Trace**: UserNeed@product.md:X → TechnicalRequirement

### Article III: Test-First Implementation
**Derived From**: [Success metrics from product.md]
**Principle**: Tests written before code, ≥2 ACs per story
**Enforcement**: PR blocks without tests
**CoD^Σ Trace**: SuccessMetric@product.md:X → TestRequirement

### Article IV: Specification-First Development
**Derived From**: [Scope boundaries]
**Principle**: spec.md before plan.md before code
**Enforcement**: Audit gates block implementation
**CoD^Σ Trace**: ScopeBoundary@product.md:X → ProcessRequirement

### Article V: Template-Driven Output
**Derived From**: [Quality requirements]
**Principle**: Use standard templates for consistency
**Enforcement**: Output format validation
**CoD^Σ Trace**: QualityNeed@product.md:X → FormatRequirement

### Article VI: Simplicity
**Derived From**: [MVP scope]
**Principle**: Minimal complexity, ≤3 projects, ≤2 abstraction layers
**Enforcement**: Architecture review
**CoD^Σ Trace**: MVPScope@product.md:X → ArchitectureConstraint

### Article VII: User-Story-Centric
**Derived From**: [JTBD]
**Principle**: Features organized by user stories (P1, P2, P3)
**Enforcement**: Task organization check
**CoD^Σ Trace**: JTBD@product.md:X → OrganizationPrinciple

---

## Step 4: Generate constitution.md

**Template:**

```markdown
# Technical Constitution: [Product Name]

**Derived From**: memory/product.md
**Created**: [timestamp]
**Version**: 1.0

---

## Preamble

This constitution establishes technical principles derived from user needs defined in product.md. Each article traces directly to user requirements.

---

## Article I: Intelligence-First Development

**Source**: [Quote from product.md]
**Derivation**: [How user need → technical principle]

**Principle**: Query project-intel.mjs and MCP tools BEFORE reading files.

**Enforcement**:
- Analysis must start with intel queries
- File reads only after intel queries complete
- Token savings tracked (target: 80%+)

**CoD^Σ Trace**:
```
UserNeed@product.md:15 "need quick answers"
  → TechnicalPrinciple: Minimize processing time
  → Implementation: Intel-first reduces context loading
  → Metric: 80% token savings
```

---

## Article II: Evidence-Based Claims

**Source**: [Quote from product.md]
**Derivation**: [How user need → technical principle]

**Principle**: Every claim requires file:line references or MCP verification.

**Enforcement**:
- No naked claims in reports
- CoD^Σ traces required
- MCP verification for external libraries

---

[Continue for Articles III-VII]

---

## Ratification

This constitution is ratified when:
- [ ] All 7 articles defined
- [ ] Each article traces to product.md
- [ ] Enforcement mechanisms specified
- [ ] CoD^Σ traces complete

---

## Amendment Process

1. Identify new user need or changed requirement
2. Trace to affected article(s)
3. Propose amendment with CoD^Σ derivation
4. Update version and changelog
```

---

## Quality Gates

| Gate | Requirement | Check |
|------|-------------|-------|
| Traceability | Every article traces to product.md | Check CoD^Σ traces |
| Completeness | All 7 articles defined | Count articles |
| Enforcement | Each article has enforcement mechanism | Check enforcement sections |
| No Invention | Principles derived, not invented | Verify product.md sources |

---

## Common Mistakes

| Mistake | Impact | Prevention |
|---------|--------|------------|
| Inventing principles | Disconnected from user needs | Always cite product.md |
| Generic articles | Not actionable | Add specific enforcement |
| Missing traces | Can't verify derivation | Require CoD^Σ per article |
| Too many articles | Overwhelming | Limit to 7-8 core articles |

---

## Handoff to Phase 3

**After constitution.md is complete:**

```markdown
## Phase 2 → Phase 3 Handoff

✅ memory/constitution.md created
✅ 7 Articles defined
✅ All traces to product.md verified
✅ Enforcement mechanisms specified

**Ready for**: /feature "description"
```

---

## Version

**Version**: 1.0.0
**Last Updated**: 2025-12-30
