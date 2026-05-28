# Create PRD Prompt

Detailed guidance for drafting PRDs that pass review gates on first submission.

---

## Step 1: Initialize PRD Directory

```bash
cp -r documents/prds/template documents/prds/{PRD_ID}
ls documents/prds/{PRD_ID}/
```

PRD-ID format: `PRD-XXXX` (4-digit zero-padded). Template contains 19 YAML files across root, `requirements/`, and `evidence_artifacts/` directories.

---

## Step 2: Customer-First Drafting Order

| Phase | Files | Focus |
|-------|-------|-------|
| 1. Foundation | `00_meta`, `01_customer`, `02_problem` | Who and why |
| 2. Direction | `03_goals_scope`, `04_solution_overview` | What and how |
| 3. Specification | `requirements/REQ-*.yaml`, `evidence_artifacts/EVID-*.yaml` | Detailed requirements |
| 4. Quality | `10_quality_framework`, `05_success_metrics`, `06_constraints_invariants` | Quality assurance |
| 5. Traceability | `07_traceability`, `08_risks_questions`, `09_decisions_review`, `11_evidence_standards`, `12_evidence_bundle`, `13_governance_model` | Completeness |

---

## Step 3: Requirement Writing

| Check | Criterion |
|-------|-----------|
| Normative language | MUST, SHALL, MUST NOT, SHALL NOT |
| Single responsibility | One behavior per requirement |
| Testable statement | Can write pass/fail test |
| Evidence linkage | >=1 evidence_id |
| Type | FUNCTIONAL, NON_FUNCTIONAL, CONSTRAINT, or INTEGRATION |

### Falsifiability Standard (Mandatory)

Every acceptance criterion MUST be **machine-verifiable**. This means:

1. **Bound by a Threshold:** Replace subjective terms with numeric bounds.
   - BAD: "System MUST be fast"
   - GOOD: "p99 latency MUST be <200ms under 1000 RPS"

2. **Verifiable by Artifact:** Each criterion MUST reference an evidence artifact type.
   - BAD: "Users should find the system easy to use"
   - GOOD: "New users MUST complete onboarding in <5 minutes (EVID: session_recording_analysis)"

3. **Falsifiable by Command:** The ideal criterion can be tested by a single shell command.
   - Example: `curl -w '%{time_total}' ... | jq '.latency < 0.2'`

**Prohibited Terms (Auto-Fail):**
- "seamless", "intuitive", "user-friendly", "reliable", "robust", "performant", "scalable" (without quantification)
- "reasonable", "appropriate", "sufficient", "adequate" (without bounds)
- "should" (use MUST, SHOULD RFC 2119 style with explicit fallback)

If a criterion uses a prohibited term without quantification, it is an `EVIDENCE_DEFECT (CRITERION_VAGUE)` with `BLOCKER` severity.

**Good:** `"The system MUST return error code 400 when input validation fails."`
**Bad:** `"The system should handle errors appropriately."` (vague, untestable)

**Good criteria:** `"WHEN input is empty THEN response status is 400"`
**Bad criteria:** `"Errors are handled correctly"` (not specific)

---

## Step 4: Evidence Artifact

**Required fields** (all must be present and non-empty):
- `id`: Format EVID-XXXX (4-digit zero-padded)
- `title`: Descriptive name for the evidence
- `category`: One of 27 valid categories (see below)
- `capture.paths`: Array with at least one path where evidence is stored
- `verification.commands`: Array with at least one command object containing:
  - `id`: Command identifier (e.g., CMD-001)
  - `shell`: Shell to use (typically "bash")
  - `command`: The actual command string
  - `network_access`: DISALLOWED, ALLOW_LISTED_ONLY, or ALLOWED
- `data.classification`: Data sensitivity level (e.g., INTERNAL, CONFIDENTIAL)
- `data.redaction`: Object with `required` (boolean) and `guidance` (array)

**Minimal template:**
```yaml
evidence_artifact:
  schema_version: "2026-01-23"
  id: "EVID-XXXX"
  title: "Short descriptive title"
  category: "TEST_RESULTS"
  capture:
    paths: ["evidence/{PRD_ID}/EVID-XXXX_output.txt"]
  verification:
    commands:
      - id: "CMD-001"
        shell: "bash"
        command: "cargo test --test test_name"
        network_access: "DISALLOWED"
  data:
    classification: "INTERNAL"
    redaction: {required: false, guidance: []}
```

**network_access:** `DISALLOWED` | `ALLOW_LISTED_ONLY` | `ALLOWED`

**27 categories:** See `standards/enums/03_evidence_categories.yaml`

---

## Step 5: Quality Framework Coverage

All 18 dimensions require both `applicability` and `disposition` fields:

**Applicability** (from `standards/enums/15_quality_applicability.yaml`):
| Value | When to Use |
|-------|-------------|
| APPLIES | Dimension is relevant to this PRD |
| DOES_NOT_APPLY | Dimension not applicable (requires `exception.requested: true`, `exception.rationale`, and `exception.required_signoffs`) |

**Disposition** (from `standards/enums/16_quality_disposition.yaml`, only when APPLIES):
| Value | When to Use |
|-------|-------------|
| EXPLICIT_REQUIREMENTS | Dimension has specific REQs in this PRD - populate `coverage.requirement_ids` |
| DELEGATED_WITH_GUARDRAILS | Covered by RFC/impl - populate `delegation.guardrails` (non-empty array) |
| NOT_APPLICABLE | Same as DOES_NOT_APPLY applicability - requires exception |

**Structure:**
```yaml
- dimension_id: ACCESSIBILITY
  applicability: APPLIES
  disposition: DELEGATED_WITH_GUARDRAILS
  coverage:
    requirement_ids: []        # Populate for EXPLICIT_REQUIREMENTS
    evidence_ids: []
  delegation:
    guardrails:                # Populate for DELEGATED_WITH_GUARDRAILS
      - "Guardrail statement describing constraint"
    required_evidence_categories: []
  exception:
    requested: false           # Set true for DOES_NOT_APPLY
    rationale: ''              # Required if requested=true
    required_signoffs: []      # Required if requested=true (min 1 authority)
```

---

## Step 6: Pre-submission Validation

```bash
# YAML validity
for f in documents/prds/{PRD_ID}/*.yaml documents/prds/{PRD_ID}/*/*.yaml; do
  python3 -c "import yaml; yaml.safe_load(open('$f'))" || echo "FAIL: $f"
done

# No placeholders
grep -rn "TBD\|TODO\|FIXME\|???" documents/prds/{PRD_ID}/ && echo "FAIL: Placeholders"

# No tabs
grep -rn $'\t' documents/prds/{PRD_ID}/ && echo "FAIL: Tabs"

# Quality dimensions count
[ $(grep -c "dimension_id:" documents/prds/{PRD_ID}/10_quality_framework.yaml) -eq 18 ] || echo "FAIL: Not 18 dimensions"
```

---

## Step 7: Four-Pass Review

After drafting, review the PRD in four passes before submission. Each pass has a distinct focus.

### Pass 1: Accuracy, Structure, Conformance

| Focus | Questions |
|-------|-----------|
| Schema conformance | Do all files match their schemas? Are required fields present? |
| Enum values | Are all categories, network_access, applicability, disposition values valid? |
| ID formats | Do all IDs match canonical patterns (PRD-XXXX, REQ-XXXX, EVID-XXXX)? |
| Counts | Are there exactly 18 quality dimensions? Do file counts match expectations? |
| References | Do all cross-references resolve? No broken links? |
| Lint rules | Would all LINT-0001 through LINT-0203 pass? |

**Fix all structural defects before proceeding.**

### Pass 2: Concision

| Focus | Questions |
|-------|-----------|
| Redundancy | Is anything said twice? Consolidate or remove. |
| Verbosity | Can statements be shortened without losing meaning? |
| Templates | Are examples minimal? One good example beats three mediocre ones. |
| Unused content | Are there sections that add no value? Remove them. |

**Target: Every sentence earns its place.**

### Pass 3: Clarity and Correctness

| Focus | Questions |
|-------|-----------|
| Ambiguity | Could any requirement be interpreted multiple ways? Fix it. |
| Testability | Can each acceptance criterion be objectively verified? |
| Completeness | Are there gaps in the requirement chain? Missing evidence? |
| Consistency | Do requirements contradict each other? |
| Sequencing | Is the order of operations clear for implementers? |

**Target: An implementer can understand exactly what to build.**

### Pass 4: Organization and Polish

| Focus | Questions |
|-------|-----------|
| File placement | Are all files in the correct directories? |
| Naming | Do file names follow conventions? |
| Ordering | Are lists alphabetized or logically ordered? |
| Navigation | Can someone find what they need quickly? |
| Cross-references | Are internal links using consistent formats? |

**Target: A reviewer can navigate the PRD effortlessly.**

---

## Submission Checklist

| Check | Lint Rule |
|-------|-----------|
| YAML parses, no tabs | LINT-0001 |
| Single root key per file | LINT-0002 |
| IDs match canonical format | LINT-0003 |
| All cross-references resolve | LINT-0004 |
| No placeholders (TBD/TODO/FIXME/???) | LINT-0005 |
| Each REQ has acceptance criteria + evidence_ids | LINT-0007 |
| Each EVID has required fields + network_access | LINT-0008 |
| All 18 quality dimensions addressed | LINT-0009 |
| ID lists sorted, no duplicates | LINT-0101, LINT-0103 |
