# PRD Review Rubric

Formal gate definitions with evidence contracts for PRD review.

## Gate Overview

Gates are executed in order. Deterministic gates run before LLM-assisted gates to catch structural issues early.

**Gate Type Definitions:**
- **TRUSTED**: Tool-based validation (YAML parsers, lint tools) - deterministic and machine-verifiable
- **DETERMINISTIC**: Algorithmic checks (graph traversal, counting) - no LLM judgment required
- **LLM-ASSISTED**: Semantic analysis requiring LLM judgment - results are UNTRUSTED until human confirms

| Gate ID | Type | Purpose |
|---------|------|---------|
| GATE-PRD-SCHEMA | TRUSTED | YAML parsing and schema conformance |
| GATE-PRD-LINT | TRUSTED | Lint rule compliance |
| GATE-PRD-TRACEABILITY | DETERMINISTIC | Requirement-evidence chain integrity |
| GATE-PRD-CCP-MAPPING | DETERMINISTIC | Cousin Prevention Gate (CCP mapping) |
| GATE-PRD-QUALITY-COVERAGE | DETERMINISTIC | Quality dimension coverage |
| GATE-PRD-EVIDENCE-STANDARDS | DETERMINISTIC | Evidence artifact completeness |
| GATE-PRD-CONTENT | LLM-ASSISTED | Semantic quality assessment |

---

## GATE-PRD-SCHEMA

**Type:** TRUSTED (deterministic, no LLM)

### Purpose

Verify all PRD files parse as valid YAML and conform to their schemas.

### Evidence Contract

| Field | Value |
|-------|-------|
| Inputs | All YAML files in `documents/prds/{PRD_ID}/` |
| Outputs | Parse results, schema validation results |
| Required | All files parse without error, all files validate against schema |

### Rubric

| Check | Pass Criteria | Tool |
|-------|---------------|------|
| YAML parse | All files parse without syntax errors | Read each file, check for YAML parse errors |
| Single root key | Each file has exactly one root key | Read and verify structure |
| Schema validation | Files match their corresponding schemas | Compare against `standards/schemas/*.yaml` |
| No tabs | Files contain no tab characters | Grep for tabs |

### Verification Steps

```bash
# Check all YAML files parse
for f in documents/prds/{PRD_ID}/*.yaml; do
  python3 -c "import yaml; yaml.safe_load(open('$f'))" || echo "FAILED: $f"
done

# Check requirements and evidence subdirectories
for f in documents/prds/{PRD_ID}/requirements/*.yaml; do
  python3 -c "import yaml; yaml.safe_load(open('$f'))" || echo "FAILED: $f"
done

for f in documents/prds/{PRD_ID}/evidence_artifacts/*.yaml; do
  python3 -c "import yaml; yaml.safe_load(open('$f'))" || echo "FAILED: $f"
done
```

### Stop Condition

FAILED if any file fails to parse or violates schema.

---

## GATE-PRD-LINT

**Type:** TRUSTED (deterministic, no LLM)

### Purpose

Verify PRD complies with all applicable lint rules from `LINT_SPEC.yaml`.

### Evidence Contract

| Field | Value |
|-------|-------|
| Inputs | All PRD files, `standards/lint/LINT_SPEC.yaml` |
| Outputs | Lint violations list |
| Required | No ERROR-severity violations |

### Rubric

**Global Rules:**

| Rule ID | Scope | Check | Pass Criteria |
|---------|-------|-------|---------------|
| LINT-0001 | ALL_YAML | YAML validity | No tabs, valid YAML |
| LINT-0002 | ALL_YAML | Single root key | Each file has exactly one root key |
| LINT-0003 | ALL_DOCS | ID format | IDs match canonical patterns |
| LINT-0004 | ALL_DOCS | Cross-references | All references resolve (path + root_key + subpath) |
| LINT-0005 | INSTANCE_DOCS | No placeholders | No TBD/TODO/FIXME/??? in required fields |
| LINT-0006 | ALL_MARKDOWN | No markdown tables | No pipe table rows in YAML |
| LINT-0007 | PRD | Requirement completeness | Each REQ has >=1 acceptance criterion and >=1 evidence_id |
| LINT-0008 | EVIDENCE_ARTIFACTS | Evidence completeness | Each EVID has >=1 command (with network_access) and >=1 capture path |
| LINT-0009 | QUALITY_FRAMEWORK | Quality coverage | All 18 dimensions; DOES_NOT_APPLY requires exception |

**Determinism Rules:**

| Rule ID | Check | Pass Criteria |
|---------|-------|---------------|
| LINT-0101 | List ordering | Lists named *_ids MUST be lexicographically sorted |
| LINT-0102 | Object list ordering | Object lists with primary key MUST be sorted by that key |
| LINT-0103 | Duplicate IDs | No duplicate IDs in same logical namespace |

**Waiver Rules:**

| Rule ID | Check | Pass Criteria |
|---------|-------|---------------|
| LINT-0201 | Waiver validity | Waivers require authority signoffs, rationale, expiration_date |
| LINT-0202 | Waiver reference | WAIVED status MUST reference approved waiver_id with matching scope |
| LINT-0203 | Waiver expiration | Expired waivers are forbidden |

### Verification Steps

```bash
# Check for placeholders in required fields
grep -rn "TBD\|TODO\|FIXME\|???" documents/prds/{PRD_ID}/*.yaml

# Check for tabs
grep -rn $'\t' documents/prds/{PRD_ID}/*.yaml

# Check ID format (PRD-XXXX, REQ-XXXX, EVID-XXXX)
grep -rn "id:" documents/prds/{PRD_ID}/ | grep -v "PRD-[0-9]\{4\}\|REQ-[0-9]\{4\}\|EVID-[0-9]\{4\}"
```

### Stop Condition

FAILED if any ERROR-severity lint violation detected.

---

## GATE-PRD-TRACEABILITY

**Type:** DETERMINISTIC (algorithmic, no LLM)

### Purpose

Verify complete traceability chain: Customer → Problem → Goal → Requirement → Evidence.

### Evidence Contract

| Field | Value |
|-------|-------|
| Inputs | All PRD files including requirements and evidence |
| Outputs | Traceability matrix, orphan list |
| Required | No orphan requirements, no orphan evidence |

### Rubric

| Check | Pass Criteria |
|-------|---------------|
| Customer defined | `01_customer.yaml` has non-empty customer segment |
| Problem stated | `02_problem.yaml` has non-empty problem statement |
| Goals linked | `03_goals_scope.yaml` references problem |
| Requirements linked | Each REQ references at least one goal or derives from problem |
| Evidence linked | Each REQ has at least one EVID; each EVID linked to at least one REQ |
| No orphan REQs | All requirements traceable to customer need |
| No orphan EVIDs | All evidence artifacts referenced by requirements |
| No broken refs | All evidence_ids in requirements resolve to existing artifacts |

### Verification Steps

```bash
# Step 1: Extract all defined evidence IDs
DEFINED_EVIDS=$(grep -h "id:" documents/prds/{PRD_ID}/evidence_artifacts/*.yaml | grep -oE "EVID-[0-9]{4}" | sort -u)

# Step 2: Extract all referenced evidence IDs from requirements
REFERENCED_EVIDS=$(grep -rh "evidence_ids:" -A 20 documents/prds/{PRD_ID}/requirements/*.yaml | grep -oE "EVID-[0-9]{4}" | sort -u)

# Step 3: Find orphan evidence (defined but not referenced)
ORPHAN_EVIDS=$(comm -23 <(echo "$DEFINED_EVIDS") <(echo "$REFERENCED_EVIDS"))

# Step 4: Find broken references (referenced but not defined)
BROKEN_REFS=$(comm -13 <(echo "$DEFINED_EVIDS") <(echo "$REFERENCED_EVIDS"))

# Step 5: Report
[ -n "$ORPHAN_EVIDS" ] && echo "ORPHAN EVIDENCE: $ORPHAN_EVIDS"
[ -n "$BROKEN_REFS" ] && echo "BROKEN REFERENCES: $BROKEN_REFS"
```

### Stop Condition

FAILED if:
- Any evidence artifact is not referenced by any requirement (orphan evidence)
- Any requirement references an evidence_id that does not exist (broken reference)

---

## GATE-PRD-CCP-MAPPING

**Type:** DETERMINISTIC (algorithmic, no LLM)

### Purpose

Prevent cousin abstractions by enforcing CCP (Codebase Component Protocol) mapping before content review.

### Evidence Contract

| Field | Value |
|-------|-------|
| Inputs | PRD requirements (`requirements/REQ-*.yaml`), `documents/architecture/component_atlas.yaml` |
| Outputs | CCP mapping report, cousin justifications |
| Required | All requirements mapped to CCP OR justified with evidence |

### Rubric

| Check | Pass Criteria |
|-------|---------------|
| CCP mapping | Every requirement MUST map to an existing CCP component |
| Cousin justification | Unmapped requirements MUST have a `cousin_justification.yaml` artifact |
| Evidence provided | `cousin_justification.yaml` MUST reference an `evidence_artifact` (EVID-XXXX) |
| Gap demonstrated | Evidence artifact MUST demonstrate the claimed capability gap |

### Cousin Justification Schema

```yaml
requirement_id: REQ-XXXX
existing_component: "path/to/component"
capability_gap: "Specific capability that is missing"
evidence_artifact: "EVID-XXXX"  # Test/proof showing the gap exists
decision: "EXTEND" | "CREATE_NEW"
decision_rationale: "Why extension is insufficient"
```

### Failure Mode

If `evidence_artifact` is missing or does not demonstrate the claimed gap, emit:
- `category: TRACEABILITY_DEFECT`
- `subcategory: COUSIN_ABSTRACTION`
- `severity: BLOCKER` (not MAJOR)

**Holonic Alignment:** This gate enforces Principia Holonica Axiom IV (Economics of Attention) — "Waste is the ultimate sin."

---

## GATE-PRD-QUALITY-COVERAGE

**Type:** DETERMINISTIC (algorithmic, no LLM)

### Purpose

Verify all 18 quality dimensions are addressed in the quality framework.

### Evidence Contract

| Field | Value |
|-------|-------|
| Inputs | `10_quality_framework.yaml` |
| Outputs | Coverage matrix |
| Required | All 18 dimensions present with valid applicability |

### Rubric

| Check | Pass Criteria |
|-------|---------------|
| All dimensions present | 18 dimension entries exist with `dimension_id` |
| Valid applicability | Each dimension has `applicability`: APPLIES or DOES_NOT_APPLY |
| Valid disposition | APPLIES dimensions have `disposition`: EXPLICIT_REQUIREMENTS, DELEGATED_WITH_GUARDRAILS, or NOT_APPLICABLE |
| Exception documented | DOES_NOT_APPLY requires `exception.requested: true` AND `exception.rationale` non-empty |
| Signoffs specified | Exceptions require `exception.required_signoffs` list with at least one authority |
| Coverage complete | EXPLICIT_REQUIREMENTS has non-empty `coverage.requirement_ids`; DELEGATED_WITH_GUARDRAILS has non-empty `delegation.guardrails` |

### Required Dimensions (18 total, alphabetically sorted)

```yaml
dimensions:
  - ACCESSIBILITY
  - AGENT_FRIENDLY_UX
  - BACKWARD_COMPATIBILITY
  - COST_EFFICIENCY
  - DATA_PRIVACY
  - DEFAULT_DENY_SECURITY
  - DETERMINISM
  - DOCUMENTATION
  - ERROR_HANDLING
  - INTEROPERABILITY
  - OBSERVABILITY
  - OPERATIONAL_READINESS
  - PERFORMANCE
  - RECOVERY_ROLLBACK
  - RELIABILITY
  - RESILIENCE
  - SCALABILITY
  - TESTABILITY
```

### Verification Steps

```bash
# Step 1: Count dimensions (must be exactly 18)
COUNT=$(grep -c "dimension_id:" documents/prds/{PRD_ID}/10_quality_framework.yaml)
[ "$COUNT" -eq 18 ] || echo "FAIL: Expected 18 dimensions, found $COUNT"

# Step 2: Check for DOES_NOT_APPLY without proper exception
grep -B5 -A10 "applicability: DOES_NOT_APPLY" documents/prds/{PRD_ID}/10_quality_framework.yaml | \
  grep -A8 "exception:" | grep "requested: false" && echo "FAIL: DOES_NOT_APPLY without exception.requested=true"

# Step 3: Check DELEGATED_WITH_GUARDRAILS has guardrails
grep -B2 -A15 "disposition: DELEGATED_WITH_GUARDRAILS" documents/prds/{PRD_ID}/10_quality_framework.yaml | \
  grep -A5 "guardrails:" | grep "\[\]" && echo "FAIL: DELEGATED_WITH_GUARDRAILS with empty guardrails"

# Step 4: Check EXPLICIT_REQUIREMENTS has requirement_ids
grep -B2 -A15 "disposition: EXPLICIT_REQUIREMENTS" documents/prds/{PRD_ID}/10_quality_framework.yaml | \
  grep -A3 "requirement_ids:" | grep "\[\]" && echo "FAIL: EXPLICIT_REQUIREMENTS with empty requirement_ids"
```

### Stop Condition

FAILED if:
- Fewer than 18 dimensions
- DOES_NOT_APPLY without `exception.requested: true` and `exception.rationale`
- DELEGATED_WITH_GUARDRAILS with empty `delegation.guardrails`
- EXPLICIT_REQUIREMENTS with empty `coverage.requirement_ids`

---

## GATE-PRD-EVIDENCE-STANDARDS

**Type:** DETERMINISTIC (algorithmic, no LLM)

### Purpose

Verify all evidence artifacts meet structural requirements.

### Evidence Contract

| Field | Value |
|-------|-------|
| Inputs | All files in `evidence_artifacts/` |
| Outputs | Artifact validation results |
| Required | All artifacts have commands, network_access, and capture_paths |

### Rubric

| Check | Pass Criteria |
|-------|---------------|
| Commands present | Each artifact has >= 1 verification command with id, shell, command |
| network_access declared | Each command declares network_access: DISALLOWED/ALLOW_LISTED_ONLY/ALLOWED |
| Capture paths defined | Each artifact has capture.paths with >= 1 path |
| Category valid | Category is from 27 approved categories |
| Data classification | Each artifact has data.classification and data.redaction |

**Valid categories (27):** See `standards/enums/03_evidence_categories.yaml`

### Verification Steps

```bash
# Check each evidence artifact for required fields per schema
for f in documents/prds/{PRD_ID}/evidence_artifacts/*.yaml; do
  grep -q "^  id:" "$f" || echo "MISSING id: $f"
  grep -q "^  category:" "$f" || echo "MISSING category: $f"
  grep -q "^  title:" "$f" || echo "MISSING title: $f"
  grep -q "^  capture:" "$f" || echo "MISSING capture: $f"
  grep -q "^    paths:" "$f" || echo "MISSING capture.paths: $f"
  grep -q "^  verification:" "$f" || echo "MISSING verification: $f"
  grep -q "^    commands:" "$f" || echo "MISSING verification.commands: $f"
  grep -q "network_access:" "$f" || echo "MISSING network_access: $f"
  grep -q "^  data:" "$f" || echo "MISSING data: $f"
  grep -q "classification:" "$f" || echo "MISSING data.classification: $f"
done
```

### Stop Condition

FAILED if any evidence artifact missing required fields (id, category, title, capture.paths, verification.commands with network_access, data.classification).

---

## GATE-PRD-CONTENT

**Type:** LLM-ASSISTED (semantic analysis, UNTRUSTED)

### Purpose

Assess semantic quality of requirements and evidence sufficiency through structured multi-angle analysis.

### Evidence Contract

| Field | Value |
|-------|-------|
| Inputs | All PRD files |
| Outputs | Content quality assessment, angle coverage matrix |
| Required | No BLOCKER-severity content issues, all required angles executed |

### Angle Dispatch Protocol

Execute analysis through 8 structured angles. See [ANGLE_PROMPTS.md](ANGLE_PROMPTS.md) for detailed prompt templates.

| Angle ID | Focus | Required | Finding Categories |
|----------|-------|----------|-------------------|
| TECHNICAL_FEASIBILITY | Can requirements be implemented? | Yes | SPEC_DEFECT |
| CUSTOMER_VALUE | Does PRD solve real problems? | Yes | SPEC_DEFECT |
| IMPLEMENTATION_RISK | What could go wrong? | Yes | SPEC_DEFECT |
| REUSE_POTENTIAL | Extend existing vs create net-new? | Yes | TRACEABILITY_DEFECT |
| VERIFIABILITY | Are requirements testable? | Yes | SPEC_DEFECT, EVIDENCE_DEFECT |
| OPERATIONAL_READINESS | Can this be deployed safely? | No | SPEC_DEFECT, EVIDENCE_DEFECT |
| SECURITY_POSTURE | Default-deny maintained? | No | EVIDENCE_DEFECT |
| COHERENCE_CONSISTENCY | Internally consistent? | Yes | SPEC_DEFECT |
| TRADEOFF_ANALYSIS | Optimizations justified? | Yes | SPEC_DEFECT |
| SYSTEM_DYNAMICS | Feedback loops stable? | Yes | SPEC_DEFECT |

**Angle Execution Requirements:**

1. **All required angles MUST be executed** (8 required angles minimum)
2. **Optional angles SHOULD be executed** for production PRDs
3. **Each angle produces findings** with `angle_id` attribution
4. **Angle coverage matrix** captured in output bundle

### Rubric

| Check | Pass Criteria |
|-------|---------------|
| Requirement clarity | Statements are unambiguous and actionable |
| Testable criteria | Each criterion can be objectively verified |
| Evidence sufficiency | Evidence would convince skeptical reviewer |
| Completeness | No obvious gaps in requirement coverage |
| Consistency | No contradictions between requirements |
| Angle coverage | All required angles executed with findings documented |

### Assessment Questions

For each requirement, evaluate through applicable angles:

1. **Clarity** (COHERENCE_CONSISTENCY): Can an implementer understand exactly what to build?
2. **Testability** (VERIFIABILITY): Can a tester write a pass/fail test from the acceptance criteria?
3. **Evidence** (VERIFIABILITY): Does the linked evidence actually demonstrate the requirement is met?
4. **Scope** (COHERENCE_CONSISTENCY): Is the requirement appropriately scoped (not too broad, not too narrow)?
5. **Feasibility** (TECHNICAL_FEASIBILITY): Can this be implemented with current technology?
6. **Risk** (IMPLEMENTATION_RISK): What could prevent successful implementation?
7. **Reuse** (REUSE_POTENTIAL): Does this duplicate existing abstractions?
8. **Tradeoff** (TRADEOFF_ANALYSIS): Is the optimization justified by a sacrifice?
9. **Dynamics** (SYSTEM_DYNAMICS): Does this create unstable feedback loops?

For the PRD overall, evaluate:

1. **Coverage**: Are there obvious requirements missing for the stated problem?
2. **Consistency**: Do requirements contradict each other?
3. **Feasibility**: Are requirements technically achievable?
4. **Customer Value**: Does the PRD solve a real, validated problem?

### Severity Assignment for Content Issues

| Issue Type | Severity | Example | Source Angle |
|------------|----------|---------|--------------|
| Contradiction between requirements | BLOCKER | REQ-0001 says "MUST use HTTP" and REQ-0002 says "MUST use gRPC" | COHERENCE_CONSISTENCY |
| Requirement impossible to implement | BLOCKER | "MUST complete in 0ms" | TECHNICAL_FEASIBILITY |
| Completely untestable requirement | BLOCKER | "System MUST be intuitive" with no criteria | VERIFIABILITY |
| Goals disconnected from problem | BLOCKER | Goals don't address stated customer pain | CUSTOMER_VALUE |
| Ambiguous but interpretable requirement | MAJOR | "MUST respond quickly" (could add "< 100ms") | COHERENCE_CONSISTENCY |
| Missing obvious requirement | MAJOR | No error handling requirement for a critical path | IMPLEMENTATION_RISK |
| Evidence doesn't fully demonstrate requirement | MAJOR | Test only covers happy path | VERIFIABILITY |
| Duplicates existing abstraction | MAJOR | Reimplements existing RetryPolicy | REUSE_POTENTIAL |
| Missing rollback strategy | MAJOR | No rollback for critical deployment | OPERATIONAL_READINESS |
| Minor clarity improvement | MINOR | Could be reworded for clarity | COHERENCE_CONSISTENCY |
| Ignored extension point | MINOR | Could leverage existing middleware | REUSE_POTENTIAL |
| Naive Optimization | MAJOR | Claims "best" without tradeoff analysis | TRADEOFF_ANALYSIS |
| Unstable Feedback Loop | BLOCKER | Design creates reinforcing loop (e.g., infinite retries) | SYSTEM_DYNAMICS |
| Style or formatting suggestion | INFO | Passive voice could be active | - |

### Angle Coverage Matrix

Each GATE-PRD-CONTENT execution produces an angle coverage matrix:

```yaml
angle_coverage:
  prd_id: PRD-XXXX
  review_timestamp: "2026-01-25T10:00:00Z"
  angles:
    - angle_id: TECHNICAL_FEASIBILITY
      required: true
      executed: true
      finding_count: 2
      blocker_count: 1
      finding_ids: [FND-PRD-XXXX-001, FND-PRD-XXXX-002]
    - angle_id: CUSTOMER_VALUE
      required: true
      executed: true
      finding_count: 0
      blocker_count: 0
      finding_ids: []
    # ... remaining angles
  summary:
    total_angles: 10
    required_angles: 8
    executed_angles: 10
    required_executed: 8
    total_findings: 12
    blocker_findings: 2
```

### Merge Strategy for Angle Findings

When multiple angles identify the same issue:

1. **Deduplicate:** Same category + subcategory + location = single finding
2. **Highest Severity Wins:** Use maximum severity from contributing angles
3. **Combine Remediation:** Merge suggestions from all angles
4. **Preserve Attribution:** Finding includes `angle_ids` list

```yaml
finding:
  finding_id: FND-PRD-0005-007
  angle_ids: [VERIFIABILITY, OPERATIONAL_READINESS]  # Both angles found this
  category: EVIDENCE_DEFECT
  subcategory: CRITERION_VAGUE
  severity: MAJOR
  # ... rest of finding
```

### Confidence Levels

| Level | Description | Action |
|-------|-------------|--------|
| HIGH | Clear pass or fail determination | Record verdict |
| MEDIUM | Minor ambiguity but likely determination | Record verdict with caveat in verdict_reason |
| LOW | Significant uncertainty | Set verdict to NEEDS_ADJUDICATION |

### Stop Condition

- FAILED if any BLOCKER-severity content issue detected
- FAILED if any required angle not executed
- NEEDS_ADJUDICATION if confidence is LOW on any MAJOR issue
- PASSED if no BLOCKER issues, all required angles executed, and HIGH/MEDIUM confidence on all assessments

---

## Output Schemas

### Evidence Bundle (minimal)

```json
{
  "schema_version": "1.0.0",
  "prd_id": "PRD-XXXX",
  "review_timestamp": "2026-01-25T10:00:00Z",
  "gates": [{"gate_id": "GATE-PRD-SCHEMA", "type": "TRUSTED", "status": "PASSED", "findings": [], "evidence": {}}],
  "findings": [],
  "verdict": "PASSED",
  "verdict_reason": "All gates passed"
}
```

### Finding

```json
{
  "finding_id": "FND-PRD-0001-001",
  "gate_id": "GATE-PRD-LINT",
  "category": "FORMAT_DEFECT",
  "subcategory": "PARSE_ERROR",
  "severity": "BLOCKER",
  "location": {"file": "documents/prds/PRD-0001/00_meta.yaml", "line": 15, "yaml_path": "prd_meta.prd.title"},
  "description": "Required field 'title' is empty",
  "remediation": "Add a descriptive title",
  "signature": "abc123..."
}
```

### Severity Levels

| Severity | Impact |
|----------|--------|
| BLOCKER | Gate FAILED, review stops |
| MAJOR | Must remediate before approval |
| MINOR | Should remediate |
| INFO | Optional improvement |

---

## References

- `standards/lint/LINT_SPEC.yaml` - Authoritative lint rules
- `standards/schemas/*.yaml` - Schema definitions
- `standards/enums/03_evidence_categories.yaml` - 27 evidence categories
- `standards/enums/04_quality_dimensions.yaml` - 18 quality dimensions
- `standards/enums/18_network_access.yaml` - network_access enum
- [ANGLE_PROMPTS.md](ANGLE_PROMPTS.md) - Multi-angle analysis prompts for GATE-PRD-CONTENT
- [FINDING_CATEGORIES.md](FINDING_CATEGORIES.md) - Finding taxonomy with angle attributions
- [FEEDBACK_LOOPS.md](FEEDBACK_LOOPS.md) - Recursive improvement through feedback signals
