# Confidence Scoring Rubric

> Quantitative risk assessment for specs and PRPs. Confidence scores predict execution success probability based on five weighted factors.

---

## Purpose

Confidence scoring answers the question: **"How likely is this spec to execute successfully?"**

A low confidence score doesn't mean "don't do it" — it means "acknowledge the risk and either mitigate it or accept it." The OpenSearch disaster (INVARIANT-44) would have scored 3.5/10 on this rubric. That low score should have triggered additional validation before proceeding.

---

## Score Ranges

| Range | Label | Signal | Action |
|-------|-------|--------|--------|
| **1-3** | Low (Red) | High risk of failure or rework | STOP. Address gaps before proceeding. |
| **4-6** | Medium (Caution) | Execution possible but risky | PROCEED with explicit risk mitigation plan. |
| **7-9** | High (Green) | Strong probability of success | PROCEED. Normal execution path. |
| **10** | Perfect (Rare) | All factors maximized | PROCEED. Consider this a template for future specs. |

**Note**: A score of 10/10 is rare and should be viewed with skepticism. If everything looks perfect, you might be missing something.

---

## Scoring Framework

### The Five Factors

| Factor | Weight | Description |
|--------|--------|-------------|
| **Requirement Clarity** | 30% | How unambiguous and complete are the requirements? |
| **Pattern Availability** | 25% | Do we have proven patterns/examples to follow? |
| **Test Coverage Plan** | 20% | How well-defined is the validation strategy? |
| **Edge Case Handling** | 15% | Are edge cases identified and addressed? |
| **Tech Familiarity** | 10% | How well does the team know the technology? |

### Calculation Formula

```
confidence_score = (
    requirement_clarity * 0.30 +
    pattern_availability * 0.25 +
    test_coverage_plan * 0.20 +
    edge_case_handling * 0.15 +
    tech_familiarity * 0.10
) * 10
```

Each factor is scored 0.0 to 1.0, resulting in a final score of 1-10.

---

## Factor Scoring Guidelines

### 1. Requirement Clarity (30% weight)

**Why 30%**: Requirements are the foundation. Ambiguous requirements cascade into every downstream decision.

| Score | Description | Example |
|-------|-------------|---------|
| **0.1-0.3** | Vague or missing requirements | "Make it fast" / "Improve the user experience" |
| **0.4-0.5** | Partial requirements with gaps | Has some metrics but missing key acceptance criteria |
| **0.6-0.7** | Complete but some ambiguity | All requirements listed but 2-3 need clarification |
| **0.8-0.9** | Clear, measurable requirements | Specific metrics, thresholds, validation methods |
| **1.0** | Unambiguous, testable, complete | Every requirement has acceptance criteria with pass/fail |

**Red Flags**:
- Subjective terms without definitions ("user-friendly", "quality", "fast")
- Missing success metrics
- "TBD" or "to be determined" anywhere in requirements
- Requirements that reference other unwritten documents

**How to Improve**:
- Replace every subjective term with a metric + threshold
- Define acceptance criteria for each requirement
- Get stakeholder sign-off on requirements before scoring

---

### 2. Pattern Availability (25% weight)

**Why 25%**: Following proven patterns dramatically reduces risk. Novel approaches compound uncertainty.

| Score | Description | Example |
|-------|-------------|---------|
| **0.1-0.3** | No patterns exist, greenfield | First time anyone has done this in your org |
| **0.4-0.5** | Partial patterns available | Similar project exists but significant differences |
| **0.6-0.7** | Good patterns with adaptation needed | Reference implementation available, needs modification |
| **0.8-0.9** | Strong patterns, minor customization | Well-documented pattern, team has used before |
| **1.0** | Exact pattern match | Copy-paste with variable substitution |

**Red Flags**:
- "We'll figure it out as we go"
- No reference implementations found
- The pattern exists but in a different language/framework
- Team has never implemented this pattern

**How to Improve**:
- Find reference implementations (GitHub, internal repos, vendor docs)
- Create a proof-of-concept before scoring
- Identify which parts are novel vs. pattern-based

---

### 3. Test Coverage Plan (20% weight)

**Why 20%**: Without a test plan, you can't verify success. Untested code/execution is hope-based engineering.

| Score | Description | Example |
|-------|-------------|---------|
| **0.1-0.3** | No test plan | "We'll test it manually when done" |
| **0.4-0.5** | Incomplete test plan | Unit tests planned but no integration/E2E |
| **0.6-0.7** | Good coverage with gaps | 70-80% of scenarios covered, missing edge cases |
| **0.8-0.9** | Comprehensive test plan | Unit, integration, E2E, performance tests defined |
| **1.0** | TDD-ready with full coverage | Test cases written before implementation |

**Red Flags**:
- "Tests will be written after implementation"
- No defined success criteria for testing
- Manual testing only
- Tests don't match requirements

**How to Improve**:
- Write test cases before scoring (even as pseudocode)
- Define coverage targets (line, branch, scenario)
- Include non-functional tests (performance, security, accessibility)

---

### 4. Edge Case Handling (15% weight)

**Why 15%**: Edge cases cause the unexpected failures that derail projects. The OpenSearch disaster was an edge case (wrong environment endpoint).

| Score | Description | Example |
|-------|-------------|---------|
| **0.1-0.3** | No edge cases identified | Happy path only, "that won't happen" |
| **0.4-0.5** | Some edge cases noted | Major edge cases listed but not addressed |
| **0.6-0.7** | Edge cases identified with partial mitigation | 60-70% of edge cases have mitigation plans |
| **0.8-0.9** | Comprehensive edge case handling | All identified edge cases have mitigations |
| **1.0** | Edge cases tested and validated | Chaos engineering / adversarial testing included |

**Red Flags**:
- "We'll handle that later"
- No failure mode analysis
- Missing input validation
- No rollback/recovery plan

**How to Improve**:
- Conduct pre-mortem: "What could go wrong?"
- Review similar project failures (Spec Deltas)
- Define degradation paths for each failure mode

---

### 5. Tech Familiarity (10% weight)

**Why 10%**: Team expertise accelerates execution. Unfamiliar tech has hidden learning costs.

| Score | Description | Example |
|-------|-------------|---------|
| **0.1-0.3** | Completely new technology | First time using this language/framework/service |
| **0.4-0.5** | Limited exposure | Team has done tutorials but no production experience |
| **0.6-0.7** | Moderate experience | 1-2 production projects with this tech |
| **0.8-0.9** | Strong experience | Regular production use, team has experts |
| **1.0** | Deep expertise | Team contributed to the technology, knows internals |

**Red Flags**:
- "We can learn it as we go"
- No one on team has production experience
- Technology is new/unstable/poorly documented
- Vendor support is limited

**How to Improve**:
- Include learning time in estimates (explicitly)
- Identify internal/external experts for escalation
- Run a spike/prototype before committing

---

## Example Scores

### Example 1: High Confidence (8.5/10)

**Project**: Add pagination to existing user list API

| Factor | Score | Reasoning |
|--------|-------|-----------|
| Requirement Clarity | 0.9 | Clear: page size 20, offset-based, max 100 pages |
| Pattern Availability | 1.0 | Exact pattern in 3 other endpoints |
| Test Coverage Plan | 0.8 | Unit + integration tests defined |
| Edge Case Handling | 0.7 | Empty results, large datasets, invalid params |
| Tech Familiarity | 0.9 | Team built this API |

**Calculation**: (0.9 * 0.30 + 1.0 * 0.25 + 0.8 * 0.20 + 0.7 * 0.15 + 0.9 * 0.10) * 10 = **8.5**

**Action**: PROCEED. Low risk, well-understood work.

---

### Example 2: Medium Confidence (5.3/10)

**Project**: Integrate new ML-based search ranking

| Factor | Score | Reasoning |
|--------|-------|-----------|
| Requirement Clarity | 0.6 | "Improve relevance" — needs specific metrics |
| Pattern Availability | 0.4 | Reference exists but different data model |
| Test Coverage Plan | 0.5 | A/B test planned but no offline evaluation |
| Edge Case Handling | 0.5 | Empty results handled, unclear on timeout |
| Tech Familiarity | 0.5 | Team knows Python but not ML frameworks |

**Calculation**: (0.6 * 0.30 + 0.4 * 0.25 + 0.5 * 0.20 + 0.5 * 0.15 + 0.5 * 0.10) * 10 = **5.3**

**Action**: PROCEED WITH CAUTION. Define relevance metrics, build offline evaluation, allocate learning time.

---

### Example 3: Low Confidence (3.5/10) — The OpenSearch Disaster

**Project**: Production index cleanup automation

This is a reconstruction of what the confidence score WOULD have been for the script that caused the OpenSearch incident.

| Factor | Score | Reasoning |
|--------|-------|-----------|
| Requirement Clarity | 0.4 | "Clean up stale indexes" — no definition of stale, no environment targeting |
| Pattern Availability | 0.3 | No approved deletion patterns for production |
| Test Coverage Plan | 0.2 | No tests, "it worked in dev" |
| Edge Case Handling | 0.2 | No validation of target environment |
| Tech Familiarity | 0.7 | Team knows OpenSearch |

**Calculation**: (0.4 * 0.30 + 0.3 * 0.25 + 0.2 * 0.20 + 0.2 * 0.15 + 0.7 * 0.10) * 10 = **3.5**

**Action**: STOP. This score would have flagged the project for review before execution.

**What a pre-execution review would have caught**:
1. No environment validation in requirements
2. No pattern for safe production deletions
3. No test for "wrong environment" scenario
4. Missing edge case: "What if env vars are wrong?"

The 14-hour outage and $340,000 impact could have been prevented with a 30-minute spec review triggered by the low confidence score.

---

### Example 4: Perfect Score (10/10) — Rare

**Project**: Add new field to existing config file

| Factor | Score | Reasoning |
|--------|-------|-----------|
| Requirement Clarity | 1.0 | Exact field name, type, default value, validation |
| Pattern Availability | 1.0 | Identical pattern used 50+ times |
| Test Coverage Plan | 1.0 | Existing test framework covers new fields automatically |
| Edge Case Handling | 1.0 | Schema validation handles all invalid inputs |
| Tech Familiarity | 1.0 | Team owns this codebase |

**Calculation**: (1.0 * 0.30 + 1.0 * 0.25 + 1.0 * 0.20 + 1.0 * 0.15 + 1.0 * 0.10) * 10 = **10.0**

**Note**: This is a trivially simple change. Perfect scores are uncommon for anything non-trivial.

---

## How to Improve Scores

### Quick Wins by Factor

| Factor | Quick Win | Time Investment |
|--------|-----------|-----------------|
| Requirement Clarity | Stakeholder review meeting | 1 hour |
| Pattern Availability | Find reference implementation | 2-4 hours |
| Test Coverage Plan | Write test case list (not code) | 1-2 hours |
| Edge Case Handling | Pre-mortem session | 30 minutes |
| Tech Familiarity | Identify expert, schedule consult | 30 minutes |

### Score Improvement Strategies

**From 3-4 to 5-6 (Red to Yellow)**:
1. Convert all subjective requirements to measurable criteria
2. Find at least one reference implementation
3. Define test success criteria (even if tests aren't written)

**From 5-6 to 7-8 (Yellow to Green)**:
1. Complete requirements review with all stakeholders
2. Build proof-of-concept following identified patterns
3. Write test cases (not just criteria)
4. Conduct pre-mortem for edge cases

**From 7-8 to 9+ (Green to High Green)**:
1. Have external review of requirements
2. Run integration tests in staging environment
3. Chaos test edge cases
4. Document decisions for future reference

---

## Integration with PRP

Confidence scores should appear in the PRP Meta section:

```yaml
confidence_score: 7.2
confidence_breakdown:
  requirement_clarity: 0.8
  pattern_availability: 0.7
  test_coverage_plan: 0.7
  edge_case_handling: 0.6
  tech_familiarity: 0.8
```

### PRP Sections That Impact Confidence

| PRP Section | Confidence Factor |
|-------------|-------------------|
| Success Criteria | Requirement Clarity |
| Timeline with Gates | Test Coverage Plan |
| Risk Assessment | Edge Case Handling |
| Resource Requirements | Tech Familiarity |

---

## Automation

Use `confidence-calculator.sh` to compute scores:

```bash
./confidence-calculator.sh 0.8 0.7 0.7 0.6 0.8
# Output: Confidence Score: 7.2 (High/Green) - PROCEED
```

The `spec-to-prp.sh` generator should call this calculator and include the result in generated PRPs.

---

## When to Re-Score

Re-calculate confidence when:
- Requirements change significantly
- New edge cases are discovered
- Team composition changes
- Reference patterns are found/invalidated
- Test plan is updated

Score changes of more than 1.0 point should be documented in the PRP.

---

*Template version: 1.0*
*Last updated: 2026-01-19*
