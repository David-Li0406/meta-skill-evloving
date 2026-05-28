# Conformance Scoring Rubric

Detailed methodology for calculating architectural conformance scores.

---

## Base Scoring Formula

**Starting Score**: 100 points

**Deductions**:
- Critical violations: -20 points each
- Warnings: -5 points each
- Info items: -1 point each

**Minimum Score**: 0 (cannot go negative)

**Formula**:
```
Score = max(0, 100 - (critical × 20) - (warnings × 5) - (info × 1))
```

---

## Severity Classification

### Critical Violations (🔴) - 20 points each

**Criteria**:
- Security vulnerability introduced
- Breaking change to established API contract
- Violates compliance requirement (HIPAA, PCI DSS, GDPR, SOC 2)
- Incompatible with core architecture (breaks fundamental design)
- Uses unapproved technology/framework
- Data corruption risk
- System stability risk

**Examples**:
- Using HTTP instead of HTTPS for API communication
- Bypassing authentication on protected endpoint
- Storing plaintext passwords
- Using unapproved database (MongoDB when PostgreSQL required)
- Breaking RESTful API contract (changing response schema)
- Direct instantiation when dependency injection required

**Why -20 points?**
- 5 critical violations = 0 score (complete failure)
- Single critical violation = 80 score (major issue, needs immediate fix)

---

### Warnings (🟡) - 5 points each

**Criteria**:
- Pattern variation without clear justification
- Missing established error handling pattern
- Inconsistent with team conventions
- Potential maintainability issue
- Performance concern (not critical)
- Missing test coverage below threshold
- Incomplete documentation
- Tight coupling introduced

**Examples**:
- Public constructor in singleton (should be private)
- Missing try/catch when ADR requires error handling
- Using camelCase when PascalCase is convention
- N+1 query problem in data access
- Test coverage at 65% when ADR requires 80%
- Missing API documentation for new endpoint

**Why -5 points?**
- 20 warnings = 0 score (death by a thousand cuts)
- 4 warnings = 80 score (acceptable with plan to address)
- Single warning = 95 score (minor issue)

---

### Info Items (🔵) - 1 point each

**Criteria**:
- Opportunity for optimization (not required)
- Alternative pattern would be clearer (subjective)
- Documentation could be enhanced (nice to have)
- Best practice not followed (but not required by ADR)
- Could use more idiomatic approach
- Missing convenience features

**Examples**:
- Could use factory pattern instead of if/else (both work)
- Could add JSDoc comments for better IDE support
- Could extract magic number to constant
- Could use async/await instead of promises
- Could add request/response examples to API docs

**Why -1 point?**
- Info items are suggestions, not requirements
- 100 info items = 0 score (excessive suggestions)
- 10-20 info items common in good code
- Should not significantly impact score

---

## Phase-Specific Thresholds

### Phase 1: Feature Design Validation

**When**: During `/design-features` (Step 4 - Document ADRs)

**Threshold Recommendations**:
- **90-100**: PROCEED — Excellent conformance
- **70-89**: PROCEED — Good conformance, minor issues
- **50-69**: REVISE — Significant issues, needs rework
- **0-49**: BLOCK — Critical issues, redesign required

**Rationale**:
- Design phase should catch issues early
- 70% threshold allows exploration while maintaining standards
- Lower bar than implementation to encourage innovation

**Typical Violation Distribution at 70**:
- 1 critical + 2 warnings = 70 (acceptable)
- 0 critical + 6 warnings = 70 (acceptable)
- 2 critical + 0 warnings = 60 (blocked - too many critical)

---

### Phase 2: Wave Design Validation

**When**: During `/design-waves` (before implementation)

**Threshold Recommendations**:
- **90-100**: PROCEED — Excellent conformance
- **80-89**: PROCEED — Good conformance
- **60-79**: REVISE — Issues found, needs adjustment
- **0-59**: BLOCK — Significant issues, redesign required

**Rationale**:
- Implementation approach should be solid before coding
- 80% threshold ensures quality before development effort
- Higher bar than feature design (more details specified)

**Typical Violation Distribution at 80**:
- 1 critical = 80 (borderline - should fix before implementing)
- 4 warnings = 80 (acceptable - minor issues)
- 0 critical + 4 warnings = 80 (good to proceed)

---

### Phase 3: Post-Implementation Validation

**When**: During `/implement-waves` (Step 5 - Architecture Review)

**Threshold Recommendations**:
- **95-100**: PROCEED — Excellent code quality
- **90-94**: PROCEED — Good code quality
- **75-89**: REVISE — Code quality issues, refactor needed
- **0-74**: BLOCK — Significant issues, cannot merge

**Rationale**:
- Production code must meet high standards
- 90% threshold ensures technical debt stays low
- Highest bar (code is written, fixing is easier than redesign)

**Typical Violation Distribution at 90**:
- 0 critical + 2 warnings = 90 (acceptable)
- 1 critical = 80 (blocked - must fix critical)
- 0 critical + 0 warnings + 10 info = 90 (acceptable)

---

## Scoring Examples

### Example 1: Perfect Score

**Violations**:
- 0 critical
- 0 warnings
- 0 info

**Calculation**:
```
Score = 100 - (0 × 20) - (0 × 5) - (0 × 1) = 100
```

**Result**: 100/100 ✅ PROCEED

**Interpretation**: Exceptional conformance, no issues found

---

### Example 2: Minor Issues

**Violations**:
- 0 critical
- 2 warnings (missing error handling, inconsistent naming)
- 5 info (could add docs, could extract constants)

**Calculation**:
```
Score = 100 - (0 × 20) - (2 × 5) - (5 × 1) = 85
```

**Result**: 85/100 ✅ PROCEED (all phases)

**Interpretation**: Good conformance, minor improvements suggested

---

### Example 3: One Critical Issue

**Violations**:
- 1 critical (using HTTP instead of HTTPS)
- 3 warnings (missing tests, incomplete docs, N+1 query)
- 8 info (various optimizations)

**Calculation**:
```
Score = 100 - (1 × 20) - (3 × 5) - (8 × 1) = 57
```

**Result**: 57/100 ⚠️ REVISE (design/wave), ❌ BLOCK (implementation)

**Interpretation**: Critical security issue must be fixed

---

### Example 4: Many Warnings

**Violations**:
- 0 critical
- 15 warnings (various pattern violations, missing conventions)
- 10 info (optimizations)

**Calculation**:
```
Score = 100 - (0 × 20) - (15 × 5) - (10 × 1) = 15
```

**Result**: 15/100 ❌ BLOCK (all phases)

**Interpretation**: Technical debt accumulation, needs significant rework

---

### Example 5: Multiple Critical Issues

**Violations**:
- 3 critical (plaintext passwords, no authentication, SQL injection)
- 5 warnings (various issues)
- 10 info (optimizations)

**Calculation**:
```
Score = 100 - (3 × 20) - (5 × 5) - (10 × 1) = 5
```

**Result**: 5/100 ❌ BLOCK (all phases)

**Interpretation**: Fundamental security issues, complete redesign needed

---

## Score Interpretation Guide

### 95-100: Exceptional
- Exemplary conformance
- Can be used as reference implementation
- No significant issues

### 85-94: Strong
- Good conformance with minor issues
- Issues are suggestions, not problems
- Safe to proceed

### 70-84: Acceptable (Design Phase)
- Conformance acceptable for early phase
- Issues identified, plan to address
- Proceed with monitoring

### 60-79: Needs Improvement
- Significant issues found
- Requires rework before proceeding
- Address warnings before implementation

### 50-59: Poor
- Major conformance issues
- Critical problems present
- Block until fixed

### 0-49: Failing
- Fundamental architectural problems
- Multiple critical violations
- Requires redesign

---

## Weighting Modifiers (Advanced)

Some violations may be weighted differently based on context:

### Critical Path Components (×1.5 weight)
- Authentication/authorization
- Payment processing
- Data encryption
- Compliance-related code

**Example**:
- Normal critical violation: -20 points
- Critical path critical violation: -30 points

### Experimental Features (×0.5 weight)
- Proof-of-concept code
- Research/exploration
- Temporary implementations

**Example**:
- Normal warning: -5 points
- Experimental warning: -2.5 points

---

## Calculating Category Scores

The overall score can be broken down by category:

### Category: Design Patterns
```
Pattern Score = 100 - (pattern_critical × 20) - (pattern_warnings × 5) - (pattern_info × 1)
```

### Category: ADR Compliance
```
ADR Score = 100 - (adr_critical × 20) - (adr_warnings × 5) - (adr_info × 1)
```

### Category: Structural Standards
```
Structure Score = 100 - (structure_critical × 20) - (structure_warnings × 5) - (structure_info × 1)
```

### Category: Security
```
Security Score = 100 - (security_critical × 20) - (security_warnings × 5) - (security_info × 1)
```

**Overall Score = Average of category scores**

---

## Script Usage

Use `calculate_conformance_score.py` to compute scores:

```bash
# From violation counts
python scripts/calculate_conformance_score.py \
  --critical 2 \
  --warnings 5 \
  --info 3 \
  --phase implementation \
  --format text

# From JSON file
python scripts/calculate_conformance_score.py \
  --violations-json violations.json \
  --phase production \
  --format json
```

**JSON Format**:
```json
{
  "critical": 2,
  "warnings": 5,
  "info": 3
}
```

**Output**:
```
Conformance Score: 65/100 ⚠️

Violations:
  Critical: 2 (-40 points)
  Warnings: 5 (-25 points)
  Info:     3 (-3 points)

Recommendation (implementation phase): REVISE ⚠️
```

---

## Reporting Guidelines

When reporting scores:

1. **Show overall score prominently**: `85/100 ✅`
2. **Break down by severity**: Critical: 0, Warnings: 3, Info: 5
3. **Show deductions**: `-15 points from warnings`
4. **Provide recommendation**: `PROCEED` / `REVISE` / `BLOCK`
5. **List violations by category**: Group related issues
6. **Show positive findings**: What conforms well
7. **Provide remediation**: How to fix each issue

---

## Continuous Monitoring

Track conformance scores over time:

```
Wave 5.1.1: 92/100 ✅ (1 warning, 3 info)
Wave 5.1.2: 88/100 ✅ (0 critical, 2 warnings, 8 info)
Wave 5.2.1: 95/100 ✅ (0 critical, 1 warning, 0 info)
Wave 5.2.2: 78/100 ⚠️ (1 critical, 0 warnings, 2 info)
```

**Trends to watch**:
- ⬆️ Improving scores: Good trajectory
- ⬇️ Declining scores: Tech debt accumulating
- 📊 Stable high scores: Maintaining quality
- 🔴 Critical violations appearing: Process breakdown

---

**Last Updated**: 2025-01-21
