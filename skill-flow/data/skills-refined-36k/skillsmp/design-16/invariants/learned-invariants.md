# Learned Invariants

Automatically captured learnings from Ralph executions, promoted from project-local to global scope.

---

## Invariants

<!-- New invariants are appended below this line -->

### INV-L001: Route Coverage

**Source:** SA Assistant / PRP-2026-01-22-001
**Date:** 2026-01-23

**Rule:** Every internal link (`href`) in UI components must have a corresponding route handler.

**Context:** When building SPAs with client-side routing (Dash, React Router, etc.), components often include links to other pages. If the route handler doesn't exist, users see "Page not found".

**Example:**
- Component has `dcc.Link(href="/account/Providence")`
- Router must handle `/account/{name}` pattern
- Test must verify the link actually navigates successfully

**Validation:**
1. Extract all `href=` values from components (excluding external URLs)
2. Verify each has a matching route in the router/callback
3. Playwright click test: click link → verify page loads (not "Page not found")

**PRP Integration:** Final gate must include route coverage check - all internal hrefs tested.

---

### INV-L002: Filter Logic Must Handle Edge Cases

**Source:** SA Assistant / PRP-2026-01-22-001
**Date:** 2026-01-23

**Rule:** Date/time filters must explicitly handle negative values and lifecycle states.

**Context:** When filtering by "days until X", negative values (past dates) satisfy `<= N` comparisons. When filtering active items, closed/completed items must be explicitly excluded.

**Anti-patterns:**
```python
# BAD: Negative days pass the filter
soon_closing = [uc for uc in usecases if uc.get('days_until_close') <= 14]

# BAD: Includes completed items
active_items = [x for x in items if x.get('priority') == 'high']
```

**Correct patterns:**
```python
# GOOD: Require positive days (future) AND active stage
soon_closing = [
    uc for uc in usecases
    if uc.get('stage') in ACTIVE_STAGES
    and 0 < uc.get('days_until_close', 999) <= 14
]
```

**Validation:**
1. Test with items that have past dates (negative days)
2. Test with items in terminal states (closed, live, cancelled)
3. Verify filter excludes both

**PRP Integration:** PRPs must define explicit lifecycle stages and which are "active" vs "terminal".

---

### INV-L003: Implementation Artifacts Must Exist Before Testing

**Source:** SA Intelligence Databricks Migration / J-002, J-004
**Date:** 2026-01-24

**Rule:** Every script/file referenced in `ralph-state.json` must physically exist before the step is marked as "in_progress".

**Context:** During Ralph execution for J-002 and J-004, the state file referenced Python scripts (`03-file-matcher.py`, `03-query-router.py`) that didn't exist. This caused test failures with `ModuleNotFoundError`. The root cause: `/design implement` generated shell scripts that *would create* files, but those shells were never executed, leaving phantom references.

**Anti-patterns:**
```json
// BAD: ralph-state.json references non-existent file
{
  "step": 3,
  "script": "03-file-matcher.py",  // ← File doesn't exist!
  "status": "pending"
}
```

**Correct Pattern:**
```bash
# GOOD: Preflight check before marking step in_progress
if [ ! -f "$SCRIPT" ]; then
    echo "ERROR: Script not found: $SCRIPT"
    echo "Run ./generate-missing.sh or create manually"
    exit 1
fi
./update-state.sh $STEP in_progress
```

**Validation:**
1. After `/design implement`, run artifact existence check
2. Before each Ralph step, verify script file exists
3. Block progress if artifact missing

**PRP Integration:** PRPs must include "Preflight Artifact Check" as Gate 0 before any implementation step.

---

### INV-L004: Test Paths Must Resolve to Deployed Artifacts

**Source:** SA Intelligence Databricks Migration / J-002, J-003, J-004, J-005
**Date:** 2026-01-24

**Rule:** Test files must import from the actual deployment location, not hypothetical paths.

**Context:** Test files were written with imports like `from csv_parser import ...` but the actual module was deployed to `sa-intel-app/backend/services/csv_parser.py`. The path resolution failed because tests weren't configured to find the deployed location.

**Anti-patterns:**
```python
# BAD: Assumes module is in same directory or PYTHONPATH
from csv_parser import parse_metadata_csv

# BAD: Relative path that doesn't account for test file location  
sys.path.insert(0, "../")
```

**Correct Pattern:**
```python
# GOOD: Compute path relative to test file location
BACKEND_PATH = Path(__file__).parent.parent.parent.parent.parent.parent / "sa-intel-app" / "backend"
sys.path.insert(0, str(BACKEND_PATH))
from services.csv_parser import parse_metadata_csv
```

**Validation:**
1. Test must specify absolute path resolution
2. Verify imported module path matches deployment path
3. Test import in isolation before running test suite

**PRP Integration:** PRPs must specify deployment paths and test import patterns explicitly.

---

### INV-L005: PRP → Script → Test Traceability Must Be Verified

**Source:** SA Intelligence Databricks Migration / All Journeys
**Date:** 2026-01-24

**Rule:** Every step in a PRP must have: (1) implementation script that exists, (2) test file that exists, (3) test that verifies implementation exists.

**Context:** Validation checked PRP structure and test *content*, but not whether the referenced files actually existed on disk. This allowed PRPs to pass validation while implementation artifacts were missing.

**Traceability Chain:**
```
PRP Phase X → ralph-state.json step X → 0X-script.py → tests/test_0X.py
     ↓              ↓                        ↓                ↓
  [exists?]      [exists?]              [exists?]        [imports work?]
```

**Validation Command:**
```bash
# verify-ralph-artifacts.sh
for step in $(jq -r '.steps[].script' ralph-state.json); do
    if [ ! -f "$step" ]; then
        echo "MISSING: $step"
        exit 1
    fi
done
for test in $(jq -r '.steps[].test' ralph-state.json); do
    if [ ! -f "tests/$test" ]; then
        echo "MISSING: tests/$test"
        exit 1
    fi
done
echo "All artifacts verified"
```

**PRP Integration:** 
- After PRP generation, run artifact verification
- Add "Artifact Verification Gate" as mandatory Phase 0
- Block implementation if any artifact missing

---

### INV-L006: Ralph-Check Must Run Before Execution

**Source:** SA Intelligence Databricks Migration / J-007, J-008, J-009
**Date:** 2026-01-24

**Rule:** After `/design implement` generates Ralph steps, `/design ralph-check` MUST run before execution to verify steps match PRP contract.

**Context:** Ralph steps can drift from PRP during generation. Common issues:
- Hash algorithm differs (md5 vs sha256)
- Field names slightly different
- Response schema doesn't match PRP exactly
- Route paths have subtle differences

Without ralph-check, these mismatches cause runtime failures or silent data corruption.

**What Ralph-Check Verifies:**
1. **Route Coverage:** Every PRP route exists in steps
2. **Field Compliance:** Response models match PRP schema
3. **Schema Verbatim:** SQL/code matches PRP appendix exactly
4. **Success Criteria:** Every SC-* has test coverage

**Workflow:**
```
/design implement → /design ralph-check → [FIX issues] → /design run
```

**Validation:**
1. Ralph-check status stored in `ralph-state.json`
2. Execution blocked if status != "COMPLIANT"
3. Fixes must be applied before proceeding

**PRP Integration:** This is now a **required step** in the design-ops workflow, not optional.

---

### INV-L007: Tests-First, Implementation-Emergent (TDD for Ralph)

**Source:** SA Intelligence Databricks Migration / J-007, J-008, J-009 Retrospective
**Date:** 2026-01-24

**Rule:** Ralph steps should generate **only tests**, not implementations. The AI coding agent writes code to pass tests.

**Context:** Generating full implementation code in step scripts wastes ~70% of tokens. The code is written once in the step, then copied to the target file, then verified by tests. This is redundant. Instead:

1. PRPs define acceptance criteria (SC-*)
2. `/design implement` generates **test files only**
3. AI coding agent writes implementation to pass tests
4. Tests verify correctness

**Old Flow (Token-Heavy):**
```
PRP → step-01.py (contains code) → test-01.py (checks code exists)
      ↓ tokens wasted ↓
```

**New Flow (TDD):**
```
PRP → test-01.py (acceptance criteria) → AI writes code → test passes
```

**Test Requirements (Critical):**
Since tests are now the sole contract, they must be:
1. **Complete**: Every SC-* has corresponding test assertions
2. **Correct**: Tests verify behavior, not just file existence
3. **Executable**: `pytest test-*.py` runs without syntax errors
4. **Integrated**: Tests share fixtures and can run as a suite

**Validation Gates:**
1. **Test Syntax Check**: `python -m py_compile test-*.py`
2. **Test Coverage Mapping**: Every SC-* traced to test function
3. **Test Dry Run**: `pytest --collect-only` succeeds
4. **Integration Check**: All tests run together without conflicts

**PRP Integration:** 
- `/design implement` now generates tests only
- New step: `/design test-validate` before execution
- AI implementation phase replaces step execution

---

### INV-L008: Test Contract Completeness

**Source:** SA Intelligence Databricks Migration
**Date:** 2026-01-24

**Rule:** Every Success Criterion (SC-*) in a PRP must have a traceable test assertion.

**Context:** When tests are the sole contract, missing test coverage = missing requirements. Unlike implementation code which can be inspected, untested requirements are invisible.

**Required Mapping:**
```
SC-1: GET /api/forecast returns {week, use_cases[], snapshots[]}
  → test_forecast_response_structure()
  → assert "week" in response
  → assert isinstance(response["use_cases"], list)
  → assert isinstance(response["snapshots"], list)
```

**Validation:**
```python
# In test file header:
"""
PRP: PRP-F-007
Success Criteria Coverage:
  SC-1 → test_forecast_response_structure [lines 45-60]
  SC-2 → test_forecast_save [lines 62-80]
  SC-3 → test_forecast_compare [lines 82-100]
"""
```

**PRP Integration:** `/design test-validate` checks this mapping exists and is complete.

---

### INV-L009: Integration Test Suite Required

**Source:** SA Intelligence Databricks Migration
**Date:** 2026-01-24

**Rule:** After all unit tests pass, an integration test must verify the system works end-to-end.

**Context:** Individual tests passing doesn't guarantee the system works together. API endpoints may pass unit tests but fail when called in sequence.

**Integration Test Template:**
```python
# tests/integration/test_full_workflow.py

def test_forecast_workflow():
    """SC-1 through SC-5: Full forecast cycle."""
    # 1. Get current forecast (SC-1)
    response = client.get("/api/forecast")
    assert response.status_code == 200
    
    # 2. Record prediction (SC-2)
    response = client.post("/api/forecast", json={...})
    assert response.json()["status"] == "saved"
    
    # 3. Compare weeks (SC-3)
    response = client.get("/api/forecast/compare")
    assert "comparisons" in response.json()
    
    # 4. View history (SC-4)
    response = client.get("/api/forecast/history/uc_001")
    assert len(response.json()["snapshots"]) <= 52
    
    # 5. Resolve (SC-5)
    response = client.post("/api/forecast/resolve/uc_001", json={"outcome": "won"})
    assert response.status_code == 200
```

**PRP Integration:** Gate scripts must include integration tests, not just unit tests.

---

### INV-L010: Dependencies Must Have Deliverables

**Source:** SA Intelligence Databricks Migration / J-010 Gap Audit
**Date:** 2026-01-24

**Rule:** Every dependency marked as "TODO" or "⏳" in a Journey/Spec must have a corresponding deliverable in the PRP with a test.

**Context:** During J-010 development, several dependencies were documented in the Journey (Vector Search index, pending_stakeholders table, spaCy install) but were either:
1. Mentioned but not converted to PRP deliverables
2. Assumed to exist from other journeys but never created
3. Dismissed as "will be covered in F3.2" without explicit tracking

This led to gaps that were only caught by manual user review.

**Validation Procedure:**
```bash
# Extract TODO/⏳ items from journey
grep -E "⏳|TODO" journey.md | grep -oE "[a-z_]+" 

# Check each appears as a deliverable in PRP
for item in $items; do
  grep -l "$item" prp.md || echo "MISSING: $item"
done
```

**PRP Integration:**
1. During `/design prp` generation, extract all `⏳|TODO` items from journey
2. Verify each has a corresponding `F*.N` deliverable
3. Block PRP completion if any are missing

---

### INV-L011: Table References Must Trace to CREATE

**Source:** SA Intelligence Databricks Migration / J-010 Gap Audit
**Date:** 2026-01-24

**Rule:** Every Delta table referenced in a spec (e.g., `INSERT INTO table_x`) must have a traceable `CREATE TABLE` statement in either the same PRP or a blocking dependency PRP.

**Context:** The `pending_stakeholders` table was referenced in J-010 as `INSERT INTO pending_stakeholders` but no PRP contained its `CREATE TABLE` statement. The spec assumed "existing flow" but the flow never existed.

**Validation:**
```python
# Find all table references
table_refs = re.findall(r'(INSERT INTO|FROM|UPDATE|DELETE FROM)\s+(\w+\.?\w+\.?\w+)', spec_text)

# Check each has CREATE
for table in tables:
    assert f"CREATE TABLE.*{table}" in any_prp, f"Missing CREATE for {table}"
```

**PRP Integration:** `/design ralph-check` should verify table lineage before execution.

---

### INV-L012: Retroactive Documentation Required for Code-First Work

**Source:** SA Intelligence Databricks Migration / J-011 (Lakebase Chat State)
**Date:** 2026-01-25

**Rule:** When implementation happens before design-ops (urgent fixes, exploration, prototyping), retroactive documentation must be created to maintain traceability.

**Context:** During Lakebase chat state implementation, the work was done pragmatically before creating Journey/Spec/PRP. This violates the design-ops workflow but is sometimes necessary for speed. The key is to document retroactively.

**Required Retroactive Artifacts:**

1. **Journey** - Document what was built, who it serves, success metrics
2. **Spec** - Define FRs/NFRs based on implemented behavior
3. **PRP** - Map code to deliverables with success criteria
4. **Lessons Learned** - Capture SDK quirks, gotchas, deviations
5. **Technical Debt** - Mark missing tests explicitly

**Template for Retroactive Journey:**
```markdown
# J-XXX: [Feature Name]

**Status**: IMPLEMENTED (Retroactive Documentation)
**Implementation Date**: YYYY-MM-DD

## What Was Built
[Summary of implementation]

## Lessons Learned
1. [SDK quirk 1]
2. [Configuration gotcha]

## Technical Debt
- [ ] Unit tests not created
- [ ] Integration tests not created

## Invariant Violations (Self-Audit)
| Invariant | Status | Notes |
|-----------|--------|-------|
| INV-01 | ✅/⚠️/❌ | [notes] |
```

**Validation:** 
1. Code-first work MUST have retroactive docs within same session
2. "IMPLEMENTED" status clearly marked
3. Technical debt itemized for future work

**PRP Integration:** This is an escape valve, not a default. Track code-first occurrences for process improvement.

---

### INV-L013: No Hallucinated Links

**Source:** SA Intelligence Databricks Migration / J-009 Newsletter Curation
**Date:** 2026-01-25

**Rule:** URLs must be extracted from source documents, NEVER generated by LLM.

**Context:** When curating newsletters, links to documentation, blogs, and case studies must come from the canonical source (PDF/HTML). LLMs are prone to hallucinating URLs that look plausible but lead to 404s or, worse, malicious destinations.

**Enforcement Points:**

1. **Parser extracts links verbatim:**
   ```python
   # GOOD: Extract href from DOM
   link = anchor_tag.get('href')
   
   # BAD: LLM generates URL
   link = llm_response['url']  # NEVER
   ```

2. **LLM prompts explicitly exclude links:**
   ```
   Rules:
   - Do NOT generate any URLs or links
   - Keep output to description only
   ```

3. **Output templates use passthrough:**
   ```html
   <a href="{source.link}">{title}</a>  <!-- link from parser -->
   <p>{llm_description}</p>              <!-- description from LLM -->
   ```

4. **Pre-send validation:**
   ```sql
   -- Every link in output must exist in source
   SELECT COUNT(*) FROM newsletter_output o
   WHERE o.link NOT IN (SELECT link FROM newsletter_source);
   -- Expected: 0
   ```

**Validation Checklist:**
- [ ] LLM prompts contain "Do NOT generate URLs"
- [ ] Parser tests verify link extraction accuracy
- [ ] Output HTML links traced to `newsletter_source.link`
- [ ] No `llm.generate(url=...)` patterns in code

**PRP Integration:** 
- FR for parsing MUST include link extraction test
- FR for LLM MUST include "no URL in output" assertion
- Final gate MUST include link provenance check

---

## INV-L014: Err Toward Action Items
**Added:** 2026-01-25  
**Context:** Signal extraction classification

When classifying extracted signals from transcripts:
- If ambiguous between `identify_next_step` and another type, choose `identify_next_step`
- Missing an action item has higher cost than misclassifying
- "We will research X" = next_step, NOT technical_win
- Any commitment, task, or follow-up = next_step

## INV-L015: LLM Description Quality

**Pattern**: Generic LLM descriptions like "X is a feature. It matters for Y."

**Root Cause**: Vague prompts that don't enforce specificity

**Solution**: Prompt engineering with:
1. BAD/GOOD examples
2. Explicit "Do NOT" rules
3. Required metrics (30%, 2x faster, etc.)
4. Rejection of generic phrases

**Example Prompt**:
```
STRICT RULES:
- Do NOT just repeat the feature name
- Do NOT say "It matters for..." 
- Be specific about capabilities (2x faster, 10 regions)

BAD: "X is a model. It matters for healthcare."
GOOD: "X delivers 50% faster inference with improved reasoning."
```

**Added**: 2026-01-25
