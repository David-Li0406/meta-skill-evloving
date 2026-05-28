# Angle Prompts

Multi-angle analysis framework for GATE-PRD-CONTENT. Each angle provides a structured lens for evaluating PRD quality from a specific perspective.

---

## Overview

During GATE-PRD-CONTENT, dispatch these angles to ensure comprehensive coverage. Each angle emits findings with specific subcategories, enabling deterministic recurrence tracking.

| Angle ID | Focus | Required |
|----------|-------|----------|
| TECHNICAL_FEASIBILITY | Can requirements be implemented? | Yes |
| CUSTOMER_VALUE | Does PRD solve real problems? | Yes |
| IMPLEMENTATION_RISK | What could go wrong? | Yes |
| REUSE_POTENTIAL | Extend existing vs create net-new? | Yes |
| VERIFIABILITY | Are requirements testable? | Yes |
| OPERATIONAL_READINESS | Can this be deployed safely? | No |
| SECURITY_POSTURE | Default-deny maintained? | No |
| COHERENCE_CONSISTENCY | Internally consistent? | Yes |
| TRADEOFF_ANALYSIS | What was sacrificed for optimization? | Yes |
| SYSTEM_DYNAMICS | Feedback loops and ecosystem impact? | Yes |

**Completion Requirement:** All required angles MUST be executed. Optional angles SHOULD be executed for production PRDs.

---

## TECHNICAL_FEASIBILITY

**Focus:** Can requirements be implemented with current technology and constraints?

### Signals to Look For

- Requirements that contradict physical or computational limits
- Stack mismatches (e.g., requiring real-time in a batch-only system)
- Performance targets that violate algorithmic complexity bounds
- Dependencies on unavailable or deprecated technologies
- Hardware or infrastructure assumptions that don't hold

### Finding Subcategories

| Subcategory | Description | Severity |
|-------------|-------------|----------|
| INFEASIBLE | Requirement cannot be implemented as specified | BLOCKER |
| STACK_MISMATCH | Requirement conflicts with system architecture | MAJOR |
| PERF_IMPOSSIBLE | Performance target violates theoretical limits | BLOCKER |

### Evaluation Questions

1. For each requirement with quantitative targets, can the target be achieved given algorithmic constraints?
2. Does the requirement assume infrastructure capabilities that exist?
3. Are there implicit technology dependencies that may not be available?
4. Do requirements assume capabilities that conflict with the current stack?
5. **Fermi Check:** Perform a back-of-the-envelope calculation. If scale increases 100x, does the math still hold?

### Example Evaluation

```yaml
requirement: "MUST respond to all queries in under 1ms"
angle: TECHNICAL_FEASIBILITY
assessment: |
  Network round-trip alone exceeds 1ms for non-local requests.
  Database queries average 5-10ms. Target is infeasible for
  any query involving network or disk I/O.
finding:
  category: SPEC_DEFECT
  subcategory: PERF_IMPOSSIBLE
  severity: BLOCKER
  remediation: "Revise to 'MUST respond in under 100ms for 95th percentile'"
```

---

## CUSTOMER_VALUE

**Focus:** Does the PRD solve real customer problems with measurable value?

### Signals to Look For

- Weak or missing customer definition
- Problems that don't map to customer pain points
- Goals disconnected from stated problems
- Success metrics that don't measure customer value
- Solutions searching for problems

### Finding Subcategories

| Subcategory | Description | Severity |
|-------------|-------------|----------|
| WEAK_CUSTOMER | Customer segment is too vague or generic | MAJOR |
| PROBLEM_UNTESTABLE | Problem statement cannot be validated | MAJOR |
| GOAL_DISCONNECTED | Goals don't address stated problem | BLOCKER |

### Evaluation Questions

1. Is the customer segment specific enough to identify real users?
2. Does the problem statement describe observable pain points?
3. Can we validate that the stated problem actually exists?
4. Do goals directly address the problem, or do they assume a solution?
5. Would solving these requirements actually improve customer outcomes?
6. **Abductive Check:** Is the proposed solution the *best explanation* for how to solve the problem? Does evidence support this mechanism over a simpler correlation?

### Example Evaluation

```yaml
customer: "Developers"
problem: "Developers need better tools"
angle: CUSTOMER_VALUE
assessment: |
  Customer segment is too broad - "developers" includes millions of
  people with wildly different needs. Problem statement is untestable
  - "better" is subjective and "tools" is undefined.
findings:
  - category: SPEC_DEFECT
    subcategory: WEAK_CUSTOMER
    severity: MAJOR
    remediation: "Narrow to 'Backend engineers working on microservices in teams of 5-20'"
  - category: SPEC_DEFECT
    subcategory: PROBLEM_UNTESTABLE
    severity: MAJOR
    remediation: "Specify observable pain: 'spend >30% of time on deployment debugging'"
```

---

## IMPLEMENTATION_RISK

**Focus:** What could go wrong during implementation, and are risks mitigated?

### Signals to Look For

- Unacknowledged technical risks
- Missing fallback strategies for critical paths
- Implicit dependencies on external systems
- Single points of failure
- Assumptions stated as facts

### Finding Subcategories

| Subcategory | Description | Severity |
|-------------|-------------|----------|
| UNMITIGATED_RISK | Known risk without documented mitigation | MAJOR |
| MISSING_FALLBACK | Critical path without degradation strategy | MAJOR |
| IMPLICIT_DEPENDENCY | Undeclared dependency on external system | MAJOR |

### Evaluation Questions

1. For each requirement, what could prevent successful implementation?
2. Are external dependencies explicitly called out with fallback strategies?
3. If a component fails, does the PRD specify graceful degradation?
4. Are there assumptions that could prove false?
5. What happens if estimated effort is significantly wrong?

### Example Evaluation

```yaml
requirement: "MUST integrate with external payment provider API"
angle: IMPLEMENTATION_RISK
assessment: |
  No fallback specified if payment provider API is unavailable.
  No timeout or retry strategy documented. Provider dependency
  is implicit - not listed in dependencies section.
findings:
  - category: SPEC_DEFECT
    subcategory: IMPLICIT_DEPENDENCY
    severity: MAJOR
    remediation: "Add explicit dependency on payment provider with SLA requirements"
  - category: SPEC_DEFECT
    subcategory: MISSING_FALLBACK
    severity: MAJOR
    remediation: "Document queuing strategy for when payment API is unavailable"
```

---

## REUSE_POTENTIAL

**Focus:** Does the PRD leverage existing capabilities or create unnecessary duplication?

### Signals to Look For

- Requirements that duplicate existing functionality
- Missed opportunities to extend existing abstractions
- Net-new implementations where composition would suffice
- Ignored extension points in current architecture
- Similar patterns solved differently elsewhere

### Finding Subcategories

| Subcategory | Description | Severity |
|-------------|-------------|----------|
| COUSIN_ABSTRACTION | Requirement duplicates existing abstraction | MAJOR |
| IGNORED_EXTENSION_POINT | Existing extension point not leveraged | MINOR |
| UNGROUNDED_SOLUTION | Solution Overview does not map to CCP | MAJOR |

### Evaluation Questions

1. Does any requirement reimplement functionality that exists elsewhere?
2. Are there existing abstractions that could be extended rather than replaced?
3. Does the solution use existing extension points in the architecture?
4. What is the net-new code ratio vs. reuse ratio?
5. Are similar problems solved consistently with existing patterns?
6. **CCP Mapping:** Can the Solution Overview be deterministically mapped to the `component_atlas.yaml`?

### Example Evaluation

```yaml
requirement: "MUST implement retry logic with exponential backoff"
angle: REUSE_POTENTIAL
assessment: |
  Codebase already has `RetryPolicy` abstraction in `core/retry.rs`
  with configurable backoff strategies. Requirement appears to
  specify reimplementation rather than reuse.
finding:
  category: TRACEABILITY_DEFECT
  subcategory: COUSIN_ABSTRACTION
  severity: MAJOR
  remediation: "Reframe as 'MUST use existing RetryPolicy with exponential config'"
```

---

## VERIFIABILITY

**Focus:** Can requirements be objectively tested with reproducible evidence?

### Signals to Look For

- Vague acceptance criteria using subjective terms
- Criteria that can't be automated
- Evidence that doesn't falsify the criterion
- Missing coverage for edge cases
- Untestable "ilities" (usability, maintainability, etc.)

### Finding Subcategories

| Subcategory | Description | Severity |
|-------------|-------------|----------|
| CRITERION_VAGUE | Acceptance criterion uses subjective terms | MAJOR |
| EVIDENCE_WEAK | Evidence cannot falsify the requirement | MAJOR |
| COVERAGE_GAP | Significant scenarios lack test coverage | MAJOR |

### Evaluation Questions

1. For each acceptance criterion, can a pass/fail test be written?
2. Does the evidence actually demonstrate the requirement is met?
3. Could the evidence pass while the requirement is not truly met (gaming)?
4. Are edge cases and error conditions covered?
5. Can the verification be automated, or does it require manual judgment?

### Verifiability Scoring

| Score | Definition |
|-------|------------|
| VERIFIABLE | Criterion is measurable, bounded, and automatable |
| CONDITIONALLY_VERIFIABLE | Verifiable with specified preconditions or manual steps |
| NOT_VERIFIABLE | Criterion cannot be objectively tested |

### Example Evaluation

```yaml
requirement: "System MUST be user-friendly"
criterion: "Users should find the system easy to use"
angle: VERIFIABILITY
assessment: |
  "User-friendly" and "easy to use" are subjective terms that
  cannot be objectively measured. No specific metric or threshold
  defined. Evidence would require opinion surveys, not tests.
finding:
  category: EVIDENCE_DEFECT
  subcategory: CRITERION_VAGUE
  severity: MAJOR
  remediation: |
    Replace with measurable criterion: "New users MUST complete
    onboarding flow in under 5 minutes with <2 errors"
```

---

## OPERATIONAL_READINESS

**Focus:** Can the system be deployed, monitored, and rolled back safely?

### Signals to Look For

- Missing rollback procedures
- No observability requirements (metrics, logs, traces)
- Unclear deployment strategy
- Missing runbook requirements
- No incident response considerations

### Finding Subcategories

| Subcategory | Description | Severity |
|-------------|-------------|----------|
| MISSING_ROLLBACK | No rollback strategy for deployment | MAJOR |
| NO_OBSERVABILITY | Missing metrics, logging, or tracing requirements | MAJOR |

### Evaluation Questions

1. Can deployments be rolled back if issues are detected?
2. Are there metrics to detect degradation before users report it?
3. Do logs provide enough context to debug production issues?
4. Is there a deployment strategy (canary, blue-green, etc.)?
5. Are SLOs defined with alerting thresholds?

### Example Evaluation

```yaml
requirement: "MUST deploy new pricing engine to production"
angle: OPERATIONAL_READINESS
assessment: |
  No rollback procedure specified. Pricing changes could have
  significant business impact if incorrect. No mention of canary
  deployment or gradual rollout strategy.
findings:
  - category: SPEC_DEFECT
    subcategory: MISSING_ROLLBACK
    severity: MAJOR
    remediation: "Add requirement for instant rollback capability with <1min MTTR"
  - category: EVIDENCE_DEFECT
    subcategory: NO_OBSERVABILITY
    severity: MAJOR
    remediation: "Add metrics for price calculation latency and error rate"
```

---

## SECURITY_POSTURE

**Focus:** Does the PRD maintain default-deny security principles?

### Signals to Look For

- Missing data classification for stored/transmitted data
- Undefined network boundaries
- Implicit trust assumptions
- Missing authentication/authorization requirements
- Unspecified encryption requirements

### Finding Subcategories

| Subcategory | Description | Severity |
|-------------|-------------|----------|
| MISSING_DATA_CLASS | Data handled without classification | MAJOR |
| UNDEFINED_NETWORK | Network boundaries not specified | MAJOR |

### Evaluation Questions

1. Is all data classified (PII, confidential, public)?
2. Are network boundaries explicit (what talks to what)?
3. Does the design assume trust that isn't established?
4. Are authentication and authorization requirements explicit?
5. Is encryption specified for data at rest and in transit?

### Example Evaluation

```yaml
requirement: "MUST store user preferences"
angle: SECURITY_POSTURE
assessment: |
  No data classification for user preferences. Could include
  PII (name, email), sensitive data (location history), or
  innocuous settings. Storage and access controls depend on
  classification.
finding:
  category: EVIDENCE_DEFECT
  subcategory: MISSING_DATA_CLASS
  severity: MAJOR
  remediation: "Classify preference types and specify encryption/access requirements"
```

---

## COHERENCE_CONSISTENCY

**Focus:** Are requirements internally consistent and logically coherent?

### Signals to Look For

- Contradictions between requirements
- Conflicting priorities without resolution
- Scope creep beyond problem statement
- Requirements that contradict constraints
- Circular dependencies between requirements

### Finding Subcategories

Uses existing SPEC_DEFECT subcategories:

| Subcategory | Description | Severity |
|-------------|-------------|----------|
| INCONSISTENCY | Requirement contradicts another | BLOCKER |
| AMBIGUITY | Requirement can be interpreted multiple ways | MAJOR |
| INCOMPLETENESS | Requirement missing necessary detail | MAJOR |

### Evaluation Questions

1. Do any two requirements contradict each other?
2. Are there conflicting priorities that need resolution?
3. Do all requirements fit within the stated scope?
4. Are there requirements that violate stated constraints?
5. Is the dependency graph acyclic?

### Example Evaluation

```yaml
requirements:
  - "REQ-0001: MUST use synchronous processing for real-time response"
  - "REQ-0005: MUST use async queue for all operations for reliability"
angle: COHERENCE_CONSISTENCY
assessment: |
  REQ-0001 and REQ-0005 directly contradict. Synchronous processing
  precludes async queuing. Cannot satisfy both simultaneously.
finding:
  category: SPEC_DEFECT
  subcategory: INCONSISTENCY
  severity: BLOCKER
  remediation: "Clarify which operations are sync vs async, or resolve conflict"
```

---

## TRADEOFF_ANALYSIS

**Focus:** What was optimized, what was sacrificed, and is the choice justified?

### Signals to Look For

- "Naive Optimization" (claiming to be best at everything: fast, cheap, and safe).
- Hidden costs or side effects ignored in the design.
- Mismatch between the optimized variable and the business goal.
- Lack of "Why not X?" reasoning.

### Finding Subcategories

| Subcategory | Description | Severity |
|-------------|-------------|----------|
| NAIVE_OPTIMIZATION | Claims "best" without tradeoff analysis | MAJOR |
| HIDDEN_COST | Tradeoff downsides are not acknowledged | MAJOR |

### Evaluation Questions

1. What was optimized (Speed, Consistency, Availability, Cost)?
2. What was sacrificed to achieve that optimization? (If nothing, look harder).
3. Is the sacrifice acceptable given the business constraints?
4. **Pareto Check:** Are we on the efficient frontier, or just picking a bad point?
5. Why was the alternative rejected?
6. **The Zero-Sum Test:** Identify the specific metric degraded to achieve a benefit.
7. **The "Why Not" Inversion:** Require a structural reason for rejecting the obvious alternative.

### Example Evaluation

```yaml
requirement: "MUST provide strong consistency across all regions with <10ms latency"
angle: TRADEOFF_ANALYSIS
assessment: |
  Violates CAP theorem/PACELC. Strong consistency + Low Latency + Partition Tolerance
  is physically impossible across global regions.
  Design claims to optimize everything (Naive Optimization).
finding:
  category: SPEC_DEFECT
  subcategory: NAIVE_OPTIMIZATION
  severity: MAJOR
  remediation: "Choose between Strong Consistency (high latency) or Eventual Consistency (low latency)"
```

---

## SYSTEM_DYNAMICS

**Focus:** Feedback loops, delays, and second-order effects on the ecosystem.

### Signals to Look For

- Reinforcing loops without dampeners (e.g., retries causing more load).
- Delays between action and system response (oscillation risk).
- Resource exhaustion risks in shared systems (tragedy of the commons).
- Unintended consequences on upstream/downstream components.

### Finding Subcategories

| Subcategory | Description | Severity |
|-------------|-------------|----------|
| UNSTABLE_FEEDBACK | Design creates reinforcing feedback loops | BLOCKER |
| SECOND_ORDER_HARM | Negative consequences on wider system | MAJOR |

### Evaluation Questions

1. Does the feature create a reinforcing loop? (e.g., auto-scaling triggered by load -> more connections -> more load).
2. Are there time delays that could cause oscillation?
3. How does this affect the shared resource budget of the Holarchy?
4. What happens if every agent does this simultaneously?
5. **Loop Simulation:** Simulate state at t+1, t+10, t+100.
6. **The "Thundering Herd" Check:** Analyze peak resource demand under simultaneous trigger conditions.

### Example Evaluation

```yaml
requirement: "Agents MUST retry failed API calls immediately"
angle: SYSTEM_DYNAMICS
assessment: |
  Immediate retry on failure creates a reinforcing loop during outages.
  If the API is down due to load, retries will increase load, prolonging the outage.
  This is a classic Thundering Herd problem.
finding:
  category: SPEC_DEFECT
  subcategory: UNSTABLE_FEEDBACK
  severity: BLOCKER
  remediation: "Implement exponential backoff with jitter"
```

---

## Angle Coverage Matrix

After executing all angles, produce coverage matrix:

```yaml
angle_coverage:
  prd_id: PRD-XXXX
  review_timestamp: "2026-01-25T10:00:00Z"
  angles:
    - angle_id: TECHNICAL_FEASIBILITY
      executed: true
      finding_count: 2
      finding_ids: [FND-PRD-XXXX-001, FND-PRD-XXXX-002]
    - angle_id: CUSTOMER_VALUE
      executed: true
      finding_count: 0
      finding_ids: []
    # ... remaining angles
  summary:
    total_angles: 10
    executed_angles: 10
    required_executed: 8
    findings_by_angle:
      TECHNICAL_FEASIBILITY: 2
      CUSTOMER_VALUE: 0
      IMPLEMENTATION_RISK: 1
      REUSE_POTENTIAL: 1
      VERIFIABILITY: 3
      OPERATIONAL_READINESS: 0
      SECURITY_POSTURE: 1
      COHERENCE_CONSISTENCY: 0
```

---

## Merge Strategy

When multiple angles produce findings for the same location:

1. **Deduplicate:** Same category + subcategory + location = single finding
2. **Highest Severity Wins:** If angles assign different severities, use highest
3. **Combine Remediation:** Merge remediation suggestions from all angles
4. **Preserve Angle Attribution:** Finding includes `angle_ids` list of all contributing angles

```yaml
finding:
  finding_id: FND-PRD-0005-007
  angle_ids: [VERIFIABILITY, OPERATIONAL_READINESS]
  category: EVIDENCE_DEFECT
  subcategory: CRITERION_VAGUE
  severity: MAJOR  # Highest from contributing angles
  location:
    file: documents/prds/PRD-0005/requirements/REQ-0003.yaml
    yaml_path: requirement.acceptance_criteria[0]
  description: "Criterion 'system performs well under load' is subjective"
  remediation: |
    From VERIFIABILITY: Add measurable threshold (e.g., p99 < 200ms at 1000 RPS)
    From OPERATIONAL_READINESS: Include monitoring metric for alerting
```

---

## References

- [REVIEW_RUBRIC.md](REVIEW_RUBRIC.md) - Gate definitions including angle dispatch
- [FINDING_CATEGORIES.md](FINDING_CATEGORIES.md) - Subcategory definitions
- [FEEDBACK_LOOPS.md](FEEDBACK_LOOPS.md) - How angle findings feed back to improve PRD templates
