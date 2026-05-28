# PRP Base Template

> **Product Requirements Prompt** - The compiled output of a validated spec.
> This template transforms human intent into agent-executable blueprints.

---

## Meta

```yaml
prp_id: {{PRP_ID}}
source_spec: {{SOURCE_SPEC_PATH}}
validation_status: {{VALIDATION_STATUS}}  # PASSED | PASSED_WITH_WARNINGS
validated_date: {{VALIDATION_DATE}}
domain: {{DOMAIN}}  # universal | consumer | construction | data | integration | remote | skill-gap
author: {{AUTHOR}}
version: {{VERSION}}
```

---

## Confidence Score

<!--
PURPOSE: Quantitative risk assessment for execution success probability.
COMPILES FROM: Spec analysis against 5 weighted factors.
REFERENCE: See templates/confidence-rubric.md for scoring guidelines.

Score Ranges:
  1-3 (Low/Red)     - STOP: Address gaps before proceeding
  4-6 (Medium/Yellow) - CAUTION: Proceed with risk mitigation plan
  7-9 (High/Green)  - PROCEED: Normal execution path
  10  (Perfect)     - PROCEED: Rare, verify nothing is missed
-->

### Overall Score

| Score | Risk Level | Recommendation |
|-------|------------|----------------|
| **{{CONFIDENCE_SCORE}}** | {{CONFIDENCE_RISK_LEVEL}} | {{CONFIDENCE_RECOMMENDATION}} |

### Breakdown

| Factor | Weight | Score | Contribution | Notes |
|--------|--------|-------|--------------|-------|
| Requirement Clarity | 30% | {{CONFIDENCE_CLARITY}} | {{CONFIDENCE_CLARITY_CONTRIB}} | {{CONFIDENCE_CLARITY_NOTES}} |
| Pattern Availability | 25% | {{CONFIDENCE_PATTERNS}} | {{CONFIDENCE_PATTERNS_CONTRIB}} | {{CONFIDENCE_PATTERNS_NOTES}} |
| Test Coverage Plan | 20% | {{CONFIDENCE_TESTS}} | {{CONFIDENCE_TESTS_CONTRIB}} | {{CONFIDENCE_TESTS_NOTES}} |
| Edge Case Handling | 15% | {{CONFIDENCE_EDGES}} | {{CONFIDENCE_EDGES_CONTRIB}} | {{CONFIDENCE_EDGES_NOTES}} |
| Tech Familiarity | 10% | {{CONFIDENCE_TECH}} | {{CONFIDENCE_TECH_CONTRIB}} | {{CONFIDENCE_TECH_NOTES}} |

### What Would Increase Confidence

<!--
List specific, actionable items that would raise the confidence score.
Focus on the lowest-scoring factors first.
-->

1. {{CONFIDENCE_IMPROVEMENT_1}}
2. {{CONFIDENCE_IMPROVEMENT_2}}
3. {{CONFIDENCE_IMPROVEMENT_3}}

### Risk Factors

<!--
Explicit acknowledgment of risks associated with current confidence level.
These should be addressed in the Risk Assessment section below.
-->

| Risk Factor | Current Mitigation | Residual Risk |
|-------------|-------------------|---------------|
| {{CONFIDENCE_RISK_1}} | {{CONFIDENCE_MITIGATION_1}} | {{CONFIDENCE_RESIDUAL_1}} |
| {{CONFIDENCE_RISK_2}} | {{CONFIDENCE_MITIGATION_2}} | {{CONFIDENCE_RESIDUAL_2}} |

### Confidence Gate

```
CONFIDENCE_CHECK := {{CONFIDENCE_SCORE}} >= 5.0
  IF CONFIDENCE_CHECK == FALSE:
    THEN escalate_to_stakeholder + document_risk_acceptance
  IF {{CONFIDENCE_SCORE}} < 4.0:
    THEN require_explicit_approval_to_proceed
```

---

## 1. Project Overview

<!--
PURPOSE: Provide enough context for an agent to understand WHY this work matters.
COMPILES FROM: Spec overview, user journeys, problem statement.
INVARIANT CHECK: No ambiguous terms (Invariant #1).
-->

### 1.1 Problem Statement

{{PROBLEM_STATEMENT}}

<!-- Example: "Users abandon checkout at 47% rate when shipping estimates exceed 5 days" -->

### 1.2 Solution Summary

{{SOLUTION_SUMMARY}}

<!-- One paragraph describing WHAT we're building, not HOW -->

### 1.3 Scope Boundaries

| In Scope | Out of Scope |
|----------|--------------|
| {{IN_SCOPE_1}} | {{OUT_SCOPE_1}} |
| {{IN_SCOPE_2}} | {{OUT_SCOPE_2}} |
| {{IN_SCOPE_3}} | {{OUT_SCOPE_3}} |

<!-- INVARIANT CHECK: Scope must be bounded (Invariant #6) -->

### 1.4 Key Stakeholders

| Role | Name | Responsibility |
|------|------|----------------|
| {{ROLE_1}} | {{NAME_1}} | {{RESPONSIBILITY_1}} |
| {{ROLE_2}} | {{NAME_2}} | {{RESPONSIBILITY_2}} |

### 1.5 Relevant Patterns

<!--
PURPOSE: Reference applicable patterns from the examples library.
REFERENCE: See examples/ directory for full pattern documentation.
-->

| Pattern | Application | Customization Needed |
|---------|-------------|---------------------|
| {{PATTERN_1}} | {{PATTERN_APPLICATION_1}} | {{PATTERN_CUSTOMIZATION_1}} |
| {{PATTERN_2}} | {{PATTERN_APPLICATION_2}} | {{PATTERN_CUSTOMIZATION_2}} |

**Pattern Links:**
- [API Client](examples/api-client.md) - If integrating with external APIs
- [Error Handling](examples/error-handling.md) - For error boundaries and recovery
- [Test Fixtures](examples/test-fixtures.md) - For test data setup
- [Config Loading](examples/config-loading.md) - For configuration management
- [Database Patterns](examples/database-patterns.md) - For data access layer

---

## 2. Success Criteria

<!--
PURPOSE: Define unambiguous, measurable outcomes.
COMPILES FROM: Spec acceptance criteria, user journey success states.
INVARIANT CHECK: Validation must be executable (Invariant #7).
-->

### 2.1 Primary Metrics

| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| {{METRIC_1}} | {{CURRENT_1}} | {{TARGET_1}} | {{METHOD_1}} |
| {{METRIC_2}} | {{CURRENT_2}} | {{TARGET_2}} | {{METHOD_2}} |
| {{METRIC_3}} | {{CURRENT_3}} | {{TARGET_3}} | {{METHOD_3}} |

### 2.2 Success Conditions

```
SUCCESS := ALL(
  {{CONDITION_1}},
  {{CONDITION_2}},
  {{CONDITION_3}}
)
```

### 2.3 Failure Conditions

```
FAILURE := ANY(
  {{FAILURE_CONDITION_1}},
  {{FAILURE_CONDITION_2}}
)
```

<!-- If any failure condition is true, stop and escalate -->

---

## 3. Timeline with Validation Gates

<!--
PURPOSE: Structure execution into verifiable phases.
COMPILES FROM: Spec milestones, dependency graph.
INVARIANT CHECK: Each gate has explicit pass/fail criteria.
-->

### Phase 1: {{PHASE_1_NAME}}

**Duration**: {{PHASE_1_DURATION}}
**Owner**: {{PHASE_1_OWNER}}

#### Deliverables
- [ ] {{DELIVERABLE_1_1}}
- [ ] {{DELIVERABLE_1_2}}

#### Validation Gate 1

| Criterion | Pass Condition | Verification |
|-----------|---------------|--------------|
| {{GATE_1_CRITERION_1}} | {{GATE_1_PASS_1}} | {{GATE_1_VERIFY_1}} |
| {{GATE_1_CRITERION_2}} | {{GATE_1_PASS_2}} | {{GATE_1_VERIFY_2}} |

```
GATE_1_PASS := {{GATE_1_CONDITION}}
```

**If gate fails**: {{GATE_1_FAILURE_ACTION}}

---

### Phase 2: {{PHASE_2_NAME}}

**Duration**: {{PHASE_2_DURATION}}
**Owner**: {{PHASE_2_OWNER}}
**Depends on**: Gate 1 passed

#### Deliverables
- [ ] {{DELIVERABLE_2_1}}
- [ ] {{DELIVERABLE_2_2}}

#### Validation Gate 2

| Criterion | Pass Condition | Verification |
|-----------|---------------|--------------|
| {{GATE_2_CRITERION_1}} | {{GATE_2_PASS_1}} | {{GATE_2_VERIFY_1}} |
| {{GATE_2_CRITERION_2}} | {{GATE_2_PASS_2}} | {{GATE_2_VERIFY_2}} |

```
GATE_2_PASS := {{GATE_2_CONDITION}}
```

**If gate fails**: {{GATE_2_FAILURE_ACTION}}

---

### Phase 3: {{PHASE_3_NAME}}

**Duration**: {{PHASE_3_DURATION}}
**Owner**: {{PHASE_3_OWNER}}
**Depends on**: Gate 2 passed

#### Deliverables
- [ ] {{DELIVERABLE_3_1}}
- [ ] {{DELIVERABLE_3_2}}

#### Final Validation Gate

| Criterion | Pass Condition | Verification |
|-----------|---------------|--------------|
| {{GATE_FINAL_CRITERION_1}} | {{GATE_FINAL_PASS_1}} | {{GATE_FINAL_VERIFY_1}} |
| {{GATE_FINAL_CRITERION_2}} | {{GATE_FINAL_PASS_2}} | {{GATE_FINAL_VERIFY_2}} |

```
PROJECT_COMPLETE := {{FINAL_GATE_CONDITION}}
```

---

## 4. Risk Assessment and Mitigation

<!--
PURPOSE: Pre-identify failure modes and recovery paths.
COMPILES FROM: Spec dependencies, external systems, skill gaps.
INVARIANT CHECK: Degradation paths exist (Invariant #10).
-->

### 4.1 Risk Matrix

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| {{RISK_1}} | {{PROB_1}} | {{IMPACT_1}} | {{MITIGATION_1}} | {{OWNER_1}} |
| {{RISK_2}} | {{PROB_2}} | {{IMPACT_2}} | {{MITIGATION_2}} | {{OWNER_2}} |
| {{RISK_3}} | {{PROB_3}} | {{IMPACT_3}} | {{MITIGATION_3}} | {{OWNER_3}} |

### 4.2 Fallback Strategies

```
IF {{RISK_1_TRIGGER}}:
  THEN {{FALLBACK_1}}

IF {{RISK_2_TRIGGER}}:
  THEN {{FALLBACK_2}}
```

### 4.3 Circuit Breakers

<!-- INVARIANT CHECK: Cost boundaries explicit (Invariant #8) -->

| Trigger | Threshold | Action |
|---------|-----------|--------|
| {{BREAKER_1_TRIGGER}} | {{BREAKER_1_THRESHOLD}} | {{BREAKER_1_ACTION}} |
| {{BREAKER_2_TRIGGER}} | {{BREAKER_2_THRESHOLD}} | {{BREAKER_2_ACTION}} |

---

## 5. Resource Requirements

<!--
PURPOSE: Enumerate everything needed for execution.
COMPILES FROM: Spec technical requirements, dependencies.
-->

### 5.1 Human Resources

| Role | Allocation | Skills Required |
|------|------------|-----------------|
| {{RESOURCE_ROLE_1}} | {{ALLOCATION_1}} | {{SKILLS_1}} |
| {{RESOURCE_ROLE_2}} | {{ALLOCATION_2}} | {{SKILLS_2}} |

### 5.2 Technical Resources

| Resource | Specification | Purpose |
|----------|--------------|---------|
| {{TECH_RESOURCE_1}} | {{TECH_SPEC_1}} | {{TECH_PURPOSE_1}} |
| {{TECH_RESOURCE_2}} | {{TECH_SPEC_2}} | {{TECH_PURPOSE_2}} |

### 5.3 External Dependencies

<!-- INVARIANT CHECK: Blast radius declared (Invariant #9) -->

| Dependency | Owner | SLA | Fallback |
|------------|-------|-----|----------|
| {{DEPENDENCY_1}} | {{DEP_OWNER_1}} | {{SLA_1}} | {{DEP_FALLBACK_1}} |
| {{DEPENDENCY_2}} | {{DEP_OWNER_2}} | {{SLA_2}} | {{DEP_FALLBACK_2}} |

### 5.4 Budget

| Category | Estimated | Cap | Approval Required |
|----------|-----------|-----|-------------------|
| {{BUDGET_CATEGORY_1}} | {{ESTIMATE_1}} | {{CAP_1}} | {{APPROVAL_1}} |
| {{BUDGET_CATEGORY_2}} | {{ESTIMATE_2}} | {{CAP_2}} | {{APPROVAL_2}} |

---

## 6. Communication Plan

<!--
PURPOSE: Define information flow and escalation paths.
COMPILES FROM: Stakeholder list, risk escalation needs.
-->

### 6.1 Regular Updates

| Audience | Frequency | Format | Owner |
|----------|-----------|--------|-------|
| {{AUDIENCE_1}} | {{FREQUENCY_1}} | {{FORMAT_1}} | {{COMM_OWNER_1}} |
| {{AUDIENCE_2}} | {{FREQUENCY_2}} | {{FORMAT_2}} | {{COMM_OWNER_2}} |

### 6.2 Escalation Matrix

| Condition | Escalate To | Within | Channel |
|-----------|-------------|--------|---------|
| Gate failure | {{ESCALATE_1}} | {{WITHIN_1}} | {{CHANNEL_1}} |
| Budget exceeded | {{ESCALATE_2}} | {{WITHIN_2}} | {{CHANNEL_2}} |
| Blocker >24h | {{ESCALATE_3}} | {{WITHIN_3}} | {{CHANNEL_3}} |

### 6.3 Decision Authority

| Decision Type | Authority | Escalation |
|--------------|-----------|------------|
| Technical implementation | {{AUTHORITY_1}} | {{ESCALATE_TECH}} |
| Scope changes | {{AUTHORITY_2}} | {{ESCALATE_SCOPE}} |
| Timeline changes | {{AUTHORITY_3}} | {{ESCALATE_TIMELINE}} |

---

## 7. Pre-Execution Checklist

<!--
PURPOSE: Verify all prerequisites before starting.
COMPILES FROM: Dependencies, resources, validation status.
-->

### 7.1 Validation Complete

- [ ] Source spec passed validator with no blocking violations
- [ ] All warnings reviewed and accepted
- [ ] Domain-specific invariants checked: {{DOMAIN}}

### 7.2 Resources Confirmed

- [ ] All team members allocated and available
- [ ] Technical resources provisioned
- [ ] Budget approved
- [ ] External dependencies confirmed

### 7.3 Communication Ready

- [ ] Kickoff meeting scheduled
- [ ] Stakeholders notified
- [ ] Escalation contacts confirmed

### 7.4 Risk Preparation

- [ ] Fallback strategies documented
- [ ] Circuit breakers configured
- [ ] Recovery procedures tested (if applicable)

---

## 8. Validation Commands

<!--
PURPOSE: Concrete, copy-pasteable commands to verify implementation.
COMPILES FROM: Test strategy, integration points, acceptance criteria.
REFERENCE: See templates/validation-commands-library.md for more patterns.

Every PRP must include 3-5 specific bash commands that verify:
1. Tests pass (unit/integration)
2. Code quality (linting/types)
3. Integration works (API/service health)
4. Data integrity (if applicable)
5. Build succeeds (compilation/packaging)
-->

### 8.1 Test Verification

```bash
# Run unit tests with coverage
{{VALIDATION_TEST_COMMAND}}

# Run integration tests
{{VALIDATION_INTEGRATION_COMMAND}}
```

### 8.2 Code Quality

```bash
# Type checking
{{VALIDATION_TYPECHECK_COMMAND}}

# Linting
{{VALIDATION_LINT_COMMAND}}
```

### 8.3 Integration Checks

```bash
# API/Service health check
{{VALIDATION_HEALTH_COMMAND}}

# Verify expected output
{{VALIDATION_OUTPUT_COMMAND}}
```

### 8.4 Build Verification

```bash
# Build the project
{{VALIDATION_BUILD_COMMAND}}
```

---

## 9. Recommended Thinking Level

<!--
PURPOSE: Guide cognitive depth for implementation and review.
COMPILES FROM: Confidence score, domain complexity, file impact.
REFERENCE: See docs/thinking-levels.md for detailed guidance.
-->

### Assessment

| Factor | Value | Impact |
|--------|-------|--------|
| Confidence Score | {{CONFIDENCE_SCORE}} | {{THINKING_CONFIDENCE_IMPACT}} |
| Domains Involved | {{DOMAIN_COUNT}} | {{THINKING_DOMAIN_IMPACT}} |
| Invariants Applied | {{INVARIANT_COUNT}} | {{THINKING_INVARIANT_IMPACT}} |
| Files Affected | {{FILE_COUNT}} | {{THINKING_FILE_IMPACT}} |
| Pattern Availability | {{PATTERN_AVAILABILITY}} | {{THINKING_PATTERN_IMPACT}} |

### Recommendation

**Overall Level**: {{THINKING_LEVEL}}

**Apply higher thinking to**:
- {{THINKING_FOCUS_1}}
- {{THINKING_FOCUS_2}}

---

## 10. State Transitions

<!--
PURPOSE: Explicit state machine for project status.
COMPILES FROM: Spec state transitions.
INVARIANT CHECK: State must be explicit (Invariant #2).
-->

```
PROJECT_STATE:
  NOT_STARTED → PHASE_1_ACTIVE     [on: kickoff_complete]
  PHASE_1_ACTIVE → PHASE_1_GATE    [on: phase_1_deliverables_complete]
  PHASE_1_GATE → PHASE_2_ACTIVE    [on: gate_1_passed]
  PHASE_1_GATE → BLOCKED           [on: gate_1_failed]

  PHASE_2_ACTIVE → PHASE_2_GATE    [on: phase_2_deliverables_complete]
  PHASE_2_GATE → PHASE_3_ACTIVE    [on: gate_2_passed]
  PHASE_2_GATE → BLOCKED           [on: gate_2_failed]

  PHASE_3_ACTIVE → FINAL_GATE      [on: phase_3_deliverables_complete]
  FINAL_GATE → COMPLETE            [on: final_gate_passed]
  FINAL_GATE → BLOCKED             [on: final_gate_failed]

  BLOCKED → *_ACTIVE               [on: blocker_resolved]
  * → CANCELLED                    [on: project_cancelled]
```

---

## 11. Execution Log

<!--
PURPOSE: Track actual execution against plan.
Populated during execution, not at PRP creation time.
-->

### Phase Completion

| Phase | Started | Gate Attempted | Gate Result | Notes |
|-------|---------|----------------|-------------|-------|
| Phase 1 | | | | |
| Phase 2 | | | | |
| Phase 3 | | | | |

### Deviations from Plan

| Date | Deviation | Impact | Resolution |
|------|-----------|--------|------------|
| | | | |

### Lessons Learned

<!-- Feed back into spec-delta if significant -->

| Category | Learning | Action |
|----------|----------|--------|
| | | |

---

## Appendix A: Source Spec Reference

**Spec Path**: {{SOURCE_SPEC_PATH}}
**Spec Version**: {{SPEC_VERSION}}
**Invariants Validated**: {{INVARIANTS_LIST}}

### Key Spec Sections Compiled

| Spec Section | PRP Section | Transformation |
|--------------|-------------|----------------|
| {{SPEC_SECTION_1}} | {{PRP_SECTION_1}} | {{TRANSFORM_1}} |
| {{SPEC_SECTION_2}} | {{PRP_SECTION_2}} | {{TRANSFORM_2}} |

---

## Appendix B: Variable Reference

All `{{VARIABLE}}` placeholders must be replaced before execution.

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `PRP_ID` | string | yes | Unique identifier (format: PRP-YYYY-MM-DD-XXX) |
| `SOURCE_SPEC_PATH` | path | yes | Path to validated source spec |
| `VALIDATION_STATUS` | enum | yes | PASSED or PASSED_WITH_WARNINGS |
| `DOMAIN` | enum | yes | Domain invariants applied |
| `METRIC_*` | string | yes | Success metrics with current/target values |
| `GATE_*` | various | yes | Validation gate criteria |
| `RISK_*` | string | no | Risk items (add/remove as needed) |
| `PHASE_*` | various | yes | Phase definitions (add phases as needed) |

### Confidence Score Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `CONFIDENCE_SCORE` | float | yes | Overall confidence score (1.0-10.0) |
| `CONFIDENCE_RISK_LEVEL` | enum | yes | Low/Red, Medium/Yellow, High/Green, or Perfect |
| `CONFIDENCE_RECOMMENDATION` | enum | yes | STOP, CAUTION, or PROCEED |
| `CONFIDENCE_CLARITY` | float | yes | Requirement clarity score (0.0-1.0) |
| `CONFIDENCE_PATTERNS` | float | yes | Pattern availability score (0.0-1.0) |
| `CONFIDENCE_TESTS` | float | yes | Test coverage plan score (0.0-1.0) |
| `CONFIDENCE_EDGES` | float | yes | Edge case handling score (0.0-1.0) |
| `CONFIDENCE_TECH` | float | yes | Tech familiarity score (0.0-1.0) |
| `CONFIDENCE_*_CONTRIB` | float | auto | Weighted contribution (calculated) |
| `CONFIDENCE_*_NOTES` | string | no | Explanation for score |
| `CONFIDENCE_IMPROVEMENT_*` | string | yes | Actions to improve confidence |
| `CONFIDENCE_RISK_*` | string | no | Risk factors from low confidence |
| `CONFIDENCE_MITIGATION_*` | string | no | Current mitigations for risks |
| `CONFIDENCE_RESIDUAL_*` | string | no | Remaining risk after mitigation |

### Validation Command Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `VALIDATION_TEST_COMMAND` | string | yes | Command to run unit tests |
| `VALIDATION_INTEGRATION_COMMAND` | string | no | Command to run integration tests |
| `VALIDATION_TYPECHECK_COMMAND` | string | yes | Command for type checking |
| `VALIDATION_LINT_COMMAND` | string | yes | Command for linting |
| `VALIDATION_HEALTH_COMMAND` | string | no | API/service health check |
| `VALIDATION_OUTPUT_COMMAND` | string | no | Verify expected outputs |
| `VALIDATION_BUILD_COMMAND` | string | yes | Build/compile command |

### Thinking Level Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `THINKING_LEVEL` | enum | yes | Normal, Think, Think Hard, or Ultrathink |
| `THINKING_CONFIDENCE_IMPACT` | string | yes | How confidence affects thinking |
| `THINKING_DOMAIN_IMPACT` | string | yes | How domain complexity affects thinking |
| `THINKING_INVARIANT_IMPACT` | string | yes | How invariant count affects thinking |
| `THINKING_FILE_IMPACT` | string | yes | How file count affects thinking |
| `THINKING_PATTERN_IMPACT` | string | yes | How pattern availability affects thinking |
| `THINKING_FOCUS_*` | string | no | Specific areas needing deeper thought |
| `DOMAIN_COUNT` | int | yes | Number of domains involved |
| `INVARIANT_COUNT` | int | yes | Total invariants applicable |
| `FILE_COUNT` | int | no | Estimated files affected |
| `PATTERN_AVAILABILITY` | enum | yes | exact, adapt, or none |

---

*Template version: 2.0*
*Last updated: 2026-01-19*
